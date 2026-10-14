# Review list — Taegeuk 1–8

Everything below is either a place where sources disagree or a choice no source settled. Each item says what the site shows now. Tick an item when you've checked it against your school's practice or the Kukkiwon video; if the site needs to change, note the fix and the move id (e.g. `T5 5-1`).

To change a form, edit `forms/taegeuk-N.json` and run `python3 tools/build_form.py forms/taegeuk-N.json --print`.

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

_Generated while building Taegeuk 5–8 on 13 October 2026. Add new items under the form they belong to._
