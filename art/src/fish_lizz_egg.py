"""Lizz (European barracuda, Sphyraena sphyraena) spawn egg: the item icon (16 x 16), 2026-11-19.

Started by the owner's rule (docs/Decisions/2026-11-18 Approving a step starts the next; skorfna bucket.md): the
owner passed its bucket (A, after the redo) (docs/Decisions/2026-11-19 Redos pass - lionfish, lizz bucket, petrica, gallinella icon; John Dory
bucket again.md), which starts its egg.

The owner's egg rules, all kept here (docs/Tools and Process/Art pipeline.md, "Fish art: lessons learnt"): vanilla's
fish-egg outline (art/src/fish_egg_common.py EGG) standing in vanilla's own pool (art/src/egg_pool.py, the owner's
exception to "never copy", for the pool only; P in the grids); a stylised egg in the fish's palette carrying only its
key features, never the whole fish squeezed in; no eye, no face, no pair of level dark dots, nothing phallic, no pale
point in front at eye height (a beak), no band across the middle (a Pokeball). The eye-pair check is the line-aware one
in art/src/fish_egg_lines.py (bars and stripes touch, so only lone dark dots count).

Key features: countershading, a dark slate back lit at the top left over a silver belly on the lower front, a small
dorsal fin raked back off the top, and two short staggered dark bars on the upper back (the barracuda's oblique
bars). The jutting lower jaw is left out (a pale point in front reads as a beak), and so is the forked tail (at the
top right it made the egg a grey sardina).

Colours: the accepted icon's (textures/item/lizz.png) and the model texture's dark back #3c5662 (k), plus vanilla's
pool.

Candidates: A two small dorsal fins far apart, B the dark forked tail at the top right, C B with faint bars; A2, A3
and A4 (the PICK) are A with the fixes of critic rounds 1-3 (see the comments at their grids).

The critic rounds and blind reads, word for word: docs/Creatures and Plants/Night log/lizz.md, "Egg".

Run:    art/.venv/bin/python art/src/fish_lizz_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/lizz_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_lizz_egg.png (the compare sheet: the candidates at 8x, 1x and 2x beside
        vanilla's fish eggs, our accepted fish eggs and the fish's own icon) and the offline hotbar previews
        art/candidates/fish_lizz_egg_hotbar.png and fish_lizz_egg_hotbar_x4.png (art/tools/hotbar_preview.py,
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


FISH = "lizz"
TITLE = "Lizz (barracuda) spawn egg: textures/item/lizz_spawn_egg.png"
PAL = {k: hx(v) for k, v in {
    "C": "#46545b", "B": "#3d5560", "D": "#445866", "E": "#4f6b77", "G": "#607888", "J": "#86a3ae",
    "H": "#6c7a80", "I": "#7a868b", "L": "#9aa6aa", "M": "#a3b2b8", "O": "#c4d0d4", "p": "#dde5e7", "Q": "#eef3f2",
    "k": "#3c5662",  # the model texture's dark back (entity/fish/lizz.png)
}.items()}
POOL = common.pool_rows("C")
BODY = [
    "......CCCC......",
    ".....CJJGEC.....",
    "....CJJGGEDC....",
    "....CJGGEEDC....",
    "...CJGGEEEDBC...",
    "..CQOMGEEEDDBC..",
    "..CQpOOMGEEDBC..",
    ".MCQppOOMLGEDCM.",
    ".LCppOOMMLLIHCL.",
    ".ICOOMMLLIIHHCI.",
]
BARS = [
    "......CCCC......",
    ".....CJGBEC.....",
    "....CJGBBEDC....",
    "....CJBBEBDC....",
    "...CJBGEBBDBC...",
    "..CQOMGBBEDDBC..",
    "..CQpOOBGEEDBC..",
    ".MCQppOOMLGEDCM.",
    ".LCppOOMMLLIHCL.",
    ".ICOOMMLLIIHHCI.",
]
CANDIDATES = {
    "A": common.patched(["................", "................", "........CD......"] + BODY + POOL,
                        {(12, 5): "D", (12, 6): "C"}),
    "B": ["................", "..........C.C...", "...........D...."] + common.patched(BODY, {(10, 0): "D"}) + POOL,
    "C": ["................", "..........C.C...", "...........D...."] + common.patched(BARS, {(10, 0): "D"}) + POOL,
}
FIN = {"A": {(8, 2), (9, 2), (12, 5), (12, 6)}, "B": {(10, 1), (12, 1), (11, 2), (10, 3)}}
FIN["C"] = FIN["B"]
# A2: critic round 1's fixes for A (PASS, "but only just"): the top fin raked back off the cap instead of a level
# nub ("an acorn stem or onion tip"); the shoulder fin gone ("just makes the right shoulder look lumpy"); the right
# flap shaded; the shaded shoulder deepened with the model's dark back k and the lit cap lifted at (8,4)
CANDIDATES["A2"] = common.patched(CANDIDATES["A"], {
    (8, 2): ".", (9, 2): "C", (10, 3): "D", (12, 5): ".", (12, 6): ".",
    (14, 10): "I", (14, 11): "H", (14, 12): "H", (10, 6): "k", (10, 7): "k", (10, 8): "k", (8, 4): "J"})
FIN["A2"] = {(9, 2), (10, 3)}
DARK = "CBDk"
# A3: critic round 2's fix for A2 (PASS: "still a generic slate-and-silver fish egg, not a barracuda in
# particular"): one short slanted bar k ahead of the dark shoulder, so the two stagger like the barracuda's oblique
# bars on the upper flank (rows 5-7 and 6-8, never level, so no pair of eyes)
CANDIDATES["A3"] = common.patched(CANDIDATES["A2"], {(7, 5): "k", (7, 6): "k", (6, 7): "D"})
FIN["A3"] = FIN["A2"]
# A4: critic round 3's fixes for A3 (PASS, "only just"; "The rear bar merges into the outline ... The bars stand
# straight up, not slanted"): the rear bar lifted one column off the outline and slanted down and forward like the
# front bar (tops on rows 5 and 6, never level); the front bar's tip against a mid-tone G, not the brightest J, and
# no hard notch behind it
CANDIDATES["A4"] = common.patched(CANDIDATES["A3"], {
    (10, 6): "E", (10, 7): "D", (10, 8): "D", (9, 6): "k", (9, 7): "k", (8, 8): "D", (7, 4): "G", (6, 6): "G"})
FIN["A4"] = FIN["A3"]
PICK = "A4"

if __name__ == "__main__":
    common.run(FISH, TITLE, PAL, CANDIDATES, FIN, DARK, PICK, os.path.abspath(__file__))
