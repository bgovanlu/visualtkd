# visualtkd.com

Modern, mobile-friendly diagrams of the Kukkiwon poomsae. Each form keeps the original 王-shaped floor plan on desktop, becomes a move-by-move carousel on phones, and ships with a two-page print sheet carrying QR codes back to the site.

## Layout

```
site/                     ← deploy this folder (the publish directory)
  index.html              forms index: Taegeuk 1–8 and the black-belt forms
  taegeuk/1/, taegeuk/2/  generated form pages + their 2-page print PDFs
  _redirects              /go/ short links used by printed QR codes (generated)
forms/                    one JSON file of data per form
templates/form.html       the shared form page template
tools/
  build_form.py           builds pages, PDFs (--print), QR check, _redirects
  build_print.py          the 2-page print sheet
design/                   character studies kept for reference (not deployed)
CLAUDE.md                 conventions for adding and changing forms
```

## URLs

| Path | Purpose |
|---|---|
| `/` | Forms index |
| `/taegeuk/1` … `/taegeuk/8` | One page per form. **Printed QR codes point here, so keep these paths stable.** |
| `/go/<name>` | Short links behind the reference QR codes on the print sheets |

Reference QR codes never point at outside sites directly. They go through `/go/<name>`, defined in `site/_redirects` as temporary (302) redirects. `_redirects` is generated from the `refs` in `forms/*.json`: if Kukkiwon, YouTube or World Taekwondo moves a page, update its `url` there and rebuild; every printed sheet keeps working.

## Deploy

**Netlify or Cloudflare Pages.** Connect this repo, leave the build command empty, and set the publish/output directory to `site`. Both read `site/_redirects` as-is. Then add `visualtkd.com` as the custom domain.

Other hosts (Vercel, GitHub Pages, nginx) don't read `_redirects`; convert the rules to that host's format.

## Building

```
cd tools && npm install && pip install -r requirements.txt && python -m playwright install chromium && cd ..
python3 tools/build_form.py forms/taegeuk-2.json --print   # one form
python3 tools/build_form.py --all --print                   # every form
```

Pages are generated from `templates/form.html` + `forms/*.json`; don't edit `site/*/index.html` by hand. `--print` also builds the PDF and decodes every QR code in it. See `CLAUDE.md` for the full conventions.

## Sources

Form content follows Kukkiwon. References link only to official Kukkiwon and World Taekwondo material.
