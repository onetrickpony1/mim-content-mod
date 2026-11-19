"""Petrica (petriċa, anglerfish, Lophius) spawn egg: the item icon (16 x 16), 2026-11-19.

Started by the owner's rule (docs/Decisions/2026-11-18 Approving a step starts the next; skorfna bucket.md): the
owner passed its model (the redo) (docs/Decisions/2026-11-19 Redos pass - lionfish, lizz bucket, petrica, gallinella icon; John Dory
bucket again.md), which starts its egg.

The owner's egg rules, all kept here (docs/Tools and Process/Art pipeline.md, "Fish art: lessons learnt"): vanilla's
fish-egg outline (art/src/fish_egg_common.py EGG) standing in vanilla's own pool (art/src/egg_pool.py, the owner's
exception to "never copy", for the pool only; P in the grids); a stylised egg in the fish's palette carrying only its
key features, never the whole fish squeezed in; no eye, no face, no pair of level dark dots, nothing phallic, no pale
point in front at eye height (a beak), no band across the middle (a Pokeball). The eye-pair check is the line-aware one
in art/src/fish_egg_lines.py (bars and stripes touch, so only lone dark dots count).

Key features: the mottled khaki camouflage (a darker mottled back, a small cream underside low on the front, 2x2 dark
blotches never level with each other) and the fishing rod: a thin dark crook growing out of the front shoulder and
reaching up and forward, with a small pale lure hanging from its tip; pale fan fins on the sides. The petriċa lies
flat on land, but the egg follows its icon and its normal fish shape in water, not a pancake. Its wide mouth is left
out (a face).

Colours: only the accepted icon's (textures/item/petrica.png), plus vanilla's pool.

Candidates: A a short rod arching forward, B A with a pale fan fin at the lower left, C A with a longer lure; B2, B3
and B4 (the PICK) are B with the fixes of critic rounds 1-3 (see the comments at their grids).

The critic rounds and blind reads, word for word: docs/Creatures and Plants/Night log/petrica.md, "Egg".

Run:    art/.venv/bin/python art/src/fish_petrica_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/petrica_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_petrica_egg.png (the compare sheet: the candidates at 8x, 1x and 2x beside
        vanilla's fish eggs, our accepted fish eggs and the fish's own icon) and the offline hotbar previews
        art/candidates/fish_petrica_egg_hotbar.png and fish_petrica_egg_hotbar_x4.png (art/tools/hotbar_preview.py,
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


FISH = "petrica"
TITLE = "Petrica (anglerfish) spawn egg: textures/item/petrica_spawn_egg.png"
PAL = {k: hx(v) for k, v in {
    "B": "#1a120c", "C": "#5a3c28", "D": "#5e3f2a", "E": "#745437", "F": "#805f3d", "G": "#8f6943",
    "H": "#9b764e", "I": "#ae8458", "J": "#bd915e", "K": "#d9bc9c", "L": "#d8c8a0",
}.items()}
POOL = common.pool_rows("C")
BODY = [
    "......CCCC......",
    ".....CJIHFC.....",
    "....CJHHJHFC....",
    "....CIJHHFEC....",
    "...CHHFHJHFEC...",
    "..CJHEEHIHFEEC..",
    "..CHFEHHHFJFEC..",
    ".ICHHHJFFEEFECI.",
    ".GCIJHFFEJEEDCG.",
    ".GCFHFEEFEEDDCF.",
]
ROD = [
    "................",
    "....EE..........",
    "...E..E.........",
]
CANDIDATES = {
    "A": common.patched(ROD + BODY + POOL, {(3, 3): "L"}),
    "B": common.patched(ROD + BODY + POOL, {(3, 3): "L", (0, 11): "K", (0, 12): "I", (1, 10): "I", (1, 11): "K"}),
    "C": common.patched(ROD + BODY + POOL, {(3, 3): "L", (3, 4): "K"}),
}
FIN = {"A": {(4, 1), (5, 1), (3, 2), (6, 2), (3, 3)}}
FIN["B"] = FIN["A"] | {(0, 11), (0, 12)}
FIN["C"] = FIN["A"] | {(3, 4)}
# B2: critic round 1's fixes for B (FAIL: "a brown potato or tied sack"; the rod "a small loop ... invisible", the
# lure "a lone bright speck"): a longer, darker rod D rising from the top and arching forward, the lure a 2 px pale
# bulb hanging straight down clear of the egg (never sticking out sideways, which reads as a beak); the upper left
# lit khaki with dark 2 px blotches instead of even 1 px noise; a shaded fan fin on the right too
CANDIDATES["B2"] = common.patched(CANDIDATES["B"], {
    (3, 2): ".", (6, 2): ".", (3, 3): ".", (4, 1): ".", (5, 1): ".",
    (7, 2): "D", (6, 1): "D", (5, 0): "D", (4, 0): "D", (3, 1): "D", (2, 2): "D", (2, 3): "D",
    (2, 4): "L", (2, 5): "J",
    (6, 4): "J", (5, 5): "J", (6, 5): "J", (5, 6): "J", (6, 6): "K",
    (5, 8): "D", (6, 8): "D", (9, 10): "D", (10, 10): "D", (7, 11): "D", (8, 11): "D",
    (15, 11): "I", (15, 12): "G", (14, 10): "I", (14, 11): "J"})
FIN["B2"] = {(7, 2), (6, 1), (5, 0), (4, 0), (3, 1), (2, 2), (2, 3), (2, 4), (2, 5), (0, 11), (0, 12), (15, 11),
             (15, 12)}
# B3: critic round 2's fixes for B2 (FAIL: the closed arch reads as "a handbag strap, or a sack with a drawstring
# tag", and at 1x it is "nearly the same as the cod egg"): the rod opened, starting at the front shoulder and reaching
# up and forward with only one end touching the egg, the lure hanging from its tip above the head; a darker mottled
# back over a small cream belly low on the front (the model's cream underside, not a band); bigger 2x2 blotches; the
# left fin dimmer and back to vanilla's flap width, so the top-left light still wins
CANDIDATES["B3"] = common.patched(CANDIDATES["B2"], {
    (7, 2): ".", (6, 1): ".", (5, 0): ".", (2, 2): ".", (2, 3): ".", (2, 4): ".", (2, 5): ".",
    (4, 4): "D", (4, 3): "D", (3, 2): "D", (3, 1): "D", (2, 1): "D", (1, 2): "D", (1, 3): "L", (1, 4): "K",
    (8, 4): "E", (9, 5): "E", (10, 6): "E", (11, 7): "E", (11, 8): "E", (10, 5): "D",
    (3, 11): "L", (4, 11): "L", (4, 12): "L", (5, 12): "K",
    (8, 7): "D", (9, 7): "D", (8, 8): "D", (9, 8): "D",
    (0, 11): "J", (0, 12): ".", (1, 11): "J",
    # the maker's own look at 8x: the 2 px blotch at (5-6,8) sat level with the new 2x2 one at (8-9,7-8), a pair of
    # eyes over the low blotch as a mouth, so it is lit khaki instead
    (5, 8): "H", (6, 8): "I"})
FIN["B3"] = {(4, 4), (4, 3), (3, 2), (3, 1), (4, 0), (2, 1), (1, 2), (1, 3), (1, 4), (0, 11), (15, 11), (15, 12)}
DARK = "BCD"
# B4, the PICK: critic round 3 (PASS on B3) and its fixes: the rod's leftover top pixel (4,0) gone, so the rod is
# one clean crook, not a knot ("most of the remaining drawstring read"); the lure a small bulb lit from above (K over
# J) instead of a tag; a darker outline pixel where the rod grows out of the shoulder
CANDIDATES["B4"] = common.patched(CANDIDATES["B3"], {(4, 0): ".", (1, 3): "K", (1, 4): "J", (5, 4): "E"})
FIN["B4"] = FIN["B3"] - {(4, 0)}
PICK = "B4"

if __name__ == "__main__":
    common.run(FISH, TITLE, PAL, CANDIDATES, FIN, DARK, PICK, os.path.abspath(__file__))
