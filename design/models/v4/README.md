# v4 — one generation per pose

Image models can't hold body geometry from text alone (MS-1 v3, every model). v4 gives the model a **pose guide** instead: a 3D mannequin posed exactly, plus the closest drawing of our character for identity and style. Each image is one figure.

## Count (Taegeuk 1–8, Koryo, Keumgang, Taebaek)

| | images |
|---|---|
| Figures on the 11 boards | 363 |
| Distinct poses (exact) | 230 |
| **Distinct poses, mirrors reused** | **129** ← one folder each |

Mirrors: a pose and its left/right mirror (lead foot, arms and facing swapped) are one generation; the site flips the image. Caveat: a flipped image also flips the dobok lapel overlap (left over right becomes right over left). If that matters, generate the mirrors too (230).

By stance: front 52 · walk 21 · back 18 · horse 9 · tiger 8 · kick 5 · ready 4 · skick 4 · crane 2 · close 2 · cross 2 · rkick 1 · knee 1. By view: side 63 · front 36 · back 30.

Budget a retry factor: expect 1.5–2 tries per pose (about 200–260 generations for the 129).

## What's in a pose folder

`<pose-id>/` (the id spells out stance, lead, view, facing and each hand, e.g. `front-leadL-side-faceL-Lpunch-Rchamber`)

- `mannequin.png`: pose guide, image 1. Left limbs blue, right limbs orange, the cone on the head is the nose, the dark cap is the toes.
- `character.jpg`: closest drawn character, image 2 (same stance and view where one exists: 120 of 129).
- `prompt.txt`: the prompt (pose, hands, view, style).
- `pair.jpg`: both side by side, for review only.

`manifest.json` lists everything, with the moves each pose is used for (`uses`, form#move). `_pairs-<stance>.jpg` are review sheets. `characters/` holds the 65 cutouts and `_index.png`; their tags are in `tools/poses/characters.json`.

## Workflow in the web app

1. Upload `mannequin.png` and `character.jpg` as references, in that order; paste `prompt.txt`.
2. Keep the result only if the feet and the knee directions match the mannequin; save it as `<pose-id>/final.png` (or note the generation URL in `manifest.json` and the GitHub Action fetches it).
3. Once the first good results exist, use one of them as image 2 for the rest of that stance; it holds the style better than the old sheets.

## Changing a pose

- Editor: serve the repo root (`python3 -m http.server` in the repo) and open `/tools/poses/mannequin.html#<pose-id>`. Use the sliders or orbit the view, then **Copy** the override JSON into `data/pose-overrides.json` under the pose id.
- Re-render: `python3 tools/poses/render.py --only <id>[,<id>]` (or no flag for all; `--all-views` writes front/side/back/top too).
- Re-pair: `python3 tools/poses/pair.py`.
- New forms: `python3 tools/poses/inventory.py` → render → pair.
