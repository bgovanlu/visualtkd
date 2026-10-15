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

## Deployment
- Live at visualtkd.com: launched by Brian on 15 October from a Claude Code session with AWS (Route 53) and GitHub access.
- `site/` is the publish directory; `site/_redirects` holds the `/go/` short links.

## Design assets
- `design/character-v2.md`: brief, references, the 10 directions and model sheet v1 (MS-1–MS-8) with correction checklists.
- `design/models/manifest.json`: every generated image with job ID, URL and full prompt; the **Fetch design images** Action downloads them into `design/models/directions/` and `design/models/ms-v1/`.

## Plan
See ROADMAP.md: Phase 1 site structure (#5, #6, #2) → Phase 2 diagram clarity (#4, #3) → Brian reviews model sheets MS-1–MS-8 → Phase 3 character v2 (#7, #1) → Phase 4 poomsae sheets v2. Launch (#8) done.

## Follow-ups
- GitHub issue #1: redesign front kicks seen from behind, and front-view kicks that read like knee lifts.
- Find individual Digital Encyclopedia videos for T7, T8, Keumgang, Taebaek.
- Keumgang mountain blocks are drawn in profile; may become front/back views after the video check.
