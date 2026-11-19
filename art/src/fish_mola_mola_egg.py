"""Mola mola (ocean sunfish, shown as Pixxiluna) spawn egg: the item icon (16 x 16), 2026-11-19.

Started by the owner's rule (docs/Decisions/2026-11-18 Approving a step starts the next; skorfna bucket.md): the mola
mola has no bucket (docs/Decisions/2026-11-19 Mola mola - can be found, not captured; escapes when hurt; basks in the
sun.md); its model and icon A are accepted, which starts its egg.

The owner's egg rules, all kept here (docs/Tools and Process/Art pipeline.md, "Fish art: lessons learnt"):
- vanilla's egg outline, measured from vanilla 26.x's fish eggs (art/src/fish_egg_common.py EGG): nothing breaks
  it but the sunfish's tall fins;
- a stylised egg in the animal's palette with only its key features (the owner's favourite, the boll egg B):
  - the tall dorsal fin, swept back, rising from the egg's back shoulder in the icon's fin greys (f lit leading
    edge, F G, the dark tip H), a triangle broad at its base, never a post, so the egg's own top stays round;
  - the clavus, the scalloped pale rim where a tail should be: a band of pale c down the egg's back (right) edge
    behind the fold k;
  - the egg lit from the top left (h), the grey-brown back B over the silver side S to the pale belly W, with one
    soft blotch n;
  - the side flaps as the pectoral fins P p on the front and the clavus' own pale c on the back.
- no eye, no face, no pair of level dark dots, no mouth.
- vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only): P in the grids;
  the icon's pectoral fin P is written Q here.

Colours: only the accepted icon A's (art/src/fish_mola_icon.py PAL), plus vanilla's pool. Nothing new.

Candidates (the sheet shows all of them; PICK is written to the mod):
- A, dorsal fin and clavus.
- B, both fins: A with the anal fin as well, a short swept blade out of the lower back, mirroring the dorsal, so the
  egg carries the sunfish's whole outline: fin up, fin down, the clavus between.
- C, short fins: B with both fins a pixel shorter.
- B2: B with critic round 1's fixes (see its comment).
- B3: B2 with critic round 2's fixes (see its comment).
- B4, the PICK: B3 with critic round 3's two fixes (see its comment).

The critic rounds and blind reads, word for word: docs/Creatures and Plants/Night log/mola_mola.md, "Egg".

Run:    art/.venv/bin/python art/src/fish_mola_mola_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/mola_mola_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_mola_mola_egg.png (the compare sheet) and the offline hotbar previews
        art/candidates/fish_mola_mola_egg_hotbar.png and fish_mola_mola_egg_hotbar_x4.png
        (art/tools/hotbar_preview.py, GUI scale 2 and 4, nothing selected).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_mola_icon import PAL as ICON  # noqa: E402  (accepted icon A)
import fish_egg_common as common  # noqa: E402

FISH = "mola_mola"
TITLE = "Mola mola (ocean sunfish, Pixxiluna) spawn egg: textures/item/mola_mola_spawn_egg.png"

PAL = {k: ICON[k] for k in "oOHGFfBhUnSLWckp"}
PAL["Q"] = ICON["P"]  # the pectoral fin (P is the pool in these grids)

POOL = common.pool_rows("o")

CANDIDATES = {
    # round 0 (the maker's own look at 1x): with the dorsal on the egg's top the egg came to a point (a garlic bulb);
    # it now rises from the back shoulder, so the top stays round
    "A": [
        "................",
        "............H...",
        "...........fG...",
        "......OOOofFG...",
        ".....OhBBkoF....",
        "....OhBBBkco....",
        "....OhUUUkco....",
        "...OhUUnUUkco...",
        "..OhUSSSSSkcco..",
        "..OUSSLSSSSkco..",
        ".QOSLLLSSSSkcoc.",
        ".pOLWWWLLSSkkoc.",
        ".pOLWWWWLLSSkoo.",
    ] + POOL,
    "B": [
        "................",
        "............H...",
        "...........fG...",
        "......OOOofFG...",
        ".....OhBBkoF....",
        "....OhBBBkco....",
        "....OhUUUkco....",
        "...OhUUnUUkco...",
        "..OhUSSSSSkcco..",
        "..OUSSLSSSSkco..",
        ".QOSLLLSSSSkcoc.",
        ".pOLWWWLLSSkkoF.",
        ".pOLWWWWLLSSkoGG",
        "..PPPooooooPooGH",
        "..PPPPPPPPPPPP..",
        "...PPPPPPPPPP...",
    ],
    "C": [
        "................",
        "................",
        "...........fG...",
        "......OOOofFG...",
        ".....OhBBkoF....",
        "....OhBBBkco....",
        "....OhUUUkco....",
        "...OhUUnUUkco...",
        "..OhUSSSSSkcco..",
        "..OUSSLSSSSkco..",
        ".QOSLLLSSSSkcoc.",
        ".pOLWWWLLSSkkoF.",
        ".pOLWWWWLLSSkoGG",
        "..PPPooooooPooG.",
        "..PPPPPPPPPPPP..",
        "...PPPPPPPPPP...",
    ],
}
# the only pixels allowed outside the egg: the dorsal fin on the back shoulder, and in B and C the anal fin at the
# lower back
DORSAL = {(12, 1), (11, 2), (12, 2), (10, 3), (11, 3), (12, 3), (11, 4)}
ANAL = {(15, 12), (14, 13), (15, 13)}
FIN = {"A": DORSAL, "B": DORSAL | ANAL, "C": (DORSAL - {(12, 1)}) | (ANAL - {(15, 13)})}
# B2: critic round 1 (FAIL, close; pick B) and its fixes: the fold darker U (11,9) (11,10) and the clavus brighter W
# (12,9) (12,10) (11,7), so the pale rim stands apart from the body at 1x and scallops against the c at (12,8); the
# anal fin lifted above the waterline (15,11) G with a lit leading edge (14,11) f, its tip in the pool softened to o
# (15,13), so "fin up, fin down" shows at 1x.
CANDIDATES["B2"] = common.patched(CANDIDATES["B"], {(11, 9): "U", (11, 10): "U", (12, 9): "W", (12, 10): "W",
                                                    (11, 7): "W", (15, 11): "G", (14, 11): "f", (15, 13): "o"})
FIN["B2"] = FIN["B"] | {(15, 11)}
# B3: critic round 2 (FAIL, close) and its fixes: the anal fin a diagonal blade leaning down and back, the dorsal's
# mirror, not a 2 x 3 stub: its top tapered (15,11) gone, a lighter base F (14,12), a dark tip H (15,13); the pale
# speck on the back flap dimmed to the fold's k (14,10), so no lone bright pixel stands outside the rim.
CANDIDATES["B3"] = common.patched(CANDIDATES["B2"], {(15, 11): ".", (14, 12): "F", (15, 13): "H", (14, 10): "k"})
FIN["B3"] = FIN["B"]
# B4, the pick: critic round 3 (PASS) and its two fixes: the pale speck on the back flap (14,10) becomes the top of
# the anal fin's lit leading edge f, so no pale bump stands level with the pectoral Q; the dorsal's back base filled
# (12,4) G, so the fin is a broad triangle and not a stem (the round 3 readers called it a spike).
CANDIDATES["B4"] = common.patched(CANDIDATES["B3"], {(14, 10): "f", (12, 4): "G"})
FIN["B4"] = FIN["B"] | {(12, 4)}
DARK = "oOH"  # the marks that must never pair up level, like eyes
PICK = "B4"

if __name__ == "__main__":
    common.run(FISH, TITLE, PAL, CANDIDATES, FIN, DARK, PICK, os.path.abspath(__file__))
