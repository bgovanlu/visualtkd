# Footwork diagrams (issue #3), 15 October 2026

**Brief:** your example from #3 (`refs/footwork-example-issue3.png`) is a kata-book "Footwork Diagram". It shows the whole form on its line, a footprint for every position numbered by the step, dotted lines for the path of each moving foot, small circles where a foot pivots, and letters for the directions.

## What's built
Everything is behind `?footwork` on any form page (e.g. `/taegeuk/1/?footwork`) until you approve it.

1. **Floor simulator** (`templates/footwork.js`). It works out where both feet are after every count from data the forms already have: stance, lead foot, facing, and the instruction text.
   - The foot named in the instruction ("step back with the right foot") moves and the other foot stays planted. When no foot is named, the shorter step wins, and on a tie the lead foot steps.
   - Kicks keep the standing foot planted. "Land, then turn" lands the kicking foot first.
   - "Feet in place", "without stepping" and same-stance counts hold. "Pivot in place", jumps and "travelling toward …" move both feet.
   - Stance sizes, in foot lengths:

     | Stance | Long | Wide | Rear foot turned out |
     |---|---|---|---|
     | Ap seogi | 1.6 | 0.4 | 15° |
     | Ap kubi | 2.7 | 0.85 | 30° |
     | Dwit kubi | 2.1 | heels in line | 90° |
     | Beom seogi | 1.1 | — | — |
     | Juchum seogi | feet 2.4 apart | | |

   - A `step` field on a move overrides the rules where needed.
2. **Per-move footwork glyph:** the circle beside each figure. Previous footprints are dashed outlines, new ones filled (red = lead or standing foot), a dashed red arrow shows the step, and a dashed blue ring marks a pivot. The blue tick is the facing. Na is always up.
3. **Whole-form plan:** a "Footwork" section under the study panel, in the style of your example. Every footprint is numbered by the count that placed it, and steps are dashed arrows. The selected count is red, and the outlined pair is where you stand after it. Click a footprint to jump to that count.

## Checks
`python3 tools/check/footwork.py` runs the simulator on every form and reports how far it ends from the start. Forms return to their start, so a large number means a misplaced step. `python3 tools/check/footwork.py taegeuk-7` lists every count. Results and open questions are in REVIEW.md. Il Jang's plan comes out as the 王 on its own, which is a good sign the rules are right.

## Next, once approved
- Make the glyph the default (it replaces the static footprint glyph) and show the plan on every form page.
- Replace the hand-placed minimap `pos` with simulated positions.
- Decide whether the plan goes on print page 2.
