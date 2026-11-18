"""Ċerna spawn egg: the item icon (16 x 16), 2026-11-18.

The pool (owner 2026-11-18, "the pool under the egg should be the same as vanilla"; docs/Decisions/2026-11-18 Boll
egg B; egg pools match vanilla.md): the pool drawn in the grid below is our old one. vanilla_pool() swaps it for
vanilla's own pool (art/src/egg_pool.py, the owner's exception to "never copy", for the pool only) before the egg
is written, keeping every body pixel; what is said below about our own pool is its history.

Built the way vanilla 26.3 builds its new per-mob spawn eggs (decisions "2026-11-18 Spawn eggs show the animal" and
"2026-11-18 Sardina egg - a representation, not a fat fish"), measured from the fish ones (cod, salmon, tropical_fish
and pufferfish _spawn_egg in art/.vanilla/item, measured, never copied) and following our accepted lampuka, tonn and
sardina eggs: the whole egg outline is kept (narrow top on row 3, widening to its full width low down, standing in a
pool) and the fish is painted onto it as a stylised token, not drawn as a whole fish.

The ċerna (dusky grouper, Epinephelus marginatus) is a big, heavy fish, so its egg is full vanilla size, like the
tonn's: rows 3 to 12, x 1 to 14 with the side fins.
At 1x it reads by:
- a darker reddish-brown cap over the top (mid to deep shade), lit on its upper-left edge, so it stands apart from
  both the lighter sides and the outline;
- a spiny dorsal fin: three dark spines joined by lit membrane, one continuous ridge along the top of the cap;
- one small black eye high on the left, in a lighter patch of the head;
- the big jutting lower jaw as a soft rounded chin: lit lip pixels with shaded ones above and below, no mouth line;
- the sides shaded with a real light ramp (lit at the front and top left, deep shade at the lower right, softened
  rims rather than a straight dark column) and mottled with irregular pale blotches, kept away from the eye;
- a pale belly patch on the lower front;
- the ROUNDED tail (not forked): a fan lit on its upper left, shaded rim round the right, at the upper right;
- small brown fins with lit tips sticking out on both sides low down, like vanilla's fish eggs.
The pool is our own: its own ramp of deep blues, its own widths and ripples; not vanilla's shared water-mob pool,
nor the lampuka's, tonn's or sardina's.
Colours are all the accepted ċerna item icon's (art/src/fish_cerna_icon.py PAL), plus the pool blues.
Photos (reference only): art/references/fish_cerna_refonly/ (list.tsv).

Run:    art/.venv/bin/python art/src/fish_cerna_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/cerna_spawn_egg.png (byte-identical on rerun) and
        art/candidates/fish_cerna_egg.png (compare sheet), with the offline hotbar previews
        art/candidates/fish_cerna_egg_hotbar.png and fish_cerna_egg_hotbar_x4.png (art/tools/hotbar_preview.py).
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
OUT_ICON = os.path.join(TEXTURES, "item", "cerna_spawn_egg.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_cerna_egg.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_cerna_refonly")
OUT_HOTBAR = os.path.join(ART, "candidates", "fish_cerna_egg_hotbar.png")
OUT_HOTBAR4 = os.path.join(ART, "candidates", "fish_cerna_egg_hotbar_x4.png")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # the ċerna: the accepted item icon's colours (art/src/fish_cerna_icon.py PAL)
    "h": hx("#c8956a"),  # brightest light: the lit edge of the cap, the belly patch
    "1": hx("#b27a55"), "2": hx("#a66c4a"), "3": hx("#93593f"), "4": hx("#7a4434"), "5": hx("#5e3228"),  # lit to shade
    "k": hx("#7a4632"),  # rim on the lit top and left
    "o": hx("#2e1a14"),  # rim on the shaded lower right
    "C": hx("#ccac88"), "c": hx("#a8866a"),  # pale blotches: in the light, partly shaded
    "e": hx("#0a0a0a"),  # the eye
    "L": hx("#b07a5e"), "l": hx("#8a5844"),  # the jutting lower jaw: lit, shaded
    "D": hx("#5a3224"), "f": hx("#8a5440"),  # dorsal: dark spines, lit membrane (also the lit tips of the side fins)
    "A": hx("#5a3426"),  # side fins
    "T": hx("#9a5e48"), "t": hx("#7a4838"), "u": hx("#4a2a20"),  # rounded tail: lit, mid, shaded rim
    # the old pool (now swapped for vanilla's): our own ramp of deep water blues
    "p": hx("#1a3553"),
    "q": hx("#23587d"),
    "r": hx("#327fa6"),
    "s": hx("#4ea4cb"),
    "w": hx("#a0dbea"),
}
# Our own old pool's colours: vanilla_pool() takes them out and puts vanilla's pool in (owner 2026-11-18,
# "the pool under the egg should be the same as vanilla"; art/src/egg_pool.py).
OLD_POOL = {PAL[k] for k in "pqrsw"}

GRID = [
    "................",
    "................",
    "......DfDfD.....",
    "......kh34f.tu..",
    ".....kh3445.TTu.",
    "....kh344c45tTu.",
    "....2e2344c5ttu.",
    "..lk1222C3345u..",
    ".LL1122c23C34o..",
    "..lhh1223c344o..",
    ".f1hCh1233c45of.",
    ".A2hh12c33445oA.",
    "..k2122334455o..",
    ".pqooooooooooqp.",
    ".qrswwsrrswwsrq.",
    "..pq.qppppq.qp..",
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
    W = 2160
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    refs = []
    for name in ("side_4.jpg", "side_1.jpg", "head_1.jpg", "caught_1.jpg", "drawing_1.jpg"):
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
        parts.append(("References (art/references/fish_cerna_refonly, list.tsv)", band))

    items = [("vanilla cod egg", os.path.join(VANILLA, "cod_spawn_egg.png")),
             ("vanilla salmon egg", os.path.join(VANILLA, "salmon_spawn_egg.png")),
             ("vanilla tropical fish egg", os.path.join(VANILLA, "tropical_fish_spawn_egg.png")),
             ("vanilla pufferfish egg", os.path.join(VANILLA, "pufferfish_spawn_egg.png")),
             ("our lampuka egg", os.path.join(TEXTURES, "item", "lampuka_spawn_egg.png")),
             ("our tonn egg", os.path.join(TEXTURES, "item", "tonn_spawn_egg.png")),
             ("our sardina egg", os.path.join(TEXTURES, "item", "sardina_spawn_egg.png")),
             ("NEW CERNA EGG", None),
             ("cerna item icon", os.path.join(TEXTURES, "item", "cerna.png")),
             ("cerna bucket", os.path.join(TEXTURES, "item", "cerna_bucket.png"))]
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
    parts.append(("The egg at 8x and 1x beside vanilla's fish eggs, our lampuka, tonn and sardina eggs and the accepted cerna item icon and bucket", band))

    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "salmon", "tropical_fish", "pufferfish")]
                    + [os.path.join(TEXTURES, "item", n + "_spawn_egg.png") for n in ("lampuka", "tonn", "sardina")] + [OUT_ICON])
    lines += copy_check(icon)
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py and the copy check", band))

    py = os.path.join(ART, ".venv", "bin", "python")
    items = ["mc:cod_spawn_egg", "mc:salmon_spawn_egg", "mc:tropical_fish_spawn_egg", "mc:pufferfish_spawn_egg",
             "mod:lampuka_spawn_egg", "mod:tonn_spawn_egg", "mod:sardina_spawn_egg", "mod:cerna_spawn_egg", "mod:cerna"]
    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items +
                       ["--select", "7", "--scale", str(scale)], check=True, capture_output=True)
    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        im = Image.open(out).convert("RGB")
        band = Image.new("RGB", (W, im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(out, ROOT) + f"  (GUI scale {scale}: vanilla cod, "
                                  "salmon, tropical fish, pufferfish eggs; our lampuka, tonn, sardina eggs; CERNA EGG "
                                  "(selected); cerna item icon)", fill=ink, font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py, GUI scale {scale})", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "\u010cerna (dusky grouper) spawn egg, textures/item/cerna_spawn_egg.png", fill=ink,
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
