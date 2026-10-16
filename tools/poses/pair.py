#!/usr/bin/env python3
"""Pair every distinct pose (data/poses.json) with the closest character
cutout (tools/poses/characters.json) and write the generation kit:

  design/models/v4/<pose>/mannequin.png   pose guide (tools/poses/render.py)
  design/models/v4/<pose>/character.jpg   closest drawn character
  design/models/v4/<pose>/pair.jpg        both side by side, for review
  design/models/v4/<pose>/prompt.txt      prompt for the image model
  design/models/v4/manifest.json          all of the above, plus uses
  design/models/v4/_pairs-<stance>.jpg    review sheets per stance

Usage: python3 tools/poses/pair.py
"""
import json, os, shutil
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V4 = os.path.join(ROOT, "design/models/v4")
CH = os.path.join(V4, "characters")

ARM = {
    "chamber": "fist chambered palm-up on the belt at the hip, elbow back",
    "guard": "fist held up in front of the chest as a guard",
    "junbi": "fist in front of the lower belly (ready position)",
    "tongmil": "both palms pushing slowly forward at chest height, fingertips up (pushing-hands ready)",
    "cover": "covered fist: one fist wrapped in the other hand in front of the face",
    "low": "low block: forearm sweeping down, fist above the front knee",
    "inside": "inside block: forearm vertical in front of the chest, fist at shoulder height",
    "outer": "outside block: forearm vertical at the outer edge of the body, fist at shoulder height",
    "high": "high block: forearm above the forehead, angled up",
    "houter": "high outside block: forearm vertical beside the head",
    "wedge": "wedge block: forearm up and out, fist at head height",
    "spread": "fist out to the side and down (low spread)",
    "xlow": "low X block: wrists crossed low in front",
    "ksout": "single knife-hand outside block, open hand",
    "ksblock": "knife-hand block in front, open hand edge forward",
    "ksguard": "open hand palm-up across the solar plexus (guarding hand)",
    "ksin": "knife-hand inside block, open hand",
    "kslow": "low knife-hand block, open hand",
    "ksside": "knife-hand side block, arm out to the side",
    "kspread": "open hand out to the side (knife-hand spread)",
    "khigh": "knife-hand high block above the forehead",
    "twist": "twisted knife-hand high block",
    "palm": "palm inside block, open hand",
    "palmlow": "open palm low, supporting",
    "pressdown": "palm pressing down in front of the belly",
    "punch": "middle punch: arm straight forward, fist at solar-plexus height",
    "hpunch": "high punch: arm straight forward, fist at face height",
    "sidepunch": "punch straight out to the side",
    "crosspunch": "punch across the body into the open target hand",
    "target": "open hand held out as a target",
    "uppercut": "uppercut: forearm rising, fist at chin height",
    "backfist": "back-fist strike at face height",
    "hammer": "hammer-fist strike",
    "hammerlow": "low hammer-fist strike",
    "hammerout": "hammer-fist strike out to the side",
    "neck": "knife-hand strike to neck height, palm up",
    "ksstrike": "knife-hand outside strike",
    "spear": "spear-hand thrust forward, fingertips first",
    "press": "open hand palm-down under the other elbow",
    "lspear": "low spear hand, palm up",
    "shoulder": "fist pulled back to the shoulder",
    "palmjaw": "palm-heel strike up at jaw height",
    "arc": "arc hand (thumb and fingers spread) at throat height",
    "elbow": "elbow strike forward at face height",
    "eltarget": "open hand held as a target in front of the face",
    "sideelbow": "elbow strike out to the side",
    "elbowpush": "fist pushing the other fist to drive the elbow",
    "hingepunch": "punch with the other fist braced under the elbow (hinge)",
    "hingetop": "fist above, braced (small hinge)",
    "hold": "hand holding, pulling back",
    "kneebreak": "pulling hand down for a knee break",
    "assist": "supporting fist under the blocking arm",
    "grab": "open hand reaching forward to grab",
    "tgrab": "twisting grab, hand turned over",
}
VIEW = {
    "front": "seen from the front, facing the viewer",
    "back": "seen from behind (back of the head and back of the dobok; the belt knot is hidden in front)",
}


def view_text(p):
    if p["view"] == "side":
        return f"seen exactly side-on (profile), facing the {'right' if p['face'] == 'R' else 'left'} edge of the image"
    return VIEW[p["view"]]


def load_forms():
    out = {}
    for f in os.listdir(os.path.join(ROOT, "forms")):
        if f.endswith(".json"):
            d = json.load(open(os.path.join(ROOT, "forms", f)))
            out[d.get("slug", f[:-5])] = out[f[:-5]] = {m["id"]: m for m in d["moves"]}
    return out


RELATED = [{"ready", "close", "walk"}, {"walk", "front"}, {"kick", "knee", "crane"},
           {"skick", "rkick"}, {"back", "tiger"}, {"horse", "back"}]


def score(p, c):
    s = 0
    if c["stance"] == p["stance"]:
        s += 10
    elif any(p["stance"] in g and c["stance"] in g for g in RELATED):
        s += 4
    if c["view"] == p["view"]:
        s += 5
        if p["view"] == "side" and c.get("face") == p.get("face"):
            s += 1
    return s - (1.5 if c["tier"] == 2 else 6 if c["tier"] == 3 else 0)


def main():
    T = json.load(open(os.path.join(ROOT, "data/techniques.json")))
    poses = json.load(open(os.path.join(ROOT, "data/poses.json")))["poses"]
    chars = {k: v for k, v in json.load(open(os.path.join(ROOT, "tools/poses/characters.json")))["figures"].items()
             if v.get("stance")}
    forms = load_forms()
    manifest, sheets = [], {}
    for p in poses:
        best = max(chars, key=lambda k: (score(p, chars[k]), k.startswith("d10"), k.startswith("ms")))
        c = chars[best]
        d = os.path.join(V4, p["id"])
        Image.open(os.path.join(CH, best + ".png")).convert("RGB").save(os.path.join(d, "character.jpg"), quality=92)
        # what the move is called
        f, mid = (p["uses"] or p["mirror_of_uses"])[0].split("#")
        mv = forms[f][mid]
        tech = T["techniques"].get(mv.get("tech"), {})
        st = T["stances"][p["stance"]]
        if "see" in st:
            st = T["techniques"][st["see"]]
        lead = {"L": "left", "R": "right"}.get(p["lead"], "")
        if p["stance"] in ("kick", "skick", "rkick", "knee"):
            legs = f"{st['name']} ({st['en'].lower()}) with the {lead} leg"
        elif p["stance"] == "crane":
            legs = f"{st['name']} ({st['en'].lower()}) standing on the {lead} leg"
        elif p["stance"] in ("ready", "close"):
            legs = f"{st['name']} ({st['en'].lower()})"
        else:
            legs = f"{st['name']} ({st['en'].lower()}) with the {lead} foot forward"
        arms = f"left hand: {ARM[p['arms']['L']]}; right hand: {ARM[p['arms']['R']]}"
        what = f"{tech.get('name', '')} ({tech.get('en', '').lower()})" if tech else ""
        prompt = (
            "Image 1 is a pose guide (a coloured 3D mannequin); image 2 is the character and drawing style.\n"
            "Draw the character from image 2 in exactly the pose, camera angle and foot placement of image 1: "
            "same joint angles, same feet, same view. Ignore the mannequin's colours and shapes; "
            "on the mannequin the LEFT limbs are blue and the RIGHT limbs are orange, the small cone on the head is the nose.\n"
            f"Pose: {legs}" + (f", {what}" if what else "") + f"; {arms}.\n"
            f"View: {view_text(p)}.\n"
            "Style: realistic adult taekwondo practitioner in a white dobok with black collar and black belt, "
            "faceless head, fine black ink line drawing with light cross-contour shading, bare feet with the toes visible. "
            "Single figure, full body, plain white background, no ground shadow, no text, no labels."
        )
        open(os.path.join(d, "prompt.txt"), "w").write(prompt + "\n")
        # review pair
        m = Image.open(os.path.join(d, "mannequin.png")).convert("RGB")
        ch = Image.open(os.path.join(CH, best + ".png")).convert("RGB")
        H = 720
        m = m.resize((round(m.width * H / m.height), H))
        ch.thumbnail((520, H))
        pair = Image.new("RGB", (m.width + 560, H + 40), "white")
        pair.paste(m, (0, 0))
        pair.paste(ch, (m.width + 20 + (520 - ch.width) // 2, H - ch.height))
        dr = ImageDraw.Draw(pair)
        dr.text((8, H + 12), p["id"], fill="black")
        dr.text((m.width + 20, H + 12), f"{best}  ({c['stance']} {c['view']}{' ' + c.get('face', '') if c['view'] == 'side' else ''})", fill="black")
        pair.save(os.path.join(d, "pair.jpg"), quality=85)
        sheets.setdefault(p["stance"], []).append(pair)
        manifest.append({
            "id": p["id"], "stance": p["stance"], "view": p["view"], "face": p["face"], "lead": p["lead"],
            "arms": p["arms"], "mannequin": f"{p['id']}/mannequin.png", "character": f"characters/{best}.png",
            "character_match": "exact" if (c["stance"], c["view"]) == (p["stance"], p["view"]) else "closest",
            "prompt": prompt, "uses": p["uses"], "mirror_of_uses": p["mirror_of_uses"],
            "figures": len(p["uses"]),
        })
    json.dump({"note": "Generation kit, one entry per distinct pose (mirrors reused). Feed image 1 = mannequin, image 2 = character, plus the prompt. Made by tools/poses/pair.py.",
               "count": len(manifest), "poses": manifest},
              open(os.path.join(V4, "manifest.json"), "w"), indent=1, ensure_ascii=False)
    for st, ims in sheets.items():
        cols = 3
        w, h = max(i.width for i in ims), max(i.height for i in ims)
        rows = (len(ims) + cols - 1) // cols
        sh = Image.new("RGB", (cols * w, rows * h), "white")
        for i, im in enumerate(ims):
            sh.paste(im, ((i % cols) * w, (i // cols) * h))
        sh.thumbnail((2400, 2400 * 4))
        sh.save(os.path.join(V4, f"_pairs-{st}.jpg"), quality=80)
    ex = sum(1 for e in manifest if e["character_match"] == "exact")
    print(f"{len(manifest)} poses paired; {ex} with a same-stance same-view character, {len(manifest) - ex} closest")


if __name__ == "__main__":
    main()
