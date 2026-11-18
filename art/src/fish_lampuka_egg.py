"""Lampuka spawn egg: the item icon (16 x 16), 2026-11-18.

The pool (owner 2026-11-18, "the pool under the egg should be the same as vanilla"; docs/Decisions/2026-11-18 Boll
egg B; egg pools match vanilla.md): the pool drawn in the grid below is our old one. vanilla_pool() swaps it for
vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only) before the egg
is written, keeping every body pixel; what is said below about our own pool is its history.

Built the way vanilla 26.3 builds its new per-mob spawn eggs, measured from the fish ones (cod, salmon,
tropical_fish and pufferfish _spawn_egg in art/.vanilla/item, measured, not loaded): the egg is the animal
itself, not an egg tinted in its colours. The egg stands in a small pool of water (rows 13 to 15; vanilla's
water-mob eggs share one pool, ours is drawn fresh with its own blues, lop-sided under the tail), widens low down where the side fins stick out (rows 9 to 12), and the
mob's own parts break the egg outline where it has them (the pufferfish's spines).

The lampuka (dolphinfish, Coryphaena hippurus) is turned a little to the left, so at 1x it reads by:
- the blunt, steep blue-green head on the left (a near-upright forehead), with a black eye high on it;
- the long dark dorsal fin, a crest from the forehead over the whole top of the egg, its rays poking up;
- the forked yellow tail flicking up behind it at the top right;
- blue-green back going to gold sides with one small blue spot toward the tail, and a cream belly that is a
  wedge low on the left, rising toward the head and thinning toward the tail (a level belly with spots read as a
  face);
- small yellow pectoral fins sticking out low on each side, as vanilla's fish eggs do.
Everything stays within x 1 to 14. Colours are the accepted lampuka item icon's (textures/item/lampuka.png),
plus one blue for the spot.
Photos (reference only): art/references/fish_lampuka_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/lampuka_spawn_egg.png
Run:    art/.venv/bin/python art/src/fish_lampuka_egg.py
"""
import glob
import os

from PIL import Image

from egg_pool import is_pool, pool_line, vanilla_pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item",
                   "lampuka_spawn_egg.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ROOT, "art", ".vanilla")), "item")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # the lampuka: the accepted item icon's colours
    "C": hx("#1c5158"),  # dark teal: outline of the back and head
    "J": hx("#2c4a48"),  # dark slate: the dorsal fin
    "N": hx("#2f7a68"),  # mid green: the steep forehead, shaded back
    "E": hx("#5cbc9e"),  # blue-green: the back
    "D": hx("#9ae2bc"),  # pale mint: light on the head
    "H": hx("#a8c03c"),  # yellow-green: where green turns to gold
    "K": hx("#e6c12c"),  # gold: the flank
    "I": hx("#a67c18"),  # dark gold: lower flank, shaded side
    "L": hx("#786024"),  # gold shadow: outline low on the egg
    "O": hx("#f6eecb"),  # cream: the belly
    "M": hx("#101010"),  # the eye
    "B": hx("#c4b43a"),  # yellow: tail and fins
    "A": hx("#5e5a1c"),  # olive: fin edges
    "S": hx("#2f6f9a"),  # blue: the small spots on the flank
    # the old pool (now swapped for vanilla's): our own ramp of water blues (in the range vanilla's water-mob eggs use, not their values),
    # lop-sided: it spreads out under the tail and its lower edge sits to the right
    "1": hx("#283f72"),
    "2": hx("#345887"),
    "3": hx("#3d72a6"),
    "4": hx("#4a95c6"),
    "5": hx("#6ccbfa"),
}
# Our own old pool's colours: vanilla_pool() takes them out and puts vanilla's pool in (owner 2026-11-18,
# "the pool under the egg should be the same as vanilla"; art/src/egg_pool.py).
OLD_POOL = {PAL[k] for k in "12345"}

GRID = [
    "................",
    "................",
    "......J.J.J...A.",
    "......JJJJ...BA.",
    ".....CDJJJN.KB..",
    "....CNDEEJNCK...",
    "....NMEEEENCKB..",
    "....NEEHEEENCBA.",
    "...CHKHKKHHENCB.",
    "..COKKHKKKKKIC..",
    ".BAOOKKKKKKSIAB.",
    ".BAOOOOKKKKIIAB.",
    ".AAOOOOOOKIIILA.",
    "..2LLLLLLLLL431.",
    ".12435454344321.",
    "...211111111222.",
]


def build():
    assert len(GRID) == 16 and all(len(r) == 16 for r in GRID)
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(GRID):
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return vanilla_pool(im, OLD_POOL)


def copy_check(icon):
    """Exact-pixel copy check against every vanilla spawn egg. Vanilla's own pool pixels are allowed (the owner's
    exception, art/src/egg_pool.py); any other copied pixel fails the run."""
    ours = {(x, y): icon.getpixel((x, y)) for x in range(16) for y in range(16) if icon.getpixel((x, y))[3] > 0}
    hits = []
    for f in sorted(glob.glob(os.path.join(VANILLA, "*spawn_egg*.png"))):
        v = Image.open(f).convert("RGBA")
        if v.size == (16, 16):
            same = [p for p, c in ours.items() if v.getpixel(p) == c and not is_pool(p, c)]
            if same:
                hits.append((len(same), os.path.basename(f)))
    assert not hits, f"copies vanilla pixels besides the pool: {hits}"
    return ["same pixel and colour as a vanilla spawn egg, besides its pool: 0 pixels", pool_line(icon)]


if __name__ == "__main__":
    icon = build()
    for line in copy_check(icon):
        print(line)
    icon.save(OUT, optimize=False)
    print("wrote", OUT)
