"""Bucket of ċawl (adult Mediterranean damselfish, Chromis chromis): the fish layer of the item icon (16 x 16), 2026-11-18.

The bucket is not ours: the item model puts the player's own vanilla minecraft:item/cod_bucket underneath as layer0
and this texture on top as layer1, so the mod ships no Mojang pixels (STYLE rule 3) and the bucket matches whatever
resource pack the player uses. This file is therefore ONLY the fish, the bucket's back outline and our water: rows
6-15 are clear, and in rows 0-5 every opaque pixel of the cod in cod_bucket is covered so no cod shows through
(check_cover(), the same as the accepted ċerna and awrata buckets), and the back-rim outline stays dark except where
the ċawl's head sits in front of it (check_rim() in art/src/fish_bucket_rim.py).

Owner rules this follows:
- buckets show the head rising out of the water, the vanilla way, never the tail (the ċerna bucket decision);
- the bucket's back outline stays visible (docs/Decisions/2026-11-18 Buckets - keep the back outline.md): over
  cod_bucket the far edge is row 2 x5-10, its corners row 3 x3-4 and x11-12, the sides rows 4-5 x2 and x13. The head
  and back cover row 2 x5-10 and the left corner 3,3-4,3; the right corner (11,3 ours, 12,3 cod_bucket's own) and
  both sides stay dark;
- the face is never flat ("cawl's face is too flat"): the head is a lit dome, shaded to the chin.

The ċawl is told apart from the ċerna and awrata buckets at 1x by:
- its dark chocolate colour (the ċerna is reddish-brown, the awrata silver);
- a steep, rounded forehead, lit on top (H at 5,1 and 4,2, W around it), stepping x4, 3, then the short round snout
  at 2,3 and the small mouth L tucked under it at 3,4;
- a rounded cheek under the eye (critic fix): mid tones r 1 r on row 4 turning down into the shaded chin and throat
  (3 4 on row 5), so the face rounds from the lit dome to the throat instead of a lit band over a dark one, and the
  lower head stands clear of the rim grey;
- one large black eye set close to the snout (5,3) inside a pale ring of W (4,3, 6,3, 5,2), as in the photos; the
  only H pixel near it touches it at a corner (4,2), the same as the accepted icon, and nothing dark sits beside it;
- the curved gill line (7,3 3, 7,4 4, 6,5 o) with the body behind it a step lighter, then shading down to the water;
- the start of the dorsal crest swept back from the nape (D 8,1, c 9,1, D 10,1, and c 8,0 with a dark K tip at 9,0,
  kept dark so it does not read as an ear), the dark back rim (K) running down into the water at 10,2.
Colours are the owner-accepted ċawl item icon's (textures/item/cawl.png, art/src/fish_cawl_icon.py PAL), same
keys, nothing new; the water is the shared shades of the other buckets.
Photos (reference only): art/references/fish_cawl_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/cawl_bucket.png (byte-identical on rerun)
With --sheet it also writes the review sheet art/candidates/fish_cawl_bucket.png and the hotbar previews
art/candidates/fish_cawl_bucket_hotbar.png (scale 2) and _hotbar_x4.png (scale 4).
Run:    art/.venv/bin/python art/src/fish_cawl_bucket.py [--sheet]
"""
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_bucket_rim import RIM, check_rim  # noqa: E402
from fish_cawl_icon import PAL as ICON  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "cawl_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water: the shared shades of the accepted buckets
    "~": hx("#2a55c4"),
    "v": hx("#1d3c96"),  # shadow on the water beside the fish where it goes under
    "^": hx("#6a92ea"),  # a glint of light on the water
    "#": RIM,            # the bucket's back-rim outline where we cover a cod pixel (vanilla's is #353535)
}
# the ċawl: the owner-accepted icon's palette, same keys (only those used here)
PAL.update({k: ICON[k] for k in "KbHW12345oeLDcrd"})  # d: only in PREVIOUS (sheet)

# rows 0-15, columns 0-15; "." is clear (vanilla cod_bucket's own outline or water shows there)
# Row 0: the tip of the dorsal crest (c, K), swept back. Row 1: the top of the forehead dome, its rounded edge K
# at 4,1, the highlight H, then W and 1 back to the crest's base D, c, d. Row 2: the forehead's front edge K 3,2, H at
# the top left, W above the eye, the body 1 2 shading back to the band b and the dark back rim K going under at 10,2.
# Row 3: the short snout K 2,3, the snout 1 and the pale ring W | eye e | W, the gill 3 at 7,3, the body 2 2 3 and our rim grey at
# 11,3. Row 4: the small mouth L 3,4 under the snout, the rounded cheek r 1 r, the gill 4, the flank going
# under (3 4) beside the water's shadow. Row 5: the chin and throat 3 4 and belly rim o into the water.
GRID = [
    "........cK......",
    "....KHW1DcD.....",
    "...KHWW12bK.....",
    "..K1WeW3223#....",
    "...Lr1r434v~~...",
    "....34ov~^~~....",
] + ["................"] * 10

# The first version (critic, 2026-11-18: the face read as two bands, a lit top over a dark bottom, the "too flat" the
# owner sent the icon back for; the lower head merged into the rim grey; the pale crest tip read as an ear at 2x).
# Sheet only.
PREVIOUS = [
    "........dc......",
    "....KHW1Dcd.....",
    "...KHWW12bK.....",
    "..KWWeW3223#....",
    "...L332434v~~...",
    "....45ov~^~~....",
] + ["................"] * 10

# The back-rim outline pixels (art/src/fish_bucket_rim.py) the head and back cover; every other one stays dark
FISH_OVER_RIM = [(5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (3, 3), (4, 3)]


def build(grid=GRID):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(grid):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                px[x, y] = PAL[ch] + (255,)
    return img


VANILLA = os.path.join(ART, ".vanilla", "item")
REFS = os.path.join(ART, "references", "fish_cawl_refonly")
SHEET = os.path.join(ART, "candidates", "fish_cawl_bucket.png")
HOTBAR = ["mc:water_bucket", "mc:cod_bucket", "bucket:cerna_bucket", "bucket:awrata_bucket", "bucket:cawl_bucket",
          "mod:cawl", "bucket:murina_bucket", "bucket:pixxispad_bucket", "bucket:incova_bucket"]
SLOT = (139, 139, 139, 255)
PY = os.path.join(ART, ".venv", "bin", "python")


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


def hotbars():
    outs = []
    for scale, name in ((2, "fish_cawl_bucket_hotbar.png"), (4, "fish_cawl_bucket_hotbar_x4.png")):
        p = os.path.join(ART, "candidates", name)
        subprocess.run([PY, os.path.join(ART, "tools", "hotbar_preview.py"), p] + HOTBAR
                       + ["--select", "4", "--scale", str(scale)], check=True, capture_output=True)
        outs.append(p)
    return outs


def sheet():
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    from measure import measure
    from fish_bucket_rim import OUTLINE

    font, small = label_font(16), label_font(13)
    W = 1700
    parts = []

    def text(lines, f=font):
        h = len(lines) * (f.size + 6) + 6
        im = Image.new("RGBA", (W, h), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    parts.append(text(["Bucket of ċawl (16 x 16): references (photos, reference only; art/references/fish_cawl_refonly)"]))
    row = Image.new("RGBA", (W, 190), (255, 255, 255, 255))
    x = 10
    for f in ("cawl_04.jpg", "cawl_02.jpg", "cawl_07.jpg", "cawl_10.jpg"):
        p = os.path.join(REFS, f)
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGBA")
        im.thumbnail((340, 180))
        row.alpha_composite(im, (x, 5))
        x += im.width + 10
    parts.append(row)

    layer = Image.open(OUT).convert("RGBA")
    ours = composite(layer)

    def ours_of(n):
        return composite(Image.open(os.path.join(ITEMS, n + ".png")).convert("RGBA"))

    icons = [("water bucket", Image.open(os.path.join(VANILLA, "water_bucket.png")).convert("RGBA")),
             ("cod bucket", Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")),
             ("ċerna (accepted)", ours_of("cerna_bucket")),
             ("awrata (accepted)", ours_of("awrata_bucket")),
             ("murina (accepted)", ours_of("murina_bucket")),
             ("pixxispad (accepted)", ours_of("pixxispad_bucket")),
             ("żiemel (accepted)", ours_of("ziemel_bucket")),
             ("inċova", ours_of("incova_bucket")),
             ("ĊAWL (in game)", ours),
             ("our layer alone", layer),
             ("ċawl item (accepted)", Image.open(os.path.join(ITEMS, "cawl.png")).convert("RGBA"))]
    parts.append(text(["8x on the slot grey: vanilla water and cod buckets | our ċerna, awrata, murina, pixxispad, żiemel "
                       "and inċova buckets | ĊAWL bucket (over cod_bucket) | the layer alone | accepted ċawl item"],
                      small))
    row = Image.new("RGBA", (W, 16 * 8 + 30), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate(icons):
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (10 + i * 150, 4))
        d.text((10 + i * 150, 134), n, fill=(0, 0, 0), font=small)
    parts.append(row)

    parts.append(text(["1x and 2x (same order), on the slot grey and on dark"]))
    for bg in (SLOT, (40, 40, 40, 255)):
        row = Image.new("RGBA", (W, 50), bg)
        for i, (n, im) in enumerate(icons):
            row.alpha_composite(im, (10 + i * 22, 17))
            row.alpha_composite(im.resize((32, 32), Image.NEAREST), (270 + i * 40, 9))
        parts.append(row)

    old = composite(build(PREVIOUS))
    parts.append(text(["First version (critic: face in two flat bands, crest tip like an ear) and the FIXED version, "
                       "at 8x, then 2x and 1x on the slot grey and on dark"]))
    row = Image.new("RGBA", (W, 150), SLOT)
    d = ImageDraw.Draw(row)
    for i, (n, im) in enumerate((("first version", old), ("FIXED", ours))):
        x0 = 10 + i * 420
        row.alpha_composite(im.resize((128, 128), Image.NEAREST), (x0, 4))
        d.text((x0, 134), n, fill=(0, 0, 0), font=small)
        row.alpha_composite(im.resize((32, 32), Image.NEAREST), (x0 + 140, 10))
        row.alpha_composite(im, (x0 + 180, 18))
        dk = Image.new("RGBA", (80, 48), (40, 40, 40, 255))
        dk.alpha_composite(im.resize((32, 32), Image.NEAREST), (6, 8))
        dk.alpha_composite(im, (52, 16))
        row.alpha_composite(dk, (x0 + 210, 2))
    parts.append(row)

    parts.append(text([f"The back-rim outline (red marks): dark everywhere except the {len(FISH_OVER_RIM)} pixels the "
                       "head and back cover (blue)"]))
    big = ours.resize((128, 128), Image.NEAREST)
    d = ImageDraw.Draw(big)
    for (x, y) in OUTLINE:
        col = (40, 80, 255) if (x, y) in FISH_OVER_RIM else (230, 30, 30)
        d.rectangle((x * 8, y * 8, x * 8 + 7, y * 8 + 7), outline=col)
    row = Image.new("RGBA", (W, 140), SLOT)
    row.alpha_composite(big, (10, 6))
    row.alpha_composite(ours.resize((128, 128), Image.NEAREST), (160, 6))
    row.alpha_composite(Image.open(os.path.join(ITEMS, "cawl.png")).convert("RGBA").resize((128, 128), Image.NEAREST),
                        (310, 6))
    parts.append(row)

    lines = ["art/tools/measure.py (whole bucket as players see it):"]
    tmp = os.path.join(os.path.dirname(SHEET), "fish_cawl_bucket_measure.tmp.png")
    for n, im in icons[:9] + [("ċawl first version", old)]:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:22s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside {float(m['interior_l']):.2f}"
                     f"  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    for p in hotbars():
        parts.append(text([f"Hotbar preview (art/tools/hotbar_preview.py): water, cod, ċerna, awrata, ĊAWL bucket (selected), "
                           f"ċawl item, murina, pixxispad, inċova buckets, on sky and night: {os.path.relpath(p, ROOT)}"],
                          small))
        im = Image.open(p).convert("RGBA")
        if im.width > W - 20:
            im = im.resize((W - 20, round(im.height * (W - 20) / im.width)), Image.NEAREST)
        row = Image.new("RGBA", (W, im.height + 10), (255, 255, 255, 255))
        row.alpha_composite(im, (10, 5))
        parts.append(row)

    out = Image.new("RGBA", (W, sum(p.height for p in parts)), (255, 255, 255, 255))
    y = 0
    for p in parts:
        out.alpha_composite(p, (0, y))
        y += p.height
    os.makedirs(os.path.dirname(SHEET), exist_ok=True)
    out.convert("RGB").save(SHEET)
    print("wrote", os.path.relpath(SHEET, ROOT))


if __name__ == "__main__":
    layer = build()
    check_cover(layer)
    check_rim(layer, os.path.join(VANILLA, "cod_bucket.png"), FISH_OVER_RIM)
    layer.save(OUT, optimize=False)
    print("wrote", os.path.relpath(OUT, ROOT))
    if "--sheet" in sys.argv[1:]:
        sheet()
