"""Turn the per-move images in design/moves/<form>/ into page figures (#7).

Each <id>.png|jpg|jpeg|webp (ready = J) is cut out (the white background outside the outline made
transparent), trimmed to the figure, scaled to a common body height and saved as <out>/fig/<id>.webp.
build_form.py --images calls this and hands the result to the page as FIGIMG; counts with no image
keep the vector figure.

Body height: a trimmed image runs from the head (or the highest hand or foot) to the soles. Low stances
are shorter than a standing figure, so each stance has a share of standing height (H below). When a
raised hand or a high kick sits above the head, or a stance needs adjusting, put the share in
design/moves/<form>/fit.json: {"14-1": 1.05}.
"""
import json, os
from PIL import Image, ImageChops, ImageDraw
from sitekit import ROOT

H = {"ready": 1, "close": 1, "walk": .99, "front": .9, "back": .88, "tiger": .9, "nieun": .9, "horse": .84, "cross": .92,
     "crane": 1, "kick": 1, "skick": .96, "rkick": 1.02, "knee": 1}
PX = 640          # stored height of a figure that fills its share (2x the largest on-screen figure)
EXT = (".png", ".jpg", ".jpeg", ".webp")

def cutout(path):
    im = Image.open(path).convert("RGB"); w, h = im.size
    work, key = im.copy(), (255, 0, 255)
    seeds = [(x, y) for x in range(0, w, 8) for y in (0, h - 1)] + [(x, y) for y in range(0, h, 8) for x in (0, w - 1)]
    for s in seeds:   # flood the background in from the border; the outline stops it
        px = work.getpixel(s)
        if px != key and min(px) > 200: ImageDraw.floodfill(work, s, key, thresh=40)
    alpha = ImageChops.difference(work, Image.new("RGB", (w, h), key)).convert("L").point(lambda v: 0 if v < 8 else 255)
    rgba = im.convert("RGBA"); rgba.putalpha(alpha)
    bot = alpha.getbbox()[3]; px = rgba.load()
    for y in range(max(0, bot - int(h * .012) - 2), bot):     # the faint floor line under the feet
        for x in range(w):
            r, g, b, a = px[x, y]
            if a and (r + g + b) / 3 > 150: px[x, y] = (255, 255, 255, 0)
    return rgba.crop(rgba.getchannel("A").getbbox())

def build(stem, F, out_dir):
    src = os.path.join(ROOT, "design/moves", stem)
    if not os.path.isdir(src): return {}
    fit = json.load(open(os.path.join(src, "fit.json"))) if os.path.exists(os.path.join(src, "fit.json")) else {}
    os.makedirs(os.path.join(out_dir, "fig"), exist_ok=True)
    found = {}
    for m in F["moves"]:
        path = next((os.path.join(src, m["id"] + e) for e in EXT if os.path.exists(os.path.join(src, m["id"] + e))), None)
        if not path: continue
        r = fit.get(m["id"], H[m["stance"]])
        c = cutout(path); hh = round(PX * r)
        c = c.resize((round(c.size[0] * hh / c.size[1]), hh), Image.LANCZOS)
        c.save(os.path.join(out_dir, "fig", m["id"] + ".webp"), "WEBP", quality=86)
        found[m["id"]] = {"src": f'fig/{m["id"]}.webp', "w": c.size[0], "h": c.size[1], "r": r}
    missing = [m["id"] for m in F["moves"] if m["id"] not in found]
    print(f"figures: {len(found)} images from design/moves/{stem}" + (f", vector for {', '.join(missing)}" if missing else ""))
    return found
