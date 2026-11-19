"""Bucket of petrica (anglerfish, Lophius): the fish layer of the item icon (16 x 16), night job piece 3 of 3
(docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md).

The bucket is not ours: the item model puts the player's own vanilla minecraft:item/cod_bucket underneath as layer0
and this texture on top as layer1, so the mod ships no Mojang pixels (STYLE rule 3). This file is ONLY the fish, the
bucket's back outline where a cod pixel lies under it, and our water: rows 6-15 are clear, every opaque cod pixel in
rows 0-5 is covered (check_cover()), no pixel equals vanilla's at the same place, and the back-rim outline stays dark
except where the head sits in front of it (check_rim() in art/src/fish_bucket_rim.py).

Owner rules this follows: the head rises out of the water, the vanilla way, never the tail (the cerna bucket); the
back outline stays visible (docs/Decisions/2026-11-18 Buckets - keep the back outline.md).

The petrica's head rises out of the water facing the player: a flat slab as wide as the bucket's mouth, two small eyes
just under its top edge, each with an olive glint, the gape one level, very dark brown row from edge to edge (a seam,
not a grin), the lower jaw below it with two pale skin flaps, mottled brown, water showing beneath. Colours are the item
icon's (art/src/fish_petrica_icon.py PAL), plus the gape's dark brown; the water is the shared shades of the other buckets.

Candidates: A (chosen, critic round 3 PASS, then polished), B (the eyes in the top outline), C (eyes on two bumps, the
jaw wider than the bucket). Round 1 (a diagonal head like the icon's) and round 2 (a black gape over a pale jaw) failed.

Writes: mod/src/main/resources/assets/mimcontent/textures/item/petrica_bucket.png (byte-identical on rerun), the
candidates in art/candidates/petrica_bucket/ and the review sheet art/candidates/fish_petrica_bucket.png.
Run:    art/.venv/bin/python art/src/fish_petrica_bucket.py
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_bucket_rim import RIM, OUTLINE, check_rim  # noqa: E402
from fish_petrica_icon import PAL as ICON  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "petrica_bucket.png")
VANILLA = os.path.join(ART, ".vanilla", "item")
CAND = os.path.join(ART, "candidates", "petrica_bucket")
SHEET = os.path.join(ART, "candidates", "fish_petrica_bucket.png")
CHOSEN = "A"


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    "~": hx("#2a55c4"),  # water: the shared shades of the accepted buckets
    "v": hx("#1d3c96"),  # shadow on the water beside the fish where it goes under
    "^": hx("#6a92ea"),  # a glint of light on the water
    "#": RIM,            # the bucket's back-rim outline where we cover a cod pixel
}
PAL.update({k: ICON[k] for k in "12345BDELMRheo"})

# rows 0-5 (rows 6-15 clear); "." is clear (vanilla cod_bucket's own outline or water shows there)
# Round 1 (a diagonal head like the icon's) FAILED: it read as a wedge, beak or wood chip, the mouth didn't show and the
# eyes were lost. From round 2 the head faces the player: a flat slab as wide as the bucket, the gape one level dark row
# right across it, the pale lower jaw below it, eyes far apart at the top corners, each with a glint beside it.
# Round 2 (the slab with a black gape over a pale jaw, eyes at the top corners with a cream glint) FAILED: a grinning
# cartoon face or a burger. From round 3: the eyes sit up ON the head's top edge as two small bumps, nothing pale beside
# them; the gape is very dark brown, not black, from edge to edge; the jaw below it is brown with only 2 pale flaps;
# more scattered speckles; the mouth and jaw rows 1 px wider each side than the head (the lower jaw juts out).
GRIDS = {
    # A: the eyes just under the top outline, each with an olive glint e beside it (the frontal photo's eye colour);
    # Round 3 PASS (best A, its first version had the eyes in the outline and the jaw wider than the bucket); the
    # critic's polish applied: eyes down a row, the head no wider than the rim, two light flecks made mid brown.
    "A": [
        "...ooooooooooo..",
        "..o34Ee3B34Eeo..",
        "..o4343343B33o..",
        "..ommmmmmmmmmo..",
        "..o3L333333L3o..",
        "...v~~^~~~~v....",
    ],
    # B: the eyes in the top outline between light bumps (round 3: "bread crust", the eyes lost)
    "B": [
        "...o1E1ooo1E1o..",
        "..o3243B34232o..",
        "..o4323343B33o..",
        "..ommmmmmmmmmo..",
        "..o3L333333L3o..",
        "...v~~^~~~~v....",
    ],
    # C: the eyes on two light bumps above the top outline, the jaw wider than the bucket (round 3: "a toad")
    "C": [
        "....o1ooooo1o...",
        "...o2E2B342E2o..",
        "..o4323343B33o..",
        ".ommmmmmmmmmmmo.",
        ".o33L333333L33o.",
        "...v~~^~~~~v....",
    ],
}
PAL["m"] = hx("#3a2a1c")    # round 3: the gape very dark brown, not black, so it is a seam, not a grin
PALS = {"A": PAL, "B": PAL, "C": PAL}
# the back-rim outline pixels the fish sits in front of (everything else on the rim must stay dark: check_rim)
FISH_OVER_RIM = {v: [p for p in OUTLINE if g[p[1]][p[0]] not in ".#~v^"] for v, g in GRIDS.items()}


def build(grid, pal=PAL):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                img.putpixel((x, y), pal[ch] + (255,))
    return img


def composite(layer):
    """What players see: our layer over vanilla's cod bucket (review only; vanilla is never written out)."""
    base = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    base.alpha_composite(layer)
    return base


def check_cover(layer):
    """No cod may show through; rows 6-15 must be clear; no pixel may equal vanilla's at the same place."""
    for y in range(6, 16):
        assert all(layer.getpixel((x, y))[3] == 0 for x in range(16)), f"row {y} not clear"
    base = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
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


def hotbar(out, items, scale):
    py = os.path.join(ART, ".venv", "bin", "python")
    subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items + ["--scale", str(scale)],
                   check=True, capture_output=True)
    return Image.open(out).convert("RGB")


def sheet(layers):
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    font, small = label_font(16), label_font(13)
    W = 1500
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []
    band = Image.new("RGB", (W, 330), bg)
    d = ImageDraw.Draw(band)
    for i, (v, layer) in enumerate(layers.items()):
        comp = composite(layer)
        big = comp.resize((128, 128), Image.NEAREST)
        t = Image.new("RGBA", (136, 136), (139, 139, 139, 255))
        t.alpha_composite(big, (4, 4))
        band.paste(t.convert("RGB"), (10 + i * 300, 24))
        rim = comp.resize((128, 128), Image.NEAREST)
        dr = ImageDraw.Draw(rim)
        for (x, y) in OUTLINE:
            col = (40, 80, 255) if (x, y) in FISH_OVER_RIM[v] else (230, 30, 30)
            dr.rectangle((x * 8, y * 8, x * 8 + 7, y * 8 + 7), outline=col)
        t = Image.new("RGBA", (136, 136), (139, 139, 139, 255))
        t.alpha_composite(rim, (4, 4))
        band.paste(t.convert("RGB"), (150 + i * 300, 24))
        for j, s in enumerate((1, 2)):
            t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), (139, 139, 139, 255))
            t.alpha_composite(comp.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (10 + i * 300 + j * 40, 180))
        d.text((10 + i * 300, 4), f"{v}" + (" (chosen)" if v == CHOSEN else "") + ": 8x, rim check (red dark, blue fish)",
               fill=ink, font=small)
    parts.append(("Candidates over vanilla cod_bucket", band))
    hb = [hotbar(os.path.join(CAND, "hotbar.png"), ["mc:water_bucket", "mc:cod_bucket", "bucket:petrica_bucket",
                                                      "mod:petrica", "bucket:sardina_bucket", "bucket:incova_bucket",
                                                      "bucket:cerna_bucket", "mc:salmon_bucket", "bucket:tonn_bucket"], 2),
          hotbar(os.path.join(CAND, "hotbar_x4.png"), ["mc:cod_bucket", "bucket:petrica_bucket", "mod:petrica",
                                                         "bucket:incova_bucket"], 4)]
    band = Image.new("RGB", (W, sum(i.height + 10 for i in hb) + 10), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    parts.append(("Hotbar preview, unselected: water, cod, PETRICA bucket, petrica item, sardina, incova, cerna buckets, "
                  "salmon, tonn bucket at 2; cod, PETRICA bucket, petrica item, incova bucket at 4", band))
    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Bucket of petrica (anglerfish), textures/item/petrica_bucket.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(SHEET)
    print("wrote", os.path.relpath(SHEET, ROOT))


def main():
    os.makedirs(CAND, exist_ok=True)
    layers = {}
    for v, g in GRIDS.items():
        layer = build(g + ["................"] * 10, PALS[v])
        check_cover(layer)
        check_rim(layer, os.path.join(VANILLA, "cod_bucket.png"), FISH_OVER_RIM[v])
        layer.save(os.path.join(CAND, f"layer_{v}.png"))
        composite(layer).save(os.path.join(CAND, f"bucket_{v}.png"))
        layers[v] = layer
    layers[CHOSEN].save(OUT, optimize=False)
    sheet(layers)
    print("wrote", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
