"""Item icon for the hmar (grey triggerfish, Balistes capriscus): the caught fish, like vanilla cod and salmon.

Night job piece 2 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). It follows the
critic-passed 3D model (art/src/fish_hmar_model.py, palette A): the same keys, each colour lifted about x1.2 for out
of water, keeping its hue. Photos (reference only): art/references/fish_hmar_refonly/ (list.tsv).

What makes it a hmar at 16 x 16:
- a deep diamond of a body, as deep as it is half long: a long straight forehead sloping down to a small mouth, the
  belly dropping to a point under the trigger, straight lines from there back to a short stalk;
- olive-grey, darker on the back with faint darker saddles, pale cream-grey on the belly;
- one black eye set high and far back from the mouth, with plain grey round it (nothing dark near it, no mouth line
  in its row, so eye and mouth can't make a face);
- the trigger: one stout dark spine standing up from the back's highest point;
- long matching soft dorsal and anal fins along the back half, ending at the stalk;
- a lyre tail: a short fan and two pointed tips.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left.

The body is drawn along the diagonal: each pixel's centre is measured along the fish (a, from the lips to the tail)
and across it (b, toward the back is +), and the outline (top and bottom of the body against a) decides what it is.
Tones come from how far across the body a pixel sits; then the edges are shaded (lit on the top left, a dark rim on
the bottom right), the eye and mouth are placed, and FIXES patches single pixels.

Candidates: A (the design above), B (the soft fins a pixel longer, the saddles a step darker), C (a slimmer body, a
pixel less deep). CHOSEN is written to the mod.

Run:  art/.venv/bin/python art/src/fish_hmar_icon.py
Writes mod/.../textures/item/hmar.png (byte-identical on rerun), the candidates and the review sheet in
art/candidates/hmar_icon/ and art/candidates/fish_hmar_icon.png, and the offline hotbar previews.
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
import fish_hmar_model as model  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "hmar.png")
CAND = os.path.join(ART, "candidates", "hmar_icon")
OUT_SHEET = os.path.join(ART, "candidates", "fish_hmar_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
CHOSEN = "A"  # round 1 (critic): C's tail on every candidate


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lift(c, k=1.2):
    """Out of water: brightness x1.2, hue and saturation kept."""
    h, s, v = colorsys.rgb_to_hsv(*(x / 255.0 for x in c))
    return tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb(h, s, min(1.0, v * k)))


MODEL = {k: hx(v) for k, v in model.PALETTES["A"].items()}
# Round 0 (maker): lifted x1.2 the whole fish read white at 1x (inside lightness 0.74, vanilla cod 0.59), so the body
# keeps the model's own tones (already a step lighter than the photos, for the water) and only the fins and tail are
# lifted, a little; the belly comes down a step from the model's near-white.
PAL = dict(MODEL)
# the fins and tail: out of water they are olive-grey like the body (the model's pale fins, made to show in the
# water, read as glowing spikes at 1x); the trailing edge (f) a step paler
PAL.update({"F": hx("#8a8671"), "f": hx("#a19d87"), "U": hx("#827e6a"), "V": hx("#75715e")})
PAL["w"] = hx("#cdc8b4")
PAL["W"] = hx("#d8d3c0")
PAL["h"] = hx("#a6a38b")                   # candidate C: the lit sheen on the back's top edge
PAL["H"] = hx("#5d5b49")                   # the outline along the back and forehead (top left)
PAL["o"] = hx("#3f3d31")                   # the dark rim in the shade (bottom right), olive like the body
PAL["O"] = hx("#58564a")                   # the tail's rim
PAL["b"] = hx("#b4af9b")                   # the belly in the shade, above the rim
PAL["X"] = hx("#5f5d4c")                   # darker saddle (candidate B)
# Round 1 (critic: the palest, most washed-out fish in the hotbar): the whole fish about 10 % darker and a touch
# greener (olive-grey).
for _k in list(PAL):
    if _k != "E":
        _r, _g, _b = PAL[_k]
        PAL[_k] = (int(round(_r * 0.88)), int(round(_g * 0.91)), int(round(_b * 0.86)))
# round 1 patch tones (the critic's, then darkened with the rest): blotches q and n, the belly fading out p, the lit
# crown L, the shaded rear of the anal fin a, the back outline one step darker D
PAL.update({"q": (114, 115, 91), "n": (136, 138, 111), "p": (150, 151, 125), "L": (160, 160, 134),
            "a": (77, 78, 64), "D": (72, 72, 58)})
# round 2 (critic): a darker olive edge on the fins' outer edges and the tail tips, the blotches a tone darker
PAL.update({"Z": (62, 62, 49), "q": (104, 105, 83)})
# round 2: 22 colours, over vanilla's 20; the near-duplicate tones share one colour
PAL["W"] = PAL["w"]
PAL["b"] = PAL["p"]
PAL["a"] = PAL["Z"]
PAL["E"] = MODEL["E"]

# The pose. A diamond turned 45 degrees becomes a square blob (tried first: the forehead and the back came out as a
# vertical and a horizontal wall), so the body shape says otherwise and the hmar lies side on, head left, as the
# critic-passed model's own side view: one icon pixel per model pixel (x = z + 8, y = model y - 7).
def side_grid(variant):
    g = [["."] * 16 for _ in range(16)]
    for z, top, bot, _ in model.COLUMNS:
        for y in range(top, bot + 1):
            k = model.side_key("A", z, y)
            g[y - 7][z + 8] = k
    for rows, z0 in ((model.DORSAL, 0), (model.ANAL, 0)):
        for y, r in rows.items():
            for i, ch in enumerate(r):
                if ch != ".":
                    g[y - 7][z0 + i + 8] = ch
    for x, y in ((5, 3), (5, 4), (6, 2), (6, 3), (6, 4)):
        g[y][x] = "T"                               # the trigger, raked back
    g[4][7] = "f"                                   # its membrane
    for y, r in TAIL[variant].items():
        for i, ch in enumerate(r):
            if ch != ".":
                g[y][13 + i] = ch
    return g


# The lyre tail, columns x 13..15: a fan on the stalk, the rear edge curved in, pointed tips up and down.
TAIL = {
    # round 1 (critic): the tips a pixel longer outward on every candidate (C's first tail)
    "C": {3: "..V", 4: "..V", 5: ".VV", 6: "UV.", 7: "UU.", 8: "UU.", 9: "UU.", 10: "UV.", 11: ".VV", 12: "..V",
          13: "..V"},
}
TAIL["A"] = TAIL["B"] = TAIL["C"]
# round 1 (critic): the eye up and back, so the snout is long
EYE = {v: (5, 6) for v in "ABC"}
# Round 1 patches, after the edges are shaded: (x, y, key).
_COMMON = [
    (4, 7, "n"), (5, 7, "c"),                     # where the eye was: mid tone; a light pixel under the new eye
    (5, 5, "L"), (6, 5, "L"), (7, 6, "L"),        # the crown lit from the top left
    (3, 7, "D"),                                  # the forehead outline a step darker (not beside the eye)
    (5, 6, "E"),
    (5, 4, "F"),                                  # the trigger a thin dark spine, not a 2 x 2 block
    (9, 10, "p"), (10, 10, "p"),                  # the pale belly fades out toward the back
    (7, 11, "w"),                                 # no dark hole in the belly
    (10, 12, "a"), (10, 13, "a"), (11, 12, "a"),  # the anal fin's rear in the shade
    (10, 11, "f"), (11, 11, "F"),
]
# Round 2 (critic): light from the top left (TL-BR was -0.03), a darker edge round the fins and tail, the pale belly
# split into a bright chin and a greyer rear with its lower edge stepping up, a pale ring beside the eye, the lower
# jaw in the snout's tone with one darker pixel for the mouth, and fewer, darker blotches.
_COMMON += [
    (6, 6, "c"), (7, 5, "m"),                                   # the eye's pale ring; no blotch near it
    (4, 5, "."), (4, 6, "L"), (3, 7, "H"),                      # the forehead lit
    (8, 3, "Z"), (9, 4, "Z"), (10, 4, "Z"), (11, 5, "Z"), (12, 6, "Z"),   # the soft dorsal's outer edge
    (8, 14, "Z"), (9, 13, "Z"), (10, 13, "Z"),                  # the anal fin's outer edge
    (15, 3, "Z"), (15, 4, "Z"), (15, 12, "Z"), (15, 13, "Z"),   # the tail tips
    (9, 10, "n"), (10, 10, "n"), (11, 10, "a"), (12, 10, "F"),  # the rear lower body and anal fin base in the shade
    (9, 11, "p"), (10, 11, "a"), (11, 11, "a"),
    (5, 10, "W"), (6, 10, "w"), (7, 10, "b"), (8, 10, "p"),     # the belly: bright chin, greyer rear
    (7, 11, "b"), (8, 11, "p"),
    (1, 9, "j"), (3, 10, "g"), (4, 10, "g"), (2, 9, "c"),       # the mouth one dark pixel; the lower jaw snout grey
]
FIXES = {
    "A": _COMMON + [(8, 8, "q"), (11, 8, "q")],                                     # two soft blotches
    "B": _COMMON + [(7, 8, "q"), (8, 9, "n"), (10, 8, "q"), (11, 9, "n")],           # two bands, each two pixels
    "C": _COMMON + [(6, 8, "q"), (6, 9, "n"), (9, 8, "q"), (9, 9, "n"), (11, 8, "n")],  # three bands down the flank
}


def finish(g, variant):
    """Shade the edges: an edge facing up or left keeps its tone (the back is already the darkest band), except that
    candidate C gives the back's top edge a lit sheen; an edge facing down or right becomes the dark rim, as vanilla
    fish items have."""
    out = [row[:] for row in g]
    for y in range(16):
        for x in range(16):
            k = g[y][x]
            if k in ".TE":
                continue

            def empty(dx, dy):
                return not (0 <= x + dx < 16 and 0 <= y + dy < 16) or g[y + dy][x + dx] == "."
            body = k in "wWsgcmkKHXlj"
            if body and (empty(0, 1) or empty(1, 0)):
                out[y][x] = "o"
            elif not body and empty(0, 1) and not empty(0, -1) and k in "UV":
                out[y][x] = "O"                     # the tail's lower edges in the shade
            elif body and (empty(0, -1) or empty(-1, 0)):
                # the top-left edge: the outline, but C puts a lit sheen on the back behind the head
                out[y][x] = "h" if variant == "C" and x >= 5 else "H"
            elif k == "w" and not empty(0, 1) and g[y + 1][x] == "o":
                out[y][x] = "b"
    for x, y, k in FIXES[variant]:
        out[y][x] = k
    return out


def render(g):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(g):
        for x, k in enumerate(row):
            if k != ".":
                im.putpixel((x, y), PAL[k] + (255,))
    return im


def check(g, variant):
    """No stray pixels, nothing dark beside the eye, the eye the only near-black pixel."""
    for y in range(16):
        for x in range(16):
            if g[y][x] == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and g[y + dy][x + dx] != "."
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                raise AssertionError(f"{variant}: stray pixel at {x},{y}")
    ex, ey = EYE[variant]
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if (dx, dy) != (0, 0):
                assert g[ey + dy][ex + dx] not in "ETkXojDqa", (variant, "dark beside the eye", ex + dx, ey + dy)
    # nothing else as dark as the eye in its row
    assert all(k not in "ETXo" for i, k in enumerate(g[ey]) if i != ex and i < 12), (variant, "dark mark in the eye's row")
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
    names = [("cod", os.path.join(VANILLA, "cod.png")), ("tropical", os.path.join(VANILLA, "tropical_fish.png"))]
    names += [(n, os.path.join(TEXTURES, "item", n + ".png")) for n in ("cawl", "cerna", "awrata")]
    band = Image.new("RGB", (W, 170), bg)
    d = ImageDraw.Draw(band)
    for i, (n, p) in enumerate([("HMAR", None)] + names):
        im = icons[CHOSEN] if p is None else Image.open(p).convert("RGBA")
        t = Image.new("RGBA", (136, 136), (139, 139, 139, 255))
        t.alpha_composite(im.resize((128, 128), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (10 + i * 150, 24))
        d.text((10 + i * 150, 4), n, fill=ink, font=small)
    parts.append(("The chosen icon at 8x beside vanilla cod and tropical fish and the accepted cawl, cerna, awrata",
                  band))
    hb = [hotbar(os.path.join(CAND, "hotbar.png"), ["mc:cod", "mod:hmar", "mc:salmon", "mod:cawl", "mod:cerna",
                                                      "mod:awrata", "mc:tropical_fish", "mc:pufferfish", "mod:kavall"], 2),
          hotbar(os.path.join(CAND, "hotbar_x4.png"), ["mc:cod", "mod:hmar", "mc:tropical_fish", "mod:cerna"], 4)]
    band = Image.new("RGB", (W, sum(i.height + 10 for i in hb) + 10), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    parts.append(("Hotbar preview, unselected (art/tools/hotbar_preview.py): cod, HMAR, salmon, cawl, cerna, awrata, "
                  "tropical fish, pufferfish, kavall at scale 2; cod, HMAR, tropical fish, cerna at 4", band))
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
    d.text((10, 8), "Hmar (grey triggerfish) item icon, textures/item/hmar.png", fill=ink, font=label_font(20))
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
        g = finish(side_grid(v), v)
        print(v)
        print("\n".join("".join(r) for r in g))
        check(g, v)
        icons[v] = render(g)
        icons[v].save(os.path.join(CAND, f"icon_{v}.png"))
    icons[CHOSEN].save(OUT_ICON)
    if "--no-sheet" not in sys.argv:
        sheet(icons)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
