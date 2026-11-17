"""Item textures for three Maltese sweets (candidates only, 2026-11-17; NOT in the mod).

Shapes and colours from the owner's photos in art/references/sweets_owner/ (reference only, unknown licence):
- Imqaret: diamond / rectangular fried pastries, golden-brown and blistered, the dark date filling showing as a dark
  stripe or core at the cut ends; sometimes a little icing sugar.
- Kannoli: a blistered golden-brown fried tube with flared ends; the owner: keep it plain ricotta, so white ricotta at
  both open ends and nothing else; a light icing-sugar dusting.
- Qagħaq tal-għasel: a pale golden pastry ring with a big hole, diagonal slits along the top showing the near-black
  purple-brown treacle (qagħaq) filling.

Run:  art/.venv/bin/python art/src/sweets.py
Writes art/candidates/{imqaret,kannoli,qaghaq_ghasel}_{a,b}.png and art/candidates/sweets_compare.png.
"""
import math
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import food_items as F  # noqa: E402  (shared helpers: hx, render, outline3, compare, paths)

hx, render, outline3 = F.hx, F.render, F.outline3

# fried pastry (imqaret, kannoli): golden-brown, blistered
FRY = {"o": hx("#7a4418"), "O": hx("#5a3010"),
       "h": hx("#f0c477"), "l": hx("#dca456"), "m": hx("#c4823a"), "d": hx("#9e6026"), "D": hx("#7c461c"),
       "k": hx("#2e1712"), "K": hx("#4e2a1c"),                      # date filling, its lit edge
       "w": hx("#f7f3e8"), "W": hx("#dcd3bf"),                      # ricotta, in shade
       "s": hx("#f4ece0")}                                          # icing sugar
# qagħaq: pale golden pastry, near-black purple-brown treacle
QAG = {"o": hx("#8a6a34"), "O": hx("#6a4f24"),
       "h": hx("#fbecc0"), "l": hx("#f0d899"), "m": hx("#ddbf78"), "d": hx("#bf9d5a"), "D": hx("#9c7c40"),
       "k": hx("#2c1820"), "K": hx("#4c2c34")}


def blank():
    return [["."] * 16 for _ in range(16)]


def finish(g, lit_rule=lambda x, y: x + y < 15):
    """Outline every opaque pixel touching transparency: lit 'o' on the top/left, 'O' on the bottom/right."""
    e = outline3(g)
    for y in range(16):
        for x in range(16):
            if e[y][x] == "#" and g[y][x] in "wW":
                g[y][x] = "W"                     # ricotta at the edge: its own shade, as on the accepted pastizz
            elif e[y][x] == "#" and g[y][x] != ".":
                g[y][x] = "o" if lit_rule(x, y) else "O"
    return g


def shade(k):
    return "h" if k > 0.62 else "l" if k > 0.25 else "m" if k > -0.15 else "d" if k > -0.55 else "D"


def put(g, pts, ch, only=None):
    for x, y in pts:
        if g[y][x] != "." and (only is None or g[y][x] in only):
            g[y][x] = ch


# ---------------- Imqaret ----------------
def _frame(ang, cx, cy):
    t = math.radians(ang)
    def f(x, y):
        dx, dy = x + .5 - cx, y + .5 - cy
        return dx * math.cos(t) + dy * math.sin(t), -dx * math.sin(t) + dy * math.cos(t)
    return f


IMQARET_A = [   # from above: a rhombus, the date showing as a dark stripe along both slanted cut ends
    "................",
    "................",
    "................",
    "................",
    ".....oooooooooo.",
    "....okhhlhlllkO.",
    "....okhllmllkO..",
    "...okllmhmmlkO..",
    "...oklmmmdmkO...",
    "..okmmdmmdmkO...",
    "..OkmddmddkO....",
    ".OOOOOOOOOOO....",
    "................",
    "................",
    "................",
    "................",
]


def imqaret_a():
    return [list(r) for r in IMQARET_A]


def imqaret_b():
    """Three-quarter view: a fried roll lying across, its left end cut to show the thick dark date core in a ring of
    pastry, a dark stripe at the right cut end, blisters and a touch of icing sugar on top."""
    g = blank()
    for y in range(4, 12):
        for x in range(1, 15):
            if (y == 4 and not 3 <= x <= 13) or (y == 11 and not 2 <= x <= 13) or (x in (1, 14) and y in (5, 10)):
                continue
            face = ((x + .5 - 3.4) / 2.5) ** 2 + ((y + .5 - 8.2) / 3.4) ** 2 <= 1
            if face:
                core = ((x + .5 - 3.5) / 1.5) ** 2 + ((y + .5 - 8.4) / 2.1) ** 2 <= 1
                g[y][x] = ("k" if (x + y) > 9 else "K") if core else ("l" if x + y < 11 else "d")
            else:
                g[y][x] = ("h" if x < 9 else "l") if y <= 5 else "l" if y == 6 else "m" if y <= 8 else "d" if y <= 9 else "D"
    for y in (7, 8, 9):
        g[y][13] = "k"
    put(g, [(7, 5), (9, 6), (11, 5), (12, 6)], "s", "hl")
    put(g, [(8, 8), (11, 7), (10, 9), (7, 9)], "d", "m")
    put(g, [(9, 8), (12, 8)], "l", "m")
    return finish(g)


# ---------------- Kannoli ----------------
def _tube(ang, cx, cy, L, r, rl):
    """A fried tube on an axis (ang degrees; negative rises to the right), half-length L, radius r; both open ends
    filled with ricotta, a rounded cap reaching rl px beyond the shell; the shell's cut rim a dark ring."""
    f = _frame(ang, cx, cy)
    g = blank()
    for y in range(16):
        for x in range(16):
            u, v = f(x, y)
            if abs(u) <= L and abs(v) <= r:
                g[y][x] = shade(-0.9 * v / r + 0.1)
                if abs(u) > L - 0.9:
                    g[y][x] = "D"
            elif abs(u) > L and ((abs(u) - L + 0.3) / (rl + 0.3)) ** 2 + (v / (r - 0.2)) ** 2 <= 1:
                g[y][x] = "w" if v < 0.7 else "W"
    return g


def kannoli_a():
    """On the exact diagonal (rising to the right), shorter and fatter than vanilla bread: blistered shell lit along
    its top-left side, its cut rims as dark rings, white ricotta caps at both ends."""
    g = blank()
    for y in range(16):
        for x in range(16):
            a, b = x - y, x + y - 15                 # a along the tube, b across it
            if abs(b) <= 3 and abs(a) <= 5:
                g[y][x] = ("d" if b < 0 else "D") if abs(a) >= 4 else {-3: "h", -2: "h", -1: "l", 0: "l", 1: "m", 2: "d", 3: "D"}[b]
            elif abs(b) <= 2 and 6 <= abs(a) <= 9 and abs(a) + abs(b) <= 10:
                g[y][x] = "w" if b <= 0 else "W"
    put(g, [(7, 7), (8, 6), (6, 9)], "d", "lm")
    put(g, [(8, 8), (6, 7)], "h", "lm")
    return finish(g)


def kannoli_b():
    """Lying level: a blistered shell, its cut rims as dark rings, white ricotta caps at both ends, icing sugar."""
    g = blank()
    for y in range(5, 11):
        for x in list(range(2, 4)) + list(range(12, 14)):
            if 6 <= y <= 9 or x in (3, 12):
                g[y][x] = "w" if y <= 7 else "W"
        for x in range(4, 12):
            g[y][x] = {5: "h", 6: "h" if x < 8 else "l", 7: "l", 8: "m", 9: "d", 10: "D"}[y]
    for x in (4, 11):
        for y in range(4, 12):
            g[y][x] = "D" if 6 <= y <= 9 else "m"
    put(g, [(6, 6), (7, 5), (9, 6), (10, 5)], "s", "hl")
    put(g, [(6, 8), (8, 9), (9, 8)], "d", "m")
    put(g, [(7, 8), (10, 7)], "h", "lm")
    return finish(g)


# ---------------- Qagħaq tal-għasel ----------------
def _ring(cx, cy, rx, ry, hole, depth, slits, tilt=55):
    """A pastry ring (torus-like shading), big hole, a low side when depth > 0; dark diagonal slits on top."""
    g = blank()
    zone = [[None] * 16 for _ in range(16)]
    mid, half = (1 + hole) / 2, (1 - hole) / 2
    for y in range(16):
        for x in range(16):
            u, v = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            r = math.hypot(u, v)
            if hole < r <= 1:
                zone[y][x] = "top"
                s = (r - mid) / half                                  # -1 inner edge .. +1 outer edge
                nx, ny = (u / r) * s, (v / r) * s
                k = 0.55 * math.sqrt(max(0, 1 - s * s)) - 0.55 * nx - 0.55 * ny - 0.1
                g[y][x] = shade(k)
            elif depth and v > 0 and r > 1 and any(math.hypot(u, (y + .5 - k - cy) / ry) <= 1 for k in range(1, depth + 1)):
                zone[y][x] = "side"
                g[y][x] = "d" if x + .5 < cx else "D"
            elif depth and r <= hole and v < 0 and math.hypot(u, (y + .5 + depth - cy) / ry) > hole:
                zone[y][x] = "wall"                                    # the far inner wall seen through the hole
                g[y][x] = "d"
    for th in slits:
        t = math.radians(th)
        px, py = cx + mid * rx * math.cos(t), cy + mid * ry * math.sin(t)
        tx, ty = -math.sin(t) * rx, math.cos(t) * ry
        n = math.hypot(tx, ty)
        a = math.radians(tilt)
        dx, dy = (tx * math.cos(a) - ty * math.sin(a)) / n, (tx * math.sin(a) + ty * math.cos(a)) / n
        for y in range(16):
            for x in range(16):
                if zone[y][x] != "top":
                    continue
                qx, qy = x + .5 - px, y + .5 - py
                along = qx * dx + qy * dy
                across = -qx * dy + qy * dx
                if abs(along) <= 2.3 and abs(across) <= 0.8:
                    g[y][x] = "k" if across <= 0.1 else "K"
    return g


def qaghaq_a():
    """Seen from above (slightly tilted): a pale ring, a big hole, seven diagonal dark treacle slits."""
    g = _ring(8.0, 8.0, 7.2, 6.9, 0.42, 0, [i * 360 / 6 + 10 for i in range(6)])
    return finish(g)


def qaghaq_b():
    """Three-quarter view: the ring as an ellipse with a low side, the far inner wall showing through the hole,
    dark slits along the top."""
    g = _ring(8.0, 7.0, 7.2, 5.0, 0.42, 2, [i * 360 / 6 + 25 for i in range(6)])
    return finish(g)


# ---- Round 2 (critic, 2026-11-17): imqaret a with a warmer plum date; kannoli a with flared lips and outlined cream ----
FRY2 = dict(FRY, k=hx("#3a1a1c"), c=hx("#8a7e66"), C=hx("#b8ad96"))   # plum date, cream outline, cream lit edge


def imqaret_v2():
    return imqaret_a()


def kannoli_v2():
    g = kannoli_a()
    for (x, y), ch in {(9, 3): "o", (13, 6): "O", (2, 10): "o", (6, 12): "O",
                       (13, 3): "c", (13, 4): "c", (13, 5): "c", (2, 11): "c", (2, 12): "c", (3, 13): "c", (4, 13): "c",
                       (5, 13): "c", (12, 3): "C", (5, 12): "C"}.items():
        g[y][x] = ch
    # edge_l <= 0.40: the cream pixels still on the silhouette edge take the cream outline too
    for x, y in ((10, 3), (11, 3), (12, 5), (3, 10)):
        g[y][x] = "c"
    return g


# ---- Varieties (owner 2026-11-17: "more varieties" of imqaret and kannoli) ----
FRYD = dict(FRY2, h=hx("#dc9c50"), l=hx("#c47c34"), m=hx("#a66026"), d=hx("#80461a"), D=hx("#603414"),
            o=hx("#5e3012"), O=hx("#44220c"))                        # deeper fried, darker golden-brown


def finish2(g):
    """finish() with the cream rule from the critic: ricotta on the silhouette edge becomes the cream outline 'c'."""
    e = outline3(g)
    for y in range(16):
        for x in range(16):
            if e[y][x] == "#" and g[y][x] != ".":
                g[y][x] = "c" if g[y][x] in "wWC" else ("o" if x + y < 15 else "O")
    return g


def over(back, front):
    g = [r[:] for r in back]
    for y in range(16):
        for x in range(16):
            if front[y][x] != ".":
                g[y][x] = front[y][x]
    return g


def parallelo(c, A, B, e=0.3, sugar=False, blist=True):
    """One imqaret from above: a parallelogram p = c + s*A + t*B (|s|, |t| <= 1); the date shows as a band at both
    cut ends (|s| near 1) between the pastry lips; lit from the top left; fried blisters; optional icing sugar."""
    det = A[0] * B[1] - A[1] * B[0]
    g = blank()
    for y in range(16):
        for x in range(16):
            dx, dy = x + .5 - c[0], y + .5 - c[1]
            sv = (dx * B[1] - dy * B[0]) / det
            tv = (A[0] * dy - A[1] * dx) / det
            if abs(sv) <= 1 and abs(tv) <= 1:
                k = -0.16 * (dx + dy) + 0.05
                g[y][x] = shade(k)
                if blist and (x * 7 + y * 11) % 9 == 0:
                    g[y][x] = "h" if k > -0.2 else "m"
                if blist and (x * 5 + y * 3) % 11 == 0:
                    g[y][x] = "d"
                if sugar and k > -0.45 and (x * 5 + y * 3) % 7 in (0, 3):
                    g[y][x] = "s"
                if abs(sv) >= 1 - e and abs(tv) <= 0.55:
                    g[y][x] = "k" if abs(tv) <= 0.3 else "K"
    return finish(g)


def runs_piece(runs, date=(), sugar=(), blist=(), pits=(), c=(8, 8)):
    """A piece drawn from row runs {y: (x0, x1)}: lit from the top left, date pixels, icing sugar, blisters."""
    g = blank()
    for y, (x0, x1) in runs.items():
        for x in range(x0, x1 + 1):
            g[y][x] = shade(-0.16 * ((x + .5 - c[0]) + (y + .5 - c[1])) + 0.05)
    g = finish(g)
    put(g, blist, "h", "lmd")
    put(g, pits, "d", "hlm")
    put(g, sugar, "s", "hlmd")
    put(g, date, "k", "hlmdD")
    return g


IMQ_SMALL = {0: (3, 9), 1: (2, 9), 2: (2, 8), 3: (1, 8), 4: (1, 7), 5: (0, 7)}


def imqaret_c():
    """A single diamond standing steeply, rising to the upper right; the date band at both slanted cut ends."""
    runs = {2: (9, 11), 3: (8, 12), 4: (8, 13), 5: (7, 12), 6: (7, 12), 7: (6, 11), 8: (6, 11), 9: (5, 10),
            10: (5, 10), 11: (4, 9), 12: (3, 8), 13: (4, 6)}
    return runs_piece(runs, date=[(9, 3), (10, 3), (11, 3), (12, 4), (4, 12), (5, 12), (6, 12), (7, 12)],
                      blist=[(8, 6), (9, 8), (7, 9)], pits=[(10, 6), (8, 9), (7, 11)])


def imqaret_d():
    """Two small diamonds, one lying over the other as on a plate; date bands at their cut ends."""
    def one(dx, dy):
        runs = {y + dy: (a + dx, b + dx) for y, (a, b) in IMQ_SMALL.items()}
        date = [(2 + dx, 1 + dy), (2 + dx, 2 + dy), (1 + dx, 3 + dy), (1 + dx, 4 + dy),
                (8 + dx, 1 + dy), (7 + dx, 2 + dy), (7 + dx, 3 + dy), (6 + dx, 4 + dy)]
        return runs_piece(runs, date=date, blist=[(4 + dx, 2 + dy)], pits=[(5 + dx, 3 + dy)])
    return over(one(6, 2), one(1, 8))


def imqaret_e():
    """The thick three-quarter roll (side and top seen, the date core at the cut end), deep-fried darker."""
    return imqaret_b()


def imqaret_f():
    """v2's diamond seen at three-quarter, so its thickness shows as a side wall with the date stripe along the
    cut end; the top dusted with icing sugar."""
    top = [[c != "." for c in r] for r in IMQARET_A[1:] + IMQARET_A[:1]]   # up one row
    g = blank()
    for y in range(16):
        for x in range(16):
            if top[y][x]:
                g[y][x] = shade(-0.16 * ((x - 8) + (y - 7)) + 0.1)
            elif (y >= 1 and top[y - 1][x]) or (y >= 2 and top[y - 2][x]):
                g[y][x] = "d" if x < 8 else "D"
    g = finish(g)
    put(g, [(2, 11), (3, 11), (3, 10), (4, 9), (4, 10), (12, 5), (12, 6), (11, 7), (11, 8), (10, 9)], "k", "hlmdD")
    put(g, [(7, 4), (9, 4), (6, 6), (8, 6), (10, 5), (5, 8), (9, 7)], "s", "hlm")
    return g


def itube(a_of, b_of, A, B, R, sugar=False, blist=True):
    """A kannolo on an integer grid: a_of/b_of give the along/across coordinates; shell |a| <= A, |b| <= B, its mouth
    lips flaring by one unit; plain ricotta in each mouth, a little narrower than the lip, R units beyond it."""
    g = blank()
    for y in range(16):
        for x in range(16):
            a, b = a_of(x, y), b_of(x, y)
            lip = abs(a) >= A - 1
            if abs(a) <= A and abs(b) <= B + (1 if lip else 0):
                t = b / B
                ch = "h" if t < -0.5 else "l" if t < 0 else "m" if t < 0.5 else "d"
                if blist and (x * 7 + y * 13) % 6 == 0 and not lip:
                    ch = "h" if t < 0.3 else "m"
                if blist and (x * 11 + y * 5) % 7 == 0 and not lip:
                    ch = "d"
                if sugar and t < 0.2 and (x * 3 + y * 7) % 3 == 0 and not lip:
                    ch = "s"
                if lip:
                    ch = "m" if b < 0 else "D"
                g[y][x] = ch
            elif A < abs(a) <= A + R and abs(b) <= B - 1 - max(0, abs(a) - A - R + 1):
                g[y][x] = "w" if b < 1 else "W"
    return finish2(g)


KANNOLI_C = [   # level, big: flared mouths (2-px lips taller than the shell), ricotta inside each mouth, sugar
    "................",
    "................",
    "................",
    "................",
    "...oo......OO...",
    "...omoooooomO...",
    ".ccmdhshhshdmcc.",
    ".cwmdlhllhldmwc.",
    ".cWDdmmdmmmdDWc.",
    ".ccDddddmdddDcc.",
    "...ODOOOOOODO...",
    "...OO......OO...",
    "................",
    "................",
    "................",
    "................",
]


def kannoli_c():
    return [list(r) for r in KANNOLI_C]


def kannoli_d():
    """Steep (rising two rows per column): blistered shell lit on its left, flared lips, ricotta at both mouths,
    icing sugar on the lit side."""
    body = {4: (8, 12), 5: (8, 12), 6: (7, 11), 7: (7, 11), 8: (6, 10), 9: (6, 10), 10: (5, 9), 11: (5, 9)}
    g = blank()
    for y, (x0, x1) in body.items():
        for x in range(x0, x1 + 1):
            g[y][x] = "hllmd"[min(4, x - x0)]
    for x in range(7, 14):
        g[3][x] = "m" if x < 10 else "D"
    for x in range(4, 11):
        g[12][x] = "m" if x < 7 else "D"
    for y, xs in ((1, (10, 11)), (2, (9, 10, 11, 12)), (13, (5, 6, 7, 8)), (14, (6, 7))):
        for x in xs:
            g[y][x] = "w" if y < 3 or x < 7 else "W"
    g = finish2(g)
    put(g, [(9, 5), (8, 7), (7, 9), (6, 11)], "s", "hl")
    put(g, [(10, 6), (9, 9), (7, 10)], "d", "lm")
    return g


KANNOLO_SMALL = [
    "...oo......OO...",
    "..comoooooomOc..",
    ".cwmdhhshhhdmwc.",
    ".cWDdmmdmmmdDWc.",
    "..cODOOOOOODOc..",
    "...OO......OO...",
]


def kannoli_e():
    """Two side by side, one behind and a little to the right, as on a tray: flared lips, ricotta in each mouth."""
    def one(dx, dy):
        g = blank()
        for r, row in enumerate(KANNOLO_SMALL):
            for x, c in enumerate(row):
                if c != "." and 0 <= x + dx < 16:
                    g[r + dy][x + dx] = c
        return g
    return over(one(1, 2), one(-1, 7))


def kannoli_f():
    """The exact diagonal, fat and long, heavily blistered, flared mouths, generous ricotta, a little icing sugar."""
    return itube(lambda x, y: x - y, lambda x, y: x + y - 15, 6, 3, 4, sugar=True)


VARIANTS = (("imqaret_c", imqaret_c, FRY2), ("imqaret_d", imqaret_d, FRY2), ("imqaret_e", imqaret_e, FRYD),
            ("imqaret_f", imqaret_f, FRY2), ("kannoli_c", kannoli_c, FRY2), ("kannoli_d", kannoli_d, FRY2),
            ("kannoli_e", kannoli_e, FRY2), ("kannoli_f", kannoli_f, FRY2))


def variants_sheet(made):
    """Two rows (imqaret, kannoli): v2 and c-f, each at 1x, 2x and 8x on slot grey, labelled with its letter."""
    from PIL import ImageDraw
    rows = [["imqaret_v2"] + ["imqaret_" + c for c in "cdef"], ["kannoli_v2"] + ["kannoli_" + c for c in "cdef"]]
    slot, bg, ink = (139, 139, 139, 255), (198, 198, 198, 255), (30, 30, 30, 255)
    S, cw, rh = 8, 16 * 8 + 24, 64 + 16 * 8 + 30
    sheet = Image.new("RGBA", (16 + 5 * cw + 120, 16 + 2 * rh), bg)
    d = ImageDraw.Draw(sheet)
    f = F.label_font(13)
    for r, names in enumerate(rows):
        y0 = 16 + r * rh
        d.text((16, y0 + 70), ("Imqaret" if r == 0 else "Kannoli"), fill=ink, font=f)
        for i, n in enumerate(names):
            im = made[n]
            x0 = 120 + i * cw
            d.rectangle([x0, y0, x0 + 17, y0 + 17], fill=slot)
            sheet.alpha_composite(im, (x0 + 1, y0 + 1))
            d.rectangle([x0 + 30, y0, x0 + 65, y0 + 35], fill=slot)
            sheet.alpha_composite(im.resize((32, 32), Image.NEAREST), (x0 + 32, y0 + 2))
            d.rectangle([x0, y0 + 44, x0 + 127, y0 + 44 + 127], fill=slot)
            sheet.alpha_composite(im.resize((128, 128), Image.NEAREST), (x0, y0 + 44))
            d.text((x0, y0 + 44 + 130), n.split("_")[1], fill=ink, font=f)
    return sheet


CANDS = (("imqaret_a", imqaret_a, FRY), ("imqaret_b", imqaret_b, FRY), ("kannoli_a", kannoli_a, FRY),
         ("kannoli_b", kannoli_b, FRY), ("qaghaq_ghasel_a", qaghaq_a, QAG), ("qaghaq_ghasel_b", qaghaq_b, QAG),
         ("imqaret_v2", imqaret_v2, FRY2), ("kannoli_v2", kannoli_v2, FRY2))
FINAL = ("imqaret_v2", "kannoli_v2", "qaghaq_ghasel_a")
LABELS = {"imqaret": "Imqaret", "kannoli": "Kannoli", "qaghaq_ghasel": "Qagħaq tal-għasel"}


def main():
    ims, made = [], {}
    for name, make, pal in CANDS:
        rows = ["".join(r) for r in make()]
        F.check(name, rows)
        im = render(rows, pal)
        im.save(os.path.join(F.OUT, name + ".png"))
        base, v = name.rsplit("_", 1)
        made[name] = (LABELS[base] + " " + v, im)
        if name not in FINAL[:2]:
            ims.append(made[name])
    ours = [("Pastizz tal-irkotta", "pastizz_irkotta"), ("Ftira", "ftira")]
    for lbl, f in ours:
        ims.append((lbl, Image.open(os.path.join(F.MOD_ITEMS, f + ".png")).convert("RGBA")))
    for v in ("cookie", "bread", "pumpkin_pie"):
        ims.append(("vanilla " + v, Image.open(os.path.join(F.VANILLA, v + ".png")).convert("RGBA")))
    rest = ims[len(CANDS) - 2:]
    F.compare(ims).save(os.path.join(F.OUT, "sweets_compare.png"))
    F.compare([made[n] for n in FINAL] + rest).save(os.path.join(F.OUT, "sweets_final.png"))
    vm = {n: v[1] for n, v in made.items()}
    for name, make, pal in VARIANTS:
        rows = ["".join(r) for r in make()]
        F.check(name, rows)
        vm[name] = render(rows, pal)
        vm[name].save(os.path.join(F.OUT, name + ".png"))
    variants_sheet(vm).save(os.path.join(F.OUT, "sweets_variants.png"))
    print("wrote", len(CANDS), "sweets candidates and sweets_compare.png")


if __name__ == "__main__":
    main()
