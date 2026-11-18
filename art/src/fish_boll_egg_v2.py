"""Boll (common stingray, Dasyatis pastinaca) spawn egg, second start: the item icon (16 x 16), 2026-11-18.

Owner 2026-11-18 (docs/Decisions/2026-11-18 Boll egg - start fresh, egg with nostrils and mouth only.md):
"start fresh on the stingray egg. it should read as an egg, with the stingray pallet, and its underside nostrils
and mouth features. thats it no tail or others". So every candidate here is a plain egg, nothing else:
- the egg outline of vanilla 26.x's water-mob eggs (measured from cod, salmon and squid _spawn_egg in
  art/.vanilla/item, never copied): a 4 px top on row 3 widening downward to 12 px on rows 9-12, its bottom edge on
  row 13 (x 5-10), standing in vanilla's own pool on rows 12-15 (art/src/egg_pool.py; owner 2026-11-18, "the pool
  under the egg should be the same as vanilla", the owner's exception to "never copy", for the pool only; it
  replaced our own pool, whose water ran under the egg on row 13); nothing pokes out of the outline;
- shaded as a rounded egg lit from the top left: the lightest cream at the upper left, rolling through the mid
  creams to the shade at the lower right;
- the only features are the ray underside's two nostrils and the mouth below them, drawn the way the accepted
  bucket N2 draws them (2 px tall nostrils in the icon's darkest brown 4, the mouth in its 3); no eye, tail, wings,
  fins, spots or other marks.
For the boll this replaces the general egg rules (cap, eye, fin flaps, parts breaking the outline).

Colours: only the accepted boll icon's (art/src/fish_boll_icon_v5.py PAL, candidate C: o L H 1 2 3 4) and the
accepted bucket's (art/src/fish_boll_bucket.py PAL, candidate N2: the creams W w s, the nostrils n and mouth m,
the water ~ v ^, now unused), plus vanilla's pool (P in the grids). Nothing else new.

Candidates (the sheet shows all of them; PICK is written to the mod). The owner picked B (2026-11-18, "for the
stingray b is the best"; docs/Decisions/2026-11-18 Boll egg B; egg pools match vanilla.md):
- A, cream egg, olive rim: the whole egg is the pale underside, its shaded lower right rolling into the olive back
  (H 1 2) just inside the outline, the way a ray's dark back shows round the edge of its belly. Nostrils across the
  middle (x6 and x9, rows 8-9), the mouth just under them (x7-8, row 10), the size of N2's face.
- B, olive egg, cream face: the reverse, the egg is the olive back (L H 1 2 3) and the cream underside is a wide
  patch on the lower front carrying the nostrils (x5 and x10, rows 9-10) and the mouth (x6-9, row 11).
- C, cream egg, olive cap: the underside with an olive cap edge over the top (rows 3-5), lit at its upper left;
  a bigger face lower down, nostrils wide apart (x5 and x10, rows 9-10) over a 4 px mouth (x6-9, row 11).
- D, cream egg, olive rim, big face high: as A but the face larger and higher, nostrils (x5 and x10, rows 7-8)
  over a 4 px mouth (x6-9, row 10), and no pool: a plain egg standing on its own, rows 2-15.
- A2, A3, A4: critic round 1's fixes for A (see the comments at their grids): slanted nostril slits and an arched
  mouth (A2), plus a thin olive edge over the top (A3), or with C's flat 4 px mouth (A4).
Blind reads (3 fresh readers, each egg alone among vanilla water-mob spawn eggs in a hotbar, no context):
- A: "a plain cream egg with a smiley face, probably a spawn egg, but I can't tell which creature it is for" /
  "a plain cream-coloured egg with a cartoon smiley face (two dot eyes and a smile)" / "A pale cream egg with a cute
  face, probably a spawn-egg-style item, but I can't tell which creature".
- B: "a tan or khaki egg with one dark eye and a mouth, probably a spawn egg for some drab, rounded creature (maybe
  a fish)" / "a darker khaki or olive egg-shaped item with a face" / "A khaki or olive egg with one eye ... maybe a
  shelled or snail-like animal".
- C: "a cream egg with a smiley face, probably a spawn egg" / "a cream egg with a smiley face" / "The same pale
  cream smiling egg".
- D: "a cream egg with a smiley face, which reads as an ordinary food egg (like a chicken egg)" / "a plain cream
  egg with a smiley face" / "A plain cream egg with a face, ... maybe an ordinary or food egg".
- A2, A3, A4 (the readers could not tell them apart at 1x): "a spawn egg, creature unclear. It looks most like a
  pale, round, frowning fish such as a grouper or a blobfish" / "A pale beige, frowning blob creature. It reads most
  like a blobfish" / "A spawn egg for a pale, round, frowning sea creature. It reads most like a blobfish".
  The slants turned the face into a frown and lost the egg read for one reader, so A stays the pick: all three
  readers read it as an egg, two as a spawn egg; none named a ray.

Run:    art/.venv/bin/python art/src/fish_boll_egg_v2.py
Writes: mod/src/main/resources/assets/mimcontent/textures/item/boll_spawn_egg.png (the PICK, byte-identical on
        rerun), art/candidates/fish_boll_egg_v2.png (the compare sheet) and the offline hotbar previews
        art/candidates/fish_boll_egg_v2_hotbar.png and fish_boll_egg_v2_hotbar_x4.png (art/tools/hotbar_preview.py,
        GUI scale 2 and 4, nothing selected).
"""
import glob
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
from fish_boll_icon_v5 import PAL as ICON  # noqa: E402
from fish_boll_bucket import PAL as BUCKET  # noqa: E402
from egg_pool import POOL as VANILLA_POOL, is_pool, pool_line  # noqa: E402

TEXTURES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures")
ITEMS = os.path.join(TEXTURES, "item")
OUT_ICON = os.path.join(ITEMS, "boll_spawn_egg.png")
CAND = os.path.join(ART, "candidates")
OUT_SHEET = os.path.join(CAND, "fish_boll_egg_v2.png")
OUT_HOTBAR = os.path.join(CAND, "fish_boll_egg_v2_hotbar.png")
OUT_HOTBAR4 = os.path.join(CAND, "fish_boll_egg_v2_hotbar_x4.png")
VANILLA = os.path.join(os.environ.get("MIM_VANILLA_TEXTURES", os.path.join(ART, ".vanilla")), "item")

# the icon's keys (outline, olive back from lit to shade) and the bucket's (creams, nostrils, mouth, water)
PAL = {k: ICON[k] for k in "oLH1234"}
PAL.update({k: BUCKET[k] for k in "Wwsnm~v^"})

# vanilla's pool (P: each pixel takes vanilla's own colour from art/src/egg_pool.py), with the egg's bottom edge in
# its outline colour on row 13, x 5-10, where vanilla's eggs have theirs; rows 12's pool pixels (3 and 12) lie under
# the boll's wide egg. Our own pool before it (rows 13-15, 1-14 / 1-14 / 3-12, water under the egg on row 13):
#   ".o~vvvvvvvvvv~o.", ".ov~^~~~~~~^~vo.", "...oooooooooo..."
POOL = [
    "..PPPooooooPPP..",
    "..PPPPPPPPPPPP..",
    "...PPPPPPPPPP...",
]

CANDIDATES = {
    # A, the critic's pick (critic round 2: PASS); the owner picked B
    "A": [
        "................",
        "................",
        "................",
        "......oooo......",
        ".....oWWwso.....",
        "....oWWWwwso....",
        "....oWWwwwso....",
        "...oWWwwwwsHo...",
        "..oWWwnwwnsH1o..",
        "..oWwwnwwnsH1o..",  # critic round 2 polish: (10,9) s, (11,9) H, the rim ramp unbroken
        "..oWwwwmmwsH1o..",
        "..owwwwwwssH2o..",
        "..oHswwwssH12o..",
    ] + POOL,
    "B": [
        "................",
        "................",
        "................",
        "......oooo......",
        ".....oLLH1o.....",
        "....oLLHH12o....",
        "....oLHH112o....",
        "...oLH111223o...",
        "..oH11WWws233o..",
        "..oH1WnWwns23o..",
        "..oH1wnwwns23o..",
        "..o11swmmws33o..",
        "..o122sss2334o..",
    ] + POOL,
    "C": [
        "................",
        "................",
        "................",
        "......oooo......",
        ".....oLLH1o.....",
        "....oLHH112o....",
        "....oWWWw12o....",
        "...oWWWwwws1o...",
        "..oWWWwwwwsH1o..",
        "..oWwnwwwwnsHo..",
        "..oWwnwwwwns1o..",
        "..owwwmmmmss1o..",
        "..oHswwwssH12o..",
    ] + POOL,
    # D: no pool, a plain egg standing on its own (rows 2-15)
    "D": [
        "................",
        "................",
        "......oooo......",
        ".....oWWwso.....",
        "....oWWWwwso....",
        "....oWWwwwso....",
        "...oWWwwwwsHo...",
        "...oWWwwwwsHo...",
        "..oWwnwwwwnsHo..",
        "..oWwnwwwwns1o..",
        "..owwwmmmmsH1o..",
        "..owwwwwwssH1o..",
        "..oHswwwssH12o..",
        "...oHsssHH12o...",
        "....o11H122o....",
        ".....oooooo.....",
    ],
    # A2: critic round 1's fix for A (A read as "a cream egg with a smiley face": round 2 px dots over a short line).
    # The nostrils are slanted slits, outer ends high (5,7) (10,7), inner ends low (6,8) (9,8), as on a real ray's
    # underside; the mouth a shallow arch, (7-8,10) with its corners down at (6,11) (9,11), not a grin; olive H at
    # (3,11) so the shaded margin frames the belly.
    "A2": [
        "................",
        "................",
        "................",
        "......oooo......",
        ".....oWWwso.....",
        "....oWWWwwso....",
        "....oWWwwwso....",
        "...oWnwwwwnHo...",
        "..oWWwnwwnsH1o..",
        "..oWwwwwwwws1o..",
        "..oWwwwmmwsH1o..",
        "..oHwwmwwmsH2o..",
        "..oHswwwssH12o..",
    ] + POOL,
    # A3: A2 with the olive back showing as a thin edge over the top (row 4, lit L at the upper left)
    "A3": [
        "................",
        "................",
        "................",
        "......oooo......",
        ".....oLLH1o.....",
        "....oWWWwwso....",
        "....oWWwwwso....",
        "...oWnwwwwnHo...",
        "..oWWwnwwnsH1o..",
        "..oWwwwwwwws1o..",
        "..oWwwwmmwsH1o..",
        "..oHwwmwwmsH2o..",
        "..oHswwwssH12o..",
    ] + POOL,
    # A4: A3 with C's wide flat mouth (x6-9, row 10) under the slanted nostrils
    "A4": [
        "................",
        "................",
        "................",
        "......oooo......",
        ".....oLLH1o.....",
        "....oWWWwwso....",
        "....oWWwwwso....",
        "...oWnwwwwnHo...",
        "..oWWwnwwnsH1o..",
        "..oWwwwwwwws1o..",
        "..oWwwmmmmsH1o..",
        "..oHwwwwwssH2o..",
        "..oHswwwssH12o..",
    ] + POOL,
}
# the egg outline each candidate must fill exactly (x from, x to per row), so nothing pokes out
EGG_POOL = {3: (6, 9), 4: (5, 10), 5: (4, 11), 6: (4, 11), 7: (3, 12), 8: (2, 13), 9: (2, 13), 10: (2, 13),
            11: (2, 13), 12: (2, 13), 13: (2, 13), 14: (2, 13), 15: (3, 12)}
EGG_PLAIN = {2: (6, 9), 3: (5, 10), 4: (4, 11), 5: (4, 11), 6: (3, 12), 7: (3, 12), 8: (2, 13), 9: (2, 13),
             10: (2, 13), 11: (2, 13), 12: (2, 13), 13: (3, 12), 14: (4, 11), 15: (5, 10)}
OUTLINE = {"A": EGG_POOL, "B": EGG_POOL, "C": EGG_POOL, "D": EGG_PLAIN, "A2": EGG_POOL, "A3": EGG_POOL, "A4": EGG_POOL}
PICK = "B"  # the owner, 2026-11-18: "for the stingray b is the best"


def check_outline(name, rows):
    """Every opaque pixel lies inside the egg outline and the outline is filled: nothing pokes out, no gaps."""
    mask = OUTLINE[name]
    for y, row in enumerate(rows):
        lo, hi = mask.get(y, (99, -1))
        for x, ch in enumerate(row):
            assert (ch != ".") == (lo <= x <= hi), f"{name}: pixel ({x},{y}) breaks the egg outline"


def render(rows):
    assert len(rows) == 16
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch == "P":
                im.putpixel((x, y), VANILLA_POOL[(x, y)] + (255,))
            elif ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
    return im


def measure(paths):
    py = os.path.join(ART, ".venv", "bin", "python")
    res = subprocess.run([py, os.path.join(ART, "tools", "measure.py")] + paths, capture_output=True, text=True)
    lines = []
    for line in res.stdout.splitlines():
        if line.startswith("{"):
            d = eval(line, {"np": __import__("numpy")})  # measure.py prints dicts with numpy floats
            lines.append(f"{d['file']:<30} cover {d['coverage']:.2f}  colours {d['colours']:>2}  dark {d['lmin']:.2f}  "
                         f"light {d['lmax']:.2f}  edge {d['edge_l']:.2f}  inside {d['interior_l']:.2f}  "
                         f"TL-BR {d['tl_minus_br']:+.2f}")
    return lines


def copy_check(name, icon):
    """Exact-pixel copy check against every vanilla spawn egg (as the other fish egg scripts). Vanilla's own pool
    pixels are allowed (the owner's exception, art/src/egg_pool.py); any other copied pixel fails the run."""
    ours = {(x, y): icon.getpixel((x, y)) for x in range(16) for y in range(16) if icon.getpixel((x, y))[3] > 0}
    hits, vcols = [], set()
    for f in sorted(glob.glob(os.path.join(VANILLA, "*spawn_egg*.png"))):
        v = Image.open(f).convert("RGBA")
        if v.size != (16, 16):
            continue
        same = [p for p, c in ours.items() if v.getpixel(p) == c and not is_pool(p, c)]
        if same:
            hits.append((len(same), os.path.basename(f)))
        vcols |= {v.getpixel((x, y))[:3] for x in range(16) for y in range(16) if v.getpixel((x, y))[3] > 0}
    shared = {c[:3] for p, c in ours.items() if not is_pool(p, c)} & vcols
    hits.sort(reverse=True)
    most = f"most: {hits[0][0]} in {hits[0][1]}" if hits else "none"
    pool = "" if name == "D" else "; " + pool_line(icon)  # D stands on its own, no pool
    return (f"{name}: same pixel and colour as a vanilla spawn egg, besides its pool: {sum(n for n, _ in hits)} pixels "
            f"over {len(hits)} eggs ({most}); our colours (besides the pool) also used by any vanilla spawn egg: "
            f"{len(shared)}{pool}"), sum(n for n, _ in hits)


def sheet(icons):
    font, small = label_font(16), label_font(13)
    W = 2400
    bg, ink = (52, 52, 56), (235, 235, 235)
    parts = []

    def van(n):
        return Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")

    def ours(n):
        return Image.open(os.path.join(ITEMS, n + ".png")).convert("RGBA")

    bucket = van("cod_bucket")
    bucket.alpha_composite(ours("boll_bucket"))
    items = ([(f"CANDIDATE {n}{' (PICK)' if n == PICK else ''}", im) for n, im in icons.items()] +
             [("vanilla cod egg", van("cod_spawn_egg")), ("vanilla salmon egg", van("salmon_spawn_egg")),
              ("vanilla squid egg", van("squid_spawn_egg")), ("vanilla pufferfish egg", van("pufferfish_spawn_egg")),
              ("our cerna egg", ours("cerna_spawn_egg")), ("our tonn egg", ours("tonn_spawn_egg")),
              ("boll icon (accepted)", ours("boll")), ("boll bucket N2 (accepted)", bucket)])
    per = 10
    for start in range(0, len(items), per):
        chunk = items[start:start + per]
        band = Image.new("RGB", (W, 128 + 110), bg)
        d = ImageDraw.Draw(band)
        for i, (name, im) in enumerate(chunk):
            x0 = 10 + i * 236
            tile = Image.new("RGBA", (128, 128), (139, 139, 139, 255))
            tile.alpha_composite(im.resize((128, 128), Image.NEAREST))
            band.paste(tile.convert("RGB"), (x0, 22))
            d.text((x0, 2), name, fill=ink, font=small)
            for j, (col, s) in enumerate((((139, 139, 139), 1), ((139, 139, 139), 2), ((40, 40, 40), 1),
                                          ((40, 40, 40), 2))):
                t = Image.new("RGBA", (40, 40), col + (255,))
                t.alpha_composite(im.resize((16 * s, 16 * s), Image.NEAREST), (4, 4))
                band.paste(t.convert("RGB"), (x0 + j * 44, 156))
        d.text((10, 204), "8x, then 1x and 2x on the slot grey, 1x and 2x on dark grey", fill=ink, font=small)
        parts.append(("The candidates at 8x, 1x and 2x beside vanilla's water-mob eggs, our accepted cerna and tonn "
                      "eggs, the accepted boll icon and bucket" if start == 0 else "(continued)", band))

    tmp = {}
    for n, im in icons.items():
        tmp[n] = os.path.join(CAND, f"fish_boll_egg_v2_{n}.tmp.png")
        im.save(tmp[n])
    lines = measure([os.path.join(VANILLA, n + "_spawn_egg.png") for n in ("cod", "salmon", "squid", "pufferfish")]
                    + [os.path.join(ITEMS, n + "_spawn_egg.png") for n in ("cerna", "tonn")] + list(tmp.values()))
    for p in tmp.values():
        os.remove(p)
    lines += [copy_check(n, im)[0] for n, im in icons.items()]
    band = Image.new("RGB", (W, 20 * len(lines) + 8), bg)
    d = ImageDraw.Draw(band)
    for i, line in enumerate(lines):
        d.text((10, 4 + 20 * i), line, fill=ink, font=label_font(14))
    parts.append(("art/tools/measure.py and the copy check", band))

    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        im = Image.open(out).convert("RGB")
        band = Image.new("RGB", (W, im.height + 30), bg)
        band.paste(im, (10, 4))
        ImageDraw.Draw(band).text((10, im.height + 8), os.path.relpath(out, ROOT) + f"  (GUI scale {scale}, nothing "
                                  "selected: vanilla cod, salmon, squid, pufferfish eggs; BOLL EGG (the pick); "
                                  "tropical fish, axolotl eggs; our cerna egg; boll icon)", fill=ink, font=small)
        parts.append((f"Hotbar preview (art/tools/hotbar_preview.py, GUI scale {scale})", band))

    H = sum(b.height + 30 for _, b in parts) + 40
    out = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(out)
    d.text((10, 8), "Boll (common stingray) spawn egg, second start: textures/item/boll_spawn_egg.png", fill=ink,
           font=label_font(20))
    y = 40
    for title, b in parts:
        d.text((10, y), title, fill=(250, 210, 120), font=font)
        out.paste(b, (0, y + 26))
        y += b.height + 30
    out.save(OUT_SHEET)
    print("wrote", os.path.relpath(OUT_SHEET, ROOT))


def hotbars():
    py = os.path.join(ART, ".venv", "bin", "python")
    items = ["mc:cod_spawn_egg", "mc:salmon_spawn_egg", "mc:squid_spawn_egg", "mc:pufferfish_spawn_egg",
             "mod:boll_spawn_egg", "mc:tropical_fish_spawn_egg", "mc:axolotl_spawn_egg", "mod:cerna_spawn_egg",
             "mod:boll"]
    for out, scale in ((OUT_HOTBAR, 2), (OUT_HOTBAR4, 4)):
        subprocess.run([py, os.path.join(ART, "tools", "hotbar_preview.py"), out] + items + ["--scale", str(scale)],
                       check=True, capture_output=True)


if __name__ == "__main__":
    for n, g in CANDIDATES.items():
        check_outline(n, g)
    icons = {n: render(g) for n, g in CANDIDATES.items()}
    for n, im in icons.items():
        line, n_same = copy_check(n, im)
        assert n_same == 0, line
    icons[PICK].save(OUT_ICON, optimize=False)
    print("wrote", os.path.relpath(OUT_ICON, ROOT), f"(candidate {PICK})")
    os.makedirs(CAND, exist_ok=True)
    hotbars()
    sheet(icons)
