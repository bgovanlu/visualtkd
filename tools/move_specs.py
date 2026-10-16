"""Write the per-move image brief for a form: one image per count, for the figure image pipeline (#7).

usage:
  python3 tools/move_specs.py forms/taegeuk-1.json      # one form
  python3 tools/move_specs.py --all                     # every built form

Writes design/moves/<form>/SPEC.md (a prompt per count, ready to paste) and spec.json (the same, as data).
The generated images go next to them as design/moves/<form>/<id>.png; tools/figures.py turns them into
the page figures. Pose words come from the move data, so a change to forms/*.json changes the brief.
"""
import json, os, sys
import sitekit as S
from sitekit import ROOT

CHARACTER = ("Same character and drawing style as the reference image: realistic anatomical ink figure drawing, fine line, "
             "light cross-contour shading, plain white background; adult, 7.5 heads tall; faceless head with short dark hair; "
             "white dobok with black V-collar; black belt with knot and tails; bare feet.")
FRAME = ("ONE figure only, full body, 2:3 portrait, the whole figure inside the frame with a margin all round (kicking foot and "
         "raised hands included), soles resting on a faint floor line near the bottom edge. No text, no labels, no numbers, "
         "no footprint diagram, no logos.")

STANCE = {
    "ready": "naranhi seogi (parallel stance): feet parallel, one foot-width apart, legs straight",
    "close": "moa seogi (closed stance): feet together, inside edges touching, legs straight",
    "walk": "ap seogi (walking stance): one natural walking step, both legs straight, front foot pointing forward, rear foot turned out slightly, hips square",
    "front": "ap kubi (front stance): long stance about 1.5 shoulder widths, front knee bent over the toes with the shin vertical, rear leg locked straight, rear heel flat and rear foot turned out about 30 degrees, hips and chest square to the front, torso upright",
    "back": "dwit kubi (back stance): front foot points forward, rear foot turned 90 degrees out, heels on one line in an L, about 70 percent of the weight on the deeply bent rear leg with the rear knee pushed out over the rear toes, front knee slightly bent, hips and chest turned sideways",
    "tiger": "beom seogi (tiger stance): short stance, front foot light with only the ball touching the floor, nearly all the weight on the bent rear leg, both knees bent",
    "horse": "juchum seogi (horse-riding stance): feet parallel about two shoulder widths apart, knees bent deeply and pushed outward over the toes, back straight",
    "cross": "kkoa seogi (cross stance): the rear foot crossed close behind the front foot, rear knee tucked behind the front knee, both knees bent, weight on the front foot",
    "crane": "hakdari seogi (crane stance): standing on one bent leg, the other foot lifted with its sole against the inside of the standing knee",
    "kick": "ap chagi (front kick): standing leg straight, the kicking leg extended forward at chest height striking with the ball of the foot, toes pulled back",
    "skick": "yeop chagi (side kick): body leaning away, the kicking leg extended straight out to the side at chest height, striking with the foot blade (outer edge of the foot)",
    "rkick": "dollyeo chagi (roundhouse kick): the hip turned over, the kicking leg swung round at head height striking with the instep",
    "knee": "mureup chigi (knee strike): standing leg straight, the other knee driven sharply up to chest height",
}
# what one hand does: end position, in plain words (the other hand is described separately)
ARM = {
    "chamber": "fist chambered palm-up on top of the belt at the side of the waist, elbow drawn back",
    "junbi": "fist in front of the belt, a fist-width from the body, both fists at the same height",
    "low": "low block (arae makki): arm extended straight down and forward over the front thigh, fist a fist-width above the knee",
    "punch": "middle punch (momtong jireugi): arm fully extended straight forward at solar-plexus height, fist palm-down",
    "hpunch": "high punch (eolgul jireugi): arm fully extended straight forward at face height, fist palm-down",
    "inside": "inside middle block (momtong an makki): forearm upright in front of the chest, elbow bent about 90 degrees, fist at shoulder height on the centre line, palm toward the body",
    "outer": "outer middle block (momtong bakkat makki): forearm upright at the side of the body at shoulder level, fist at shoulder height, palm forward",
    "high": "high block (eolgul makki): forearm held across and a fist-width above the forehead, angled slightly upward",
    "backfist": "back-fist strike (deungjumeok ap chigi): arm arcs up and forward, back of the fist striking at face height, elbow slightly bent",
    "guard": "fist raised in front of the chest in a guard (kick guard)",
    "ksout": "single knife-hand outer block (hansonnal bakkat makki): open hand, forearm upright at the side at shoulder height, knife edge outward",
    "ksblock": "knife-hand block (sonnal makki): open hand, forearm upright at shoulder height in front of the lead shoulder, knife edge forward",
    "ksguard": "guarding open hand palm-up across the solar plexus, below the blocking arm",
    "spear": "spear-hand thrust (pyeonsonkkeut sewo tzireugi): open hand, fingers straight, thrust forward at solar-plexus height with the palm facing sideways",
    "press": "open hand palm-down under the elbow of the thrusting arm, pressing",
    "neck": "knife-hand neck strike (sonnal mok chigi): open hand swung horizontally inward, palm up, knife edge at neck height",
    "khigh": "knife-hand high block (sonnal eolgul makki): open hand held across and above the forehead, knife edge up",
    "twist": "twisted knife-hand high block (sonnal biteureo makki): open hand raised in front of the face, palm turned outward",
    "palm": "palm inside block (batangson an makki): open hand, heel of the palm sweeping in front of the chest to the centre line",
    "kslow": "low knife-hand block (sonnal arae makki): open hand extended down over the front thigh, knife edge down",
    "ksside": "knife-hand side block (sonnal yeop makki): open hand extended straight out to the side at shoulder height",
    "eltarget": "open hand held as a target in front of the chest, palm toward the striking elbow",
    "grab": "open hand reaching forward to grab at face height, then pulling back",
    "hammer": "hammer-fist strike (me jumeok naeryeo chigi): arm swung down and forward, bottom of the fist striking at chest height",
    "elbow": "elbow strike (palkup dollyeo chigi): arm folded, elbow swung forward horizontally at chin height",
    "houter": "high outer block: forearm upright at the side of the head, fist at head height",
    "spread": "low spreading block (arae hecheo makki): arm extended down and out to the side of the hip",
    "xlow": "low X block (otgeoreo arae makki): both wrists crossed in an X in front of the lower belly, arms angled down",
    "wedge": "wedge block (hecheo makki): forearm upright at the side, both arms spreading outward at shoulder height",
    "uppercut": "uppercut (chi jireugi): fist driven upward in front of the chin, palm toward the body",
    "cover": "covering palm wrapped over the other fist in front of the chest",
    "sidepunch": "side punch (yeop jireugi): arm fully extended straight out to the side at shoulder height",
    "assist": "supporting fist placed under the elbow of the blocking arm",
    "tongmil": "pushing-hands ready (tongmilgi junbi): both open hands raised in front of the face, fingertips angled toward each other, as if pushing a rock",
    "ksstrike": "knife-hand outer strike (sonnal bakkat chigi): open hand swung outward horizontally at neck height, palm down",
    "arc": "arc-hand strike (kaljaebi): hand open in a C between thumb and fingers, thrust forward at throat height",
    "kneebreak": "open hand pulling down at knee height (knee break)",
    "hold": "open hand holding at the side of the hip, palm up",
    "target": "open hand held as a target in front of the chest, palm forward",
    "crosspunch": "punch across the body into the target hand at chest height",
    "lspear": "low spear hand: open hand thrust down and forward at groin height, palm up",
    "shoulder": "fist resting on the front of the opposite shoulder, elbow down",
    "pressdown": "palm pressing block (batangson nulleo makki): open hand pushing straight down in front of the belly, palm down",
    "sideelbow": "side elbow strike (palkup yeop chigi): arm folded, elbow driven straight out to the side at shoulder height",
    "elbowpush": "open palm pushing against the fist of the striking arm",
    "hammerlow": "hammer-fist striking down in front of the belly",
    "palmlow": "open palm held low in front of the belly as a target for the hammer-fist",
    "palmjaw": "palm-heel strike up and forward at jaw height",
    "ksin": "knife-hand inside block (sonnal an makki): open hand sweeping in front of the chest to the centre line",
    "hingepunch": "large hinge (keun dolcheogi): forearm level across the chest at shoulder height, fist at the other shoulder",
    "hingetop": "small hinge: fist held above the other fist in front of the chest",
    "hammerout": "hammer-fist outer strike: arm swung outward horizontally, bottom of the fist at shoulder height",
    "kspread": "knife-hand spreading block: open hand extended down and out to the side",
    "tgrab": "twisting grab: open hand reaching forward at chest height and twisting",
    "gyeopson": "open hand resting over the other in front of the lower belly, left over right (overlapped-hands ready)",
    "upelbow": "rising elbow strike (palkup ollyeo chigi): elbow driven up and forward to chin height, fist finishing beside the ear",
    "sidebf": "back-fist strike out to the side at face height, arm almost straight",
    "crossbf": "back-fist strike across the body to the other side at face height",
}
SIDE = {"L": "left", "R": "right"}

def view_words(m):
    if m["view"] == "front": return "FRONT view: the figure faces the viewer.", None
    if m["view"] == "back": return "BACK view: the figure faces away from the viewer, back to us.", None
    near = "R" if m["face"] == "R" else "L"
    return (f'SIDE view, in profile, facing the {SIDE[m["face"]].upper()} edge of the image '
            f'(its {SIDE[near]} side is nearest the viewer).'), near

def stance_words(m):
    st, lead = m["stance"], m.get("lead")
    w = STANCE[st]
    if st in ("kick", "skick", "rkick", "knee"): return f'{w}. Kicking leg: {SIDE[lead].upper()}.'
    if st == "crane": return f'{w}. Standing leg: {SIDE[lead].upper()}.'
    if st in ("ready", "close", "horse"): return w + "."
    return f'{w}. {SIDE[lead].upper()} foot forward.'

def hand_words(m, near):
    arms = m.get("arms") or {}
    out = []
    for s in ("R", "L"):
        code = arms.get(s, "chamber")
        tag = f' ({"near" if s == near else "far"} arm)' if near else ""
        out.append(f'{SIDE[s].upper()} hand{tag}: {ARM[code]}.')
    return " ".join(out)

def spec(F, stem):
    rows = []
    for m in F["moves"]:
        vw, near = view_words(m)
        name = S.LIB["techniques"][m["tech"]]
        prompt = " ".join([CHARACTER, FRAME, vw, "Stance: " + stance_words(m), hand_words(m, near),
                           f'This is {("count " + m["id"]) if m["id"] != "J" else "the ready posture"} of {F["title"]}: {m["desc"]}'])
        rows.append({"id": m["id"], "file": f'{m["id"]}.png', "view": m["view"], "face": m.get("face"),
                     "stance": m["stance"], "lead": m.get("lead"), "arms": m.get("arms") or {},
                     "tech": m["tech"], "name": f'{name["name"]} · {name["en"]}', "desc": m["desc"], "prompt": prompt})
    return rows

def write(path):
    F = json.load(open(path)); stem = os.path.splitext(os.path.basename(path))[0]
    d = os.path.join(ROOT, "design/moves", stem); os.makedirs(d, exist_ok=True)
    rows = spec(F, stem)
    json.dump({"form": F["title"], "slug": F["slug"], "moves": rows}, open(os.path.join(d, "spec.json"), "w"), ensure_ascii=False, indent=1)
    md = [f'# {F["title"]}: one image per count\n',
          f'Generated by `tools/move_specs.py` from `forms/{stem}.json`; do not edit by hand.\n',
          "**Save each image here** as `<id>.png` (ready = `J.png`). PNG or JPEG, 2:3 portrait, at least 1024 px tall. "
          "**Reference images:** `design/models/directions/d10-realistic-anatomical-CHOSEN.png` for the character, plus the model sheet "
          "for the stance (`design/models/ms-v2/`, or `ms-v3/` once approved).\n",
          "Draw each figure exactly as described: side views face the edge named in the prompt (the build does not mirror), "
          "and \"near arm\" is the arm closer to the viewer. Then run `python3 tools/build_form.py forms/"
          f'{stem}.json --images` to see the page with them.\n',
          "| Count | File | View | Stance | Technique |", "|---|---|---|---|---|"]
    for r in rows:
        v = r["view"] + (f' → {SIDE[r["face"]]}' if r["face"] else "")
        md.append(f'| {r["id"]} | `{r["file"]}` | {v} | {r["stance"]}{" " + r["lead"] if r["lead"] else ""} | {r["name"]} |')
    for r in rows:
        md += ["", f'## {r["id"]} · {r["name"]} → `{r["file"]}`', "```", r["prompt"], "```"]
    open(os.path.join(d, "SPEC.md"), "w").write("\n".join(md) + "\n")
    print("spec ->", os.path.relpath(d, ROOT), f"({len(rows)} images)")

if __name__ == "__main__":
    for p in (S.form_files() if "--all" in sys.argv else [a for a in sys.argv[1:] if not a.startswith("--")]):
        write(p)
