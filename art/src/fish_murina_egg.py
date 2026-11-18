"""Murina spawn egg: the item icon (16 x 16), 2026-11-18.

Built the way vanilla 26.3 builds its new per-mob spawn eggs (decisions "2026-11-18 Spawn eggs show the animal" and
"2026-11-18 Sardina egg - a representation, not a fat fish"), measured from the fish ones (cod, salmon, tropical_fish
and pufferfish _spawn_egg in art/.vanilla/item, measured, never copied) and following our accepted lampuka, tonn,
sardina and cerna eggs: the whole egg outline is kept (narrow top on rows 2 to 3, widening to its full width low down,
standing in a pool) and the moray is painted onto it as a stylised token, not drawn as a whole eel.

The murina (Mediterranean moray, Muraena helena) is a long, medium-heavy fish. Round 2 (after the critic) keeps it
within x 1 to 14 (the body x 1 to 13, widest at rows 8 to 10), the top at row 3 below the crest, cover about 0.59.
At 1x it reads by:
- the broad head filling the left of the egg, facing left, lit on its upper left, with the crown at the top (row 3);
- one small pale eye at (6,5) in a darker socket (a tone-4 pixel right of it): the only pale mark on the head; no
  cream spot left of x 8 or in row 5;
- a pointed snout over rows 7 to 9 (tip at 1,8) and the long dark mouth line from it, bending down at its corner
  (5,9) as the moray's gape does, with the lower jaw in its own darker tone under it; no teeth, no second eye;
- the low continuous fin along the back: a lit ridge (row 2, x 8 to 11) stepping down the right shoulder (12,3 and
  13,4-5); it breaks the top outline as vanilla's fish fins do. No side fins: the moray has no pectoral fins;
- no tail: a lit tail tip flicking up out of the pool at the lower right was tried in round 2 and taken out at the
  owner's request (2026-11-18, "3 disconnected pixels at the right side"); the pool fills its place again;
- the violet-brown body mostly in the lit tones 1 to 3 of the icon's ramp, 4 and 5 only at the shaded edge, a 1 px
  shaded rim stepping in 1 to 3 px runs, the bottom corners rounded into the pool, and the body mottled with cream
  spots that take the light (bright on the lit upper body, tan in the middle, dull mauve in the shade).
Round 1 (shown on the sheet) filled x 0 to 15 with straight walls and a darker interior, and read as a sibling of the
cerna egg.
The pool is our own: a teal ramp (not vanilla's shared water-mob blues, nor the lampuka's, tonn's, sardina's or
cerna's), with its own shape: ripples curling up at both ends of the top row, the widest row in the middle and a
narrow, broken bottom row.
Colours are all the accepted murina item icon's (art/src/fish_murina_icon.py PAL), plus the pool.
Photos (reference only): art/references/fish_murina_refonly/ (list.tsv).

Run:    art/.venv/bin/python art/src/fish_murina_egg.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/murina_spawn_egg.png (byte-identical on rerun) and
        art/candidates/fish_murina_egg.png (compare sheet), with the offline hotbar previews
        art/candidates/fish_murina_egg_hotbar.png and fish_murina_egg_hotbar_x4.png (art/tools/hotbar_preview.py).
"""
import glob
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
OUT_ICON = os.path.join(TEXTURES, "item", "murina_spawn_egg.png")
OUT_SHEET = os.path.join(ART, "candidates", "fish_murina_egg.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")
REFS = os.path.join(ART, "references", "fish_murina_refonly")
OUT_HOTBAR = os.path.join(ART, "candidates", "fish_murina_egg_hotbar.png")
OUT_HOTBAR4 = os.path.join(ART, "candidates", "fish_murina_egg_hotbar_x4.png")
OUR_EGGS = ("lampuka", "tonn", "sardina", "cerna")


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PAL = {
    # the murina: the accepted item icon's colours (art/src/fish_murina_icon.py PAL)
    "1": hx("#8c6a6a"), "2": hx("#765660"), "3": hx("#62464e"), "4": hx("#503a40"), "5": hx("#433036"),  # lit to shade
    "k": hx("#705660"),  # lit rim: the top of the head and the crown
    "o": hx("#2a1a1f"),  # shaded rim: the right side, under the egg, the dip in front of the fin
    "C": hx("#e2d09c"), "c": hx("#b49c84"), "d": hx("#806a6c"),  # cream mottle: in the light, mid, in the shade
    "E": hx("#f0e8bc"),  # the small pale eye
    "L": hx("#866670"),  # the snout tip and the lit ridge of the back fin
    "l": hx("#5c4650"),  # the lower jaw and the shaded end of the back fin
    "M": hx("#200f14"),  # the mouth line
    # the pool: our own teal ramp
    "p": hx("#183a4a"),
    "q": hx("#21607a"),
    "r": hx("#2c88a2"),
    "s": hx("#4caec6"),
    "w": hx("#ace6ee"),
}

GRID = [
    "................",
    "................",
    "........LLLL....",
    "......k11122L...",
    "....k1111c22ol..",
    "....k1E41122ol..",
    "...k11112C22o...",
    "..k1111122c2o...",
    ".LMMM1222d2C3o..",
    "..lllM12c22d3o..",
    "...lk21222c2do..",
    "...k1122d222o...",
    "....k1222222o...",
    ".qrsqoooooooqsq.",
    ".prsrrwssrwrsrp.",
    "..pqqppqqppqqp..",
]

# round 1 (sent back by the critic: too big, straight walls, too dark, a sibling of the cerna egg), kept only
# to show on the sheet
PREV_GRID = [
    "................",
    "................",
    "......kk.LLLk...",
    ".....k11kL5434L.",
    "....k1112c33c4ol",
    "...k1E1123C34o..",
    "..k1111223c3d4o.",
    ".L112222dC3c34o.",
    "L1MMM22233d3d45o",
    ".llllM23C3c4d45o",
    "..lk2d23d34c445o",
    "...k23d23d44d5o.",
    "...oo3c34d4555o.",
    ".qrooooooooooorp",
    ".prsrrwssrwrsrp.",
    "...pqppqqppqp...",
]


def render(rows, changes=None):
    pal = dict(PAL, **(changes or {}))
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), pal[ch] + (255,))
    return im


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<26} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def copy_check(icon):
    """Exact-pixel copy check against every vanilla spawn egg (as art/candidates/critic_sardina_egg_v5/check.py),
    and the pool colours against our other eggs."""
    ours = {(x, y): icon.getpixel((x, y)) for x in range(16) for y in range(16) if icon.getpixel((x, y))[3] > 0}
    hits = []
    vcols = set()
    for f in sorted(glob.glob(os.path.join(VANILLA, "*spawn_egg*.png"))):
        v = Image.open(f).convert("RGBA")
        if v.size != (16, 16):
            continue
        same = [p for p, c in ours.items() if v.getpixel(p) == c]
        if same:
            hits.append((len(same), os.path.basename(f)))
        vcols |= {v.getpixel((x, y))[:3] for x in range(16) for y in range(16) if v.getpixel((x, y))[3] > 0}
    shared = {c[:3] for c in ours.values()} & vcols
    hits.sort(reverse=True)
    most = f"most: {hits[0][0]} in {hits[0][1]}" if hits else "none"
    pool = {PAL[k] for k in "pqrsw"}
    egg_cols = set()
    for n in OUR_EGGS:
        e = Image.open(os.path.join(TEXTURES, "item", n + "_spawn_egg.png")).convert("RGBA")
        egg_cols |= {e.getpixel((x, y))[:3] for x in range(16) for y in range(16) if e.getpixel((x, y))[3] > 0}
    return [f"same pixel and colour as a vanilla spawn egg: {sum(n for n, _ in hits)} pixels over {len(hits)} eggs ({most})",
            f"our colours also used by any vanilla spawn egg: {len(shared)}",
            f"pool colours also used by our lampuka, tonn, sardina or cerna egg: {len(pool & egg_cols)}"]


def tile_row(d, band, x0, name, im, small, ink):
    tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
    tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
    band.paste(tile.convert("RGB"), (x0, 22))
    d.text((x0, 2), name, fill=ink, font=small)
    for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1), ((40, 40, 40), 2))):
        t = Image.new("RGBA", (40, 40), col + (255,))
        t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
        band.paste(t.convert("RGB"), (x0 + (j % 2) * 44 + (j // 2) * 88, 156))


def sheet(icon):
    font, small = label_font(16), label_font(13)
    W = 2400
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    refs = []
    for name in ("m10.jpg", "m11.jpg", "m08.jpg", "m13.jpg", "o04.jpg", "o01.jpg"):
        p = os.path.join(REFS, name)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((310, round(310 * im.height / im.width)), Image.LANCZOS)
            refs.append((name, im))
    if refs:
        h = max(im.height for _, im in refs) + 26
        band = Image.new("RGB", (W, h), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(refs):
            band.paste(im, (10 + i * 320, 22))
            d.text((10 + i * 320, 2), f"{name} (reference only)", fill=ink, font=small)
        parts.append(("References (art/references/fish_murina_refonly, list.tsv): out of water for the colour, "
                      "heads for the crown, eye and mouth", band))

    bucket = Image.open(os.path.join(VANILLA, "cod_bucket.png")).convert("RGBA")
    bucket.alpha_composite(Image.open(os.path.join(TEXTURES, "item", "murina_bucket.png")).convert("RGBA"))
    items = [("vanilla cod egg", os.path.join(VANILLA, "cod_spawn_egg.png")),
             ("vanilla salmon egg", os.path.join(VANILLA, "salmon_spawn_egg.png")),
             ("vanilla tropical fish egg", os.path.join(VANILLA, "tropical_fish_spawn_egg.png")),
             ("vanilla pufferfish egg", os.path.join(VANILLA, "pufferfish_spawn_egg.png"))]
    items += [(f"our {n} egg", os.path.join(TEXTURES, "item", n + "_spawn_egg.png")) for n in OUR_EGGS]
    items += [("NEW MURINA EGG", icon),
              ("murina item icon", os.path.join(TEXTURES, "item", "murina.png")),
              ("murina bucket", bucket)]
    band = Image.new("RGB", (W, 128 + 120), bg)
    d = ImageDraw.Draw(band)
    for i, (name, p) in enumerate(items):
        im = p if isinstance(p, Image.Image) else Image.open(p).convert("RGBA")
        tile_row(d, band, 10 + i * 214, name, im, small, ink)
    d.text((10, 202), "8x, then 1x and 2x on light grey, 1x and 2x on dark grey", fill=ink, font=small)
    parts.append(("The egg at 8x and 1x beside vanilla's fish eggs, our accepted lampuka, tonn, sardina and cerna eggs "
                  "and the accepted murina item icon and bucket", band))

    band = Image.new("RGB", (W, 128 + 120), bg)
    d = ImageDraw.Draw(band)
    tile_row(d, band, 10, "round 1 (sent back)", render(PREV_GRID), small, ink)
    tile_row(d, band, 224, "NEW (round 2)", icon, small, ink)
    tile_row(d, band, 438, "our cerna egg", Image.open(os.path.join(TEXTURES, "item", "cerna_spawn_egg.png"))
             .convert("RGBA"), small, ink)
    sil = Image.new("RGBA", (16 * 3 + 8, 16), (0, 0, 0, 0))
    for i, im in enumerate((render(PREV_GRID), icon,
                            Image.open(os.path.join(TEXTURES, "item", "cerna_spawn_egg.png")).convert("RGBA"))):
        a = im.split()[3].point(lambda v: 255 if v else 0)
        sil.paste(Image.new("RGBA", (16, 16), (20, 20, 20, 255)), (i * 20, 0), a)
    t = Image.new("RGBA", (sil.width * 4 + 8, 72), (139, 139, 139, 255))
    t.alpha_composite(sil.resize((sil.width * 4, 64), Image.NEAREST), (4, 4))
    band.paste(t.convert("RGB"), (660, 22))
    d.text((660, 2), "silhouettes at 4x: round 1, new, cerna", fill=ink, font=small)
    d.text((660, 110), "New: pulled in to x 1-14 (body x 1-13, widest at rows 8-10), top at row 3 below the crest;",
           fill=ink, font=small)
    d.text((660, 128), "right side stepped, bottom corners rounded into the pool, a 1 px shaded rim, interior one "
           "tone lighter;", fill=ink, font=small)
    d.text((660, 146), "no cream spot on the head or in row 5, the eye in a darker socket; a pointed snout over rows "
           "7-9.", fill=ink, font=small)
    d.text((660, 164), "The tail tip at the lower right was taken out at the owner's request; the pool fills its place.",
           fill=ink, font=small)
    parts.append(("Round 1 and round 2 beside the cerna egg", band))

    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "salmon", "tropical_fish", "pufferfish")]
                    + [os.path.join(TEXTURES, "item", n + "_spawn_egg.png") for n in OUR_EGGS] + [OUT_ICON])
    lines += copy_check(icon)
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py and the copy check", band))

    py = os.path.join(ART, ".venv", "bin", "python")
    items = ["mc:cod_spawn_egg", "mod:cerna_spawn_egg", "mod:murina_spawn_egg", "mod:murina"]
    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items +
                       ["--select", "2", "--scale", str(scale)], check=True, capture_output=True)
    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        im = Image.open(out).convert("RGB")
        band = Image.new("RGB", (W, im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(out, ROOT) + f"  (GUI scale {scale}: vanilla cod "
                                  "egg; our cerna egg; MURINA EGG (selected); murina item icon)", fill=ink, font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py, GUI scale {scale})", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Murina (Mediterranean moray) spawn egg, textures/item/murina_spawn_egg.png", fill=ink,
           font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    out.save(OUT_SHEET)
    print("wrote", OUT_SHEET)


if __name__ == "__main__":
    icon = render(GRID)
    icon.save(OUT_ICON, optimize=False)
    print("wrote", OUT_ICON)
    sheet(icon)
