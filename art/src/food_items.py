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
from PIL import Image, ImageDraw

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
    ("pastizz_irkotta_v7", irkotta_v3, P3, "pastizz_irkotta"),
    ("pastizz_pizelli_v6", pizelli_v3R, P3, "pastizz_pizelli"),
]


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
        d.text((x0, y0 + 16 * S + 1), n, fill=(30, 30, 30, 255))
    # real-size rows: 1x and 2x, on slot grey, everything side by side
    y = 16 + rows_big * (cell + 14) + 6
    for scale in (1, 2):
        d.text((16, y), f"{scale}x", fill=(30, 30, 30, 255))
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
        v3.append((name, im))
    # the ġbejna (r6) is made here now (gbejna_v6); pilot_textures.gbejna is kept for history
    gb = render(["".join(r) for r in gbejna_v6()], GBEJNA_PAL)
    gb.save(os.path.join(OUT, "gbejna_v6.png"))
    gb.save(os.path.join(MOD_ITEMS, "gbejna.png"))
    v3.append(("gbejna_v6", gb))
    preview(v3).save(os.path.join(OUT, "preview.png"))
    print("wrote", len(images), "round-1 candidates, v2 and v3 pieces (v3 into the mod) and preview.png")


if __name__ == "__main__":
    main()
