"""Item icon for the gallinella (tub gurnard, Chelidonichthys lucerna): the caught fish, like vanilla cod and salmon.

Night job piece 2 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). It follows the
critic-passed 3D model (art/src/fish_gallinella_model.py, palette A): the same keys and hues, out of water. The model's
palette is already a step lighter than the photos (for the water), so most tones are used as they are and only the fins
are lifted (x1.1). Photos (reference only): art/references/fish_gallinella_refonly/ (list.tsv).

What makes it a gurnard at 16 x 16, and not the trilja (slim pink mullet) or the marzpan (deep red parrotfish):
- a big boxy head at the lower left, the deepest part of the fish, with a steep forehead and the eye high on it;
- a red-orange back with a few red-brown mottles, a salmon flank and a pale cream belly, tapering to a slim stalk;
- the huge pectoral "wing" spread out under the body behind the head: a turquoise fan with a bright blue rim and a
  mid-blue blotch at its inner rear (never as dark as the eye, never in the eye's row);
- a low spiny dorsal behind the head and a squared orange tail at the upper right.
The finger rays are left out, as on the model (they read as legs).

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left.

Candidates: A (the design above), B (the wing smaller, folded closer to the body), C (A with a pale cream-salmon throat, for countershading).
CHOSEN is written to the mod.

Run:  art/.venv/bin/python art/src/fish_gallinella_icon.py
Writes mod/.../textures/item/gallinella.png (byte-identical on rerun), the candidates and the review sheet in
art/candidates/gallinella_icon/ and art/candidates/fish_gallinella_icon.png, and the offline hotbar previews.
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
import fish_gallinella_model as model  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "gallinella.png")
CAND = os.path.join(ART, "candidates", "gallinella_icon")
OUT_SHEET = os.path.join(ART, "candidates", "fish_gallinella_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
CHOSEN = "A"


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lift(c, k=1.1):
    h, s, v = colorsys.rgb_to_hsv(*(x / 255.0 for x in c))
    return tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb(h, s, min(1.0, v * k)))


M = {k: hx(v) for k, v in model.PALETTES["A"].items()}
PAL = {
    # the body: the model's ramp (0 belly .. 5 darkest back)
    "h": M["3"],            # the lit edge of the back
    "m": M["4"],            # the back
    "k": M["B"],            # red-brown mottles on the back, well behind the eye
    "g": M["2"],            # the salmon flank
    "w": M["0"],            # the cream belly
    "c": M["1"],            # the pale lower flank
    "o": hx("#d8a080"),     # the belly's shaded rim (bottom right, away from the light)
    "H": M["4"],            # the bony head
    "J": M["5"],            # the head's shaded front and lower edge
    "j": hx("#c0583a"),     # the mouth line, under the snout
    "E": M["E"],            # the eye: the only near-black
    # fins: the model's colours, lifted x1.1
    "F": lift(M["F"]), "G": lift(M["G"]), "R": lift(M["R"]), "L": lift(M["L"]), "D": lift(M["D"]), "d": lift(M["d"]),
    "q": M["q"], "Q": M["Q"], "T": lift(M["T"]), "t": M["t"],
}
# round 0 (measured): lifted, the wing was the brightest part at the lower right (light from the wrong side, TL-BR
# -0.20) and nothing outlined the fish (edge 0.66 against vanilla's 0.26-0.42). The wing keeps the model's hues but
# darker, the rim a deep blue, and the belly and tail rims a shaded red-brown. Light from the top left wins over
# countershading on an icon (as on vanilla cod): the back's lit edge light, the lower flank a shaded salmon, the cream
# only at the throat (lower left).
PAL.update({"F": hx("#3f8e86"), "G": hx("#62b0a2"), "R": hx("#2f7cd0"), "L": hx("#5aaef0"), "D": hx("#3a64a8"),
            "d": hx("#5a88cc"), "o": hx("#b0603e"), "h": hx("#ffc090"), "w": hx("#fde0c4"), "c": hx("#eea07a"), "m": hx("#f4864c"),
            "g": hx("#e8845a"), "H": hx("#f4844a"),
            "t": hx("#d0643c"), "T": hx("#f08a50"), "J": hx("#c4502e"),
            "f": hx("#2f7a74"),   # the darker rays
            # round 2: a redder body, a lit back band, a mid shadow, a dark rim
            "m": hx("#ec7446"), "H": hx("#ec7446"), "h": hx("#faa069"), "s": hx("#d6683e"), "d": hx("#b0603e"),
            "J": hx("#c0583a"), "l": hx("#f48856"), "t": hx("#c05a3a"), "T": hx("#d0643c"), "R": hx("#5aaef0"), "D": hx("#2f7cd0"),
            "q": hx("#b0603e")})   # the dorsal spines in the belly rim's red-brown (20 colours at most)

GRIDS = {
    # round 2 (critic: read as a dragon head; blind: "shrimp"): a longer body pinched to a narrow stalk before a two-lobed
    # fan tail in a darker red-orange; no spikes standing off the back; one dark stepped edge under the head; a lit back
    # band, a mid shadow on the lower flank; the fin rooted behind the head, fanning down and right in diagonal rays to a
    # continuous bright blue rim, with a 2 px deep-blue blotch inside. Round 3: no dark mottles on the back (one read as
    # a brow by the eye); the fin rooted on the flank behind the head, the blotch a band away from a stepped rim
    "A": [
        "................",
        "...........TT...",
        "...........tTT..",
        "..........hdtTT.",
        ".........hmd.tT.",
        "........hhd.....",
        "......shmmmsd...",
        ".....hhhmsmsd...",
        "...hmmmlmmsd....",
        "..hHHEHmmmsd....",
        "..hHHHHmmssd....",
        ".hHHHHsmssdF....",
        ".hHHHmsFfGGGR...",
        "..JJmssdFDDGGR..",
        "......FfGGGRRR..",
        "........RRR.....",
    ],
    # B: the same fish with the wing folded smaller, nearer the body
    "B": [
        "................",
        "............TTT.",
        "...........tTTT.",
        "..........htTT..",
        ".......q.hmgTT..",
        "......qQhmmgo...",
        ".....hhmmkmgo...",
        "....hhmmmmggo...",
        "...hHHmmkmgco...",
        "..hHEHmmmgcco...",
        ".hHHHHmggcco....",
        ".HHHHHggccoo....",
        ".jHHggcoFfGR....",
        "..jcco.fGdGR....",
        ".......RLRL.....",
        "................",
    ],
}
GRIDS["C"] = [row.replace("..JJm", "..Jcc") if i == 13 else row for i, row in enumerate(GRIDS["A"])]   # C: a pale throat


def render(g):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(g):
        assert len(row) == 16, (y, row)
        for x, k in enumerate(row):
            if k != ".":
                im.putpixel((x, y), PAL[k] + (255,))
    return im


def check(g, variant):
    """No stray pixels (each opaque pixel has an opaque 4-neighbour); nothing dark or blue in the eye's row or beside
    the eye; the eye the only near-black."""
    for y in range(16):
        for x in range(16):
            if g[y][x] == ".":
                continue
            assert any(0 <= x + dx < 16 and 0 <= y + dy < 16 and g[y + dy][x + dx] != "."
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), (variant, "stray pixel", x, y)
    ey, ex = next((y, x) for y in range(16) for x in range(16) if g[y][x] == "E")
    assert sum(r.count("E") for r in g) == 1
    # no mark in the eye's row within 4 px of it (the belly's dark rim at the far end of the row is the outline)
    assert not any(g[ey][x] in "kDdjJ" for x in range(max(0, ex - 4), min(16, ex + 5)) if x != ex), (
        variant, "a mark in the eye's row")
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            assert g[ey + dy][ex + dx] not in "kDdjJ" or (dx, dy) == (0, 0), (variant, "dark beside the eye")


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
    names += [(n, os.path.join(TEXTURES, "item", n + ".png")) for n in ("trilja", "marzpan", "skorfna", "cerna")]
    band = Image.new("RGB", (W, 170), bg)
    d = ImageDraw.Draw(band)
    for i, (n, p) in enumerate([("GALLINELLA", None)] + names):
        im = icons[CHOSEN] if p is None else Image.open(p).convert("RGBA")
        t = Image.new("RGBA", (136, 136), (139, 139, 139, 255))
        t.alpha_composite(im.resize((128, 128), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (10 + i * 150, 24))
        d.text((10 + i * 150, 4), n, fill=ink, font=small)
    parts.append(("The chosen icon at 8x beside vanilla cod and salmon, the trilja and marzpan (the other red fish), the "
                  "skorfna and cerna", band))
    chosen = os.path.join(CAND, f"icon_{CHOSEN}.png")
    hb = [hotbar(os.path.join(CAND, "hotbar.png"), ["mc:cod", "file:" + chosen, "mc:salmon", "mod:trilja", "mod:marzpan",
                                                      "mod:skorfna", "mod:cerna", "mc:tropical_fish", "mod:lampuka"], 2),
          hotbar(os.path.join(CAND, "hotbar_x4.png"), ["mc:cod", "file:" + chosen, "mod:trilja", "mod:marzpan"], 4)]
    band = Image.new("RGB", (W, sum(i.height + 10 for i in hb) + 10), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    parts.append(("Hotbar preview, unselected (art/tools/hotbar_preview.py): cod, GALLINELLA, salmon, trilja, marzpan, "
                  "skorfna, cerna, tropical fish, lampuka at scale 2; cod, GALLINELLA, trilja, marzpan at 4", band))
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
    d.text((10, 8), "Gallinella (tub gurnard) item icon, textures/item/gallinella.png", fill=ink, font=label_font(20))
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
