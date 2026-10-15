# Model sheets v3: prompts for the Higgsfield web app

Ready-to-paste prompts for the third round of the model sheets, built from Brian's comments in #9–#16 and what went wrong in v2.

## How to use this

1. **Model:** pick an image model on your unlimited plan that accepts reference images: **GPT Image** (best at following "change only X"), **Nano Banana** or **Seedream 4.5**. Use **3:2** for the sheets, **2:3** for single figures, and the highest resolution offered.
2. **References:** attach the files listed under each prompt. They're in this repo; download them from GitHub (open the file, then "Download raw file"):
   - `design/models/directions/d10-realistic-anatomical-CHOSEN.png` (the chosen character)
   - `design/models/ms-v2/…` (the v2 sheets being edited)
3. **Save as** the file name given under each prompt, into `design/models/ms-v3/`. Commit it, or attach it to the sheet's issue. I'll check each one against the comments and post the results.
4. **Order:** single figures first (MS-3, MS-4, MS-7 front row), because the sheet prompts that follow use them as references.

### What changed from v2
- **Edit where v2 was close.** Edits keep what's already right: MS-1, MS-2, MS-5, MS-6, MS-7 side row, MS-8.
- **One figure per image for the hard stances** (MS-3 dwit kubi, MS-4 beom seogi, MS-7 front-row kicks). In v2 the models lost the geometry when drawing several views at once. Generate one view, check it, then use it as the reference for the other views.
- **No footprint panels.** Footprints will be drawn exactly in SVG on the site (they're the same shapes as the footwork diagrams, #3), so the image models no longer draw them.
- **The same character block** opens every prompt, so the style stays consistent across models.

### Character block (already included in each prompt)
> Same character and drawing style as the reference image: realistic anatomical ink figure drawing, fine line, light cross-contour shading, white background; adult, 7.5 heads tall; faceless head with short dark hair and simple realistic ears; white dobok with black V-collar; black belt with knot and tails; bare feet. VIEW NAMES: FRONT = the viewer stands where the face looks (the direction of motion); BACK = opposite; SIDE = 90° to that.

### Arms block (stance sheets)
> Both fists rest on top of the belt at the SIDES of the waist (not the front), about 2 inches further back than relaxed, elbows drawn back behind the body line, forearms level, fists palm-up (palm side facing up, knuckles down). No punch, no block.

---

## MS-1 · Basic stances (edit) → `ms1-basic-stances-v3.png`
**Attach:** `ms-v2/ms1-basic-stances-v2.png`
**Prompt:**
```
Edit the attached image. Keep every figure, stance, label and position exactly the same. Make the figures larger to fill their cells (same 3 x 3 grid, less empty space between columns).
Change ONLY the arms in all nine figures: both fists rest on top of the belt at the SIDES of the waist, not at the front corners, about 2 inches further back than now, elbows drawn back behind the body line, forearms level, fists palm-up (palm side facing up, knuckles down). In the SIDE views the near fist sits palm-up on the belt at the back half of the hip. No other changes.
```

## MS-2 · Ap kubi (edit) → `ms2-ap-kubi-v3.png`
**Attach:** `ms-v2/ms2-ap-kubi-v2.png`
**Prompt:**
```
Edit the attached image. Keep the FRONT, SIDE and BACK figures, the knee bends, the straight rear leg, the foot angles and the labels. REMOVE the TOP-DOWN FOOTPRINT panel and its captions entirely; spread the three figures evenly across the width.
Changes:
1. Narrower stance in the FRONT and BACK views: the side-to-side distance between the two feet (centre to centre) equals the shoulder width plus 2 inches, so each foot sits just outside the line of its shoulder. The stance length front to back stays the same.
2. Arms in all three figures: both fists on top of the belt at the SIDES of the waist, 2 inches further back than now, elbows drawn back, fists palm-up. In the SIDE view the near fist is clearly palm-up at the back half of the hip.
No other changes.
```

## MS-3 · Dwit kubi (new, one view at a time)
The stance (same in every view): left foot forward.
- **Feet:** the front (left) foot points straight ahead, in the direction the face looks. The rear (right) foot is turned 90° out. The feet make an L, with the front heel set about 1.5 inches back from the rear heel's line, toward the rear-foot side. About 1½ foot lengths from front toes to rear heel.
- **Weight:** about 70% on the rear leg, which is deeply bent with the knee pushed out over the rear toes. The front knee is slightly bent and the front foot is light.
- **Body:** hips and chest turned 90° toward the rear-foot side; the head turns to look straight over the front foot.

### 3a · SIDE view alone → `ms3a-dwit-kubi-side-v3.png` (2:3)
**Attach:** `directions/d10-realistic-anatomical-CHOSEN.png`
**Prompt:**
```
Same character and drawing style as the reference image: realistic anatomical ink figure drawing, fine line, light cross-contour shading, white background; adult, 7.5 heads tall; faceless head with short dark hair and simple realistic ears; white dobok with black V-collar; black belt; bare feet.
ONE full-body figure, DWIT KUBI (back stance), seen so that the CHEST and HIPS face the viewer squarely.
The stance runs left to right across the picture: the FRONT foot is on the viewer's RIGHT and points to the right (toes to the right, seen from its inner side); the REAR foot is on the viewer's LEFT, turned to point straight at the viewer (we see its toes). Distance from front toes to rear heel: about one and a half foot lengths.
About 70 percent of the weight on the REAR leg: the rear knee is deeply bent and pushed out to the viewer's LEFT, directly over the rear toes; the hips sit low over the rear foot. The front leg is only slightly bent and light, the front heel barely touching.
Torso upright. The head is turned 90 degrees to look to the viewer's RIGHT, over the front foot (profile of the head).
Both fists rest on top of the belt at the sides of the waist, palm-up, elbows drawn back.
No text, no logos.
```

### 3b · FRONT view alone → `ms3b-dwit-kubi-front-v3.png` (2:3)
**Attach:** `ms3a-dwit-kubi-side-v3.png` (once it's right) + `d10-…CHOSEN.png`
**Prompt:**
```
Same character, stance and drawing style as the first reference image, now seen from the FRONT: the viewer stands where the face looks.
The face looks straight at the viewer. The FRONT (left) foot points straight at the viewer, close to the centre line. Because the hips and chest are turned 90 degrees, the torso is seen side-on: the figure's LEFT shoulder and left arm are nearest the viewer, the chest faces the viewer's LEFT. The REAR (right) foot is behind, turned 90 degrees, pointing to the viewer's LEFT; the rear knee is bent and pushed out to the viewer's left over the rear toes, carrying most of the weight, so the hips sit low and toward the rear foot.
Both fists on the belt at the sides of the waist, palm-up, elbows back.
No text, no logos.
```

### 3c · BACK view alone → `ms3c-dwit-kubi-back-v3.png` (2:3)
**Attach:** `ms3a-…` + `ms3b-…`
**Prompt:**
```
Same character, stance and drawing style as the reference images, now seen from the BACK: the viewer stands behind the figure, opposite to where the face looks. We see the back of the head. The torso is seen side-on: the figure's RIGHT shoulder is nearest the viewer, the chest faces the viewer's RIGHT. The REAR (right) foot is nearest the viewer, turned 90 degrees and pointing to the viewer's RIGHT, its knee bent and pushed out over the toes carrying most of the weight; the FRONT foot is farther away, pointing straight away from the viewer.
Both fists on the belt at the sides of the waist, palm-up.
No text, no logos.
```

### 3d · Assemble the sheet → `ms3-dwit-kubi-v3.png` (3:2)
**Attach:** `ms3b`, `ms3a`, `ms3c`
**Prompt:**
```
Combine the three attached figures into one model sheet on white, unchanged, same scale, standing on one faint floor line, in this order with labels underneath: FRONT, SIDE, BACK. Title above in small capitals: DWIT KUBI (BACK STANCE). No other text.
```

## MS-4 · Beom seogi (new, one view at a time)
The stance (same in every view): left foot forward.
- **Feet:** very short. The front heel is about 2 inches behind the line of the rear toes, so the feet overlap front to back; they're side by side, about a fist apart.
- **Rear foot:** flat with the heel down, turned out about 30°. It carries almost all the weight, and its knee is well bent.
- **Front foot:** only the ball and toes touch the floor; the heel is raised clearly; the knee is bent and drawn slightly in.
- **Body:** hips about 45°, torso upright, sitting low like a cat ready to spring.

### 4a · SIDE view alone → `ms4a-beom-seogi-side-v3.png` (2:3)
**Attach:** `d10-…CHOSEN.png` + `ms-v1/ms4-beom-seogi.png` (its SIDE figure was the closest)
**Prompt:**
```
Same character and drawing style as the first reference image: realistic anatomical ink figure drawing, fine line, light cross-contour shading, white background; adult, 7.5 heads tall; faceless head with short dark hair and simple realistic ears; white dobok with black V-collar; black belt; bare feet.
ONE full-body figure in BEOM SEOGI (tiger stance), seen in profile, facing the viewer's RIGHT, posed like the SIDE figure of the second reference image but corrected:
- The feet are very close: the front heel is about 2 inches BEHIND the toes of the rear foot (the feet overlap in length).
- REAR foot (left in the picture): FLAT on the floor with the HEEL DOWN, carrying almost all the body weight; the rear knee is clearly bent and the hips sit low over the rear foot.
- FRONT foot (right in the picture): only the BALL of the foot and the toes touch the floor, the HEEL is RAISED high; the front knee is bent.
- Torso upright, chin level, looking to the right.
Both fists on top of the belt at the sides of the waist, palm-up, elbows drawn back.
No text, no logos.
```

### 4b · FRONT view alone → `ms4b-beom-seogi-front-v3.png` (2:3)
**Attach:** `ms4a-…` + `d10-…CHOSEN.png`
**Prompt:**
```
Same character, stance and drawing style as the first reference image, now seen from the FRONT (the face looks at the viewer). Both knees bent and the hips low. The front (left) foot is nearer the viewer, only its ball and toes on the floor with the heel visibly lifted, its knee bent and drawn slightly toward the centre. The rear (right) foot is just behind and to the side, flat, turned out about 30 degrees, carrying the weight. The hips are turned about 45 degrees, so the right hip is a little farther away. Both fists on the belt at the sides, palm-up.
No text, no logos.
```

### 4c · BACK view alone → `ms4c-beom-seogi-back-v3.png` (2:3)
**Attach:** `ms4a-…` + `ms4b-…`
**Prompt:**
```
Same character, stance and drawing style as the reference images, now seen from the BACK. The rear (right) foot is nearest the viewer: flat, heel down, turned out about 30 degrees, knee bent, carrying the weight. The front foot is just ahead, only its ball on the floor, the raised heel visible from behind. Hips low and turned about 45 degrees. Both fists on the belt at the sides.
No text, no logos.
```

### 4d · Assemble → `ms4-beom-seogi-v3.png` (3:2)
Same as 3d, with the title BEOM SEOGI (TIGER STANCE).

## MS-5 · Juchum and kkoa seogi (edit) → `ms5-juchum-kkoa-v3.png`
**Attach:** `ms-v2/ms5-juchum-kkoa-v2.png`
**Prompt:**
```
Edit the attached image. Keep all six figures, labels and layout. Keep the horse-stance SIDE view and both BACK views as they are.
Changes:
1. JUCHUM SEOGI FRONT and BACK views: turn BOTH FEET INWARD so the toes point slightly toward each other (about 15 degrees), knees still pushed out over the feet.
2. KKOA SEOGI FRONT view: redraw the legs to match the KKOA SEOGI BACK view: the LEFT foot planted flat, pointing forward; the RIGHT leg crosses BEHIND the left leg, with only the BALL of the right foot on the floor just outside the left heel; both knees bent and pressed together. The legs do NOT cross at the knees with the feet apart.
3. KKOA SEOGI SIDE view: the same foot position, the right foot clearly behind the left heel, on its ball.
Arms unchanged (fists on the belt). No other changes.
```

## MS-6 · Hakdari seogi (edit) → `ms6-hakdari-v3.png`
**Attach:** `ms-v2/ms6-hakdari-v2.png`
**Prompt:**
```
Edit the attached image. Keep the three figures (FRONT, SIDE, BACK), the arms (fists on the belt), the upright torso and the labels.
Changes in all three views:
1. The STANDING right leg is BENT at the knee like the front leg of a front stance: knee forward over the toes, shin angled forward, the body lower than now.
2. The LIFTED left leg: the left knee still points FORWARD, but lift the foot HIGHER so it sits right BESIDE the standing knee: the SOLE of the left foot faces DOWN toward the floor (horizontal), and the INNER EDGE of the left foot just touches the inner side of the right knee. The foot is not hanging toe-down at shin height.
No other changes.
```

## MS-7 · Kicks
### 7a · Side row (edit) → `ms7a-kicks-side-v3.png`
**Attach:** `ms-v2/ms7-kicks-v2.png`
**Prompt:**
```
Edit the attached image. Keep the TOP ROW only and remove the bottom row; keep AP CHAGI and MUREUP CHIGI exactly as they are.
YEOP CHAGI: the body leans away in ONE STRAIGHT LINE with the kicking leg (no twist like a roundhouse); hips stacked, seen side-on; the kicking foot is TENSE AND FLAT, the sole facing the target, toes pulled back, the outer edge (foot blade) and heel leading, heel slightly higher than the toes; the supporting foot turned so its HEEL points toward the target.
DOLLYEO CHAGI: the supporting foot FULLY PIVOTED so its HEEL points at the target; hips turned over; strike with the instep, toes pointed.
No other changes.
```

### 7b · Front row, one kick per image (2:3), all with the target where the viewer stands
**Attach:** `d10-…CHOSEN.png` + `7a`
- **Ap chagi FRONT** → `ms7b-ap-front-v3.png`
  ```
  Same character and style as the references. FRONT view of AP CHAGI (front kick) at full extension: the right leg kicks straight toward the viewer at chest height; we see the BALL OF THE FOOT nearest us, the TOES PULLED BACK hard (toes pointing up), the knee and shin foreshortened behind it; the supporting foot flat; guard arms. No text.
  ```
- **Yeop chagi FRONT** → `ms7b-yeop-front-v3.png`
  ```
  Same character and style as the references. FRONT view of YEOP CHAGI (side kick) at full extension, the kick coming straight at the viewer: we see the SOLE of the right foot nearest us, foot horizontal, the outer edge (foot blade) at the bottom and the heel leading; the leg foreshortened straight behind it; the torso leaning away to one side behind the leg; the supporting foot turned away. No text.
  ```
- **Dollyeo chagi FRONT** → `ms7b-dollyeo-front-v3.png`
  ```
  Same character and style as the references. FRONT view of DOLLYEO CHAGI (roundhouse kick) at the moment of impact, the target where the viewer stands: the right leg swings round horizontally at head height from the viewer's left, striking with the INSTEP (top of the foot), toes pointed; the hips are turned over; the SUPPORTING FOOT is fully pivoted so its HEEL points at the viewer. No text.
  ```

### 7c · Assemble → `ms7-kicks-v3.png` (3:2)
**Attach:** `7a` + the three `7b` images + `ms-v2/ms7-kicks-v2.png` (for the mureup front figure)
```
Combine into one sheet on white, 2 rows x 4 columns, same scale, labels as in the last reference image: top row the four side views (AP CHAGI, YEOP CHAGI, DOLLYEO CHAGI, MUREUP CHIGI) from the first image; bottom row the front views: AP, YEOP and DOLLYEO from the next three images, and MUREUP CHIGI front from the last image. Figures unchanged.
```

## MS-8 · Hands and feet (edit, then highlight)
### 8a · Plain → `ms8-hands-feet-v3.png`
**Attach:** `ms-v2/ms8-hands-feet-v2.png`
**Prompt:**
```
Edit the attached image. Keep the layout, labels and every hand and foot drawing except the ones listed:
1. RIDGE HAND (SONNAL DEUNG): palm facing DOWN, fingers straight and together, the THUMB TUCKED UNDER the palm, so the inner edge on the index-finger side forms a clean ridge.
2. ARC HAND (KALJAEBI): PALM FACING DOWN, the four fingers straight and TOGETHER, the THUMB spread wide apart, the hand forming an open V between thumb and index finger; seen from above at a slight angle.
3. All eight FEET: redraw about 25 percent LESS realistic than the hands: cleaner outlines, fewer veins and tendons, lighter shading, simpler toes. Same poses.
No other changes.
```

### 8b · Highlighted → `ms8-hands-feet-highlight-v3.png`
**Attach:** `ms8-hands-feet-v3.png` (from 8a)
**Prompt:**
```
Reproduce the attached image EXACTLY, nothing moved or redrawn. The ONLY change: tint the striking or blocking surface of each item with a translucent signal-red overlay (about 45 percent opacity, crisp edge, the ink lines visible through it):
FIST front, side, back: the first two knuckles (index and middle). KNIFE HAND: the outer edge, little-finger side, from the base of the little finger to the wrist. RIDGE HAND: the inner edge, index-finger side, from the index knuckle to the base of the thumb. SPEAR HAND: the fingertips. PALM HEEL: the heel of the palm. ARC HAND: the inner side of the index finger and the web between thumb and index finger. BACK FIST: the backs of the first two knuckles, on the hand itself, NOT the sleeve.
Feet: SIDE, FRONT, BACK and TOP-DOWN: no tint. BALL OF FOOT: the pad under the toes. FOOT BLADE: the outer edge from the little toe back to the heel. INSTEP: the top of the foot. HEEL: the back and underside of the heel.
```

---

## Checklist per sheet
After each image, compare it with its issue: MS-1 #9 · MS-2 #10 · MS-3 #11 · MS-4 #12 · MS-5 #13 · MS-6 #14 · MS-7 #15 · MS-8 #16. When a single-figure view is right, keep it: it becomes the pose reference for the rig (#7) even if the assembled sheet comes out messy.
