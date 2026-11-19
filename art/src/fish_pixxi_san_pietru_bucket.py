"""Bucket of pixxi San Pietru (John Dory, Zeus faber): the fish layer of the item icon (16 x 16), night job piece 3
of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md).

The bucket is not ours: the item model puts the player's own vanilla minecraft:item/cod_bucket underneath as layer0
and this texture on top as layer1, so the mod ships no Mojang pixels (STYLE rule 3). This file is ONLY the fish, the
bucket's back outline where a cod pixel lies under it, and our water: rows 6-15 are clear, every opaque cod pixel in
rows 0-5 is covered (check_cover()), no pixel equals vanilla's at the same place, and the back-rim outline stays dark
except where the head sits in front of it (check_rim() in art/src/fish_bucket_rim.py).

Owner rules this follows: the head rises out of the water, the vanilla way, never the tail (the cerna bucket); the
back outline stays visible (docs/Decisions/2026-11-18 Buckets - keep the back outline.md).

The John Dory's head, rising up and to the left: the dark jutting lower jaw and the gape at the top left, the black
eye with a pale gold pixel above it, the lit olive-gold head, the spiny dorsal fin standing up behind it, then the
tall body diving to the lower right into the water with the edge of St Peter's spot at the waterline. Colours are the
critic-passed item icon's (art/src/fish_pixxi_san_pietru_icon.py PAL), same keys, nothing new; the water is the
shared shades of the other buckets.

Candidates: A (the head high, the spot's edge at the waterline), B (the head a row lower, no spot), C (A with a
taller fin). Bucket critic rounds: 2 (PASS in round 2).

REDO 2026-11-19 (owner: "too flat and fat they dont look like the fish"): the grids below replaced the night version,
following the redrawn icon. C (greyer, near-black spines) chosen. Redo critic rounds: 3 of 3, all FAIL; the owner
judges. Blind reads: all three took it for a bucket of the same fish as the icon, probably a John Dory (50-55%).

REDO 2 2026-11-19 (owner: icon C accepted; the bucket fails, "the mouth looks like a magnet or duck bill"): redrawn
from the accepted icon in its palette, two candidates. Mouth critic rounds: A PASS in round 1, then the blind readers
still saw a pale bill (the head stuck out past the bucket), fixed, A PASS again in round 2.

Writes: mod/src/main/resources/assets/mimcontent/textures/item/pixxi_san_pietru_bucket.png (byte-identical on rerun),
the candidates in art/candidates/pixxi_san_pietru_bucket/ and the review sheet
art/candidates/fish_pixxi_san_pietru_bucket.png.
Run:    art/.venv/bin/python art/src/fish_pixxi_san_pietru_bucket.py
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fish_bucket_rim import RIM, OUTLINE, check_rim  # noqa: E402
from fish_pixxi_san_pietru_icon import PALS as ICONS, model_band  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
OUT = os.path.join(ITEMS, "pixxi_san_pietru_bucket.png")
VANILLA = os.path.join(ART, ".vanilla", "item")
CAND = os.path.join(ART, "candidates", "pixxi_san_pietru_bucket")
SHEET = os.path.join(ART, "candidates", "fish_pixxi_san_pietru_bucket.png")
CHOSEN = "A"


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = {
    "~": hx("#2a55c4"),  # water: the shared shades of the accepted buckets
    "v": hx("#1d3c96"),  # shadow on the water beside the fish where it goes under
    "^": hx("#6a92ea"),  # a glint of light on the water
    "#": RIM,            # the bucket's back-rim outline where we cover a cod pixel
}
PAL.update({k: ICONS["A"][k] for k in "oHGObWSRXEmjfnd"})
PAL["v"] = hx("#1d3c96")
PAL_C = dict(PAL)
PAL_C.update({k: ICONS["C"][k] for k in "oHGObWSRXEmjfnd"})   # C: the icon's greyer olive

GRIDS = {
    # Redo 2 (owner, 2026-11-19: icon C accepted; the bucket fails, "the mouth looks like a magnet or duck bill"):
    # redrawn from the accepted icon, in its palette. The head rises out of the water facing up and left with the
    # mouth only a small dark jaw line in the head's outline (no pale lips, nothing sticking out); the eye high on the
    # head, a black pupil with its pale ring above and in front, as on the icon; three near-black spines raked back
    # with light tips; the thumbprint mid-body above the water with a hint of pale ring; the back slopes into the
    # water. A: the gape a dark notch under the snout, the chin a step ahead. B: the gape opening upward at the
    # snout's tip, the jaw a dark line under it. Mouth critic round 1: A PASS (B's dark wedge read as a small beak);
    # its polish applied after: the lip tip k a softer dark olive-brown. Blind reads after it: all three still saw
    # a pale bill at the top left (the eye's two cream pixels and the lit chin), so the eye keeps one cream pixel above
    # it and the chin and the pixel in front of the eye are mid olive.
    # Round 2 fix: the head moved a pixel right so nothing pokes out past the bucket's left side (the pale snout out
    # there read as a bill), the spot a pixel further back from the eye. Round 2: A PASS (B's tan lower jaw read as
    # a flat open bill).
    "A": [
        "....oXon.n.n....",
        "...oOEfOfOf.....",
        "...kmOORSSb.....",
        "...ooObbSSbb#...",
        "..#~oObbbWW~~...",
        "..#~~obWWWv~~...",
    ],
    "B": [
        "....oXon.n.n....",
        "...mOEfOfOf.....",
        "...ooOORSSb.....",
        "...oOObbSSbb#...",
        "..#~oObbbWW~~...",
        "..#~~obWWWv~~...",
    ],
}
PAL_C["k"] = hx("#4a4230")                  # A's lip tip: dark olive-brown, not the outline's near-black (critic polish)
PALS = {"A": PAL_C, "B": PAL_C}


def fish_over_rim(grid):
    """The rim outline pixels the fish sits in front of: those our layer paints with a fish colour, not a dark grey."""
    def dark(c):
        return max(c) < 0x40 and max(c) - min(c) < 6
    return [(x, y) for (x, y) in OUTLINE if y < len(grid) and grid[y][x] not in ".~v^#" and not dark(PAL[grid[y][x]])]


FISH_OVER_RIM = {v: fish_over_rim(g) for v, g in GRIDS.items()}


def build(grid, P=PAL):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                img.putpixel((x, y), P[ch] + (255,))
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
    parts = [("The accepted model, side on in game (spine close-up, and in the tank)", model_band(W, bg))]
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
    hb = [hotbar(os.path.join(CAND, "hotbar.png"), ["mc:water_bucket", "mc:cod_bucket", "file:" + os.path.join(CAND, f"bucket_{CHOSEN}.png"),
                                                      "mod:pixxi_san_pietru", "bucket:kavall_bucket", "bucket:cerna_bucket",
                                                      "mc:salmon_bucket", "mc:pufferfish_bucket", "mc:tropical_fish_bucket"], 2),
          hotbar(os.path.join(CAND, "hotbar_x4.png"), ["mc:cod_bucket", "file:" + os.path.join(CAND, f"bucket_{CHOSEN}.png"),
                                                         "mod:pixxi_san_pietru", "bucket:cerna_bucket"], 4)]
    band = Image.new("RGB", (W, sum(i.height + 10 for i in hb) + 10), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    parts.append(("Hotbar preview, unselected: water, cod, PIXXI SAN PIETRU bucket, its item, kavall and cerna buckets, "
                  "salmon, pufferfish, tropical fish buckets at 2; cod, PIXXI SAN PIETRU bucket, its item, cerna bucket at 4",
                  band))
    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Bucket of pixxi San Pietru (John Dory), textures/item/pixxi_san_pietru_bucket.png", fill=ink,
           font=label_font(20))
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
