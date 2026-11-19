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

REDO 2026-11-19 (owner: "too flat and fat they dont look like the fish"): redrawn side on as a deep diamond with
shading, raked spines, a jutting jaw and the thumbprint (the GRID and PAL below replace the night version above).
A golden olive, B A with a pale halo round the spot, C a greyer silver-olive with near-black spines (chosen by every
critic). Redo critic rounds: 3 of 3, all FAIL (round 3 "close"); the owner judges. Blind reads: all three named a
John Dory, about 60% sure.

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
CHOSEN = "C"


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

# Redo 2026-11-19 (owner: "too flat and fat they dont look like the fish"). Side on, head left, like the hmar: on the
# diagonal the deep disc turned into a round blob. The outline now follows the accepted model's side view: a tall
# compressed disc, deeper than long once the fins count, with a steep forehead down to the big jutting jaw, a keel
# under the throat with the pelvic fin, the long spines rising up and back from the top of the head with filaments
# streaming back, and the rounded tail fan on a short stalk. Shaded for volume: lit top left (H, G), olive-gold in the
# middle (O), darker toward the back and the lower right (b, W), a pale but shaded belly (L, l, w) and a dark rim.
PAL = {
    "o": hx("#3a3422"),  # outline, dark olive
    "p": hx("#5a5236"),  # the belly's outline, a step lighter
    "H": hx("#e2d6a2"),  # the lit highlight, top left
    "G": hx("#c6b47a"),  # lit gold
    "O": hx("#a8995e"),  # olive-gold
    "b": hx("#8a7d4a"),  # mid shade
    "W": hx("#6e6440"),  # shade at the back and lower right
    "L": hx("#e6e2cc"),  # pale belly, lit
    "l": hx("#c3bda2"),  # pale belly
    "w": hx("#9c967c"),  # pale belly, shaded
    "S": hx("#3e3220"),  # St Peter's thumbprint
    "R": hx("#d4c27e"),  # its pale gold halo (candidate B)
    "E": hx("#141210"),  # pupil
    "X": hx("#f2eedc"),  # the eye's pale ring
    "m": hx("#2a2418"),  # the gape
    "j": hx("#b0a88a"),  # the jaw
    "f": hx("#4e4630"),  # spine
    "n": hx("#8a8160"),  # filament
    "d": hx("#9d9068"),  # membrane and soft fins
    "T": hx("#7a6f48"),  # tail
    "u": hx("#5a5236"),  # the tail's edge
    "P": hx("#a59e82"),  # pelvic fin
    "t": hx("#aea683"),  # the tail fan's lighter edge
    "s": hx("#64573a"),  # the thumbprint's mid-dark edge
}
# C: the greyer olive of the market photos (jd05, jd10) and of the model under water
PAL_C = dict(PAL)
PAL_C.update({"H": hx("#dcd6b8"), "G": hx("#bdb48e"), "O": hx("#a29a74"), "b": hx("#857e5c"), "W": hx("#686247"),
              "T": hx("#767052"), "d": hx("#9a9474"), "f": hx("#2e2a1e"), "S": hx("#4a4232"), "R": hx("#c4bc98"),
              "s": hx("#5a5440"), "t": hx("#aaa588"), "w": hx("#7e7862"), "p": hx("#4a4534")})
PALS = {"A": PAL, "B": PAL, "C": PAL_C}

# Keys: o outline, p belly outline, H G O b W the lit-to-shaded flank, L l w the belly, S spot, R its halo, E pupil,
# X eye ring, m gape, j jaw, f spine, n filament, d membrane and soft fins, T tail, u tail edge, P pelvic fin.
# Round 1 (critic: still a pale ball with fuzz on top, longer than deep; the jaw a notch; the spines one block; a flat
# pale belly stripe). Redrawn as a deep diamond, taller than long: the back peaks at (7,3) and the keel at the
# pelvic spine (7,15); four 1 px spines rise from the back with a gap between each, dark roots and light filament
# tips trailing back; the mouth a dark gape slanting down and back from (0,7), the lips lit, jutting past the
# forehead; the eye high on the head with a pale glint; the highlight on the shoulder and the belly shaded; the
# thumbprint a 2 x 2 behind the middle with a mid-dark edge; a narrow stalk and a rounded fan, lighter at its edge.
# Round 2 (critic: close; the spot out-darks the eye, the spines a vertical comb, the forehead too gentle): the eye a
# near-black pupil at (5,6) in a pale ring; the spot a step lighter with a hint of pale ring (C); the spines raked
# back, each tip a pixel behind its base and the filaments further back; a steeper forehead; a dark tail stalk.
GRID = [
#    0123456789012345
    "........n.n.n...",  # 0
    ".......f.f.f....",  # 1
    "......f.f.f.....",  # 2
    "......f.f.f.....",  # 3
    "....oHooo.f.....",  # 4
    "...oHXHGGof.....",  # 5
    "...oXEGGGOo.....",  # 6
    "mjoHGGGOOOOo..T.",  # 7
    "jmoGGGOOObbo.uTt",  # 8
    ".jmGOOOOSSWWoTTt",  # 9
    "..oOOObbSSsooTTt",  # 10
    "...oObbWsWo..TTt",  # 11
    "....obWWWo....T.",  # 12
    ".....pwwp.......",  # 13
    "......pp........",  # 14
    ".......P........",  # 15
]


def grid(variant):
    g = [list(r) for r in GRID]
    if variant == "B":
        # B: the thumbprint in its pale halo, as on the real fish (above and in front, the lit side)
        for x, y in ((8, 8), (9, 8), (7, 9), (7, 10)):
            g[y][x] = "R"
    if variant == "C":
        # C (round 2): a hint of the pale ring on three pixels round the spot
        for x, y in ((7, 9), (8, 8), (10, 10)):
            g[y][x] = "R"
    return g


def render(g, variant):
    P = PALS[variant]
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(g):
        for x, k in enumerate(row):
            if k != ".":
                im.putpixel((x, y), P[k] + (255,))
    return im


def check(g, variant):
    """No stray pixels (touching nothing, even at a corner); one pupil."""
    for y in range(16):
        for x in range(16):
            if g[y][x] == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and g[y + dy][x + dx] != "."
                       for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy):   # diagonal lines allowed
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


MODEL_SHOTS = os.path.join(ART, "candidates", "pixxi_san_pietru_model")


def model_band(W, bg=(52, 52, 56)):
    """The owner-accepted model, side on in game (the spine close-up and the tank view), for the review sheets."""
    shots = [("redo_spines_side.png", (300, 120, 720, 470)), ("redo_side.png", (290, 60, 560, 320))]
    band = Image.new("RGB", (W, 330), bg)
    x = 10
    for name, box in shots:
        path = os.path.join(MODEL_SHOTS, name)
        if not os.path.exists(path):
            continue
        im = Image.open(path).convert("RGB").crop(box)
        im = im.resize((int(im.width * 300 / im.height), 300))
        band.paste(im, (x, 10))
        x += im.width + 20
    return band


def sheet(icons):
    font, small = label_font(16), label_font(13)
    W = 1800
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = [("The accepted model, side on in game (spine close-up, and in the tank)", model_band(W, bg))]
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
