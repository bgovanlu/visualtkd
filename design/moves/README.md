# Per-move figure images (#7)

One image per count, per form, to replace the vector figures on the form pages and print sheets.

## For whoever generates the images
- **Brief:** each form has its own folder here (`taegeuk-1/` … `taebaek/`, named after `forms/<form>.json`). Its `SPEC.md` lists every count with a ready-to-paste prompt; `spec.json` has the same data.
- **File names:** save each image in that form's folder as `<id>.png`, using the count shown in SPEC.md: `J.png` (ready), `1.png`, `14-1.png`, `14-2.png` and so on. JPEG or WebP are fine too.
- **Format:** one figure per image, full body, plain white background, 2:3 portrait, at least 1024 px tall, with a margin all round and nothing touching the edge. No text, numbers or footprints.
- **Facing:** draw side views facing the edge named in the prompt. The build does not mirror images, because mirroring swaps the left and right hands. "Near arm" means the arm closer to the viewer.
- **References:** `design/models/directions/d10-realistic-anatomical-CHOSEN.png` for the character, plus the model sheet for the stance in `design/models/ms-v2/` (or `ms-v3/` once approved).
- **Partial sets are fine:** counts with no image keep the current vector figure.

## Building with them
```
python3 tools/build_form.py forms/taegeuk-1.json --images           # page -> preview/taegeuk/1/
python3 tools/build_form.py forms/taegeuk-1.json --images --print   # plus the print PDF and QR check
```
- `tools/figures.py` turns each image into a page figure:
  - cuts the figure out of the white background;
  - trims it;
  - scales it to a common body height using a per-stance share of standing height, because low stances stand shorter;
  - writes `preview/<slug>/fig/<id>.webp`.
- If one figure looks too big or small (for example, a hand or kicking foot above the head makes the trimmed image taller), set its share in `<form>/fit.json`: `{"14-1": 1.05}`.
- `preview/` is git-ignored and never deployed. Once the images are approved, the build will write image figures straight to `site/`.

To rebuild the briefs after changing a form's moves, run `python3 tools/move_specs.py --all`.
