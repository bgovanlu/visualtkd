# visualtkd.com

Modern, mobile-friendly diagrams of the Kukkiwon poomsae. Each form keeps its original floor line on desktop (王 for the Taegeuk forms; 士, 山, 工 for Koryo, Keumgang, Taebaek), becomes a move-by-move carousel on phones, and ships with a two-page print sheet carrying QR codes back to the site.

## Layout

```
site/                     ← deploy this folder (the publish directory)
  index.html              forms index: Taegeuk 1–8 and the black-belt forms
  taegeuk/1/ … /8/        generated form pages + their 2-page print PDFs
  koryo/ keumgang/ taebaek/  black-belt form pages + print PDFs
  _redirects              /go/ short links used by printed QR codes (generated)
forms/                    one JSON file of data per form
templates/form.html       the shared form page template
tools/
  build_form.py           builds pages, PDFs (--print), QR check, _redirects
  build_print.py          the 2-page print sheet
  deploy_aws.py           deploys site/ to AWS (stack, upload, cache invalidation)
  check/                  screenshots for review: shot.py (board / phone), figs.py (enlarged poses) -> shots/
  authoring/              scripts that wrote some forms/*.json (reference only; re-running overwrites)
infra/aws/                CloudFormation stack (S3, CloudFront, ACM, Route 53), viewer-request function, deployer IAM policy
infra/route53/            DNS records kept outside the stack (no-mail MX/SPF/DMARC)
design/                   character studies kept for reference (not deployed)
CLAUDE.md                 conventions for adding and changing forms
REVIEW.md                 open questions per form, to check against the Kukkiwon videos
docs/STATUS.md            what's built, short links, deployment state, follow-ups
ROADMAP.md                phases and plan for every open GitHub issue
```

## URLs

| Path | Purpose |
|---|---|
| `/` | Forms index |
| `/taegeuk/1` … `/taegeuk/8`, `/koryo`, `/keumgang`, `/taebaek` | One page per form. **Printed QR codes point here, so keep these paths stable.** |
| `/go/<name>` | Short links behind the reference QR codes on the print sheets |

Reference QR codes never point at outside sites directly. They go through `/go/<name>`, defined in `site/_redirects` as temporary (302) redirects. `_redirects` is generated from the `refs` in `forms/*.json`: if Kukkiwon, YouTube or World Taekwondo moves a page, update its `url` there and rebuild; every printed sheet keeps working.

## Deploy

**AWS: S3 + CloudFront**, defined in `infra/aws/site.yaml` (stack `visualtkd-site`, us-east-1). The bucket is private and read only by CloudFront; ACM issues the certificate for `visualtkd.com` and `www`; the stack also owns the Route 53 alias records.

```
python3 tools/deploy_aws.py             # update the stack, upload site/, invalidate the cache
python3 tools/deploy_aws.py --content   # upload + invalidate only (page or PDF changes)
```

CloudFront doesn't read `_redirects`. A viewer-request function (`infra/aws/viewer-request.js`) does what a static host would: `www` → `visualtkd.com`, `/taegeuk/1` → `/taegeuk/1/` → `index.html`, and the `/go/` short links, which `deploy_aws.py` compiles in from `site/_redirects`. **A new or changed short link therefore needs the full deploy, not `--content`.**

The deploying credentials need `infra/aws/deployer-policy.json` (or admin).

## Building

```
cd tools && npm install && python3 -m venv ../.venv && ../.venv/bin/pip install -r requirements.txt && ../.venv/bin/python -m playwright install chromium && cd ..
python3 tools/build_form.py forms/taegeuk-2.json --print   # one form
python3 tools/build_form.py --all --print                   # every form
```

Pages are generated from `templates/form.html` + `forms/*.json`; don't edit `site/*/index.html` by hand. `--print` also builds the PDF and decodes every QR code in it. See `CLAUDE.md` for the full conventions.

## Sources

Form content follows Kukkiwon. References link only to official Kukkiwon and World Taekwondo material.
