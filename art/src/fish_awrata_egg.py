"""Awrata spawn egg: the item icon (16 x 16), 2026-11-18.

Built the way vanilla 26.3 builds its new per-mob spawn eggs (decisions "2026-11-18 Spawn eggs show the animal" and
"2026-11-18 Sardina egg - a representation, not a fat fish"), measured from the fish ones (cod, salmon, tropical_fish
and pufferfish _spawn_egg in art/.vanilla/item, measured, never copied) and following our accepted lampuka, tonn,
sardina and ċerna eggs: the whole egg outline is kept (narrow top on row 3, widening low down, standing in its own
pool) and the bream's features are painted onto it as a stylised token, not drawn as a whole fish.

The awrata (gilthead sea bream, Sparus aurata) is a medium fish, so its egg is about the lampuka's size: rows 3 to 12,
x 2 to 13, with small side fins at x 1 and 14 and the tail breaking the top outline.
At 1x it reads by:
- a blue-grey back cap over the top, lit on its upper left, with a silver sheen just under it at the front;
- a steep rounded forehead on the left (the outline drops almost straight from row 5 to row 9, rounding at both ends);
- the GOLD band across the forehead, just above the eye, running in from the lit rim: a mark across the head, not
  sticking out (so no beak) and well below the top (so no crown);
- one small black eye in light silver, nothing dark around it;
- the dark gill mark with its red-orange foot behind the eye and lower than it (core one row below the eye's row,
  two pixels behind it, the foot under that), so it never sits level with the eye;
- silver sides on a real light ramp, lit top left to shaded lower right, crossed by thin darker lengthwise lines
  (one tone darker than the silver around them, kept away from the eye);
- the forked tail at the upper right, two lobes with dark tips and a notch between, breaking the top outline;
- small grey fins sticking out low on both sides, like vanilla's fish eggs.
The pool is our own: a greener sea-blue ramp with its own widths and ripples; not vanilla's shared water-mob pool,
nor the lampuka's, tonn's, sardina's or ċerna's.
Colours are all the accepted awrata item icon's (art/src/fish_awrata_icon.py PAL), plus the pool colours.
Photos (reference only): art/references/fish_awrata_refonly/ (list.tsv).

Run:    art/.venv/bin/python art/src/fish_awrata_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/awrata_spawn_egg.png (byte-identical on rerun) and
        art/candidates/fish_awrata_egg.png (compare sheet), with the offline hotbar previews
        art/candidates/fish_awrata_egg_hotbar.png and fish_awrata_egg_hotbar_x4.png (art/tools/hotbar_preview.py).
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

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "awrata_spawn_egg.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_awrata_egg.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_awrata_refonly")
OUT_HOTBAR = os.path.join(ART, "candidates", "fish_awrata_egg_hotbar.png")
OUT_HOTBAR4 = os.path.join(ART, "candidates", "fish_awrata_egg_hotbar_x4.png")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # the awrata: the accepted item icon's colours (art/src/fish_awrata_icon.py PAL)
    "K": hx("#4f6477"), "b": hx("#7d91a3"),  # blue-grey back: rim, lit band
    "W": hx("#e6ecee"), "1": hx("#cdd6db"), "2": hx("#b4bec6"), "3": hx("#9ba7b1"), "4": hx("#83909b"),
    "5": hx("#6b7783"),  # silver light ramp, sheen to shade; 3 to 5 also draw the thin lines
    "o": hx("#343d47"),  # rim on the shaded lower right
    "O": hx("#56626e"),  # softer rim: tail stalk, fins
    "e": hx("#0a0a0a"),  # the eye
    "G": hx("#e8bf4c"), "g": hx("#c39a42"),  # golden forehead band: lit, shaded
    "p": hx("#68747f"), "P": hx("#46535e"),  # gill mark: soft edge, core
    "R": hx("#b8664a"),  # its red-orange foot
    "t": hx("#46535e"),  # dark tips of the forked tail
    # the pool: our own greener sea-blue ramp
    "x": hx("#173f52"),
    "y": hx("#1f5f74"),
    "z": hx("#2c8296"),
    "Z": hx("#47a6b4"),
    "v": hx("#9ee2dc"),
}

GRID = [
    "................",
    "................",
    "............t...",
    "......KbbK..4.t.",
    ".....KbWbbKO34t.",
    "....KbWWbbbKo...",
    "....bW1W1123o...",
    "...KGGg12234o...",
    "...b1e112334o...",
    "...b112Pp3445o..",
    ".3K1122R34445oO.",
    ".Ob1223334455oO.",
    "..O2233444555o..",
    ".xyoooooooooozx.",
    ".yzvZzzZvzzZzZy.",
    "..xy.yxxxy.xyx..",
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
    """Exact-pixel copy check against every vanilla spawn egg (as art/candidates/critic_lampuka_egg/check.py)."""
    ours = {(x, y): icon.getpixel((x, y)) for x in range(16) for y in range(16) if icon.getpixel((x, y))[3] > 0}
    hits, shared = [], set()
    vcols = set()
    for f in sorted(glob.glob(os.path.join(VANILLA, "*spawn_egg*.png"))):
        v = Image.open(f).convert("RGBA")
        if v.size != (16, 16):
            continue
        same = [p for p, c in ours.items() if v.getpixel(p) == c]
        if same:
            hits.append((len(same), os.path.basename(f)))
        vcols |= {v.getpixel((x, y))[:3] for x in range(16) for y in range(16) if v.getpixel((x, y))[3] > 0}
    shared = {c[:3] for c in ours.values()} & vcols
    hits.sort(reverse=True)
    most = f"most: {hits[0][0]} in {hits[0][1]}" if hits else "none"
    return [f"same pixel and colour as a vanilla spawn egg: {sum(n for n, _ in hits)} pixels over {len(hits)} eggs ({most})",
            f"our colours also used by any vanilla spawn egg: {len(shared)}"]


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 2180
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    refs = []
    for name in ("awrata_02.jpg", "awrata_06.jpg", "awrata_08.jpg", "awrata_09.jpg"):
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
        parts.append(("References (art/references/fish_awrata_refonly, list.tsv)", band))

    items = [("vanilla cod egg", os.path.join(VANILLA, "cod_spawn_egg.png")),
             ("vanilla salmon egg", os.path.join(VANILLA, "salmon_spawn_egg.png")),
             ("vanilla tropical fish egg", os.path.join(VANILLA, "tropical_fish_spawn_egg.png")),
             ("vanilla pufferfish egg", os.path.join(VANILLA, "pufferfish_spawn_egg.png")),
             ("our lampuka egg", os.path.join(TEXTURES, "item", "lampuka_spawn_egg.png")),
             ("our tonn egg", os.path.join(TEXTURES, "item", "tonn_spawn_egg.png")),
             ("our sardina egg", os.path.join(TEXTURES, "item", "sardina_spawn_egg.png")),
             ("our cerna egg", os.path.join(TEXTURES, "item", "cerna_spawn_egg.png")),
             ("NEW AWRATA EGG", None),
             ("awrata item icon", os.path.join(TEXTURES, "item", "awrata.png")),
             ("awrata bucket", "BUCKET")]
    band = Image.new("RGB", (W, 128 + 120), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        if p is None:
            im = icon
        elif p == "BUCKET":  # the layered bucket as the game draws it: vanilla cod bucket, our layer on top
            im = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
            im.alpha_composite(Image.open(os.path.join(TEXTURES, "item", "awrata_bucket.png")).convert("RGBA"))
        else:
            im = Image.open(p).convert("RGBA")
        x0 = 10 + i * 196
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(tile.convert("RGB"), (x0, 22))
        d.text((x0, 2), name, fill=ink, font=small)
        for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
            t = Image.new("RGBA", (40, 40), col + (255,))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x0 + (j % 2) * 44 + (j // 2) * 88, 156))
    d.text((10, 202), "8x, then 1x and 2x on light grey, 1x and 2x on dark grey", fill=ink, font=small)
    parts.append(("The egg at 8x and 1x beside vanilla's fish eggs, our accepted lampuka, tonn, sardina and cerna eggs, and the accepted awrata item icon and bucket", band))

    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "salmon", "tropical_fish", "pufferfish")]
                    + [os.path.join(TEXTURES, "item", n + "_spawn_egg.png") for n in ("lampuka", "tonn", "sardina", "cerna")] + [OUT_ICON])
    lines += copy_check(icon)
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py and the copy check", band))

    py = os.path.join(ART, ".venv", "bin", "python")
    items = ["mc:cod_spawn_egg", "mod:cerna_spawn_egg", "mod:awrata_spawn_egg", "mod:awrata"]
    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items +
                       ["--select", "2", "--scale", str(scale)], check=True, capture_output=True)
    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        im = Image.open(out).convert("RGB")
        band = Image.new("RGB", (W, im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(out, ROOT) + f"  (GUI scale {scale}: vanilla cod egg, "
                                  "our cerna egg, AWRATA EGG (selected), awrata item icon)", fill=ink, font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py, GUI scale {scale})", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Awrata (gilthead sea bream) spawn egg, textures/item/awrata_spawn_egg.png", fill=ink,
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
    icon = render(GRID)
    icon.save(OUT_ICON, optimize=False)
    print("wrote", OUT_ICON)
    sheet(icon)
