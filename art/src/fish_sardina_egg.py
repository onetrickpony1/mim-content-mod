"""Sardina spawn egg: the item icon (16 x 16), 2026-11-18.

The pool (owner 2026-11-18, "the pool under the egg should be the same as vanilla"; docs/Decisions/2026-11-18 Boll
egg B; egg pools match vanilla.md): the pool drawn in the grid below is our old one. vanilla_pool() swaps it for
vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only) before the egg
is written, keeping every body pixel; what is said below about our own pool is its history.

Built the way vanilla 26.3 builds its new per-mob spawn eggs (decision "2026-11-18 Spawn eggs show the animal"),
measured from the fish ones (cod, salmon, tropical_fish and pufferfish _spawn_egg in art/.vanilla/item, measured,
never copied): the egg is the animal itself, not an egg tinted in its colours. It stands in a small pool of water
(rows 13 to 15) and the fish's own parts (dorsal fin, tail, side fins) break the egg outline.
The pool is our own: its own ramp of blues, its own widths (narrow top, widest in the middle row, drawn in to
x 4 to 11 at the bottom), its own ripple highlights; not vanilla's shared water-mob pool, nor the lampuka's or tonn's.

How vanilla's fish eggs and our accepted lampuka and tonn eggs show their fish (studied before drawing this one):
the whole egg outline is kept (a narrow top on row 3, widening to its full width low down) and the fish is painted
onto it as a stylised token, not drawn as a whole fish: the back colour as a cap over the top, a pale belly patch on
the lower front, the side fins as small flaps sticking out on both sides low down, and a few signature parts (an eye
high on the left, a dorsal fin or tail breaking the top outline). The first sardina eggs drew the fish itself, snout
and all, squashed into the egg's space, which read as a fat sardine; this one follows the vanilla way.

The sardina (European sardine, Sardina pilchardus) is a small, slim fish, so its egg is a little smaller than the
tonn's: rows 4 to 12 (tonn 3 to 12) and x 3 to 12 at the widest (tonn 1 to 14), with the fins at x 2 and 13.
At 1x it reads by:
- a blue-green cap over the top of the egg, lit teal on its upper-left edge, with a small dorsal fin on top;
- one big black eye high on the left, in a ring of silver, with a muted gold hint of the gill cover behind it;
- a pale teal sheen band where the back meets the bright silver sides and white belly patch;
- two soft dark spots on and just under that band, offset in height (not a pair, so no face);
- the deeply forked tail in the dark back colour, flicking up behind the egg at the top right: the left lobe two
  pixels tall with a lit edge, joined solidly to the right lobe and the stalk so it reads as a tail, not a sprig;
- small grey fins sticking out on both sides low down, like vanilla's fish eggs.
Everything stays within x 1 to 14. Colours are the sardina item icon's (textures/item/sardina.png; the spots in a
darker tone of their own, #4b6170), plus the pool blues.
Photos (reference only): art/references/fish_sardina_refonly/ (list.tsv).

Run:    art/.venv/bin/python art/src/fish_sardina_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/sardina_spawn_egg.png (byte-identical on rerun) and
        art/candidates/fish_sardina_egg.png (compare sheet; the in-game hotbar crop comes from .art-runs/sardinaegg6/).
"""
import glob
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(ART, ".."))
sys.path.insert(0, os.path.join(ART, "tools"))
from font import label_font  # noqa: E402
from egg_pool import POOL_COLOURS, is_pool, pool_line, vanilla_pool  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "sardina_spawn_egg.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_sardina_egg.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_sardina_refonly")
SHOTS = os.path.join(ROOT, ".art-runs", "sardinaegg6", "build", "smoke-run", "screenshots")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # the sardina: the item icon's colours
    "h": hx("#8cc6be"),  # lit teal edge of the back, the sheen line, the lit tail tip
    "f": hx("#4a7076"),  # the back where the light falls on it, the dorsal fin
    "k": hx("#24525e"),  # dark blue-green back
    "w": hx("#eef3f2"),  # bright silver-white
    "s": hx("#b4c2c9"),  # silver
    "g": hx("#7e8e99"),  # grey silver, the shaded lower right, the snout tip
    "o": hx("#2f3a45"),  # shaded outline
    "d": hx("#4b6170"),  # the spots: dark enough to show at 1x, still clearly lighter than the eye
    "e": hx("#0a0a0a"),  # the eye
    "Y": hx("#a88a44"),  # the gill cover: a hint of gold, kept muted so it doesn't read as a beak
    "a": hx("#5f6d78"),  # pectoral and anal fins
    "T": hx("#587a80"),  # forked tail
    # the old pool (now swapped for vanilla's): our own ramp of water blues
    "1": hx("#1f3d6a"),
    "2": hx("#2b5a8e"),
    "3": hx("#3878ad"),
    "4": hx("#4f9bcd"),
    "5": hx("#94d8f4"),
}
# Our own old pool's colours: vanilla_pool() takes them out and puts vanilla's pool in (owner 2026-11-18,
# "the pool under the egg should be the same as vanilla"; art/src/egg_pool.py).
OLD_POOL = {PAL[k] for k in "12345"}

GRID = [
    "................",
    "................",
    "..........f..k..",
    ".......f..fkk...",
    "......hkkkk.....",
    ".....hfkkko.....",
    "....hfkkkkko....",
    "....wekkkkko....",
    "...hwwwYhdhgo...",
    "...swwwwsssdo...",
    "..aswwwwsssgoa..",
    "..aoswwssgggoa..",
    "...ogsssggggo...",
    "..24oooooooo32..",
    ".12345333454321.",
    "....12211121....",
]

# the previous version (v5, passed by the critic, before the darker tail and spots), kept only to show on the sheet
PREV_GRID = [
    "................",
    "................",
    "..........h..T..",
    ".......f...TT...",
    "......hkkkT.....",
    ".....hfkkko.....",
    "....hfkkkkko....",
    "....wekkkkko....",
    "...hwwwYhdhgo...",
    "...swwwwsssdo...",
    "..aswwwwsssgoa..",
    "..aoswwssgggoa..",
    "...ogsssggggo...",
    "..24oooooooo32..",
    ".12345333454321.",
    "....12211121....",
]


def render(rows, changes=None):
    pal = dict(PAL, **(changes or {}))
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), pal[ch] + (255,))
    return im


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<26} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def copy_check(icon):
    """Exact-pixel copy check against every vanilla spawn egg (as art/candidates/critic_lampuka_egg/check.py).
    Vanilla's own pool pixels are allowed (the owner's exception, art/src/egg_pool.py); any other copied pixel
    fails the run."""
    ours = {(x, y): icon.getpixel((x, y)) for x in range(16) for y in range(16) if icon.getpixel((x, y))[3] > 0}
    hits, shared = [], set()
    vcols = set()
    for f in sorted(glob.glob(os.path.join(VANILLA, "*spawn_egg*.png"))):
        v = Image.open(f).convert("RGBA")
        if v.size != (16, 16):
            continue
        same = [p for p, c in ours.items() if v.getpixel(p) == c and not is_pool(p, c)]
        if same:
            hits.append((len(same), os.path.basename(f)))
        vcols |= {v.getpixel((x, y))[:3] for x in range(16) for y in range(16) if v.getpixel((x, y))[3] > 0}
    shared = ({c[:3] for c in ours.values()} - POOL_COLOURS) & vcols
    assert not hits, f"copies vanilla pixels besides the pool: {hits}"
    hits.sort(reverse=True)
    most = f"most: {hits[0][0]} in {hits[0][1]}" if hits else "none"
    return [f"same pixel and colour as a vanilla spawn egg, besides its pool: {sum(n for n, _ in hits)} pixels over {len(hits)} eggs ({most})",
            f"our colours (besides the pool) also used by any vanilla spawn egg: {len(shared)}",
            pool_line(icon)]


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 1940
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    refs = []
    for name in ("side_1.jpg", "sardinia.jpg", "drawing_gervais.jpg", "sardina_galicia.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((310, round(310 * im.height / im.width)), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = max(im.height for _, im in refs) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im, (10 + i * 320, 22))
            d.text((10 + i * 320, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References (art/references/fish_sardina_refonly, list.tsv)", band))

    items = [("vanilla cod egg", os.path.join(VANILLA, "cod_spawn_egg.png")),
             ("vanilla salmon egg", os.path.join(VANILLA, "salmon_spawn_egg.png")),
             ("vanilla tropical fish egg", os.path.join(VANILLA, "tropical_fish_spawn_egg.png")),
             ("vanilla pufferfish egg", os.path.join(VANILLA, "pufferfish_spawn_egg.png")),
             ("our lampuka egg", os.path.join(TEXTURES, "item", "lampuka_spawn_egg.png")),
             ("our tonn egg", os.path.join(TEXTURES, "item", "tonn_spawn_egg.png")),
             ("previous sardina egg (v5)", "PREV"),
             ("NEW SARDINA EGG", None),
             ("sardina item icon", os.path.join(TEXTURES, "item", "sardina.png"))]
    band = Image.new("RGB", (W, 128 + 120), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = icon if p is None else render(PREV_GRID, {"d": hx("#5f7684")}) if p == "PREV" else Image.open(p).convert("RGBA")
        x0 = 10 + i * 214
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(tile.convert("RGB"), (x0, 22))
        d.text((x0, 2), name, fill=ink, font=small)
        for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
            t = Image.new("RGBA", (40, 40), col + (255,))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x0 + (j % 2) * 44 + (j // 2) * 88, 156))
    d.text((10, 202), "8x, then 1x and 2x on light grey, 1x and 2x on dark grey", fill=ink, font=small)
    parts.append(("The egg at 8x and 1x (and the previous version) beside vanilla's fish eggs, our lampuka and tonn eggs and the sardina item icon", band))

    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "salmon", "tropical_fish", "pufferfish")]
                    + [os.path.join(TEXTURES, "item", n + "_spawn_egg.png") for n in ("lampuka", "tonn")] + [OUT_ICON])
    lines += copy_check(icon)
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py and the copy check", band))

    shot = sorted(glob.glob(os.path.join(SHOTS, "*fish-09*.png")))
    if shot:
        im = Image.open(shot[0]).convert("RGB")
        w, h = im.size
        gui = max(1, min(4, w // 320, h // 240))
        crop = im.crop((w // 2 - 92 * gui, h - 23 * gui, w // 2 + 92 * gui, h))
        scale = max(1, (W - 20) // crop.width)
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.NEAREST)
        band = Image.new("RGB", (W, crop.height + 30), bg)
        band.paste(crop, (10, 4))
        ImageDraw.Draw(band).text((10, crop.height + 8), os.path.relpath(shot[0], ROOT) +
                                  "  (cod egg, lampuka, tonn, SARDINA, cerna, awrata, murina, ziemel, salmon egg)",
                                  fill=ink, font=small)
        parts.append(("In game: hotbar (fish-09), spawn eggs", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Sardina (European sardine) spawn egg, textures/item/sardina_spawn_egg.png", fill=ink,
           font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)
    print("wrote", OUT_SHEET)


if __name__ == "__main__":
    icon = vanilla_pool(render(GRID), OLD_POOL)
    icon.save(OUT_ICON, optimize=False)
    print("wrote", OUT_ICON)
    sheet(icon)
