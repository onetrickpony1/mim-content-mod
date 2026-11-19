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

Night review: 8 critic rounds, all FAIL; the round 8 version was installed. The owner rejected it (2026-11-19: "too
flat and fat they dont look like the fish"; docs/Decisions/2026-11-19 Night fish icons and buckets - most pass; John
Dory, gallinella, lingwata bucket redo.md).

REDO (up to 3 critic rounds, then the owner judges): a slim body tapering diagonally from the big head (not a deep
goldfish body), more volume (a darker back and edge, light from the top left), and the wing drawn as a real fan (fan()):
teal root, rays, a bright blue rim. Round 1 FAIL (a straight belly wall, stripes, navy near the eye's row); round 2 FAIL
(belly wall, checkered fin with a navy hole, pale pixels in the eye's row, head not boxy); round 3 FAIL (no tail fin: a
blunt stub, so it read as a prawn or carrot; head too round). Round 3's tail and brow fixes are applied but were not
judged again (the round limit). Blind reads: round 1 "Red mullet", "Red fish (maybe a gurnard)", "Gurnard (a red fish
with blue wing-like fins)"; round 2 "Red fish", "Gurnard", "Red shrimp/prawn"; round 3 "Red gurnard", "Red gurnard",
"Red gurnard".

SECOND REDO (owner, 2026-11-19: "the fin looks too disconnected from the body"; docs/Decisions/2026-11-19 Redo verdicts
- lizz bucket, lionfish, lingwata Q, gallinella, John Dory.md): the body, head and forked tail kept; the wing's root now
sits on the flank just behind the head and the fan is drawn over the body (fan(..., over=...)), dark teal at the root,
paler outward with a darker ray every 30 degrees (no checker), the blue rim on the outer edge. Candidates A (the fan
spread right and down over the lower flank) and B (the root lower, the fan swept back under the belly). Round 1 PASS
(A). Its optional polish is not applied: clear (8,15) to round the fin's corner, light blue at (10,15) and (11,15) to
carry the rim along the bottom, and mid red at (10,10) to soften the outline pixel beside the fin's top. Blind reads:
"Red snapper", "red gurnard", "Gurnard (tub gurnard)".

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left.

Candidates: A (the design above), B (the wing smaller, folded closer to the body), C (A with a pale cream-salmon throat, for countershading).
CHOSEN is written to the mod.

Run:  art/.venv/bin/python art/src/fish_gallinella_icon.py
Writes mod/.../textures/item/gallinella.png (byte-identical on rerun), the candidates and the review sheet in
art/candidates/gallinella_icon/ and art/candidates/fish_gallinella_icon.png, and the offline hotbar previews.
"""
import colorsys
import math
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

# REDO (owner, 2026-11-19: "too flat and fat they dont look like the fish"; docs/Decisions/2026-11-19 Night fish icons
# and buckets - most pass; John Dory, gallinella, lingwata bucket redo.md). The night's icon (8 rounds, gave up) is kept
# as art/candidates/gallinella_icon/rejected_night.png for the side-by-side. What changed:
# - the silhouette: a big boxy head (a flat top, a steep stepped forehead, 5-6 px deep), then a body tapering steadily
#   (4, 3, 2 px) to a slim stalk and a forked tail: a gurnard's wedge, not a deep goldfish;
# - volume, not flat: a lit top-left edge, a darker red band along the back, lit and mid flank tones, a shaded lower
#   flank, a pale throat and belly, and a dark red-brown outline along the lower right;
# - the wing: a big fan spread out from behind the head, drawn from its root outward: rays alternating turquoise and
#   pale turquoise, a scalloped bright blue rim on the outer edge, a deep-blue blotch near the root.
PAL = {
    "h": hx("#f8a070"),   # the lit top-left edge
    "b": hx("#b84430"),   # the darker back band
    "n": hx("#e4644a"),   # the lit flank
    "m": hx("#e0583a"),   # the flank
    "s": hx("#c84e34"),   # the shaded lower flank
    "c": hx("#f4c0a0"),   # the pale throat and belly
    "o": hx("#8c3424"),   # the dark outline, lower right
    "d": hx("#902e20"),   # the chin's dark edge
    "E": M["E"],          # the eye: the only near-black
    "F": hx("#2f7a74"),   # the wing's root
    "G": hx("#45a090"),   # wing rays
    "g": hx("#80d4c4"),   # pale rays between
    "R": hx("#3a8ae8"),   # the bright blue rim
    "L": hx("#7cc4fa"),   # the rim's light scallops
    "B": hx("#2a4a9a"),   # the deep-blue blotch near the root
    "T": hx("#d8603c"),   # the tail
    "t": hx("#b04a30"),   # the tail's shaded base
}

# The fish without its wing: head lower left, tail upper right. The eye's row has nothing dark near the eye.
BODY = [
    # redo round 1 (critic): the belly edge stepped diagonally parallel to the back, so the body tapers from the head
    # to a 2-3 px stalk; no dark band inside the back (it read as a stripe); the nape a step above the back line; a
    # rounded chin. Round 2: no pale pixels in or near the eye's row (the belly's cream became a gill line), the dark
    # belly edge stops behind the gill where the wing's root takes over, a forehead step, a notched tail. Round 3: a
    # forked tail fan across the body line (upper lobe up-left, lower lobe down-right, a notch between) out of a 1 px
    # dark stalk, and a flat brow (one step) for the boxy head
    "...........ns...",
    "............sT..",
    "...........tTTsn",
    "..........hbo.so",
    ".........hbmo...",
    "........hnmso...",
    ".......hnnmo....",
    ".....hmnnmso....",
    "..hhhhnnnmo.....",
    "..hhhhnnmso.....",
    ".hhnEnnmsmo.....",
    ".hnnnnmsss......",
    ".hnnmmsss.......",
    "...dsssoo.......",
    "................",
    "................",
]


def fan(cx, cy, a0, a1, r, over=None, root=1.6):
    """The wing: every pixel within r of the root (cx, cy) and between the angles a0..a1 (degrees, 0 = right, 90 =
    down): the root dark teal, then rays alternating every 16 degrees, the outer ring the scalloped blue rim. Clear
    pixels are always filled; body pixels too where over(x, y) is true, so the wing lies over the flank and grows out
    of it (owner, second redo: "the fin looks too disconnected from the body"). The head (h, E) is never covered."""
    g = [list(row) for row in BODY]
    for y in range(16):
        for x in range(16):
            k0 = g[y][x]
            if k0 != "." and not (over and over(x, y) and k0 not in "hE"):
                continue
            dx, dy = x - cx, y - cy
            rr = math.hypot(dx, dy)
            a = math.degrees(math.atan2(dy, dx))
            if rr < 0.5 or (rr <= r + 0.3 and a0 <= a <= a1):
                if rr > r - 1.0:
                    k = "R" if int(a // 18) % 2 == 0 else "L"
                elif rr < root:
                    k = "F"
                elif rr < root + 1.6:
                    k = "G"
                else:   # the outer fan pale, with a darker ray every 30 degrees (no checker)
                    k = "G" if abs(((a - a0) % 30) - 15) > 11 else "g"
                g[y][x] = k
    return ["".join(row) for row in g]


GRIDS = {
    # second redo (owner: the fin looked disconnected): the wing's root sits ON the flank just behind the head and the
    # fan is drawn over the body there, so no outline or gap separates them, as on the accepted model and bucket
    # A: the root behind the gill, the fan spread out to the right and down like a wing, over the lower flank
    "A": fan(8.0, 11.0, -20, 90, 6.0, over=lambda x, y: y >= 11 and x >= 7),
    # B: the root a little lower and further forward, the fan swept back and down along the belly
    "B": fan(7.5, 11.5, 0, 105, 6.2, over=lambda x, y: (y >= 11 and x >= 7) or (y >= 12 and x >= 6)),
}


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
    assert not any(g[ey][x] in "bdoB" for x in range(max(0, ex - 4), min(16, ex + 5)) if x != ex), (
        variant, "a mark in the eye's row")
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            assert g[ey + dy][ex + dx] not in "bdoB" or (dx, dy) == (0, 0), (variant, "dark beside the eye")


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
    parts.append(("Candidates A, B at 8x, 2x, 1x", band))
    # the rejected night icon beside the chosen candidate, at 8x, 2x and 1x (a rework must show at 1x)
    band = Image.new("RGB", (W, 200), bg)
    d = ImageDraw.Draw(band)
    x = 10
    rej = Image.open(os.path.join(CAND, "rejected_night.png")).convert("RGBA")
    rej2 = Image.open(os.path.join(CAND, "rejected_redo1.png")).convert("RGBA")
    bucket = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    bucket.alpha_composite(Image.open(os.path.join(TEXTURES, "item", "gallinella_bucket.png")).convert("RGBA"))
    for n, im in (("rejected (night)", rej), ("rejected (redo 1)", rej2), (f"new {CHOSEN}", icons[CHOSEN]),
                  ("accepted bucket", bucket)):
        for sc in (8, 2, 1):
            t = Image.new("RGBA", (16 * sc + 8, 16 * sc + 8), (139, 139, 139, 255))
            t.alpha_composite(im.resize((16 * sc, 16 * sc), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x, 24))
            d.text((x, 4), f"{n} {sc}x" if sc == 8 else f"{sc}x", fill=ink, font=small)
            x += max(16 * sc + 20, 60)
        x += 40
    parts.append(("Rejected: night ('too flat and fat'), redo 1 ('the fin looks too disconnected'); the new one; the "
                  "accepted bucket", band))
    # the owner-accepted 3D model in the game, side and three-quarter, for the look and colours
    shots = [Image.open(os.path.join(ART, "candidates", "gallinella_model", f"ingame_{n}.png")).convert("RGB")
             for n in ("side", "three_quarter")]
    shots = [im.crop((im.width // 4, im.height // 4, im.width * 3 // 4, im.height * 3 // 4)).resize((640, 360))
             for im in shots]
    band = Image.new("RGB", (W, 370), bg)
    for i, im in enumerate(shots):
        band.paste(im, (10 + i * 660, 4))
    parts.append(("The accepted 3D model in the game: side, three-quarter (zoomed)", band))
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
