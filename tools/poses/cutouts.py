#!/usr/bin/env python3
"""Cut single figures out of the model sheets (design/models/...).

Each sheet is thresholded, dilated and split into connected components;
components that are tall enough to be a figure are kept (text labels and
captions are dropped). Each cutout is saved on a white background with a
small margin under design/models/v4/characters/<sheet>-<n>.png, and an
index sheet (_index.png) numbers them so they can be tagged in
tools/poses/characters.json.

Usage: python3 tools/poses/cutouts.py
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEETS = {
    "d10": "design/models/directions/d10-realistic-anatomical-CHOSEN.png",
    "ms1v2": "design/models/ms-v2/ms1-basic-stances-v2.png",
    "ms2v2": "design/models/ms-v2/ms2-ap-kubi-v2.png",
    "ms3v2": "design/models/ms-v2/ms3-dwit-kubi-v2.png",
    "ms4v2": "design/models/ms-v2/ms4-beom-seogi-v2.png",
    "ms5v2": "design/models/ms-v2/ms5-juchum-kkoa-v2.png",
    "ms6v2": "design/models/ms-v2/ms6-hakdari-v2.png",
    "ms7v2": "design/models/ms-v2/ms7-kicks-v2.png",
    "ms1sd45": "design/models/ms-v3/ms1-basic-stances-v3-seedream45-4K.png",
    "ms1sd5l": "design/models/ms-v3/ms1-basic-stances-v3-seedream5L-4K.png",
}
SPLIT = {"d10": (3,)}          # components that hold two touching figures
OUT = os.path.join(ROOT, "design/models/v4/characters")


def cut(key, path):
    im = Image.open(os.path.join(ROOT, path)).convert("RGB")
    scale = 1360 / im.height
    small = im.resize((round(im.width * scale), 1360), Image.LANCZOS)
    g = np.asarray(small.convert("L"), dtype=np.int16)
    ink = g < 200
    ink = ndimage.binary_dilation(ink, iterations=9)       # join limbs and belt to body
    lab, n = ndimage.label(ink)
    boxes = ndimage.find_objects(lab)
    found = []
    for i, sl in enumerate(boxes):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if h < 0.17 * small.height or w < 25:                # captions, labels, rules
            continue
        if w > 0.6 * small.width:                            # frame lines
            continue
        found.append((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop, i + 1))
    found.sort(key=lambda b: (round(b[1] / 150), b[0]))     # rows, then left to right
    # two figures touching (d10 back view + ap kubi): split at the emptiest column
    split = []
    for n, (x0, y0, x1, y1, li) in enumerate(found, 1):
        if n in SPLIT.get(key, ()):
            cols = (lab[y0:y1, x0:x1] == li).sum(0)
            a, b = int(.3 * len(cols)), int(.7 * len(cols))
            m = x0 + a + int(np.argmin(cols[a:b]))
            split += [(x0, y0, m, y1, li), (m, y0, x1, y1, li)]
        else:
            split.append((x0, y0, x1, y1, li))
    found = split
    res = []
    for k, (x0, y0, x1, y1, li) in enumerate(found, 1):
        mask = (lab[y0:y1, x0:x1] == li)
        crop = np.asarray(small)[y0:y1, x0:x1].copy()
        crop[~mask] = 255                                    # remove neighbours' bits
        crop = strip_caption(crop)
        pad = 24
        canvas = Image.new("RGB", (crop.shape[1] + 2 * pad, crop.shape[0] + 2 * pad), "white")
        canvas.paste(Image.fromarray(crop), (pad, pad))
        name = f"{key}-{k:02d}.png"
        canvas.save(os.path.join(OUT, name))
        res.append(name)
    return res


def strip_caption(crop):
    """Drop a caption under the feet: the last band of ink if it is short
    and separated from the figure by a white gap."""
    rows = (crop.min(2) < 200).sum(1)
    on = rows > 0
    runs, y = [], 0
    while y < len(on):
        if on[y]:
            z = y
            while z < len(on) and on[z]:
                z += 1
            runs.append((y, z)); y = z
        else:
            y += 1
    h = len(on)
    while len(runs) > 1 and runs[-1][1] - runs[-1][0] < 0.08 * h and runs[-1][0] - runs[-2][1] >= 3:
        crop = crop[:runs[-2][1] + 2]
        runs.pop()
    return crop


def index(names):
    th = 260
    tiles = []
    for n in names:
        t = Image.open(os.path.join(OUT, n))
        t.thumbnail((180, th))
        tiles.append((n, t))
    cols = 10
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 190, rows * (th + 24)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (n, t) in enumerate(tiles):
        x, y = (i % cols) * 190, (i // cols) * (th + 24)
        sheet.paste(t, (x + (190 - t.width) // 2, y + th - t.height))
        d.text((x + 4, y + th + 4), n[:-4], fill="black")
    sheet.save(os.path.join(OUT, "_index.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    allnames = []
    for key, p in SHEETS.items():
        r = cut(key, p)
        print(f"{key}: {len(r)} figures")
        allnames += r
    index(allnames)
    print(f"{len(allnames)} cutouts -> {os.path.relpath(OUT, ROOT)}")
