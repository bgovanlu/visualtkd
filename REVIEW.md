# Review list — Taegeuk 1–8 and the first four black-belt forms

Everything below is either a place where sources disagree or a choice no source settled. Each item says what the site shows now. Tick an item when you've checked it against your school's practice or the Kukkiwon video; if the site needs to change, note the fix and the move id (e.g. `T5 5-1`).

To change a form, edit `forms/<form>.json` (e.g. `taegeuk-3.json`, `koryo.json`) and run `python3 tools/build_form.py forms/<form>.json --print`.

**How to read the move ids:** a step with several counts uses sub-numbers, the same way kicks already do. For example, `6-1` is a kick, `6-2` the strike that follows it, and `6-3` the block after that.

---

## All forms

- [ ] **Back-stance naming.** Fandom names dwit kubi by the **rear** foot ("right back stance, left foot forward"). Yonggi names it by the **front** foot. The site avoids both: chips show the front foot ("L · Dwit kubi" = left foot forward), and instructions say "back stance with the left foot forward". Decide which convention the chips should follow.
- [ ] **Front kicks seen from behind** are drawn as a grey raised leg over the body. You've said this is weak; it's tracked in [issue #1](https://github.com/bgovanlu/visualtkd/issues/1). Affected moves:

  | Form | Moves |
  |---|---|
  | T2 | 16-1, 17-1, 18-1 |
  | T3 | 19-1, 20-1 |
  | T4 | 14-1 |
  | T5 | 14-1, 20-1 |
  | T7 | 21-1, 23-1 |
  | T8 | 19-1, 19-2 |

- [ ] **Front kicks seen from the front** read like a knee lift. Affected moves:

  | Form | Moves |
  |---|---|
  | T4 | 6-1 |
  | T5 | 6-1, 7-1 |
  | T8 | 3-1, 3-2, 11-1 |

  Best fixed together with issue #1.
- [ ] **Side and roundhouse kicks on the centre line** (T4 7, 8-1; T6 6-1, 12-1) are drawn in profile, which breaks the "centre figures face you" rule. A straight-on side kick is hard to read.
- [ ] **Side kicks on the side bars** (T5 16-1, 18-1). The figure faces the direction of travel, so the kicking leg is the far, grey leg.
- [ ] **Floor positions** for the minimap and the floor plan are approximate in T5–T8. The order of moves and the facing directions are what the sources settle. Where each figure stands on the 王 is our layout.
- [ ] **Move numbering** follows one source's step list per form and gives sub-numbers to multi-technique steps. Kukkiwon's own movement counts (shown in each page header) don't always match the number of steps:

  | Form | Header shows | Steps in our list |
  |---|---|---|
  | T4 | 20 | 18 |
  | T5 | 20 | 20 |
  | T6 | 19 | 19 |
  | T7 | 25 | 25 |
  | T8 | 24 | 27 |

- [ ] **Video links for T7 and T8** go to the Kukkiwon Digital Encyclopedia playlist, not a single video. Once you find the individual videos, change `refs[].url` for `video-t7` and `video-t8`. Printed sheets keep working because they go through `/go/`.

## Site pages and technique library (Phase 1, #5 #6 #2)

- [ ] **About text** on the landing page (`/#about`, written in `tools/build_site.py`). It currently names no person, school or federation and gives no contact. It says the site is independent and not affiliated with Kukkiwon or World Taekwondo. Tell me what to add.
- [ ] **Library URL scheme** `/library/<family>/#<slug>` (families `stances`, `blocks`, `strikes`, `kicks`, `hands-feet`; slugs are the romanised names). Built as proposed in ROADMAP.md. Confirm before any of these paths get printed.
- [ ] **Library descriptions** (`data/techniques.json`, all 60 techniques and 9 stances) are written in our own words from general Kukkiwon practice. Please read them through. These points are the least settled:
  - **Forearm blocks:** they all name the surface as *palmok* (forearm). Kukkiwon distinguishes bakkat palmok and an palmok per block; we haven't assigned these block by block yet.
  - **No surface given:** knee break (Koryo 12-2), large hinge and small hinge (keun / jageun doljjeogwi).
  - **Grouping:** we filed jageun doljjeogwi and keun doljjeogwi under blocks, and the knee break and twisting grab under strikes ("grabs and breaks").
  - **Ap kubi:** described as "most of the weight on the front leg" and "rear foot turned out about 30°".
  - **Dwit kubi:** "most of the weight on the rear leg", hips turned to the side.
- [ ] **Hands and feet page** shows a technique that uses each surface, not a close-up of the hand or foot. The close-ups come from model sheet MS-8 in Phase 3.
- [ ] **`figH` in the form JSON has never taken effect.** A later `:root` rule in the template resets `--fig-h` to 150px, so only `cardW` shrinks the cards. We left this alone so the print sheets don't move. Fix it with the character v2 rebuild, or drop the field.

## Footwork simulator (Phase 2, #3) and same-stance moves (#4)

See `design/footwork.md` and `design/same-stance.md`. Open any form with `?footwork` to see the footwork, or with `?same=a|b|c` for the same-stance treatments.

- [ ] **Pick a same-stance treatment:** A, B or C.
- [ ] **Check the footwork diagrams** on two forms against your example (`design/refs/footwork-example-issue3.png`). Then we decide whether they replace the footprint glyph by default.
- [ ] **T7 21-2 to 25 (horse stances on the centre line).** The data draws these from behind, facing na, with the feet across the line. But the instructions ("land in a horse stance" after a kick toward na; "step the right foot forward into a horse stance") need the feet *on* the na line and the body facing sideways. The simulator assumes the latter (`"step": {"horse": "along"}`). Which is right? If the body faces sideways, the figures should be side views.
- [ ] **T8 7** ("cross the left foot in front of the right and step out"). Does the stance travel toward da³, and how far? The simulator currently leaves it in place, because assuming a full stance length of travel made the end position worse.
- [ ] **Where each form ends, simulated** (foot lengths from the start, before the final baro step): T1 1.4, T2 0.6, T3 1.1, T4 0.8, T5 1.7, T6 2.3, T7 5.2, T8 3.1, Koryo 2.3, Keumgang 2.7, Taebaek 4.2. The largest values point at steps worth checking against the video (T7 and Taebaek).
- [ ] **The minimap still uses the hand-placed `pos`.** The simulated positions could replace it once the footwork is approved.

## Taegeuk 1 · Il Jang

Sources: Kukkiwon page, standard Kukkiwon sequence. The fandom page wouldn't load when this was built.

- [ ] **Moves 7–10.** The inside blocks use the hand opposite the forward foot (7: right walking stance with left block; 9: left stance with right block), and the punches in 8 and 10 are reverse punches (baro).

## Taegeuk 2 · Ee Jang

Sources: [Kukkiwon](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1349&page=2&menuLevel=3&menuNo=72), [NBTKDA chart](https://www.nbtkda.com/s/Taegeuk-2-NBTKDA-Poomsae-Chart.pdf), [Wikipedia](https://en.wikipedia.org/wiki/Taegeuk_Ee_Jang). These agree on every stance, technique and hand.

- [ ] **Directions of 13 and 14.** No source states them. Drawn as: 13 is a 270° left turn to face ra³; 14 pivots 180° to face da³. This fits Wikipedia's note that the last turn is a pivot in place.

## Taegeuk 3 · Sam Jang

Sources: [NBTKDA page](https://www.nbtkda.com/taegeuk-3) (techniques and turn types), [Taekwondo Nation](https://taekwondonation.com/tae-kwon-do-form-3-taegeuk-sam-jang) (full list), [Wikipedia](https://en.wikipedia.org/wiki/Taegeuk_Sam_Jang).

- [ ] **Move 5, turn direction.** Drawn as a left turn toward ga, the only way the step lands facing ga. Taekwondo Nation says "turn right".
- [ ] **Moves 5–6, technique.** Drawn as a knife-hand neck strike (NBTKDA, Wikipedia). Taekwondo Nation calls it a ridge-hand.
- [ ] **Moves 7–10, which side.** Drawn with 7–8 facing da² and 9–10 facing ra², following Il Jang and Ee Jang. Not stated by any source.
- [ ] **Move 13.** Drawn as a 270° left turn to face ra³.

## Taegeuk 4 · Sa Jang

Sources: [Miami Taekwondo Schools](https://mtftaekwondo.com/taegeuk-4-sa-jang-jin-symbolizes-thunder-20-movements/) (full list), [Taekwondo Nation](https://www.taekwondonation.com/tae-kwon-do-belt-form-4-taegeuk-sa-jang/), [NBTKDA page](https://www.nbtkda.com/taegeuk-4), [Wikipedia](https://en.wikipedia.org/wiki/Taegeuk_Sa_Jang).

- [ ] **Moves 9–12, which side.** Drawn as 9–10 facing ra³ (270° left turn) and 11–12 facing da³.
- [ ] **Move 2 wording.** Taekwondo Nation's text for move 2 ("double knife-hand strike") doesn't match the spear-hand thrust that every other source gives. Drawn as a spear-hand thrust.

## Taegeuk 5 · Oh Jang

Sources: fandom (full list), [Taekwondo Nation](https://www.taekwondonation.com/tae-kwon-do-form-5-taegeuk-oh-jang/) (full list), [Kukkiwon](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1352&page=2&menuLevel=3&menuNo=72).

- [ ] **Moves 2 and 4, stance.** Both sources call it a walking stance; Kukkiwon's name is *oen seogi* / *oreun seogi*, a short stance with one foot turned out. Drawn as a short walking stance in profile, with the hammer-fist going forward.
- [ ] **Move 5.** Fandom has two blocks (5-1 left inside block, then 5-2 right inside block). Taekwondo Nation has one right middle block. **Drawn as fandom's two blocks.**
- [ ] **Move 19.** Fandom has a low block then an inside block. Taekwondo Nation has a low block then a right **punch**. **Drawn as fandom's inside block.**
- [ ] **Move 20, landing stance.** Fandom says rear cross stance (left foot behind); Taekwondo Nation says "oreun ap kkoa seogi" (front cross). Drawn as rear cross stance. Kihap here per fandom; Taekwondo Nation doesn't give a kihap.
- [ ] **Moves 10 and 12, which elbow strike.** Drawn as palkup dollyeo chigi into the palm. Taekwondo Nation doesn't name the side.
- [ ] **Moves 16-1 and 18-1, the arm during the side kick.** Fandom says the arm is extended; drawn as a side-punch arm.
- [ ] **Floor layout.** Drawn with 5–8 travelling down the centre to the third line, 9–12 on the third line, 15–18 on the middle line, and 19–20 returning up the centre (the same pattern as Sa Jang). Not stated by the sources.

## Taegeuk 6 · Yuk Jang

Sources: [Yonggi Taekwondo](https://www.sites.google.com/site/yonggitaekwondo/poomse/yuk-jang) (full list with kihap), [Taekwondo Nation](https://taekwondonation.com/tae-kwon-do-form-6-taegeuk-yuk-jang) (full list, muddled turns), [Kukkiwon](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1353&page=2&menuLevel=3&menuNo=72). Fandom wouldn't load.

- [ ] **Move 12, turn direction.** Yonggi says "270° counter-clockwise", which would face ra³. **Drawn facing da³ instead**, with 14–15 facing ra³. That is the only way move 16 can face ga and the last four moves can step *backward* toward the start, as both sources describe.
- [ ] **Move 5, turn direction.** Yonggi says "90° right"; drawn as a left turn toward ga, consistent with every other form.
- [ ] **Moves 2-2, 4-2, 13-2, 15-2.** After the kick the foot returns to its starting place, giving a back stance and an outer block with the arm opposite the front foot (Yonggi). Taekwondo Nation just says "middle block".
- [ ] **Moves 16–17.** Double knife-hand block in back stance (Yonggi, Taekwondo Nation); Taekwondo Nation calls it a one-hand block.
- [ ] **Moves 18–19.** Palm block then punch (Yonggi); Taekwondo Nation says "one-hand middle block" then punch.
- [ ] **Kihap.** On 12-1, the left roundhouse kick (Yonggi only).

## Taegeuk 7 · Chil Jang

Sources: [Yonggi Taekwondo](https://www.sites.google.com/site/yonggitaekwondo/poomse/chil) (25 moves, kihap), [Bob Allen](https://starling.us/wmtkd/bob_allen/taeguek7.html) (33 counts with facing directions), [Taekwondo Nation](https://www.taekwondonation.com/tae-kwon-do-form-7-taegeuk-chil-jang) (20 steps), [Kukkiwon](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1354&page=2&menuLevel=3&menuNo=72). Directions follow Bob Allen; numbering follows Yonggi.

- [ ] **Moves 1 and 3.** Yonggi and Bob Allen have a palm block; Taekwondo Nation has a knife-hand block. **Drawn as a palm block.**
- [ ] **Moves 5–6, stance.** Yonggi and Bob Allen have a back stance with a low knife-hand guarding block; Taekwondo Nation has a front stance with a low knife-hand block. **Drawn as back stance.**
- [ ] **Move 7, turn direction.** Yonggi says "90° clockwise", which would face ra²; Bob Allen and Taekwondo Nation say left. **Drawn facing da².**
- [ ] **Moves 12–13, scissors blocks.** Bob Allen has two scissors blocks per step (normal, then reversed); Yonggi lists one per step. **Drawn as two figures per step** (12-1/12-2, 13-1/13-2). Which arm is high on the first count follows Taekwondo Nation (left middle, right low in a left front stance).
- [ ] **Moves 15-2 and 18-2, cross stance.** Yonggi calls it a "rear cross stance"; Bob Allen calls it a "twisted stance". Drawn as a cross stance with the rear foot tucked behind.
- [ ] **Moves 20–25, horse stance.** Drawn from behind with the feet wide, since Bob Allen has the body facing na. The target kicks (21-1, 23-1) are drawn as front kicks; the real kick is an inward crescent into the palm.
- [ ] **Move 24, stance.** Yonggi says "left stance"; Bob Allen says the body stays in place and only the gaze turns. **Drawn as horse stance.**
- [ ] **Move 25.** Yonggi and Taekwondo Nation have a horse stance and side punch with a kihap; Bob Allen has a right front stance and middle punch. **Drawn as horse stance and side punch, with kihap.**

## Taegeuk 8 · Pal Jang

Sources: [Yonggi Taekwondo](https://www.sites.google.com/site/yonggitaekwondo/poomse/pal-jang) (27 moves), [Bob Allen](https://starling.us/wmtkd/bob_allen/taeguek8.html) (36 counts with facing directions), [Taekwondo Nation](https://www.taekwondonation.com/tae-kwon-do-form-8-taegeuk-pal-jang/) (20 steps), [Kukkiwon](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1355&page=1&menuLevel=3&menuNo=72). Directions follow Bob Allen; numbering follows Yonggi. **This form has the most open questions; check it against the video first.**

- [ ] **Kihaps.** Yonggi has two (3-2 and 19-2, both jumping kicks); Bob Allen has one (3); Taekwondo Nation has two (3 and its step 16). **Drawn with two.**
- [ ] **Move 18, stance and block.** Yonggi has a back stance with an augmented low block; Bob Allen has a tiger stance with a double low block. **Drawn as back stance with augmented low block.**
- [ ] **Move 19-3, which hand blocks.** Yonggi has a left inside block, then a double punch left then right. Bob Allen has a right inside block, then a left punch. **Drawn as right block, left punch, right punch**, mirroring move 3.
- [ ] **Move 27, which hand punches.** Bob Allen says left; Yonggi says right. **Drawn as right**, so the hands alternate after the left elbow and left back-fist.
- [ ] **Moves 5–8, mountain blocks and pulling uppercuts.** Facing directions come from Bob Allen: 5 ra, 6 da, 7 da, 8 ra. The mountain block is drawn as one arm high and one arm low; check the arm shape against the video.
- [ ] **Moves 9–17, where they happen.** Bob Allen has 9–11 facing ga again after the mountain blocks, so the layout places them at the bottom. 12–14 face da² and 15–17 face ra².
- [ ] **Moves 20–27.** Placed on the top bar: 20–23 facing da¹, 24–27 facing ra¹.
- [ ] **Move 1, the augmented outer block.** Bob Allen says the second hand guards the solar plexus. Drawn with that hand under the blocking elbow.
- [ ] **Tiger stance during the knife-hand blocks (12, 15).** Bob Allen calls them high double knife-hand blocks; Yonggi calls them guarding blocks. Drawn at middle height.

---

# Black-belt forms

These three were harder to source than the Taegeuk forms. The Kukkiwon pages give the meaning but not the moves, and several chart sites were unreachable (NBTKDA chart images, Yonggi's Koryo page, Bob Allen). Each sequence below was checked against two or three step lists; the video is the real test. **Review these against the Kukkiwon videos before teaching from them.**

## All three black-belt forms

- [ ] **New floor shapes.** The page template now draws other floor lines besides 王. Koryo is 士 (short start bar, long bar below it, stem continuing to ga). Keumgang is 山 (base bar with three prongs). Taebaek is 工 (two bars joined by the stem). As on the Taegeuk pages, start (na) is at the top, so each glyph is drawn upside down from how it's printed. Check that this matches how you expect to read them.
- [ ] **Side groups are stylised.** On the bars, groups are placed by the order of the moves, not by exact floor position, as in the 王 forms. Taebaek 9–18 is the clearest case: the sources put both groups to one side of the far bar, but the site draws one group on each side.
- [ ] **Notes moved under the board.** These forms need the middle rows for figures, so the four side notes (form note, footprints, belt, how the diagram reads) sit in a box below the floor plan.
- [ ] **Horse-stance figures face the way the body faces.** On the bars, horse-stance and crane-stance figures are drawn facing ga (front view) even though they sit on a side line. Their technique goes to the side: knife-hand side block, target punch, large hinge.
- [ ] **Print sheets for long forms.** The boards are 1,500–1,760 px wide, so page 1 prints at about 0.41–0.48 scale. Page 2 zooms back up and uses tighter rows so the sequence table stays readable (about 7 pt). Check a printed copy for legibility.
- [ ] **Videos.** Koryo links its own Kukkiwon Digital Encyclopedia video (Mookas TV, `keZTTPuXHJo`). I couldn't find individual videos for Keumgang and Taebaek, so `/go/video-keumgang` and `/go/video-taebaek` point to the series playlist. When you find the right video, swap its URL into the JSON and rebuild; the printed QR keeps working.

## Koryo · 고려

Sources: [Blue Dragon TKD](https://www.bluedragontkd.net/taekwondo/poomse/black-belt-forms/koryo.html) (30 numbered steps), [Taekwondo Nation](https://www.taekwondonation.com/tae-kwon-do-black-belt-form-one-koryo) (36 steps, several mislabelled blocks), [MTC Koryo terminology sheet](https://www.martialarts.com.au/mtcmedia/MTC-1st-Dan-Koryo-KoreanWords.pdf) (24 steps), [NBTKDA](https://www.nbtkda.com/koryo) (technique list and kihaps), [Kukkiwon](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1356&page=1&menuLevel=3&menuNo=72). Numbering follows Blue Dragon's 30 steps, which matches Kukkiwon's 30 movements.

- [ ] **Move 2-1 and 6-1, kicking leg.** Blue Dragon and Taekwondo Nation have the **rear** leg doing the double side kick and landing forward. **Drawn as the rear leg.**
- [ ] **Moves 4 and 8, which arm blocks.** Both sources say the arm on the side of the front foot (right arm in 4). **Drawn that way.** Blue Dragon's back-stance names are inconsistent here, so the stance is described by the front foot.
- [ ] **Moves 9–11, the knife-hand block.** Taekwondo Nation calls it a palm block; Blue Dragon, MTC and NBTKDA have a single knife-hand low block. **Drawn as a knife-hand low block.**
- [ ] **Move 13, turn direction.** Taekwondo Nation says turn left; Blue Dragon says step the left foot and turn right. Both end in a right front stance facing na. **The text says "turn 180° toward na" without naming a side.**
- [ ] **Move 15, stance.** Blue Dragon and MTC have the left foot drawn back into a walking stance. **Drawn as walking stance.**
- [ ] **Move 18, cross step.** The ap kkoa seogi before the side kick isn't counted, so it's folded into the kick's instruction rather than drawn as its own figure. Should it get a figure?
- [ ] **Moves 18-2 and 23-2, the low spear hand.** All sources have a turn back toward the centre after the kick. Taekwondo Nation puts the pulling fist at the opposite shoulder; Blue Dragon says "upper shoulder". **Drawn with the fist at the shoulder of the striking arm.**
- [ ] **Moves 20-2 and 25-2, side elbow.** **Drawn facing ga in a horse stance,** with the elbow toward the side you came from and the other palm pushing the fist.
- [ ] **Moves 27–30, strikes and stances.** Blue Dragon has an outer strike in 27 and inward neck strikes in 28–29, with walking stances in 29 and 30. MTC has front stances throughout. **Drawn as Blue Dragon** (walking stances bring you back to the start; four front stances would overshoot).
- [ ] **Kihaps** at 11-3 and 30 (Blue Dragon, NBTKDA, Taekwondo Nation agree).

## Keumgang · 금강

Sources: [Blue Dragon TKD](https://www.bluedragontkd.net/poomse/keumgang/) (27 motions, kihaps at 11 and 21), [Frontline Martial Arts](https://www.frontline-ma.co.uk/Poomsae%20Keumgang.pdf) (27 moves with turn directions), [Phoenix Taekwondo](https://www.phoenixtaekwondo.net/images/poomsae/Poomsae_keumgang.pdf), [Taekwondo Nation](https://www.taekwondonation.com/tae-kwon-do-black-belt-form-two-keumgang/), [NBTKDA](https://nbtkda.com/keumgang) (technique list, timings), [Kukkiwon](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1357&page=1&menuLevel=3&menuNo=72).

- [ ] **Which way the body faces in the mountain-block groups (11–14, 21–24).** No source says so directly. I worked it out from Frontline's turn directions: 11 and 14 face da, 12 and 13 face ra, and the mirror for 21–24. That puts these figures in profile, which is the weakest drawing on the page (a mountain block reads best from the front). **Please check against the video.** If the body faces ga or na there, these become front or back views.
- [ ] **Crane stances (8, 15, 18, 25) face ga,** looking toward the side you're about to travel. Frontline's "90° turn left" at move 8 could mean the body turns, not only the head.
- [ ] **Large hinge.** Drawn with the elbow pointing toward the direction of travel and the other fist across the chest. Blue Dragon describes it as a "hook punch with the elbow back", which could also mean the elbow points away from the travel direction.
- [ ] **360° turns (10, 17, 20, 27).** Blue Dragon says step across with the left foot; Frontline says turn over the left shoulder. The text only says "turn 360° travelling toward da/ra".
- [ ] **Moves 5–7, which hand blocks.** Blue Dragon has the knife hand on the same side as the front foot. **Drawn that way.**
- [ ] **Move 13 and 23, parallel stance.** Drawn as the ready (naranhi) stance with a low spread block. NBTKDA says hold it for about 5 seconds, and the crane-stance diamond blocks for about 8 seconds.

## Taebaek · 태백

Sources: [Blue Dragon TKD](https://www.bluedragontkd.net/taekwondo/poomse/black-belt-forms/taebaek.html) (26 steps), [Taekwondo fandom wiki](https://taekwondo.fandom.com/wiki/Taebaek) (steps 5–8 only, cross-check), [NBTKDA](https://www.nbtkda.com/taebaek) (techniques, kihaps, linking notes), [Korea Taekwondo News](https://koreatkdnews.com/news/article.html?no=17394) (technique order by section), [namu.wiki](https://namu.wiki/w/%ED%83%9C%EB%B0%B1(%ED%92%88%EC%83%88)) (floor line, linking notes), [Kukkiwon](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1358&page=1&menuLevel=3&menuNo=72).

- [ ] **Moves 6–8, grab then punch.** Fandom has the twisting grab done in place (6-1), then a step and punch (6-2). Blue Dragon and Korea Taekwondo News describe the same thing as one motion. **Drawn as two figures per step.**
- [ ] **Move 9, which side first.** Blue Dragon has a 270° turn to the left on the right foot, which faces **ra**. No other source gives a direction. **Drawn facing ra³ first, then da³ from move 14.**
- [ ] **Moves 10–11 and 15–16, stance.** Blue Dragon keeps the back stance for the pulling uppercut and the punch. It may instead slide into a front stance; no second source settles it. **Drawn as back stance.** Check the video.
- [ ] **Move 11 and 16, the punch.** Blue Dragon calls it a side punch; NBTKDA calls it a forward (bandae) punch. **Drawn as a middle punch with the front-side hand.**
- [ ] **Moves 13-1 and 18-1.** NBTKDA has a hammer-fist outer strike together with the side kick. **Drawn in one figure** ("side kick with hammer-fist strike").
- [ ] **Move 21, the wrist release.** The release (japhin sonmok ppaegi) and the turning back-fist are one count in all sources. **Drawn as one figure (the back-fist),** with the release in the instruction.
- [ ] **Moves 23–26 repeat the first line.** namu.wiki notes the first bar is walked twice. Both passes sit on the top bar; 23–26 are placed nearest the centre and at the ends.
- [ ] **Kihaps** at 8-2 and 22 (NBTKDA: third reverse punch and third forward punch; Blue Dragon agrees).

## Pyongwon · 평원

Sources: [Daum cafe 고려 태권도, 고단자품새 – 평원](https://m.cafe.daum.net/KRTGD/VMiG/2?q=D_aSce_-d5P550) (Korean table of all 21 movements with gaze 시선, position 위치, stance, footwork and technique, laid out like the Kukkiwon textbook), [Korea Taekwondo News, 이송학 사범의 품새이야기](https://koreatkdnews.com/news/article.html?no=15437) (a Kukkiwon instructor on the floor line and the Kukkiwon numbering 6-1…6-3, 14-1…14-3), [NBTKDA chart](https://images.squarespace-cdn.com/content/v1/58b45cec6b8f5bc3d705a16e/8db77a22-7733-4089-9e70-e7058773b54d/12+Pyeongwon+Poomsae+Chart+-+NBTKDA+Poomsae+Chart.png) (front leg, hands, kihaps, timings; from [nbtkda.com/pyeongwon](https://www.nbtkda.com/pyeongwon)), [Phoenix Taekwondo step chart](https://www.phoenixtaekwondo.net/images/poomsae/Poomsae_pyongwon.pdf), [Wakeup News](https://www.wakeupnews.co.kr/news/articleView.html?idxno=374) and [maniareport](https://www.maniareport.com/view.php?ud=2022010711314091405e8e941087_19) (floor line 一, new techniques), Taekwondo fandom wiki (cross-check only, search snippets), [Kukkiwon](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1359&page=1&menuLevel=3&menuNo=72) (meaning only; the Kukkiwon floor-line image the cafe embeds, `04_03_12_ex1.jpg`, is no longer on their server). namu.wiki blocked automated reading.

- [ ] **Floor line (fixed 16 Oct).** The first version drew three bars. The Korean sources agree it is one straight line, 一: you start in the middle and move only sideways ("앞뒤로 움직이는 동작이 없으며 모든 동작은 양 옆으로만"). The board now shows one line with five spots from the ra end to the da end; each spot is a column of the counts made there. Where each count stands is worked out from the footwork (the cafe's 위치 column puts 6-3 to 8 at one end and 14-3 to 16 at the other; its other rows are inconsistent), so the spot for the transition counts (6-1, 6-2, 10–13, 14-1, 14-2, 18–21) is approximate.
- [ ] **Numbering (changed 16 Oct).** Now Kukkiwon's 21 movements (Korea Taekwondo News, the cafe table). Where one movement has two techniques they get sub-numbers: 8-1 large hinge and 8-2 high side block, 9-1/9-2 the two back-fists, 12-1 diamond block and 12-2 small hinge, 13-1 side kick and 13-2 elbow, and the mirror 16, 17, 20, 21. The first version used NBTKDA's 14 steps.
- [ ] **Directions.** The cafe's gaze column confirms: 3 faces ra; 4 turns in place to face da; 5–6-2 go toward da; 6-3 to 7 face ra; horse, cross and crane stances (8–12) look toward ra; 13–14-2 go toward ra; 14-3 to 15 face da; 16–20 look toward da; 21 goes toward da.
- [ ] **Moves 9 and 17, the strike.** The cafe has 등주먹 당겨 턱치기 (back-fist, pulling, to the chin) and lists 당겨턱지르기 (pulling uppercut punch) among the new techniques, as do Wakeup News and maniareport; NBTKDA has a pulling back-fist front strike. **Drawn as back-fist strikes** (stamp with pulling back-fist, then the other back-fist). Check against the video: these may be pulling uppercuts.
- [ ] **Moves 8 and 16.** NBTKDA: large hinge, then high augmented side block. The cafe has 거들어 아래막기 at 8 and 거들어 얼굴막기 at 16 (probably a typo at 8); the new-technique lists name 거들어 얼굴옆막기. **Drawn as large hinge (8-1) and augmented high side block (8-2).**
- [ ] **Move 4, knife-hand block.** The cafe has 한손날 몸통 바깥막기 (single knife-hand outer block), in place; NBTKDA "sonnal makgi" with the left arm. **Drawn as a single knife-hand outer block.**
- [ ] **Moves 6-3 and 14-3.** The cafe and Phoenix: 손날 몸통막기 (double knife-hand block); NBTKDA calls it "sonnal geodeureo makgi". **Drawn as the double knife-hand block.**
- [ ] **Moves 9-2 and 17-2, the second back-fist.** Direction not stated. **Drawn striking across the body to the same side.**
- [ ] **Moves 12 and 20, crane stance.** The cafe: 왼학다리서기, 오른발 끌어올려 (standing on the left leg, right foot drawn up) at 12, and the mirror at 20. **Drawn that way.**
- [ ] **Side-kick hands (6-2, 13-1, 14-2).** No source says; drawn with both fists in guard as in Koryo. 21-1 has the hammer-fist strike (NBTKDA; the cafe doesn't list it).
- [ ] **Kihaps** at 9 and 17. NBTKDA puts it on the stamp and back-fist (9-1, 17-1); the cafe puts it after the second strike. **Marked on 9-1 and 17-1.**

## Sipjin · 십진

Sources: [Kukkiwon textbook video, 품새_십진](https://www.youtube.com/watch?v=mcExAWuoj7o) (linked from the [Kukkiwon Korean page](https://www.kukkiwon.or.kr/base/board/read?boardManagementNo=37&boardNo=992&menuLevel=3&menuNo=62); used for facing and travel), [NBTKDA chart](https://images.squarespace-cdn.com/content/v1/58b45cec6b8f5bc3d705a16e/56dc5f82-19eb-4513-b4e4-6f7ab854a69d/13+Sipjin+Poomsae+Chart+-+NBTKDA+Poomsae+Chart.png) (front leg, technique names in Korean, timings, kihaps; from [nbtkda.com/sipjin](https://www.nbtkda.com/sipjin)), [Phoenix Taekwondo step chart](https://www.phoenixtaekwondo.net/images/poomsae/Poomsae_sipjin.pdf) (28 movements, 41 techniques, photo per step), [Wakeup News](https://www.wakeupnews.co.kr/news/articleView.html?idxno=374) (floor line 十, the ten new techniques), Taekwondo fandom wiki (cross-check only: a 28-movement list with directions), [Taekwondo Nation](https://www.taekwondonation.com/learn-tae-kwon-black-belt-five-shipjin) (25 steps, unreliable), [Kukkiwon](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1360&page=1&menuLevel=3&menuNo=72) (meaning). No Korean move table with gaze and position columns was found (namu.wiki blocked; the Daum cafe has only Pyongwon).

- [ ] **Floor line and start.** 十 with the start where the lines cross (fandom: the only form besides Hansu that starts in the middle; the video agrees). Counts 2–11 go out along the bar to da then ra; 12–20 go up the stem toward na; the kicks 21–23 come back down past the start toward ga; 24–28 go back up toward na. **The board puts 12–14, 21-2–23-1, 27, 28 in the row between the crossing and the na end, 15–21-1 at the na end, 23-2–25 below the crossing; spots are approximate.**
- [ ] **The bar is not symmetric.** In the video (as far as its camera cuts allow) the da end is about twice as far from the start as the ra end, because the yoke strike (6) and the closed stance (7) happen on the da side of the start; the footwork simulator agrees. Drawn as two equal halves on the board; the footwork view shows the real offset.
- [ ] **End position.** As described by all sources (26–28 each step forward toward na), the simulator ends about two steps toward na of the start (5.7 foot lengths); the video ends close to the start. One of the 24/25 turn or the kick landings probably travels further toward ga than drawn. **24 is drawn pivoting on the left foot with the right foot stepping back toward ga**, which the video's camera distance supports.
- [ ] **Numbering.** Kukkiwon says 28 movements. The fandom list numbers exactly 28 and matches NBTKDA's 22 counts technique for technique; used with sub-numbers: 3-1 wrist turn, 3-2 spear hand, 3-3/3-4 punches (and 8, 13); 5-1 grab, 5-2 side punch (and 10); 21–23 kick then strike. Bull block's widening pause (fandom 2a) is not drawn.
- [ ] **Wrist turn as its own figure (3-1, 8-1, 13-1).** NBTKDA gives it a count in the back stance (5 s); fandom folds it into the slide to front stance. **Drawn in the back stance, open hand turning, other palm still on the wrist.**
- [ ] **13-3/13-4 punch order.** Fandom: left then right; NBTKDA: right then left (mirrors 8). **Drawn right then left.**
- [ ] **Facing at 4 and 9 (opening mountain block).** Fandom says "turn 90° right"; that would face ga. The video shows the back to camera (facing na) with the side punch going on toward da, and the stepping-forward foot can only lead toward da if the body faces na. **Drawn facing na, looking along the bar.**
- [ ] **Yoke strike (6, 11) gaze.** Not stated. Drawn facing ga, no look direction in the text.
- [ ] **14, knife-hand block.** NBTKDA: 손날 거들어 내려막기 (augmented knife-hand downward block, left arm with right hand assisting); fandom: double knife-hand low block. **Drawn as the augmented low knife-hand block (same as Pyongwon 7).**
- [ ] **16–18 facing.** Fandom: pivot 90° counter-clockwise from facing na (so facing ra), right foot slides back into horse stance across the stem; 19 pivots another 90° to face ga. **Drawn facing ra (side view)**; the video's inset shows a profile. Could equally be read as facing da: check.
- [ ] **Rock push hands (15, 20, 24).** Which hand is high is not stated; sources say "right rock push" each time. **Drawn right hand high, left hand in front of the face.** 15 starts from the hip (side not given); 20 from the right hip (fandom).
- [ ] **19, scooping lift.** Fandom "pull up block", NBTKDA 올려 걸어 막기 (끌어 올리기), Wakeup 걷어올리기. **Named geodeo olligi; drawn as the left forearm lifting in front with the hand open.**
- [ ] **26, ridge-hand block.** NBTKDA: 손날등 거들어 막기 (augmented); the new-technique lists: 손날등몸통막기. **Drawn with the other hand guarding (as the double knife-hand block).**
- [ ] **Kicks 21-1–23-1 hands.** NBTKDA: small hinge (fists at the hip) during each kick. **Drawn with the fists at the opposite hip.**
- [ ] **Kihaps** at 5-2, 10-2 and 23-2 (NBTKDA, Phoenix). All agree.

## Jitae · 지태

Sources: [Kukkiwon textbook video](https://www.youtube.com/watch?v=_BHoCPC_a18) (QR on the [Kukkiwon page](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1361&page=1&menuLevel=3&menuNo=72); used for facing and travel), [NBTKDA chart](https://images.squarespace-cdn.com/content/v1/58b45cec6b8f5bc3d705a16e/07d74705-4b31-41d0-a21b-eb3a76e267ac/14+Jitae+Poomsae+Chart-+NBTKDA+Poomsae+Chart.png) (22 counts: front leg, technique names in Korean, timings, kihaps; notes on [nbtkda.com/jitae](https://www.nbtkda.com/jitae)), [NBTKDA performance guide](https://www.nbtkda.com/p58sec) (June 2024 timing changes), Taekwondo fandom wiki (cross-check only: a 28-movement list with directions), Kukkiwon (meaning, floor line ㅗ). The Phoenix Jitae page no longer exists (404); no Korean move table was found.

- [ ] **Floor line and start.** ㅗ: the base line (earth) at na, a short stem toward ga. You start at the centre of the base line; 1–4 go along it (da, then ra), 5–14 up the stem facing ga, 15–22 at the stem in horse and crane stance, 23-2–24 punch back toward na, 25–28 on the base line again (da, then ra). **On the board 15–23-1 are drawn at the end of the stem.** The footwork simulator puts them only about halfway up it: the horse stance at 15 is formed by moving the left foot back past the right, so the farthest point of the form is 11–12.
- [ ] **End position.** NBTKDA: Jitae finishes about one front stance behind (na of) its start. The simulator agrees (1.9 foot lengths toward na). 25–28 are drawn on the same base line as 1–4.
- [ ] **Numbering.** Kukkiwon says 28 movements. Fandom numbers 28 and matches NBTKDA's 22 counts technique for technique; used with sub-numbers: 2-1 upward block / 2-2 punch (and 4); 7-1 kick / 7-2 block (and 9); 11-1 small hinge / 11-2 diamond punch; 12-1 / 12-2 inside blocks; 14-1 kick / 14-2, 14-3 punches; 20-1 small hinge / 20-2 side kick; 23-1 side kick / 23-2 punch. Note the asymmetry fandom gives: 20 = hinge + kick, but 22 = hinge alone and 23 = kick + punch. **Followed as given.**
- [ ] **11-1, small hinge before the diamond punch.** NBTKDA lists it as its own row (both fists at the right hip, left over right); fandom calls it "lower the left arm to prepare". **Drawn as its own figure, still in the left front stance before the step.**
- [ ] **Facing at 15–22.** Fandom: pivot counter-clockwise, left foot into horse stance; the video (main camera at ga) shows a profile facing da, left side toward na. **Drawn facing da (front-view figures, techniques to the sides): 16 and 21 block toward na, 17, 18, 19 and the 20-2 kick toward ga, the 23-1 kick toward na.** If the body faced ra instead, every side would swap and the punches 23-2, 24 would go toward ga: check.
- [ ] **Hammer-fist target strike (18).** At philtrum height in the sources; **drawn at shoulder height** so the arm does not cross the face (figure rule).
- [ ] **Timings.** NBTKDA chart: 2 and 4 are 4 + 4 s, 8 and 10 are 8 s. NBTKDA's June 2024 update: 8 and 10 changed to 5 s (and the upward block → punch pairs to 4 + 4 s). **Pages say about 4 s for 2/4 and about 5 s for 8 and 10.** Bull block (15) drawn as slow (about 5 s); not stated by the chart.
- [ ] **Move 1 and 3: an palmok (inner-forearm) outer block** per NBTKDA; fandom just "outward block". 8 is the bakkat palmok outer block. **Added "An palmok momtong bakkat makki" to the library.**
- [ ] **6, knife-hand block.** NBTKDA 손날 올려막기 (knife-hand rising block); fandom "single knifehand high block". **Named sonnal ollyeo makki, drawn as the knife-hand high block.**
- [ ] **13, single low knife-hand block** (NBTKDA 손날 내려막기, "step back"); **listed under the existing sonnal arae makki entry.** Fandom says the right foot steps back; drawn so.
- [ ] **10, front stance.** NBTKDA "left shifts"; fandom "slide the left foot back". **Drawn as the left foot sliding forward**, which keeps the footwork in line with the video's travel up the stem.
- [ ] **14-2, 14-3 double punch.** Both sources: land the right foot back behind in a left front stance, right punch first, then left (NBTKDA: the only double punch that starts with the rear hand). Agreed.
- [ ] **Bull block (15).** NBTKDA: different from Sipjin, fists rising straight up hip-width apart, ending between the hands. **Drawn with the Sipjin bull-block pose**; the library text notes the difference.
- [ ] **Side kicks (20-2, 23-1) arms.** NBTKDA: "side kick + small hinge". **Drawn with the fists stacked at the hip during the kick.** 21 sets the right foot down beside the left (closed stance) before lifting the left: not given its own figure.
- [ ] **Kihaps** at 18 (hammer-fist target strike) and 24 (punch), NBTKDA. Fandom agrees.

## Cheonkwon · 천권

Sources: [Kukkiwon textbook video](https://www.youtube.com/watch?v=bGr5_MblBp8) (QR on the [Kukkiwon page](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1362&page=1&menuLevel=3&menuNo=72); used for facing and travel), [NBTKDA chart](https://images.squarespace-cdn.com/content/v1/58b45cec6b8f5bc3d705a16e/8b6f38f6-bcc6-411f-b49c-225980ffd976/15+Cheonkwon+Poomsae+Chart+-+NBTKDA+Poomsae+Chart.png) (21 counts: front leg, Korean names, timings, kihap; performance notes on [nbtkda.com/cheonkwon](https://www.nbtkda.com/cheonkwon)), Taekwondo fandom wiki (cross-check only: a 26-count list with directions), Kukkiwon (meaning, floor line ㅜ). No Korean move table found; the Kukkiwon pages give no movement count.

- [ ] **Movement count.** Not stated by Kukkiwon's pages. Fandom numbers 26 counts and matches NBTKDA's 21 technique for technique; 26 is also the commonly quoted figure. **Page says 26 movements**, sub-numbered: 2-1 opening block / 2-2 uppercut; 4-1 wrist escape / 4-2 punch (and 6); 7-1 twist block / 7-2 wrist escape; 8-1 kick / 8-2 low block; 11-1 swinging block / 11-2 punch (and 12, 14, 15); 18-1 kick / 18-2 punch; 20-1 / 20-2 the two quick-step blocks; 22-1 tornado kick / 22-2 punch; 25 and 26 opening block then push. Check against the Kukkiwon textbook.
- [ ] **Floor line and start.** ㅜ: you start at the foot of the stem (na end), go up it facing ga (1–9), along the bar at the ga end (10–12 toward ra, 13–15 toward da), back down the stem facing na (16–22) and finish near the start (23–26). **Na stays at the top, so the board draws the ㅜ upside down.** The simulator ends 2.5 foot lengths toward ga of the start.
- [ ] **Not drawn as separate figures:** the small hinges before both diamond side punches (NBTKDA 19a, 20b), the overlapped-hands position before each opening block at 25 and 26 (NBTKDA 21c, 21f), and fandom's 1a (hands rising to the chest). Fandom does not number them.
- [ ] **Short front stances (3, 5, 7-1).** NBTKDA: jageun ap gubi, one step shorter than a front stance, the rear foot pointing forward, made by moving the back foot up. Fandom: front stance, "without stepping" at 5 and 7. **Drawn as front stance figures (no separate short-stance chip); descriptions say "short front stance".** At 3 the description has the right foot sliding forward from the tiger stance (NBTKDA "right shifts").
- [ ] **Twisting knife-hand block (3, 5, 7-1).** NBTKDA 손날 비틀어 막기 with no height; Taegeuk 6's similar block is a high block. **New library entry, drawn at chest height.**
- [ ] **10–15 names.** NBTKDA: augmented inner-forearm outer block, swinging block (휘둘러 막기), swing and pull (휘둘러 잡아당기기), forward punches; fandom: augmented outward block, breaking the grip, side punches. **NBTKDA names used; the punches drawn as middle punches in back stance.** 12-1 and 15-1 drawn already in the new stance (the swing is made during the step).
- [ ] **10, the 270° turn.** Fandom: step the left foot and turn 270° counter-clockwise to face ra. Drawn so; the video's camera cut does not show the turn.
- [ ] **20-1 block.** NBTKDA: inner-forearm outer block with the left palm slapping onto the right wrist (안팔목 바깥막기 + 바탕손 눌러막기); fandom: right inward block with a slap. **Drawn as the outer block with the palm on the wrist.** Its stance, nieunja seogi (ㄴ-shaped stance), is **new on the site** (library, footprint, chip and simulator); its figure reuses the back-stance body pose.
- [ ] **Quick steps (20).** NBTKDA: right, left, right, left, the second step closing into the ㄴ-shaped stance, the fourth into back stance. The simulator moves both feet about two foot lengths per figure.
- [ ] **21–22-2 horse stance facing ra**, right side toward na, diamond side punch toward na (from fandom's "land with the right foot forward" and the return direction). **Drawn as front-view figures.** If the stance faced da the punch would be the left: check.
- [ ] **Tornado target kick (22-1)** drawn as a front kick into the left palm, seen from behind (same as Taegeuk 7's target kicks), with the jump carrying the body about two foot lengths toward na.
- [ ] **23–24 mountain blocks.** Fandom: "pivot 180°" from the horse stance; the horse stance faces ra, so 23 is drawn **turning to face ga, left foot forward**, then 24 facing na. The video shows the front at 23 and the back at 24, which agrees. Low hand knife edge, high hand ridge (NBTKDA). 5 s each.
- [ ] **25–26 facing ga** (video). Fandom: left foot slides in to closed stance, then the right foot steps forward into tiger stance; then back and the left foot forward. Mountain push hands: NBTKDA, the hand on the front-foot side low (belt), the other at lip height. **High hand drawn at chest height** so it does not cross the face.
- [ ] **Uppercut (2-2)** drawn at chest height in front view (ends at lip height per NBTKDA), so it does not cover the face.
- [ ] **Kihap** at the side kick 8-1 (NBTKDA, fandom). Only one.

## Hansu · 한수

Sources: [Kukkiwon textbook video](https://www.youtube.com/watch?v=dUHTrwkoYw8) (QR on the [Kukkiwon page](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1363&page=1&menuLevel=3&menuNo=72); confirms the centre-line moves and the diagonal work, though its camera cuts make exact diagonals hard to read), [NBTKDA chart](https://images.squarespace-cdn.com/content/v1/58b45cec6b8f5bc3d705a16e/6c17d898-5159-4952-83a9-7cc315d03561/16+Hansu+Poomsae+Chart+-+NBTKDA+Poomsae+Chart.png) (21 counts: front leg, Korean names, kihaps; notes on [nbtkda.com/hansu](https://www.nbtkda.com/hansu)), Taekwondo fandom wiki (cross-check only: 27 counts with the corner for every move), Kukkiwon (meaning, floor line 水).

- [ ] **Movement count.** Not stated on Kukkiwon's pages. Fandom numbers 27 and matches NBTKDA's 21 technique for technique. **Page says 27 movements**; sub-numbers only for kick + technique pairs (15, 16, 18, 24, 25, 27).
- [ ] **Diagonal directions (new on the site).** 10–27 face the four diagonals, named by the two edges they point between: ga-da (forward-left of the start), na-da, ga-ra, na-ra. **Directions follow fandom's corner for each move**; NBTKDA confirms the diagonal step at 10. The video agrees in general but its camera cuts don't let me check each corner. Diagonal moves are drawn as side views (facing right for da diagonals, left for ra), horse stances as front views.
- [ ] **Floor line 水 on the board.** The centre line holds 1–9; four spokes run from it to the corner groups (na-ra top left, na-da top right, ga-ra bottom left, ga-da bottom right); the moves that come back toward the centre (12–13, 17–18, 21–22, 26–27) sit beside the spokes. Schematic: the minimap uses the simulated positions.
- [ ] **End position.** The simulator ends 3.4 foot lengths toward na of the start. The centre-line part alone (two steps forward, three back, one forward) leaves you about one foot length behind the start before the diagonals begin.
- [ ] **Angled front stance (mo ap kubi) at 3, 5, 7** drawn with the front stance chip; descriptions say "angled front stance". Mountain block with the **rear arm high** (NBTKDA: from the front the rear arm should be hidden); fandom gives no arms.
- [ ] **4, 6, 8 punches.** Fandom: turn the torso square, punch; NBTKDA: "forward stance, reverse punch". Drawn so.
- [ ] **10 and 19 (pressing block + arc-hand strike).** NBTKDA 7: left hand strike, right hand block (and mirrored at 15b). Fandom 19a/19b splits a closed-stance chamber from the strike; **drawn as one figure**, with the feet coming together then stepping out (footwork hint).
- [ ] **Assisting stance (gyeotdari seogi), new on the site** for 11 and 20: library entry, footprint, chip, simulator; the figure reuses the cross-stance body. NBTKDA: the double punch lands with the front foot, as in Taegeuk 7.
- [ ] **12 and 21, low target block.** Horse stance facing na-da (na-ra), the blocking forearm meeting the other palm at the belt (NBTKDA: right arm at 12, left at 21). Which way the body faces in these horse stances is from fandom only: check.
- [ ] **13 and 22, knife-hand diamond block.** NBTKDA 10: left arm low, right arm high (mirrored at 18). Drawn so.
- [ ] **14 and 23 small hinge in crane stance, still facing the ga diagonal and looking toward the na diagonal** (fandom). The side kicks 15-1 and 24-1 go toward the na diagonal.
- [ ] **16-2 and 25-2, stamp + back fist.** NBTKDA: "forward" back-fist strike; fandom: back fist "to the right side of the body". **New library entry (stamp with back-fist strike), drawn forward.** Back cross stance. Kihap on both (NBTKDA, fandom).
- [ ] **17–18 and 26–27 travel across the centre** from one na diagonal toward the opposite ga diagonal (fandom: "you continue that northeastward movement"). Horse at 17 facing na-ra, 18-2 turned to face ga-da (mirrored at 26/27-2), the knife-hand strike and the elbow both toward the ga diagonal ahead. Check against the textbook.
- [ ] **Overlapped-hands start and finish** (gyeopson junbi), as Cheonkwon. Baro: the right foot steps in (fandom; NBTKDA "right steps").

## Ilyeo · 일여

Sources: [Kukkiwon textbook video](https://www.youtube.com/watch?v=GV0TwhH5Hkk) (QR on the [Kukkiwon page](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1364&page=1&menuLevel=3&menuNo=72); **the directions are taken from it**), [NBTKDA chart](https://images.squarespace-cdn.com/content/v1/58b45cec6b8f5bc3d705a16e/3af5ed7c-4182-41bb-92e3-a070c1c87428/17+Ilyeo+Poomsae+Chart+-+NBTKDA+Poomsae+Chart.png) (12 counts: front leg, Korean names, timings, kihaps; notes on [nbtkda.com/ilyeo](https://www.nbtkda.com/ilyeo)), Taekwondo fandom wiki (cross-check only: 23 counts), Kukkiwon (meaning, floor line 卍).

- [ ] **The 卍 glyph.** Kukkiwon's floor line for Ilyeo is 卍, the Buddhist manji (Wonhyo, oneness). The page shows it in the header and the note explains it as the Buddhist symbol. Brian: confirm you are happy to show the glyph, or swap it for a text label.
- [ ] **Movement count.** Not stated on Kukkiwon's pages. Fandom numbers 23 and matches NBTKDA's 12 technique for technique. **Page says 23 movements**; sub-numbers: 9-1 / 9-2 (and 16, 20) twist-and-pull then punch, 19-1 front kick / 19-2 jumping side kick / 19-3 high X block (and 23).
- [ ] **Directions: fandom disagrees with the video; the video is followed.** Fandom turns 90° left at every diamond and knife-hand block and keeps each side kick going straight on; that puts 11 facing da, but the video shows 11–13 facing ga, the side kick 14 going out to da with 15–16 following it, 17 facing na, 18 facing ra (fandom: 180°), 21 facing ga and 22 facing da (fandom: 180°). Read with 卍's four-fold symmetry, each arm is: diamond block facing one way, turn 90° left for the knife-hand block, punch and jump, the side kick 90° further left, then the X block and punch along the kick. Drawn so: 3 ga; 4–6 da; 7–9 na; 10 ra; 11–13 ga; 14–16 da; 17 na; 18–20 ra; 21 ga; 22–23 da. NBTKDA's note that every turn is to the left except the last agrees, and the simulator then ends 0.7 foot lengths from the start.
- [ ] **3, the first diamond block, faces ga** (the video shows the front); drawn as the left foot stepping forward into back stance. Fandom: turn 90° left.
- [ ] **6 and 13, pressing block + spear-hand thrust.** NBTKDA: first time right hand presses, left hand thrusts; second time the other way round. Fandom: right spear hand both times. **Drawn per NBTKDA.** Kihap on both (both sources).
- [ ] **Reverse crane stance (ogeum seogi), new on the site** for 6 and 13: standing on the right leg, the left instep behind the right knee. Library entry, chip and simulator; the figure reuses crane stance with the lifted foot drawn behind. The jumps forward are not given extra travel in the simulator.
- [ ] **7 and 14, side kick with single mountain block** (5 s), drawn with the left arm low over the kicking leg and the right arm high; neither source says which arm is high.
- [ ] **High X block (8, 15, 19-3, 23-3)**: left over right, except 23-3 right over left (NBTKDA: the landing leg decides).
- [ ] **9-1 / 16-1 / 20-1, two-hand twist and pull** drawn as its own figure in back stance (NBTKDA counts it separately; fandom folds it into the step).
- [ ] **18 and 22, fists-at-waist ready** in closed stance, drawn as its own figure (NBTKDA "slowly", not 5 s).
- [ ] **Board.** 卍 drawn with the centre line, the middle bar, a short bar from the centre out to the left at the top (10–13) and to the right at the bottom (3–6), and prongs for the right arm's hook up (17) and the left arm's hook down (21–23). Schematic: groups follow the arms in order, not the exact spots.

## ITF forms (Chang Hon tul) — skeleton only, 18 October 2026

The forms index now has two sections: **World Taekwondo forms** (the Kukkiwon poomsae: Taegeuk and black-belt) and **ITF forms**. The ITF section lists the 24 patterns as planned cards. Each card shows the pattern's floor diagram (its skeleton layout), rank and move count. No ITF pages or print sheets exist yet. The data is `itf` in `data/catalog.json`.

**Sources so far.**
- **Diagrams, counts and ready postures:** a club chart that reproduces the Encyclopedia ("ITF Patterns on Mobile", Taekwon-Do Kildare, 2019).
- **Cross-checks:** the per-pattern pages of the ITF led by Choi Jung Hwa (itf-administration.com), and Kidokwan's article on the diagram origins.
- **Fandom:** not used.
- **Still to do:** check every diagram against a scan of the Encyclopedia / Condensed Encyclopedia before building the first ITF page.

- [x] **URLs.** The paths are `/itf/<name>`. Chon-Ji shipped at `/itf/chon-ji` on 18 Oct 2026, so the scheme is now printed and fixed.
- [ ] **Diagram orientation.** The cards draw each diagram as the Encyclopedia does: **D at the top** (the way the student faces at the start), C at the bottom, B left, A right, with the ready position as a red dot. The Kukkiwon pages put **na at the top with the student facing down the page**, so the two families face opposite ways. Keep the book orientation for ITF, or flip it to match the Kukkiwon pages?
- [ ] **Which ITF.** There are several ITF federations: ITF-HQ in Vienna, the ITF led by Choi Jung Hwa, and others. Neither main body publishes a free per-pattern page or video I could confirm, so the cards carry no reference links yet. Pick the federation whose version the sheets should follow, and its references.
- [ ] **Juche or Ko-Dang (no. 15).** The card shows Juche (45 moves, ITF-HQ). Choi Jung Hwa's ITF uses the name "Kodang" for the same 45 moves. Some schools still teach the original 39-move Ko-Dang, whose diagram I couldn't confirm. Decide the name, and whether to add the 39-move Ko-Dang as an extra card.
- [ ] **Saju Jirugi and Saju Makgi.** These are the 10th-gup fundamental exercises. They aren't among the 24 patterns, so they aren't listed. Add them as a "Fundamental exercises" row?
- [ ] **Ranks.** Each card shows the rank where a pattern is usually learned (Chon-Ji at 9th gup … Tong-Il at 6th dan). Some syllabi list the grade a pattern is tested for instead, which shifts each colour-belt pattern by one. Use your school's syllabus.
- [ ] **Do-San diagram.** The chart draws a stepped half-卍: half a bar from the start to B, the stem to D, then half a bar to E. Yet Do-San's opening moves go to both B and A, so the real floor line probably has a full bottom bar. The card follows the chart for now. It shows no glyph name because the Encyclopedia gives no meaning for this diagram.
- [ ] **Ul-Ji diagram.** Some texts print "⊥". The drawn diagram is a 乙-like zig-zag: start at the D end, half a bar to F, the stem to C, then half a bar to A. That fits "his surname" (乙). The card shows 乙.
- [ ] **Yul-Gok diagram.** The card draws 士 with the two short diagonals from the start shown in the chart. Check against the book.
- [ ] **Yoo-Sin diagram.** The chart shows I with diagonals at both ends. The card draws a plain I until the diagonal directions are confirmed.
- [ ] **Choong-Jang diagram.** Drawn as ⊥ (bar B–A through the start, stem to D, short tail toward C). The Encyclopedia gives no meaning for it.
- [ ] **Juche diagram.** 山 drawn upside down (bar at the D end with the start on it, legs down to F and E, long stem to C). This matches D at the top, the same way the Kukkiwon 王 glyphs read upside down.
- [ ] **Card links.** Each ITF card links to that pattern's page on itf-administration.com (the ITF led by Choi Jung Hwa). I checked all 24 numbers on 18 Oct 2026; that site names pattern 15 "Kodang". The section's references also include the Encyclopedia page of the Vienna ITF. Swap them if you choose the other federation.
- [ ] **Move counts.** The cards follow the Encyclopedia counts. Choi-Yong is listed as 45 on some sites and Tong-Il as 42; I used 46 and 56. Recount each pattern when its page is built.

## Chon-Ji · 천지 (ITF) — 18 October 2026

This is the first ITF page: `/itf/chon-ji`, with a 2-page print sheet.

**Sources.**
- **Sequence:** the official pattern text on the ITF (Choi Jung Hwa) site. It matches, move for move, a club chart that reproduces the Encyclopedia text and diagram (Taekwon-Do Kildare). The ITF Korean technique names come from that chart.
- **Fandom:** not used.
- **Video:** I found no official ITF video. The only YouTube copies are club uploads, so the page cites the two official ITF sites only.

- [ ] **Orientation (the big one).** The board shows the student **facing D, down the page**, the same way the Kukkiwon pages face ga. C is at the top, **B (the student's left) on the right of the page and A on the left**. The ITF books draw the same cross from behind the student, with D at the top, B on the left and A on the right. The page's "How the diagram reads" note says so. Alternatively, flip the ITF boards to the book view, which would put most figures in back view.
- [ ] **Kihap at 17.** The official ITF page marks a kihap after move 17. The Encyclopedia-based chart has none. The page shows it at 17.
- [ ] **Inner forearm middle side block (9, 11, 13, 15)** is drawn with the Kukkiwon outer-block arm, square to the front. In ITF the L-stance body is half-facing. This is a new library entry (`anpalmok`); check its description, especially where the block starts.
- [ ] **Stance drawing.** Walking stance uses the ap kubi figure and footprint; the ITF version has the rear foot turned out about 25° and the front kneecap over the heel. L-stance uses the dwit kubi figure; the ITF niunja sogi has both feet turned in about 15°. The sine-wave motion isn't shown.
- [ ] **L-stance chips name the rear foot**, as the ITF does: "R · Niunja sogi" means the right foot is back. The Kukkiwon back-stance chips name the front foot. Instructions say both ("right L-stance … left foot forward, weight on the right leg").
- [ ] **Names.** Stances and techniques show their ITF names, from a new `itf` field in `data/techniques.json`:
  - Gunnun sogi
  - Niunja sogi
  - Narani junbi sogi
  - Palmok najunde makgi
  - Kaunde jirugi
  - Anpalmok kaunde yop makgi

  The Hangul spellings are mine. Library entries now show an "ITF" line under the Kukkiwon name.
- [ ] **Punches are marked "obverse"** (punching hand on the same side as the front foot). ITF calls this baro, which is the opposite of the Kukkiwon use of baro, so the page uses the English word.
- [ ] **Footwork.** The simulator ends 3.5 foot-lengths behind the start (Kukkiwon forms: 0.6–5.7). The phone minimap snaps each count onto its arm of the cross.
- [ ] **Image briefs** (`design/moves/itf-chon-ji/SPEC.md`) still describe the stances in Kukkiwon terms (ap kubi, dwit kubi). Adjust them before generating ITF figure images.
- [ ] **Print seal.** The 天地 seal in the print header renders badly (an empty box, with the characters spilling below). The Koryo sheet does the same, so it's an older print-CSS issue on every black-belt sheet, not new with Chon-Ji.

## Dan-Gun · 단군 (ITF) — 18 October 2026

`/itf/dan-gun`, with a 2-page print sheet, on the I board: the A–B bar through the start at the top, the stem down to D, and the far E–F bar at the bottom.

**Sources.** The official pattern text (ITF, Choi Jung Hwa) and the Encyclopedia-based chart agree on all 21 movements. The ITF Korean names come from the chart. Fandom was not used. There is no official video.

- [ ] **Kihaps at 8 and 17.** These follow the official ITF page; the chart has none.
- [ ] **270° turns at 9 and 18.** The text says "turning counter-clockwise" toward a side that is on the student's right, so both are drawn as 270° turns to the left with the rear (left) foot swinging round. The instructions say "Turn 270° to the left".
- [ ] **E and F.** E is drawn on the student's right (page left, below A) and F on the left (page right, below B), following the chart's diagram, which has F left and E right with D at the top.
- [ ] **Twin forearm block (9, 11)** is drawn with the front arm upright out in front of the shoulder and the rear arm guarding above the forehead (new library entry `sangpalmok`). Neither source says which arm rises. The front-arm-middle / rear-arm-high version is the common one; check it.
- [ ] **New arm poses for side views:** `sideblk` and `twinhigh`. These keep the forearms clear of the face. Chon-Ji's inner forearm side blocks now use `sideblk` too.
- [ ] **Knife-hand middle outward strike (18, 20)** uses the Kukkiwon knife-hand outer strike (hansonnal bakkat chigi), which is drawn at neck height. ITF says middle (shoulder height).
- [ ] **Knife-hand guarding block (1, 3)** uses the Kukkiwon double knife-hand block figure.
- [ ] **13 and 14** are separate counts in the same stance (low block, then rising block "in a continuous motion"). On the board they are two figures, not one combined card.
- [ ] **Footwork.** The simulator ends 1.8 foot-lengths from the start.

## Do-San · 도산 (ITF) — 18 October 2026

`/itf/do-san`, with a 2-page print sheet.

**Sources.** The official pattern text (ITF, Choi Jung Hwa) and the Encyclopedia-based chart agree on all 24 movements. The chart's Korean labels for 18 and 19 are shifted by one; that's a typo in the chart. Fandom was not used. There is no official video.

- [ ] **Floor line.** The book draws Do-San as a stepped half-卍: half a bar to B, the stem to D, half a bar to E. But the moves go to both ends of both bars and also run along two diagonals. So the board is drawn as Dan-Gun's I:
  - the A–B bar with the start at the top;
  - the stem down to D;
  - the E–F bar at the bottom;
  - the diagonal moves (13–16 toward CE, 17–20 toward CF) beside the stem just above the far bar, without lines (lines there came out almost flat). Their footprints show the diagonal facing.

  The header shows the floor line as "I". The forms-page card still shows the book's stepped shape.
- [ ] **Kihaps at 6 and 22.** These follow the official ITF page; the chart has none.
- [ ] **Moves 3 and 11** ("move the left foot on line AB, then turn clockwise"). Drawn as: the left foot shifts back onto the line and you pivot to face the other way. So 3–4 happen about where 1–2 did, not out at the A end.
- [ ] **Move 9** is a 270° turn to the left, as in Dan-Gun.
- [ ] **Move 7.** Twist the right hand free, then turn a full circle counter-clockwise and step forward. It's drawn as one figure (the back fist).
- [ ] **Fingertip thrust (6).** The left hand is drawn under the right elbow, as in the Kukkiwon spear-hand thrust. The texts don't say where the other hand goes.
- [ ] **High wedging block (13, 17)** uses the Kukkiwon middle wedge figure; the ITF block is high.
- [ ] **Back fist high side strike (7, 8)** uses a new ITF-only arm, `bfside`. In front view the fist is foreshortened beside the head, clear of the face. The Kukkiwon front-view back fists (T5 6-2, 7-2, 8; Sipjin 23-2) still cross the face; that's a separate question.
- [ ] **Sitting-stance knife-hand strikes (23, 24)** are drawn in front view facing D, with the strike to the side, as Koryo does. The table's direction column shows D.
- [ ] **Front snap kicks (14, 18)** keep both arms in the wedging block, as the text says.
- [ ] **Footwork.** The simulator ends 2.2 foot-lengths from the start.

## History page (/history/) — 18 October 2026

This is a short history in our own words. It's checked against the Kukkiwon's History of Taekwondo, its 1970s chronology and its introduction page, the Vienna ITF's history page and World Taekwondo's 2017 rebrand notice. Those five pages are linked at the bottom of the history page. These points rest on general knowledge rather than those pages, so check them:

- [ ] **The five kwans** are named as Chung Do Kwan, Moo Duk Kwan, Song Moo Kwan, Chang Moo Kwan and Ji Do Kwan (first called Yun Moo Kwan). Oh Do Kwan (1954, Choi Hong Hi and Nam Tae Hi) is mentioned separately. Accounts differ on which schools count as the "original five".
- [ ] **KTA "after a few years under another name"**: this refers to the Korea Taesoodo Association period (about 1962–65). It's deliberately vague; confirm or drop it.
- [ ] **Taegeuk and the black-belt poomsae replaced the Palgwe forms.** The page gives no year for this, because sources give 1967 for Palgwe and 1971–72 for Taegeuk.
- [ ] **ITF dates:** headquarters to Toronto in 1972 and later to Vienna, work with North Korea from 1980, the Encyclopedia in 1983, the 2001–2002 split, and the 2014 WT–ITF agreement.
- [ ] **Olympics:** demonstration sport in 1988 and 1992, medal sport from 2000. The Kukkiwon page calls 1988 an "official event"; the page says demonstration.
- [ ] **ATA (1969) and GTF (1990)** each get one line. Add or remove branches as you like.
- [ ] **The family-tree diagram** at the top simplifies a lot: it shows the ITF and the Kukkiwon/WTF as two branches of the KTA. Say if it is too simple for your students.

---

_Taegeuk items generated while building Taegeuk 5–8, and black-belt items while building Koryo, Keumgang and Taebaek, both on 13 October 2026. Add new items under the form they belong to._
