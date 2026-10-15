# Status — 14 October 2026

## Forms: 11 of 17 built
| Form | Path | Figures | Review |
|---|---|---|---|
| Taegeuk Il Jang | /taegeuk/1 | 21 | Published |
| Taegeuk Ee Jang | /taegeuk/2 | 24 | Reviewed (back-view kick accepted for now) |
| Taegeuk Sam – Pal Jang | /taegeuk/3 … /8 | 30–39 | Open items in REVIEW.md (T8 has the most) |
| Koryo 高麗 (士) | /koryo | 47 | Open items in REVIEW.md |
| Keumgang 金剛 (山) | /keumgang | 28 | Open items; mountain-block facing is the biggest question |
| Taebaek 太白 (工) | /taebaek | 40 | Open items in REVIEW.md |

Planned: Pyongwon, Sipjin, Jitae, Cheonkwon, Hansu, Ilyeo.

Every print sheet is exactly 2 pages and every QR code decodes to its expected link.

## Short links (`/go/`, generated into `site/_redirects`)
- Kukkiwon form pages: `kukkiwon-t1` … `t8` (boardNo 1347, 1349–1355), `kukkiwon-koryo` / `keumgang` / `taebaek` (1356–1358), `kukkiwon-poomsae`
- Videos (Kukkiwon Digital Encyclopedia, Mookas TV): `video-t1` … `t6`, `video-koryo`; `video-t7`, `t8`, `keumgang`, `taebaek` point to the series playlist until individual videos are found
- `kukkiwon-youtube`, `wt-poomsae-rules`

## Deployment — not live yet
- `visualtkd.com` is registered and delegated to Route 53.
- No host is set up and no records exist in the hosted zone yet.
- Planned host: Cloudflare Pages or Netlify (no build command, publish directory `site`); both read `_redirects`. Then in Route 53: apex alias/ALIAS and `www` CNAME to the host, and the host's domain-verification record if it asks for one.
- On AWS-only hosting (S3 + CloudFront + ACM), `_redirects` would need converting to CloudFront Function or S3 routing rules.

## Plan
See ROADMAP.md: Phase 1 site structure (#5, #6, #2) → Phase 2 diagram clarity (#4, #3) → Brian reviews model sheets MS-1–MS-8 → Phase 3 character v2 (#7, #1) → Phase 4 poomsae sheets v2. Launch (#8) whenever hosting is unblocked.

## Follow-ups
- GitHub issue #1: redesign front kicks seen from behind, and front-view kicks that read like knee lifts.
- Find individual Digital Encyclopedia videos for T7, T8, Keumgang, Taebaek.
- Keumgang mountain blocks are drawn in profile; may become front/back views after the video check.
