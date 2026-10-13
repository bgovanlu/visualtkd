# visualtkd.com

Modern, mobile-friendly diagrams of the Kukkiwon poomsae. Each form keeps the original 王-shaped floor plan on desktop, becomes a move-by-move carousel on phones, and ships with a two-page print sheet carrying QR codes back to the site.

## Layout

```
site/                     ← deploy this folder (the publish directory)
  index.html              forms index: Taegeuk 1–8 and the black-belt forms
  taegeuk/1/index.html    Taegeuk Il Jang
  taegeuk/1/taegeuk-1-print.pdf
  _redirects              /go/ short links used by printed QR codes
tools/
  build_print.py          builds a form's 2-page PDF (floor plan + sequence)
  package.json            fonts embedded in the PDFs
  requirements.txt
design/                   character studies kept for reference (not deployed)
```

## URLs

| Path | Purpose |
|---|---|
| `/` | Forms index |
| `/taegeuk/1` … `/taegeuk/8` | One page per form. **Printed QR codes point here, so keep these paths stable.** |
| `/go/<name>` | Short links behind the reference QR codes on the print sheets |

Reference QR codes never point at outside sites directly. They go through `/go/<name>`, defined in `site/_redirects` as temporary (302) redirects. If Kukkiwon, YouTube or World Taekwondo moves a page, change one line in `_redirects`; every printed sheet keeps working.

## Deploy

**Netlify or Cloudflare Pages.** Connect this repo, leave the build command empty, and set the publish/output directory to `site`. Both read `site/_redirects` as-is. Then add `visualtkd.com` as the custom domain.

Other hosts (Vercel, GitHub Pages, nginx) don't read `_redirects`; convert the rules to that host's format.

## Rebuilding a print sheet

```
cd tools && npm install && pip install -r requirements.txt && python -m playwright install chromium && cd ..
python3 tools/build_print.py site/taegeuk/1/index.html site/taegeuk/1/taegeuk-1-print.pdf \
  https://visualtkd.com/taegeuk/1 "Taegeuk Il Jang" "태극 1장 · 18 movements"
```

The sheet is US Letter: page 1 is the floor plan, page 2 the full sequence and references. Both pages carry a QR to the form's page and a footer naming where the sheet was printed from, its edition and page number. Korean text uses Noto Serif CJK KR from the system.

## Sources

Form content follows Kukkiwon. References link only to official Kukkiwon and World Taekwondo material.
