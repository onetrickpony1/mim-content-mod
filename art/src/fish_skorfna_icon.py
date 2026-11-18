"""Item icon for the skorfna (scorpionfish): the caught fish, like vanilla cod and salmon.

The skorfna has two skins on one approved model (owner 2026-11-18, "skorfna approved"): the black scorpionfish
(Scorpaena porcus, Skorfna sewda), the default, and the red one (S. scrofa, Ċippullazza). Both drop the same item,
so the icon shows the black one. The model came first, so the icon follows it: same features, and the model's
black palette before its in-game lift (fish_skorfna_model.py keeps PALETTES["black"] and lifts it x1.18 for the
water; an icon sits about x1.2 darker than its model, so the icon uses the unlifted values as they are).

What makes it a scorpionfish at 16 px (model shots in art/candidates/fish_skorfna_model/round4/, photos in
art/references/fish_skorfna_refonly/, list.tsv):
- a big head, a third of the length (columns 0-4 of the 15), lighter than the body, with a wide downturned mouth: a
  2 px dark gape running back from the lip (in this pose "back and down" is to the right), over a pale jutting chin;
- one eye, high on the head (2,9), with nothing dark in its row near it and no cirrus (a dark flap over the eye
  read as a second eye on the model);
- one tall spiny dorsal from over the gill cover to the stalk: dark spine tips standing 1 px proud of a brown
  membrane that joins them, tallest at the front (4 px over the back) and lowest at the rear (1 px);
- a big fan pectoral behind the head: pale rays fanning back and down from the flank, with a dark rim that breaks
  out of the belly line;
- a body that tapers behind the head to a slim stalk (not ball-like: longer than the cerna, 28 against 26 along the
  axis, and only 4 px deep without its fins), mottled dark brown with dark saddles and red-brown patches (2 px,
  never lone dots), and a pale belly;
- a rounded tail fan with a dark band across it.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left: a lit rim along the back under the dorsal and over the head, the belly side
darker at the rim.

Run:  art/.venv/bin/python art/src/fish_skorfna_icon.py
Writes mod/.../textures/item/skorfna.png (byte-identical on rerun), art/candidates/fish_skorfna_icon.png (compare
sheet: candidates at 8x, 1x and 2x beside vanilla and the accepted fish, the model shots, the references) and the
offline hotbar previews art/candidates/fish_skorfna_icon_hotbar*.png (no slot selected).
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(ART, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ART, "tools"))
from font import label_font  # noqa: E402
from fish_skorfna_model import PALETTES  # noqa: E402  (the approved model's colours, before the water lift)

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "skorfna.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_skorfna_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_skorfna_refonly")
SHOTS = os.path.join(ART, "candidates", "fish_skorfna_model", "round4")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def palette(variant):
    """The model's palette for one skin, by the model's own keys, plus two aliases for the icon's outline."""
    p = {k: hx(v) for k, v in PALETTES[variant].items()}
    p["h"] = p["C"]   # the lit rim along the back and over the head (the model's lighter flaps)
    p["o"] = p["B"]   # the shaded rim on the belly side and under the chin (the model's darkest blotch)
    return p


PAL = palette("black")
# Keys used: body ramp 0 (pale belly) J (belly shade, chin) h (lit rim) 1 2 3 4 (mid to dark), blotches B (dark
# saddle) R (red-brown), o (shaded rim), E (eye), M (the gape), fins S (spine tips) D (dark band, rim) F (membrane)
# f (shaded membrane) r (pale rays).

# A: the proposal. Columns 0-4 are the head: the snout front steps 0,11-13 / 1,9-14 / 2,8-14 / 3,7-14, the lip 0,12
# in the body's light tone, the gape M at 1-2,12 running back from it, the pale chin J at 0-2,13 jutting under it,
# the eye at 2,9 inside the lit rim (h 1,9 2,8). Behind the head the belly rises a pixel a column (13, 12, 11, 10,
# 9, 8, 7, 5) while the back rises every other column, so the body tapers to the stalk at 11,3-5. The dorsal spine
# tips S at 3,3 5,3 7,2 9,2 stand 1 px over the membrane F (4,4 6,4 8,3 10,3), each spine dark (D) one pixel down,
# the membrane shaded (f) at its base. The pectoral fans out from 5-6,10: pale rays r, lit h, rimmed with D at
# 9,10 8,11 6-7,12, so it sticks out of the belly line. Dark saddles B at 9-10,5 6-7,7 9,6 and red-brown R at 8,7 7,8.
# The tail fan rounds off at the top right with a dark band (12,1 13,2 14,3) across it.
SKORFNA_A = [
    ".............rF.",
    "............DrFF",
    ".......S.S..FDFf",
    "...S.S.DFfF2fFD.",
    "...DFDFffh13.f..",
    "...FFffhhBBo....",
    "...ffhh12B3.....",
    "...hh2BBR4o.....",
    "..h1233R4o......",
    ".hE123rhf.......",
    ".h122rrhFD......",
    "h12200rFD.......",
    "1MM00JDD........",
    "JJJ0o...........",
    ".ooo............",
    "................",
]

# B: A with the first spine a pixel taller (3,2), so the dorsal is clearly tallest at the front, and a bigger fan
# that reaches a pixel further below the belly (8-9,11 7-8,12).
SKORFNA_B = [
    ".............rF.",
    "............DrFF",
    "...S...S.S..FDFf",
    "...D.S.DFfF2fFD.",
    "...DFDFffh13.f..",
    "...FFffhhBBo....",
    "...ffhh12B3.....",
    "...hh2BBR4o.....",
    "..h1233R4o......",
    ".hE123rhf.......",
    ".h122rrhhD......",
    "h12200rhFD......",
    "1MM00JFDD.......",
    "JJJ0o...........",
    ".ooo............",
    "................",
]

# C: A, warmer: more red-brown mottling on the flank (7-8,6 5,7), as on the black skin's patches.
SKORFNA_C = [
    ".............rF.",
    "............DrFF",
    ".......S.S..FDFf",
    "...S.S.DFfF2fFD.",
    "...DFDFffh13.f..",
    "...FFffhhBBo....",
    "...ffhhRRB3.....",
    "...hhRBBR4o.....",
    "..h1233R4o......",
    ".hE123rhf.......",
    ".h122rrhFD......",
    "h12200rFD.......",
    "1MM00JDD........",
    "JJJ0o...........",
    ".ooo............",
    "................",
]

# D (round 2, the proposal): B with the critic's fixes (round 1: FAIL; one blind reader saw the head and tail
# swapped and the three candidates could not be told apart):
# - a bulkier, blunter head that is the lightest mass: 0,10 h, 0,11 1, 1,11 h, 3,8 h;
# - the gape steps down to the right (M 1,12 then 2,13: downturned), and the chin rim is 2 px (2-3,14), so the head
#   end no longer stacks dark-pale-dark like a banded tail;
# - the tail opens into a fan wider than the stalk (12,0 r, 14,4 f, 15,1-3), with its dark band moved to the fan's
#   base (12,1-2 13,3), so it no longer reads as a gill line or mouth on a head;
# - nothing light in the eye's row near the eye (6,9 2, 7,9 3): the fan starts at row 10;
# - the dorsal tips 3,2 5,2 7,2 stand at the front, the rear spine 9,3 sits 1 px over the membrane.
# Then the round 2 critic (PASS, with fixes) and three blind readers, who all saw the head at the top right because the
# tail was the widest, blockiest end with a lit patch like a face: the tail is a smaller rounded fan (13-14 / 12-15 /
# 12-15 / 12-14 / 13-14), all in fin browns with no pale r, its dark band at the base; membrane f at 4,3 and 6,3 joins
# the front spines into one fin; a darker root 2 at 5,11 parts the pectoral's pale rays from the pale belly.
SKORFNA_D = [
    ".............Ff.",
    "............DFFf",
    "...S.S.S....DFff",
    "...DfDfDFSF2fDf.",
    "...DFDFffh13.ff.",
    "...FFffhhBBo....",
    "...ffhh12B3.....",
    "...hh2BBR4o.....",
    "..hh233R4o......",
    ".hE12323f.......",
    "hh122rrhhD......",
    "1h2202rhFD......",
    "1M100JFDD.......",
    "JJM0o...........",
    "..oo............",
    "................",
]

CANDIDATES = (("D", SKORFNA_D), ("A", SKORFNA_A), ("B", SKORFNA_B), ("C", SKORFNA_C))
CHOICE = "D"   # the candidate written to the mod (A, B and C are round 1, kept for the sheet)


def render(rows, pal=None):
    pal = pal or PAL
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), pal[ch] + (255,))
    return im


def check(name, rows):
    """Warn about lone pixels (no opaque 4-neighbour) and about anything but the eye in the eye's 3x3 neighbourhood
    that is as dark as the gape."""
    dark = {"E", "B", "S", "o", "M", "D"}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and rows[y + dy][x + dx] != "."
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                print(f"warning: {name}: lone pixel at {x},{y}")
    eyes = [(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == "E"]
    assert len(eyes) == 1, (name, eyes)
    ex, ey = eyes[0]
    for x, c in enumerate(rows[ey]):
        if c in dark and c != "E" and abs(x - ex) <= 4:
            print(f"warning: {name}: dark pixel {c} at {x},{ey} in the eye's row")
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            c = rows[ey + dy][ex + dx]
            if (dx or dy) and c in dark:
                print(f"warning: {name}: dark pixel {c} beside the eye at {ex + dx},{ey + dy}")


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<22} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


FINS = set("SDFfr")


def build(rows, fins=FINS):
    """Depth across the fish's axis (most pixels on one diagonal x-y), widest row, and length along the axis."""
    body = [(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c != "." and c not in fins]
    by_a = {}
    for x, y in body:
        by_a.setdefault(x - y, []).append(x + y)
    depth = max((max(v) - min(v)) // 2 + 1 for v in by_a.values())
    widths = [sum(1 for c in r if c != "." and c not in fins) for r in rows]
    length = max(by_a) - min(by_a) + 1
    return depth, max(widths), length


def tiles(band, im, x0, y0):
    """The icon at 8x, then 1x and 2x on light and dark grey."""
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, y0))
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
        t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + 136 + (j % 2) * 44, y0 + (j // 2) * 46))


ACCEPTED = ("cerna", "awrata", "lampuka", "tonn", "sardina", "murina", "incova", "pixxispad", "cawl", "huta_kahla")
VAN_FISH = ("cod", "salmon", "pufferfish", "tropical_fish")


def text_band(lines, W, bg, ink):
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    return band


def image_band(named, W, bg, ink, box):
    small = label_font(13)
    ims = []
    for label, p in named:
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im.thumbnail(box, Image.NEAREST if im.width < 400 else Image.LANCZOS)
            ims.append((label, im))
    h = max(im.height for _, im in ims) + 26
    band = Image.new("RGB", (W, h), bg)
    d = ImageDraw.Draw(band)
    x = 10
    for label, im in ims:
        band.paste(im, (x, 22))
        d.text((x, 2), label, fill=ink, font=small)
        x += max(im.width, 200) + 12
    return band


def hotbars():
    """Offline hotbar previews (owner 2026-11-18: flat icons need no Minecraft run), no slot selected."""
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    tmp = {}
    for name, rows in CANDIDATES:
        p = os.path.join(ART, "candidates", f"fish_skorfna_icon_{name}.png")
        render(rows).save(p, optimize=False)
        tmp[name] = p
    sets = (("", ["mc:cod", "mod:cerna", "mod:skorfna", "mc:salmon", "mod:awrata", "mod:murina", "mc:pufferfish",
                  "mod:lampuka", "mc:tropical_fish"], "2"),
            ("_x4", ["mc:cod", "mod:cerna", "mod:skorfna", "mc:salmon", "mod:awrata", "mod:murina", "mc:pufferfish",
                     "mod:lampuka", "mc:tropical_fish"], "4"),
            ("_candidates_x4", ["mc:cod", "file:" + tmp["D"], "mc:salmon", "file:" + tmp["A"], "mod:cerna",
                                "file:" + tmp["B"], "file:" + tmp["C"], "mc:pufferfish"], "4"))
    out = []
    for suffix, items, scale in sets:
        p = os.path.join(ART, "candidates", f"fish_skorfna_icon_hotbar{suffix}.png")
        subprocess.run([py, tool, p] + items + ["--scale", scale], check=True, capture_output=True)
        out.append((p, items))
    return out


def sheet(icons, hb):
    font, small = label_font(16), label_font(13)
    W = 2000
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    parts.append(("The approved model (round 4): in game beside vanilla cod, and the offline sheet (black skin top)",
                  image_band([("in game, black skin, 2x crops", os.path.join(SHOTS, "crops_black_2x.png")),
                              ("offline: side, three-quarter, top; black, red", os.path.join(SHOTS, "offline",
                                                                                             "skorfna_sheet.png"))],
                             W, bg, ink, (700, 560))))
    parts.append(("References (art/references/fish_skorfna_refonly, list.tsv): out of water for colour, specimen for "
                  "shape", image_band([(n, os.path.join(REFS, n)) for n in
                                       ("black_caught_1.jpg", "black_caught_2.jpg", "black_specimen_side.jpg",
                                        "black_head.jpg")], W, bg, ink, (420, 300))))

    # colour: the model's black palette (unlifted) as the icon uses it
    keys = "0Jh1234BRoEMSDFfr"
    band = Image.new("RGB", (W, 60), bg)
    d = ImageDraw.Draw(band)
    for j, k in enumerate(keys):
        d.rectangle((10 + j * 92, 6, 10 + j * 92 + 88, 40), fill=PAL[k])
        d.text((12 + j * 92, 42), f"{k} #%02x%02x%02x" % PAL[k], fill=ink, font=label_font(11))
    parts.append(("Palette: fish_skorfna_model.PALETTES['black'] before its x1.18 water lift (h = C, o = B)", band))

    # candidates at 8x, 1x and 2x beside vanilla and the accepted fish
    items = [(f"{'>> ' if n == CHOICE else ''}CANDIDATE {n}", icons[n]) for n, _ in CANDIDATES]
    items += [(f"vanilla {n}", Image.open(os.path.join(VANILLA, f"{n}.png")).convert("RGBA")) for n in VAN_FISH[:2]]
    items += [(f"{n} (accepted)", Image.open(os.path.join(TEXTURES, "item", f"{n}.png")).convert("RGBA"))
              for n in ACCEPTED[:3]]
    per_row = 8
    rows_n = (len(items) + per_row - 1) // per_row
    band = Image.new("RGB", (W, rows_n * 170 + 24), bg)
    d = ImageDraw.Draw(band)
    for i, (name, im) in enumerate(items):
        x0, y0 = 10 + (i % per_row) * 244, 22 + (i // per_row) * 170
        tiles(band, im, x0, y0)
        d.text((x0, y0 - 20), name, fill=ink, font=small)
    d.text((10, rows_n * 170), "8x, then 1x and 2x on light and dark grey", fill=ink, font=small)
    parts.append(("The candidates beside vanilla cod and salmon and the accepted cerna, awrata and lampuka", band))

    # all at 1x and 2x in a row
    row = [icons[n] for n, _ in CANDIDATES] + [Image.open(os.path.join(TEXTURES, "item", f"{n}.png")).convert("RGBA")
                                               for n in ACCEPTED] \
        + [Image.open(os.path.join(VANILLA, f"{n}.png")).convert("RGBA") for n in VAN_FISH]
    band = Image.new("RGB", (W, 175), bg)
    d = ImageDraw.Draw(band)
    y = 6
    for s in (1, 2):
        for col in ((139, 139, 139), (40, 40, 40)):
            strip = Image.new("RGBA", (len(row) * (16 * s + 4) + 4, 16 * s + 8), col + (255,))
            for i, im in enumerate(row):
                strip.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4 + i * (16 * s + 4), 4))
            band.paste(strip.convert("RGB"), (10, y))
            y += 16 * s + 12
    d.text((10, y), "D, A, B, C, " + ", ".join(ACCEPTED) + ", " + ", ".join(VAN_FISH), fill=ink, font=small)
    parts.append(("All at 1x and 2x", band))

    # the red skin, for comparison only (not written to the mod)
    red = palette("red")
    band = Image.new("RGB", (W, 128 + 40), bg)
    d = ImageDraw.Draw(band)
    for i, (name, im) in enumerate(((f"black {CHOICE} (the item)", icons[CHOICE]),
                                    (f"{CHOICE} in the red skin's palette (not used)",
                                     render(dict(CANDIDATES)[CHOICE], red)))):
        tiles(band, im, 10 + i * 340, 22)
        d.text((10 + i * 340, 2), name, fill=ink, font=small)
    parts.append(("The same pixels in the red skin's palette, to judge whether a red item would be worth offering", band))

    # build against the accepted fish
    lines = []
    for n in ACCEPTED:
        im = Image.open(os.path.join(TEXTURES, "item", f"{n}.png")).convert("RGBA")
        rows = ["".join("#" if im.getpixel((x, y))[3] else "." for x in range(16)) for y in range(16)]
        dep, wid, ln = build(rows, set())
        lines.append(f"{n:<11} outline: deepest across the axis {dep:>2} px   widest row {wid:>2}   length along the "
                     f"axis {ln:>2}   length/depth {ln / dep:.1f}")
    for name, rows in CANDIDATES:
        dep, wid, ln = build(["".join("." if c == "." else "#" for c in r) for r in rows], set())
        dep_b, wid_b, ln_b = build(rows)
        lines.append(f"{'skorfna ' + name:<11} outline: deepest across the axis {dep:>2} px   widest row {wid:>2}   "
                     f"length along the axis {ln:>2}   length/depth {ln / dep:.1f}   (body alone, fins left out: "
                     f"{dep_b} / {wid_b} / {ln_b})")
    parts.append(("Build against the accepted fish (deepest = most pixels on one cross-diagonal, fins included)",
                  text_band(lines, W, bg, ink)))

    paths = [os.path.join(ART, "candidates", f"fish_skorfna_icon_{n}.png") for n, _ in CANDIDATES]
    lines = measure(paths + [os.path.join(TEXTURES, "item", f"{n}.png") for n in ACCEPTED[:3]]
                    + [os.path.join(VANILLA, f"{n}.png") for n in VAN_FISH[:2]])
    lines.append("STYLE.md food ranges: cover 0.29-0.77, colours 6-20, dark 0.0-0.35, light 0.32-0.99, TL-BR +0.01-+0.17")
    parts.append(("art/tools/measure.py", text_band(lines, W, bg, ink)))

    ims = [Image.open(p).convert("RGB") for p, _ in hb]
    band = Image.new("RGB", (W, sum(im.height + 10 for im in ims) + 24), bg)
    y = 4
    for im in ims:
        band.paste(im, (10, y))
        y += im.height + 10
    ImageDraw.Draw(band).text((10, y), "art/tools/hotbar_preview.py, no slot selected: cod, cerna, SKORFNA, salmon, "
                              "awrata, murina, pufferfish, lampuka, tropical fish at GUI scale 2 and 4; then cod, D, "
                              "salmon, A (round 1), cerna, B, C, pufferfish at 4", fill=ink, font=small)
    parts.append(("Hotbar preview (offline, as the game draws flat items)", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), f"Skorfna (black scorpionfish) item icon, textures/item/skorfna.png = candidate {CHOICE}",
           fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)


def main():
    icons = {}
    for name, rows in CANDIDATES:
        check(name, rows)
        icons[name] = render(rows)
    icons[CHOICE].save(OUT_ICON, optimize=False)
    hb = hotbars()
    sheet(icons, hb)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
