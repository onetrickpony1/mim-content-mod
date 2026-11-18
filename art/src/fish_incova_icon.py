"""Item icon for the incova (European anchovy, Engraulis encrasicolus): the caught fish, like vanilla cod and salmon.

The owner: anchovies are not sardines (2026-11-18). This is the anchovy's first piece and sets its look and palette.
What makes it an anchovy, and not the sardina beside it (photos in art/references/fish_incova_refonly/, list.tsv;
colour from the fish out of water: portugal.jpg on the beach, ifremer1.jpg and lonja.jpg fresh at market):
- slimmer and rounder in cross-section than the sardina, a cigar of even depth (5 pixels across its rows against the
  sardina's 6-7), tapering only at the very end to a thin tail stalk;
- a long pointed snout that overhangs the mouth: the tip sits on the back's line, and the lower jaw starts well behind
  it, so the head ends in a point, not a blunt nose;
- a very long mouth: one dark grey line from under the snout tip back past the eye, fading to silver-grey behind it;
- a large eye set far forward, three pixels behind the snout tip, inside the pale head;
- a bright silver band along the middle of the flank, one unbroken near-white line from behind the gill to the tail
  stalk (the sardina has no band, only silver sides);
- a blue-green to greenish back (greener than the sardina's blue-teal), a pale silver-green head;
- no dark spots: the sardina's row of spots behind the gill is left out on purpose; no gold gill cover, only a faint
  straw tint on the gill;
- a forked tail, one small triangular dorsal fin mid-back, and small pelvic and anal fins.

Pose and light follow vanilla's fish items (measured with art/tools/measure.py, never copied): head lower left, tail
upper right, light from the top left. The back faces the light, so its outer edge is a lit green sheen with the dark
blue-green back just inside, then the silver band, silver and grey sides, and a dark rim on the shaded belly.

Run:  art/.venv/bin/python art/src/fish_incova_icon.py
Writes mod/.../textures/item/incova.png (byte-identical on rerun), art/candidates/fish_incova_icon.png (compare sheet)
and the offline hotbar previews art/candidates/fish_incova_icon_hotbar.png and _hotbar_x4.png.
"""
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

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
OUT_ICON = os.path.join(TEXTURES, "item", "incova.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_incova_icon.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_incova_refonly")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # round 2 (critic): the mint edge dulled a step, the mouth line darker and longer
    # back: lit green sheen on the edge facing the light, dark blue-green back, a lighter blue-green toward the head
    "h": hx("#86b89e"), "k": hx("#244c48"), "m": hx("#3f7568"),
    # flank: the bright silver band, silver, grey toward the shaded belly, dark rim on the belly
    "W": hx("#f6faf8"), "s": hx("#c3cdd0"), "g": hx("#8c99a1"), "o": hx("#3a4650"),
    "e": hx("#0b0d0d"),                        # eye
    "j": hx("#4e5a62"), "J": hx("#9aa6ab"),    # the long mouth line: one dark run past the eye, fading behind it
    "p": hx("#dfe5e3"),                        # the pale lower jaw
    "G": hx("#cfd3b8"),                        # faint straw tint on the gill cover (not the sardina's gold)
    "F": hx("#93b0a6"), "f": hx("#6f8e86"),    # dorsal fin: lit tip, fin
    "a": hx("#5f6d78"),                        # pelvic and anal fins (in the shade)
    "T": hx("#7a9a93"), "u": hx("#5f837c"), "t": hx("#4c6763"),  # tail: lit upper lobe, its base, shaded lower lobe
}

PAL_ROUND1 = {
    # round 1 (critic: FIX, a blunt snout and a short mouth), kept only for the compare sheet
    # back: lit green sheen on the edge facing the light, dark blue-green back, a lighter blue-green toward the head
    "h": hx("#8ec3a6"), "k": hx("#244c48"), "m": hx("#3f7568"),
    # flank: the bright silver band, silver, grey toward the shaded belly, dark rim on the belly
    "W": hx("#f6faf8"), "s": hx("#c3cdd0"), "g": hx("#8c99a1"), "o": hx("#3a4650"),
    "e": hx("#0b0d0d"),                        # eye
    "j": hx("#6c7a80"), "J": hx("#9aa6ab"),    # the long mouth line: under the snout, fading behind the eye
    "p": hx("#dfe5e3"),                        # the pale lower jaw
    "G": hx("#cfd3b8"),                        # faint straw tint on the gill cover (not the sardina's gold)
    "F": hx("#93b0a6"), "f": hx("#6f8e86"),    # dorsal fin: lit tip, fin
    "a": hx("#5f6d78"),                        # pelvic and anal fins (in the shade)
    "T": hx("#7a9a93"), "u": hx("#5f837c"), "t": hx("#4c6763"),  # tail: lit upper lobe, its base, shaded lower lobe
}

# Head lower left, tail upper right. Round 2 (critic): the snout runs to a point at 0,14 (a fin-toned tip past the lit
# 1,14) on the back's line; eye at 3,12, with no white touching it (2,13 is now the snout's grey-green). The mouth is
# one dark run from 2,14 through 3,13 to 4,13, back past the eye, then fades (J at 4,12); the pale lower jaw (3,14)
# sits under it, set back behind the tip, and 4,14 closes the belly outline. The body is 5 pixels across every row from the gill to the stalk (cigar), bands h k/m W s/g o along the
# diagonal, so the silver band W is one unbroken line from 6,10 to 10,6. The dorsal fin is a small triangle at
# 6-7,6-7 mid-back; pelvic (8,11) and anal (11,8) are single shaded pixels on the belly. The stalk (10-11,4) forks
# into an upper lobe up to 13,0 and a lower lobe right to 15,3, so the fish runs corner to corner, notch 13,3 open.
INCOVA = [
    ".............T..",
    "............T...",
    "...........TT...",
    "...........Tu.tt",
    "..........hkutt.",
    ".........hkgo...",
    "......FfhkWso...",
    "......fhkWgo....",
    "......hkWgoa....",
    ".....hmWso......",
    "....hmWso.......",
    "...hmGsoa.......",
    "..heJpo.........",
    ".hfjjo..........",
    "fhjpo...........",
    "................",
]

# Round 1 (critic: FIX), kept only for the compare sheet.
INCOVA_ROUND1 = [
    "................",
    "............T...",
    "...........TT...",
    "...........Tu.t.",
    "..........hkutt.",
    ".........hkgo...",
    "......FfhkWso...",
    "......fhkWgo....",
    "......hkWgoa....",
    ".....hmWso......",
    "....hmWso.......",
    "...hmGsoa.......",
    "..heJpo.........",
    ".hWjpo..........",
    ".hj.............",
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


def build(path, fins):
    """Body depth across the diagonal (pixels along x+y at one x-y) and the widest row, fins and tail left out."""
    im = Image.open(path).convert("RGBA")
    body = [(x, y) for y in range(16) for x in range(16)
            if im.getpixel((x, y))[3] and im.getpixel((x, y))[:3] not in fins]
    by_a = {}
    for x, y in body:
        by_a.setdefault(x - y, []).append(x + y)
    rows = {}
    for x, y in body:
        rows[y] = rows.get(y, 0) + 1
    return max(max(v) - min(v) + 1 for v in by_a.values()), max(rows.values()), len(body)


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


def tiles(band, im, x0, y0):
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, y0))
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
        t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + 136 + (j % 2) * 44, y0 + (j // 2) * 46))


ACCEPTED = ("sardina", "lampuka", "tonn", "cerna", "awrata", "murina", "pixxispad")


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 2230
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    # references
    refs = []
    for name in ("portugal.jpg", "ifremer1.jpg", "lonja.jpg", "gervais.jpg", "side.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((420, round(420 * im.height / im.width)), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = max(im.height for _, im in refs) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im, (10 + i * 432, 22))
            d.text((10 + i * 432, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References (art/references/fish_incova_refonly, list.tsv); colour from the fish out of water",
                      band))

    # palette
    keys = "hkmWsgoejJpGFfaTut"
    band = Image.new("RGB", (W, 54), bg)
    d = ImageDraw.Draw(band)
    for j, c in enumerate(keys):
        rgb = PAL[c]
        d.rectangle((10 + j * 92, 4, 10 + j * 92 + 88, 44), fill=rgb)
        d.text((10 + j * 92 + 3, 26), f"{c} #%02x%02x%02x" % rgb,
               fill=(255, 255, 255) if sum(rgb) < 380 else (0, 0, 0), font=label_font(12))
    parts.append(("Palette: back h k m, band W, flank s g, belly rim o, eye e, mouth j J, lower jaw p, gill G, "
                  "fins F f a, tail T u t", band))

    # 8x and 1x beside vanilla and the accepted fish
    items = [("INCOVA", None), ("vanilla cod", os.path.join(VANILLA, "cod.png")),
             ("vanilla salmon", os.path.join(VANILLA, "salmon.png"))]
    items += [(f"{n} (accepted)", os.path.join(TEXTURES, "item", f"{n}.png")) for n in ACCEPTED]
    per_row = 5
    rows_n = (len(items) + per_row - 1) // per_row
    band = Image.new("RGB", (W, rows_n * 170 + 24), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = icon if p is None else Image.open(p).convert("RGBA")
        x0, y0 = 10 + (i % per_row) * 440, 22 + (i // per_row) * 170
        tiles(band, im, x0, y0)
        d.text((x0, y0 - 20), name, fill=ink, font=small)
    d.text((10, rows_n * 170), "8x, then 1x and 2x on light and dark grey", fill=ink, font=small)
    parts.append(("The icon at 8x and 1x beside vanilla cod and salmon and the accepted fish", band))

    # round 2 beside round 1 and the sardina, 8x, 2x, 1x
    sard = Image.open(os.path.join(TEXTURES, "item", "sardina.png")).convert("RGBA")
    old = render(INCOVA_ROUND1, PAL_ROUND1)
    band = Image.new("RGB", (W, 128 + 40), bg)
    d = ImageDraw.Draw(band)
    x = 10
    for s in (8, 2, 1):
        for name, im in (("incova round 1", old), ("INCOVA round 2", icon), ("sardina", sard)):
            t = Image.new("RGBA", (16 * s + 8, 16 * s + 8), (139, 139, 139, 255))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
            band.paste(t.convert("RGB"), (x, 22))
            d.text((x, 2), f"{name} {s}x", fill=ink, font=small)
            x += max(16 * s + 20, 150)
        x += 30
    parts.append(("Round 2 (pointed snout, long mouth, longer tail) beside round 1 and the accepted sardina", band))

    # numbers
    paths = [os.path.join(VANILLA, "cod.png"), os.path.join(VANILLA, "salmon.png")]
    paths += [os.path.join(TEXTURES, "item", f"{n}.png") for n in ACCEPTED] + [OUT_ICON]
    lines = measure(paths)
    lines.append("STYLE.md food ranges: cover 0.29-0.77, colours 6-20, dark 0.0-0.35, light 0.32-0.99, TL-BR +0.01-+0.17")
    import fish_sardina_icon as sardina
    for n, fins in (("sardina", {sardina.PAL[c] for c in "faT"}), ("incova", {PAL[c] for c in "FfaTut"})):
        dep, wid, area = build(os.path.join(TEXTURES, "item", f"{n}.png"), fins)
        lines.append(f"{n} build: depth {dep} px across the diagonal, widest row {wid}, body {area} px "
                     "(fins and tail left out)")
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py", band))

    # offline hotbar preview (owner 2026-11-18: flat icons need no Minecraft run), at the GUI scale and at 4x
    py = os.path.join(ART, ".venv", "bin", "python")
    tool = os.path.join(ART, "tools", "hotbar_preview.py")
    row = ["mc:cod", "mod:sardina", "mod:incova", "mc:salmon", "mod:lampuka", "mod:tonn", "mod:cerna", "mod:awrata",
           "mod:murina"]
    hb = []
    for suffix, extra in (("", ["--scale", "2"]), ("_x4", ["--scale", "4"])):
        out = os.path.join(ART, "candidates", f"fish_incova_icon_hotbar{suffix}.png")
        subprocess.run([py, tool, out] + row + ["--select", "2"] + extra, check=True, capture_output=True)
        hb.append(Image.open(out).convert("RGB"))
    out = os.path.join(ART, "candidates", "fish_incova_icon_hotbar_pair.png")
    subprocess.run([py, tool, out, "mc:cod", "mod:sardina", "mod:incova", "mod:pixxispad", "--select", "2",
                    "--scale", "4"], check=True, capture_output=True)
    hb.append(Image.open(out).convert("RGB"))
    band = Image.new("RGB", (W, sum(im.height + 10 for im in hb) + 24), bg)
    y = 4
    for im in hb:
        band.paste(im, (10, y))
        y += im.height + 10
    ImageDraw.Draw(band).text((10, y), "art/tools/hotbar_preview.py: cod, sardina, INCOVA (selected), salmon, lampuka, "
                              "tonn, cerna, awrata, murina at scale 2 and 4; then cod, sardina, INCOVA, pixxispad at 4",
                              fill=ink, font=small)
    parts.append(("Hotbar preview (offline, as the game draws flat items)", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Incova (European anchovy) item icon, textures/item/incova.png", fill=ink, font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)


def main():
    check(INCOVA)
    icon = render(INCOVA)
    icon.save(OUT_ICON, optimize=False)
    sheet(icon)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), "and", os.path.relpath(OUT_SHEET, ROOT))


if __name__ == "__main__":
    main()
