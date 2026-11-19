"""Item icon for the tird (ornate wrasse, Thalassoma pavo, the male): the caught fish, like vanilla cod and salmon.

Night job piece 2 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). It follows the
critic-passed 3D model (art/src/fish_tird_model.py, palette A): the same keys, each colour lifted about x1.2 for out
of water and keeping its hue. Photos (reference only): art/references/fish_tird_refonly/ (list.tsv).

What makes it a tird at 16 x 16:
- small and slim: five or six pixels across the diagonal, pointed at the snout, tapering to a thin stalk;
- a turquoise-blue head, lit on top, with one pink-violet line behind and below the eye;
- one black eye near the top of the head, nothing dark beside it;
- just behind the head a bright turquoise bar, then a red-orange band two pixels wide, both running across the body;
- a green body, lit along the back's edge, darker on the back, a cream belly and a shaded belly rim (plain, like the
  model: its red-line pixels turned to maroon squares under water and were dropped);
- a low teal dorsal fin along the back;
- a lunate tail: a green base, two turquoise lobes swept back to dark blue tips, the notch between them left open.

Icon critic rounds: 2 (PASS in rounds 1 and 2; round 1's fixes applied).

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left.

The body is drawn from two numbers per pixel: a = x - y, the place along the fish (snout -12, stalk 7), and
d = x + y, the depth across it (back edge small, belly large). The cross bars are lines of constant a, the shading
runs with d. Fins and the tail are placed pixel by pixel.

Candidates: A (the design above, a plain green body like the passed model), B (two thin broken red lines on the body,
as the first model had), C (the head bluer, as candidate B of the model). CHOSEN is written to the mod.

Run:  art/.venv/bin/python art/src/fish_tird_icon.py
Writes mod/.../textures/item/tird.png (byte-identical on rerun), the candidates and the review sheet in
art/candidates/tird_icon/ and art/candidates/fish_tird_icon.png, and the offline hotbar previews.
"""
import colorsys
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(ART, ".."))
sys.path.insert(0, os.path.join(ART, "tools"))
sys.path.insert(0, HERE)
from font import label_font  # noqa: E402
import fish_tird_model as model  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "tird.png")
CAND = os.path.join(ART, "candidates", "tird_icon")
OUT_SHEET = os.path.join(ART, "candidates", "fish_tird_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
CHOSEN = "A"


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lift(c, k=1.2):
    """Out of water: brightness x1.2, hue and saturation kept."""
    h, s, v = colorsys.rgb_to_hsv(*(x / 255.0 for x in c))
    return tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb(h, s, min(1.0, v * k)))


def palette(variant):
    """The model's palette, NOT lifted: the model's colours were already pushed lighter and brighter for the water over
    four critic rounds, and lifted another x1.2 they read pastel and lime at 1x (maker, first look: inside 0.73 and
    edge 0.72 against vanilla's 0.54 and 0.32). The edges get darker tones so the fish has vanilla's darker rim."""
    M = {k: hx(v) for k, v in model.PALETTES[variant].items()}
    P = dict(M)
    P["m"] = hx("#3c8240")                   # the back: a darker green, the fish's upper rim (countershading)
    P["l"] = M["g"]                          # the lit upper flank, just inside the back (light from the top left)
    P["g"] = hx("#78bc48")                   # the flank
    P["u"] = hx("#78bc48")                   # the tail's base, the flank's green
    P["w"] = hx("#d4e6a4")                   # the cream belly
    P["o"] = hx("#2e5a3a")                   # the shaded belly rim, a dark green (never as dark as the eye)
    P["h"] = lift(M["H"], 1.15)              # the lit crown of the head
    P["n"] = hx("#2f7088")                   # the head's shaded underside and chin
    P["q"] = hx("#a8481e")                   # the band where it rounds into the shaded belly
    P["F"] = hx("#4f9a88")                   # the dorsal fin, a mid teal
    # icon critic round 1 (PASS, with fixes): the greens less neon, a touch toward olive (l, g, u); the belly cream
    # dimmer so the lit back reads as the light side (w); the bar a clearer, greener pale cyan (B); a dark teal (t)
    # joining each tail tip to the fin
    P["l"] = hx("#a2c862")
    P["g"] = hx("#7eb04c")
    P["u"] = hx("#7eb04c")
    P["w"] = hx("#c2d698")
    P["B"] = hx("#a8f4d0")
    P["t"] = hx("#3f8a8a")
    return P


PALS = {"A": palette("A"), "B": palette("A"), "C": palette("B")}

# The body's outline: for each a, the d range from the back edge to the belly rim.
# (maker, first look: five pixels across was a stick, cover 0.26 under vanilla's 0.29) six to seven across the middle.
LOHI = {-12: (14, 15), -11: (13, 16), -10: (12, 17)}
LOHI.update({a: (12, 18) for a in range(-9, 2)})
LOHI.update({2: (13, 18), 3: (13, 18), 4: (13, 18), 5: (13, 17), 6: (14, 17), 7: (14, 16)})
EYE = (2, 11)                                 # a -9, d 13: one pixel in from the crown, near the front


def body_key(variant, a, d):
    lo, hi = LOHI[a]
    if a <= -8:                                # the head
        if a == -12:
            return "S"
        if (a, d) == (-8, 18):
            return "L"                         # the pink-violet line, low on the cheek, well away from the eye
        if d == lo:
            return "h"
        if d >= hi:
            return "n"
        if d == hi - 1:
            return "c"
        return "H"
    if a == -7:                                # the turquoise bar
        return "b" if d >= hi else "B"
    if a in (-6, -5):                          # the red-orange band
        return "q" if d >= hi else "R"
    if d == hi:
        return "o"
    if d == hi - 1:
        return "w"
    if d == lo:
        return "m"                             # the back's dark rim
    if d == lo + 1:
        return "l"                             # the lit upper flank
    if variant == "B" and a in (-2, 2) and d == 15:
        return "r"                             # the thin red lines, broken: one pixel on the flank ...
    if variant == "B" and a in (-1, 3) and d == 13:
        return "k"                             # ... and one on the back a step behind it
    return "g"


# The dorsal fin along the back (d = lo - 1) and the tail, pixel by pixel: (x, y, key).
DORSAL_A = range(-6, 4)
# (maker, first look: the upper lobe stood straight up like a stick) a crescent across the fish's line: the base on
# the stalk (a 8 and 9), the arc (a 10, green in the middle, turquoise to the ends) and the two tips one step further
# back (a 11), dark blue-grey.
TAIL = [
    (11, 3, "u"), (12, 4, "u"), (11, 2, "u"), (12, 3, "u"), (13, 4, "u"),
    (11, 1, "t"), (12, 2, "u"), (13, 3, "u"), (14, 4, "d"),
    (11, 0, "d"),
]
# (icon critic round 1: the lower tip stuck out as a 2 px spike, the upper one read as a speck) each tip joined to the
# fin by a dark teal pixel (t) or set straight on the green base, the lower one pulled in a pixel


def grid(variant):
    g = [["."] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            a, d = x - y, x + y
            if a in LOHI and LOHI[a][0] <= d <= LOHI[a][1]:
                g[y][x] = body_key(variant, a, d)
            elif a in DORSAL_A and d == LOHI[a][0] - 1:
                g[y][x] = "F"
    g[EYE[1]][EYE[0]] = "E"
    for x, y, k in TAIL:
        assert g[y][x] == ".", ("tail over body", variant, x, y, g[y][x])
        g[y][x] = k
    return g


def render(g, P):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(g):
        for x, k in enumerate(row):
            if k != ".":
                im.putpixel((x, y), P[k] + (255,))
    return im


def check(g, variant):
    """No stray pixels (each opaque pixel has an opaque 4-neighbour), and nothing dark beside the eye."""
    for y in range(16):
        for x in range(16):
            if g[y][x] == ".":
                continue
            assert any(0 <= x + dx < 16 and 0 <= y + dy < 16 and g[y + dy][x + dx] != "."
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), (variant, "stray pixel", x, y)
    ex, ey = EYE
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            assert g[ey + dy][ex + dx] not in "odqL" or (dx, dy) == (0, 0), (variant, "dark beside the eye")
    assert sum(r.count("E") for r in g) == 1


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{os.path.basename(d['file']):<22} cover {d['coverage']:.2f}  colours {d['colours']:>2}  "
                         f"dark {d['lmin']:.2f}  light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  "
                         f"inside {d['interior_l']:.2f}  TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def hotbar(out, items, scale):
    py = os.path.join(ART, ".venv", "bin", "python")
    subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items + ["--scale", str(scale)],
                   check=True, capture_output=True)
    return Image.open(out).convert("RGB")


def sheet(icons):
    font, small = label_font(16), label_font(13)
    W = 1800
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []
    band = Image.new("RGB", (W, 200), bg)
    d = ImageDraw.Draw(band)
    x = 10
    for v, im in icons.items():
        for s in (8, 2, 1):
            t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), (139, 139, 139, 255))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x, 24))
            d.text((x, 4), f"{v} {s}x" + (" (chosen)" if v == CHOSEN and s == 8 else ""), fill=ink, font=small)
            x += max(16 * s + 20, 60)
        x += 30
    parts.append(("Candidates A, B, C at 8x, 2x, 1x", band))
    names = [("cod", os.path.join(VANILLA, "cod.png")), ("tropical fish", os.path.join(VANILLA, "tropical_fish.png"))]
    names += [(n, os.path.join(TEXTURES, "item", n + ".png")) for n in ("cawl", "sardina", "cerna", "tonn")]
    band = Image.new("RGB", (W, 170), bg)
    d = ImageDraw.Draw(band)
    for i, (n, p) in enumerate([("TIRD", None)] + names):
        im = icons[CHOSEN] if p is None else Image.open(p).convert("RGBA")
        t = Image.new("RGBA", (136, 136), (139, 139, 139, 255))
        t.alpha_composite(im.resize((128, 128), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (10 + i * 150, 24))
        d.text((10 + i * 150, 4), n, fill=ink, font=small)
    parts.append(("The chosen icon at 8x beside vanilla cod and tropical fish and the accepted cawl, sardina, cerna, tonn",
                  band))
    hb = [hotbar(os.path.join(CAND, "hotbar.png"), ["mc:cod", "mod:tird", "mc:salmon", "mc:tropical_fish", "mod:cawl",
                                                      "mod:sardina", "mod:cerna", "mod:tonn", "mod:lampuka"], 2),
          hotbar(os.path.join(CAND, "hotbar_x4.png"), ["mc:cod", "mod:tird", "mc:tropical_fish", "mod:cawl"], 4)]
    band = Image.new("RGB", (W, sum(i.height + 10 for i in hb) + 10), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    parts.append(("Hotbar preview, unselected (art/tools/hotbar_preview.py): cod, TIRD, salmon, tropical fish, cawl, "
                  "sardina, cerna, tonn, lampuka at scale 2; cod, TIRD, tropical fish, cawl at 4", band))
    lines = measure([os.path.join(VANILLA, "cod.png"), os.path.join(VANILLA, "salmon.png")]
                    + [os.path.join(CAND, f"icon_{v}.png") for v in icons])
    lines.append("STYLE.md food ranges: cover 0.29-0.77, colours 6-20, dark 0.0-0.35, light 0.32-0.99, TL-BR +0.01-+0.17")
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py", band))
    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Tird (ornate wrasse) item icon, textures/item/tird.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)


def main():
    os.makedirs(CAND, exist_ok=True)
    icons = {}
    for v in PALS:
        g = grid(v)
        check(g, v)
        icons[v] = render(g, PALS[v])
        icons[v].save(os.path.join(CAND, f"icon_{v}.png"))
        if v == CHOSEN:
            print("\n".join("".join(r) for r in g))
    icons[CHOSEN].save(OUT_ICON)
    sheet(icons)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
