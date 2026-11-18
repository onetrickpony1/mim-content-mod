"""Item icon for the marzpan (Mediterranean parrotfish, Sparisoma cretense, the red female): the caught fish.

What makes it a marzpan (photos in art/references/fish_marzpan_refonly/, list.tsv; the market photo shows its colours
out of water):
- a deep, oblong body with a blunt, rounded head (not the cerna's big jaw, not the awrata's steep bream forehead);
- scarlet red, darker along the back and paling to pink toward the belly;
- a grey-lilac patch on the cheek with the eye at its front, a gold ring round the eye (open toward the snout), and a
  yellow stripe along the lower edge of the patch;
- the short beak-like mouth: a dark corner at the tip of the snout;
- a yellow saddle on top of the tail stalk, then a square-cut red tail;
- a long low dorsal fin along the back.

Colours: the accepted 3D model's palette (art/src/fish_marzpan_model.py PAL). The brief asks for the model's colours
lifted about x1.2 for out of water, but the model's reds already sit at full red (255), so a lift only washes them pale;
the icon keeps the model's colours as they are and adds two darker red-browns for the outline, as vanilla's fish do.
Pose and light follow vanilla's fish items: head lower left, tail upper right, light from the top left.

Candidates: A, B (no cheek stripe, a plainer head), C (A with a pectoral fin on the flank, reworked after review;
installed).
Run:  art/.venv/bin/python art/src/fish_marzpan_icon.py [--sheet]
Writes mod/.../textures/item/marzpan.png (byte-identical on rerun); with --sheet also the review sheet
art/candidates/fish_marzpan_icon.png and the candidates as art/candidates/marzpan_icon_<X>.png.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(ART, ".."))
TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "marzpan.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_marzpan_icon.png")
VANILLA = os.path.join(ART, ".vanilla", "item")
REFS = os.path.join(ART, "references", "fish_marzpan_refonly")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # the body, palest (belly) to darkest (back): the model's reds
    "0": hx("#ffa890"), "1": hx("#ff9470"), "2": hx("#ff7048"), "3": hx("#f45a38"), "4": hx("#dc4630"),
    "5": hx("#bc3828"),
    "k": hx("#a83224"),                       # the outline on the lit back and forehead
    "o": hx("#7a2219"),                       # the outline on the shaded belly side
    "M": hx("#5e1a14"),                       # the corner of the beak-like mouth (dark red-brown, not black)
    "H": hx("#d8c4d0"), "G": hx("#bca4b6"), "g": hx("#9c8498"),   # the grey-lilac cheek patch: lit, mid, gill edge
    "E": hx("#0a0a0a"),                       # the eye: the only black
    "O": hx("#ff9a2c"),                       # the gold ring round the eye
    "Y": hx("#fff05a"), "y": hx("#f2d23c"),   # the yellow cheek stripe and the saddle on the tail stalk
    "w": hx("#d8a82c"),                       # the cheek stripe where it turns under, in shade
    "D": hx("#a02c20"), "f": hx("#ec6446"),   # the long low dorsal fin: dark rays, lit membrane
    "P": hx("#ff7a50"), "p": hx("#e05a3a"),   # the pectoral fin (candidate C)
    "T": hx("#ff7a56"), "t": hx("#f0603e"), "u": hx("#cc4632"),   # the square-cut tail: lit, mid, trailing rim
}

# Head lower left, tail upper right. The head is blunt: its front is a short column (x 1, rows 9-12) under a lit
# forehead rim (k). The eye (2,10) sits at the front of the grey patch with the gold ring above, behind and below it
# (open toward the snout, which stays red in front of it). The yellow stripe runs under the patch (row 12) to the
# mouth corner (M, 1,12). The body shades from a dark back (5, 4) to a pale belly (1, 0) with a dark red-brown belly
# outline (o); the long dorsal (D) runs along the back from 2,8 to 8,4; the yellow saddle (Y, y) sits on the stalk
# just before the square-cut tail fan (T, t, with a trailing rim u).
A = [
    "................",
    "...........Ttu..",
    "..........TTTtu.",
    "..........yTttu.",
    ".......Df.Yytu..",
    ".....Df4223yo...",
    "....D4223314o...",
    "...f42233114o...",
    "..D422333114o...",
    ".kOGG233114o....",
    ".4EOGg33114o....",
    ".4OGGg3114o.....",
    ".MYYYY114o......",
    "..ooooooo.......",
    "................",
    "................",
]
# B: a plainer head: no yellow cheek stripe (the lower cheek is red), the patch a little larger
B = [r for r in A]
B[12] = ".M4GGg114o......"
# C: A with a small pectoral fin on the flank behind the gill cover; after the first review (critic round 1): lit from
# the top left (a light run just inside the back, the belly side in shade), a 2 px blunt snout with the mouth corner
# at its foot (1,11), the gold ring only behind the eye (3,10), the cheek stripe shaded toward the underside, the chin
# and the belly stepped round, the tail's trailing edge squared off at the top.
C = [
    "................",
    "...........Ttuu.",
    "..........TTTtu.",
    "..........yTttu.",
    ".......Df.Yytu..",
    ".....Df4223yo...",
    "....D4123334o...",
    "...f41233334o...",
    "..D412333334o...",
    "..kGG233334o....",
    ".4EOGgP3334o....",
    ".MgGGgpP34o.....",
    "..oyyw44oo......",
    "...ooooo........",
    "................",
    "................",
]
CANDIDATES = {"A": A, "B": B, "C": C}
CHOSEN = "C"


def render(rows, pal=PAL):
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), pal[ch] + (255,))
    return im


def check(rows):
    """Warn about stray pixels (no opaque 4-neighbour); fail if any pixel copies vanilla's cod at the same place."""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != "." and not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and rows[y + dy][x + dx] != "."
                                     for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                print(f"warning: stray pixel at {x},{y}")
    im = render(rows)
    for n in ("cod", "salmon", "tropical_fish", "pufferfish"):
        p = os.path.join(VANILLA, n + ".png")
        if os.path.exists(p):
            v = Image.open(p).convert("RGBA")
            same = [(x, y) for y in range(16) for x in range(16)
                    if im.getpixel((x, y))[3] and im.getpixel((x, y)) == v.getpixel((x, y))]
            assert not same, f"pixels identical to vanilla {n}: {same}"


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})
            lines.append(f"{os.path.basename(d['file']):<22} cover {d['coverage']:.2f}  colours {d['colours']:>2}  "
                         f"dark {d['lmin']:.2f}  light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  "
                         f"inside {d['interior_l']:.2f}  TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def sheet():
    sys.path.insert(0, os.path.join(ART, "tools"))
    from font import label_font
    font, small = label_font(16), label_font(13)
    W = 1500
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []
    refs = []
    for name in ("market_1.jpg", "side_2.jpg", "big_red.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            refs.append(im.resize((300, round(300 * im.height / im.width)), Image.LANCZOS))
    if refs:
        band = Image.new("RGB", (W, max(i.height for i in refs) + 10), bg)
        for i, im in enumerate(refs):
            band.paste(im, (10 + i * 310, 5))
        parts.append(("References (reference only)", band))
    cand_paths = []
    for k, rows in CANDIDATES.items():
        p = os.path.join(ART, "candidates", f"marzpan_icon_{k}.png")
        render(rows).save(p)
        cand_paths.append((f"candidate {k}" + (" (installed)" if k == CHOSEN else ""), p))
    items = [("vanilla cod", os.path.join(VANILLA, "cod.png")), ("vanilla salmon", os.path.join(VANILLA, "salmon.png")),
             ("vanilla tropical fish", os.path.join(VANILLA, "tropical_fish.png")),
             ("cerna", os.path.join(TEXTURES, "item", "cerna.png")),
             ("awrata", os.path.join(TEXTURES, "item", "awrata.png"))] + cand_paths
    band = Image.new("RGB", (W, 128 + 100), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = Image.open(p).convert("RGBA")
        x0 = 10 + i * 176
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(tile.convert("RGB"), (x0, 22))
        d.text((x0, 2), name, fill=ink, font=small)
        for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
            t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x0 + (0, 26, 70, 96)[j], 154))
    parts.append(("8x, then 1x and 2x on light and dark grey", band))
    lines = measure([p for _, p in items])
    lines.append("STYLE.md food ranges: cover 0.29-0.77, colours 6-20, dark 0.0-0.35, light 0.32-0.99, TL-BR +0.01-+0.17")
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py", band))
    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Marzpan (parrotfish) item icon, textures/item/marzpan.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)
    print("sheet:", OUT_SHEET)


def main():
    for rows in CANDIDATES.values():
        check(rows)
    render(CANDIDATES[CHOSEN]).save(OUT_ICON, optimize=False)
    print("wrote", os.path.relpath(OUT_ICON, ROOT))
    if "--sheet" in sys.argv[1:]:
        sheet()


if __name__ == "__main__":
    main()
