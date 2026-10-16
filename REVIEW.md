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

Sources: [NBTKDA chart](https://images.squarespace-cdn.com/content/v1/58b45cec6b8f5bc3d705a16e/8db77a22-7733-4089-9e70-e7058773b54d/12+Pyeongwon+Poomsae+Chart+-+NBTKDA+Poomsae+Chart.png) (14 steps with sub-counts, front leg, hands, kihaps, timings; from [nbtkda.com/pyeongwon](https://www.nbtkda.com/pyeongwon)), [Phoenix Taekwondo step chart](https://www.phoenixtaekwondo.net/images/poomsae/Poomsae_pyongwon.pdf) (21 movements / 29 techniques, same order), Taekwondo fandom wiki (cross-check only: steps 1–4 with turn directions, from search snippets; the page itself wouldn't load), [Kukkiwon](https://www.kukkiwon.or.kr/eng/board/read?boardManagementNo=55&boardNo=1359&page=1&menuLevel=3&menuNo=72) (meaning only). NBTKDA and Phoenix agree on every stance and technique in order. **No source gives a direction for every move, so check this form against the video before teaching from it.**

- [ ] **Directions.** Only the first steps are stated (fandom: turn right into back stance for the low knife-hand block, then the horse stance "looking right, pivot counterclockwise"). The rest follow from the order of the techniques and the mirror symmetry of the two halves: 1-3 faces ra; 2-1 to 3-2 travel toward da; 3-3 to 9-2 face and travel toward ra; 9-3 to 14-2 face and travel toward da. Horse, cross and crane stances face ga.
- [ ] **Move 2-1, knife-hand block.** NBTKDA has a left-arm "sonnal makgi" and Phoenix a "knife hand block" (the photo shows one hand). **Drawn as a single knife-hand block (hansonnal bakkat makki), the other hand at the hip.**
- [ ] **Moves 3-3 and 9-3.** NBTKDA calls them "sonnal geodeureo makgi" (assisted knife-hand block); Phoenix calls them a double knife-hand block. **Drawn as the double knife-hand block** (sonnal momtong makki) already in the library.
- [ ] **Moves 5-2 and 11-2, the second back-fist.** NBTKDA: "left fist strike + right arm assist" after the right back-fist. The direction isn't stated. **Drawn striking across the body to the same side (ra in 5-2, da in 11-2)**, the other arm across the chest.
- [ ] **Moves 5-1 and 11-1, stamp.** The stamping foot (right, then left) comes down in horse stance; the figure doesn't show the stamp itself, only the instruction does.
- [ ] **Moves 7 and 13, crane stance.** NBTKDA's "front leg" column says Right at 7 and Left at 13, which we read as the **lifted** leg, because the side kick that follows is made with that leg (8-1 right, 14-1 left). **Drawn standing on the left leg at 7 and the right leg at 13.**
- [ ] **Side-kick hands (3-2, 8-1, 9-2).** No source says; drawn with both fists in guard as in Koryo. 14-1 has the hammer-fist strike (NBTKDA).
- [ ] **Floor plan.** The floor line is one straight line (一). The board shows it as three passes along that line (out and toward da, back toward ra, toward da again), so the three bars are the same line, not three lines. Positions on the minimap are approximate.
- [ ] **Numbering.** Follows NBTKDA's 14 steps with sub-numbers (34 figures); Kukkiwon counts 21 movements.
- [ ] **Kihaps** at 5-1 and 11-1 (NBTKDA and Phoenix agree).

---

_Taegeuk items generated while building Taegeuk 5–8, and black-belt items while building Koryo, Keumgang and Taebaek, both on 13 October 2026. Add new items under the form they belong to._
