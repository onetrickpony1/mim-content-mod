"""Bucket of murina: the fish layer of the item icon (16 x 16), 2026-11-18.

The bucket is not ours: the item model (made by art/src/pilot_models.py) puts the player's own vanilla
minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships no Mojang
pixels (STYLE rule 3) and the bucket matches whatever resource pack the player uses. This file is therefore ONLY
the fish: rows 6-15 are clear, and in rows 1-5 every opaque pixel of the cod in cod_bucket is covered so no cod
shows through (checked by check_cover() on every run, against art/.vanilla's cod_bucket when it is there).
Same method as the owner-accepted cerna bucket (art/src/fish_cerna_bucket.py), whose check and water shades it uses.

Laid out the way vanilla shows its live fish in a bucket, and the way the owner asked for the cerna ("the head
mostly visible as vanilla fish", 2026-11-18): only the head and the neck rise out of the water inside the rim, the
head at the upper left, the neck sloping down to the right into the water. No tail shows: the rest of the eel is
under water. A moray pokes its head out of a hole with its mouth open (photos m07, m09, m16, m19), so the pose suits
it. The back of the rim stays visible at the right (11,2 / 12,3 / 13,4) and the water at the front edge.

The murina (Mediterranean moray, Muraena helena) is told apart at 1x by:
- the broad head, six rows high, with a raised crown (rows 0-1) that steps down to the narrower neck behind it;
- the pointed snout (the lit upper lip at 2,3, one pixel past the rim as the forehead slopes down to it);
- the long dark mouth line (row 4) under the snout, with the lower jaw lit at its tip below it: the mouth open;
- the one small pale eye above the front of the mouth, with only lit body tones round it (no dark pixel, no spot);
- the violet-brown skin, lit on the crown (top left) and shading to the throat and the neck's far side;
- a few cream spots on the neck where it meets the water (none on the head, as on the accepted icon).
Colours are the owner-accepted murina item icon's (textures/item/murina.png, art/src/fish_murina_icon.py), same
keys, nothing new; the water where the eel goes under is the cerna bucket's own shades.
Photos (reference only): art/references/fish_murina_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/murina_bucket.png (byte-identical on rerun)
With --sheet it also writes the review sheet art/candidates/fish_murina_bucket.png (references, what players see,
i.e. this layer over vanilla's cod_bucket, at 8x and 1x beside vanilla's fish buckets and the accepted cerna bucket,
the layer alone, the accepted murina item, measure.py numbers, and offline hotbar previews at GUI scale 2 and 4).
Run:    art/.venv/bin/python art/src/fish_murina_bucket.py [--sheet]
"""
import os
import subprocess

from PIL import Image

from fish_bucket_rim import check_rim

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item",
                   "murina_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water where the eel goes under: the accepted cerna bucket's shades
    "~": hx("#2a55c4"),
    "v": hx("#1d3c96"),  # the shadow on the water beside the neck
    "^": hx("#6a92ea"),  # a glint of light on the water
    # the murina: the owner-accepted item icon's palette (textures/item/murina.png, art/src/fish_murina_icon.py)
    "1": hx("#8c6a6a"), "2": hx("#765660"), "3": hx("#62464e"), "4": hx("#503a40"), "5": hx("#433036"),  # lit to shade
    "k": hx("#705660"),                       # lit rim: the crown and the top of the neck
    "C": hx("#e2d09c"), "c": hx("#b49c84"), "d": hx("#806a6c"),  # cream spots: in the light, mid, in the shade
    "E": hx("#f0e8bc"),                       # the small pale eye, the only pale mark on the head
    "L": hx("#866670"), "l": hx("#5c4650"),   # the lit lip tips (snout, lower jaw) and the shaded lower jaw
    "M": hx("#200f14"),                       # the open mouth line
}

# rows 0-15, columns 0-15; "." is clear
# The crown (5-7,0) rises a row above the neck's top (8-9,1 then 10,2), so the head stands out broad from the
# narrower neck. The forehead slopes down to the left in single steps (4,1 / 3,2) to the pointed snout (L, 2,3); the
# mouth line runs back under it along row 4 (3-5) and ends in the shaded corner (l, 6,4); the lower jaw shows below
# it, lit at the tip (L, 3,5). The eye (5,2) sits above the front of the mouth with only lit tones round it. The neck
# slopes down to the right, shading 2-3-4-5 to its far side, into the water: a shadow (v) beside it and a glint (^).
# Spots only on the neck near the waterline (c 7,3 and 8,4, d 10,4 and 7,5, C 8,5): the one bright spot sits low at
# the waterline, well below the eye, so it cannot read as a second eye (critic, 2026-11-18).
GRID = [
    ".....kkk........",
    "....k111kk......",
    "...k1E1122k.....",
    "..L1222c3345....",
    "...MMMl3c4dv~...",
    "...Ll45dCv^~....",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# Shapes tried and dropped on the way (sheet only): the snout inside the rim made the front a flat wall, and a crown
# level with the neck read as a lump, not a head.
TRIED = {
    "snout in the rim": [
        "................",
        "....kkkk........",
        "...k1E12kkk.....",
        "...L11223C3~....",
        "...MMMl34c5v~...",
        "....l45dv~^~....",
    ] + ["................"] * 10,
    "crown level with neck": [
        "................",
        "....kkkkk.......",
        "...k1E1122k.....",
        "...L1222334~....",
        "...MMMl34c5v~...",
        "...Ll45dCv^~....",
    ] + ["................"] * 10,
}


# The back-rim outline pixels (art/src/fish_bucket_rim.py) that the head and the neck cover; every other one stays dark
FISH_OVER_RIM = [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3), (11, 3)]


def build(grid=GRID):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(grid):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                px[x, y] = PAL[ch] + (255,)
    return img


ART = os.path.join(ROOT, "art")
VANILLA = os.path.join(ART, ".vanilla", "item")
ITEMS = os.path.dirname(OUT)
REFS = os.path.join(ART, "references", "fish_murina_refonly")
SHEET = os.path.join(ART, "candidates", "fish_murina_bucket.png")
SLOT = (139, 139, 139, 255)


def hotbars():
    """Offline hotbar previews (art/tools/hotbar_preview.py) at GUI scale 2 and 4."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    outs = []
    for suffix, scale in (("", "2"), ("_x4", "4")):
        out = os.path.join(ART, "candidates", f"fish_murina_bucket_hotbar{suffix}.png")
        subprocess.run([py, tool, out, "mc:cod_bucket", "bucket:cerna_bucket", "bucket:murina_bucket",
                        "mc:salmon_bucket", "mod:murina", "--select", "2", "--scale", scale],
                       check=True, capture_output=True)
        outs.append(out)
    return outs


def sheet():
    import sys
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    from measure import measure

    font, small = label_font(16), label_font(13)
    W = 1700
    parts = []

    def text(lines, f=font, h=None):
        h = h or (len(lines) * (f.size + 6) + 6)
        im = Image.new("RGBA", (W, h), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    # references: morays with the head out of a hole, mouth open
    parts.append(text(["Bucket of murina (16 x 16): references, the head out of a hole with the mouth open "
                       "(art/references/fish_murina_refonly, reference only)"]))
    row = Image.new("RGBA", (W, 190), (255, 255, 255, 255))
    x = 10
    for f in ("m16.jpg", "m19.jpg", "m07.jpg", "m09.jpg", "o01.jpg"):
        im = Image.open(os.path.join(REFS, f)).convert("RGBA")
        im.thumbnail((320, 180))
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    parts.append(row)

    ours = composite(Image.open(OUT).convert("RGBA"))
    cerna = composite(Image.open(os.path.join(ITEMS, "cerna_bucket.png")).convert("RGBA"))
    icons = [("cod", Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")),
             ("salmon", Image.open(os.path.join(VANILLA, "salmon_bucket.png")).convert("RGBA")),
             ("tropical fish", Image.open(os.path.join(VANILLA, "tropical_fish_bucket.png")).convert("RGBA")),
             ("pufferfish", Image.open(os.path.join(VANILLA, "pufferfish_bucket.png")).convert("RGBA")),
             ("cerna bucket", cerna),
             ("MURINA (in game)", ours),
             ("our layer alone", Image.open(OUT).convert("RGBA")),
             ("murina item", Image.open(os.path.join(ITEMS, "murina.png")).convert("RGBA"))]
    tried = [(n, composite(build(g))) for n, g in TRIED.items()]
    parts.append(text(["8x on the slot grey: vanilla cod, salmon, tropical fish, pufferfish | accepted cerna bucket | "
                       "MURINA (over cod_bucket) | layer alone | accepted murina item | shapes tried and dropped"]))
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(icons + tried):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)

    parts.append(text(["1x and 2x, on the slot grey and on dark (same order)"]))
    row = Image.new("RGBA", (W, 100), SLOT)
    ImageDraw.Draw(row).rectangle((0, 50, W, 100), fill=(40, 40, 40))
    for i, (n, im) in enumerate(icons):
        for y0 in (0, 50):
            row.alpha_composite(im, (10 + i * 20, y0 + 17))
            row.alpha_composite(im.resize((32, 32), Image.NEAREST), (200 + i * 40, y0 + 9))
    parts.append(row)

    lines = ["art/tools/measure.py (whole composite as players see it):"]
    tmp = os.path.join(os.path.dirname(SHEET), "fish_murina_bucket_measure.tmp.png")
    for n, im in icons[:6]:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:18s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside {float(m['interior_l']):.2f}"
                     f"  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    parts.append(text(["Hotbar preview (art/tools/hotbar_preview.py, offline, as the game draws flat items) at GUI scale 2 "
                       "and 4: vanilla cod bucket, cerna bucket, MURINA BUCKET (selected), vanilla salmon bucket, "
                       "murina item"]))
    for p in hotbars():
        hb = Image.open(p).convert("RGBA")
        row = Image.new("RGBA", (W, hb.height + 10), (255, 255, 255, 255))
        row.alpha_composite(hb, (10, 5))
        parts.append(row)

    out = Image.new("RGBA", (W, sum(p.height for p in parts)), (255, 255, 255, 255))
    y = 0
    for p in parts:
        out.alpha_composite(p, (0, y))
        y += p.height
    os.makedirs(os.path.dirname(SHEET), exist_ok=True)
    out.convert("RGB").save(SHEET)
    print("wrote", os.path.relpath(SHEET, ROOT))


def composite(layer):
    """What players see: our layer over vanilla's cod bucket (review only; vanilla is never written out)."""
    base = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    base.alpha_composite(layer)
    return base


def check_cover(layer):
    """No cod may show through; rows 6-15 must be clear; no pixel may equal vanilla's at the same place."""
    cod = os.path.join(VANILLA, "cod_bucket.png")
    for y in range(6, 16):
        assert all(layer.getpixel((x, y))[3] == 0 for x in range(16)), f"row {y} not clear"
    if not os.path.exists(cod):
        print("note: art/.vanilla missing, cover not checked")
        return
    base = Image.open(cod).convert("RGBA")
    fishy = [(x, y) for y in range(6) for x in range(16)
             if base.getpixel((x, y))[3] and base.getpixel((x, y))[:3] not in ((0x35, 0x35, 0x35), (0x23, 0x4f, 0xcc))]
    shows = [p for p in fishy if layer.getpixel(p)[3] == 0]
    assert not shows, f"cod shows through at {shows}"
    same = []
    for n in ("cod_bucket", "salmon_bucket", "tropical_fish_bucket", "water_bucket", "bucket"):
        v = Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")
        same += [(n, x, y) for y in range(16) for x in range(16)
                 if layer.getpixel((x, y))[3] and layer.getpixel((x, y)) == v.getpixel((x, y))]
    assert not same, f"pixels identical to vanilla: {same}"
    print(f"cover ok: all {len(fishy)} cod pixels covered, 0 pixels identical to vanilla")


if __name__ == "__main__":
    import sys
    layer = build()
    check_cover(layer)
    check_rim(layer, os.path.join(VANILLA, "cod_bucket.png"), FISH_OVER_RIM)
    layer.save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT))
    if "--sheet" in sys.argv[1:]:
        sheet()
