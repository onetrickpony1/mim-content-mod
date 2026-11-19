"""Lionfish (Pterois miles) spawn egg: the item icon (16 x 16), 2026-11-19.

Started by the owner's rule (docs/Decisions/2026-11-18 Approving a step starts the next; skorfna bucket.md): the
owner passed its model (redone slimmer and shaded) (docs/Decisions/2026-11-19 Redos pass - lionfish, lizz bucket, petrica, gallinella icon; John Dory
bucket again.md), which starts its egg.

The owner's egg rules, all kept here (docs/Tools and Process/Art pipeline.md, "Fish art: lessons learnt"): vanilla's
fish-egg outline (art/src/fish_egg_common.py EGG) standing in vanilla's own pool (art/src/egg_pool.py, the owner's
exception to "never copy", for the pool only; P in the grids); a stylised egg in the fish's palette carrying only its
key features, never the whole fish squeezed in; no eye, no face, no pair of level dark dots, nothing phallic, no pale
point in front at eye height (a beak), no band across the middle (a Pokeball). The eye-pair check is the line-aware one
in art/src/fish_egg_lines.py (bars and stripes touch, so only lone dark dots count).

Key features: the bands, wide rust-maroon with thin broken cream lines wrapped round the egg and fading into a salmon
belly, and the long separate rust spines over the top; the side flaps are banded fan fins. It must not read as a
jellyfish egg or the skorfna egg (a crest of short spines on a brown egg).

Colours: only the accepted icon's (textures/item/lionfish.png), plus vanilla's pool. Nothing new.

Candidates: A diagonal 2 px rust / 2 px cream bands, B 2 px rust / 1 px cream, C B with fans breaking the outline;
A2, A3 and A4 (the PICK) are A with the fixes of critic rounds 1-3 (see the comments at their grids).

The critic rounds and blind reads, word for word: docs/Creatures and Plants/Night log/lionfish.md, "Egg".

Run:    art/.venv/bin/python art/src/fish_lionfish_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/lionfish_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_lionfish_egg.png (the compare sheet: the candidates at 8x, 1x and 2x beside
        vanilla's fish eggs, our accepted fish eggs and the fish's own icon) and the offline hotbar previews
        art/candidates/fish_lionfish_egg_hotbar.png and fish_lionfish_egg_hotbar_x4.png (art/tools/hotbar_preview.py,
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


FISH = "lionfish"
TITLE = "Lionfish spawn egg: textures/item/lionfish_spawn_egg.png"
PAL = {k: hx(v) for k, v in {
    "o": "#5b291a", "B": "#5b291a", "d": "#7a3a25", "D": "#954632", "e": "#a64630",
    "M": "#fff7ea", "J": "#ffedd4", "I": "#ffe7cb", "H": "#e6c5a6", "G": "#f0b69e", "F": "#d8866a",
}.items()}
POOL = common.pool_rows("o")
SPINES = [
    "........e.......",
    ".....e..J...J...",
    "......J.e..e....",
]
CANDIDATES = {
    "A": SPINES + [
        "......oooo.J....",
        ".....oMJDdo.....",
        "....oMJeDIHo....",
        "....oJeDIHdo....",
        "...oJeDJIddHo...",
        "..oMeDJIDdHGdo..",
        "..oeDJIDdHGddo..",
        ".FoDIIDdHHddGoF.",
        ".doIIDdHHddGGod.",
        ".FoIddHGddGGBoF.",
    ] + POOL,
    "B": SPINES + [
        "......oooo.J....",
        ".....oeJDDo.....",
        "....oeJDDIDo....",
        "....oJDDIDDo....",
        "...oJDDJDDHdo...",
        "..oJeDJDDIddGo..",
        "..oeDJDDIddGdo..",
        ".FoeJDDIddHddoF.",
        ".doJDDIDdHddGod.",
        ".FoDDIDdHddGdoF.",
    ] + POOL,
}
CANDIDATES["C"] = common.patched(CANDIDATES["B"], {(1, 9): "F", (0, 10): "F", (0, 11): "d", (0, 12): "F",
                                                   (14, 9): "F", (15, 10): "F", (15, 11): "d", (15, 12): "F"})
_sp = {(8, 0), (5, 1), (6, 2), (8, 1), (8, 2), (12, 1), (11, 2), (11, 3)}
_fans = {(0, 10), (0, 11), (0, 12), (15, 10), (15, 11), (15, 12)}
FIN = {"A": _sp, "B": _sp, "C": _sp | _fans | {(1, 9), (14, 9)}}
# A2: critic round 1's fixes for A (FAIL: "a red-and-white peppermint candy or circus tent with birthday candles on
# top"): the spines rust, not candles, the middle one leaning forward ((12,1) e, (11,3) d, (8,1) D, (8,0) gone, (7,0) e;
# one pale pixel left at (6,2)); less white (the brightest cream M only at (6,4)); a salmon belly, so the bands fade
# out low down; every second rust band darker (d), so the bands are uneven like the icon's
CANDIDATES["A2"] = common.patched(CANDIDATES["A"], {
    (12, 1): "e", (11, 3): "d", (8, 1): "D", (8, 0): ".", (7, 0): "e", (5, 5): "J", (3, 8): "J",
    (3, 10): "G", (4, 10): "G", (3, 11): "G", (4, 11): "H", (3, 12): "G", (8, 5): "d", (6, 7): "d"})
FIN["A2"] = (_sp - {(8, 0)}) | {(7, 0)}
DARK = "oBdDe"
# A3: critic round 2's fixes for A2 (FAIL: "Still candy ... even, parallel, high-contrast diagonal stripes"; the pale
# spine pixel "a candle flame or spark"): the spines all rust, joined to the outline, the tallest tipped with the
# pale peach H; the cream bands thinned to broken 1 px lines so the rust takes over; the lower bands bent toward
# upright so they wrap the curve; the fan flaps banded dark-pale-dark
CANDIDATES["A3"] = common.patched(CANDIDATES["A2"], {
    (6, 2): "e", (6, 3): "d", (7, 0): "H",
    (7, 4): "D", (6, 5): "e", (9, 6): "d", (8, 7): "D", (7, 8): "D", (6, 9): "D", (5, 10): "H",
    (8, 9): "D", (9, 10): "D", (10, 12): "d",
    (1, 10): "d", (1, 12): "d", (1, 11): "G", (14, 10): "d", (14, 12): "d", (14, 11): "G"})
FIN["A3"] = FIN["A2"]
# A4, the PICK: critic round 3 (PASS on A3) and its optional polish: the tallest spine's tip rust like the others
# (its pale tip was "the last thing that can still read as a candle flame or spark"), the spine beside it a lighter rust
CANDIDATES["A4"] = common.patched(CANDIDATES["A3"], {(7, 0): "D", (8, 1): "e"})
FIN["A4"] = FIN["A3"]
PICK = "A4"

if __name__ == "__main__":
    common.run(FISH, TITLE, PAL, CANDIDATES, FIN, DARK, PICK, os.path.abspath(__file__))
