# Status — 14 October 2026

## Forms: 12 of 17 built
| Form | Path | Figures | Review |
|---|---|---|---|
| Taegeuk Il Jang | /taegeuk/1 | 21 | Published |
| Taegeuk Ee Jang | /taegeuk/2 | 24 | Reviewed (back-view kick accepted for now) |
| Taegeuk Sam – Pal Jang | /taegeuk/3 … /8 | 30–39 | Open items in REVIEW.md (T8 has the most) |
| Koryo 高麗 (士) | /koryo | 47 | Open items in REVIEW.md |
| Keumgang 金剛 (山) | /keumgang | 28 | Open items; mountain-block facing is the biggest question |
| Taebaek 太白 (工) | /taebaek | 40 | Open items in REVIEW.md |
| Pyongwon 平原 (一) | /pyongwon | 34 | Open items in REVIEW.md; directions inferred, check against the video first |
| Sipjin 十進 (十) | /sipjin | 43 | Open items in REVIEW.md; directions checked against the Kukkiwon textbook video |
| Jitae 地跆 (ㅗ) | /jitae | 39 | Open items in REVIEW.md; directions checked against the Kukkiwon textbook video |
| Cheonkwon 天拳 (ㅜ) | /cheonkwon | 41 | Open items in REVIEW.md; directions checked against the Kukkiwon textbook video |

Planned: Hansu, Ilyeo.

Every print sheet is exactly 2 pages and every QR code decodes to its expected link.

## Short links (`/go/`, generated into `site/_redirects`)
- Kukkiwon form pages: `kukkiwon-t1` … `t8` (boardNo 1347, 1349–1355), `kukkiwon-koryo` / `keumgang` / `taebaek` / `pyongwon` / `sipjin` / `jitae` / `cheonkwon` (1356–1362), `kukkiwon-poomsae`
- Videos (Kukkiwon Digital Encyclopedia, Mookas TV): `video-t1` … `t6`, `video-koryo`; `video-t7`, `t8`, `keumgang`, `taebaek`, `pyongwon` point to the series playlist until individual videos are found; `video-sipjin`, `video-jitae` and `video-cheonkwon` are the Kukkiwon textbook (vol. 3) videos linked from the Kukkiwon pages
- `kukkiwon-youtube`, `wt-poomsae-rules`

## Deployment — live on AWS since 14 October 2026
- https://visualtkd.com, served by CloudFront distribution `EGPPRILDVGXUB` from the private bucket `visualtkd-site-820501670514`. Stack `visualtkd-site` in us-east-1 (`infra/aws/site.yaml`); deploy with `tools/deploy_aws.py`.
- Route 53 zone `Z06165962R1Q3DUXU1VLW`. The stack owns the A/AAAA aliases (apex and `www`) and the ACM validation CNAMEs; the no-mail records (null MX, `v=spf1 -all`, DMARC `p=reject`) are applied by hand from `infra/route53/visualtkd.com.json`.
- Checked live on 14 Oct: every form path 301s to its trailing-slash page and serves its PDF, all 25 `/go/` links 302 to their `_redirects` targets, `www` and `http` redirect to `https://visualtkd.com`, missing pages return 404 with the forms index.

## Design assets
- `design/character-v2.md`: brief, references, the 10 directions and model sheet v1 (MS-1–MS-8) with correction checklists.
- `design/models/ms-v3-prompts.md`: v3 prompts for the Higgsfield web app (unlimited models aren't available through the API).
- `design/models/manifest.json`: every generated image with job ID, URL and full prompt; the **Fetch design images** Action downloads them into `design/models/directions/` and `design/models/ms-v1/`.

## Plan
See ROADMAP.md: Phase 1 site structure (#5, #6, #2) → Phase 2 diagram clarity (#4, #3) → Brian reviews model sheets MS-1–MS-8 → Phase 3 character v2 (#7, #1) → Phase 4 poomsae sheets v2. Launch (#8) done.

## Follow-ups
- GitHub issue #1: redesign front kicks seen from behind, and front-view kicks that read like knee lifts.
- Find individual Digital Encyclopedia videos for T7, T8, Keumgang, Taebaek.
- Keumgang mountain blocks are drawn in profile; may become front/back views after the video check.
