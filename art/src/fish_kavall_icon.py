"""Item icon for the kavall (Atlantic chub mackerel, Scomber colias): the caught fish, like vanilla cod and salmon.

Night job piece 2 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). It follows the
critic-passed 3D model (art/src/fish_kavall_model.py, palette A): the same keys, each colour lifted about x1.2 for out
of water and keeping its hue. Photos (reference only): art/references/fish_kavall_refonly/ (list.tsv).

What makes it a kavall at 16 x 16:
- a slim torpedo, five pixels across the diagonal, pointed at the snout, tapering to a thin stalk;
- a blue-green back with thin dark bars every third pixel, starting well behind the eye (nothing dark near it);
- a lit sheen on the back's edge, a green-silver upper flank, a bright silver lower flank and a dark belly rim;
- one big black eye with a pale cheek ring below and behind it, and no other dark mark in its row;
- two dorsal fins set apart, a small finlet on the back and one under the belly just before the tail;
- a deeply forked olive-yellow tail.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left.

The body is drawn in diagonal bands: band c holds the pixels with x + y = c (c 13 is the back's edge, c 17 the belly
rim), each band given as a run of colour keys from its first x. Fins and the tail are placed pixel by pixel.

Candidates: A (the design above), B (a sixth band: silver and grey below the band, a deeper fish), C (the bars run on
into the upper flank, two pixels long, from the trunk's middle back). CHOSEN is written to the mod.

Run:  art/.venv/bin/python art/src/fish_kavall_icon.py
Writes mod/.../textures/item/kavall.png (byte-identical on rerun), the candidates and the review sheet in
art/candidates/kavall_icon/ and art/candidates/fish_kavall_icon.png, and the offline hotbar previews.
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
import fish_kavall_model as model  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "kavall.png")
CAND = os.path.join(ART, "candidates", "kavall_icon")
OUT_SHEET = os.path.join(ART, "candidates", "fish_kavall_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
CHOSEN = "A"


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lift(c, k=1.2):
    """Out of water: brightness x1.2, hue and saturation kept."""
    h, s, v = colorsys.rgb_to_hsv(*(x / 255.0 for x in c))
    return tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb(h, s, min(1.0, v * k)))


MODEL = {k: hx(v) for k, v in model.PALETTES["A"].items()}
PAL = {k: lift(v) for k, v in MODEL.items()}
PAL["E"] = MODEL["E"]                       # the eye stays black
# the back keeps the model's own tones (lifted x1.2 they read pale mint at 1x), the bars a step darker so they show
for key in "Hmg":
    PAL[key] = MODEL[key]
PAL["k"] = hx("#24504f")                    # round 2: lighter, so the eye stays the darkest mark
PAL.update({"n": hx("#6f8f8c"), "b": hx("#c9d5d3"), "B": hx("#e6efed"), "r": hx("#c3d0ce"), "R": hx("#a3b3b3"),
            "G": hx("#d6e0de"), "q": hx("#7d8e90"), "D": hx("#8a8f6e"),
            # round 2 polish (critic): the silver shine kept to two highlights, softer elsewhere (Y); no lone dark
            # pixel by the head (O)
            "Y": hx("#dfe8e5"), "O": hx("#6a7a7e")})
# the tail and fins: the model's olive-yellow, lifted only half way (fully lifted the tail read as a bright flag)
for key in "FfaTtu":
    PAL[key] = lift(MODEL[key], 1.08)
PAL["h"] = lift(MODEL["H"])                 # the lit sheen on the back's edge: the head's steel, lifted x1.2
PAL["o"] = hx("#3d4a52")                    # the dark belly rim, in the shade (bottom right)
# fins: the model's olive-yellow, lifted
FIN = {k: PAL[k] for k in "FfaTtu"}

# The body, row by row: y -> (first x, keys). The back's edge steps one pixel left per row and the belly's edge too,
# so the fish lies on the diagonal, six pixels across each row in the middle (thinner at the stalk and the snout).
# Each row runs from the lit back edge (h) through the back (m, with the dark bars k), the green-silver flank (g), the
# bright silver (W) to the shaded belly rim (o).
ROWS = {
    # round 2 (critic): the belly swells at rows 8-10 (its edge steps in 1 and 2 px runs, not one straight staircase);
    # the belly shades from bright silver (W, three highlights on the lit front half) through pale (B) to a shaded pale
    # (b) beside the dark rim; the eye's ring is a soft grey-silver (r, R), not pure white, the gill a pale silver (G)
    # and the pixel two behind the eye a mid grey (q), so the eye is the only near-black pixel; the bars are a lighter
    # dark teal, three of them, each running on onto the flank in a fading tone (n), the first well behind the eye.
    "A": {
        3: (10, "hmm"),            # the stalk, teal right to the tail
        4: (9, "hkmgo"),           # a bar near the tail
        5: (7, "hmmgbbo"),
        6: (6, "hkknYbo"),         # a bar: dark across the back, fading onto the flank
        7: (5, "hmmgWbo"),
        8: (4, "hkknWbbo"),        # a bar; the belly starts to swell
        9: (3, "hmmgYbbo"),
        10: (2, "hmmgBbbo"),
        11: (2, "hHHGbO"),         # the head: the steel crown, the pale gill cover; the belly rim eases out (O)
        12: (1, "HrErq"),          # the eye, ringed in soft grey-silver
        13: (1, "HRR"),
        14: (1, "Hj"),             # the pointed snout, the mouth's end
    },
}
ROWS["B"] = {y: (x0, keys.replace("hkkn", "hkmn")) for y, (x0, keys) in ROWS["A"].items()}   # thinner bars
ROWS["C"] = dict(ROWS["A"])
ROWS["C"].update({8: (4, "hmmgWbbo"), 9: (3, "hkkgWbbo")})   # the third bar a row nearer the head
# Fins and tail, pixel by pixel: (x, y, key).
FINS = [
    (4, 7, "D"), (5, 6, "D"), (4, 6, "D"),        # the first dorsal fin, grey-olive (round 2: cream read as a spot)
    (7, 4, "f"),                                  # the small second dorsal fin, set apart
    (10, 2, "f"),                                 # a finlet on the back before the tail
    (12, 7, "a"),                                 # the anal fin
    (10, 10, "a"),                                # the pelvic fin, under the swollen belly
    # the forked tail: an upper lobe up from the stalk, a lower lobe out to the right, the notch between left open
    (13, 0, "T"), (14, 0, "T"), (12, 1, "T"), (13, 1, "T"), (12, 2, "T"), (13, 2, "u"),
    (13, 3, "u"), (14, 4, "t"), (15, 4, "t"), (15, 5, "t"),
]


def grid(variant):
    g = [["."] * 16 for _ in range(16)]
    for y, (x0, keys) in ROWS[variant].items():
        for i, k in enumerate(keys):
            g[y][x0 + i] = k
    for x, y, k in FINS:
        assert g[y][x] == ".", ("fin over body", variant, x, y)
        g[y][x] = k
    return g


def render(g):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(g):
        for x, k in enumerate(row):
            if k != ".":
                im.putpixel((x, y), PAL[k] + (255,))
    return im


def check(g, variant):
    """No stray pixels (each opaque pixel has an opaque 4-neighbour), and nothing dark beside the eye."""
    for y in range(16):
        for x in range(16):
            if g[y][x] == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and g[y + dy][x + dx] != "."
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                print(f"warning {variant}: stray pixel at {x},{y}")
    ey, ex = next((y, x) for y in range(16) for x in range(16) if g[y][x] == "E")
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            k = g[ey + dy][ex + dx]
            assert k not in "ko", (variant, "dark beside the eye", ex + dx, ey + dy)


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
    # candidates at 8x, 2x, 1x
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
    # beside vanilla and accepted fish
    names = [("cod", os.path.join(VANILLA, "cod.png")), ("salmon", os.path.join(VANILLA, "salmon.png"))]
    names += [(n, os.path.join(TEXTURES, "item", n + ".png")) for n in ("sardina", "incova", "tonn", "cerna")]
    band = Image.new("RGB", (W, 170), bg)
    d = ImageDraw.Draw(band)
    for i, (n, p) in enumerate([("KAVALL", None)] + names):
        im = icons[CHOSEN] if p is None else Image.open(p).convert("RGBA")
        t = Image.new("RGBA", (136, 136), (139, 139, 139, 255))
        t.alpha_composite(im.resize((128, 128), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (10 + i * 150, 24))
        d.text((10 + i * 150, 4), n, fill=ink, font=small)
    parts.append(("The chosen icon at 8x beside vanilla cod and salmon and the accepted sardina, incova, tonn, cerna",
                  band))
    # hotbar previews, unselected
    hb = [hotbar(os.path.join(CAND, "hotbar.png"), ["mc:cod", "mod:kavall", "mc:salmon", "mod:sardina", "mod:incova",
                                                      "mod:tonn", "mod:cerna", "mc:tropical_fish", "mod:lampuka"], 2),
          hotbar(os.path.join(CAND, "hotbar_x4.png"), ["mc:cod", "mod:kavall", "mc:salmon", "mod:incova"], 4)]
    band = Image.new("RGB", (W, sum(i.height + 10 for i in hb) + 10), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    parts.append(("Hotbar preview, unselected (art/tools/hotbar_preview.py): cod, KAVALL, salmon, sardina, incova, tonn, "
                  "cerna, tropical fish, lampuka at scale 2; cod, KAVALL, salmon, incova at 4", band))
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
    d.text((10, 8), "Kavall (chub mackerel) item icon, textures/item/kavall.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)


def main():
    os.makedirs(CAND, exist_ok=True)
    icons = {}
    for v in ROWS:
        g = grid(v)
        check(g, v)
        icons[v] = render(g)
        icons[v].save(os.path.join(CAND, f"icon_{v}.png"))
        if v == CHOSEN:
            print("\n".join("".join(r) for r in g))
    icons[CHOSEN].save(OUT_ICON)
    sheet(icons)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
