"""Gallinella (tub gurnard, Chelidonichthys lucerna) spawn egg: the item icon (16 x 16), 2026-11-19.

Started by the owner's rule (docs/Decisions/2026-11-18 Approving a step starts the next; skorfna bucket.md): the
owner passed its icon (the second redo, the fin growing out of the side) (docs/Decisions/2026-11-19 Redos pass - lionfish, lizz bucket, petrica, gallinella icon; John Dory
bucket again.md), which starts its egg.

The owner's egg rules, all kept here (docs/Tools and Process/Art pipeline.md, "Fish art: lessons learnt"): vanilla's
fish-egg outline (art/src/fish_egg_common.py EGG) standing in vanilla's own pool (art/src/egg_pool.py, the owner's
exception to "never copy", for the pool only; P in the grids); a stylised egg in the fish's palette carrying only its
key features, never the whole fish squeezed in; no eye, no face, no pair of level dark dots, nothing phallic, no pale
point in front at eye height (a beak), no band across the middle (a Pokeball). The eye-pair check is the line-aware one
in art/src/fish_egg_lines.py (bars and stripes touch, so only lone dark dots count).

Key feature, the owner's: the big turquoise "wing" (the pectoral fin) with its bright blue scalloped rim, spread as a
fan over the egg's lower right, three dark rays meeting at one root, breaking the outline a little at the right; the
red-orange egg lit at the top left around it, with a small pale belly low on the front (kept small: a big pale patch
on a red egg is the marzpan's).

Colours: only the accepted icon's (textures/item/gallinella.png) plus the model texture's pale peach #fcc8a0 (p),
plus vanilla's pool.

Candidates: A the wing on the right, B a bigger wing on the right, C the wing on the left; B2, B3 and B4 (the PICK)
are B with the fixes of critic rounds 1-3 (see the comments at their grids).

The critic rounds and blind reads, word for word: docs/Creatures and Plants/Night log/gallinella.md, "Egg".

Run:    art/.venv/bin/python art/src/fish_gallinella_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/gallinella_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_gallinella_egg.png (the compare sheet: the candidates at 8x, 1x and 2x beside
        vanilla's fish eggs, our accepted fish eggs and the fish's own icon) and the offline hotbar previews
        art/candidates/fish_gallinella_egg_hotbar.png and fish_gallinella_egg_hotbar_x4.png (art/tools/hotbar_preview.py,
        GUI scale 2 and 4, nothing selected).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fish_egg_common as common  # noqa: E402
from fish_egg_lines import check_marks  # noqa: E402

common.check_marks = check_marks
# the sheet also shows the eight fish eggs the owner passed on 2026-11-19 ([[2026-11-19 Spawn eggs - all eight pass]])
TODAY = ("kavall", "marzpan", "tird", "sawt", "trilja", "hmar", "lingwata", "mola_mola")
common.ACCEPTED = tuple(common.ACCEPTED) + tuple(n for n in TODAY if n not in common.ACCEPTED)


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


FISH = "gallinella"
TITLE = "Gallinella (gurnard) spawn egg: textures/item/gallinella_spawn_egg.png"
PAL = {k: hx(v) for k, v in {
    "C": "#8c3424", "E": "#b04a30", "F": "#b84430", "G": "#c84e34", "H": "#e0583a", "K": "#e4644a",
    "M": "#f8a070", "p": "#fcc8a0",
    "D": "#2f7a74", "J": "#45a090", "N": "#80d4c4", "L": "#3a8ae8", "O": "#7cc4fa",
}.items()}
POOL = common.pool_rows("C")
TOP = [
    "................",
    "................",
    "................",
    "......CCCC......",
    ".....CMMKHC.....",
    "....CMMKKHGC....",
    "....CMKKHHGC....",
    "...CMKKHHHGFC...",
]
CANDIDATES = {
    "A": TOP + [
        "..CMKKHHJNNNOL..",
        "..CKKHHJNJNNNOL.",
        ".GCppHGDJNJNNOL.",
        ".GCppGFDJJNJNOL.",
        ".FCpGFFDDJJNNOL.",
    ] + POOL,
    "C": TOP + [
        "..LONNNJHHHGFC..",
        ".LONNNJNJHHGFC..",
        ".LONNJNJDHGGFCF.",
        ".LONJNJJDGGFECF.",
        ".LOJJNJDDGFFECE.",
    ] + POOL,
}
CANDIDATES["B"] = common.patched(CANDIDATES["A"], {(9, 7): "J", (10, 7): "N", (11, 7): "N", (12, 7): "O",
                                                   (13, 7): "L", (13, 8): "O", (14, 8): "L", (15, 10): "L",
                                                   (15, 11): "L"})
FIN = {"A": {(14, 9)}, "B": {(13, 7), (14, 8), (14, 9), (15, 10), (15, 11)}, "C": {(1, 9)}}
# B2: critic round 1's fixes for B (FAIL: "a flat teal patch, not a fin with rays ... stuck on like a sticking
# plaster"; the pale belly "is marzpan's exact recipe"): the wing all light turquoise N with three dark rays J
# spreading from its root at the lower middle; the root tapered (no straight D column); the pale belly shrunk to two
# pixels; one more blue scallop on the rim (14,9) O
CANDIDATES["B2"] = common.patched(CANDIDATES["B"], {
    (9, 11): "J", (9, 10): "J", (10, 9): "J", (10, 8): "J", (10, 7): "J", (10, 11): "J", (11, 10): "J", (12, 9): "J",
    (11, 12): "J", (12, 11): "J",
    (9, 7): "N", (9, 8): "N", (11, 8): "N", (9, 9): "N", (11, 9): "N", (10, 10): "N", (12, 10): "N", (11, 11): "N",
    (10, 12): "N",
    (7, 9): "H", (8, 8): "H", (8, 10): "D",
    (4, 10): "K", (4, 11): "G", (3, 10): "M",
    (14, 9): "O"})
FIN["B2"] = FIN["B"]
DARK = "CD"
# B3: critic round 2's fixes for B2 (narrow FAIL: "The rays read as a checker or diamond net, not a fan"; the top
# edge "a straight horizontal line"; the rim blending into the pool): three rays (up, up-right, flat) meeting at one
# root near (9-10,11); the root narrowed; the top-left corner tapered so the fan widens toward the rim; the rim's
# lowest pixel turned dark teal, apart from the pool
CANDIDATES["B3"] = common.patched(CANDIDATES["B2"], {
    (11, 12): "N", (12, 11): "N", (11, 11): "J", (12, 12): "J", (9, 12): "D", (9, 7): "H", (9, 8): "J",
    (13, 12): "J"})
FIN["B3"] = FIN["B2"]
# B4, the PICK: critic round 3's fixes for B3 (narrow FAIL: the dark root pixels "make a hard L-shaped dark frame"
# that "reads as the edge of a patch or a hole"): the body takes back both root corners, so the root narrows to the
# one pixel (7,11) where the rays meet, and the fan's top-left is tapered
CANDIDATES["B4"] = common.patched(CANDIDATES["B3"], {(7, 10): "G", (7, 12): "F", (8, 9): "H"})
FIN["B4"] = FIN["B3"]
PICK = "B4"

if __name__ == "__main__":
    common.run(FISH, TITLE, PAL, CANDIDATES, FIN, DARK, PICK, os.path.abspath(__file__))
