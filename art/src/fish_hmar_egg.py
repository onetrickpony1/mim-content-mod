"""Hmar (grey triggerfish, Balistes capriscus) spawn egg: the item icon (16 x 16), 2026-11-19.

Started by the owner's rule (docs/Decisions/2026-11-18 Approving a step starts the next; skorfna bucket.md): the
hmar's bucket was accepted (docs/Decisions/2026-11-19 Night fish icons and buckets - most pass; John Dory,
gallinella, lingwata bucket redo.md), which starts its egg.

The owner's egg rules, all kept here (docs/Tools and Process/Art pipeline.md, "Fish art: lessons learnt"):
- vanilla's egg outline, measured from vanilla 26.x's fish eggs (art/src/fish_egg_common.py EGG): nothing breaks
  it but the trigger on top;
- a stylised egg in the animal's palette with only its key features (the owner's favourite, the boll egg B):
  - the trigger: the one stout dark spine (o) at the front of the back, a small pale sail of membrane f behind it,
    standing on the egg's top the way the skorfna egg's comb does;
  - the faint darker saddles (q K) on the olive-grey flank, as two soft blotches never level with each other, over
    the pale cream-grey belly (s W);
  - the egg lit from the top left (L h), the outline the icon's own: H on the lit side, o in the shade;
  - the side flaps as the soft fins in the icon's fin olives F V.
- no eye, no face, no pair of level dark dots.
- vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only): P in the grids.

Colours: only the accepted icon A's (art/src/fish_hmar_icon.py PAL), plus vanilla's pool. Nothing new.

Candidates (the sheet shows all of them; PICK is written to the mod):
- A, two blotches: two soft saddle blotches (q round a K centre), one high at the front, one low behind.
- B, dark blotches: A's blotches bigger and darker (K).
- C, trigger and back: A with the back's darker top (U F) round the trigger.
- C2: C with critic round 1's fixes (see its comment).
- C3: C2 with critic round 2's fixes, the trigger on the front shoulder (see its comment).
- C4, the PICK: C3 with critic round 3's fixes, the trigger raked back (see its comment). All three critic rounds
  failed; C4 is installed as the best try.

The critic rounds and blind reads, word for word: docs/Creatures and Plants/Night log/hmar.md, "Egg".

Run:    art/.venv/bin/python art/src/fish_hmar_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/hmar_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_hmar_egg.png (the compare sheet) and the offline hotbar previews
        art/candidates/fish_hmar_egg_hotbar.png and fish_hmar_egg_hotbar_x4.png (art/tools/hotbar_preview.py,
        GUI scale 2 and 4, nothing selected).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_hmar_icon import PAL as ICON  # noqa: E402  (accepted icon A)
import fish_egg_common as common  # noqa: E402

FISH = "hmar"
TITLE = "Hmar (grey triggerfish) spawn egg: textures/item/hmar_spawn_egg.png"

PAL = {k: ICON[k] for k in "oOZHTKqmUFnfpsLWVh"}

POOL = common.pool_rows("o")

CANDIDATES = {
    # round 0 (the maker's own look at 1x): the first grids' spine continued the egg's narrow top into a point and
    # the saddles, long bands running up to the top, made the egg a striped garlic bulb; the spine is now dark o
    # with a pale sail f behind it, and the saddles are two soft blotches, one high at the front and one low behind,
    # never level, on a paler flank (s p)
    "A": [
        "................",
        "......o.........",
        "......off.......",
        "......HHHo......",
        ".....HLLUFo.....",
        "....HLqqLsUo....",
        "....HqKqssUo....",
        "...HLssqsssUo...",
        "..HLspssqqsUUo..",
        "..HspsssqKqUUo..",
        ".FHsWsspsqqUUoV.",
        ".FHWWWssppsUUoV.",
        ".VHsWWsspppUUoO.",
    ] + POOL,
    "B": [
        "................",
        "......o.........",
        "......off.......",
        "......HHHo......",
        ".....HLLUFo.....",
        "....HLqKqsUo....",
        "....HqKKqsUo....",
        "...HLqKqsssUo...",
        "..HLspqsqKqUUo..",
        "..HspssqKKKqUo..",
        ".FHsWsspqKqUUoV.",
        ".FHWWWssppsUUoV.",
        ".VHsWWsspppUUoO.",
    ] + POOL,
    "C": [
        "................",
        "......o.........",
        "......off.......",
        "......HHHo......",
        ".....HUUUFo.....",
        "....HLUqUUFo....",
        "....HqKqssUo....",
        "...HLssqsssUo...",
        "..HLspssqqsUUo..",
        "..HspsssqKqUUo..",
        ".FHsWsspsqqUUoV.",
        ".FHWWWssppsUUoV.",
        ".VHsWWsspppUUoO.",
    ] + POOL,
}
# C2: critic round 1 (FAIL, pick C) and its fixes: the trigger is one stout raked wedge, dark o two pixels wide at
# its base (7,2), stepping down to the back's U (8,2) (the pale sail f vanished on the slot grey); the blotches' dark
# K cores softened to q (6,6) (9,9), and three pale p specks on the flank made s (4,8) (3,9) (7,10), so the egg reads
# smooth-skinned, not as a mottled skorfna or grouper.
CANDIDATES["C2"] = common.patched(CANDIDATES["C"], {(7, 2): "o", (8, 2): "U", (6, 6): "q", (9, 9): "q", (4, 8): "s",
                                                    (3, 9): "s", (7, 10): "s"})
# C3: critic round 2 (FAIL: still an onion with a point; C2 looked like A B C at 1x) and its fixes: the egg keeps
# vanilla's rounded 4 px top and the trigger moves off the top onto the front (upper left) shoulder, a short stout
# spine o at (5,2) (5,3) beside the top, not on the centre line; the top-left crown lit L (6,3) (6,4) so it reads round
# instead of a dark cap.
CANDIDATES["C3"] = common.patched(CANDIDATES["C2"], {(6, 1): ".", (6, 2): ".", (7, 2): ".", (8, 2): ".", (5, 3): "o",
                                                     (5, 2): "o", (6, 3): "L", (6, 4): "L"})
# the only pixels allowed outside the egg: the trigger and its sail on top (C3: the trigger on the front shoulder)
FIN = {n: {(6, 1), (6, 2), (7, 2), (8, 2)} for n in CANDIDATES}
FIN["C3"] = {(5, 2), (5, 3)}
# C4, installed: critic round 3 (FAIL: the upright spine read as the left outline carrying on, a lopsided cone; at 1x
# still like A to C2) and its fixes: the spine a 2 px thorn raked back over the crown, root (5,3) and tip (6,2), with
# a dark root o on the shoulder (5,4); the pale belly wider (6,10) (6,11) W. Not judged again (three rounds was the
# limit), so it waits for the owner as the best try.
CANDIDATES["C4"] = common.patched(CANDIDATES["C3"], {(5, 2): ".", (6, 2): "o", (5, 4): "o", (6, 10): "W", (6, 11): "W"})
FIN["C4"] = {(5, 3), (6, 2)}
DARK = "oZHT"  # the marks that must never pair up level, like eyes
PICK = "C4"

if __name__ == "__main__":
    common.run(FISH, TITLE, PAL, CANDIDATES, FIN, DARK, PICK, os.path.abspath(__file__))
