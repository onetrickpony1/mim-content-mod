"""Trilja (striped red mullet, Mullus surmuletus) spawn egg: the item icon (16 x 16), 2026-11-19.

Started by the owner's rule (docs/Decisions/2026-11-18 Approving a step starts the next; skorfna bucket.md): the
trilja's bucket was accepted (docs/Decisions/2026-11-19 Night fish icons and buckets - most pass; John Dory,
gallinella, lingwata bucket redo.md), which starts its egg.

The owner's egg rules, all kept here (docs/Tools and Process/Art pipeline.md, "Fish art: lessons learnt"):
- vanilla's egg outline, measured from vanilla 26.x's fish eggs (cod, salmon in art/.vanilla/item, never copied):
  a 4 px top on row 3 widening to 12 px on rows 8-9, the one-pixel side flaps at x 1 and 14 on rows 10-12, the
  bottom edge on row 13 (x 5-10); nothing breaks the outline but the small first dorsal fin on top;
- a stylised egg in the animal's palette with only its key features (the owner's favourite, the boll egg B):
  - the striped first dorsal fin: a pale stripe F over a dark rose band K, sitting on the egg's top;
  - the gold line along the flank (y), wrapped round the egg's curve;
  - the rosy colouring: a red back m lit at the upper left (h c), the rose flank o, a pale pink belly p q, the dark
    rose rim r in the shade at the lower right;
  - the side flaps as the pale pink pelvic fins T C.
- no eye, no face, no pair of level dark dots; nothing pale points forward at eye height (no beak), the barbels
  are left out (on every model and icon try they read as a beard, tusks or legs).
- vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only): P in the grids.

Colours: only the accepted icon A's (art/src/fish_trilja_icon.py PAL), plus vanilla's pool. Nothing new.

Candidates (the sheet shows all of them; PICK is written to the mod):
- A, diagonal line: the gold line runs from the lower front up to the back, as on the icon (head low left, tail up
  right), the red back above it, the pale belly below.
- B, wrapped line: the gold line is a ring round the egg seen from a little above, so it dips in the middle (U), the
  red back above it and the pale belly below, a second faint gold line (Y) under it.
- C, two diagonal lines: A with a second, paler line (Y) a row under the gold one, the striped look of surmuletus.
- A2, the PICK: A with critic round 1's fixes (see its comment).

The critic rounds and blind reads, word for word: docs/Creatures and Plants/Night log/trilja.md, "Egg".

Run:    art/.venv/bin/python art/src/fish_trilja_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/trilja_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_trilja_egg.png (the compare sheet: the candidates at 8x, 1x and 2x beside
        vanilla's fish eggs, our accepted fish eggs and the trilja's own icon) and the offline hotbar previews
        art/candidates/fish_trilja_egg_hotbar.png and fish_trilja_egg_hotbar_x4.png (art/tools/hotbar_preview.py,
        GUI scale 2 and 4, nothing selected).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_trilja_icon import PAL as ICON  # noqa: E402  (accepted icon A)
import fish_egg_common as common  # noqa: E402

FISH = "trilja"
TITLE = "Trilja (striped red mullet) spawn egg: textures/item/trilja_spawn_egg.png"

PAL = {k: ICON[k] for k in "rmMhcoypqTCFKY"}
PAL["D"] = (0xa8, 0x42, 0x4a)  # the accepted model's M (art/src/fish_trilja_model.py PALETTES A), the deepest red

POOL = common.POOL_ROWS

CANDIDATES = {
    "A": [
        "................",
        "................",
        ".......FFF......",
        "......rKKKF.....",
        ".....rhhmmr.....",
        "....rhcmmmmr....",
        "....rhmmmmor....",
        "...rhmmmooyyr...",
        "..rhmmooyyppor..",
        "..rmooyyqqppor..",
        ".Troyyqqqppoor..",
        ".Tryqqqqpppoor..",
        ".Crppqqppooomr..",
    ] + POOL,
    "B": [
        "................",
        "................",
        ".......FFF......",
        "......rKKKF.....",
        ".....rhhmmr.....",
        "....rhcmmmmr....",
        "....rhmmmmmr....",
        "...rhmmmmmmmr...",
        "..rhooommmoomr..",
        "..ryooooooooyr..",
        ".Trpyyoooyyppr..",
        ".TrqqqyyyqqpprT.",
        ".CrpqYYYYqppor..",
    ] + POOL,
    "C": [
        "................",
        "................",
        ".......FFF......",
        "......rKKKF.....",
        ".....rhhmmr.....",
        "....rhcmmmmr....",
        "....rhmmmmor....",
        "...rhmmmooyyr...",
        "..rhmmooyyYYor..",
        "..rmooyyYYppor..",
        ".TroyyYYqppoor..",
        ".TryYYqqpppoor..",
        ".CrYqqqppooomr..",
    ] + POOL,
}
# A2, the pick: critic round 1 (PASS, pick A) and its fixes: the lower right flank steps down to the back red m
# (12,10) (12,11) (11,12), so the light falls off from the top left (TL-BR was -0.02); the fin's front pixel (7,2) is
# the dark band K, so the pale stripe slopes back from (8,2) and no pale nub sits on the egg's tip; the lit shoulder
# a pixel wider (4,8) h, breaking up the flat red back.
CANDIDATES["A2"] = list(CANDIDATES["A"])
for (_x, _y), _ch in {(12, 10): "m", (12, 11): "m", (11, 12): "m", (7, 2): "K", (4, 8): "h"}.items():
    CANDIDATES["A2"][_y] = CANDIDATES["A2"][_y][:_x] + _ch + CANDIDATES["A2"][_y][_x + 1:]
# added below so the grids above stay readable: the right flaps (x 14, rows 10-12), and the outline on the shaded
# right side (rows 5-12) and the right half of the bottom edge in the model's deeper red D, a step under r
for _n, _g in CANDIDATES.items():
    for _y, _ch in ((10, "T"), (11, "T"), (12, "C")):
        _g[_y] = _g[_y][:14] + _ch + _g[_y][15:]
    for _y in range(5, 13):
        _x = common.EGG[_y][1] - (1 if _y >= 10 else 0)
        _g[_y] = _g[_y][:_x] + "D" + _g[_y][_x + 1:]
    _g[13] = _g[13][:8] + "DDD" + _g[13][11:]
# the only pixels allowed outside the egg: the dorsal fin, lying low over the egg's top and sloping back onto the
# shoulder; its dark band K is the egg's own top edge
FIN = {n: {(7, 2), (8, 2), (9, 2), (10, 3)} for n in CANDIDATES}
DARK = "rKD"  # the marks that must never pair up level, like eyes
PICK = "A2"

if __name__ == "__main__":
    common.run(FISH, TITLE, PAL, CANDIDATES, FIN, DARK, PICK, os.path.abspath(__file__))
