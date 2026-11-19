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

REDO 3 2026-11-19 (owner: "All pass except john dory bucket. That needs a redo, consider very different possible
version"): six very different concepts instead of another tweak of the layout above, all kept selectable in GRIDS
(U upright, S sail, F one-fin sail, T tilted tall oval, L lying on the water, D wide disc), refined by critic rounds
(at most 3, owner 2026-11-19) and blind reads; PICK is installed and the sheet shows every concept for the owner.

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
PICK = "L"      # the redo-3 concept installed (see REDO3 below); the owner chooses among them on the sheet
CHOSEN = PICK


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
PAL_C.update({k: ICONS["C"][k] for k in "lwPs"})              # redo 3: the icon's pale belly, pelvic fin, spot edge

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

# Redo 3 (owner, 2026-11-19: "All pass except john dory bucket. That needs a redo, consider very different possible
# version"). Six very different concepts, not another tweak of A. Keys as above, all the accepted icon C's colours;
# W (the icon's dark shade) also serves as the fin membrane between the near-black spines f.
REDO3 = {
    # U upright: standing on its tail, head up, the spines streaming down its left side. Critic round 1: FAIL ("a
    # duck or bird head poking up"), dropped; kept for the owner to see.
    "U": [
        "....ooom........",
        "...oHGGmo.......",
        "..ofEGGOOo#.....",
        ".nfWGGOOOlo#....",
        "n.fWGObSSlwo~...",
        ".nfWOObSSlwwP...",
    ],
    # S sail: only the spiny dorsal fin and the top of the back break the water, the eye just above it at the left.
    # Round 1: weak PASS (eye raised, the spine lattice thinned after it). Round 2: FAIL ("a tan cap or wedge", no
    # head mass), dropped.
    "S": [
        ".....n..n.......",
        "....fWWfWWn.....",
        "...fWWWWWWWW....",
        "..oEXGOObbbbo...",
        ".oHGOObbv~~~~...",
        "..oOb~vvvv~~~...",
    ],
    # F one-fin sail: one big front spine and its fin, the head at the left. Round 1: FAIL ("a shark fin or a
    # duckling"), dropped; kept for the owner to see.
    "F": [
        "......f.........",
        "....ofWfn.......",
        "...ofWWWfn#.....",
        "..oHXGGOOOo#....",
        ".oHEGOObbv~~~...",
        "..oob~vvvv~~~...",
    ],
    # T tilted tall oval: the whole deep body side on, head up and to the right, half out of the water, the
    # thumbprint in the middle, the filaments trailing along the top. Round 1: PASS (filaments moved off the left
    # end, where they read as a tail). Round 2: borderline FAIL (the dark top band a lid, the head too small); the
    # band broken with two lit pixels and a dark lower jaw put under the eye. Round 3: FAIL ("a lumpy, crumpled
    # pile"); its last fix applied (the dark top middle lit), kept for the owner to see.
    "T": [
        ".......n.n......",
        "....fWfGGGGo....",
        "...ofWWoHGGo....",
        "...oHGGOOGGXEo..",
        "...oGOSSOObbomo.",
        "...oObSSbbWWWo..",
    ],
    # L lying on the water, seen from above: the round side up, head left, the spines fanned along the top edge and
    # sweeping back, the thumbprint below the middle, the rim showing at the right of row 2. Round 1: PASS, the best.
    # Round 2: PASS, best pick; the thumbprint rounded with its mid-dark edge s (kept out of the eye's row, owner
    # lesson) and the mouth line angled up at (2,5). Round 3: PASS, best of three; the lit nose pixel (2,3)
    # toned down so nothing glows in front of the eye.
    "L": [
        "......n.n.n.....",
        "...fWfWfWfn.....",
        "..oHGGGGOOo#....",
        ".oGXEGOOOObbbo..",
        ".omGGOOSSsbbbo..",
        "..moOOsSSbWWo...",
    ],
    # D wide disc: the top of a big deep disc lying across the whole bucket. Round 1: FAIL ("a burger bun or a lid",
    # the pale jaw a beak); the jaw removed and the right end rounded after it. Round 2: FAIL (a broader twin of L,
    # "flat and fat"); the front edge darkened and the rim shown at the right of row 2. Round 3: weak PASS ("a
    # round loaf", no mouth); a dark mouth added at (2,4) and the nose toned down.
    "D": [
        ".....n.n.n......",
        "....ofWfWfo.....",
        "..ooHGGGGOOb##..",
        ".oGGXEGGOOObbbo.",
        ".omGGOOOSSObbbo.",
        ".oOOObbbSSbbWWo.",
    ],
}
REDO3_NAMES = {"U": "upright", "S": "sail", "F": "one-fin sail", "T": "tilted tall oval", "L": "lying on the water",
               "D": "wide disc"}
GRIDS.update(REDO3)
PALS.update({k: PAL_C for k in REDO3})


def fish_over_rim(grid):
    """The rim outline pixels the fish sits in front of: those our layer paints with a fish colour, not a dark grey."""
    def dark(c):
        return max(c) < 0x40 and max(c) - min(c) < 6
    return [(x, y) for (x, y) in OUTLINE if y < len(grid) and grid[y][x] not in ".~v^#" and not dark(PAL_C[grid[y][x]])]


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
    """Every redo-3 concept at 8x, 2x and 1x over vanilla's cod bucket beside the accepted icon and the rejected redo-2
    bucket, the rim check of the pick, and the offline hotbar."""
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    font, small = label_font(16), label_font(13)
    W = 1500
    bg, ink = (52, 52, 56), (235, 235, 235)
    SLOT = (139, 139, 139, 255)
    parts = [("The accepted model, side on in game (spine close-up, and in the tank)", model_band(W, bg))]
    icon = Image.open(os.path.join(ITEMS, "pixxi_san_pietru.png")).convert("RGBA")
    cells = [(f"{v} {REDO3_NAMES[v]}" + (" (PICK)" if v == PICK else ""), composite(layers[v])) for v in REDO3]
    cells += [("redo 2 A (rejected)", composite(layers["A"])), ("the accepted icon", icon)]
    per_row = 4
    rows = (len(cells) + per_row - 1) // per_row
    band = Image.new("RGB", (W, rows * 200 + 10), bg)
    d = ImageDraw.Draw(band)
    for i, (label, im) in enumerate(cells):
        x, y = 10 + (i % per_row) * 360, 6 + (i // per_row) * 200
        d.text((x, y), label, fill=ink, font=small)
        t = Image.new("RGBA", (136, 136), SLOT)
        t.alpha_composite(im.resize((128, 128), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x, y + 20))
        for k, s in enumerate((2, 1)):
            t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), SLOT)
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x + 150 + k * 50, y + 20))
        if label.endswith("(PICK)"):
            rim = composite(layers[PICK]).resize((128, 128), Image.NEAREST)
            dr = ImageDraw.Draw(rim)
            for (px, py) in OUTLINE:
                col = (40, 80, 255) if (px, py) in FISH_OVER_RIM[PICK] else (230, 30, 30)
                dr.rectangle((px * 8, py * 8, px * 8 + 7, py * 8 + 7), outline=col)
            t = Image.new("RGBA", (136, 136), SLOT)
            t.alpha_composite(rim, (4, 4))
            band.paste(t.convert("RGB"), (x + 150, y + 64 if False else y + 60))
    parts.append(("Redo 3: every concept at 8x, 2x and 1x over vanilla cod_bucket (the pick also with its rim check: "
                  "red dark, blue fish), the rejected redo 2 and the accepted icon", band))
    files = []
    for v in REDO3:
        files.append("file:" + os.path.join(CAND, f"bucket_{v}.png"))
    hb = [hotbar(os.path.join(CAND, "hotbar.png"), ["mc:cod_bucket"] + files + ["mod:pixxi_san_pietru",
                                                                             "bucket:skorfna_bucket"], 2),
          hotbar(os.path.join(CAND, "hotbar_pick.png"), ["mc:water_bucket", "mc:cod_bucket",
                                                         "file:" + os.path.join(CAND, f"bucket_{PICK}.png"),
                                                         "mod:pixxi_san_pietru", "bucket:cerna_bucket",
                                                         "bucket:lingwata_bucket", "mc:salmon_bucket",
                                                         "mc:pufferfish_bucket", "mc:tropical_fish_bucket"], 2),
          hotbar(os.path.join(CAND, "hotbar_x4.png"), ["mc:cod_bucket"] + files[:4], 4),
          hotbar(os.path.join(CAND, "hotbar_x4b.png"), files[4:] + ["mod:pixxi_san_pietru", "mc:salmon_bucket"], 4)]
    band = Image.new("RGB", (W, sum(i.height + 10 for i in hb) + 10), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    parts.append(("Hotbar preview, unselected: cod bucket, concepts " + ", ".join(REDO3) + ", the icon, skorfna bucket "
                  "(scale 2); water, cod, the PICK, its icon, cerna and lingwata buckets, salmon, pufferfish, tropical "
                  "fish (scale 2); the concepts at scale 4", band))
    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Bucket of pixxi San Pietru (John Dory), redo 3: very different versions for the owner to choose "
                    "from (textures/item/pixxi_san_pietru_bucket.png)", fill=ink, font=label_font(20))
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
