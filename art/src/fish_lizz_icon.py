"""Item icon for the lizz (European barracuda, Sphyraena sphyraena): the caught fish, like vanilla cod and salmon.

Night job (2026-11-18): the 3D model came first (art/src/fish_lizz_model.py) and set the palette; the icon takes the
model's colours lifted about 1.2x for out of water (the model's palette is already a step lighter for the water, so
the brightest silvers stay where they are and only the slate and grey tones lift).
Photos (reference only): art/references/fish_lizz_refonly/ (list.tsv); colour from the fresh fish out of water.

What makes it a lizz, at 1x:
- the longest, slimmest fish of the set, running corner to corner: head lower left, tail upper right, like vanilla's
  fish items;
- a long pointed head with the lower jaw jutting past the upper snout, a grey mouth line between them;
- two small dorsal fins set far apart on the back (one mid-back, one near the tail), small pale fins below;
- a dark slate back (lit at its outer edge, facing the light at the top left), silver sides with faint darker bars,
  a white belly with a soft grey rim on the shaded side;
- a dark, deeply forked tail.
No teeth and no face marks: one black eye, with no dark or bright pixel beside it in its row.

Candidates: A (the body four pixels across, slimmest), B (five across, a bright belly row), C (A with the bars
stronger and a longer jaw). The installed one is CHOSEN.

Run:  art/.venv/bin/python art/src/fish_lizz_icon.py [--sheet]
Writes mod/.../textures/item/lizz.png (byte-identical on rerun); with --sheet also art/candidates/fish_lizz_icon.png
(references, candidates at 8x, 2x and 1x beside vanilla and accepted fish, measure.py numbers) and the offline hotbar
previews art/candidates/fish_lizz_icon_hotbar_<cand>.png.
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

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "lizz.png")
CAND_DIR = os.path.join(ART, "candidates")
OUT_SHEET = os.path.join(CAND_DIR, "fish_lizz_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_lizz_refonly")
CHOSEN = "C"


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lift(c, k=1.2):
    """The model's colour lifted for out of water: brightness x k (capped), hue and saturation kept."""
    h, s, v = colorsys.rgb_to_hsv(*(x / 255.0 for x in c))
    r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, v * k))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


# The model's palette (art/src/fish_lizz_model.py PAL), copied by value so this file stands alone.
MODEL = {
    "K": "#3c5662", "B": "#597582", "b": "#4b646f", "G": "#9bb0b9", "g": "#80959c", "S": "#deeaee",
    "W": "#f9ffff", "M": "#748186", "J": "#bac7cb", "D": "#6b7e85", "d": "#4f6067", "F": "#ccd0c1",
    "f": "#abb0a6", "T": "#63726f", "t": "#475254",
}
PAL = {k: lift(hx(v)) for k, v in MODEL.items()}
# Round 2 palette (critic: light the top-left back, dark outline at the lower right, a cool slate tail). The slate and
# grey tones are the model's lifted about 1.2x; the silvers and white are the model's, already at the top.
PAL.update({k: hx(v) for k, v in {
    "h": "#86a3ae", "B": "#4f6b77", "b": "#3d5560", "S": "#c4d0d4", "g": "#a3b2b8", "W": "#eef3f2", "s": "#dde5e7",
    "o": "#46545b", "e": "#0b0d0e", "M": "#6c7a80", "J": "#b4c0c4", "D": "#5d7884", "d": "#86a3ae",
    "U": "#8aa2b0", "T": "#607888", "t": "#445866", "F": "#9aa6aa", "f": "#7a868b"}.items()})


# Round 2 (critic round 1: FAIL, "a syringe or sword blade"; blind reads: a sword, a needlefish, a fishing rod).
# Head lower left, tail upper right. The body is a spindle, five pixels across at the head and tail and six in the
# middle (rows 6-9), with the light on the back: a lit slate edge (h) at the top left, the slate back (B, with faint
# bars b), silver (S, bars g), the white belly (W) kept one pixel inside, a light silver (s) and a dark grey outline (o)
# all along the shaded lower right, so no white touches the edge.
# The head: one black eye (2,12) ringed by the lit edge and silver; the upper snout ends at 0,14 (B) over a mid-grey
# mouth pixel (M, 1,14), and the silver lower jaw (J, 0,15) juts one pixel further.
# Fins: a small spiny dorsal mid-back (5,6-7), a second one far back (8-9,3), well apart; two-pixel shaded pelvic
# (8,10-11) and anal (13,6-7) fins on the belly outline. The tail: a short stalk (10-11,2-3), its root lit (U), and two
# tapering lobes two pixels thick, up (10-11,0-1) and right (12-15,3-4), cool slate like the body, darker at the tips.
GRIDS = {
    "A": [
        "..........tt....",
        "..........TT....",
        "..........UT....",
        "........dDUTTTtt",
        ".........hbSoTtt",
        "........hBSso...",
        ".....d.hbgWsoF..",
        ".....DhBSWso.f..",
        ".....hBSWso.....",
        "....hbgWso......",
        "...hBSWoF.......",
        "..hBSso.f.......",
        ".heSso..........",
        "hSso............",
        "BMo.............",
        "Jo..............",
    ],
    # B: A with the two dorsal fins a pixel taller
    "B": [
        "..........tt....",
        "..........TT....",
        "..........UT....",
        ".......ddDUTTTtt",
        ".........hbSoTtt",
        "....d...hBSso...",
        "....dd.hbgWsoF..",
        "....dDhBSWso.f..",
        ".....hBSWso.....",
        "....hbgWso......",
        "...hBSWoF.......",
        "..hBSso.f.......",
        ".heSso..........",
        "hSso............",
        "BMo.............",
        "Jo..............",
    ],
    # C: A with a fuller, fan-shaped tail
    "C": [
        ".........ttt....",
        "..........TTt...",
        "..........UTT..t",
        "........dDUTTTTt",
        ".........hbSoTtt",
        "........hBSso...",
        ".....d.hbgWsoF..",
        ".....DhBSWso.f..",
        ".....hBSWso.....",
        "....hbgWso......",
        "...hBSWoF.......",
        "..hBSso.f.......",
        ".heSso..........",
        "hSso............",
        "BMo.............",
        "Jo..............",
    ],
}


def grid(cand):
    return GRIDS[cand]


def render(rows):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


def check(rows):
    """Stray pixels (no opaque 4-neighbour) and anything dark beside the eye in its row."""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and rows[y + dy][x + dx] != "."
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                print(f"warning: stray pixel at {x},{y}")
            if ch == "e":
                for dx in (-2, -1, 1, 2):
                    if 0 <= x + dx < 16 and row[x + dx] in "ekd":
                        print(f"warning: dark pixel beside the eye at {x + dx},{y}")


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


def sheet(cands):
    from font import label_font
    font, small = label_font(16), label_font(13)
    W = 1800
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    refs = []
    for name in ("side.jpg", "barracuda.jpg", "fmib.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im.thumbnail((560, 180))
            refs.append(im)
    if refs:
        band = Image.new("RGB", (W, 190), bg)
        x = 10
        for im in refs:
            band.paste(im, (x, 5))
            x += im.width + 10
        parts.append(("References (reference only): fresh European barracuda out of water, the d'Orbigny plate", band))

    items = [("cand " + c + (" (installed)" if c == CHOSEN else ""), im) for c, im in cands.items()]
    for n in ("cod", "salmon"):
        items.append(("vanilla " + n, Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")))
    for n in ("pixxispad", "incova", "huta_kahla", "sardina"):
        p = os.path.join(TEXTURES, "item", n + ".png")
        if os.path.exists(p):
            items.append((n + " (accepted)", Image.open(p).convert("RGBA")))
    band = Image.new("RGB", (W, 2 * 200), bg)
    d = ImageDraw.Draw(band)
    for i, (n, im) in enumerate(items):
        x0, y0 = 10 + (i % 5) * 350, 22 + (i // 5) * 200
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(tile.convert("RGB"), (x0, y0))
        for j, (col, sc) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
            t = Image.new("RGBA", (16 * sc + 8, 16 * sc + 8), col + (255,))
            t.alpha_composite(im.resize((16 * sc, 16 * sc), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x0 + 136 + (j % 2) * 44, y0 + (j // 2) * 46))
        d.text((x0, y0 - 18), n, fill=ink, font=small)
    parts.append(("Candidates at 8x, then 1x and 2x on light and dark grey, beside vanilla and accepted long fish", band))

    tmp = []
    for c, im in cands.items():
        p = os.path.join(CAND_DIR, "tmp_lizz_icon_%s.png" % c)
        im.save(p)
        tmp.append(p)
    lines = measure(tmp + [os.path.join(VANILLA, "cod.png"), os.path.join(VANILLA, "salmon.png")])
    for p in tmp:
        os.remove(p)
    band = Image.new("RGB", (W, 22 * len(lines) + 10), bg)
    d = ImageDraw.Draw(band)
    for i, ln in enumerate(lines):
        d.text((10, 4 + 22 * i), ln, fill=ink, font=small)
    parts.append(("art/tools/measure.py", band))

    H = sum(28 + b.height for _, b in parts)
    out = Image.new("RGB", (W, H), bg)
    y = 0
    d = ImageDraw.Draw(out)
    for t, b in parts:
        d.text((10, y + 5), t, fill=ink, font=font)
        out.paste(b, (0, y + 28))
        y += 28 + b.height
    out.save(OUT_SHEET)
    print("sheet:", OUT_SHEET)


def main():
    cands = {}
    for c in ("A", "B", "C"):
        rows = grid(c)
        check(rows)
        cands[c] = render(rows)
    os.makedirs(os.path.dirname(OUT_ICON), exist_ok=True)
    cands[CHOSEN].save(OUT_ICON)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "(candidate %s)" % CHOSEN)
    if "--sheet" in sys.argv[1:]:
        sheet(cands)
        py = os.path.join(ART, ".venv", "bin", "python")
        for c, im in cands.items():
            p = os.path.join(CAND_DIR, "lizz_icon_%s.png" % c)
            im.save(p)
            subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"),
                            os.path.join(CAND_DIR, "fish_lizz_icon_hotbar_%s.png" % c),
                            "mc:cod", "file:" + p, "mc:salmon", "mod:pixxispad", "mc:tropical_fish", "--scale", "4"],
                           check=True, capture_output=True)
            os.remove(p)


if __name__ == "__main__":
    main()
