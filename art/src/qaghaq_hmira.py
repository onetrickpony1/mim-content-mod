"""The qagħqa tal-ħmira item icon (catalogue D8): the Maltese aniseed and sesame yeast bread ring.

From the owner's photos in art/references/qaghaq_hmira_owner/ (reference only, never traced, kept out of git):
- a PLUMP, puffy ring of soft bread, more like a fat bagel than a pastry ring: the bread is thick and the hole is
  small, often half closed into a crease;
- a glossy, egg-washed crust, golden-brown to deep chestnut on top, paler and more golden low on the sides;
- covered all over the top in pale cream sesame seeds, close together.
So it must read differently from the accepted qagħaq tal-għasel (a thin pale ring, a big hole, dark treacle slits)
and from the qagħqa tal-appostli (another sesame ring): this one is the small, fat, dark, glossy one.

Each candidate is a ring seen a little from above, lit from the top left: a torus-shaded top, a short side, a small
hole (transparent or a dark crease), deterministic sesame seeds, a warm dark outline (lighter on the top and left).

Writes art/candidates/qaghaq_hmira_{a,b,c}.png and art/candidates/qaghaq_hmira_compare.png (with the in-game hotbar
crop when art/candidates/ingame_qaghaq_hmira/ holds the 20-hotbar-bakes shot), and installs the PICK as the mod
texture item/qaghaq_hmira.png.
Run:  art/.venv/bin/python art/src/qaghaq_hmira.py
"""
import glob
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
sys.path.insert(0, HERE)
from font import label_font  # noqa: E402
from measure import measure  # noqa: E402
from food_items import render, hx, check  # noqa: E402  (read only: food_items' own output is unchanged)

ITEMS = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")
VANILLA = os.path.join(ROOT, "art", ".vanilla", "item")
OUT = os.path.join(ROOT, "art", "candidates")
INGAME = os.path.join(OUT, "ingame_qaghaq_hmira")

PICK = "b"  # the most distinct from the appostli candidates (lighter, top-down, see-through hole)

# glossy egg-washed crust: deep chestnut in shade to golden on the lit crown, a gloss highlight; pale cream sesame
PAL = {"o": hx("#8a4e26"), "O": hx("#663618"),                          # outline lit / shade
       "g": hx("#f0c47c"),                                              # gloss on the crown
       "h": hx("#d28c46"), "l": hx("#b46c2e"), "m": hx("#985526"), "d": hx("#7c421c"), "D": hx("#623216"),
       "p": hx("#cc9452"), "P": hx("#a8743a"),                          # paler golden low on the side, its shade
       "k": hx("#3a1a0a"),                                              # the dark hole / crease
       "s": hx("#f6e6bc"), "S": hx("#dcc08a")}                          # sesame, lit / in shade


def h2(x, y, seed):
    v = math.sin(x * 127.1 + y * 311.7 + seed * 74.7) * 43758.5453
    return v - math.floor(v)


def shade(k):
    return "h" if k > 0.55 else "l" if k > 0.2 else "m" if k > -0.15 else "d" if k > -0.5 else "D"


def ring(cx, cy, rx, ry, hole, depth, dark_hole=False, crease=0.0):
    """A plump ring: zone map ('top', 'side', 'hole') and a shaded grid.
    hole: the hole's radius as a fraction of the ring; dark_hole paints it as a shadowed well instead of see-through;
    crease squeezes the hole into a slanting slit (0 = round)."""
    g = [["."] * 16 for _ in range(16)]
    z = [[None] * 16 for _ in range(16)]
    mid, half = (1 + hole) / 2, (1 - hole) / 2
    for y in range(16):
        for x in range(16):
            u, v = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            r = math.hypot(u, v)
            # the hole, optionally squeezed along a diagonal into a crease
            a = math.radians(-35)
            hu, hv = u * math.cos(a) - v * math.sin(a), u * math.sin(a) + v * math.cos(a)
            rh = math.hypot(hu, hv / max(0.35, 1 - crease))
            if r <= 1 and rh <= hole:
                z[y][x] = "hole"
                g[y][x] = "k" if dark_hole else "."
                continue
            if r <= 1:
                z[y][x] = "top"
                s = max(-1.0, min(1.0, (r - mid) / half))
                nx, ny = (u / max(r, 1e-6)) * s, (v / max(r, 1e-6)) * s
                k = 0.55 * math.sqrt(max(0, 1 - s * s)) - 0.8 * nx - 0.8 * ny - 0.1
                g[y][x] = shade(k)
            elif depth and v > 0 and any(math.hypot(u, (y + .5 - d - cy) / ry) <= 1 for d in range(1, depth + 1)):
                z[y][x] = "side"
                low = math.hypot(u, (y + .5 - depth - cy) / ry) <= 1 and math.hypot(u, (y + .5 - depth + 1 - cy) / ry) > 1
                left = x + .5 < cx - rx * 0.25
                g[y][x] = ("p" if left else "P") if low else ("l" if left else "d")
    return g, z


def outline(g):
    """Opaque pixels touching transparency (outside or the see-through hole) become outline: 'o' facing up/left,
    'O' facing down/right."""
    out = [r[:] for r in g]
    for y in range(16):
        for x in range(16):
            if g[y][x] == ".":
                continue
            score, edge = 0, False
            for dx, dy, w in ((0, -1, 1), (-1, 0, 1), (0, 1, -1), (1, 0, -1)):
                xx, yy = x + dx, y + dy
                if not (0 <= xx < 16 and 0 <= yy < 16) or g[yy][xx] == ".":
                    edge = True
                    score += w
            if edge:
                out[y][x] = "o" if score > 0 or (score == 0 and x + y < 15) else "O"
    return out


def hole_rim(g, z):
    """A dark hole gets a shaded rim on its far (upper) side, a lit one on its near side, so it reads as a well."""
    out = [r[:] for r in g]
    for y in range(16):
        for x in range(16):
            if z[y][x] != "top" or g[y][x] in "oO":
                continue
            if y + 1 < 16 and z[y + 1][x] == "hole":
                out[y][x] = "D"                     # the far inner wall, in shadow
            elif y - 1 >= 0 and z[y - 1][x] == "hole" and g[y][x] in "mdD":
                out[y][x] = "l"                     # the near lip catches the light
    return out


def gloss(g, z, pts):
    for x, y in pts:
        if z[y][x] == "top" and g[y][x] not in "oO":
            g[y][x] = "g"
    return g


def sesame(g, z, seed, want, side_want=0):
    """Pale seeds on the crust: never 4-adjacent, none on the outline, the gloss or the hole rim; lit 's' on light
    crust, shaded 'S' on dark crust."""
    seeds = set()
    for region, n in (("top", want), ("side", side_want)):
        cells = sorted((h2(x, y, seed), x, y) for y in range(16) for x in range(16)
                       if z[y][x] == region and g[y][x] in "hlmdpP")
        got = 0
        for _, x, y in cells:
            if got >= n:
                break
            if any((x + dx, y + dy) in seeds for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                continue
            if sum((x + dx, y + dy) in seeds for dx, dy in ((1, 1), (-1, -1), (1, -1), (-1, 1))) > 1:
                continue
            seeds.add((x, y))
            got += 1
    for x, y in seeds:
        g[y][x] = "s" if g[y][x] in "hlp" else "S"
    return g


def make(letter):
    if letter == "a":    # three-quarter view, small see-through hole, a short side
        g, z = ring(8.0, 7.0, 7.1, 5.4, 0.26, 2)
        g = outline(g)
        g = gloss(g, z, [(4, 4), (5, 3)])
        g = sesame(g, z, 11, 17, 3)
    elif letter == "b":  # three-quarter view, the hole a dark half-closed crease, a deeper side (puffier)
        g, z = ring(8.0, 6.8, 7.1, 5.2, 0.32, 3, dark_hole=True, crease=0.55)
        g = outline(g)
        g = hole_rim(g, z)
        g = gloss(g, z, [(4, 4), (5, 3)])
        g = sesame(g, z, 8, 17, 3)
        # critic round 1: centre the hole (it leaned right): the crease moves one pixel left, its far wall in shadow
        for (x, y), ch in (((6, 7), "D"), ((7, 7), "k"), ((9, 7), "D")):
            g[y][x] = ch
    else:                # nearly from above, round and fat, a small dark well of a hole
        g, z = ring(8.0, 7.6, 6.9, 6.5, 0.24, 1, dark_hole=True)
        g = outline(g)
        g = hole_rim(g, z)
        g = gloss(g, z, [(4, 5), (5, 4)])
        g = sesame(g, z, 17, 20, 1)
    rows = ["".join(r) for r in g]
    check("qaghaq_hmira_" + letter, rows)
    return render(rows, PAL), rows


def vcentre(im):
    ys = [y for y in range(16) for x in range(16) if im.getpixel((x, y))[3]]
    return (min(ys) + max(ys)) / 2


def up(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def compare(cands):
    font = label_font(14)
    ours = [(n, Image.open(os.path.join(ITEMS, f + ".png")).convert("RGBA"))
            for n, f in (("qagħaq tal-għasel", "qaghaq_ghasel"), ("ħobż malti", "hobz_malti"))]
    van = [("vanilla " + n, Image.open(os.path.join(VANILLA, n + ".png")).convert("RGBA")) for n in ("bread", "cookie")]
    pieces = cands + ours + van
    pad, lab, cw = 12, 20, 128 + 16 + 32 + 3 * 12
    rows = []
    for bg in ((232, 232, 228, 255), (139, 139, 139, 255)):
        img = Image.new("RGBA", (pad + len(pieces) * cw, lab + 128 + 2 * pad), bg)
        d = ImageDraw.Draw(img)
        for i, (n, im) in enumerate(pieces):
            x0 = pad + i * cw
            d.text((x0, 2), n, font=font, fill=(20, 20, 20, 255))
            img.alpha_composite(up(im, 8), (x0, lab + pad // 2))
            img.alpha_composite(im, (x0 + 128 + pad, lab + 56))
            img.alpha_composite(up(im, 2), (x0 + 128 + 2 * pad + 16, lab + 48))
        rows.append(img)
    # a mock hotbar row on inventory grey at 1x and 2x: vanilla bread, cookie, the candidates, għasel, ħobż
    strip = [van[0][1], van[1][1]] + [im for _, im in cands] + [ours[0][1], ours[1][1]]
    for k in (1, 2):
        img = Image.new("RGBA", (max(420, pad * 2 + len(strip) * (18 * k + 2)), 18 * k + lab + pad), (139, 139, 139, 255))
        ImageDraw.Draw(img).text((pad, 2), f"{k}x: bread, cookie, candidates, għasel, ħobż", font=font,
                                 fill=(20, 20, 20, 255))
        for i, im in enumerate(strip):
            img.alpha_composite(up(im, k), (pad + i * (18 * k + 2) + k, lab + k))
        rows.append(img)
    shots = sorted(glob.glob(os.path.join(INGAME, "*20-hotbar-bakes*.png")))
    if shots:
        s = Image.open(shots[-1]).convert("RGBA")
        img = Image.new("RGBA", (s.width * 2 + 2 * pad, s.height * 2 + lab + 2 * pad), (232, 232, 228, 255))
        ImageDraw.Draw(img).text((pad, 2), "in game (2x): bread, cookie, pastizz, pastizz xema, qassatat, ħmira, "
                                 "appostli, għasel, ħobż", font=font, fill=(20, 20, 20, 255))
        img.alpha_composite(up(s, 2), (pad, lab + pad // 2))
        rows.append(img)
    W = max(r.width for r in rows)
    sheet = Image.new("RGBA", (W, sum(r.height + 4 for r in rows)), (200, 200, 196, 255))
    y = 0
    for r in rows:
        sheet.alpha_composite(r, (0, y))
        y += r.height + 4
    p = os.path.join(OUT, "qaghaq_hmira_compare.png")
    sheet.save(p)
    print("wrote", os.path.relpath(p, ROOT))


def main():
    os.makedirs(OUT, exist_ok=True)
    cands = []
    for letter in "abc":
        im, rows = make(letter)
        name = "qaghaq_hmira_" + letter
        p = os.path.join(OUT, name + ".png")
        im.save(p)
        m = measure(p)
        print(name, {k: m[k] for k in ("coverage", "colours", "edge_l", "interior_l", "tl_minus_br")},
              "outline/inside", round(m["edge_l"] / m["interior_l"], 2), "vcentre", vcentre(im))
        cands.append((name, im))
        if letter == PICK:
            im.save(os.path.join(ITEMS, "qaghaq_hmira.png"))
    compare(cands)


if __name__ == "__main__":
    main()
