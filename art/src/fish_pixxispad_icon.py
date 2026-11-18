"""Item icon for the pixxispad (swordfish, Xiphias gladius): the caught fish, like vanilla cod and salmon.

What makes it a pixxispad (photos in art/references/fish_pixxispad_refonly/, list.tsv; colour from the fish out of
water, on deck and at market: sw09, sw01, sw02):
- a long, sleek torpedo body, slimmer than the tonn, deepest just behind the head and tapering to a thin tail stalk;
- the sword: a long, flat, pointed bill about a third of the fish's length, pale bronze-grey, lit on top and shaded
  underneath, running down the diagonal to the lower-left corner and set apart from the head by a short lower jaw and
  a dark mouth line under its base;
- a dark bronze to purplish-black back fading to silvery-brown sides and a pale belly (no scales, no stripes);
- a tall, rigid, sickle-shaped first dorsal fin standing up just behind the head;
- a large eye;
- a deeply forked crescent tail, both lobes long and thin, with a keel (a dark ridge) on the stalk;
- a long, low, sickle pectoral fin under the gill; no pelvic fins.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left. The dark back faces the light, so its upper edge carries a warm bronze sheen
(the gloss seen on fresh fish) and the pale belly takes the shade on its lower right, as the tonn icon does. The
tonn's back is navy and its sides cold silver; the pixxispad's back is purple-bronze and its sides warm silver-brown,
so the two never share a colour.

Run:  art/.venv/bin/python art/src/fish_pixxispad_icon.py
Writes mod/.../textures/item/pixxispad.png (byte-identical on rerun), art/candidates/fish_pixxispad_icon.png (compare
sheet) and the offline hotbar previews art/candidates/fish_pixxispad_icon_hotbar.png and _hotbar_x4.png.
"""
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
OUT_ICON = os.path.join(TEXTURES, "item", "pixxispad.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_pixxispad_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_pixxispad_refonly")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # sword: pale bronze-grey (lit top), darker toward the tip, shaded underside at its base (the mouth line)
    "S": hx("#c4b4a4"), "s": hx("#9a8a80"), "u": hx("#6e5c5c"),
    # back, lit top left: purple-bronze rim and sheen (round 2: not tan), then the purple back
    "H": hx("#8a7072"), "h": hx("#7a6266"), "1": hx("#664c5c"), "2": hx("#4a3442"),
    # sides and belly: bronze-silver, silver, pale, then shaded toward the lower right
    "3": hx("#8c7876"), "4": hx("#a69896"), "5": hx("#ccc2ba"), "g": hx("#7a6e72"), "G": hx("#54484f"),
    "o": hx("#24161e"),                       # shaded rim (belly side, under the jaw)
    "e": hx("#0a080c"),                       # the eye
    "j": hx("#7a6670"),                       # short pointed lower jaw
    "p": hx("#5a4450"),                       # long low pectoral fin
    "D": hx("#8a7480"), "d": hx("#5a4450"),   # dorsal fin: lit leading edge, membrane (lifted for the dark slot)
    "T": hx("#8a7480"), "t": hx("#5e4654"),   # tail: lit, dark
    "k": hx("#1c1218"),                       # keel on the tail stalk
}

PAL_ROUND1 = {
    # round 1 (critic: FIX), kept only for the compare sheet
    # sword: pale bronze-grey (lit top), darker toward the tip, shaded underside at its base (the mouth line)
    "S": hx("#c4b4a4"), "s": hx("#9a8a80"), "u": hx("#6e5c5c"),
    # back, lit top left: bronze rim and sheen, then the purple back
    "H": hx("#ac8e78"), "h": hx("#8a6e5c"), "1": hx("#664c5c"), "2": hx("#4a3442"),
    # sides and belly: bronze-silver, silver, pale, then shaded toward the lower right
    "3": hx("#8c7876"), "4": hx("#a69896"), "5": hx("#ccc2ba"), "g": hx("#7a6e72"), "G": hx("#54484f"),
    "o": hx("#24161e"),                       # shaded rim (belly side, under the jaw)
    "e": hx("#0a080c"),                       # the eye
    "j": hx("#7a6670"),                       # short pointed lower jaw
    "p": hx("#5a4450"),                       # long low pectoral fin
    "D": hx("#745e6a"), "d": hx("#44323e"),   # dorsal fin: lit leading edge, dark membrane
    "T": hx("#745e6a"), "t": hx("#3a2a34"),   # tail: lit, dark
    "k": hx("#1c1218"),                       # keel on the tail stalk
}

# Head lower left, tail upper right. The sword runs one pixel wide down the diagonal from the upper jaw (4,11) to the
# lower-left corner (0,15), pale on the lit top; its base is two wide (the shaded underside u at 4,12, which is also
# the mouth line) above the short lower jaw (5,12), so the bill stays apart from the head. The body is a slim torpedo,
# 5-7 pixels across its rows (the tonn is 7-8), deepest behind the eye and tapering to a 2-pixel stalk at 11-12,3;
# back and belly edges step by 1-3 pixels. Bands from the lit back to the shaded belly: bronze rim h, a bronze sheen
# line H (9,5 to 6,8), a purple back 1 and 2 two pixels wide (so the back reads dark, as on the fresh fish), then
# bronze-silver 3, silver 4, pale 5 on the belly behind the head, shade g and G, dark rim o. Large eye at 5,10 inside
# the lit forehead, the only dark pixel on the head. Round 2 (critic): the tall sickle dorsal moved forward
# over the shoulder, 6-7,3-6 (lit leading edge D rising to its tip at 7,3, concave trailing edge with a gap behind
# it at 8-9,4), well apart from the tail so the pair no longer reads as arrow fletching;, a crescent tail (upper lobe up to 13,0, lower lobe right to 15,2,
# a deep fork between) on a dark keeled stalk (k), and the long low pectoral as a sickle under the belly
# (9,11, 7-8,12, tip 9,13). Fins lifted a step so they hold on the dark slot.
PIXXISPAD = [
    ".............T..",
    "............T...",
    "............t..t",
    ".......D...hktt.",
    "......Dd..h1G...",
    "......DdhH12o...",
    "......dhH123o...",
    "......hH123o....",
    ".....hH1235o....",
    ".....h12354o....",
    "....he354go.....",
    "....S45Gop......",
    "...SujGpp.......",
    "..S......p......",
    ".s..............",
    "s...............",
]

# Round 1, kept only for the compare sheet: a straight tube with the dorsal beside the tail (read as arrow fletching).
PIXXISPAD_ROUND1 = [
    ".............T..",
    ".........D..T...",
    "........Dd..t..t",
    "........Dd.hktt.",
    ".........dh1G...",
    "........hH12o...",
    ".......hH123o...",
    "......hH123o....",
    ".....hH1235o....",
    ".....h12354o....",
    "....he354go.....",
    "....S45Gop......",
    "...SujG.........",
    "..S.............",
    ".s..............",
    "s...............",
]


def render(rows, pal=None):
    pal = pal or PAL
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), pal[ch] + (255,))
    return im


def check(rows):
    """Warn about stray pixels (no opaque 8-neighbour)."""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and rows[y + dy][x + dx] != "."
                       for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy):
                print(f"warning: stray pixel at {x},{y}")


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<18} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def build(rows):
    """Rows and the tallest column of body pixels across the fish's axis (anti-diagonal x+y), fins excluded."""
    fins = set("DdTtp")
    body = [(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c not in fins and c not in ".Ssu"]
    by_a = {}
    for x, y in body:
        by_a.setdefault(x - y, []).append(x + y)
    depth = max(max(v) - min(v) + 1 for v in by_a.values())
    widths = [sum(1 for c in r if c not in fins and c not in ".Ssu") for r in rows]
    return depth, max(widths)


# Colour from photos of the fish out of water (deck, market): (box, note)
SAMPLES = {
    "sw09_2.jpg": ((560, 150, 760, 300), "on deck, fresh"),
    "sw01_market.jpg": ((480, 60, 640, 190), "market stall, head and back"),
    "sw02_essaouira.jpg": ((420, 330, 640, 410), "landed, Essaouira (wet)"),
}


def sample_photos():
    import numpy as np
    out = {}
    for name, (box, note) in SAMPLES.items():
        p = os.path.join(REFS, name)
        if not os.path.exists(p):
            continue
        a = np.array(Image.open(p).convert("RGB").crop(box)).reshape(-1, 3).astype(float)
        lum = a @ [0.2126, 0.7152, 0.0722]
        q = np.percentile(lum, [5, 35, 65, 95])
        cols = [tuple(int(v) for v in np.median(a[(lum >= lo) & (lum <= hi)], 0))
                for lo, hi in ((q[0], q[1]), (q[1], q[2]), (q[2], q[3]))]
        out[name] = (cols, note)
    return out


def tiles(band, im, x0, y0):
    """The icon at 8x, then 1x and 2x on light and dark grey."""
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, y0))
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
        t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + 136 + (j % 2) * 44, y0 + (j // 2) * 46))


ACCEPTED = ("lampuka", "tonn", "sardina", "cerna", "awrata", "murina")


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 1980
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    # references
    refs = []
    for name in ("sw09_2.jpg", "sw01_market.jpg", "sw02_essaouira.jpg", "sw12_g2.jpg", "sw05_stuffed.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((380, round(380 * im.height / im.width)), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = max(im.height for _, im in refs) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im, (10 + i * 392, 22))
            d.text((10 + i * 392, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References (art/references/fish_pixxispad_refonly, list.tsv); colour from the fish out of water",
                      band))

    # colour: photo samples beside the palette
    samples = sample_photos()
    band = Image.new("RGB", (W, 34 * (len(samples) + 1) + 10), bg)
    d = ImageDraw.Draw(band)
    y = 6
    for name, (rgbs, note) in list(samples.items()) + [
            ("PALETTE", ([PAL[c] for c in "hH12345gGo"] + [PAL[c] for c in "SsDt"], "body ramp hH12345gGo, then sword S s, fins D t"))]:
        d.text((10, y + 8), name, fill=ink, font=small)
        for j, rgb in enumerate(rgbs):
            d.rectangle((200 + j * 74, y, 200 + j * 74 + 70, y + 28), fill=rgb)
            d.text((200 + j * 74 + 2, y + 16), "#%02x%02x%02x" % rgb,
                   fill=(255, 255, 255) if sum(rgb) < 380 else (0, 0, 0), font=label_font(11))
        d.text((200 + 14 * 74 + 10, y + 8), note, fill=ink, font=small)
        y += 34
    parts.append(("Colour: photo samples (dark, mid, light) beside the palette", band))

    # 8x and 1x beside vanilla and the accepted fish
    items = [("vanilla cod", os.path.join(VANILLA, "cod.png")), ("vanilla salmon", os.path.join(VANILLA, "salmon.png"))]
    items += [(f"{n} (accepted)", os.path.join(TEXTURES, "item", f"{n}.png")) for n in ACCEPTED]
    items.append(("PIXXISPAD", None))
    per_row = 8
    rows_n = (len(items) + per_row - 1) // per_row
    band = Image.new("RGB", (W, rows_n * 170 + 24), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = icon if p is None else Image.open(p).convert("RGBA")
        x0, y0 = 10 + (i % per_row) * 244, 22 + (i // per_row) * 170
        tiles(band, im, x0, y0)
        d.text((x0, y0 - 20), name, fill=ink, font=small)
    d.text((10, rows_n * 170), "8x, then 1x and 2x on light and dark grey", fill=ink, font=small)
    parts.append(("The icon at 8x and 1x beside vanilla cod and salmon and the accepted fish", band))

    # round 2 beside round 1 (critic: FIX), at 8x, then 1x and 2x on light and dark grey
    band = Image.new("RGB", (W, 128 + 40), bg)
    d = ImageDraw.Draw(band)
    for i, (name, im) in enumerate((("ROUND 2 (dorsal forward, pectoral sickle, purple back, lighter fins)", icon),
                                    ("round 1 (critic: FIX, read as a quill)", render(PIXXISPAD_ROUND1, PAL_ROUND1)))):
        x0 = 10 + i * 490
        tiles(band, im, x0, 22)
        d.text((x0, 2), name, fill=ink, font=small)
    parts.append(("New beside round 1 (8x, then 1x and 2x)", band))

    # lookalikes: things a thin dark diagonal with a pale shaft could be mistaken for
    looks = [("vanilla arrow", os.path.join(VANILLA, "arrow.png")), ("vanilla feather", os.path.join(VANILLA, "feather.png")),
             ("PIXXISPAD round 2", None), ("round 1", "R1")]
    band = Image.new("RGB", (W, 128 + 40), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(looks):
        im = icon if p is None else render(PIXXISPAD_ROUND1, PAL_ROUND1) if p == "R1" else Image.open(p).convert("RGBA")
        x0 = 10 + i * 244
        tiles(band, im, x0, 22)
        d.text((x0, 2), name, fill=ink, font=small)
    parts.append(("Lookalike check beside the vanilla arrow and feather", band))

    # build compared: depth across the axis and widest row
    lines = []
    for n in ACCEPTED:
        im = Image.open(os.path.join(TEXTURES, "item", f"{n}.png")).convert("RGBA")
        rows = ["".join("#" if im.getpixel((x, y))[3] else "." for x in range(16)) for y in range(16)]
        dep, wid = build(rows)
        lines.append(f"{n:<10} deepest across the axis {dep:>2} px-diagonals (fins included)   widest row {wid:>2}")
    rows = ["".join("." if c == "." else "#" for c in r) for r in PIXXISPAD]
    dep, wid = build(rows)
    dep_b, wid_b = build(PIXXISPAD)
    lines.append(f"{'pixxispad':<10} deepest across the axis {dep:>2} px-diagonals (fins included)   widest row {wid:>2}"
                 f"   (body alone {dep_b} / {wid_b}; the sword is 5 of the fish's 15 diagonal steps)")
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("Build against the accepted fish (slimmer than the tonn)", band))

    # numbers
    lines = measure([os.path.join(VANILLA, "cod.png"), os.path.join(VANILLA, "salmon.png")]
                    + [os.path.join(TEXTURES, "item", f"{n}.png") for n in ACCEPTED] + [OUT_ICON])
    lines.append("STYLE.md food ranges: cover 0.29-0.77, colours 6-20, dark 0.0-0.35, light 0.32-0.99, TL-BR +0.01-+0.17")
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py", band))

    # offline hotbar preview (owner 2026-11-18: flat icons need no Minecraft run), at the GUI scale and at 4x
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    hb = []
    for suffix, items, extra in (
            ("", ["mc:cod", "mod:tonn", "mod:lampuka", "mod:pixxispad", "mc:salmon", "mod:sardina", "mod:cerna",
                  "mod:awrata", "mod:murina"], ["--scale", "2"]),
            ("_x4", ["mc:cod", "mod:tonn", "mod:lampuka", "mod:pixxispad", "mc:salmon", "mod:sardina", "mod:cerna",
                     "mod:awrata", "mod:murina"], ["--scale", "4"]),
            ("_lookalikes", ["mc:arrow", "mc:feather", "mc:cod", "mod:pixxispad", "mod:tonn"], ["--scale", "4"])):
        out = os.path.join(ART, "candidates", f"fish_pixxispad_icon_hotbar{suffix}.png")
        subprocess.run([py, tool, out] + items + ["--select", "3"] + extra, check=True, capture_output=True)
        hb.append(Image.open(out).convert("RGB"))
    band = Image.new("RGB", (W, sum(im.height + 10 for im in hb) + 24), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    ImageDraw.Draw(band).text((10, y), "art/tools/hotbar_preview.py: cod, tonn, lampuka, PIXXISPAD (selected), salmon, "
                              "sardina, cerna, awrata, murina at scale 2 and 4; then arrow, feather, cod, PIXXISPAD, tonn at 4",
                              fill=ink, font=small)
    parts.append(("Hotbar preview (offline, as the game draws flat items)", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Pixxispad (swordfish) item icon, textures/item/pixxispad.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)


def main():
    check(PIXXISPAD)
    icon = render(PIXXISPAD)
    icon.save(OUT_ICON, optimize=False)
    sheet(icon)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
