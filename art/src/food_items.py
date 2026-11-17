"""Item textures for two Maltese foods: ħobż tal-Malti and pastizz tal-irkotta.

Three candidates each, drawn as explicit 16x16 pixel maps over a small palette
(some start from a procedural layout, frozen into the maps after hand clean-up).
Shapes and colours come from art/references/bread_*.jpg and pastizzi_*.jpg.

Run:  art/.venv/bin/python art/src/food_items.py
Round 3 (current): art/candidates/*_v3*.png, installed as hobz_malti.png, pastizz_irkotta.png,
pastizz_pizelli.png (option R) and gbejna.png (gbejna_v6).
Writes the round-1 candidates art/candidates/hobz_{a,b,c}.png, pastizz_{irkotta,pizelli}_{a,b,c}.png,
the round-2 pieces art/candidates/*_v2.png (also copied into the mod as hobz_malti.png,
pastizz_irkotta.png, pastizz_pizelli.png) and art/candidates/preview.png (the v2 pieces beside vanilla).
"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from font import label_font  # noqa: E402  (Pillow's default font has no ħ ż ġ)

LABELS = {"hobz": "Ħobż", "pastizz_irkotta": "Pastizz tal-irkotta", "pastizz_pizelli": "Pastizz tal-piżelli",
          "gbejna": "Ġbejna"}


def label(name):
    """File-style name -> real Maltese spelling plus the version, e.g. hobz_v6 -> 'Ħobż v6'."""
    for k, v in LABELS.items():
        if name.startswith(k + "_"):
            return v + " " + name[len(k) + 1:]
    return name

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ART, "candidates")
VANILLA = ("/tmp/claude-1000/-home-cultar-Apps-Untitled-Malta-in-Minecraft-Content-Mod/"
           "e094b0a5-e6f9-4507-a5c0-ed895a344095/scratchpad/vanilla/assets/minecraft/textures/item")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


# --- Ħobż: wood-fired crust (golden to dark brown), floury tops, pale crumb where it tears ---
BREAD = {
    "O": hx("#77491c"),  # outline, lit side (top/left)
    "#": hx("#4c2f11"),  # outline, shade side (bottom/right)
    "D": hx("#6f4418"),  # cracks, deep crust
    "d": hx("#8c5820"),  # dark crust
    "m": hx("#a9712d"),  # crust
    "l": hx("#c58f43"),  # light crust
    "h": hx("#dcb26a"),  # flour dusting / highlight
    "f": hx("#f1e4c0"),  # crumb / heavy flour
    "C": hx("#cdb27c"),  # crumb in shade
}

# --- Pastizz: laminated pastry, golden layers, white ricotta ---
PASTRY = {
    "O": hx("#a25c22"),  # outline, lit side
    "#": hx("#713c15"),  # outline, shade side
    "D": hx("#9b5620"),  # layer gaps (dark lines)
    "d": hx("#bb6f2b"),  # layer in shade
    "m": hx("#d68f3f"),  # layer
    "l": hx("#eab265"),  # layer lit
    "h": hx("#f8d996"),  # highlight on layer edges
    "r": hx("#f7f3e8"),  # ricotta
    "R": hx("#d8cfbb"),  # ricotta in shade
    "b": hx("#e3c48a"),  # ricotta browned in the oven
    "y": hx("#d6cf74"),  # peas, lit
    "g": hx("#b5a93e"),  # peas (curried mushy peas, yellow-green)
    "G": hx("#7a7a2a"),  # peas in shade
}
FILL_SHADE = {"r": "R", "R": "R", "b": "R", "y": "G", "g": "G", "G": "G"}

# A: round ħobża seen from above-front: floury cracked dome, crust torn open along the lower left
HOBZ_A = [
    "................",
    "................",
    "................",
    "......OOOO......",
    "....OOhffhOO....",
    "...OhfhDhllm#...",
    "..OhfDllDhlmd#..",
    "..OfhlDDllDmd#..",
    ".OhlDlmlDmmDmd#.",
    ".OlDmlmDmmDmdd#.",
    "..ODDDDmDmmdd#..",
    "..CffCfCDmddD#..",
    "...CfCCCDddD#...",
    "....#DDddDD#....",
    ".....######.....",
    "................",
]

# B: oval loaf lying a little tilted, a lengthwise split along the top showing crumb
HOBZ_B = [
    "................",
    "................",
    "................",
    "................",
    ".......OOOOO#...",
    "....OOhlhlhfl#..",
    "...OhlhlhffCmd#.",
    "..OlhfffCDmmdd#.",
    ".OhffCCDmmDmdd#.",
    ".OfCDmmmDmmdDd#.",
    ".ODmmDmmmdmdd#..",
    ".OmmdmDddDd##...",
    "..#########.....",
    "................",
    "................",
    "................",
]

# C: long loaf pointing away, its torn end towards the viewer showing the pale crumb face
HOBZ_C = [
    "................",
    "................",
    ".........OOOO...",
    ".......OOhfhl#..",
    "......OhflDlmd#.",
    ".....OhlDlmmDd#.",
    ".....OlmlmDmdd#.",
    "...OOOODmmDmd#..",
    "..OmfffmDmmdd#..",
    "..OmfCffmDmd#...",
    "..OmffCfmDd#....",
    "..OmfCffd#......",
    "..#dCffd#.......",
    "...#dCCd#.......",
    ".....##.........",
    "................",
]

# Pastizzi: research notes (Wikipedia "Pastizz", en + mt): the pastry is folded differently by filling, so
# people can tell them apart: ricotta ones are folded down the MIDDLE (a symmetric diamond with the
# white filling showing along a central seam), pea ones down the SIDE (a rounder half-moon with the
# yellow-green curried peas showing along one edge). References: pastizzi_1/4 (pea), pastizzi_2/3/5/6.
# In these maps "x" marks the outline; every edge pixel is outlined automatically (see autooutline).

# Ricotta A: from above, diamond on the diagonal, ricotta along the central seam, herringbone layers
IRKOTTA_A = [
    "................",
    "............xx..",
    ".........xxhlx..",
    ".......xxhlDdx..",
    ".....xxhmmrRDx..",
    "....xhlllrrRDx..",
    "....xlllrrRmx...",
    "...xhmmrrRmdx...",
    "...xllrrRDdx....",
    "..xhlrRmmDdx....",
    "..xlDmDmddx.....",
    "..xDmmDddx......",
    ".xDmdddx........",
    ".xxxxx..........",
    "................",
    "................",
]

# Ricotta B: three-quarter view, pointed ends left and right, the ricotta bulging out of the top
# seam (with a browned fleck), layers fanning down the front
IRKOTTA_B = [
    "................",
    "................",
    "................",
    "............xx..",
    "......xxxxxxhlx.",
    "....xxrrrbrRDmx.",
    "...xhrrbrrRRDx..",
    "..xhlRRRRRDmdx..",
    ".xhlDllDlmDmdx..",
    "xllDlmmDmmmDx...",
    ".xDmmmDmdddDx...",
    "..xdmdDdddDx....",
    "...xxxxxxxx.....",
    "................",
    "................",
    "................",
]

# Ricotta C: from above, diamond the other way (top left to bottom right), fat, the seam burst open
# with a wide strip of baked ricotta (browned flecks)
IRKOTTA_C = [
    "................",
    "................",
    "..xxx...........",
    "..xhDxxx........",
    "..xlrrhlxx......",
    "..xmrbrRhlxx....",
    "...xDrrrRlmlx...",
    "...xmDrbrRlmx...",
    "....xdmrrrRmlx..",
    "....xDdmrbRmdx..",
    ".....xmDmrRDmx..",
    "......xdDmRDdx..",
    "........xdDDdx..",
    "...........xxx..",
    "................",
    "................",
]

# Pea A: from above, half-moon: round back to the top left, folded down the side, the curried peas
# showing (and oozing) along the straight seam at the lower right; layers follow the round back
PIZELLI_A = [
    "................",
    "................",
    ".......xxxxx....",
    ".....xxhhhllxx..",
    "....xhhhhlllDgx.",
    "...xhhDDDllDgx..",
    "...xhDhhllDgx...",
    "..xhDhllmDgx....",
    "..xhDllmDgx.....",
    "..xlDlmDyx......",
    "..xlmDDgx.......",
    "..xmmDgx........",
    "...xDgx.........",
    "...xGx..........",
    "................",
    "................",
]

# Pea B: the curled shell: a pointed tip at the top left, layers fanning out from it, peas showing
# along the side seam at the lower left (as in pastizzi_1)
PIZELLI_B = [
    "................",
    "................",
    "..xx............",
    "..xhxxxxxxx.....",
    "...xhhhhhllxx...",
    "....xhmmmmhllx..",
    "....xhDhhlmmlmx.",
    "...xhDhDDlllDmx.",
    "...xhlDllDlmDmx.",
    "...xylDlmmDmmDx.",
    "...xgylDmmmDmDx.",
    "...xGgymDmmDddx.",
    "....xGggmDddDdx.",
    ".....xGgdDdddx..",
    ".......xxxxx....",
    "................",
]

# Pea C: three-quarter view, lying on its flat seam: round back on top, layers arching end to end,
# a line of peas along the bottom seam with a couple of drips
PIZELLI_C = [
    "................",
    "................",
    "................",
    "................",
    "......xxxxx.....",
    "....xxhhhllxx...",
    "...xhhhDDlllmx..",
    "..xhlhDllDllmmx.",
    ".xhlhDlDDlDmmdx.",
    ".xlmDlDmmDmDmdx.",
    ".xDgyggyggygGx..",
    "..xxGxxxxGxxx...",
    "................",
    "................",
    "................",
    "................",
]
CANDIDATES = [
    ("hobz_a", HOBZ_A, BREAD),
    ("hobz_b", HOBZ_B, BREAD),
    ("hobz_c", HOBZ_C, BREAD),
    ("pastizz_irkotta_a", IRKOTTA_A, PASTRY),
    ("pastizz_irkotta_b", IRKOTTA_B, PASTRY),
    ("pastizz_irkotta_c", IRKOTTA_C, PASTRY),
    ("pastizz_pizelli_a", PIZELLI_A, PASTRY),
    ("pastizz_pizelli_b", PIZELLI_B, PASTRY),
    ("pastizz_pizelli_c", PIZELLI_C, PASTRY),
]


# ---- Round 2 (after the independent critic's review): one chosen piece per food, refined ----

# Ħobż v2 (from hobz_b): domed top, darker right half with blotches, the split as a torn "ear"
# at the lower left (crumb with a jagged dark lip below it, bright crust edge above)
HOBZ_V2 = [
    "................",
    "................",
    "................",
    "......OOOOO.....",
    ".....OhlmhmO#...",
    "....Ohllhmlhm#..",
    "...Olhhhmmhmmd#.",
    "..Ohffff#mmDdd#.",
    "..ff#m#mmmDmdd#.",
    ".OffDmmmmDmdDd#.",
    ".ODmmDmmmdmmd#..",
    "..#mdmDddDd#....",
    "...########.....",
    "................",
    "................",
    "................",
]

# Pastizz tal-irkotta v2 (from irkotta_a): plumper diamond, a thin 1-px ricotta slit down the
# middle edged with darker pastry, layer lines alongside it with highlights; twisted tips kept
IRKOTTA_V2 = [
    "................",
    "............OO..",
    ".........OOOd#..",
    "......OOOdldm#..",
    ".....OhhddrRd#..",
    "....OhhddrRdm#..",
    "...OhlddrRdmmm#.",
    "...OhldrRdmmmm#.",
    "..OhldrRdmmmm#..",
    "..OldrRddmmm#...",
    "..Oldmdmhdm#....",
    "..Odmmhdm##.....",
    ".Odmmm###.......",
    ".O####..........",
    "................",
    "................",
]

# Pastizz tal-piżelli v2 (from pizelli_a): same pastry and line style as the ricotta one, round
# puffed back, two layer arcs following it, the mushy peas bulging 2 px along the side seam
PIZELLI_V2 = [
    "................",
    "................",
    "......OOOOOO....",
    "....OOllllmmO#..",
    "....OlhdlmmmdgG.",
    "...OhddlmmmdgG..",
    "...OdhdmmdygG...",
    "..OhdhdmdygG....",
    ".OlhdhddygG.....",
    ".OlhdhdggG......",
    ".OlmdmdgG.......",
    "..OmmdgG........",
    "...OdgG.........",
    "...#G#..........",
    "................",
    "................",
]

V2 = [
    ("hobz_v2", HOBZ_V2, BREAD, "hobz_malti"),
    ("pastizz_irkotta_v2", IRKOTTA_V2, PASTRY, "pastizz_irkotta"),
    ("pastizz_pizelli_v2", PIZELLI_V2, PASTRY, "pastizz_pizelli"),
]
MOD_ITEMS = os.path.join(ART, "..", "mod", "src", "main", "resources", "assets", "mimcontent", "textures", "item")


# ---- Round 3 (2026-11-17, after the critic's v2 review and the owner's bread photos) ----
# Drawn by rules on hand-chosen silhouettes (runs = {row: (first x, last x)}), with hand-placed details.
# Pastizzi pair: one outline (#713c15), one golden pastry ramp, one layer motif (curved dark gap + light lip);
# only the silhouette and the filling differ. Ħobż: shape from bread_owner_3, bake level from bread_owner_1,
# cracked floury top from bread_owner_2.
import math

P3 = {"#": hx("#713c15"), "D": hx("#9a6226"), "d": hx("#b97f34"), "m": hx("#d9a24e"),
      "l": hx("#ebbf6c"), "h": hx("#f8d996"), "r": hx("#f7f3e8"), "R": hx("#d8cfbb"),
      "p": hx("#b5ae52"), "P": hx("#9e9a3e"), "s": hx("#6d6a2a"), "q": hx("#c4b85a"), "Y": hx("#c8c24a"), "y": hx("#a39f35")}
B3 = {"O": hx("#4c2f11"), "o": hx("#6f4418"), "D": hx("#6f4418"), "d": hx("#8c5820"), "m": hx("#a9712d"),
      "l": hx("#c58f43"), "F": hx("#cdb88e"), "f": hx("#b8a074"), "g": hx("#a48659"), "c": hx("#5e3b16")}


def outline3(g):
    out = [r[:] for r in g]
    for y in range(16):
        for x in range(16):
            if g[y][x] == ".":
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if not (0 <= xx < 16 and 0 <= yy < 16) or g[yy][xx] == ".":
                    out[y][x] = "#"
                    break
    return out


def paint(g, ch, pts):
    for x, y in pts:
        if g[y][x] not in ".#":
            g[y][x] = ch


def runs_grid(runs):
    g = [["."] * 16 for _ in range(16)]
    for y, rr in runs.items():
        for a, b in rr:
            for x in range(a, b + 1):
                g[y][x] = "m"
    return g


def sym(runs):
    """Complete a shape by 180-degree rotation (both pointed ends alike)."""
    out = dict(runs)
    for y, rr in runs.items():
        out[15 - y] = [(15 - b, 15 - a) for a, b in rr]
    return out


def rot(pts):
    return [(15 - x, 15 - y) for x, y in pts]


def diagonal_pastry(runs):
    """Long diamond along the top-right/bottom-left diagonal, lit from the top left, rim highlights."""
    g = runs_grid(runs)
    for y in range(16):
        for x in range(16):
            if g[y][x] != ".":
                s = x + y - 15
                g[y][x] = "l" if s <= -3 else ("m" if s < 4 else "d")
    g = outline3(g)
    for y in range(16):
        for x in range(16):
            if g[y][x] == "l" and (g[y - 1][x] == "#" or g[y][x - 1] == "#") and (x + y) % 2 == 0:
                g[y][x] = "h"
    return g


def end_chevrons(g):
    """The layer motif: a dark curved layer gap wrapping each pointed end, a light lip inside it."""
    A1 = [(10, 3), (11, 3), (12, 3), (12, 4), (12, 5)]
    A1h = [(9, 4), (10, 4), (11, 4), (11, 5)]
    for pts, ch in ((A1, "D"), (A1h, "h"), ([(13, 2)], "h")):
        paint(g, ch, pts)
        paint(g, ch, rot(pts))


def arcs(g, C, radii, lipw=1.0):
    """Layer gaps as circle arcs round C (the seam), each with a light lip on its outer side."""
    for y in range(16):
        for x in range(16):
            if g[y][x] in ".#":
                continue
            d = math.hypot(x + .5 - C[0], y + .5 - C[1])
            for r in radii:
                if abs(d - r) < 0.5:
                    g[y][x] = "D"
                elif 0.5 <= d - r < 0.5 + lipw:
                    g[y][x] = "h" if g[y][x] != "d" else "l"


IRK_RUNS = sym({1: [(13, 14)], 2: [(13, 14)], 3: [(9, 14)],  # r6: tips pointed, not cut square
                 4: [(5, 14)], 5: [(4, 13)], 6: [(3, 13)], 7: [(3, 13)]})
# r7: one pixel wider on each side across the middle third (rows 5-10), tips unchanged
IRK_RUNS7 = sym({1: [(13, 14)], 2: [(13, 14)], 3: [(9, 14)], 4: [(5, 14)], 5: [(3, 14)], 6: [(2, 14)], 7: [(2, 14)]})


def irkotta_v3():
    """Folded down the middle: long even diamond, ricotta as a soft lens along the central seam
    (1 px at the ends, 3 px in the middle), shadow side lower right, edged dark."""
    g = diagonal_pastry(IRK_RUNS7)
    # r7: a shorter seam (7 px) so it reads as filling inside the pastry: shade pixel at each end
    lens_r = [(9, 6), (8, 7), (7, 8), (6, 9), (7, 7)]
    lens_R = [(10, 5), (5, 10)]
    paint(g, "r", lens_r)
    paint(g, "R", lens_R)
    lens = set(lens_r + lens_R)
    for x, y in list(lens):
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            q = (x + dx, y + dy)
            if q in lens or g[q[1]][q[0]] in "#.":
                continue
            g[q[1]][q[0]] = "#" if dx + dy > 0 else "D"
    end_chevrons(g)
    for (x, y), ch in {(13, 2): "d", (13, 3): "D", (2, 13): "d"}.items():  # r4: the tips are the crispiest
        g[y][x] = ch
    # r5: no 1-px stalks (they read as a sweet-wrapper twist): blunt pointed tips; layers echoed on the right half
    for (x, y), ch in {(13, 1): ".", (14, 1): ".", (1, 14): ".", (2, 14): ".", (13, 2): "#", (2, 13): "#",
                       (11, 8): "D", (10, 9): "D"}.items():
        g[y][x] = ch
    g = reoutline(g)
    # r7: most highlights become the pea one's mid gold; keep the three nearest the top left
    hs = sorted([(x + y, x, y) for y in range(16) for x in range(16) if g[y][x] == "h"])
    for _, x, y in hs[3:]:
        g[y][x] = "m"
    return g



IRK_RUNS4 = sym({1: [(13, 14)], 2: [(10, 14)], 3: [(7, 14)], 4: [(5, 14)], 5: [(4, 13)], 6: [(3, 13)], 7: [(3, 13)]})


def irkotta_v4():
    """The owner's pick (2026-11-17): round 4's ricotta pastizz, exactly. Long diamond with short tip stalks,
    ricotta lens along the central seam (1 px at the ends, 3 px in the middle), chevrons at both ends,
    crisp darker tips. Later rounds (v5-v7) are kept only as candidate files."""
    g = diagonal_pastry(IRK_RUNS4)
    lens_r = [(10, 5), (9, 6), (8, 7), (7, 8), (6, 9), (5, 10), (8, 6), (7, 7), (6, 8)]
    lens_R = [(9, 7), (8, 8), (7, 9)]
    paint(g, "r", lens_r)
    paint(g, "R", lens_R)
    lens = set(lens_r + lens_R)
    for x, y in list(lens):
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            q = (x + dx, y + dy)
            if q in lens or g[q[1]][q[0]] in "#.":
                continue
            g[q[1]][q[0]] = "#" if dx + dy > 0 else "D"
    end_chevrons(g)
    for (x, y), ch in {(13, 2): "d", (13, 3): "D", (2, 13): "d"}.items():
        g[y][x] = ch
    return g

def tilted_mask(cx=7.8, cy=8.5, a=7.6, b=5.1, ang=24, p=1.7):
    """Rounded body whose long axis rises to the right by ang degrees; p < 2 gives softly pointed ends."""
    t = math.radians(ang)
    g = [["."] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            dx, dy = x + .5 - cx, y + .5 - cy
            u = dx * math.cos(t) - dy * math.sin(t)
            v = dx * math.sin(t) + dy * math.cos(t)
            if abs(u / a) ** p + (v / b) ** 2 <= 1:
                g[y][x] = "m"
    return g


def reoutline(g):
    """Any opaque pixel touching transparency becomes outline (after pixels were cleared)."""
    out = [r[:] for r in g]
    for y in range(16):
        for x in range(16):
            if g[y][x] != "." and any(not (0 <= x + dx < 16 and 0 <= y + dy < 16) or g[y + dy][x + dx] == "."
                                      for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = "#"
    return out


def pizelli_v3R():
    """Piżelli (r6): fatter and rounder than the ricotta one but tilted the same way (~24 deg), box x1-14 y3-13;
    folded down the side, so the peas show as one continuous seam along the upper curved edge (yellow-olive,
    a darker row inside, one shadow pixel); short curved layer lines echo the ricotta one's."""
    g = tilted_mask()
    for y in range(16):
        for x in range(16):
            if g[y][x] != ".":
                lt = 0.5 - 0.07 * ((x - 8) + (y - 8))
                g[y][x] = "l" if lt > 0.72 else ("m" if lt > 0.22 else "d")
    g = outline3(g)
    paint(g, "h", [(4, 7), (5, 7), (6, 8), (7, 9), (8, 6), (9, 7), (10, 8)])
    paint(g, "D", [(4, 8), (5, 8), (6, 9), (7, 10), (8, 7), (9, 8), (10, 9)])
    for x, y in [(6, 5), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 5), (13, 6)]:
        g[y][x] = "Y"
    for x, y in [(6, 6), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 6), (13, 7)]:
        g[y][x] = "y"
    g[8][12] = "s"
    return g


def gbejna_v6():
    """Ġbejna (r6): a round of fresh cheese, box x2-13 y3-13 (centre 8, like vanilla egg/cookie/bread).
    Domed elliptical top (rows 3-7) lightest at the top left, a faint basket-imprint ring; a short side
    (rows 8-12) with subtle ribs on every other pixel; warm dark outline, darker bottom/right."""
    G = [["."] * 16 for _ in range(16)]
    cx, rx, top_cy, bot_cy, ry = 8.0, 6.0, 5.6, 11.4, 2.6
    for y in range(16):
        for x in range(16):
            u = (x + .5 - cx) / rx
            top = u * u + ((y + .5 - top_cy) / ry) ** 2 <= 1
            bot = u * u + ((y + .5 - bot_cy) / ry) ** 2 <= 1
            side = abs(u) <= 1 and top_cy <= y + .5 <= bot_cy
            if top:
                d = 0.55 * (x + .5 - cx) / rx + 0.45 * (y + .5 - top_cy) / ry
                G[y][x] = "T" if d < 0.0 else ("t" if d < 0.6 else "S")
            elif bot or side:
                G[y][x] = "r" if x % 2 else ("S" if x < 9 else "Q")  # the right of the side in shade
    edge = reoutline(G)
    for y in range(16):
        for x in range(16):
            if edge[y][x] == "#" and G[y][x] != ".":
                below = y + 1 >= 16 or G[y + 1][x] == "."
                right = x + 1 >= 16 or G[y][x + 1] == "."
                G[y][x] = "O" if (below or right) and y >= 7 else "o"
    for x in (6, 7, 8, 9):  # faint basket imprint
        if G[6][x] in "tT":
            G[6][x] = "k"
    return G


GBEJNA_PAL = {"T": hx("#f2eedc"), "t": hx("#e6e0c8"), "k": hx("#d8d0b4"), "S": hx("#d8d0b4"), "Q": hx("#cbc2a2"), "r": hx("#c2b68e"),
              "o": hx("#5e4a2e"), "O": hx("#4a3a24")}


def pizelli_v3S():
    """Option S: the ricotta diamond's twin, folded down the SIDE instead of the middle: same silhouette
    and end layers, no central seam, the peas bulging out of the lower-right flank (pushing the outline
    out), one layer arc curling round them."""
    runs = {y: list(rr) for y, rr in IRK_RUNS.items()}
    g = runs_grid(runs)
    g[8][13] = g[10][12] = "m"
    for y in range(16):
        for x in range(16):
            if g[y][x] != ".":
                s = x + y - 15
                g[y][x] = "l" if s <= -3 else ("m" if s < 4 else "d")
    g = outline3(g)
    for y in range(16):
        for x in range(16):
            if g[y][x] == "l" and (g[y - 1][x] == "#" or g[y][x - 1] == "#") and (x + y) % 2 == 0:
                g[y][x] = "h"
    arcs(g, (12.0, 9.5), (4.6,))
    end_chevrons(g)
    for (x, y), c in {(12, 8): "p", (13, 8): "P", (11, 9): "p", (12, 9): "s", (11, 10): "P", (12, 10): "P",
                      (10, 10): "p"}.items():
        g[y][x] = c
    for x, y in [(11, 8), (12, 7), (10, 9), (9, 10), (10, 11), (11, 11), (13, 9), (14, 8), (13, 10), (12, 11)]:
        g[y][x] = "#"
    return g


HOBZ_RUNS = {3: [(5, 10)], 4: [(3, 12)], 5: [(2, 13)], 6: [(1, 14)], 7: [(1, 14)], 8: [(1, 14)], 9: [(1, 14)],
             10: [(1, 14)], 11: [(1, 14)], 12: [(2, 13)], 13: [(3, 12)]}
HOBZ_CRACKS = {(4, 5): "c", (5, 6): "D", (6, 6): "D", (7, 7): "c", (8, 8): "c",
               (8, 4): "c", (9, 5): "c", (10, 5): "c", (11, 6): "D", (12, 6): "D",
               (2, 8): "c", (3, 8): "c", (4, 8): "c", (10, 7): "c", (11, 8): "c",
               (5, 5): "F", (9, 4): "F", (10, 4): "F", (3, 7): "F", (6, 5): "F"}


def hobz_v3(cap=(7.6, 6.6, 6.3, 3.4)):
    """Round crusty ħobża, 14 x 11: domed floury top with a network of dark cracks, golden-brown side
    crust darkening to a burnt base (rows 12-13)."""
    g = runs_grid(HOBZ_RUNS)
    cx, cy, rx, ry = cap
    for y in range(16):
        for x in range(16):
            if g[y][x] == ".":
                continue
            u, v = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            if u * u + v * v <= 1:
                t = 0.55 - 0.35 * u - 0.45 * v
                g[y][x] = "F" if t > 0.75 else ("f" if t > 0.3 else "g")
            else:
                t = 0.5 - 0.06 * (x - 7.5) - 0.12 * (y - 9) - (0.25 if y >= 12 else 0)
                g[y][x] = "l" if t > 0.62 else ("m" if t > 0.32 else ("d" if t > 0.05 else "D"))
    edge = outline3(g)
    for y in range(16):
        for x in range(16):
            if edge[y][x] == "#":
                g[y][x] = "o" if (x + y < 15 and y < 9) else "O"
    for (x, y), ch in HOBZ_CRACKS.items():
        g[y][x] = ch
    return g


V3 = [
    ("hobz_v6", hobz_v3, B3, "hobz_malti"),
    ("pastizz_irkotta_v7", irkotta_v3, P3, None),  # candidate only; the owner picked v4
    ("pastizz_irkotta_v4", irkotta_v4, P3, "pastizz_irkotta"),
    ("pastizz_pizelli_v6", pizelli_v3R, P3, None),  # superseded by the owner's pick (round 8)
    ("pastizz_pizelli_v8a", lambda: [list(r) for r in pizelli_v8a()], PASTRY, None),
    ("pastizz_pizelli_v8b", lambda: [list(r) for r in pizelli_v8b()], P3, "pastizz_pizelli"),
]


# ---- Round 8 (owner 2026-11-17): the piżelli redone from round-1 candidate b ----
# Owner: "its quite close, but it has a bit of a dangly tail which real ones dont have." The tail at the top
# left ((2,2), (3,2), (2,3) and the nub at (3,4)) is removed; (3,3) stays as a short blunt folded point flush
# with the round body (pastizzi_1, pastizzi_4). Not moved: rows 3-14, mass centre 8.3 (vanilla foods 7.5-8.8;
# moving up a row would give 7.3).
def _pizelli_b_no_tail():
    rows = [list(r) for r in PIZELLI_B]
    for x, y in ((2, 2), (3, 2), (2, 3), (3, 4)):
        rows[y][x] = "."
    return ["".join(r) for r in rows]


def pizelli_v8a():
    """Closest to b: tail removed, b's own palette and pixels otherwise."""
    return autooutline(_pizelli_b_no_tail())


def pizelli_v8b():
    """b without the tail, in the accepted irkotta's outline and pastry ramp (P3), with the pea seam in the
    later yellow-olive: lighter #c8c24a along the seam, #a39f35 at its outer edge, one #6d6a2a shadow."""
    g = [list(r) for r in autooutline(_pizelli_b_no_tail())]
    remap = {"O": "#", "y": "Y", "g": "Y", "G": "y"}
    for y in range(16):
        for x in range(16):
            g[y][x] = remap.get(g[y][x], g[y][x])
    g[11][5] = "s"  # one shadow pea deep in the seam
    # light from the top left (tl_minus_br >= 0.05 with the single outline): pastry just inside the
    # right-hand outline goes one step darker
    for y in range(15):
        for x in range(15):
            if (g[y][x + 1] == "#" or g[y + 1][x] == "#") and g[y][x] in "lmd" and x + y > 15:
                g[y][x] = {"l": "m", "m": "d", "d": "D"}[g[y][x]]
            elif g[y][x] == "m" and x + y < 12:  # and the top-left pastry one step lighter
                g[y][x] = "l"
    g = g[1:] + [["."] * 16]  # critic r8: up one row, rows 2-13, centre 7.5 like vanilla
    return ["".join(r) for r in g]


# ---- Pastizzi tax-xema' (owner's facts and photos, 2026-11-17; candidates only, NOT in the mod yet) ----
# Puff pastry, smooth and glossy, no filling showing. Tal-irkotta: a full circle like a mini pie, about double
# the normal pastizz; tal-piżelli: a half-moon, the normal size but about twice as thick. Shapes from the
# owner's photos art/references/xema_owner_*.jpg/png (reference only). Same outline and ramp as irkotta v4.
def top_mask(shape, **k):
    m = [[False] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            m[y][x] = shape(x + .5, y + .5, **k)
    return m

def circle(px, py, cx, cy, rx, ry):
    return ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2 <= 1

def half(px, py, cx, cy, rx, ry, ang):
    t = math.radians(ang)
    dx, dy = px - cx, py - cy
    u = dx * math.cos(t) - dy * math.sin(t)       # along the straight (folded) edge
    v = dx * math.sin(t) + dy * math.cos(t)       # away from it, towards the round back
    return v >= 0 and (u / rx) ** 2 + (v / ry) ** 2 <= 1

def extruded(top, depth, shade_top, ring=None, shine=()):
    """3/4 view of a thick pastry: the top face, and below it the side wall (the top shifted down 1..depth
    rows) shown as stacked pale puff layers, darker towards the right."""
    g = [["."] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if top[y][x]:
                g[y][x] = shade_top(x, y)
            elif any(0 <= y - k and top[y - k][x] for k in range(1, depth + 1)):
                k = min(k for k in range(1, depth + 1) if 0 <= y - k and top[y - k][x])
                right = x >= 10
                g[y][x] = ("l" if not right else "m") if k % 2 == 1 else ("d" if not right else "D")
    g = outline3(g)
    for y in range(1, 16):  # the glossy (waxy) egg-wash catches the light along the top-left rim
        for x in range(1, 16):
            if top[y][x] and g[y][x] not in ".#" and (g[y - 1][x] == "#" or g[y][x - 1] == "#") and x < 8:
                g[y][x] = "h"
            elif top[y][x] and g[y][x] not in ".#" and (g[y - 1][x] == "#") and x < 11:
                g[y][x] = "l"
    for x, y in (ring or []):
        if g[y][x] not in ".#": g[y][x] = "D"
    paint(g, "h", shine)
    return g

def lit_shade(cx, cy, rx, ry):
    def f(x, y):
        u, v = (x + .5 - cx) / rx, (y + .5 - cy) / ry
        lit = -0.6 * u - 0.6 * v
        r = math.hypot(u, v)
        if r > 0.85 and lit < 0.2: return "d"
        return "l" if lit > 0.2 else ("m" if lit > -0.25 else "d")
    return f

def ring_pts(cx, cy, rx, ry, frac):
    pts = []
    for y in range(16):
        for x in range(16):
            r = math.hypot((x + .5 - cx) / rx, (y + .5 - cy) / ry)
            if abs(r - frac) < 0.12: pts.append((x, y))
    return pts

def xema_irkotta_a():
    cx, cy, rx, ry = 8.0, 6.4, 7.0, 3.9
    top = top_mask(circle, cx=cx, cy=cy, rx=rx, ry=ry)
    return extruded(top, 4, lit_shade(cx, cy, rx, ry), ring_pts(cx, cy, rx, ry, 0.62), [(4, 4), (5, 4), (3, 5)])

def xema_irkotta_b():
    cx, cy, rx, ry = 8.0, 7.3, 7.0, 4.6
    top = top_mask(circle, cx=cx, cy=cy, rx=rx, ry=ry)
    return extruded(top, 2, lit_shade(cx, cy, rx, ry), ring_pts(cx, cy, rx, ry, 0.6), [(4, 4), (5, 3), (3, 5)])

def xema_pizelli_a():
    cx, cy, rx, ry = 7.6, 9.6, 7.0, 6.6
    top = top_mask(half, cx=cx, cy=cy, rx=rx, ry=ry, ang=180)   # round back up, folded edge at the bottom
    return extruded(top, 3, lit_shade(cx, cy - 3, rx, ry * 0.6), None, [(5, 6), (6, 5)])

def xema_pizelli_b():
    """Thicker still: the folded edge as a 4-row band of puff layers, the round back tilted a little."""
    cx, cy, rx, ry = 8.0, 8.8, 6.9, 5.8
    top = top_mask(half, cx=cx, cy=cy, rx=rx, ry=ry, ang=190)
    return extruded(top, 4, lit_shade(cx, cy - 3, rx, ry * 0.6), None, [(5, 5), (6, 4)])



# ---- Bread dishes (candidates only, 2026-11-17; NOT in the mod yet) ----
# Ftira: a flattish ring-shaped Maltese sourdough (en Wikipedia "Ftira"; UNESCO 2020), refs ftira_1/2.jpg.
# Ftira għawdxija: Gozo's ftira baked open like a pizza, thin potato slices with ġbejna, olives, capers,
# onion or anchovies (recipe sites; no free photo found). Ħobż biż-żejt: ħobż rubbed with kunserva,
# topped with tuna, capers, olives, onion, mint (en Wikipedia "Maltese bread"), refs hobz_bizzejt_1/2.jpg.
# Crust and flour colours are the accepted ħobż's (B3).
BR = dict(B3)  # the accepted ħobż crust and flour colours, plus toppings
BR.update({"#": hx("#4c2f11"), "w": hx("#f1e4c0"), "W": hx("#d9c9a0"),   # crumb
           "K": hx("#7a2414"), "k": hx("#a8321e"), "q": hx("#c8472a"),   # kunserva
           "t": hx("#c9a77f"), "T": hx("#a78560"),                       # tuna
           "C": hx("#6b7a2a"), "B": hx("#2e2a22"), "b": hx("#4a3f30"),   # caper, olive
           "n": hx("#efe9da"), "M": hx("#4f8a3a"),                       # onion, mint
           "P": hx("#ead39a"), "p": hx("#c99a52"),                       # potato slice, its browned edge
           "G": hx("#f2eedc"), "A": hx("#7a5a44")})                     # ġbejna, anchovy

def E(px, py, cx, cy, rx, ry):
    return ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2 <= 1

def outline_split(g):
    """Outline: lit 'o' on the top/left, dark 'O' on the bottom/right (like the ħobż)."""
    e = outline3(g)
    for y in range(16):
        for x in range(16):
            if e[y][x] == "#" and g[y][x] != ".":
                g[y][x] = "o" if (y < 8 and x + y < 16) else "O"
    return g

def disc3q(cx, cy, rx, ry, depth):
    """Top face + side wall (3/4 view). Returns (grid of 'top'/'side'/None)."""
    z = [[None] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if E(x + .5, y + .5, cx, cy, rx, ry): z[y][x] = "top"
            elif any(E(x + .5, y + .5 - k, cx, cy, rx, ry) for k in range(1, depth + 1)): z[y][x] = "side"
    return z

FLOUR_A = [(4, 5), (5, 5), (11, 5), (12, 5), (5, 9), (6, 9)]
FLOUR_B = [(4, 6), (5, 6), (11, 5), (12, 5), (6, 10), (7, 10)]


def ftira(see_through=False):
    """Plain ftira: a broad FLAT ring, much flatter and wider than the ħobż, with a small hole in the middle;
    matte golden crust with a few white flour patches; a low darker side. a: the hole a dark pit with a lit
    far rim; b: flatter still, the small hole open (see-through)."""
    if see_through:
        cx, cy, rx, ry, depth = 8.0, 7.4, 7.2, 3.9, 2
    else:
        cx, cy, rx, ry, depth = 8.0, 7.2, 7.1, 4.4, 2
    z = disc3q(cx, cy, rx, ry, depth)
    g = [["."] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if z[y][x] is None: continue
            if z[y][x] == "top":
                lit = -0.5 * (x + .5 - cx) / rx - 0.6 * (y + .5 - cy) / ry
                g[y][x] = "l" if lit > 0.15 else ("m" if lit > -0.35 else "d")
            else:
                g[y][x] = "d" if x < 9 else "D"
    for x, y in (FLOUR_B if see_through else FLOUR_A):
        if g[y][x] in "lm": g[y][x] = "F"
        elif g[y][x] == "d": g[y][x] = "f"
    if see_through:
        g[7][7] = g[7][8] = "."
    else:
        for x, y in ((7, 6), (8, 6), (7, 7), (8, 7)):
            g[y][x] = "c"
        g[7][7] = "D"; g[7][8] = "D"
        g[5][7] = "l"; g[5][8] = "l"; g[6][6] = "D"; g[6][9] = "d"
    g = outline_split(g)
    return g


def slices(g, z, centres, r=1.6):
    """Thin potato slices, overlapping like roof tiles: pale disc, browned edge on its lower right."""
    for sx, sy in centres:
        for y in range(16):
            for x in range(16):
                if z[y][x] != "top": continue
                d = math.hypot(x + .5 - sx, (y + .5 - sy) * 1.25)
                if d <= r:
                    edge = d > r - 0.9 and (x + .5 - sx) + (y + .5 - sy) > 0.3
                    g[y][x] = "p" if edge else "P"


def ftira_ghawdxija(variant="a"):
    """Ftira għawdxija: a round flat Gozo bread-pie, the crust rim showing round the edge, the top covered in
    thin overlapping potato slices with fresh ġbejna, black olives, capers, onion (a) or anchovies (b)."""
    if variant == "a":
        cx, cy, rx, ry, depth = 8.0, 7.3, 7.1, 4.6, 2
    else:
        cx, cy, rx, ry, depth = 8.0, 7.6, 6.9, 5.9, 1
    z = disc3q(cx, cy, rx, ry, depth)
    g = [["."] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if z[y][x] == "top":
                inner = E(x + .5, y + .5, cx, cy, rx - 1.3, ry - 1.1)
                lit = -0.5 * (x + .5 - cx) / rx - 0.6 * (y + .5 - cy) / ry
                g[y][x] = "P" if inner else ("l" if lit > 0.1 else ("m" if lit > -0.4 else "d"))
                if inner: z[y][x] = "top"
                else: z[y][x] = "rim"
            elif z[y][x] == "side":
                g[y][x] = "d" if x < 9 else "D"
    if variant == "a":
        cs = [(4.5, 6.0), (7.5, 5.0), (10.8, 5.6), (5.5, 8.6), (8.6, 7.8), (11.4, 8.4), (7.4, 10.0)]
    else:
        cs = [(5.0, 5.0), (8.2, 4.4), (11.2, 5.4), (4.2, 8.0), (7.4, 7.6), (10.6, 8.2), (6.0, 10.6), (9.4, 10.8)]
    slices(g, z, cs)
    if variant == "a":
        tops = {(6, 6): "G", (7, 6): "G", (10, 8): "G", (4, 8): "B", (9, 5): "B", (11, 9): "B",
                (6, 9): "C", (12, 6): "C", (8, 9): "n", (5, 5): "n"}
    else:
        tops = {(5, 6): "A", (6, 7): "A", (7, 8): "A", (10, 5): "A", (9, 6): "A", (8, 7): "A",
                (4, 9): "B", (11, 9): "B", (8, 4): "B", (6, 11): "C", (12, 7): "C", (9, 10): "G", (10, 10): "G"}
    for (x, y), c in tops.items():
        if g[y][x] not in ".": g[y][x] = c
    g = outline_split(g)
    return g


def hobz_bizzejt(variant="a"):
    """Ħobż biż-żejt: ħobż rubbed with kunserva (tomato paste) so the cut face is red, a crust rim round it,
    topped with tuna, capers, olives, onion and mint. a: a thick slice; b: half a ħobża, cut side up, its
    domed floury crust below."""
    if variant == "a":
        cx, cy, rx, ry, depth = 8.0, 7.0, 6.9, 5.0, 2
    else:
        cx, cy, rx, ry, depth = 8.0, 6.2, 7.0, 3.9, 5
    z = disc3q(cx, cy, rx, ry, depth)
    g = [["."] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if z[y][x] == "top":
                inner = E(x + .5, y + .5, cx, cy, rx - 1.2, ry - 1.1)
                lit = -0.5 * (x + .5 - cx) / rx - 0.6 * (y + .5 - cy) / ry
                if inner:
                    g[y][x] = "q" if lit > 0.25 else ("k" if lit > -0.35 else "K")
                else:
                    g[y][x] = "W" if variant == "a" and lit > -0.2 else ("m" if lit > -0.2 else "d")
            elif z[y][x] == "side":
                k = min(k for k in range(1, depth + 1) if E(x + .5, y + .5 - k, cx, cy, rx, ry))
                lit = -0.6 * (x + .5 - cx) / rx - 0.15 * k
                g[y][x] = "l" if lit > 0.25 else ("m" if lit > -0.25 else ("d" if lit > -0.6 else "D"))
    if variant == "b":
        for x, y in ((3, 9), (4, 10), (6, 11), (10, 10), (11, 11)):
            if g[y][x] in "lm": g[y][x] = "f"
        cx2 = {(6, 5): "t", (7, 5): "T", (8, 6): "t", (9, 5): "t", (5, 6): "n", (10, 6): "C", (11, 5): "B",
               (4, 6): "C", (7, 7): "M", (8, 4): "B", (6, 7): "t", (10, 4): "n", (12, 6): "t"}
    else:
        cx2 = {(6, 5): "t", (7, 5): "T", (6, 6): "t", (8, 6): "t", (9, 7): "T", (7, 7): "t",
               (5, 8): "C", (10, 5): "C", (11, 8): "B", (4, 6): "B", (8, 9): "n", (9, 9): "n",
               (10, 7): "M", (6, 9): "t", (12, 6): "n"}
    for (x, y), c in cx2.items():
        if g[y][x] not in ".": g[y][x] = c
    g = outline_split(g)
    return g




def _reoutline_split(g):
    g = [["." if c == "." else ("m" if c in "oO" else c) for c in r] for r in g]
    return outline_split(g)


def ftira_v2():
    """Critic r1 on ftira b: flatter (body rows 5-12, the top dome row removed) and matte floury."""
    g = ftira(True)
    g = [list("." * 16)] + g[:5] + g[6:]          # drop the first dome row, keep the rest in place
    g = _reoutline_split(g)
    for x, y in ((3, 7), (4, 8), (10, 9), (11, 8), (6, 10), (12, 6), (2, 6), (3, 6)):
        if g[y][x] not in ".oO":
            g[y][x] = "F"
    return g


def ftira_ghawdxija_v2():
    """Critic r1 on ftira għawdxija b: gold potato-slice arcs instead of brown squiggles, tomato, more ġbejna."""
    g = [["p" if c == "A" else c for c in r] for r in ftira_ghawdxija("b")]
    for (x, y), c in {(11, 5): "k", (4, 9): "k", (5, 5): "G", (9, 8): "G", (4, 11): "G"}.items():
        g[y][x] = c
    return g


def hobz_bizzejt_v2():
    """Critic r1 on ħobż biż-żejt b: white crumb between crust and topping, more tuna, 3-row side crust."""
    g = hobz_bizzejt("b")
    for x, y in ((3, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 8), (4, 8)):
        g[y][x] = "W"
    for (x, y), c in {(4, 5): "t", (5, 4): "T", (10, 6): "t", (6, 7): "T", (8, 8): "t"}.items():
        g[y][x] = c
    # red at most ~40% of the top: crumb rim along the far edge too, and more tuna flakes
    for (x, y), c in {(6, 3): "W", (7, 3): "W", (8, 3): "W", (9, 3): "W", (4, 4): "W",
                      (7, 6): "t", (11, 7): "T", (12, 5): "t", (9, 4): "t", (5, 7): "t"}.items():
        g[y][x] = c
    g = g[:10] + g[11:] + [list("." * 16)]          # side crust 4 rows -> 3
    return g


# Ħobż biż-żejt v3 (owner 2026-11-17): Maltese bread is cut VERTICALLY into many slices, so the dish is
# upright cross-section slices of the ħobża: the loaf's profile (domed top, flat burnt base), crust all round,
# the pale crumb face rubbed thin with kunserva and oil, a few toppings.
BR["Q"] = hx("#e2a27c")   # crumb with a thin smear of kunserva and oil
SLICE_RUNS = {3: [(5, 10)], 4: [(3, 12)], 5: [(2, 13)], 6: [(1, 14)], 7: [(1, 14)], 8: [(1, 14)], 9: [(1, 14)],
              10: [(1, 14)], 11: [(1, 14)], 12: [(1, 14)], 13: [(2, 13)]}


def _slice(runs, dx=0, dy=0, toppings=None, smear_seed=0):
    g = runs_grid({y + dy: [(a + dx, b + dx) for a, b in rr] for y, rr in runs.items()})
    edge = outline3(g)
    ring = outline3([["." if edge[y][x] == "#" else c for x, c in enumerate(r)] for y, r in enumerate(edge)])
    base = max(y for y in range(16) if any(c != "." for c in g[y]))
    for y in range(16):
        for x in range(16):
            if g[y][x] == ".":
                continue
            if edge[y][x] == "#":
                g[y][x] = "o" if (y < base - 2 and x + y < 16 + dx + dy) else "O"
            elif ring[y][x] == "#":       # the crust band round the slice: burnt at the base, gold on the dome
                g[y][x] = "D" if y >= base - 1 else ("l" if x + y < 13 + dx + dy else ("m" if y < 8 + dy else "d"))
            else:                          # crumb, a thin kunserva smear in streaks, a few holes
                h = (x * 5 + y * 3 + smear_seed) % 7
                g[y][x] = "Q" if h in (0, 3) else ("q" if h == 5 and (x + y) % 3 == 0 else "w")
                if (x * 3 + y * 7 + smear_seed) % 13 == 0:
                    g[y][x] = "W"
    for (x, y), c in (toppings or {}).items():
        if g[y + dy][x + dx] not in ".oO":
            g[y + dy][x + dx] = c
    return g


V3_TOPS = {(5, 6): "t", (6, 6): "T", (6, 7): "t", (9, 9): "t", (10, 9): "T", (10, 6): "B", (11, 6): "b",
           (4, 9): "C", (8, 7): "C", (7, 10): "n", (8, 10): "n", (11, 9): "M", (12, 8): "M"}


def hobz_bizzejt_v3a():
    """One upright slice of ħobża, face-on, topped."""
    return _slice(SLICE_RUNS, toppings=V3_TOPS)


def hobz_bizzejt_v3b():
    """Two slices overlapping: one behind, up and to the right, mostly hidden; the front one topped."""
    small = {y: [(a + 1, b - 2)] for y, ((a, b),) in SLICE_RUNS.items() if y >= 3}
    back = _slice(small, dx=2, dy=-2, smear_seed=3)
    front_runs = {y: [(a, b - 2)] for y, ((a, b),) in SLICE_RUNS.items()}
    front = _slice(front_runs, dx=0, dy=1, toppings={(5, 6): "t", (6, 6): "T", (6, 7): "t", (8, 9): "t",
                   (9, 9): "T", (9, 6): "B", (10, 6): "b", (4, 9): "C", (7, 7): "C", (6, 10): "n",
                   (10, 8): "M", (11, 8): "M"}, smear_seed=1)
    g = [r[:] for r in back]
    for y in range(16):
        for x in range(16):
            if front[y][x] != ".":
                g[y][x] = front[y][x]
    return g


def ftira_v3():
    """Critic r2: ftira v2 up one row (rows 4-11) so its centre matches the ħobż."""
    return ftira_v2()[1:] + [list("." * 16)]


def ftira_ghawdxija_v3():
    """Critic r2: the potato made the signature: overlapping slices as short gold lower-edge crescents on pale
    slice bodies with a white highlight up-left; the scattered gold flecks removed; tomato, olive, caper."""
    g = [["P" if c == "p" else c for c in r] for r in ftira_ghawdxija_v2()]
    for y, spans in ((6, ((3, 4), (7, 8), (11, 12))), (8, ((2, 3), (5, 6), (9, 10))), (10, ((4, 5), (8, 9)))):
        for a, b in spans:
            for x in range(a, b + 1):
                g[y][x] = "p"
            if g[y - 1][a - 1] not in "oOlmd":   # never over the outline or the crust rim
                g[y - 1][a - 1] = "G"
    for (x, y), c in {(6, 7): "k", (10, 10): "k", (4, 10): "B", (9, 5): "C"}.items():
        g[y][x] = c
    return g


BR["r"] = hx("#c8603a")   # kunserva red-orange (critic r3: #e2a27c read as ham)
BR["S"] = hx("#f0dca0")   # potato slice, pale top
BR["s"] = hx("#b07a36")   # potato slice, darker lower-right rim


def hobz_bizzejt_v4():
    """The owner's pick v3b with the kunserva smear red-orange instead of pink."""
    return [["r" if c == "Q" else c for c in r] for r in hobz_bizzejt_v3b()]


def ftira_ghawdxija_v4():
    """Critic r3: the face as fish-scale potato slices like roof tiles: pale tops, a darker lower-right rim on
    each slice, rows offset so the arcs overlap; ġbejna cut to three spots; olives, capers, tomato kept."""
    g = ftira_ghawdxija_v3()
    keep = set("oOlmdBCk")
    for y in range(16):
        for x in range(16):
            if g[y][x] not in keep and g[y][x] != ".":
                g[y][x] = "S"
    for y, xs in ((6, (4, 7, 10)), (8, (3, 6, 9, 12)), (10, (5, 8, 11))):
        for x in xs:
            for px, py in ((x - 1, y), (x, y), (x + 1, y - 1)):   # a short arc: bottom edge turning up the right
                if g[py][px] == "S":
                    g[py][px] = "s"
    for x, y in ((5, 5), (8, 7), (7, 9)):
        g[y][x] = "G"
    return g


def autooutline(rows):
    """Every opaque pixel touching transparency becomes outline: lit 'O' where it faces up/left,
    shaded '#' where it faces down/right; filling at the edge becomes the filling's shade."""
    g = [list(r) for r in rows]
    out = [r[:] for r in g]
    for y in range(16):
        for x in range(16):
            ch = g[y][x]
            if ch == ".":
                continue
            score, edge = 0, False
            for dx, dy, w in ((0, -1, 1), (-1, 0, 1), (0, 1, -1), (1, 0, -1)):
                xx, yy = x + dx, y + dy
                if not (0 <= xx < 16 and 0 <= yy < 16) or g[yy][xx] == ".":
                    edge = True
                    score += w
            if edge:
                if ch in FILL_SHADE:
                    out[y][x] = FILL_SHADE[ch]
                elif score > 0 or (score == 0 and x + y < 15):
                    out[y][x] = "O"
                else:
                    out[y][x] = "#"
            elif ch == "x":
                print(f"warning: interior outline pixel at {x},{y}")
                out[y][x] = "D"
    return ["".join(r) for r in out]


def render(rows, pal):
    assert len(rows) == 16, len(rows)
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row, len(row))
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), pal[ch] + (255,))
    return im


def check(name, rows):
    """Warn about stray pixels: opaque pixels with no opaque 4-neighbour."""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            n = 0
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < 16 and 0 <= yy < 16 and rows[yy][xx] != ".":
                    n += 1
            if n == 0:
                print(f"warning: {name}: stray pixel at {x},{y}")


def preview(images):
    slot = (139, 139, 139, 255)
    S = 8
    cell = 16 * S + 16
    van = []
    for v in ("bread", "cookie", "pumpkin_pie", "baked_potato", "egg"):
        p = os.path.join(VANILLA, v + ".png")
        if os.path.exists(p):
            van.append(("vanilla " + v, Image.open(p).convert("RGBA")))
    big = [(n, im) for n, im in images] + van
    cols = 6
    rows_big = (len(big) + cols - 1) // cols
    small_h = 16 * 2 + 40
    W = cols * cell + 16
    H = 16 + rows_big * (cell + 14) + 2 * small_h + 20
    sheet = Image.new("RGBA", (W, H), (198, 198, 198, 255))
    d = ImageDraw.Draw(sheet)
    for i, (n, im) in enumerate(big):
        x0 = 16 + (i % cols) * cell
        y0 = 16 + (i // cols) * (cell + 14)
        d.rectangle([x0, y0, x0 + 16 * S - 1, y0 + 16 * S - 1], fill=slot)
        e = im.resize((16 * S, 16 * S), Image.NEAREST)
        sheet.alpha_composite(e, (x0, y0))
        d.text((x0, y0 + 16 * S + 1), label(n), fill=(30, 30, 30, 255), font=label_font(12))
    # real-size rows: 1x and 2x, on slot grey, everything side by side
    y = 16 + rows_big * (cell + 14) + 6
    for scale in (1, 2):
        d.text((16, y), f"{scale}x", fill=(30, 30, 30, 255), font=label_font(12))
        x = 40
        for n, im in big:
            sz = 18 * scale
            d.rectangle([x, y, x + sz - 1, y + sz - 1], fill=slot)
            sheet.alpha_composite(im.resize((16 * scale, 16 * scale), Image.NEAREST), (x + scale, y + scale))
            x += sz + 6 * scale
        y += small_h
    return sheet


def main():
    os.makedirs(OUT, exist_ok=True)
    images = []
    for name, rows, pal in CANDIDATES:
        check(name, rows)
        if pal is PASTRY:
            rows = autooutline(rows)
        im = render(rows, pal)
        im.save(os.path.join(OUT, name + ".png"))
        images.append((name, im))
    for name, rows, pal, item in V2:  # round 2 kept as candidates only
        check(name, rows)
        render(rows, pal).save(os.path.join(OUT, name + ".png"))
    v3 = []
    for name, make, pal, item in V3:
        g = make()
        check(name, ["".join(r) for r in g])
        im = render(["".join(r) for r in g], pal)
        im.save(os.path.join(OUT, name + ".png"))
        if item:
            im.save(os.path.join(MOD_ITEMS, item + ".png"))
        if name not in ("pastizz_pizelli_v6", "pastizz_irkotta_v7"):  # superseded; kept as files only
            v3.append((name, im))
    # the ġbejna (r6) is made here now (gbejna_v6); pilot_textures.gbejna is kept for history
    gb = render(["".join(r) for r in gbejna_v6()], GBEJNA_PAL)
    gb.save(os.path.join(OUT, "gbejna_v6.png"))
    gb.save(os.path.join(MOD_ITEMS, "gbejna.png"))
    v3.append(("gbejna_v6", gb))
    preview(v3).save(os.path.join(OUT, "preview.png"))
    for name, make in (("ftira_a", lambda: ftira(False)), ("ftira_b", lambda: ftira(True)),
                       ("ftira_ghawdxija_a", lambda: ftira_ghawdxija("a")), ("ftira_ghawdxija_b", lambda: ftira_ghawdxija("b")),
                       ("hobz_bizzejt_a", lambda: hobz_bizzejt("a")), ("hobz_bizzejt_b", lambda: hobz_bizzejt("b")),
                       ("ftira_v2", ftira_v2), ("ftira_ghawdxija_v2", ftira_ghawdxija_v2), ("hobz_bizzejt_v2", hobz_bizzejt_v2),
                       ("hobz_bizzejt_v3a", hobz_bizzejt_v3a), ("hobz_bizzejt_v3b", hobz_bizzejt_v3b),
                       ("ftira_v3", ftira_v3), ("ftira_ghawdxija_v3", ftira_ghawdxija_v3),
                       ("hobz_bizzejt_v4", hobz_bizzejt_v4), ("ftira_ghawdxija_v4", ftira_ghawdxija_v4)):
        render(["".join(r) for r in make()], BR).save(os.path.join(OUT, name + ".png"))  # candidates only
    # tax-xema': the owner accepted both "b" candidates (2026-11-17); they are installed in the mod
    for name, make, item in (("pastizz_xema_irkotta_a", xema_irkotta_a, None),
                             ("pastizz_xema_irkotta_b", xema_irkotta_b, "pastizz_xema_irkotta"),
                             ("pastizz_xema_pizelli_a", xema_pizelli_a, None),
                             ("pastizz_xema_pizelli_b", xema_pizelli_b, "pastizz_xema_pizelli")):
        im = render(["".join(r) for r in make()], P3)
        im.save(os.path.join(OUT, name + ".png"))
        if item:
            im.save(os.path.join(MOD_ITEMS, item + ".png"))
    round5()
    print("wrote", len(images), "round-1 candidates, v2 and v3 pieces (v3 into the mod) and preview.png")


# ---- Ftira, frozen (owner accepted ftira_v3, 2026-11-17): installed as ftira.png; byte-identical to the candidate ----
FTIRA_ACCEPTED = [
    "................",
    "................",
    "................",
    "................",
    "...ooooooooOO...",
    ".ooFFFloommmFOO.",
    ".olFllo..OmmmdO.",
    ".OlmFmmOOmmFddO.",
    ".OmmmmmmddFdddO.",
    ".OddmmFfddddDDO.",
    "..OOdddddDDDOO..",
    "....OOOOOOOO....",
    "................",
    "................",
    "................",
    "................",
]


# ---- Round 5 (2026-11-17): ħobż biż-żejt and ftira għawdxija redone from scratch ----
# Ħobż biż-żejt (owner): the ħobża is sliced VERTICALLY into many slices, so each slice is a cross-section of the
# round loaf: wide, low and rounded (not a sandwich-loaf dome), dark crust all round with a burnt flat base, and
# the crumb VERY white, clearly white under a thin smear of kunserva and a few toppings.
V5 = dict(B3)
V5.update({"O": hx("#4c2f11"), "o": hx("#6f4418"), "c": hx("#3e260d"),     # outline lit / shade, burnt base
           "w": hx("#f4efe2"), "W": hx("#e3dccb"),                         # crumb, crumb holes / shade
           "r": hx("#c8603a"), "R": hx("#a84a2c"),                         # kunserva smear, its thicker bits
           "t": hx("#c9a77f"), "T": hx("#a78560"),                         # tuna flakes
           "B": hx("#2e2a22"), "b": hx("#5a4c3a"),                         # olive, its shine
           "C": hx("#6b7a2a"), "M": hx("#4f8a3a"), "N": hx("#76ad52")})    # caper, mint leaf, mint lit


def _slice_runs(runs, dx=0, dy=0):
    m = [[False] * 16 for _ in range(16)]
    for y, (x0, x1) in runs.items():
        for x in range(x0 + dx, x1 + dx + 1):
            m[y + dy][x] = True
    return m


def _slice_paint(m, toppings, holes=()):
    """Thin crust like a real cut ħobża: dark outline all round, a 1-px golden crust band over the top, a burnt
    band along the flat base; everything else is very white crumb (greyer next to the lower-right crust)."""
    g = [["w" if m[y][x] else "." for x in range(16)] for y in range(16)]
    edge = outline3(g)
    ys = [y for y in range(16) if any(m[y])]
    top, base = ys[0], ys[-1]
    xs = [x for x in range(16) if any(m[y][x] for y in ys)]
    midx = (xs[0] + xs[-1]) / 2
    isedge = lambda x, y: 0 <= x < 16 and 0 <= y < 16 and edge[y][x] == "#" and m[y][x]
    for y in ys:
        for x in range(16):
            if not m[y][x]:
                continue
            if edge[y][x] == "#":
                g[y][x] = "c" if y >= base - 1 and (y + 1 >= 16 or not m[y + 1][x]) else \
                          ("o" if (x - midx) * 0.6 + (y - top) < 3.5 else "O")
            elif y >= base - 1:
                g[y][x] = "D"                                       # burnt base
            elif isedge(x, y - 1):
                g[y][x] = "l" if x < midx else ("m" if x < midx + 4 else "d")   # golden top crust
            elif isedge(x + 1, y) and x > midx or y == base - 2:
                g[y][x] = "W"
    for x, y in holes:
        if g[y][x] == "w": g[y][x] = "W"
    for (x, y), ch in toppings.items():
        if g[y][x] in "wW": g[y][x] = ch
    return g


SLICE5 = {4: (5, 10), 5: (3, 12), 6: (2, 13), 7: (1, 14), 8: (1, 14), 9: (1, 14), 10: (1, 14), 11: (2, 13), 12: (3, 12)}


def hobz_bizzejt_v5a():
    """One upright slice, face on: the round loaf's cross-section, 14 x 9 (rows 4-12)."""
    tops = {(5, 7): "t", (6, 7): "T", (4, 8): "r", (5, 8): "r", (7, 8): "r", (8, 8): "R", (9, 7): "r", (10, 7): "r",
            (6, 8): "t", (11, 8): "B", (11, 7): "b", (4, 9): "C", (10, 9): "t", (9, 9): "T", (6, 10): "M", (7, 10): "N",
            (12, 9): "C", (8, 9): "r"}
    return _slice_paint(_slice_runs(SLICE5), tops, [(9, 6), (3, 10), (12, 6)])


def hobz_bizzejt_v5b():
    """Two slices: one upright behind (upper right), the front one leaning back against it, top tipped right."""
    back = _slice_paint(_slice_runs({2: (7, 12), 3: (5, 13), 4: (4, 14), 5: (4, 14), 6: (4, 14), 7: (4, 14),
                                     8: (5, 14), 9: (5, 13), 10: (7, 12)}),
                        {(9, 5): "r", (10, 5): "r", (11, 6): "r", (12, 5): "C", (10, 6): "t", (13, 6): "t"}, [(8, 6)])
    front = _slice_paint(_slice_runs({7: (5, 10), 8: (3, 11), 9: (2, 12), 10: (2, 12), 11: (1, 11), 12: (1, 11),
                                      13: (1, 10), 14: (2, 8)}),
                         {(4, 10): "t", (5, 10): "T", (3, 11): "r", (4, 11): "r", (6, 11): "r", (7, 11): "R",
                          (8, 10): "r", (9, 10): "r", (8, 11): "B", (8, 12): "b", (3, 12): "C", (6, 12): "M", (7, 12): "N",
                          (10, 11): "t", (5, 11): "t"}, [(7, 9), (2, 12)])
    g = [r[:] for r in back]
    for y in range(16):
        for x in range(16):
            if front[y][x] != ".":
                g[y][x] = front[y][x]
    return g


# Ftira għawdxija (owner): "not made from a ftira at all. its a differently baked thing." The owner's photos
# (art/references/ftira_ghawdxija_owner_*, reference only): a round open bake, a THICK golden pastry rim folded
# over the edge in pleats like a rustic galette, the middle covered in overlapping pale potato slices, with
# tomato, red onion, olives and herbs between them.
FG = {"O": hx("#6a3f16"), "o": hx("#8a5622"),                           # outline lit / shade
      "h": hx("#f2cd85"), "l": hx("#e0a956"), "m": hx("#c98a3c"), "d": hx("#a2652a"), "D": hx("#7e4c1e"),  # pastry
      "x": hx("#4a3018"),                                                # shadow under the folded rim
      "S": hx("#f3e6b4"), "s": hx("#c9a24e"), "u": hx("#a98a4a"),       # potato slice, its edge, a roasted spot
      "r": hx("#c63d26"), "R": hx("#8f2a1c"),                            # tomato
      "v": hx("#8a3d68"), "B": hx("#2b2620"), "g": hx("#5d7f34")}        # red onion, olive, herbs


def _galette(cx, cy, rx, ry, depth, rim_in, folds, filling_cs, disc, filler, phase=0.0, wall="d"):
    g = [["."] * 16 for _ in range(16)]
    zone = [[None] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            u, v = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            th = math.atan2(v, u)
            f = (th / (2 * math.pi) * folds + phase) % 1.0                 # position within a pleat
            rout = 1.0 - (0.09 if f < 0.16 else 0.0)                      # each pleat's edge tucks in a little
            r = math.hypot(u, v)
            if r <= rout:
                zone[y][x] = ("fill", f) if r < rim_in else ("rim", f)
            elif depth and any(math.hypot(u, (y + .5 - k - cy) / ry) <= rout for k in range(1, depth + 1)) and v > 0:
                zone[y][x] = ("side", f)
    for y in range(16):
        for x in range(16):
            z = zone[y][x]
            if not z: continue
            kind, f = z
            lit = -0.8 * (x + .5 - cx) / rx - 0.85 * (y + .5 - cy) / ry      # light from the top left
            if kind == "rim":
                k = lit + (0.35 if f > 0.55 else 0.0) - (0.5 if f < 0.16 else 0.0)   # pleat: lit roll, dark crease
                g[y][x] = "h" if k > 0.6 else "l" if k > 0.15 else "m" if k > -0.3 else "d" if k > -0.75 else "D"
            elif kind == "side":
                g[y][x] = "d" if x + .5 < cx else "D"
            else:
                g[y][x] = filler(x, y)
    for (sx, sy) in filling_cs:                                            # potato slices, back to front
        for y in range(16):
            for x in range(16):
                if not zone[y][x] or zone[y][x][0] != "fill": continue
                du, dv = (x + .5 - sx) / disc[0], (y + .5 - sy) / disc[1]
                d = math.hypot(du, dv)
                if d <= 1:
                    g[y][x] = "s" if (d > 0.55 and du + dv > 0.5) else "S"
    # the rim's inner wall: in shade on the top left (it faces away from the light), lit on the bottom right
    for y in range(16):
        for x in range(16):
            if not (zone[y][x] and zone[y][x][0] == "rim"): continue
            nb = lambda dx, dy: 0 <= x + dx < 16 and 0 <= y + dy < 16 and zone[y + dy][x + dx] and zone[y + dy][x + dx][0] == "fill"
            if nb(1, 0) or nb(0, 1):
                g[y][x] = wall
            elif nb(-1, 0) or nb(0, -1):
                g[y][x] = "l"
    return g, zone


def _ftg_filler(x, y):
    return "r"


def _fill_map(g, z, rows):
    """Hand-placed filling: potato slices (S lit, s their lower-right edge, u a roasted spot) with tomato,
    red onion, olive and herbs between them; '.' keeps what is there; only filling pixels change."""
    for y, row in rows.items():
        for x, c in enumerate(row):
            if c != "." and z[y][x] and z[y][x][0] == "fill":
                g[y][x] = c


def _ftg_finish(g):
    e = outline3(g)
    for y in range(16):
        for x in range(16):
            if e[y][x] == "#" and g[y][x] != ".":
                g[y][x] = "O" if (y >= 8 or x + y > 17) else "o"
    return g


def _potatoes(g, z, discs, disc, gaps, extra=None):
    """Filling: a bed of tomato, red onion, olive and herbs ('gaps', picked per pixel), then potato slices laid
    over it in the order given (later ones overlap earlier ones). disc: rows of the slice shape, '.' = not part
    of it, 'S' pale top, 's' its darker lower-right edge."""
    for y in range(16):
        for x in range(16):
            if z[y][x] and z[y][x][0] == "fill":
                g[y][x] = gaps[(x * 5 + y * 3) % len(gaps)]
    for x0, y0 in discs:
        for dy, row in enumerate(disc):
            for dx, c in enumerate(row):
                x, y = x0 + dx, y0 + dy
                if c != "." and 0 <= x < 16 and 0 <= y < 16 and z[y][x] and z[y][x][0] == "fill":
                    g[y][x] = c
    for (x, y), c in (extra or {}).items():
        if z[y][x] and z[y][x][0] == "fill":
            g[y][x] = c


def ftira_ghawdxija_v5a():
    """From above: round, a thick pleated golden rim (3 px), round pale potato slices overlapping in rows across
    the middle, tomato, red onion, olive and herbs showing between them. 14 px across, rows 1-14."""
    g, z = _galette(8.0, 8.0, 7.0, 7.0, 0, 0.62, 9, [], (1, 1), _ftg_filler, 0.3, wall="m")
    _potatoes(g, z, [(4, 4), (8, 4), (2, 7), (6, 7), (10, 7), (4, 10), (8, 10)],
              (".SS.", "SSSs", ".ss."), "rRrvrRgr", {(7, 8): "u", (5, 5): "u", (10, 6): "B", (8, 9): "g", (10, 10): "R", (11, 8): "R"})
    return _ftg_finish(g)


def ftira_ghawdxija_v5b():
    """Three-quarter view: the same bake as an ellipse with a low side, the near rim thick and rolled over,
    the potato slices squashed into ovals. 14 x 11, rows 3-13."""
    g, z = _galette(8.0, 7.3, 7.0, 4.6, 2, 0.6, 9, [], (1, 1), _ftg_filler, 0.3)
    _potatoes(g, z, [(4, 5), (8, 5), (2, 7), (6, 7), (10, 7), (4, 9), (8, 9)],
              ("SSSs", ".ss."), "rRrvrRgr", {(7, 7): "u", (11, 6): "B", (5, 9): "g", (9, 9): "v"})
    return _ftg_finish(g)


FG["H"] = hx("#fbf3d0")   # potato slice highlight


def ftira_ghawdxija_v6():
    """Critic r5 on v5a: the reverse of 'pizza': a red tomato bed (darker in the lower-right gaps) with five big
    pale potato slices, 3 x 2 each, red showing between them; only four accents. Rim pixels as in v5a."""
    g, z = _galette(8.0, 8.0, 7.0, 7.0, 0, 0.62, 9, [], (1, 1), _ftg_filler, 0.3, wall="m")
    fill = lambda x, y: z[y][x] and z[y][x][0] == "fill"
    for y in range(16):
        for x in range(16):
            if fill(x, y):
                g[y][x] = "R" if x + y >= 17 else "r"
    for x0, y0 in ((4, 4), (8, 4), (5, 7), (9, 7), (6, 10)):
        for dx, c in enumerate("HSS"):
            if fill(x0 + dx, y0): g[y0][x0 + dx] = c
        for dx in range(3):
            if fill(x0 + dx, y0 + 1): g[y0 + 1][x0 + dx] = "s"
    for (x, y), c in {(7, 6): "B", (11, 9): "B", (4, 9): "v", (8, 9): "g"}.items():
        if fill(x, y): g[y][x] = c
    return _ftg_finish(g)


# critic r6: an exact filling layout (no straight red lines); critic key -> palette: H=H, P=S, S=s, R=r, D=R, O=B, N=v, G=g
FTG_V7 = {4: (5, "RHPSDR"), 5: (4, "RPPPSHPR"), 6: (4, "HPSNRPPS"), 7: (4, "PPPSGPSD"), 8: (4, "SSRHPPOR"),
          9: (4, "RODPPPSH"), 10: (4, "RHPSSRPP"), 11: (5, "DSRGRS")}


def ftira_ghawdxija_v7():
    """v6's rim, size and outline; the filling replaced by FTG_V7 (rim pixels kept where a cell is rim)."""
    g, z = _galette(8.0, 8.0, 7.0, 7.0, 0, 0.62, 9, [], (1, 1), _ftg_filler, 0.3, wall="m")
    key = {"H": "H", "P": "S", "S": "s", "R": "r", "D": "R", "O": "B", "N": "v", "G": "g"}
    for y, (x0, row) in FTG_V7.items():
        for i, c in enumerate(row):
            x = x0 + i
            if z[y][x] and z[y][x][0] == "fill":
                g[y][x] = key[c]
    return _ftg_finish(g)


# ---- Round 6 (owner 2026-11-17): ħobż biż-żejt "far too much white and its really bone white". The owner's photos
# art/references/hobz_bizzejt_owner_1/2.jpg (reference only): the slice face is covered almost edge to edge in
# kunserva, heaped with tuna, olives, capers, onion, a basil/mint leaf, sometimes crumbled ġbejna; only a golden
# toasted crust rim shows. Same rounded slice outline as v5a.
V6 = dict(V5)
V6.update({"r": hx("#b8432c"), "q": hx("#c8603a"), "R": hx("#8f2a1c"),          # kunserva base, lit, shadow
           "B": hx("#2b2620"), "C": hx("#6b7a2a"), "G": hx("#ece4cf"), "e": hx("#e6d9bc"),
           "n": hx("#c9a0b8")})                                                   # onion (pale pink-white)


def _toast(m, tops, crumb_line=False):
    """Slice outline from the mask: dark outline (burnt base), a 1-px golden toasted crust band all round
    (lit top left, darker lower right), the face covered in kunserva, lit at the top left, shaded lower right."""
    g = [["r" if m[y][x] else "." for x in range(16)] for y in range(16)]
    edge = outline3(g)
    inner = [["." if edge[y][x] == "#" else g[y][x] for x in range(16)] for y in range(16)]
    ring = outline3(inner)
    ys = [y for y in range(16) if any(m[y])]
    top, base = ys[0], ys[-1]
    xs = [x for x in range(16) if any(m[y][x] for y in ys)]
    midx = (xs[0] + xs[-1]) / 2
    for y in ys:
        for x in range(16):
            if not m[y][x]:
                continue
            k = (x - midx) * 0.45 + (y - top) * 0.9
            if edge[y][x] == "#":
                g[y][x] = "c" if y == base else ("o" if k < 3.5 else "O")
            elif ring[y][x] == "#":
                g[y][x] = "D" if y >= base - 1 else ("l" if k < 1.8 else "m" if k < 4.2 else "d")
            else:
                g[y][x] = "q" if k < 1.2 else ("R" if k > 5.6 else "r")
                if crumb_line and ring[y - 1][x] == "#" and y - 1 > top:
                    g[y][x] = "e"
    for (x, y), ch in tops.items():
        if g[y][x] in "qrRe": g[y][x] = ch
    return g


def hobz_bizzejt_v6a():
    """One slice (v5a's outline), red face heaped with toppings."""
    tops = {(5, 6): "t", (6, 6): "T", (6, 7): "t", (9, 6): "B", (10, 6): "b", (8, 7): "C", (4, 8): "C",
            (11, 7): "t", (11, 8): "T", (12, 8): "t", (7, 8): "G", (8, 8): "G", (5, 9): "M", (6, 9): "N",
            (9, 9): "t", (10, 9): "T", (3, 7): "n", (12, 6): "C", (10, 8): "R", (7, 9): "R"}
    return _toast(_slice_runs(SLICE5), tops)


def hobz_bizzejt_v6b():
    """Two smaller slices side by side and staggered, as on a plate (owner photo 1)."""
    left = _toast(_slice_runs({5: (2, 5), 6: (1, 6), 7: (0, 7), 8: (0, 7), 9: (0, 7), 10: (0, 7), 11: (1, 6), 12: (2, 5)}),
                  {(2, 7): "t", (3, 7): "T", (5, 7): "B", (5, 8): "b", (2, 9): "C", (3, 8): "G", (4, 9): "t", (5, 9): "T",
                   (3, 10): "M", (4, 10): "N"})
    right = _toast(_slice_runs({3: (10, 13), 4: (9, 14), 5: (8, 15), 6: (8, 15), 7: (8, 15), 8: (8, 15), 9: (9, 14), 10: (10, 13)}),
                   {(10, 5): "t", (11, 5): "T", (10, 6): "t", (13, 5): "C", (13, 6): "B", (13, 7): "b", (10, 7): "G",
                    (11, 7): "M", (12, 7): "N", (12, 6): "R"})
    g = [r[:] for r in left]
    for y in range(16):
        for x in range(16):
            if right[y][x] != "." and g[y][x] == ".":
                g[y][x] = right[y][x]
    return g


# Ftira għawdxija v8 (owner: prefers v5b, "maybe clean that one up a bit on the crust area"): v5b's filling exactly,
# the rim redrawn as one clean thick folded band: smooth outline, highlight along the top-left, shade lower right,
# the near rim a thick roll with regular pleat creases.
FTG_V8_RIM = [
    "................",
    "................",
    "....oooooooo....",
    "..oohhllllllmoo.",
    ".ohlm******lmdO.",
    ".ohm********ldO.",
    ".olm********ldO.",
    ".olm********mdO.",
    ".Olml******lmdO.",
    ".Olhhllhllmlm dO.".replace(" ", ""),
    ".OmlmdlmdmmdmDO.",
    "..OdmDdmDddDDO..",
    "....OOOOOOOO....",
    "................",
    "................",
    "................",
]


def ftira_ghawdxija_v8():
    src = up1(ftira_ghawdxija_v5b)()
    g = [list(r) for r in FTG_V8_RIM]
    for y in range(16):
        for x in range(16):
            if g[y][x] == "*":
                g[y][x] = src[y][x]
    return g


def ftira_ghawdxija_v9():
    """Critic r7 on v8: back to v5b's round, slightly lumpy outline; v8's filling and rim colours kept.
    Any pastry pixel left touching transparency becomes outline, so the outline has no gaps."""
    g = ftira_ghawdxija_v8()
    for (x, y), c in {(14, 3): ".", (1, 4): ".", (14, 4): ".", (2, 4): "o", (13, 4): "O",
                      (1, 10): ".", (14, 10): ".", (2, 10): "O", (13, 10): "O",
                      (4, 12): ".", (11, 12): ".", (4, 11): "O", (11, 11): "O",
                      (1, 7): ".", (2, 7): "o"}.items():
        g[y][x] = c
    for y in range(16):
        for x in range(16):
            if g[y][x] not in ".oO" and any(not (0 <= x + dx < 16 and 0 <= y + dy < 16) or g[y + dy][x + dx] == "."
                                            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                print(f"v9: outline gap filled at {x},{y}")
                g[y][x] = "O" if (y >= 8 or x + y > 17) else "o"
    return g


def up1(make):
    """Up one row, so the mass centre sits near vanilla's 7.5-8.0."""
    return lambda: make()[1:] + [["."] * 16]


V5_CANDIDATES = (("hobz_bizzejt_v5a", up1(hobz_bizzejt_v5a), V5), ("hobz_bizzejt_v5b", up1(hobz_bizzejt_v5b), V5),
                 ("ftira_ghawdxija_v5a", ftira_ghawdxija_v5a, FG), ("ftira_ghawdxija_v5b", up1(ftira_ghawdxija_v5b), FG),
                 ("ftira_ghawdxija_v6", ftira_ghawdxija_v6, FG), ("ftira_ghawdxija_v7", ftira_ghawdxija_v7, FG),
                 ("hobz_bizzejt_v6a", up1(hobz_bizzejt_v6a), V6), ("hobz_bizzejt_v6b", hobz_bizzejt_v6b, V6),
                 ("ftira_ghawdxija_v8", ftira_ghawdxija_v8, FG), ("ftira_ghawdxija_v9", ftira_ghawdxija_v9, FG))
FINAL = ("hobz_bizzejt_v6a", "ftira_ghawdxija_v5b", "ftira_ghawdxija_v9")   # critic r7: bread_final.png
COMPARE = ("hobz_bizzejt_v6a", "hobz_bizzejt_v6b", "ftira_ghawdxija_v5b", "ftira_ghawdxija_v8")  # owner r6


def round5():
    """Install the frozen ftira; write the round-5 candidates (NOT installed) and bread_compare.png."""
    fi = render(FTIRA_ACCEPTED, BR)
    fi.save(os.path.join(MOD_ITEMS, "ftira.png"))
    ims = [("Ħobż", Image.open(os.path.join(MOD_ITEMS, "hobz_malti.png")).convert("RGBA")), ("Ftira", fi)]
    picked = {}
    for name, make, pal in V5_CANDIDATES:
        rows = ["".join(r) for r in make()]
        check(name, rows)
        im = render(rows, pal)
        im.save(os.path.join(OUT, name + ".png"))
        lbl = ("Ħobż biż-żejt " if name.startswith("hobz") else "Ftira għawdxija ") + name.split("_")[-1]
        if name in COMPARE or name in FINAL:
            picked[name] = (lbl, im)
    head = ims[:]
    ims += [picked[n] for n in COMPARE]
    final = head + [picked[n] for n in FINAL]
    for v in ("bread", "pumpkin_pie", "cookie"):
        ims.append(("vanilla " + v, Image.open(os.path.join(VANILLA, v + ".png")).convert("RGBA")))
    compare(ims).save(os.path.join(OUT, "bread_compare.png"))
    van = [i for i in ims if i[0].startswith("vanilla")]
    compare(final + van).save(os.path.join(OUT, "bread_final.png"))


def compare(ims):
    slot, bg, ink = (139, 139, 139, 255), (198, 198, 198, 255), (30, 30, 30, 255)
    S, cw = 8, 16 * 8 + 20
    W = 16 + len(ims) * cw
    H = 16 + 22 + 18 + 40 + 16 * S + 40
    sheet = Image.new("RGBA", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    f = label_font(12)
    for i, (n, im) in enumerate(ims):
        x0 = 16 + i * cw
        d.rectangle([x0, 16, x0 + 17, 33], fill=slot)                       # 1x
        sheet.alpha_composite(im, (x0 + 1, 17))
        d.rectangle([x0 + 30, 16, x0 + 30 + 35, 51], fill=slot)            # 2x
        sheet.alpha_composite(im.resize((32, 32), Image.NEAREST), (x0 + 32, 18))
        y8 = 64
        d.rectangle([x0, y8, x0 + 16 * S - 1, y8 + 16 * S - 1], fill=slot)  # 8x
        sheet.alpha_composite(im.resize((16 * S, 16 * S), Image.NEAREST), (x0, y8))
        d.text((x0, y8 + 16 * S + 4), n, fill=ink, font=f)
    return sheet


if __name__ == "__main__":
    main()
