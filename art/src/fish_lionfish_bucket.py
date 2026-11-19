"""Bucket of lionfish: the fish layer of the item icon (16 x 16), night job 2026-11-19.

The bucket is not ours: the item model puts the player's own vanilla minecraft:item/cod_bucket underneath as layer0
and this texture on top as layer1, so the mod ships no Mojang pixels (STYLE rule 3). Rows 6-15 are clear, and in rows
0-5 every opaque pixel of the cod in cod_bucket is covered so no cod shows through (check_cover() on every run). The
back-rim outline is checked by art/src/fish_bucket_rim.py (the owner's "keep the back outline").

Owner rule: a bucket shows the fish's head rising out of the water, the vanilla way, never the tail or the whole fish.
For the lionfish that head carries:
  - the bands: red-brown and cream across the head and the back as it sinks into the water (in the eye's own row the
    red-brown is its pale belly tone, so nothing dark sits near the eye);
  - one black eye in pale skin, with a red-brown tentacle and a cream tip standing over it;
  - behind the head, the long separate spines standing up out of the water, red-brown with cream tips;
  - the tip of the fan pectoral breaking the water beside the head.
Colours are the passed icon's (art/src/fish_lionfish_icon.py PAL, the model's palette C lifted x1.2), nothing new;
the water and the rim tone are the shared bucket shades (art/src/fish_bucket_rim.py).

Writes mod/src/main/resources/assets/mimcontent/textures/item/lionfish_bucket.png (the PICK, byte-identical on
rerun), the review sheet art/candidates/lionfish_bucket/sheet.png and hotbar previews in the same folder.
Run:    art/.venv/bin/python art/src/fish_lionfish_bucket.py
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
from fish_bucket_rim import RIM, check_rim, _dark as rim_dark  # noqa: E402
from fish_lionfish_icon import PAL as ICON  # noqa: E402
from font import label_font  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "art")
TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT = os.path.join(TEXTURES, "item", "lionfish_bucket.png")
OUT_DIR = os.path.join(ART, "candidates", "lionfish_bucket")
VANILLA = os.path.join(ART, ".vanilla", "item")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


PAL = dict(ICON)
PAL.update({
    "~": hx("#2a55c4"),   # the shared water shades
    "v": hx("#1d3c96"),   # shadow on the water where the fish goes under
    "^": hx("#6a92ea"),   # a glint
    "#": RIM,
})
EMPTY = ["................"] * 10

# rows 0-5, columns 0-15; "." is clear (vanilla cod_bucket's own outline or water shows there)
CANDIDATES = {
    # A: the head at the left of the mouth, rising up and left; eye at 5,2 in pale skin; the tentacle over it (4,0 R,
    # its pale root 4,1 s, so nothing dark touches the eye); three spines (7, 9, 11) with cream tips standing behind the head; the bands d/D cross the head and back
    # in rows 1 and 3, pale w in the eye's row; the fan's tip (d, R) breaks the water at 6-7,4. After critic round 1
    # (PASS): the tentacle got a pale tip (5,0), and the fan's pink tip and the dark water shadow under the eye (5-6,4),
    # which read as a mouth, became plain water and a dark ray.
    "A": [
        "....Rs.s.s.s....",
        "...psppS.S.S....",
        "..pPPEPWwwPw....",
        ".qPPPWPdDPdD....",
        ".Wqqq~dR~~~~~...",
        "...^~~~~~~~~....",
    ] + EMPTY,
    # B: the head a row higher, the eye at 5,1, the spines taller (rows 0-1 above the back at row 2), the back's bands
    # in rows 2-3, the chin dipping into the water at row 4.
    "B": [
        "...Rs....s.s.s..",
        "..pPPEPWwS.S.S..",
        "..qPPWPdDPdDd...",
        ".qPPqWdDPdDP....",
        ".WqqvrRv~~~~~...",
        "...^~~~~~~~~....",
    ] + EMPTY,
    # C: A with a bigger fan breaking the water: two banded rays (6-8,4 and 7-9,5) beside the chin.
    "C": [
        "....R..s.s.s....",
        "...psppS.S.S....",
        "..pPPEPWwwPw....",
        ".qPPPWPdDPdD....",
        ".WqqqrRrR~~~~...",
        "...^~rRrR~~~....",
    ] + EMPTY,
    # A2, round 2: three blind readers saw A as a pale fish with its jaws open and teeth showing (the cream spine tips
    # over the pale row behind the eye read as teeth over an open mouth). So the spines (8, 10, 12) now stand on a dark
    # back line (row 2, x 8-11) with red-brown bases and only their tips cream, the eye moves a pixel forward (4,2) to
    # keep the dark back 4 px away, a red-brown band crosses the back behind the head (row 3), and the head is the
    # icon's pinkish band and fin tones (w, r) round a few light P, so it no longer reads as a pale open jaw.
    "A2": [
        "....R...s.s.s...",
        "...wsPwpS.S.S...",
        "..rpEPwpdDdd....",
        ".rPPwrdDPdDd....",
        ".prrw~dR~~~~~...",
        "...^~~~~~~~~....",
    ] + EMPTY,
    # A3, round 3: critic round 2 still saw teeth over a dark open mouth in A2 (the even cream spine tips over the solid
    # dark back, a cream pixel inside it). The back is now banded (red-brown R and dark d alternating), the cream pixel
    # in it is gone, only the front spine keeps a cream tip (the others a pink one), and the head is mid pink (w) with a
    # red-brown band behind the eye (6,1 and 6,3, nothing touching the eye).
    "A3": [
        "....R...s.w.w...",
        "...wswRpS.S.S...",
        "..rpEwwpdRdR....",
        ".rwwwrRDDRdR....",
        ".prrw~dR~~~~~...",
        "...^~~~~~~~~....",
    ] + EMPTY,
}
PICK = "A3"   # critic round 3: PASS; then its first polish point: the cream snout pixel (2,3), a hint of a lip, is pink


def build(grid):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        assert len(row) == 16, (y, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                img.putpixel((x, y), PAL[ch] + (255,))
    return img


def composite(layer):
    base = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    base.alpha_composite(layer)
    return base


def check_eye(name, grid):
    """One eye; nothing dark in its 3 x 3 or within 3 px in its row."""
    dark = set("EdDSRv#")
    eyes = [(x, y) for y, r in enumerate(grid) for x, c in enumerate(r) if c == "E"]
    assert len(eyes) == 1, (name, eyes)
    ex, ey = eyes[0]
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if not (dx or dy) or not (0 <= ey + dy < len(grid)):
                continue
            c = grid[ey + dy][ex + dx]
            if c in dark:
                print(f"note: {name}: dark {c} beside the eye at {ex + dx},{ey + dy}")
    for x, c in enumerate(grid[ey]):
        assert not (c in dark and c != "E" and abs(x - ex) <= 3), f"{name}: dark {c} in the eye's row at {x},{ey}"


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
    for n in ("cod_bucket", "salmon_bucket", "tropical_fish_bucket", "pufferfish_bucket", "axolotl_bucket",
              "tadpole_bucket", "water_bucket", "bucket"):
        p = os.path.join(VANILLA, n + ".png")
        if os.path.exists(p):
            v = Image.open(p).convert("RGBA")
            same += [(n, x, y) for y in range(16) for x in range(16)
                     if layer.getpixel((x, y))[3] and layer.getpixel((x, y)) == v.getpixel((x, y))]
    assert not same, f"pixels identical to vanilla: {same}"
    return len(fishy)


def fish_over(layer):
    """The back-rim outline pixels the fish covers (fish colours, not water, not dark)."""
    from fish_bucket_rim import OUTLINE, WATER
    return [p for p in OUTLINE if layer.getpixel(p)[3] and layer.getpixel(p)[:3] not in WATER
            and not rim_dark(layer.getpixel(p))]


def hotbars(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    outs = []
    for name, items in (("hotbar", ["mc:cod_bucket", "bucket:lionfish_bucket", "bucket:skorfna_bucket",
                                    "mc:pufferfish_bucket", "bucket:pixxi_san_pietru_bucket", "mc:salmon_bucket",
                                    "bucket:cerna_bucket", "mod:lionfish", "mc:tropical_fish_bucket"]),
                        ("hotbar_candidates", ["mc:cod_bucket"] + ["file:" + paths[n] for n in CANDIDATES]
                         + ["bucket:skorfna_bucket", "bucket:pixxi_san_pietru_bucket", "mc:salmon_bucket"])):
        for suffix, scale in (("", "2"), ("_x4", "4")):
            out = os.path.join(OUT_DIR, name + suffix + ".png")
            subprocess.run([py, tool, out] + items + ["--scale", scale], check=True, capture_output=True)
            outs.append(out)
    return outs


def sheet(comps, hb):
    bg, ink = (52, 52, 56), (235, 235, 235)
    items = [(("> " if n == PICK else "") + "candidate " + n, im) for n, im in comps.items()]
    for n in ("skorfna_bucket", "pixxi_san_pietru_bucket"):
        items.append((n, composite(Image.open(os.path.join(TEXTURES, "item", n + ".png")).convert("RGBA"))))
    items.append(("vanilla cod_bucket", Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")))
    W = 6 * 220 + 20
    grid = Image.new("RGB", (W, 200), bg)
    d = ImageDraw.Draw(grid)
    for i, (name, im) in enumerate(items):
        x0 = 10 + i * 220
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        grid.paste(tile.convert("RGB"), (x0, 24))
        for j, s in enumerate((1, 2)):
            t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), (139, 139, 139, 255))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            grid.paste(t.convert("RGB"), (x0 + 136, 24 + j * 30))
        d.text((x0, 4), name, fill=ink, font=label_font(13))
    hbs = [Image.open(p).convert("RGB") for p in hb]
    out = Image.new("RGB", (max(W, max(h.width for h in hbs) + 20), 200 + sum(h.height + 10 for h in hbs) + 40), bg)
    out.paste(grid, (0, 30))
    ImageDraw.Draw(out).text((10, 6), "Lionfish bucket (layer over vanilla cod_bucket, 8x, 1x, 2x); hotbars: cod bucket, "
                             "LIONFISH, skorfna, pufferfish, pixxi San Pietru, salmon, cerna buckets, the lionfish item, "
                             "tropical fish bucket; then cod bucket, candidates, skorfna, pixxi, salmon buckets",
                             fill=ink, font=label_font(14))
    y = 236
    for h in hbs:
        out.paste(h, (10, y))
        y += h.height + 10
    out.save(os.path.join(OUT_DIR, "sheet.png"))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    comps, paths = {}, {}
    for name, grid in CANDIDATES.items():
        check_eye(name, grid)
        layer = build(grid)
        check_cover(layer)
        print(name, end=": ")
        check_rim(layer, os.path.join(VANILLA, "cod_bucket.png"), fish_over(layer))
        comps[name] = composite(layer)
        paths[name] = os.path.join(OUT_DIR, "composite_%s.png" % name)
        comps[name].save(paths[name])
        if name == PICK:
            layer.save(OUT)
    sheet(comps, hotbars(paths))
    print("wrote", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
