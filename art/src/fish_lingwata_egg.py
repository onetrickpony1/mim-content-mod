"""Lingwata (common sole, Solea solea) spawn egg: the item icon (16 x 16), 2026-11-19.

Started by the owner's rule (docs/Decisions/2026-11-18 Approving a step starts the next; skorfna bucket.md): the
lingwata's bucket was accepted, which starts its egg.

The owner's egg rules, all kept here (docs/Tools and Process/Art pipeline.md, "Fish art: lessons learnt"):
- vanilla's egg outline, measured from vanilla 26.x's fish eggs (art/src/fish_egg_common.py EGG); nothing breaks it;
- a stylised egg in the animal's palette with only its key features (the owner's favourite, the boll egg B):
  - the fringe fin that runs right round a sole's body: a pale band just inside the outline, F at the upper left,
    1 on the shaded side, all round the egg;
  - the sandy body a step darker (2 lit at the upper left, 3) with the icon's scattered dark speckles m, one to a row
    so no two ever stand level (no pair of eyes);
  - the side flaps in the fringe's own tones.
- no eye, no face, no pair of level dark dots; the dark-tipped pectoral is left out (a dark dot on a pale patch reads
  as an eye).
- vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only): P in the grids.

Colours: only the accepted icon I's (art/src/fish_lingwata_icon.py PAL), plus vanilla's pool. Nothing new.

Candidates (the sheet shows all of them; PICK is written to the mod):
- A, plain fringe: the pale band round the egg, smooth.
- B, wide fringe: A with the band two pixels wide on the lit upper left, where the icon's fringe is widest.
- C, ticked fringe: A with the fin rays ticked in f every other pixel, as the icon's fringe.
- C2: C with critic round 1's fixes (see its comment).
- C3, the PICK: C2 with critic round 2's polish (see its comment).
- D: C2 with the tail fan at the upper right shoulder (see its comment); critic round 2 and the blind readers read
  it as a stalk on a potato or a tied sack, so it is not used.

The critic rounds and blind reads, word for word: docs/Creatures and Plants/Night log/lingwata.md, "Egg".

Run:    art/.venv/bin/python art/src/fish_lingwata_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/lingwata_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_lingwata_egg.png (the compare sheet) and the offline hotbar previews
        art/candidates/fish_lingwata_egg_hotbar.png and fish_lingwata_egg_hotbar_x4.png (art/tools/hotbar_preview.py,
        GUI scale 2 and 4, nothing selected).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_lingwata_icon import PAL as ICON  # noqa: E402  (accepted icon I)
import fish_egg_common as common  # noqa: E402

FISH = "lingwata"
TITLE = "Lingwata (common sole) spawn egg: textures/item/lingwata_spawn_egg.png"

PAL = {k: ICON[k] for k in "OKFf123mtT"}

POOL = common.pool_rows("O")

CANDIDATES = {
    # round 0 (the maker's own look at 1x): the first grids' body was as pale as the fringe, a plain potato; the body
    # is now the darker 2 3 and the fringe the palest F 1, darkest outline O on the shaded side
    "A": [
        "................",
        "................",
        "................",
        "......KKKK......",
        ".....KFFF1O.....",
        "....KF22231O....",
        "....KF2m231O....",
        "...KF2233331O...",
        "..KF22333m331O..",
        "..KF2m3333331O..",
        ".FKF3333m3331O1.",
        ".fKF333333m31O1.",
        ".fKFF11111111Ot.",
    ] + POOL,
    "B": [
        "................",
        "................",
        "................",
        "......KKKK......",
        ".....KFFF1O.....",
        "....KFF2231O....",
        "....KF2m231O....",
        "...KFF233331O...",
        "..KFF2333m331O..",
        "..KF2m3333331O..",
        ".FKF3333m3331O1.",
        ".fKF333333m31O1.",
        ".fKFF11111111Ot.",
    ] + POOL,
    "C": [
        "................",
        "................",
        "................",
        "......KKKK......",
        ".....KFfF1O.....",
        "....KF2223fO....",
        "....Kf2m231O....",
        "...KF223333fO...",
        "..Kf22333m331O..",
        "..KF2m333333fO..",
        ".FKf3333m3331O1.",
        ".fKF333333m3fO1.",
        ".fKFf1f1f1f1fOt.",
    ] + POOL,
}
# C2: critic round 1 (FAIL, pick C) and its fixes: the fringe carries on down the shaded right side (12,8) (12,10) f,
# so it reads as a ring all round and not as rim light; the base row is one shaded fringe f (7,12) (9,12) (11,12)
# instead of a crimped f/1 pie crust; the lone tick on the lit upper left (5,6) is F again.
CANDIDATES["C2"] = common.patched(CANDIDATES["C"], {(12, 8): "f", (12, 10): "f", (7, 12): "f", (9, 12): "f",
                                                    (11, 12): "f", (5, 6): "F"})
# C3, the pick: critic round 2 (PASS, pick C2) and its polish: a darker shade band t just inside the shaded right
# fringe (10,7) (11,8) (11,9) (11,10), so the body rounds from the top left to the bottom right and the f fringe
# shows as a pale ring between t and the outline O; the lone f tick in the lit cap (7,4) is plain fringe F.
CANDIDATES["C3"] = common.patched(CANDIDATES["C2"], {(10, 7): "t", (11, 8): "t", (11, 9): "t", (11, 10): "t",
                                                    (7, 4): "F"})
# D: C2 with the sole's small round tail fan (the icon's T t) at the upper right shoulder, the one signature part the
# critic named that could break the outline (the cawl egg carries its tail the same way)
TAIL = {(11, 4): "t", (11, 3): "T", (12, 3): "T", (12, 2): "t", (13, 2): "t", (13, 3): "t"}
CANDIDATES["D"] = common.patched(CANDIDATES["C2"], TAIL)
FIN = {n: set() for n in CANDIDATES}  # nothing outside the egg but D's tail
FIN["D"] = set(TAIL)
DARK = "Om"  # the marks that must never pair up level, like eyes
PICK = "C3"

if __name__ == "__main__":
    common.run(FISH, TITLE, PAL, CANDIDATES, FIN, DARK, PICK, os.path.abspath(__file__))
