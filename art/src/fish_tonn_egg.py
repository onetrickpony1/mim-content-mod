"""Tonn spawn egg: the item icon (16 x 16), 2026-11-18.

The pool (owner 2026-11-18, "the pool under the egg should be the same as vanilla"; docs/Decisions/2026-11-18 Boll
egg B; egg pools match vanilla.md): the pool drawn in the grid below is our old one. vanilla_pool() swaps it for
vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only) before the egg
is written, keeping every body pixel; what is said below about our own pool is its history.

Built the way vanilla 26.3 builds its new per-mob spawn eggs (decision "2026-11-18 Spawn eggs show the animal"),
measured from the fish ones (cod, salmon, tropical_fish and pufferfish _spawn_egg in art/.vanilla/item, measured,
never copied): the egg is the animal itself, not an egg tinted in its colours. It stands in a small pool of water
(rows 13 to 15), widens low down where the side fins stick out, and the mob's own parts break the egg outline.
The pool is our own: its own ramp of blues, its own widths (wider on top, the bottom row drawn in to the left),
its own ripple highlights; not vanilla's shared water-mob pool and not the lampuka egg's.

The tonn (Atlantic bluefin tuna, Thunnus thynnus) is turned a little to the left, so at 1x it reads by:
- a pointed, conical snout breaking the egg outline on the left, with a black eye just above and behind it;
- a deep blue-black back over the top of the egg with a cobalt sheen on its lit upper-left edge;
- a silver-white belly below a blue band that rises from the snout toward the tail (countershading);
- the stiff crescent tail, two thin blue-black lobes with one lit tip, flicking up behind the egg at the top right;
- a short greyish-yellow second dorsal fin sticking up from the top of the back;
- two small yellow finlets with dark edges on the tail stalk, just below the tail;
- a short dark pectoral fin on the side, and the dark anal fin sticking out low on the right.
No paired spots or marks (they read as a face). Everything stays within x 1 to 14. Colours are the tonn item
icon's (textures/item/tonn.png), plus the pool blues.
Photos (reference only): art/references/fish_tonn_refonly/ (list.tsv).

Run:    art/.venv/bin/python art/src/fish_tonn_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/tonn_spawn_egg.png (byte-identical on rerun) and
        art/candidates/fish_tonn_egg.png (compare sheet; the in-game hotbar crop comes from .art-runs/tonnegg2/).
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
OUT_ICON = os.path.join(TEXTURES, "item", "tonn_spawn_egg.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_tonn_egg.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_tonn_refonly")
SHOTS = os.path.join(ROOT, ".art-runs", "tonnegg2", "build", "smoke-run", "screenshots")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # the tonn: the item icon's colours
    "H": hx("#a0b8dc"),  # cobalt sheen on the lit back
    "h": hx("#6584b8"),  # lit edge of the back, the lit tip of the tail
    "k": hx("#1f2d52"),  # deep navy back
    "b": hx("#3a5e98"),  # the blue band where back meets silver
    "w": hx("#e8edf1"),  # silver-white belly in the light
    "s": hx("#b4bfcb"),  # silver
    "g": hx("#848fa0"),  # grey silver
    "G": hx("#5a6476"),  # dark grey, shaded lower right
    "o": hx("#181e2c"),  # shaded outline
    "e": hx("#0a0a0a"),  # the eye
    "p": hx("#1f2a44"),  # pectoral fin
    "f": hx("#7a7a6e"),  # second dorsal fin
    "F": hx("#a8a07a"),  # its lit tip
    "a": hx("#3e4252"),  # anal fin
    "y": hx("#f0c828"),  # finlets, lit
    "Y": hx("#a8801a"),  # finlets, shaded
    "t": hx("#1b2746"),  # tail, shaded lobe
    # the old pool (now swapped for vanilla's): our own ramp of water blues
    "1": hx("#233a6c"),
    "2": hx("#2c5590"),
    "3": hx("#376fa8"),
    "4": hx("#4b8fc4"),
    "5": hx("#7fc8ee"),
}
# Our own old pool's colours: vanilla_pool() takes them out and puts vanilla's pool in (owner 2026-11-18,
# "the pool under the egg should be the same as vanilla"; art/src/egg_pool.py).
OLD_POOL = {PAL[k] for k in "12345"}

GRID = [
    "................",
    "........F.hk.tt.",
    "........Ff.kkt..",
    "......hHkf..t...",
    ".....hHkkkkt....",
    "....hHkkkkkoy...",
    "....hkkkkkkkoy..",
    "...Hehkkkkbbo...",
    "..hkkkkbbbwwgo..",
    ".HkbbbwpwwssgGo.",
    "..owwwwwpwssgGo.",
    "..swwwwwwssggGa.",
    "..oswwwssgggGoa.",
    ".24ooooooooo542.",
    ".23454334543432.",
    "..1221112221....",
]


def render(rows):
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
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
    W = 1300
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    refs = []
    for name in ("tonn_06.jpg", "tonn_03.jpg", "tonn_13.jpg", "tonn_02.jpg"):
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
        parts.append(("References (art/references/fish_tonn_refonly, list.tsv)", band))

    items = [("vanilla cod egg", os.path.join(VANILLA, "cod_spawn_egg.png")),
             ("vanilla salmon egg", os.path.join(VANILLA, "salmon_spawn_egg.png")),
             ("vanilla tropical fish egg", os.path.join(VANILLA, "tropical_fish_spawn_egg.png")),
             ("vanilla pufferfish egg", os.path.join(VANILLA, "pufferfish_spawn_egg.png")),
             ("TONN EGG", None),
             ("tonn item icon", os.path.join(TEXTURES, "item", "tonn.png"))]
    band = Image.new("RGB", (W, 128 + 120), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = icon if p is None else Image.open(p).convert("RGBA")
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
    parts.append(("The egg at 8x and 1x beside vanilla's fish eggs and our tonn item", band))

    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "salmon", "tropical_fish", "pufferfish")]
                    + [os.path.join(TEXTURES, "item", "lampuka_spawn_egg.png"), OUT_ICON])
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
                                  "  (cod egg, lampuka, TONN, sardina, cerna, awrata, murina, ziemel, salmon egg)",
                                  fill=ink, font=small)
        parts.append(("In game: hotbar (fish-09), spawn eggs", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Tonn (Atlantic bluefin tuna) spawn egg, textures/item/tonn_spawn_egg.png", fill=ink,
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
