"""Item icon for the trilja (striped red mullet, Mullus surmuletus): the caught fish, like vanilla cod and salmon.

Night job piece 2 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). It follows the
3D model (art/src/fish_trilja_model.py, palette A): the same keys, each colour lifted about x1.2 for out of water and
keeping its hue. Photos (reference only): art/references/fish_trilja_refonly/ (list.tsv).

What makes it a trilja at 16 x 16, and not the marzpan (the scarlet parrotfish, deep-bodied, grey-lilac cheek,
square tail):
- a slimmer fish, rosy pink-red, not scarlet, with a white belly (countershaded);
- a steep, blunt head, squared off at the front, the eye high on it;
- two pale chin barbels under the mouth;
- a yellow line along the middle of the flank from behind the head to the stalk;
- a striped first dorsal fin and a small second one set apart;
- a forked tail.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left. The body is given row by row (first x, colour keys from the lit back edge to the
shaded belly rim); fins, barbels and the tail are placed pixel by pixel.

Candidates: A (the design above, two barbels tucked at the chin), B (a single barbel), C (one joined pair). CHOSEN is written to the mod.

Run:  art/.venv/bin/python art/src/fish_trilja_icon.py
Writes mod/.../textures/item/trilja.png (byte-identical on rerun), the candidates and the review sheet in
art/candidates/trilja_icon/ and art/candidates/fish_trilja_icon.png, and the offline hotbar previews.
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
import fish_trilja_model as model  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "trilja.png")
CAND = os.path.join(ART, "candidates", "trilja_icon")
OUT_SHEET = os.path.join(ART, "candidates", "fish_trilja_icon.png")
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
PAL.update({
    "h": hx("#ffa09c"),                     # the lit back edge and head top (light from the top left)
    "m": hx("#e05a64"),                     # the back, a deeper rose-red (round 4)
    "p": hx("#f6c4bc"),                     # the pale pink lower flank
    "M": hx("#e1646a"),                     # the back toward the tail, in shade
    "r": hx("#b0485a"),                     # the shaded belly rim (bottom right), a dark rose-red (round 4)
    "q": hx("#f2cfc8"),                     # the belly, pale pink-white
    "C": hx("#ff9791"),                     # the throat, a step darker so the barbels show
    "y": hx("#e8c050"),                     # the yellow line, a soft gold (round 2: a saturated band swamped it)
    "F": hx("#f5d7af"),                     # the first dorsal's pale stripe
    "B": hx("#f0e1c8"),                     # the barbels, cream, a touch below white
    "K": hx("#b84850"),                     # the first dorsal's dark stripe
})
PAL["o"] = hx("#ff9e98")                    # the rose flank between the back and the line
# The whole fish sits a row low (DY), like vanilla's fish items, so the lit back carries the top-left half and the light
# measures top-left to bottom-right as vanilla's do (round 3: the pale belly made it read lit from below).
DY = 1

# Round 3 (critics, rounds 1-2: a straight stick, lit backwards; then a horn over the head, twig tail, a swamping
# line): drawn pixel by pixel. Each body row runs from the lit back edge (upper left) through the back, the rose
# flank, the one-pixel yellow line, pale pink and the belly to the soft shaded rim (lower right). The body is deepest
# behind the head and tapers to the stalk; the head is steep and blunt, the eye high on it with cheek round it.
ROWS = {
    3: (11, "Mr"),                 # the stalk
    4: (10, "Mmor"),               # the line stops two pixels short of the tail
    5: (9, "Mmoyr"),
    6: (7, "mmmoyqr"),             # round 4: the line a row lower, along the middle of the flank
    7: (6, "hmmoyqr"),
    8: (5, "hmmoypqr"),
    9: (4, "hmmoypqr"),            # the line ends here, well behind the eye
    10: (3, "hhmcopqr"),
    11: (2, "hhEccpqr"),           # the eye high on the steep head
    12: (2, "hccCqqr"),
    13: (3, "jjrr"),               # the mouth's corner at the blunt front, the rim under the chin starting behind the
                                   # eye (round 4 polish: a dark run under the eye could read as a frown)
}
FINS = {
    "A": [
        # the first dorsal on the middle of the back, striped pale / dark rose / pale; a gap; the small second one
        (6, 6, "F"), (7, 5, "K"), (6, 5, "f"), (7, 4, "F"),
        (9, 4, "f"), (10, 3, "f"),
        # the anal fin under the rear
        (13, 7, "r"),                # round 4 polish: crimson, a pale one read as a lone speck
        # the forked tail: a filled upper lobe and lower lobe, the notch open between
        (13, 3, "u"), (12, 2, "u"), (12, 1, "T"), (13, 1, "T"), (12, 0, "T"),
        (14, 3, "t"), (15, 3, "t"), (15, 2, "t"),
        # round 4 (critic: two stubs apart read as feet): the barbels tucked against the chin, on a diagonal
        (2, 13, "B"), (3, 14, "B"),
    ],
}
FINS["B"] = [f for f in FINS["A"] if f[2] != "B"] + [(3, 14, "B")]                  # a single barbel
FINS["C"] = [f for f in FINS["A"] if f[2] != "B"] + [(3, 14, "B"), (4, 14, "B")]     # one joined pair
VARIANTS = ("A", "B", "C")


def grid(variant):
    g = [["."] * 16 for _ in range(16)]
    for y, (x0, keys) in ROWS.items():
        for i, k in enumerate(keys):
            g[y + DY][x0 + i] = k
    for x, y, k in FINS[variant]:
        y += DY
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
            if 0 <= ey + dy < 16 and 0 <= ex + dx < 16:
                assert g[ey + dy][ex + dx] not in "KryY", (variant, "dark or yellow beside the eye", ex + dx, ey + dy)


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
    names = [("cod", os.path.join(VANILLA, "cod.png")), ("salmon", os.path.join(VANILLA, "salmon.png"))]
    names += [(n, os.path.join(TEXTURES, "item", n + ".png")) for n in ("marzpan", "kavall", "cerna", "sardina")]
    band = Image.new("RGB", (W, 170), bg)
    d = ImageDraw.Draw(band)
    for i, (n, p) in enumerate([("TRILJA", None)] + names):
        im = icons[CHOSEN] if p is None else Image.open(p).convert("RGBA")
        t = Image.new("RGBA", (136, 136), (139, 139, 139, 255))
        t.alpha_composite(im.resize((128, 128), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (10 + i * 150, 24))
        d.text((10 + i * 150, 4), n, fill=ink, font=small)
    parts.append(("The chosen icon at 8x beside vanilla cod and salmon, the marzpan (red parrotfish), kavall, cerna, "
                  "sardina", band))
    hb = [hotbar(os.path.join(CAND, "hotbar.png"), ["mc:cod", "mod:trilja", "mod:marzpan", "mc:salmon", "mod:kavall",
                                                      "mod:cerna", "mod:sardina", "mc:tropical_fish", "mod:lampuka"], 2),
          hotbar(os.path.join(CAND, "hotbar_x4.png"), ["mc:cod", "mod:trilja", "mod:marzpan", "mc:salmon"], 4)]
    band = Image.new("RGB", (W, sum(i.height + 10 for i in hb) + 10), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    parts.append(("Hotbar preview, unselected (art/tools/hotbar_preview.py): cod, TRILJA, marzpan, salmon, kavall, "
                  "cerna, sardina, tropical fish, lampuka at scale 2; cod, TRILJA, marzpan, salmon at 4", band))
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
    d.text((10, 8), "Trilja (striped red mullet) item icon, textures/item/trilja.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)


def main():
    os.makedirs(CAND, exist_ok=True)
    icons = {}
    for v in VARIANTS:
        g = grid(v)
        check(g, v)
        icons[v] = render(g)
        icons[v].save(os.path.join(CAND, f"icon_{v}.png"))
        if v == CHOSEN:
            print("\n".join("".join(r) for r in g))
    if "--install" in sys.argv:
        icons[CHOSEN].save(OUT_ICON)
    sheet(icons)
    print("wrote", os.path.relpath(OUT_SHEET, ROOT), "(and", os.path.relpath(OUT_ICON, ROOT) + ")" if "--install" in
          sys.argv else "(not installed: pass --install)")


if __name__ == "__main__":
    main()
