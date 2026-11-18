"""Item icon for the huta kahla (blue shark, Prionace glauca): the caught fish, like vanilla cod and salmon.

This icon is the blue shark's first piece and sets its look and palette; its bucket, spawn egg and model copy it.

What makes it a blue shark (photos in art/references/fish_huta_kahla_refonly/, list.tsv):
- a very slender, long body with a long, pointed conical snout, slimmer than every accepted fish;
- a large round eye near the front of the head (one dark pixel, nothing else dark near it);
- very long, narrow, sickle-shaped pectoral fins, the strongest cue after the colour;
- a single first dorsal fin set back toward the middle of the body, tall and triangular, its leading edge swept back;
- a heterocercal tail: the upper lobe much longer than the lower;
- five gill slits: left out, as at 16 pixels they read as stripes or extra eyes;
- an indigo-blue back, bright blue sides and a sharp change to a white belly (countershading). Photos of landed
  sharks (bs01 on deck, bs03 at the Vigo market, bs07 on a boat) show a duller slate-blue than underwater shots
  (the old film scans also pull toward teal-grey); the palette keeps the blue clear enough to read at 1x, a step
  below the underwater cobalt.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left. The dorsal rim carries a lit blue, brightest over the head; under it the
indigo back, then the bright blue side, the white belly, and a grey-blue shade on the lower right rim. The fins are
two-tone (lit leading edge, darker membrane). The tonn's back is navy over cold silver sides with yellow finlets; the
shark's is a more violet indigo over bright blue sides, with no yellow, so the two never share a colour.

Run:  art/.venv/bin/python art/src/fish_huta_kahla_icon.py
Writes mod/.../textures/item/huta_kahla.png (byte-identical on rerun), art/candidates/fish_huta_kahla_icon.png
(compare sheet) and the offline hotbar previews art/candidates/fish_huta_kahla_icon_hotbar*.png.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(ART, ".."))
sys.path.insert(0, os.path.join(ART, "tools"))
from font import label_font  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "huta_kahla.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_huta_kahla_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_huta_kahla_refonly")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # round 2: the back rim is indigo (1), a dark outline as on the tonn; the light sits one pixel inside it,
    # over the head and front third only (D)
    "1": hx("#303a86"), "3": hx("#4a66c0"),
    # white belly (sharp countershading line), then the belly turning away from the light into shade
    "5": hx("#e8ecf6"), "6": hx("#a8b0cc"), "g": hx("#6e76a0"), "G": hx("#464e7c"),
    "e": hx("#0a0a16"),                       # the eye
    "D": hx("#7a90dc"), "d": hx("#4a5cb4"),   # lit inner back and dorsal leading edge; dorsal membrane
    "P": hx("#4a5eb6"), "p": hx("#262e74"),   # pectoral: mid-blue blade, dark tip (p is also the dorsal tip)
    "L": hx("#7a90dc"), "k": hx("#323c8c"),   # pectoral: lit leading edge, dark trailing edge
    "T": hx("#6e84d4"), "t": hx("#323c8c"),   # tail: lit leading edge, dark
}

PAL_ROUND1 = {
    # dorsal rim, lit from the top left: a pale sheen along the whole back
    "H": hx("#8ea4e6"),
    # indigo back, then the bright blue side
    "1": hx("#303a86"), "3": hx("#4a66c0"),
    # white belly (sharp countershading line), then the belly turning away from the light into shade
    "5": hx("#e8ecf6"), "6": hx("#a8b0cc"), "g": hx("#6e76a0"), "G": hx("#464e7c"),
    "o": hx("#1e2248"),                       # darkest rim, under the tail stalk
    "e": hx("#0a0a16"),                       # the eye
    "D": hx("#7a90dc"), "d": hx("#4a5cb4"),   # first dorsal: lit leading edge, membrane
    "P": hx("#4a5eb6"), "p": hx("#262e74"),   # long sickle pectoral: lit root, dark blade
    "T": hx("#6e84d4"), "t": hx("#323c8c"),   # tail: lit leading edge, dark
}

# Head lower left, tail upper right. Round 2 (critic: FIX, round 1 read as a thin blue streak at 1x and 2x):
# - the back rim is indigo 1, a dark outline like the tonn's, so the fish holds its shape against light backdrops;
#   the light D sits one pixel inside it over the head and front third (3,12 4,11 5,10);
# - the first dorsal is a short solid shark triangle further forward than round 1 and than the pixxispad's: base
#   5,8 to 7,6, lit leading edge D (5,7 6,6), membrane d, dark tip p at 6,5;
# - the snout tapers: the tip 0,14 is side blue 3, the white belly stops before it, and 2,14 is shade G;
# - the tail stalk narrows to 3 pixels (rows 4-6) in indigo and shade, and the white belly gives way to 6 toward the
#   tail, so the full depth (5-6 px) stays only around the dorsal and pectoral;
# - (round 3, owner: the round 2 pectoral, a 1-pixel line out to 11,15, was "too thin and long" to read as a fin)
#   the pectoral is a broad blade under the gill: a 3-pixel root on the belly at 6-8,13, sweeping back and down 4
#   pixels to a point at 10,15. Lit leading edge L (6,13 7,14), mid-blue blade P, dark trailing edge k (9,13) and
#   dark tip p (9,14 10,15), joined diagonally so the fin ends in a swept point (critic polish). The notch at 8,12 keeps its trailing edge apart from the belly.
# Bands from the back to the belly: indigo rim 1, lit D (front only), bright blue side 3, white belly 5, then the
# belly turning into shade 6 and G. The upper tail lobe climbs from the stalk to 13,0; the lower lobe is a short
# 2-pixel blade pointing right (13-14,4). The eye is one dark pixel at 2,13 inside the blue.
HUTA_KAHLA = [
    ".............T..",
    "............Tt..",
    "............Tt..",
    "...........1t...",
    "..........13Gtt.",
    "......p..11G....",
    "......Dd11G.....",
    ".....Dd1136G....",
    ".....d1135G.....",
    ".....11356G.....",
    "....1D356G......",
    "...1D356G.......",
    "..1D356G........",
    ".1e356LPPk......",
    "35G....LPp......",
    "..........p.....",
]

# Round 2 (owner: FIX, "its long fin is too thin and long so it doesnt read as a fin"), kept only for the compare
# sheet; it uses PAL.
HUTA_KAHLA_ROUND2 = [
    ".............T..",
    "............Tt..",
    "............Tt..",
    "...........1t...",
    "..........13Gtt.",
    "......p..11G....",
    "......Dd11G.....",
    ".....Dd1136G....",
    ".....d1135G.....",
    ".....11356G.....",
    "....1D356G......",
    "...1D356G.......",
    "..1D356G........",
    ".1e356PPp.......",
    "35G......pp.....",
    "...........p....",
]

# Round 1 (critic: FIX, read as a thin blue streak or a pen at 1x), kept only for the compare sheet, with its palette.
HUTA_KAHLA_ROUND1 = [
    ".............T..",
    "............Tt..",
    "............Tt..",
    "........D..Ht...",
    "........D.H3Gtt.",
    ".......DdH13o...",
    "......DdH13G....",
    ".......H135G....",
    "......H135G.....",
    ".....H1356G.....",
    "....H1356G......",
    "...H1356G.......",
    "..H1356G........",
    ".He356Ppp.......",
    "H56G.....pp.....",
    "................",
]


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


def check(rows):
    """Warn about stray pixels (no opaque 8-neighbour)."""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and rows[y + dy][x + dx] != "."
                       for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy):
                print(f"warning: stray pixel at {x},{y}")


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<18} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


FINS = set("DdTtPpLk")


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


# Colour from photos of the shark out of water: (box, note)
SAMPLES = {
    "bs01.jpg": ((440, 820, 560, 1100), "on deck, Ireland"),
    "bs03.jpg": ((120, 290, 520, 430), "landed, Vigo fish market"),
}


def sample_photos():
    import numpy as np
    out = {}
    for name, (box, note) in SAMPLES.items():
        p = os.path.join(REFS, name)
        if not os.path.exists(p):
            continue
        a = np.array(Image.open(p).convert("RGB").crop(box)).reshape(-1, 3).astype(float)
        lum = a @ [0.2126, 0.7152, 0.0722]
        q = np.percentile(lum, [5, 35, 65, 95])
        cols = [tuple(int(v) for v in np.median(a[(lum >= lo) & (lum <= hi)], 0))
                for lo, hi in ((q[0], q[1]), (q[1], q[2]), (q[2], q[3]))]
        out[name] = (cols, note)
    return out


def tiles(band, im, x0, y0):
    """The icon at 8x, then 1x and 2x on light and dark grey."""
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, y0))
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
        t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + 136 + (j % 2) * 44, y0 + (j // 2) * 46))


ACCEPTED = ("tonn", "pixxispad", "lampuka", "sardina", "cerna", "awrata", "murina")
VAN_FISH = ("cod", "salmon", "pufferfish")


def text_band(lines, W, bg, ink):
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    return band


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 2000
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    # references
    refs = []
    for name in ("bs01.jpg", "bs03.jpg", "bs07.jpg", "bs06.jpg", "bs05.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im.thumbnail((380, 300), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = max(im.height for _, im in refs) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im, (10 + i * 392, 22))
            d.text((10 + i * 392, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References (art/references/fish_huta_kahla_refonly, list.tsv): landed sharks for colour, "
                      "drawing and underwater for shape", band))

    # colour: photo samples beside the palette
    samples = sample_photos()
    band = Image.new("RGB", (W, 34 * (len(samples) + 1) + 10), bg)
    d = ImageDraw.Draw(band)
    y = 6
    for name, (rgbs, note) in list(samples.items()) + [
            ("PALETTE", ([PAL[c] for c in "1D356G"] + [PAL[c] for c in "DdLPkpTt"],
                         "body ramp 1 D 3 5 6 G, then dorsal D d, pectoral L P k p, tail T t"))]:
        d.text((10, y + 8), name, fill=ink, font=small)
        seen = []
        for rgb in rgbs:
            if rgb not in seen:
                seen.append(rgb)
        for j, rgb in enumerate(seen):
            d.rectangle((200 + j * 74, y, 200 + j * 74 + 70, y + 28), fill=rgb)
            d.text((200 + j * 74 + 2, y + 16), "#%02x%02x%02x" % rgb,
                   fill=(255, 255, 255) if sum(rgb) < 380 else (0, 0, 0), font=label_font(11))
        d.text((200 + 15 * 74 + 10, y + 8), note, fill=ink, font=small)
        y += 34
    parts.append(("Colour: photo samples of landed sharks (dark, mid, light) beside the palette", band))

    # 8x and 1x beside vanilla and the accepted fish
    items = [("HUTA KAHLA", None)]
    items += [(f"{n} (accepted)", os.path.join(TEXTURES, "item", f"{n}.png")) for n in ACCEPTED]
    items += [(f"vanilla {n}", os.path.join(VANILLA, f"{n}.png")) for n in VAN_FISH]
    per_row = 8
    rows_n = (len(items) + per_row - 1) // per_row
    band = Image.new("RGB", (W, rows_n * 170 + 24), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = icon if p is None else Image.open(p).convert("RGBA")
        x0, y0 = 10 + (i % per_row) * 244, 22 + (i // per_row) * 170
        tiles(band, im, x0, y0)
        d.text((x0, y0 - 20), name, fill=ink, font=small)
    d.text((10, rows_n * 170), "8x, then 1x and 2x on light and dark grey", fill=ink, font=small)
    parts.append(("The icon at 8x and 1x beside the accepted fish and vanilla cod, salmon and pufferfish", band))

    # all fish at 1x in one row, as they sit together in a chest
    band = Image.new("RGB", (W, 2 * 30 + 16), bg)
    d = ImageDraw.Draw(band)
    row = [icon] + [Image.open(os.path.join(TEXTURES, "item", f"{n}.png")).convert("RGBA") for n in ACCEPTED] \
        + [Image.open(os.path.join(VANILLA, f"{n}.png")).convert("RGBA") for n in VAN_FISH]
    for k, col in enumerate(((139, 139, 139), (40, 40, 40))):
        strip = Image.new("RGBA", (len(row) * 20 + 4, 24), col + (255,))
        for i, im in enumerate(row):
            strip.alpha_composite(im, (4 + i * 20, 4))
        band.paste(strip.convert("RGB"), (10, 6 + k * 32))
    d.text((260, 12), "1x: HUTA KAHLA, " + ", ".join(ACCEPTED) + ", cod, salmon, pufferfish", fill=ink, font=small)
    parts.append(("All at 1x", band))

    # round 2 beside round 1 and the tonn and pixxispad: 8x, then 1x and 2x on light and dark grey
    band = Image.new("RGB", (W, 128 + 40), bg)
    d = ImageDraw.Draw(band)
    for i, (name, im) in enumerate((("ROUND 3 (broad pectoral)", icon),
                                    ("round 2 (owner: FIX, pectoral too thin)", render(HUTA_KAHLA_ROUND2)),
                                    ("round 1 (critic: FIX, a thin streak at 1x)", render(HUTA_KAHLA_ROUND1, PAL_ROUND1)),
                                    ("tonn (accepted)", Image.open(os.path.join(TEXTURES, "item", "tonn.png")).convert("RGBA")),
                                    ("pixxispad (accepted)",
                                     Image.open(os.path.join(TEXTURES, "item", "pixxispad.png")).convert("RGBA")))):
        x0 = 10 + i * 330
        tiles(band, im, x0, 22)
        d.text((x0, 2), name, fill=ink, font=small)
    parts.insert(2, ("Round 3 beside rounds 2 and 1, the tonn and the pixxispad (8x, then 1x and 2x)", band))

    # build compared
    lines = []
    for n in ACCEPTED:
        im = Image.open(os.path.join(TEXTURES, "item", f"{n}.png")).convert("RGBA")
        rows = ["".join("#" if im.getpixel((x, y))[3] else "." for x in range(16)) for y in range(16)]
        dep, wid, ln = build(rows, set())
        lines.append(f"{n:<10} outline: deepest across the axis {dep:>2} px   widest row {wid:>2}   length along the axis "
                     f"{ln:>2}   length/depth {ln / dep:.1f}")
    rows = ["".join("." if c == "." else "#" for c in r) for r in HUTA_KAHLA]
    dep, wid, ln = build(rows, set())
    dep_b, wid_b, ln_b = build(HUTA_KAHLA)
    lines.append(f"{'huta kahla':<10} outline: deepest across the axis {dep:>2} px   widest row {wid:>2}   length along the "
                 f"axis {ln:>2}   length/depth {ln / dep:.1f}   (body alone, fins left out: {dep_b} / {wid_b} / {ln_b})")
    parts.append(("Build against the accepted fish: the slimmest of them (deepest = most pixels on one cross-diagonal, "
                  "fins included)", text_band(lines, W, bg, ink)))

    # numbers
    lines = measure([OUT_ICON] + [os.path.join(TEXTURES, "item", f"{n}.png") for n in ACCEPTED]
                    + [os.path.join(VANILLA, f"{n}.png") for n in VAN_FISH])
    lines.append("STYLE.md food ranges: cover 0.29-0.77, colours 6-20, dark 0.0-0.35, light 0.32-0.99, TL-BR +0.01-+0.17")
    parts.append(("art/tools/measure.py", text_band(lines, W, bg, ink)))

    # offline hotbar preview (owner 2026-11-18: flat icons need no Minecraft run), at the GUI scale and at 4x
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    set_a = ["mc:cod", "mod:tonn", "mod:pixxispad", "mod:huta_kahla", "mc:salmon", "mod:lampuka", "mod:sardina",
             "mod:cerna", "mod:awrata"]
    set_b = ["mc:pufferfish", "mod:murina", "mod:tonn", "mod:huta_kahla", "mod:pixxispad", "mc:cod"]
    hb = []
    for suffix, items_, extra in (("", set_a, ["--scale", "2"]), ("_x4", set_a, ["--scale", "4"]),
                                  ("_b_x4", set_b, ["--scale", "4"])):
        out = os.path.join(ART, "candidates", f"fish_huta_kahla_icon_hotbar{suffix}.png")
        subprocess.run([py, tool, out] + items_ + ["--select", "3"] + extra, check=True, capture_output=True)
        hb.append(Image.open(out).convert("RGB"))
    band = Image.new("RGB", (W, sum(im.height + 10 for im in hb) + 24), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    ImageDraw.Draw(band).text((10, y), "art/tools/hotbar_preview.py: cod, tonn, pixxispad, HUTA KAHLA (selected), salmon, "
                              "lampuka, sardina, cerna, awrata at scale 2 and 4; then pufferfish, murina, tonn, "
                              "HUTA KAHLA, pixxispad, cod at 4", fill=ink, font=small)
    parts.append(("Hotbar preview (offline, as the game draws flat items)", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Huta kahla (blue shark) item icon, textures/item/huta_kahla.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)


def main():
    check(HUTA_KAHLA)
    icon = render(HUTA_KAHLA)
    icon.save(OUT_ICON, optimize=False)
    sheet(icon)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
