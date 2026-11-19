"""Item icon for the pixxi San Pietru (John Dory, Zeus faber): the caught fish, like vanilla cod and salmon.

Night job piece 2 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). It follows the
critic-passed 3D model (art/src/fish_pixxi_san_pietru_model.py, palette B): the same keys, each colour lifted about
x1.2 for out of water and keeping its hue. Photos (reference only): art/references/fish_pixxi_san_pietru_refonly/.

What makes it a John Dory at 16 x 16:
- a tall, thin oval disc, almost as tall as it is long;
- St Peter's thumbprint: a soft mid brown-olive spot a little above the middle of the side, no ring, lighter than the
  eye's pupil, so it never reads as an eye;
- the eye high near the front: the only black pixel, with cream pixels round it;
- a big upturned jaw jutting forward and up at the front;
- long dorsal spines swept back over the back, a rounded tail fan, the darker olive back and the pale belly.

Drawn pixel by pixel, side on with the head left: the disc is nearly round, so tilted like vanilla's long fish it
read as a lump. Light from the top left, a darker outline like vanilla's.

Candidates: A golden olive (the Mediterranean photo jd02); B a greyer olive (the market photos jd05, jd10); C as A
with the spot a step lighter. Icon critic rounds: 8 (PASS in round 8). CHOSEN is written to the mod.

Run:  art/.venv/bin/python art/src/fish_pixxi_san_pietru_icon.py
Writes mod/.../textures/item/pixxi_san_pietru.png (byte-identical on rerun), the candidates and the review sheet in
art/candidates/pixxi_san_pietru_icon/ and art/candidates/fish_pixxi_san_pietru_icon.png, and the offline hotbar
previews.
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
import fish_pixxi_san_pietru_model as model  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "pixxi_san_pietru.png")
CAND = os.path.join(ART, "candidates", "pixxi_san_pietru_icon")
OUT_SHEET = os.path.join(ART, "candidates", "fish_pixxi_san_pietru_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
CHOSEN = "A"


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lift(c, k=1.2):
    """Out of water: brightness x1.2, hue and saturation kept."""
    h, s, v = colorsys.rgb_to_hsv(*(x / 255.0 for x in c))
    return tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb(h, s, min(1.0, v * k)))


def scale(c, k):
    return tuple(max(0, min(255, int(round(x * k)))) for x in c)


MODEL = {k: hx(v) for k, v in model.PALETTES[model.CHOSEN].items()}
PAL = {k: lift(v) for k, v in MODEL.items()}
PAL["E"] = MODEL["E"]                       # the pupil stays black
PAL["S"] = MODEL["S"]                       # the spot keeps the model's tone: lifted it washed out to a stain
PAL["s"] = MODEL["s"]
# the back and the spines keep the model's own darker olive (lifted, the back read pale and the spines vanished);
# the pale belly is not lifted further (the model's is already near white), and the lowest band is a shaded pale so
# the light still falls from the top left
for key in "KBbfdLW":
    PAL[key] = MODEL[key]
PAL["W"] = scale(MODEL["L"], 0.97)
PAL["n"] = MODEL["d"]


# The outline: the model's back edge, a step darker (vanilla's fish have a darker rim, about 0.6 of the inside)
PAL["o"] = scale(MODEL["K"], 0.8)
# the tail keeps the model's own tones (lifted, it read as a pale flag)
PAL["T"] = MODEL["T"]
PAL["u"] = MODEL["r"]
PAL["X"] = hx("#f4f2e6")                   # the eye's glint
# round 1 fixes: the flank toned from yellow toward the photos' olive-gold (the lifted model colours read as a
# banana), the spot's ring only a step lighter than the flank round it, so the spot is no second eye
PAL.update({"G": hx("#c6b683"), "O": hx("#b4a679"), "b": hx("#938962"), "L": hx("#d8d1b2"), "W": hx("#a3976f"),
            "S": hx("#5c4e35"), "T": hx("#8a7f52"), "u": hx("#5e5634"),
            "H": hx("#d8cea5"), "V": hx("#857b57"), "W": hx("#9a8e68"), "d": hx("#6f6850"), "w": hx("#a49c7c")})
PAL.update({"H": hx("#d8cc96"), "G": hx("#b9a96a"), "O": hx("#a89a5c"), "b": hx("#8c7f48"), "W": hx("#766b3e"),
            "V": hx("#5e5634"), "S": hx("#55462b"), "n": hx("#c9bd8e"), "o": hx("#433d2a"),
            "s": hx("#6c5c3a"), "I": hx("#d8cc96"), "q": hx("#5e5634"), "m": hx("#433d2a"), "D": hx("#8a7f52"),
            "T": hx("#6e6644"), "f": hx("#6e6644"), "k": hx("#36311f"), "S": hx("#504228")})
PAL["R"] = hx("#c4b472")                   # the spot's ring: one step lighter than the flank (round 3: brighter, it made the spot an eye)
# B: a greyer olive flank, as the market photos jd05 and jd10 (A follows the golden Mediterranean fish, jd02)
PAL_B = dict(PAL)
PAL_B.update({"O": hx("#a09a70"), "G": hx("#b4ae84"), "b": hx("#86805c"), "W": hx("#706a4a")})
# C: as A with the spot a step lighter, a softer smudge
PAL_C = dict(PAL)
PAL_C["S"] = hx("#5e5034")
PALS = {"A": PAL, "B": PAL_B, "C": PAL_C}

# Keys: o outline, G lit golden back, O olive-gold, b mid flank, W shaded belly, S spot, H the lit highlight on the back, V the shaded belly rim, d spine membrane, w the jaw's shade, E pupil, X its glint, j lower jaw, m gape, f spine, n spine tip, T tail, u tail lobes.
# Round 1 (critic: level and round it read as a cartoon face or a pufferfish, no jaw, lit backwards, too heavy): laid
# on vanilla's diagonal, head lower left, tail upper right; a thin oval 6 px across, lit from the top left along the
# back and darkest along the belly's lower-right edge; four spines of uneven length standing up off the back (swept
# toward the tail, which on this diagonal is straight up); a dark gape at the jutting jaw; a 2 x 2 eye with a glint
# and no ring; the spot behind and above the middle, out of line with the eye, in a pale gold ring; a forked tail.
# Round 2 (critic: lit backwards, spines like insect legs, tail like antlers): the lightest tone moved to the back at
# the top left and the belly rim shaded; the spines joined by a membrane into one fin; the tail filled into one fan.
GRID = [
    "........n...o...",
    "......nff.n.To..",
    ".....fDfDfD.TTo.",
    ".....fDoDoooTToo",
    ".....ooHGGoTo...",
    "....oHHGGOOk....",
    "...oIHGGOObk....",
    "..oHEGGGObWk....",
    "oGoHGGGSSWWk....",
    "mmHGGOOSSOo.....",
    ".oGGOObbWo......",
    ".oGOObWWo.......",
    "..oObWWoff......",
    "...oooo.........",
    "...f............",
    "................",
]


def grid(variant):
    return [list(r) for r in GRID]


def render(g, variant):
    P = PALS[variant]
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(g):
        for x, k in enumerate(row):
            if k != ".":
                im.putpixel((x, y), P[k] + (255,))
    return im


def check(g, variant):
    """No stray pixels; the eye is a 2 x 2 with one glint."""
    for y in range(16):
        for x in range(16):
            if g[y][x] == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and g[y + dy][x + dx] != "."
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                print(f"warning {variant}: stray pixel at {x},{y}")
    assert sum(r.count("E") for r in g) == 1, variant


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{os.path.basename(d['file']):<26} cover {d['coverage']:.2f}  colours {d['colours']:>2}  "
                         f"dark {d['lmin']:.2f}  light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  "
                         f"inside {d['interior_l']:.2f}  TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def hotbar(out, items, sc):
    py = os.path.join(ART, ".venv", "bin", "python")
    subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items + ["--scale", str(sc)],
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
    names += [(n, os.path.join(TEXTURES, "item", n + ".png")) for n in ("cerna", "tonn", "awrata", "kavall")]
    band = Image.new("RGB", (W, 170), bg)
    d = ImageDraw.Draw(band)
    for i, (n, p) in enumerate([("PIXXI SAN PIETRU", None)] + names):
        im = icons[CHOSEN] if p is None else Image.open(p).convert("RGBA")
        t = Image.new("RGBA", (136, 136), (139, 139, 139, 255))
        t.alpha_composite(im.resize((128, 128), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (10 + i * 150, 24))
        d.text((10 + i * 150, 4), n, fill=ink, font=small)
    parts.append(("The chosen icon at 8x beside vanilla cod and salmon and the cerna, tonn, awrata and kavall", band))
    hb = [hotbar(os.path.join(CAND, "hotbar.png"), ["mc:cod", "file:" + os.path.join(CAND, f"icon_{CHOSEN}.png"),
                                                      "mc:salmon", "mod:cerna", "mod:awrata", "mod:tonn",
                                                      "mc:tropical_fish", "mc:pufferfish", "mod:kavall"], 2),
          hotbar(os.path.join(CAND, "hotbar_x4.png"), ["mc:cod", "file:" + os.path.join(CAND, f"icon_{CHOSEN}.png"),
                                                         "mc:salmon", "mc:tropical_fish"], 4)]
    band = Image.new("RGB", (W, sum(i.height + 10 for i in hb) + 10), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    parts.append(("Hotbar preview, unselected (art/tools/hotbar_preview.py): cod, PIXXI SAN PIETRU, salmon, cerna, awrata, "
                  "tonn, tropical fish, pufferfish, kavall at scale 2; cod, PIXXI SAN PIETRU, salmon, tropical fish at 4",
                  band))
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
    d.text((10, 8), "Pixxi San Pietru (John Dory) item icon, textures/item/pixxi_san_pietru.png", fill=ink,
           font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)


def main():
    os.makedirs(CAND, exist_ok=True)
    icons = {}
    for v in ("A", "B", "C"):
        g = grid(v)
        check(g, v)
        icons[v] = render(g, v)
        icons[v].save(os.path.join(CAND, f"icon_{v}.png"))
    icons[CHOSEN].save(OUT_ICON)
    sheet(icons)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
