"""Item icon for the golden pastizz: the accepted Pastizz tal-Irkotta (v4), turned gold the way vanilla turns food gold.

Owner (2026-11-18): "design 'the golden pastizz' a gold pastizz based on the pastizz tal-irkotta". The shape is the
accepted v4 pastizz exactly (`irkotta_v4()` in food_items.py, the same grid, pixel for pixel): its silhouette, its
end chevrons (the layer folds) and the ricotta lens peeking out of the seam. Only the colours change.

How vanilla turns food gold (art/.vanilla/item, studied at 8x, measured, never copied)
- golden_apple vs apple and golden_carrot vs carrot: the SAME pixels. The alpha mask is identical (0 pixels differ)
  and every pixel keeps its place in the shading ramp; it is a pure palette swap, one plain colour to one gold
  colour. The plain ramp's order is kept: the darkest red stays the darkest gold, the brightest stays brightest.
- The ramp is lifted hard and spread wide. The apple's red body (luminance 0.18-0.30) becomes gold at 0.43-0.89;
  the carrot's orange (0.30-0.79) becomes 0.43-0.99. Gold is much brighter and higher-contrast than the food.
- The hue slides along the ramp: dark gold is orange-brown (hue ~30), the middle is true gold (~42), the light
  tones turn lemon (~48 then ~61). Saturation stays high (~0.8) all the way up; there is no grey in it.
- The sparkle is the food's own highlight, pushed to near-white: the apple's 4 light pink pixels and the carrot's
  3 lightest become a near-white yellow (luminance 0.99). No new sparkle pixels are added on the apple or carrot.
  They sit where the plain food's highlight was: upper left, on the lit rim.
- The outline keeps its pixels but darkens a step to a deep warm red-brown (carrot 0.21 -> 0.12; apple 0.10 ->
  0.12). Parts that aren't the food itself stay apart: the apple's stem is unchanged, and the carrot's green top
  becomes a darker, duller olive-gold ramp (0.10-0.32) so it still reads as a separate part.
- glistering_melon_slice is the exception: it is redrawn (mirrored, 80 alpha pixels differ). Its rind becomes a
  gold ramp, but the red flesh stays red and gains pale pink and one pure white sparkle. That is the model for
  keeping the filling its own colour (candidate B below).
- The enchanted glint is not in any of these textures; the game draws it (the golden pastizz gets no glint here).

So the golden pastizz is a palette swap of v4: the pastry ramp (#, D, d, m, l, h) goes onto our own gold ramp with
the same hue slide, the top-left rim highlights (h) become lemon and a 3-pixel group nearest the top-left corner becomes a
near-white sparkle (as the apple's highlight does), and the outline darkens to a deep warm brown. The colours are
our own, picked by luminance and hue to sit on vanilla's curve, not taken from vanilla; the copy check below fails
the run if any colour or pixel matches a vanilla item texture.

Three candidates differ only in the ricotta:
  A  the ricotta turned gold too (the whole pastizz is metal, like the apple);
  B  the ricotta kept pale cream (like the glistering melon's flesh);
  C  the ricotta as a pale gold (in between).

Run:  art/.venv/bin/python art/src/food_golden_pastizz.py
Writes (byte-identical on rerun):
  mod/.../textures/item/golden_pastizz.png        the pick (PICK below)
  art/candidates/food_golden_pastizz.png          compare sheet: candidates at 1x, 2x and 8x beside the plain
                                                   pastizz, the vanilla golden apple and carrot and their plain ones
  art/candidates/food_golden_pastizz_hotbar.png   unselected hotbar (art/tools/hotbar_preview.py), scale 2 and 4
  art/candidates/food_golden_pastizz_hotbar_glint.png   the same with one simulated enchant-glint frame
  art/candidates/food_golden_pastizz_{a,b,c}.png  each candidate at 16x16
"""
import glob
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.dirname(ART)
VANILLA = os.path.join(ART, ".vanilla", "item")
TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
CAND = os.path.join(ART, "candidates")
OUT_ICON = os.path.join(TEXTURES, "item", "golden_pastizz.png")
OUT_SHEET = os.path.join(CAND, "food_golden_pastizz.png")
OUT_HOTBAR = os.path.join(CAND, "food_golden_pastizz_hotbar.png")
OUT_GLINT = os.path.join(CAND, "food_golden_pastizz_hotbar_glint.png")
PLAIN = os.path.join(TEXTURES, "item", "pastizz_irkotta.png")
PY = os.path.join(ART, ".venv", "bin", "python")

sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ART, "tools"))
import food_items  # noqa: E402  (the accepted v4 grid and its palette P3)
from font import label_font  # noqa: E402


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


# Our gold ramp, one colour per v4 symbol. Luminance / hue (vanilla's curve: 0.12 outline, dark ~0.43 hue ~30,
# mid ~0.64 hue ~42, light ~0.8 hue ~48, lemon ~0.9 hue ~60, sparkle ~0.98 near-white).
GOLD = {
    "#": hx("#4e1d0a"),  # outline: deep warm brown, a step darker than the pastry's #713c15
    "D": hx("#a65a0e"),  # layer gaps (the folds): dark orange-gold
    "d": hx("#c98314"),  # shadow side (lower right)
    "m": hx("#e1aa1a"),  # body
    "l": hx("#efd03c"),  # lit side (upper left)
    "h": hx("#f2f069"),  # rim highlights: lemon
    "*": hx("#fdfdd8"),  # sparkle: a 3-pixel group on the top-left rim (SPARKLE), near-white
}
RICOTTA = {
    "a": {"r": hx("#f6ef7e"), "R": hx("#e6c12e")},   # gold: lemon lens, its shaded half body-gold
    "b": {"r": food_items.P3["r"], "R": food_items.P3["R"]},  # the accepted v4 ricotta cream, unchanged
    "c": {"r": hx("#faf0b4"), "R": hx("#e3cd7c")},   # pale gold: cream pushed toward gold
}
NAMES = {"a": "A: ricotta gold", "b": "B: ricotta cream", "c": "C: ricotta pale gold"}
PICK = "c"
SPARKLE = [(5, 5), (4, 6), (5, 6)]


def grid():
    """The accepted v4 grid, with a 3-pixel sparkle cluster on the top-left rim: the two highlights nearest the
    corner, (5,5) and (4,6), and the lit pixel between them, (5,6). Critic round 1: a third sparkle at (3,9) stood
    alone and read as a stray white dot, so it stays a lemon highlight and the sparkle is one group, like vanilla's."""
    g = [list(r) for r in food_items.irkotta_v4()]
    for x, y in SPARKLE:
        assert g[y][x] in "hl", f"sparkle at {x},{y} is not on the lit rim"
        g[y][x] = "*"
    return g


def render(g, pal):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            if g[y][x] != ".":
                im.putpixel((x, y), pal[g[y][x]])
    return im


def check_base():
    """The grid is still the accepted icon: rendered in v4's palette it must equal pastizz_irkotta.png."""
    g = [list(r) for r in food_items.irkotta_v4()]
    plain = Image.open(PLAIN).convert("RGBA")
    mine = render(g, food_items.P3)
    for y in range(16):
        for x in range(16):
            a, b = plain.getpixel((x, y)), mine.getpixel((x, y))
            assert (a[3] == 0 and b[3] == 0) or a == b, f"v4 grid no longer matches pastizz_irkotta.png at {x},{y}"


def copy_check(icon, allow=()):
    """No pixel may match the same pixel of any vanilla item texture, and no colour may be a vanilla item colour
    (STYLE rule 3). `allow` lists colours that are ours by design (the plain pastizz's own ricotta in B)."""
    ours = {(x, y): icon.getpixel((x, y)) for x in range(16) for y in range(16) if icon.getpixel((x, y))[3] > 0}
    hits, vcols = [], set()
    for f in sorted(glob.glob(os.path.join(VANILLA, "*.png"))):
        v = Image.open(f).convert("RGBA")
        if v.size[0] != 16 or v.size[1] < 16:
            continue
        same = [p for p, c in ours.items() if v.getpixel(p) == c]
        if same:
            hits.append((len(same), os.path.basename(f)))
        vcols |= {v.getpixel((x, y))[:3] for x in range(16) for y in range(16) if v.getpixel((x, y))[3] > 0}
    shared = {c[:3] for c in ours.values()} & vcols - {c[:3] for c in allow}
    assert not hits, f"copies vanilla pixels: {hits}"
    assert not shared, f"uses vanilla colours: {sorted(shared)}"
    return len(ours)


def glint(icon, phase=0):
    """One simulated enchant-glint frame: a soft purple diagonal band added over the opaque pixels (the game draws
    the real one, animated; this is only to judge the icon under it)."""
    out = icon.copy()
    for y in range(16):
        for x in range(16):
            c = icon.getpixel((x, y))
            if c[3] == 0:
                continue
            t = ((x - y + phase) % 12) / 12.0
            k = max(0.0, 1 - abs(t - 0.5) * 4) * 0.55 + 0.12
            add = (int(128 * k), int(64 * k), int(204 * k))
            out.putpixel((x, y), tuple(min(255, c[i] + add[i]) for i in range(3)) + (255,))
    return out


def hotbar(items, scale):
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "h.png")
        subprocess.run([PY, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items + ["--scale", str(scale)],
                       check=True, capture_output=True)
        return Image.open(out).convert("RGB")


def hotbar_sheet(cands, glinted, path):
    with tempfile.TemporaryDirectory() as td:
        items = ["mc:bread", "mc:apple", "mc:golden_apple", "mc:golden_carrot", "mod:pastizz_irkotta"]
        for k in "abc":
            im = glint(cands[k]) if glinted else cands[k]
            p = os.path.join(td, f"{k}.png")
            im.save(p)
            items.append("file:" + p)
        if glinted:  # the golden apple under the same simulated glint, for comparison
            p = os.path.join(td, "ga.png")
            glint(Image.open(os.path.join(VANILLA, "golden_apple.png")).convert("RGBA")).save(p)
            items[2] = "file:" + p
        rows = [hotbar(items, s) for s in (2, 4)]
    w = max(r.width for r in rows)
    sheet = Image.new("RGB", (w, sum(r.height for r in rows) + 10), (139, 139, 139))
    y = 0
    for r in rows:
        sheet.paste(r, (0, y))
        y += r.height + 10
    sheet.save(path, optimize=False)


def compare_sheet(cands):
    ink, bg = (235, 235, 235), (48, 48, 52)
    def v(n):
        return Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")
    tiles = [("plain pastizz (v4)", Image.open(PLAIN).convert("RGBA"))]
    tiles += [(NAMES[k] + (" (pick)" if k == PICK else ""), cands[k]) for k in "abc"]
    tiles += [("vanilla apple", v("apple")), ("vanilla golden apple", v("golden_apple")),
              ("vanilla carrot", v("carrot")), ("vanilla golden carrot", v("golden_carrot"))]
    tw = 150
    W = 10 + tw * len(tiles)
    H = 230
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    small = label_font(11)
    for i, (name, im) in enumerate(tiles):
        x0 = 10 + i * tw
        d.text((x0, 4), name, fill=(250, 210, 120) if "pick" in name else ink, font=small)
        tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
        tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
        sheet.paste(tile.convert("RGB"), (x0, 22))
        for j, (back, s) in enumerate((((198, 198, 198), 1), ((198, 198, 198), 2), ((60, 60, 64), 1),
                                        ((60, 60, 64), 2))):
            t = Image.new("RGBA", (16 * s + 4, 16 * s + 4), back + (255,))
            t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (2, 2))
            sheet.paste(t.convert("RGB"), (x0 + [0, 22, 62, 84][j], 160))
    d.text((10, 208), "8x, then 1x and 2x on light and dark grey. The glint is the game's; see the _hotbar_glint sheet.",
           fill=ink, font=small)
    sheet.save(OUT_SHEET, optimize=False)


def main():
    check_base()
    g = grid()
    cands = {}
    for k in "abc":
        pal = dict(GOLD)
        pal.update(RICOTTA[k])
        cands[k] = render(g, pal)
        n = copy_check(cands[k], allow=RICOTTA["b"].values() if k == "b" else ())
        cands[k].save(os.path.join(CAND, f"food_golden_pastizz_{k}.png"), optimize=False)
        print(f"{k}: {n} px, no vanilla pixel or colour copied")
    cands[PICK].save(OUT_ICON, optimize=False)
    compare_sheet(cands)
    hotbar_sheet(cands, False, OUT_HOTBAR)
    hotbar_sheet(cands, True, OUT_GLINT)
    for p in (OUT_ICON, OUT_SHEET, OUT_HOTBAR, OUT_GLINT):
        print("wrote", os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
