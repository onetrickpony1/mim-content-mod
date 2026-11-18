"""Bucket of tonn: the fish layer of the item icon (16 x 16), 2026-11-18.

The bucket is not ours: the item model (made by art/src/pilot_models.py) puts the player's own vanilla
minecraft:item/cod_bucket underneath as layer0 and this texture on top as layer1, so the mod ships no Mojang
pixels (STYLE rule 3) and the bucket matches whatever resource pack the player uses. This file is therefore ONLY
the fish: rows 6-15 are clear, and in rows 1-5 the tuna covers every opaque pixel of the cod in cod_bucket so no
cod shows through (checked by check_cover() on every run, against art/.vanilla's cod_bucket when it is there).
Same method as the lampuka bucket (art/src/fish_lampuka_bucket.py).

Laid out the way vanilla lays its live fish in a bucket (measured from cod_bucket, salmon_bucket,
tropical_fish_bucket): the fish lies across the bucket mouth in rows 1 to 5, head to the left, tail to the right
against the back of the rim, with no black outline of its own (its darkest shades make its edge).

The tonn (Atlantic bluefin tuna, Thunnus thynnus) is told apart at 1x by:
- the thick dark blue-black back, two rows deep over most of the body, turning to blue along the side;
- the pointed snout at the left (one pixel ahead of the head) and the eye low on the blue cheek;
- the silver-white belly, shaded grey along its lower edge;
- the narrow tail stalk with yellow finlets above and below it (lit above, shaded below);
- the crescent tail at the right: a dark base with two lobes, both tips blue, notch open to the right.
Colours are the tonn item icon's (textures/item/tonn.png, art/src/fish_tonn_icon.py); the water seen under the
tail stalk is our own shade, the same as the lampuka bucket's. Photos (reference only):
art/references/fish_tonn_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/tonn_bucket.png
With --sheet it also writes the review sheet art/candidates/fish_tonn_bucket.png (references, what players see,
i.e. this layer over vanilla's cod_bucket, at 8x and 1x beside vanilla's fish buckets and the lampuka bucket,
the layer alone, measure.py numbers, and the in-game hotbar crop from the tonnbucket2 art run).
Run:    art/.venv/bin/python art/src/fish_tonn_bucket.py [--sheet]
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item",
                   "tonn_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water under the tail stalk: our own shade (the lampuka bucket's), near the bucket's deep water
    "~": hx("#2a55c4"),
    # the tonn: the item icon's colours
    "o": hx("#181e2c"),  # darkest navy: the top edge of the back, the tail stalk
    "k": hx("#1f2d52"),  # dark blue-black: the back
    "b": hx("#3a5e98"),  # blue: the side below the back; both tail tips (the lower one seen against the dark rim)
    "h": hx("#6584b8"),  # light blue: snout and forehead
    "H": hx("#a0b8dc"),  # pale blue: light on the cheek
    "w": hx("#e8edf1"),  # silver-white: throat and belly
    "s": hx("#b4bfcb"),  # silver
    "g": hx("#848fa0"),  # grey silver: lower belly
    "G": hx("#5a6476"),  # dark grey: the belly's shaded edge
    "e": hx("#0a0a0a"),  # the eye
    "y": hx("#f0c828"),  # finlets, lit (above the stalk)
    "Y": hx("#a8801a"),  # finlets, shaded (below the stalk)
    "t": hx("#1b2746"),  # the tail
}

# rows 0-15, columns 0-15; "." is clear
GRID = [
    "................",
    "....hkkkko...b..",
    "...hkkkkkkyyt...",
    "..hHebbbbbGot...",
    "...wwwwssgYYt...",
    "....gssggG~~.b..",
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


def build():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(GRID):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                px[x, y] = PAL[ch] + (255,)
    return img


VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")
ITEMS = os.path.dirname(OUT)
REFS = os.path.join(ROOT, "art", "references", "fish_tonn_refonly")
SHOTS = os.path.join(ROOT, ".art-runs", "tonnbucket2", "build", "smoke-run", "screenshots")
SHEET = os.path.join(ROOT, "art", "candidates", "fish_tonn_bucket.png")
SLOT = (139, 139, 139, 255)


def sheet():
    import glob
    import sys
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
    from font import label_font
    from measure import measure

    font, small = label_font(16), label_font(13)
    W = 1500
    parts = []

    def text(lines, f=font, h=None):
        h = h or (len(lines) * (f.size + 6) + 6)
        im = Image.new("RGBA", (W, h), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    # references
    parts.append(text(["Bucket of tonn (16 x 16): references (photos and drawings, reference only)"]))
    row = Image.new("RGBA", (W, 190), (255, 255, 255, 255))
    x = 10
    for f in ("tonn_02.jpg", "tonn_06.jpg", "tonn_04.jpg", "tonn_13.jpg"):
        im = Image.open(os.path.join(REFS, f)).convert("RGBA")
        im.thumbnail((340, 180))
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    parts.append(row)

    # 8x beside vanilla and the lampuka bucket
    names = [("cod", os.path.join(VANILLA, "cod_bucket.png")), ("salmon", os.path.join(VANILLA, "salmon_bucket.png")),
             ("tropical fish", os.path.join(VANILLA, "tropical_fish_bucket.png")),
             ("lampuka bucket", "LAMPUKA"), ("TONN (in game)", None), ("our layer alone", OUT),
             ("tonn item", os.path.join(ITEMS, "tonn.png"))]
    tonn = composite(Image.open(OUT).convert("RGBA"))
    lamp = composite(Image.open(os.path.join(ITEMS, "lampuka_bucket.png")).convert("RGBA"))
    tmp = os.path.join(os.path.dirname(SHEET), "fish_tonn_bucket_composite.tmp.png")
    tmp_l = os.path.join(os.path.dirname(SHEET), "fish_tonn_bucket_lampuka.tmp.png")
    tonn.save(tmp)
    lamp.save(tmp_l)

    def load(p):
        return tonn if p is None else lamp if p == "LAMPUKA" else Image.open(p).convert("RGBA")

    icons = [(n, load(p)) for n, p in names]
    parts.append(text(["8x on the slot grey: vanilla cod, salmon, tropical fish buckets | the lampuka bucket | the tonn "
                       "bucket as players see it (our layer over their cod_bucket) | our layer alone | the tonn item"]))
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(icons):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)

    parts.append(text(["1x and 2x, as in the hotbar (same order)"]))
    row = Image.new("RGBA", (W, 60), SLOT)
    for i, (n, im) in enumerate(icons):
        row.alpha_composite(im, (10 + i * 20, 20))
        row.alpha_composite(im.resize((32, 32), Image.NEAREST), (200 + i * 40, 12))
    parts.append(row)

    lines = ["art/tools/measure.py:"]
    for n, p in names[:6]:
        m = measure(tmp if p is None else tmp_l if p == "LAMPUKA" else p)
        lines.append(f"  {n:15s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside {float(m['interior_l']):.2f}"
                     f"  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    os.remove(tmp_l)
    parts.append(text(lines, small))

    shots = sorted(glob.glob(os.path.join(SHOTS, "*fish-08*.png")))
    parts.append(text(["In game, hotbar at 3x (art run tonnbucket2; slot 1 vanilla cod, last vanilla salmon; the rest are "
                       "the mod's fish items, buckets and eggs): " + (", ".join(os.path.basename(s) for s in shots)
                                                                      or "no shots yet")]))
    for s in shots:
        im = Image.open(s).convert("RGBA")
        sx = im.width / 854
        hb = im.crop((round(240 * sx), round(430 * sx), round(612 * sx), im.height))  # the hotbar
        hb = hb.resize((hb.width * 3, hb.height * 3), Image.NEAREST)
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
    layer.save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT))
    if "--sheet" in sys.argv[1:]:
        sheet()
