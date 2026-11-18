"""Item icon for the ċawl (Mediterranean damselfish, Chromis chromis): the caught fish, like vanilla cod and salmon.

What makes it a ċawl (photos in art/references/fish_cawl_refonly/, list.tsv):
- a small, deep, oval, flat-sided body;
- a deeply forked tail with long pointed lobes, pale at their edges;
- a small mouth and a fairly large eye;
- one long dorsal fin running along the whole back;
- the adult is dark chocolate brown, with the scales showing as a faint darker net and paler fin edges.

The adult is drawn: the brown fish seen over every Maltese rock. The vivid blue juvenile is left for later.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied) and our accepted fish:
head lower left, tail upper right, light from the top left. The brown is lifted a step above the flash photos
(cawl_02, cawl_04, cawl_06, cawl_07) so the icon never reads as a black blob: a warm lit brown under the back runs
down a ramp of 5 body tones to the dark belly and rim.

This icon sets the ċawl's look and palette: its bucket, spawn egg and model copy PAL below.

Run:  art/.venv/bin/python art/src/fish_cawl_icon.py
Writes mod/.../textures/item/cawl.png (byte-identical on rerun) and art/candidates/fish_cawl_icon.png (compare sheet,
with offline hotbar previews from art/tools/hotbar_preview.py, also saved as art/candidates/fish_cawl_icon_hotbar.png
and _hotbar_x4.png).
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
OUT_ICON = os.path.join(TEXTURES, "item", "cawl.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_cawl_icon.png")
OUT_HOTBAR = os.path.join(ART, "candidates", "fish_cawl_icon_hotbar.png")
OUT_HOTBAR4 = os.path.join(ART, "candidates", "fish_cawl_icon_hotbar_x4.png")
OUT_HOTBAR_R2 = os.path.join(ART, "candidates", "fish_cawl_icon_hotbar_round2_round4.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_cawl_refonly")
HOTBAR = ["mc:cod", "mc:salmon", "mod:sardina", "mod:lampuka", "mod:tonn", "mod:cerna", "mod:awrata", "mod:murina",
          "mod:cawl"]


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    "K": hx("#3c291d"),                       # back rim, where the light falls on the dark back
    "b": hx("#5f4535"),                       # band just inside the back rim
    # chocolate light ramp, from the warm sheen under the back (W) to the shaded belly (5)
    "H": hx("#a07c5c"),                       # highlight on the forehead and snout, where the head turns to the light
    "W": hx("#8a6a50"), "1": hx("#735540"), "2": hx("#614636"), "3": hx("#4f3a2c"), "4": hx("#432f23"),
    "5": hx("#36261c"),
    "o": hx("#1d130c"),                       # rim on the shaded belly side
    "e": hx("#0a0a0a"),                       # eye (the only black)
    "L": hx("#402b1f"),                       # small mouth on the shaded chin
    "D": hx("#4a3428"), "d": hx("#7a6656"),   # dorsal fin: body, paler edge
    "c": hx("#5c4132"),                       # dorsal crest, a step lighter than the back rim
    "F": hx("#2b1d15"),                       # pelvic and anal fins (dark)
    # forked tail: pale lobe tips and outer edges (p), lit lobe (q), shaded lobe (r), dark edge along the notch (t)
    "p": hx("#a8968a"), "q": hx("#8e705d"), "r": hx("#6d5242"), "t": hx("#4a3428"),
}

# Build: 84 pixels, between the sardina (69) and the awrata (96); outline overlap 0.59 with the awrata and 0.62
# with the ċerna. A short, deep oval with a blunt round head (no forehead hump like the awrata's): deepest just
# behind the eye, 9 px across the diagonal, narrowing to a 2 px tail stalk at 10,5-10,6.
# Head, reworked in round 3 after the owner (2026-11-18: "cawl's face is too flat"): a steep, rounded forehead that
# steps 2 px at a time (x 4, 4, 3, 3, 2, 2 down rows 6-11) up to the back. The head is a lit dome: a highlight (H) at
# 5,8-5,9, up and behind the eye and never touching it, inside a ring of lit tones (W) on the forehead and snout.
# The eye (4,10) is the only black and sits in that lit socket: W in front, above and behind it, joined to the
# forehead dome (6,9 W too), and the shaded chin and throat (3) below it.
# Round 4 (critic, 2026-11-18: round 3 looked like round 2 at GUI scale 2, the chin under the eye was lit and the
# lower gill arc melted into the belly): chin and throat 3,11-4,11 shaded to 3, the lit cheek 6,10 at 1, and the
# body behind the gill arc lifted (8,9 1, 8,10 2, 8,11 3) so the arc stands two steps darker than its neighbours.
# The gill line is a curve of darker pixels around the eye (6,8 7,9 7,10 7,11 6,12).
# The small mouth is a rounded corner on the snout (2,11 rim, 3,12 dark underside), on the shaded chin.
# The dorsal fin runs along the whole back as the darker rim (D, K) from the forehead to the stalk, rising in a crest
# over the middle of the back (5-8,4 and 6-7,3: a step lighter than the back rim (c), a paler edge (d), dark base (D)).
# After the critic (2026-11-18) the body is a step darker than the first version, and the belly tones 4 and 5 a step
# deeper again so the ramp keeps 5 distinct body tones; the back rim (K), belly rim (o) and dark fins (F) went a step
# deeper too, so the outline stays well below the inside (body edge 0.19 against inside 0.28).
# Pelvic (8,13) and anal (11,8) fins are dark stubs breaking the belly outline.
# The deeply forked tail: an upper lobe straight up (10-11, 1-4) and a lower lobe to the right (11-14, 4-5), mirrored
# about the body axis. The notch reaches in to 11,4, right behind the stalk, deeper than the awrata's (13,1). Each
# lobe is lit on its outer side (q), shaded towards the notch (r, t) and pale at the tip (p).
# Scales: the lit flank alternates tones 1 and 2 (rows 8-11) so it shows a faint net, never bright specks.
# Every outline steps in runs of 1-3 px.
CAWL = [
    "................",
    "...........p....",
    "..........qr....",
    "......dc..qt....",
    ".....cdDDqr.rqp.",
    ".....dDKKb3trrq.",
    "....DKbW124r....",
    "....KbW123o.....",
    "...KWH32234F....",
    "...bWHW313o.....",
    "..bWeW142o......",
    "..K333353o......",
    "...L3454o.......",
    "....45o.F.......",
    "................",
    "................",
]


# Round 2 (after the critic's palette fix), sent back by the owner (2026-11-18): "cawl's face is too flat". Same
# palette as now, without the head highlight H. Kept for the compare sheet; rounds 3 and 4 changed only the head.
CAWL_ROUND2 = [
    "................",
    "...........p....",
    "..........qr....",
    "......dc..qt....",
    ".....cdDDqr.rqp.",
    ".....dDKKb3trrq.",
    "....DKbW124r....",
    "...DKbW123o.....",
    "...KbW12234F....",
    "..Kb1W2123o.....",
    "..b1e1234o......",
    "..K123245o......",
    "...L2345o.......",
    "....45o.F.......",
    "................",
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
    """Warn about stray pixels (no opaque 4-neighbour)."""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            if not any(0 <= x + dx < 16 and 0 <= y + dy < 16 and rows[y + dy][x + dx] != "."
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
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


def hotbar(out, scale):
    args = [os.path.join(ART, ".venv", "bin", "python"), os.path.join(ART, "tools", "hotbar_preview.py"), out] + HOTBAR
    subprocess.run(args + ["--select", str(len(HOTBAR) - 1), "--scale", str(scale)], check=True, capture_output=True)
    return Image.open(out).convert("RGB")


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 1420
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    # references (flash or good light: true colour)
    refs = []
    for name in ("cawl_04.jpg", "cawl_02.jpg", "cawl_07.jpg", "cawl_10.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((340, round(340 * im.height / im.width)), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = max(im.height for _, im in refs) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im, (10 + i * 350, 22))
            d.text((10 + i * 350, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References, flash-lit for true colour (art/references/fish_cawl_refonly, list.tsv)", band))

    # 8x and 1x beside vanilla and our accepted fish
    items = [("vanilla cod", os.path.join(VANILLA, "cod.png")),
             ("vanilla salmon", os.path.join(VANILLA, "salmon.png"))]
    items += [(n + " (accepted)", os.path.join(TEXTURES, "item", f + ".png"))
              for n, f in (("sardina", "sardina"), ("lampuka", "lampuka"), ("tonn", "tonn"), ("ċerna", "cerna"),
                           ("awrata", "awrata"), ("murina", "murina"), ("pixxispad", "pixxispad"))]
    items.append(("ĊAWL", None))
    band = Image.new("RGB", (W, 128 + 100), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = icon if p is None else Image.open(p).convert("RGBA")
        x0 = 10 + i * 140
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(tile.convert("RGB"), (x0, 22))
        d.text((x0, 2), name, fill=(250, 210, 120) if p is None else ink, font=small)
        for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
            t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x0 + (0, 26, 66, 92)[j], 154))
    d.text((10, 206), "8x, then 1x and 2x on light and dark grey", fill=ink, font=small)
    parts.append(("The icon at 8x and 1x beside vanilla cod and salmon and our accepted fish", band))

    # round 2 and round 4, at 8x, 2x and 1x, beside the ċerna and the awrata, with the pixels that changed
    r2 = render(CAWL_ROUND2)
    four = [("ċerna (accepted)", Image.open(os.path.join(TEXTURES, "item", "cerna.png")).convert("RGBA")),
            ("awrata (accepted)", Image.open(os.path.join(TEXTURES, "item", "awrata.png")).convert("RGBA")),
            ("ċawl round 2 (owner: face too flat)", r2), ("ĊAWL round 4", icon)]
    band = Image.new("RGB", (W, 128 + 120), bg)
    d = ImageDraw.Draw(band)
    for i, (name, im) in enumerate(four):
        x0 = 10 + i * 345
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        band.paste(tile.convert("RGB"), (x0, 22))
        d.text((x0, 2), name, fill=(250, 210, 120) if im is icon else ink, font=small)
        for j, (col, sc) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
            t = Image.new("RGBA", (16 * sc + 8, 16 * sc + 8), col + (255,))
            t.alpha_composite(im.resize((16 * sc, 16 * sc), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x0 + 136 + (j % 2) * 34 + (j // 2) * 80, 22))
    changed = [f"{x},{y}" for y in range(16) for x in range(16) if r2.getpixel((x, y)) != icon.getpixel((x, y))]
    d.text((10, 160), "8x, then 1x and 2x on light and dark grey", fill=ink, font=small)
    d.text((10, 182), f"Pixels changed from round 2 to round 4 ({len(changed)}, all in the head, x 2-8, y 7-12):",
           fill=ink, font=small)
    d.text((10, 202), "  ".join(changed), fill=ink, font=small)
    parts.append(("Round 2 and round 4 (head reworked) beside the ċerna and the awrata", band))

    # round 2 and round 4 next to each other in the hotbar at GUI scale 2, where the critic judged them
    r2_path = os.path.join(ART, "candidates", "fish_cawl_icon_round2.png")
    r2.save(r2_path, optimize=False)
    subprocess.run([os.path.join(ART, ".venv", "bin", "python"), os.path.join(ART, "tools", "hotbar_preview.py"),
                    OUT_HOTBAR_R2, "mod:cerna", "mod:awrata", "file:" + r2_path, "mod:cawl", "--select", "3",
                    "--scale", "2"], check=True, capture_output=True)
    im = Image.open(OUT_HOTBAR_R2).convert("RGB")
    band = Image.new("RGB", (W, im.height + 30), bg)
    band.paste(im, (10, 4))
    ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(OUT_HOTBAR_R2, ROOT), fill=ink, font=small)
    parts.append(("Hotbar at GUI scale 2: ċerna, awrata, ċawl round 2, ċawl round 4 (selected)", band))

    # build: opaque pixel count, size of the bounding box, and outline overlap (intersection over union)
    def mask(im):
        return {(x, y) for y in range(16) for x in range(16) if im.getpixel((x, y))[3]}
    mine = mask(icon)
    rows = [f"ċawl {len(mine)} px"]
    for name, f in (("sardina", "sardina"), ("awrata", "awrata"), ("ċerna", "cerna"), ("tonn", "tonn")):
        m = mask(Image.open(os.path.join(TEXTURES, "item", f + ".png")).convert("RGBA"))
        rows.append(f"{name} {len(m)} px, overlap {len(m & mine) / len(m | mine):.2f}")
    band = Image.new("RGB", (W, 28), bg)
    ImageDraw.Draw(band).text((10, 4), "   ".join(rows), fill=ink, font=label_font(14))
    parts.append(("Build: pixels covered, and outline overlap with the ċawl (intersection over union)", band))

    # palette
    band = Image.new("RGB", (W, 60), bg)
    d = ImageDraw.Draw(band)
    for i, (k, c) in enumerate(PAL.items()):
        x0 = 10 + i * 69
        d.rectangle((x0, 4, x0 + 28, 32), fill=c)
        d.text((x0, 36), f"{k} #{c[0]:02x}{c[1]:02x}{c[2]:02x}", fill=ink, font=label_font(11))
    parts.append(("Palette (the bucket, egg and model copy these)", band))

    # numbers
    lines = measure([os.path.join(VANILLA, "cod.png"), os.path.join(VANILLA, "salmon.png")] +
                    [os.path.join(TEXTURES, "item", f + ".png") for f in ("sardina", "awrata", "cerna")] + [OUT_ICON])
    lines.append("STYLE.md food ranges: cover 0.29-0.77, colours 6-20, dark 0.0-0.35, light 0.32-0.99, TL-BR +0.01-+0.17")
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py", band))

    # hotbar previews (offline, art/tools/hotbar_preview.py), GUI scale 2 (as in the game's screenshots) and 4
    for scale, path in ((2, OUT_HOTBAR), (4, OUT_HOTBAR4)):
        im = hotbar(path, scale)
        if im.width > W - 20:
            im = im.resize((W - 20, round(im.height * (W - 20) / im.width)), Image.NEAREST)
        band = Image.new("RGB", (W, im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(path, ROOT), fill=ink, font=small)
        parts.append((f"Hotbar preview at GUI scale {scale}, on light and dark: cod, salmon, sardina, lampuka, tonn, "
                      "ċerna, awrata, murina, ċawl (selected)", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Ċawl (Mediterranean damselfish) item icon, textures/item/cawl.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)


def main():
    check(CAWL)
    icon = render(CAWL)
    icon.save(OUT_ICON, optimize=False)
    sheet(icon)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
