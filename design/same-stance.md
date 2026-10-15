# Same-stance moves (issue #4): three treatments to compare (15 October 2026)

**The problem:** 61 of the 363 counts in the built forms keep the stance from the count before and change only the arms. Examples: block then punch, double punches, back-fist then punch with the feet in place. Today each one is a full new figure, so the reader has to work out what changed.

## How other diagrams handle it
These are the techniques printed manuals and notation systems use for "the body holds, a limb moves":

- **Step-by-step frames** (kata and poomsae books): one full figure per count. Clear, but the reader compares near-identical figures. This is what the site does today.
- **Ghosting or chronophotography** (Marey-style multiple exposure, sports coaching sheets): the earlier position drawn faint behind the new one, in one frame.
- **Motion arrows** (instructional and safety-card illustration): a curved arrow from the limb's start to its end. The eye follows the path, not two pictures.
- **Unchanged parts de-emphasised** (technical illustration, IKEA-style assembly steps): what stays put is greyed so the change stands out.
- **Numbered overlays** (dance notation, play diagrams): several positions in one picture, each numbered in order.

The three prototypes combine these differently.

## The prototypes
Each one is live on any form page through the URL. Use `?same=off` to turn them off:

| | `?same=a` · **A. Carry-over** *(recommended)* | `?same=b` · **B. Combined card** | `?same=c` · **C. Inset strip** |
|---|---|---|---|
| On the board | Every count keeps its own card. Legs are drawn light, a dashed red arc runs from where the acting hand was to where it lands, and the card is marked "same stance". | One card per stance. Earlier counts are light "ghost" arms, and every count is numbered at its acting hand. The cards for the later counts are removed. | The first count is drawn in full. Later counts become small arm-only thumbnails (no legs, no footprint), marked "same stance". |
| Phone and study panel | Same as the board. | The combined figure, with the current count's number filled red. | Full figures (the thumbnails are a board-only device). |
| Strengths | Keeps "one figure per count". The board layout and print size don't change. The arc shows the path, not just the end point. | Fewest figures: a 3-count step reads as one picture. Good for double punches. | The change stands out by size. The board is a little narrower. |
| Weaknesses | Still one figure per count, so long chains (Pal Jang 3-3 to 3-5) take space. | Breaks one-figure-per-count. Ghost arms overlap in front view (Pal Jang 3-3 to 3-5), and the card labels get long. | Thumbnails lose the footprint and the floor line. Small arm thumbnails are hard to read at print scale. |

Screenshots (from `tools/check/same.py`):

| Form | A | B | C |
|---|---|---|---|
| Taegeuk Il Jang, board | [A](same-stance/taegeuk-1-a-board.png) | [B](same-stance/taegeuk-1-b-board.png) | [C](same-stance/taegeuk-1-c-board.png) |
| Taegeuk Pal Jang, board | [A](same-stance/taegeuk-8-a-board.png) | [B](same-stance/taegeuk-8-b-board.png) | [C](same-stance/taegeuk-8-c-board.png) |
| Pal Jang 27 on a phone | [A](same-stance/taegeuk-8-a-phone.png) | [B](same-stance/taegeuk-8-b-phone.png) | [C](same-stance/taegeuk-8-c-phone.png) |

## Detection
A count carries its stance when its stance, lead foot, facing, view and side all match the count before it, and neither count is a kick or the ready stance. That catches 67 counts. Six of them move the feet even though the stance doesn't change, so they are marked `"carry": false` in the form data:

- T7 25: steps forward into a new horse stance.
- T8 7: crosses the feet and steps out.
- Keumgang 10, 17, 20, 27: 360° turns into the large hinge.

That leaves 61. The footwork simulator (#3) will check these per move, so the overrides can go once it lands.

## To decide
1. Pick A, B or C (or a mix: for example A on the board and B on phones).
2. Once picked, set it as the default (the `same` field per form, or the template default), drop the switch, update the legend, rebuild all forms and check the print sheets still fit on 2 pages.
