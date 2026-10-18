# Status — 14 October 2026

## World Taekwondo forms: 17 of 17 built
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
| Hansu 漢水 (水) | /hansu | 34 | Open items in REVIEW.md; first form with diagonal directions |
| Ilyeo 一如 (卍) | /ilyeo | 31 | Open items in REVIEW.md; directions from the Kukkiwon textbook video (fandom differs) |

Planned: none; all 17 Kukkiwon forms are published.

## ITF forms: 5 of 24 built
| Form | Path | Figures | Review |
|---|---|---|---|
| Chon-Ji 天地 (+) | /itf/chon-ji | 20 | Open items in REVIEW.md; orientation (D at the bottom) is the big one |
| Dan-Gun 檀君 (I) | /itf/dan-gun | 22 | Open items in REVIEW.md; 270° turns, twin forearm block arms |
| Do-San 島山 (I + diagonals) | /itf/do-san | 25 | Open items in REVIEW.md; floor line drawn as I instead of the book's half-卍 |
| Won-Hyo 元曉 (I) | /itf/won-hyo | 29 | Open items in REVIEW.md; fixed stance and bending ready stance drawn with Kukkiwon figures |
| Yul-Gok 栗谷 (士) | /itf/yul-gok | 39 | Open items in REVIEW.md; X-stance jump drawn from behind, elbow strike front view |

The forms index has an **ITF forms** section, next to **World Taekwondo forms**, with a planned card for each of the 24 Chang Hon patterns. Each card has the pattern's floor diagram (skeleton layout), rank and move count from `itf` in `data/catalog.json`. The other 19 have no pages or print sheets yet. Each card links to its official pattern page; the section lists the official ITF references.

## History page
`/history/` is a top-level page in the nav, between Library and How to read. It gives a short history of taekwondo (roots, kwans, the 1955 name, the ITF and Chang Hon patterns, the Kukkiwon and the WTF, WTF → World Taekwondo, the ITF after Choi, other branches, the two families of forms), with a family-tree diagram and official references. The claims that need checking are in REVIEW.md. Open questions (URLs, orientation, federation, Juche/Ko-Dang, diagrams) are in REVIEW.md.

Every print sheet is exactly 2 pages and every QR code decodes to its expected link.

## Short links (`/go/`, generated into `site/_redirects`)
- Kukkiwon form pages: `kukkiwon-t1` … `t8` (boardNo 1347, 1349–1355), `kukkiwon-koryo` / `keumgang` / `taebaek` / `pyongwon` / `sipjin` / `jitae` / `cheonkwon` / `hansu` / `ilyeo` (1356–1364), `kukkiwon-poomsae`
- Videos (Kukkiwon Digital Encyclopedia, Mookas TV): `video-t1` … `t6`, `video-koryo`; `video-t7`, `t8`, `keumgang`, `taebaek`, `pyongwon` point to the series playlist until individual videos are found; `video-sipjin`, `video-jitae`, `video-cheonkwon`, `video-hansu` and `video-ilyeo` are the Kukkiwon textbook (vol. 3) videos linked from the Kukkiwon pages
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
