# visualtkd.com — working conventions

Modern diagrams of the Kukkiwon poomsae: one page per form, a two-page print sheet per form, and a forms index. Read this before adding or changing a form.

## How a form is built

Every form page is **generated**; never hand-edit `site/<form>/index.html`.

- `templates/form.html` — the one page template (layout, figure renderer, carousel, print hooks). Change shared behaviour here.
- `forms/<form>.json` — everything specific to one form: moves, floor-plan layout, minimap positions, trigram, notes, references.
- `tools/build_form.py` — renders template + data into `site/<slug>/index.html`, builds the print PDF with `--print`, decodes every QR in that PDF, and regenerates `site/_redirects`.

```
python3 tools/build_form.py forms/taegeuk-2.json --print     # one form
python3 tools/build_form.py --all --print                     # everything (after a template change)
```

Setup: `cd tools && npm install && pip install -r requirements.txt && python -m playwright install chromium`. The PDF needs `pdftoppm` (poppler) and the system font Noto Serif CJK KR.

After building a new form: set its `url` in the `FORMS` list in `site/index.html` (this flips its card to "Open" and moves the progress meter).

## Review list

`REVIEW.md` lists every source disagreement and unsettled choice, per form. When you add or change a form, add its open items there (and in the commit message).

## Adding a form — checklist

1. **Verify the sequence against at least two sources** before writing data: the Kukkiwon page for the form plus a published move chart. Check stance (ap seogi vs ap kubi, which foot leads), technique, hand/foot, direction, and kihap for every move. The taekwondo.fandom.com wiki may be used as a cross-check source, never as a page link. Any disagreement between sources, or any choice not settled by a source, is listed for Brian's review in the commit/PR, not decided silently.
2. Write `forms/<form>.json` (copy the nearest existing form).
3. Build with `--print`; the QR check must pass.
4. Look at the desktop floor plan, a phone carousel card and both PDF pages before committing.
5. Update the index card, commit, push.

## Move data (`moves[]`)

```
{"id":"8-2","dir":"da2","view":"side","face":"R","stance":"front","lead":"R",
 "arms":{"R":"hpunch"},"tech":"hpunch","hand":"R","note":"bandae","desc":"…"}
```

- `id`: Kukkiwon counting. A kick and the strike after it share a number: `8-1` (kick), `8-2` (strike). Ready is `J`.
- `dir`: `na` (top/start), `ga` (bottom), `da1–3` (right side of page), `ra1–3` (left side). You start at na facing ga, so a **left** turn from the start faces **da** (right of the page).
- `view`: `side` for moves along the ra/da bars (needs `face`: `R` = facing right of page, `L` = left); `front` for moves toward ga; `back` for moves toward na. Exception: side and roundhouse kicks (`skick`, `rkick`) are always drawn in profile. On the centre line, set `face` so the kicking leg is the near (white) leg; on the side bars, `face` follows the direction of travel.
- `stance`: `ready`, `close` (moa seogi), `walk` (ap seogi), `front` (ap kubi), `back` (dwit kubi), `tiger` (beom seogi), `horse` (juchum seogi), `cross` (kkoa seogi), `kick` (ap chagi, also used for jumping and target kicks), `skick` (yeop chagi), `rkick` (dollyeo chagi), `knee` (mureup chigi). `lead` = forward foot, or the kicking leg for kicks. For `back`, `lead` is the **front** foot; descriptions say "back stance with the left foot forward" so the naming convention can't be misread.
- `arms`: per hand. Fist: `low`, `punch`, `hpunch`, `inside`, `outer`, `high`, `backfist`, `guard`, `junbi`. Open hand (drawn flat): `ksout` (single knife-hand outer block), `ksblock` + `ksguard` (double knife-hand block: blocking hand + guarding hand), `spear` + `press` (spear-hand thrust + pressing hand under the elbow), `neck` (knife-hand neck strike), `khigh` (knife-hand high block; with `neck` = swallow-form), `twist` (twisted knife-hand high block), `palm` (palm inside block), `kslow` (low knife-hand block), `ksside` (knife-hand side block), `eltarget` / `grab` (open target or pulling hand). More fists: `hammer`, `elbow`, `houter` (high outer block), `spread`, `xlow` (low X block), `wedge`, `uppercut`, `cover` (covered fist), `sidepunch`, `assist` (supporting fist under the blocking arm). Combined techniques are built per hand: scissors = `outer` + `low`, mountain = `houter` + `low`. Unlisted hands are chambered at the hip.
- `tech` keys the label table `T` in the template (every key above plus combined names such as `scissors`, `mountain`, `duppercut`, `apalm`, `aouter`, `alow`, `obackfist`, `tkick`, `jkick`); add new techniques there.
- Steps with several techniques (double punch, block then punch) get sub-numbers like kicks: `17-1` block, `17-2` punch, `17-3` punch. One figure per count.
- `note`: `bandae` (punch hand = lead foot) or `baro` (opposite hand). `kihap: true` on the shouting move.
- `desc`: one plain instruction sentence: turn and direction, stance, technique.

## Floor plan (`layout`, `pos`, `boardMin`)

- Keep the original book layout: the 王 shape. `r1`, `r3`, `r5` are the three bars (left → right on the page); `c2`, `c4` are the centre column between bars. Group a kick with its strike, and figures that share a spot, in a nested list: `["16-2","16-1"]`.
- Every move id must appear exactly once in `layout` and in `pos` (build fails otherwise).
- `pos` is the phone minimap position on a 100×60 grid: bars at y 8/30/52, centre x 50, ra side x 10–30, da side x 70–90.
- `boardMin` = desktop board width in px; raise it when a bar holds more figures (Il Jang 1120, Ee Jang 1320).
- Optional `cardW` / `figH` shrink the figure cards when a bar holds 9+ figures (Sam Jang 104/124, Sa Jang 112/132). Keep the print sheet to exactly 2 pages; check the page count after building.

## Figure

- Design **Textbook line A1 "Natural"**: realistic adult proportions, single-contour limbs, sloped shoulders, faceless head (profile shape only on side views), short hair cap above the hairline, black-collar dobok, belt in the selected colour.
- **Near limbs white, far limbs grey** — this is how left/right is read; keep it for every pose.
- Seen from behind, a kicking leg is raised in front of the body: draw it over the torso in the far-side grey. (Brian finds this weak; redesign tracked in GitHub issue #1.)
- Seen from the front, punches and knife-hand neck strikes come toward the viewer: draw the arm foreshortened with the fist face / knife-hand edge, never across the face.
- New poses go in the template's `skel()`; check them in front, side and back views before use.
- No faces, no brand logos, no copyrighted characters.

## Stance cues

- Chips: walking stance = outlined, front stance = **filled**, back stance = double outline, kick = dashed.
- Footprint glyph (top view, rotated to the facing direction): red foot leads, blue tick = facing. Ap seogi short and nearly in line; ap kubi long and fist-width wide with the rear foot turned out; dwit kubi an L shape, heels in line, rear foot turned 90°.

## URLs — stable, because they are printed

- Form pages: `visualtkd.com/taegeuk/1` … `/taegeuk/8` (later: black-belt forms by name, e.g. `/koryo`). **Never rename a published path**; printed QR codes point there.
- References never link out directly from paper. Each has a short link `visualtkd.com/go/<name>` (e.g. `kukkiwon-t2`, `video-t2`) defined by the form's `refs[].go`; `site/_redirects` is generated from all forms as 302 redirects. If a destination moves, fix the JSON `url` and rebuild — never reprint.
- One `go` name must always mean one URL (the build fails on conflicts).

## References

Only official sources, in this order: the Kukkiwon page for the form, the Kukkiwon poomsae index, the Kukkiwon Digital Encyclopedia video for the form (published on YouTube by Mookas TV; say so), the Kukkiwon YouTube channel, the World Taekwondo Poomsae Competition Rules PDF. Each reference card has a generic icon (gate = Kukkiwon, play = video, channel, document = PDF) and a source label; do not draw brand logos.

## Print sheet (US Letter, 2 pages)

- Page 1: header + full floor plan; the belt picker becomes a ruled "Practice notes" box.
- Page 2: full sequence table + references.
- Both pages: form QR top right ("Scan to practise" + short address); a QR on every reference card with its `/go/` address printed under it.
- Footer on every page: `Printed from visualtkd.com/<slug> · <form name>` | `Edition <Month Year> · Page x of y`.
- The build decodes every QR from the rendered PDF; never ship a sheet that fails this check.

## Page behaviour

- Desktop: floor plan, study panel with Play, sequence table, references.
- Phone (≤760px): move-by-move carousel with minimap, plus a Floor plan toggle. No horizontal page scroll.
- Light and dark themes via CSS tokens; fonts Noto Serif KR (display/Korean), IBM Plex Sans Condensed (body), IBM Plex Mono (labels).

## Writing

Plain, direct English. Korean names romanised as Kukkiwon does (Taegeuk Il Jang, ap seogi, arae makki) with Hangul alongside. Describe meanings in your own words; don't copy Kukkiwon text.

## Deploy

Netlify or Cloudflare Pages: no build command, publish directory `site`. Both read `site/_redirects`.
