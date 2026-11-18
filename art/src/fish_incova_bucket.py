"""Bucket of incova (European anchovy): the fish layer of the item icon (16 x 16), 2026-11-18.

The bucket is not ours: the item model puts the player's own vanilla minecraft:item/cod_bucket underneath as layer0
and this texture on top as layer1, so the mod ships no Mojang pixels (STYLE rule 3) and the bucket matches whatever
resource pack the player uses. This file is therefore ONLY the fish, the bucket's back outline and our water: rows
6-15 are clear, and in rows 0-5 every opaque pixel of the cod in cod_bucket is covered so no cod shows through
(check_cover(), the same as the accepted cerna and awrata buckets), and the back-rim outline stays dark except where
the anchovy's head sits in front of it (check_rim() in art/src/fish_bucket_rim.py).

Owner rules this follows:
- "it should be the head mostly visible as vanilla fish" (the cerna bucket): only the head and the front of the body
  rise out of the water, never the tail;
- the bucket's back outline stays visible (docs/Decisions/2026-11-18 Buckets - keep the back outline.md): over
  cod_bucket the far edge is row 2 x5-10, its corners row 3 x3-4 and x11-12, the sides rows 4-5 x2 and x13. The head
  covers only row 2 x5-8 and, with its lower jaw, the corner 4,3; x9-10, 3,3, the right corner and both sides
  stay dark (our RIM grey where a cod pixel lies under it).

The incova is told apart from the sardina's bucket at 1x by:
- a slim, pointed head facing left and up, the snout tip (2,1) overhanging the mouth, a lit green crown above;
- one large eye set forward (5,1), with no light or white pixel below it;
- the long mouth line: one dark run on row 2 from under the snout (3,2) back past the eye (5,2), fading (J, 6,2);
  the lower jaw (4,3, grey g: a pale one read as a tooth) sits under it, set back behind the tip;
- a silver gill cover (s, 7,2) joining the head to the silver band;
- the greenish back and the bright silver band running down to the right into the water, one clean diagonal each
  (sheen h 8,2 to 11,5; dark back k 8,3 to 10,5; band W 7,3 to 9,5), with silver and the shaded belly rim below.
The sardina's bucket shows a level white fish over the water; this one shows a green-backed head diving in on a
diagonal.

Colours are the owner-accepted incova item icon's (textures/item/incova.png, art/src/fish_incova_icon.py PAL), same
keys, nothing new; the water is the shared shades of the other buckets, the inner wall where it shows is the head.
Photos (reference only): art/references/fish_incova_refonly/ (list.tsv).

Writes: mod/src/main/resources/assets/mimcontent/textures/item/incova_bucket.png (byte-identical on rerun)
With --sheet it also writes the review sheet art/candidates/fish_incova_bucket.png and the hotbar previews
art/candidates/fish_incova_bucket_hotbar.png (scale 2) and _hotbar_x4.png (scale 4).
Run:    art/.venv/bin/python art/src/fish_incova_bucket.py [--sheet]
"""
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_bucket_rim import RIM, check_rim  # noqa: E402
from fish_incova_icon import PAL as ICON  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "incova_bucket.png")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    # water: the shared shades of the accepted buckets
    "~": hx("#2a55c4"),
    "v": hx("#1d3c96"),  # shadow on the water beside the fish where it goes under
    "^": hx("#6a92ea"),  # a glint of light on the water
    "#": RIM,            # the bucket's back-rim outline where we cover a cod pixel (vanilla's is #353535)
}
# the incova: the owner-accepted icon's palette, same keys (only those used here)
PAL.update({k: ICON[k] for k in "hkmWsgoejJf"})

# rows 0-15, columns 0-15; "." is clear (vanilla cod_bucket's own outline or water shows there)
# Head: crown h h m on row 0 (rounded, 4-6), the snout tip f at 2,1 then the lit snout h 3,1; the eye 5,1 between a
# darker green m (4,1) and the lit back h (6,1). Mouth line j 3-5 on row 2 under the snout and the eye, J 6,2 where it
# fades past the eye; the grey lower jaw g 4,3 under it, the silver gill cover s 7,2. Behind the gill the body dives to the lower right at 45
# degrees: sheen h, dark back k, silver band W, silver s, belly rim o, each one clean diagonal into the water.
# Rim: row 2 x9-10 ours (#), x11 is cod_bucket's own dark; row 3 x3 and x11 ours, x12 cod_bucket's own; the sides
# rows 4-5 x2/x13 are cod_bucket's own. Water fills the mouth around the fish (v shadow beside it, ^ a glint).
GRID = [
    "....hhm.........",
    "..fhmehh........",
    "...jjjJsh##.....",
    "...#gosWkhv#....",
    "...~~vosWkhv~...",
    "....~^~osWkh....",
] + ["................"] * 10

# The back-rim outline pixels (art/src/fish_bucket_rim.py) the head covers; every other one stays dark
FISH_OVER_RIM = [(5, 2), (6, 2), (7, 2), (8, 2), (4, 3)]


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
REFS = os.path.join(ART, "references", "fish_incova_refonly")
SHEET = os.path.join(ART, "candidates", "fish_incova_bucket.png")
HOTBAR = ["mc:water_bucket", "mc:cod_bucket", "bucket:sardina_bucket", "bucket:incova_bucket", "mod:incova",
          "bucket:cerna_bucket", "bucket:awrata_bucket", "bucket:murina_bucket"]
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
    for scale, name in ((2, "fish_incova_bucket_hotbar.png"), (4, "fish_incova_bucket_hotbar_x4.png")):
        p = os.path.join(ART, "candidates", name)
        subprocess.run([PY, os.path.join(ART, "tools", "hotbar_preview.py"), p] + HOTBAR
                       + ["--select", "3", "--scale", str(scale)], check=True, capture_output=True)
        outs.append(p)
    return outs


def sheet():
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    from measure import measure

    font, small = label_font(16), label_font(13)
    W = 1500
    parts = []

    def text(lines, f=font):
        h = len(lines) * (f.size + 6) + 6
        im = Image.new("RGBA", (W, h), (255, 255, 255, 255))
        d = ImageDraw.Draw(im)
        for i, ln in enumerate(lines):
            d.text((10, 4 + i * (f.size + 6)), ln, fill=(0, 0, 0), font=f)
        return im

    parts.append(text(["Bucket of incova (16 x 16): references (photos, reference only)"]))
    row = Image.new("RGBA", (W, 190), (255, 255, 255, 255))
    x = 10
    for f in ("portugal.jpg", "lonja.jpg", "ifremer1.jpg", "side.jpg"):
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
             ("cerna (accepted)", ours_of("cerna_bucket")),
             ("awrata (accepted)", ours_of("awrata_bucket")),
             ("murina (accepted)", ours_of("murina_bucket")),
             ("sardina (older)", ours_of("sardina_bucket")),
             ("INCOVA (in game)", ours),
             ("our layer alone", layer),
             ("incova item", Image.open(os.path.join(ITEMS, "incova.png")).convert("RGBA"))]
    parts.append(text(["8x on the slot grey: vanilla water and cod buckets | accepted cerna, awrata, murina buckets | "
                       "older sardina bucket | INCOVA bucket (over cod_bucket) | the layer alone | accepted incova item",
                       "(the other buckets are as they are on disk now; another maker is fixing their back outline)"],
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
            row.alpha_composite(im.resize((32, 32), Image.NEAREST), (230 + i * 40, 9))
        parts.append(row)

    parts.append(text(["The back-rim outline (red marks): dark everywhere except the 5 pixels the head covers (blue)"]))
    from fish_bucket_rim import OUTLINE
    big = ours.resize((128, 128), Image.NEAREST)
    d = ImageDraw.Draw(big)
    for (x, y) in OUTLINE:
        col = (40, 80, 255) if (x, y) in FISH_OVER_RIM else (230, 30, 30)
        d.rectangle((x * 8, y * 8, x * 8 + 7, y * 8 + 7), outline=col)
    row = Image.new("RGBA", (W, 140), SLOT)
    row.alpha_composite(big, (10, 6))
    row.alpha_composite(ours.resize((128, 128), Image.NEAREST), (160, 6))
    parts.append(row)

    lines = ["art/tools/measure.py (whole bucket as players see it):"]
    tmp = os.path.join(os.path.dirname(SHEET), "fish_incova_bucket_measure.tmp.png")
    for n, im in icons[:7]:
        im.save(tmp)
        m = measure(tmp)
        lines.append(f"  {n:18s} coverage {m['coverage']:.2f}  colours {m['colours']:2d}  darkest {float(m['lmin']):.2f}"
                     f"  lightest {float(m['lmax']):.2f}  outline {float(m['edge_l']):.2f}  inside {float(m['interior_l']):.2f}"
                     f"  top-left minus bottom-right {float(m['tl_minus_br']):+.2f}")
    os.remove(tmp)
    parts.append(text(lines, small))

    for p in hotbars():
        parts.append(text([f"Hotbar preview (art/tools/hotbar_preview.py): water, cod, sardina, INCOVA bucket (selected), "
                           f"incova item, cerna, awrata, murina buckets, on sky and night: {os.path.relpath(p, ROOT)}"],
                          small))
        im = Image.open(p).convert("RGBA")
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
