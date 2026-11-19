"""Item icon for the sawt (lesser weever, Echiichthys vipera): the caught fish, like vanilla cod and salmon.

Night job piece 2 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). It follows the
critic-passed 3D model (art/src/fish_sawt_model.py, palette A): the same keys, each colour lifted about x1.2 for out
of water and keeping its hue. Photos (reference only): art/references/fish_sawt_refonly/ (list.tsv).

What makes it a weever at 16 x 16:
- a slim body, deepest at the head, tapering to a thin stalk;
- the short jet-black first dorsal fin (the venomous one) just behind the head: its key mark;
- the eye on the back's edge (the eyes sit on top of the head), with a gold ring and nothing else dark near it;
- a blunt head with an upturned mouth: the pale lower jaw at the front;
- a sandy-gold back with thin oblique dark lines, gold flanks, a cream belly;
- a long, low second dorsal fin, a square yellow tail with a black edge.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left.

Candidates: A (the design above), B (A without the oblique lines: a plainer flank), C (A with a taller dorsal fin, one
more spine pixel; the critic's pick). CHOSEN is written to the mod.

Run:  art/.venv/bin/python art/src/fish_sawt_icon.py
Writes mod/.../textures/item/sawt.png (byte-identical on rerun), the candidates and the review sheet in
art/candidates/sawt_icon/ and art/candidates/fish_sawt_icon.png, and the offline hotbar previews.
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
import fish_sawt_model as model  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "sawt.png")
CAND = os.path.join(ART, "candidates", "sawt_icon")
OUT_SHEET = os.path.join(ART, "candidates", "fish_sawt_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
CHOSEN = "A"  # overridden below, after the grids


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lift(c, k=1.2):
    """Out of water: brightness x1.2, hue and saturation kept."""
    h, s, v = colorsys.rgb_to_hsv(*(x / 255.0 for x in c))
    return tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb(h, s, min(1.0, v * k)))


MODEL = {k: hx(v) for k, v in model.PALETTES["A"].items()}
PAL = {k: lift(v) for k, v in MODEL.items()}
for key in "ESsK":
    PAL[key] = MODEL[key]                   # the eye, the black fin and the tail's edge stay black
# Like vanilla's cod (measured, not copied): a mid-tone outline on the lit top-left edge, the darkest outline on the
# shaded bottom-right edge, the light inside. Fully lifted x1.2 the pale tones went white at 1x, so the light ones are
# lifted less (the model's tone, or a little above it), keeping the hue.
PAL.update({
    "h": hx("#8a6c38"),   # the back's edge outline, a mid tone
    "m": hx("#b08a48"),   # the back (the model's side top row)
    "L": hx("#7a5e30"),   # the oblique lines
    "g": hx("#d4b468"),   # the gold flank
    "c": hx("#e4cc88"),   # the pale gold lower flank
    "b": hx("#f0e6c4"),   # the cream belly
    "o": hx("#6e5630"),   # the shaded belly outline (bottom right), the darkest edge
    "O": hx("#7e6438"),
    "q": hx("#d4b468"),   # the cheek
    "R": hx("#c9a24a"),   # one gold iris pixel under the eye
    "J": hx("#e4cc88"),   # the jutting lower jaw, pale
    "P": hx("#c4a868"),   # the pelvic and anal fins
    "p": hx("#b09455"),   # the low second dorsal
    "T": hx("#f0c020"), "t": hx("#c89818"),
})
# The body, row by row (top row first): head lower left, tail upper right. "." is clear.
GRIDS = {
    # round 1 (critic): the fin and tail edge warm brown-black so the eye is the only true black; no gold under the eye
    # and no pale point at the snout; a highlight just inside the back (H) so the light comes from the top left; the
    # belly's cream toned down so it doesn't read as a stripe; a bulkier head, a narrower stalk. Round 2: the stalk's
    # gap filled with the tail's root, the fin's lowest pixel made back outline (3 px clear of the eye), no pale pixel
    # near the eye, a darker gold band along the back
    "A": [
        "............K...",
        "...........TTK..",
        "..........hTTTK.",
        ".........hmtTTK.",
        "........hHmto...",
        ".......pHLgco...",
        "....SspmLggco...",
        "...SShHmgcco....",
        "...hhmLggco.....",
        "...hmHgcPco.....",
        "..hhPggPPo......",
        ".hEmHgcco.......",
        "hmmqggcO........",
        ".qJcco..........",
        "..Jo............",
        "................",
    ],
}
GRIDS["B"] = [r.replace("L", "m") for r in GRIDS["A"]]          # no oblique lines
GRIDS["C"] = list(GRIDS["A"])                                   # a taller first dorsal: one more spine pixel
GRIDS["C"][5] = "....S..pHLgco..."
CHOSEN = "C"
PAL["H"] = hx("#d4b468")                    # the highlight just inside the lit back
for key in "SK":
    PAL[key] = hx("#2e241a")                # the fin and the tail's edge: warm brown-black, so the eye is the only black
PAL["s"] = hx("#4a3a2a")


def render(g):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(g):
        assert len(row) == 16, (y, row)
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
    for dy in (-2, -1, 0, 1, 2):
        for dx in (-2, -1, 0, 1, 2):
            if 0 <= ey + dy < 16 and 0 <= ex + dx < 16 and (dx or dy):
                assert g[ey + dy][ex + dx] not in "SsKLE", (variant, "dark near the eye", ex + dx, ey + dy)


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
    names += [(n, os.path.join(TEXTURES, "item", n + ".png")) for n in ("sardina", "incova", "skorfna", "cerna")]
    band = Image.new("RGB", (W, 170), bg)
    d = ImageDraw.Draw(band)
    for i, (n, p) in enumerate([("SAWT", None)] + names):
        im = icons[CHOSEN] if p is None else Image.open(p).convert("RGBA")
        t = Image.new("RGBA", (136, 136), (139, 139, 139, 255))
        t.alpha_composite(im.resize((128, 128), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (10 + i * 150, 24))
        d.text((10 + i * 150, 4), n, fill=ink, font=small)
    parts.append(("The chosen icon at 8x beside vanilla cod and salmon and the accepted sardina, incova, skorfna, cerna",
                  band))
    hb = [hotbar(os.path.join(CAND, "hotbar.png"), ["mc:cod", "mod:sawt", "mc:salmon", "mod:sardina", "mod:incova",
                                                      "mod:skorfna", "mod:cerna", "mc:tropical_fish", "mod:lampuka"], 2),
          hotbar(os.path.join(CAND, "hotbar_x4.png"), ["mc:cod", "mod:sawt", "mc:salmon", "mod:skorfna"], 4)]
    band = Image.new("RGB", (W, sum(i.height + 10 for i in hb) + 10), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    parts.append(("Hotbar preview, unselected (art/tools/hotbar_preview.py): cod, SAWT, salmon, sardina, incova, skorfna, "
                  "cerna, tropical fish, lampuka at scale 2; cod, SAWT, salmon, skorfna at 4", band))
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
    d.text((10, 8), "Sawt (lesser weever) item icon, textures/item/sawt.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)


def main():
    os.makedirs(CAND, exist_ok=True)
    icons = {}
    for v, g in GRIDS.items():
        check(g, v)
        icons[v] = render(g)
        icons[v].save(os.path.join(CAND, f"icon_{v}.png"))
    icons[CHOSEN].save(OUT_ICON)
    sheet(icons)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
