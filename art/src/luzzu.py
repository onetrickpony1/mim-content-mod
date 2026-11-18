"""The luzzu: the Maltese fishing boat, as a rideable boat with its own model (owner, 2026-11-17).

What makes a luzzu (from the reference photos in art/references/luzzu_refonly/, web photos kept for reference
only, out of git; listed in list.tsv there):
- a double-ended carvel hull (smooth, flush planking), pointed at both bow and stern, with a sweeping sheer:
  the gunwale is low amidships and rises towards both ends, most steeply near them;
- a tall upright stem post at the bow and a stern post, standing well clear of the sheer and raked a little
  outboard, the bow post the taller;
- the Eye of Osiris (Horus) painted or carved on both sides of the bow, high on the bow panel;
- bright banded paint along the sheer over a blue hull: a capping, a band on the rubbing strake, then a band
  that widens into a big V at the bow; a white boot-top and a dark bottom at the waterline, which is level;
- a wooden gunwale rail and rubbing strakes standing proud of the planking;
- an open boat with small decks at the ends, an inboard engine and long oars on thole pins: long, thin shafts
  with narrow blades, painted like the boat's trim.
Proportions from the photos and boat listings: length to beam about 2.7 to 3 to 1 (7.7 m x 2.8 m, 8.5 m x 3 m).

Colour schemes (the owner: luzzijiet come in several orders of colours, the oars in the trim colour):
- green: yellow capping, red strake band, yellow V, blue hull, green posts, deck and oars (photos 05, 11, 13, 16);
- red: blue at the top, a red strake band, yellow V, blue hull, red bottom, red posts, blue oars (photos 02, 03);
- brown: yellow capping, a broad varnished-wood band, yellow V, blue hull, wooden posts and oars
  (photos 04, 15, 17, 19, 26).

Model (in pixels, 1/16 block): 46 long at the hull, about 50 over the raked posts, 18 wide at the widest, 8 high
amidships with the sheer rising about 6 px to the ends, both ends narrowing to a point (a pointed lozenge from
above, a sharp cutwater under each post); the posts carry the height (bow post to 26, stern
post to 22). The vanilla boat is 32 x 20 x 9; the hitbox stays vanilla, the seats rise 2 px with the hull
(LuzzuBoat). Each half of the hull is a chain of
segments, each tilted a little more than the one inside it, so the sheer and the bottom curve up smoothly.
The boat floats with the water about 5.85 px above its base (vanilla buoyancy). A luzzu barely sinks into the
water, so the hull rides 2 px higher than a vanilla boat's (bottom at 4 px, keel at 3, sheer at 12): only the
bottom paint and keel are under water, the white boot-top (6 to 7 px) and all the bands above it.

The script writes, so the model and its textures can never drift apart:
- the entity textures textures/entity/boat/luzzu*.png, one per colour scheme (each face is painted from where
  its pixels sit on the boat, so the bands run on across the boxes);
- the model code mod/src/main/java/com/maltaminecraft/mimcontent/client/LuzzuModel.java;
- the item icons textures/item/luzzu*.png (a three-quarter view, bow to the upper right, like the vanilla boats).
Run: art/.venv/bin/python art/src/luzzu.py
"""
import math
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "LuzzuModel.java")

# colours measured from the photos (sunlit paint), kept a little flat because the game shades the faces itself
BLUE = (30, 118, 188)
YELLOW = (232, 182, 48)
RED = (176, 48, 38)
BRIGHT_RED = (196, 44, 36)
WHITE = (226, 224, 212)
BOTTOM = (112, 50, 40)        # red-brown antifouling
DARK_BOTTOM = (78, 50, 44)
GREEN = (38, 138, 78)
WOOD = (178, 118, 58)         # varnished wood, the lighter ochre of photo 17
FLOOR = (132, 96, 58)
INSIDE = (111, 135, 150)      # the inside of the hull (#6f8796)
EYE_D, EYE_K = (40, 34, 44), (28, 46, 92)

SCHEMES = {
    # name: capping, strake band (and its rows), V, hull, bottom, posts, oars, deck
    "luzzu": dict(cap=YELLOW, band=RED, band_rows=1, vee=YELLOW, hull=BLUE, bottom=BOTTOM, post=GREEN, oar=GREEN, deck=GREEN),
    "luzzu_red": dict(cap=BLUE, band=BRIGHT_RED, band_rows=1, vee=YELLOW, hull=BLUE, bottom=BRIGHT_RED, post=BRIGHT_RED,
                      oar=BLUE, deck=BLUE, icon_inside=0.9),
    "luzzu_brown": dict(cap=YELLOW, band=WOOD, band_rows=2, vee=YELLOW, hull=BLUE, bottom=DARK_BOTTOM, post=WOOD, oar=WOOD,
                        deck=BLUE, icon_inside=0.45),
}

# the hull, in model space (x to the bow, y down, z across); boat height Y = 6 - y
LIFT = 2            # the hull rides this many px higher than a vanilla boat: a luzzu barely sinks into the water
KEEL_DEPTH = 4      # the keel reaches from the hull bottom (4 px up) to the boat's base, where it rests ashore
TOP = -4.0 - LIFT   # the sheer amidships, 12 px up (the bottom stays at 4 px: 3 px of blue topside amidships)
MID_HALF_LEN, MID_HALF, MID_H = 5, 9, 8
# segments from amidships to the bow (the stern mirrors them): (length, tilt in degrees, half-beam, height, open?)
SEGS = [
    (3, 0, 9, 8, True),     # as wide as amidships: the widest part carries fore and aft
    (2, 6, 8, 8, True),
    (3, 12, 6, 8, True),
    (5, 20, 5, 8, False),   # the bow panel, with the eye
    (2, 22, 3, 6, False),   # then narrowing to a point at the post: a sharp cutwater, not a transom; short and
    (2, 28, 2, 4, False),   # gently tilted, so no bottom corner reaches out past the post
    (1, 34, 1, 2, False),
]
WALL = 2
EYE_SEG = 3
WELL_V = 3   # the eye panel is open too: its V-stepped sides become walls and its bottom step the floor, so the
             # well runs on into the bow and stern (room for three aboard) while the outside stays the same
POSTS = {True: (12.0, 26), False: (-8.0, 22)}   # bow / stern: rake in degrees, height of the top (px up)
TIP_SEGS = 3                                       # the last segments, whose ends and undersides show head-on
OAR_POSE = (11.0, -6.5 - LIFT, 8.0)  # the thole pins: beside the helm, 6.5 px ahead of the rower's shoulders, on the
                                    # gunwale's outer edge (owner 2026-11-18; must match client/LuzzuOars.java)
WATER_Y, BOOT_Y = 6.0, 7.0   # bottom paint below 6 px (the water stands at 5.85), white boot-top from 6 to 7 px


def chain(bow):
    """The pivots and tilts of one half's segments: each pivots at its inboard top corner, which is where the
    previous one's top edge ends."""
    s = 1 if bow else -1
    x, y, out = s * MID_HALF_LEN, TOP, []
    for length, deg, half, h, open_ in SEGS:
        a = math.radians(deg)
        out.append(dict(pivot=(x, y), zrot=-s * a, length=length, half=half, h=h, open=open_, bow=bow))
        x, y = x + s * length * math.cos(a), y - length * math.sin(a)
    return out, (x, y)


def v_section(k, half, h):
    """The layers of a closed end segment, top down: (y from, y to, half-beam), narrowing in three steps so the
    end tapers from the gunwale to the keel head-on."""
    if k == EYE_SEG:
        layers = [(0, 4, half), (4, 6, half - 1), (6, h, half - 3)]
    else:
        layers = [(0, 2, half), (2, h - 1, half - 1), (h - 1, h, half - 2)]
    out = []
    for y0, y1, hb in layers:
        hb = max(1, hb)
        if y1 <= y0:
            continue
        if out and out[-1][2] == hb:
            out[-1] = (out[-1][0], y1, hb)
        else:
            out.append((y0, y1, hb))
    return out


def bilge_walls(x0, xs, half, h, zs, info):
    """One side wall of an open part with a bilge: the full half-beam down through the white boot-top (so the
    bands read unbroken in profile), then the bottom-paint rows step in: a row at half - 1, then the floor
    (half - 3) as the bottom row, over the keel."""
    out = []
    for y0, y1, outer_ in ((0, h - 2, half), (h - 2, h - 1, half - 1)):
        z0 = outer_ - WALL if zs > 0 else -outer_
        out.append(("wall", x0, y0, z0, xs, y1 - y0, WALL, dict(info, lower=y0 > 0)))
    return out


def deg_of(k):
    return SEGS[k][1]


def parts():
    """The model as named parts, each with its pose and cubes. A cube is (role, x, y, z, w, h, d, info)."""
    out = []
    mid = []
    m = MID_HALF_LEN
    for zs in (1, -1):
        mid.extend(bilge_walls(-m, 2 * m, MID_HALF, MID_H, zs, dict(open=True, seg=-1)))
        mid.append(("strake", -m, 1, MID_HALF if zs > 0 else -MID_HALF - 1, 2 * m, 1, 1, dict(seg=-1)))
    fb = max(1, MID_HALF - 3)
    mid.append(("floor", -m, MID_H - 1, -fb, 2 * m, 1, 2 * fb, dict(seg=-1)))
    # a deep keel, down to the boat's base: under water when afloat, and ashore the hull rests on it
    mid.append(("keel", -9, MID_H, -1, 18, KEEL_DEPTH, 2, dict(seg=-1)))
    out.append(dict(name="hull_mid", pivot=(0.0, TOP), zrot=0.0, cubes=mid))
    ends = {}
    for bow in (True, False):
        segs, end = chain(bow)
        ends[bow] = end
        for k, sg in enumerate(segs):
            L, half, h = sg["length"], sg["half"], sg["h"]
            lap = 1 if deg_of(k) else 0     # one pixel of overlap back into the previous segment, where it tilts
            x0 = -lap if bow else -L
            xs = L + lap
            info = dict(open=sg["open"] or k == WELL_V, seg=k, bow=bow)
            cubes = []
            if sg["open"]:
                for zs in (1, -1):
                    cubes.extend(bilge_walls(x0, xs, half, h, zs, info))
                fb = max(1, half - 3)
                cubes.append(("floor", x0, h - 1, -fb, xs, 1, 2 * fb, info))
                inner = ((2, h - 2, half - WALL), (h - 2, h - 1, half - 3))
            elif k == WELL_V:
                # the V section's steps as walls (the same outside), the bottom step as a raised floor
                layers = v_section(k, half, h)
                for y0, y1, hb in layers[:-1]:
                    for zs in (1, -1):
                        z0 = hb - WALL if zs > 0 else -hb
                        cubes.append(("wall", x0, y0, z0, xs, y1 - y0, WALL, dict(info, lower=y0 > 0)))
                y0, y1, hb = layers[-1]
                cubes.append(("deck", x0, y0, -hb, xs, y1 - y0, 2 * hb, dict(info, lower=True, well=True)))
                # the one pixel this part laps back into the last bilge part: there the bilge is a pixel wider
                # than this floor, so a floor that wide closes the corners beside it
                pw = SEGS[k - 1][2] - 3
                cubes.append(("deck", -lap if bow else 0, y0, -pw, lap, 1, 2 * pw, dict(info, lower=True, well=True)))
                inner = [(max(1, a), b, c - WALL) for a, b, c in layers[:-1]]   # from 1 px down: tucked under the end deck
            if (sg["open"] or k == WELL_V) and k + 1 < len(SEGS) and not (SEGS[k + 1][4] or k + 1 == WELL_V):
                # a bulkhead across the last pixel of the well, where the narrower V section of the closed end
                # begins: it closes the corners beside the floorboards and sits inside this part's hull. It fills
                # only the space between the inner faces of the walls, so none of its faces lies on an outer face
                # (two faces in one plane flicker)
                bx = L - 1 if bow else -L
                for y0, y1, hb in inner:
                    cubes.append(("bulkhead", bx, y0, -hb, 1, y1 - y0, 2 * hb, info))
            if not (sg["open"] or k == WELL_V):
                # a V section: the full half-beam at the top, narrower below, so head-on the end steps in to the keel
                for y0, y1, hb in v_section(k, half, h):
                    cubes.append(("deck", x0, y0, -hb, xs, y1 - y0, 2 * hb, dict(info, lower=y0 > 0)))
            if half > 3:
                sl = L - 1 if k == EYE_SEG else L   # stop short of the narrower tip, so no chip shows outside the hull
                sx = 0 if bow else -sl
                cubes.append(("strake", sx, 1, half, sl, 1, 1, info))
                cubes.append(("strake", sx, 1, -half - 1, sl, 1, 1, info))
            out.append(dict(name=("bow_" if bow else "stern_") + str(k + 1), pivot=sg["pivot"], zrot=sg["zrot"], cubes=cubes))
    # each post IS the stem: its outer face lines up with the outermost corner of the end boxes, and its foot
    # with the lowest corner within 3 px of the tip, so it runs down the cutwater
    for bow in (True, False):
        deg, top = POSTS[bow]
        pts = []
        for p in out:
            if not p["name"].startswith("bow_" if bow else "stern_"):
                continue
            ca, sa = math.cos(p["zrot"]), math.sin(p["zrot"])
            for role, cx, cy, cz, w, h, d, _ in p["cubes"]:
                for lx in (cx, cx + w):
                    for ly in (cy, cy + h):
                        pts.append((p["pivot"][0] + lx * ca - ly * sa, p["pivot"][1] + lx * sa + ly * ca))
        reach = max(abs(x) for x, _ in pts)
        ex = (reach - 1.0) * (1 if bow else -1)
        base = max(y for x, y in pts if abs(x) >= reach - 3)
        length = round((base - (6 - top)) / math.cos(math.radians(deg)))
        out.append(dict(name="stem_post" if bow else "stern_post", pivot=(ex, base), zrot=math.radians(deg),
                        cubes=[("post", -1, -length, -1, 2, length, 2, dict(bow=bow))]))
    return out


def water_patches():
    """Boxes that keep the sea out of the open hull (like vanilla's water patch): level, 6 to 9 px up, just above
    the water (5.85 px) and above the floorboards (5 px)."""
    out = [(-MID_HALF_LEN, MID_HALF_LEN, MID_HALF - WALL)]
    x = MID_HALF_LEN
    for length, deg, half, h, open_ in SEGS:
        if open_:   # (the well in the eye panel has its floor above the water: no patch, or it would cut the sea)
            out.append((x, x + length, half - WALL))
            out.append((-x - length, -x, half - WALL))
        x += length
    return out


def oar_cubes(side):
    """A luzzu oar: a long thin shaft and a long, narrow blade with a square end."""
    bx = -0.501 if side == "left" else -0.499
    return [("oar_shaft", -0.5, 0.0, -7.0, 1, 1, 23), ("oar_blade", bx, -1.0, 6.0, 1, 3, 11)]


# ---------------------------------------------------------------- paint

def hash01(x, y, seed):
    v = math.sin(x * 127.1 + y * 311.7 + seed * 74.7) * 43758.5453
    return v - math.floor(v)


def jitter(rgb, x, y, seed, amount=0.035):
    f = 1.0 + (hash01(x, y, seed) - 0.5) * 2 * amount
    return tuple(max(0, min(255, round(c * f))) for c in rgb)


def shade(rgb, f):
    return tuple(max(0, min(255, round(c * f))) for c in rgb)


def vee_rows(x):
    """Rows of the V band under the strake band: none amidships, widening towards the bow (less at the stern)."""
    reach = abs(x) - 9.0
    if reach <= 0:
        return 0
    return int(reach * (0.7 if x > 0 else 0.3))


EYE_TOP = 2   # the eye's top row on the bow panel, the same on every scheme: right under the band, all on the outer tier


def eye(lx, row):
    """The Eye of Osiris, 5 x 2 (owner 2026-11-18: sharper, smaller, less round): a sharp almond like the real
    eyes (photos 10, 16, 26), its dark brow sweeping back to a point at the stern (column 0), the white closed at
    both ends with the iris between. The whole eye lies on the outer tier of the bow panel (rows 2-3), so it reads as
    one eye from the front too (owner 2026-11-18: not on two levels); a row of the V's yellow under it frames it. On
    the brown boat the brow lies on the wood band's lower row, like real varnished luzzus (photos 15, 26)."""
    shape = ["DDDD.",
             "DWKWD",
             "YYYYY"]
    j, i = row - EYE_TOP, int(math.floor(lx))
    if 0 <= j < len(shape) and 0 <= i < 5:
        return {"D": EYE_D, "W": WHITE, "K": EYE_K, "Y": YELLOW}.get(shape[j][i])
    return None


def outer(sc, X, Y, row, lx, info):
    """The outside of the hull: bands that follow the sheer near the top, level bands at the waterline."""
    if row == 0:
        return sc["cap"]
    if info.get("bow") and info.get("seg") == EYE_SEG:
        e = eye(lx, row)   # (before the band: on the brown boat the brow lies on the wood band)
        if e:
            return e
    if row <= sc["band_rows"]:
        return sc["band"]
    vstart = sc["band_rows"] + 1
    if row < vstart + vee_rows(X):
        if Y >= BOOT_Y + 2:   # the V stops short, so at least two rows of blue stay above the boot-top
            return sc["vee"]
    if Y < WATER_Y:
        return sc["bottom"]
    if Y < BOOT_Y:
        return WHITE
    return sc["hull"]


def by_height(sc, Y):
    """Hull colours by height alone: bottom paint below the waterline, the white boot-top, then blue."""
    if Y < WATER_Y:
        return sc["bottom"]
    if Y < BOOT_Y:
        return WHITE
    return sc["hull"]


def inside(row):
    return shade(INSIDE, 0.86) if row % 2 == 1 else INSIDE   # plank seams


def paint(sc, role, face, X, Y, Z, row, lx, cube, info):
    _, x0, y0, z0, w, h, d, _ = cube
    if role == "keel":
        return sc["bottom"]
    if role == "bulkhead" and not (face in ("+x", "-x") and (face == "+x") == (info.get("bow") is True)):
        return shade(INSIDE, 1.12)   # the same even interior colour as the inward faces of the end
    if role == "deck" and info.get("well") and face == "top":
        return FLOOR if int(math.floor(Z)) % 3 else shade(FLOOR, 0.82)   # the floorboards run on into the ends
    if role == "post":
        return shade(sc["post"], 0.7) if face == "top" else sc["post"]
    if role == "strake":
        return sc["band"] if face not in ("top", "bottom") else shade(sc["band"], 0.73)
    bow = info.get("bow")
    tip = info.get("seg", -1) >= len(SEGS) - TIP_SEGS
    if role == "deck" and info.get("lower") and face == "top":
        return by_height(sc, Y)   # the ledge where the V section steps in
    if role == "wall" and info.get("lower") and face == "top":
        return INSIDE             # the bilge steps, seen from inside the boat
    if role in ("wall", "deck") and face == "bottom":
        return by_height(sc, Y)   # undersides of the steps: hull colours by height
    if tip and role == "deck":
        # head-on the tip shows its ends and undersides: hull colours by height, a narrow V under the post
        outward_end = face in ("+x", "-x") and (face == "+x") == (bow is True)
        if face == "bottom" or outward_end:
            return by_height(sc, Y)
        if face == "top":
            return sc["deck"]
    if face == "bottom":
        return sc["bottom"]
    # the end faces: those looking back amidships are inside the boat; those looking out are risers, one flat colour
    if face in ("+x", "-x"):
        inward = (face == "-x") == (bow is True) if bow is not None else False
        if inward:   # one even interior colour, lifted a little against the game's shading of these faces
            return sc["cap"] if row == 0 and role == "deck" and not info.get("lower") else shade(INSIDE, 1.12)
        if role == "floor":
            return shade(FLOOR, 0.8)
        # the bands run straight on across the joint, a little lighter to cancel the game's shading of end faces;
        # the top two rows are capping, so the seam at the top reads as one rail
        if row <= 1:
            return sc["cap"]
        return shade(outer(sc, X, Y, row, lx, dict(info, seg=-2)), 1.12)   # (the eye is on the sides only)
    if role == "floor":
        if face != "top":
            return shade(FLOOR, 0.8)
        return FLOOR if int(math.floor(Z)) % 3 else shade(FLOOR, 0.82)   # boards with seams
    if role == "deck":
        if face == "top":
            return sc["cap"] if abs(Z) > d / 2 - 1 else sc["deck"]
        return outer(sc, X, Y, row, lx, info)
    # wall
    if face == "top":
        return sc["cap"]
    outward = (face == "+z" and z0 >= 0) or (face == "-z" and z0 < 0)
    if not outward:
        return inside(row)
    return outer(sc, X, Y, row, lx, info)


def oar_paint(sc, role, face, i, j):
    if role == "oar_blade":
        return shade(sc["oar"], 1.1) if face in ("+x", "-x") else sc["oar"]
    return sc["oar"]


# ---------------------------------------------------------------- texture layout

def pack(sizes, width):
    """Shelf packing of (w, h) rectangles, tallest first; returns positions in input order and the height."""
    order = sorted(range(len(sizes)), key=lambda k: (-sizes[k][1], -sizes[k][0], k))
    pos, x, y, shelf = [None] * len(sizes), 0, 0, 0
    for k in order:
        w, h = sizes[k]
        if x + w > width:
            x, y, shelf = 0, y + shelf, 0
        pos[k] = (x, y)
        x += w
        shelf = max(shelf, h)
    return pos, y + shelf


def face_texels(u, v, w, h, d):
    """Each face of a cube as (face, rect, texel -> local model coords relative to the cube's min corner),
    following Minecraft's cube UV layout (ModelPart.Cube). Model y points down; "top" is the face at min y."""
    return [
        ("top", (u + d, v, w, d), lambda i, j: (i + .5, 0.01, d - j - .5)),
        ("bottom", (u + d + w, v, w, d), lambda i, j: (i + .5, h - 0.01, d - j - .5)),
        ("-x", (u, v + d, d, h), lambda i, j: (0.01, j + .5, d - i - .5)),
        ("-z", (u + d, v + d, w, h), lambda i, j: (i + .5, j + .5, 0.01)),
        ("+x", (u + d + w, v + d, d, h), lambda i, j: (w - 0.01, j + .5, i + .5)),
        ("+z", (u + d + w + d, v + d, w, h), lambda i, j: (w - i - .5, j + .5, d - 0.01)),
    ]


def layout():
    ps = parts()
    cubes = [(pi, c) for pi, p in enumerate(ps) for c in p["cubes"]]
    oars = [(side, c) for side in ("left", "right") for c in oar_cubes(side)]
    sizes = [(2 * c[6] + 2 * c[4], c[6] + c[5]) for _, c in cubes] + [(2 * c[6] + 2 * c[4], c[6] + c[5]) for _, c in oars]
    pos, height = pack(sizes, 128)
    return ps, cubes, oars, pos, (64 if height <= 64 else 128)


def build_texture(sc, ps, cubes, oars, pos, tex_h):
    img = np.zeros((tex_h, 128, 4), dtype=np.uint8)
    for k, (pi, cube) in enumerate(cubes):
        p = ps[pi]
        role, cx, cy, cz, w, h, d, info = cube
        u, v = pos[k]
        ca, sa = math.cos(p["zrot"]), math.sin(p["zrot"])
        px, py = p["pivot"]
        for face, (fu, fv, fw, fh), m in face_texels(u, v, int(w), int(h), int(d)):
            for j in range(fh):
                for i in range(fw):
                    lx, ly, lz = m(i, j)
                    x, y, z = cx + lx, cy + ly, cz + lz          # in the part's own space
                    mx, my = px + x * ca - y * sa, py + x * sa + y * ca
                    X, Y, Z = mx, 6 - my, z
                    row = int(math.floor(y)) if face not in ("top", "bottom") else 0
                    along = x if info.get("bow", True) else -x
                    rgb = paint(sc, role, face, X, Y, Z, row, along, cube, info)
                    img[fv + j, fu + i] = (*jitter(rgb, fu + i, fv + j, 7), 255)
    for k, (side, (role, x, y, z, w, h, d)) in enumerate(oars):
        u, v = pos[len(cubes) + k]
        for face, (fu, fv, fw, fh), _m in face_texels(u, v, w, h, d):
            for j in range(fh):
                for i in range(fw):
                    img[fv + j, fu + i] = (*jitter(oar_paint(sc, role, face, i, j), fu + i, fv + j, 3), 255)
    return img


# ---------------------------------------------------------------- Java model

def f(v):
    return f"{round(float(v), 6)!r}F"


def java(ps, cubes, oars, pos, tex_h):
    blocks = []
    k = 0
    for pi, p in enumerate(ps):
        lines = []
        for cube in p["cubes"]:
            role, x, y, z, w, h, d, _ = cube
            u, v = pos[k]
            k += 1
            lines.append(f".texOffs({u}, {v}).addBox({f(x)}, {f(y)}, {f(z)}, {f(w)}, {f(h)}, {f(d)}) // {role}")
        px, py = p["pivot"]
        pose = (f"PartPose.offsetAndRotation({f(px)}, {f(py)}, 0.0F, 0.0F, 0.0F, {f(p['zrot'])})"
                if p["zrot"] else f"PartPose.offset({f(px)}, {f(py)}, 0.0F)")
        blocks.append(f'        root.addOrReplaceChild("{p["name"]}", CubeListBuilder.create()\n            '
                      + "\n            ".join(lines) + f"\n            , {pose});")
    for side in ("left", "right"):
        lines = []
        for n, (s, (role, x, y, z, w, h, d)) in enumerate(oars):
            if s == side:
                u, v = pos[len(cubes) + n]
                lines.append(f".texOffs({u}, {v}).addBox({f(x)}, {f(y)}, {f(z)}, {f(w)}, {f(h)}, {f(d)})")
        ox, oy, oz = OAR_POSE
        if side == "left":
            pose = f"PartPose.offsetAndRotation({f(ox)}, {f(oy)}, {f(oz)}, 0.0F, 0.0F, (float) (Math.PI / 16))"
        else:
            pose = f"PartPose.offsetAndRotation({f(ox)}, {f(oy)}, {f(-oz)}, 0.0F, (float) Math.PI, (float) (Math.PI / 16))"
        blocks.append(f'        root.addOrReplaceChild("{side}_paddle", CubeListBuilder.create()\n            '
                      + "\n            ".join(lines) + f",\n            {pose});")
    patch = [f"            .addBox({f(x0)}, -3.0F, {f(-hz)}, {f(x1 - x0)}, 3.0F, {f(2 * hz)})" for x0, x1, hz in water_patches()]
    return f"""package com.maltaminecraft.mimcontent.client;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.client.model.object.boat.AbstractBoatModel;

/**
 * The luzzu's model: a double-ended hull whose halves are chains of segments, each tilted a little more than the
 * one inside it, so the sheer sweeps up to raked stem and stern posts; rubbing strakes and two long oars (rowed
 * like a vanilla boat's paddles). Shared by every colour scheme. Made by art/src/luzzu.py together with its
 * textures (textures/entity/boat/luzzu*.png); change the script and run it again rather than editing this file.
 */
public class LuzzuModel extends AbstractBoatModel {{
    public LuzzuModel(ModelPart root) {{
        super(root);
    }}

    public static LayerDefinition createBodyLayer() {{
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
{chr(10).join(blocks)}
        return LayerDefinition.create(mesh, 128, {tex_h});
    }}

    /** Keeps the sea from showing inside the open hull, like vanilla's boat water patch. */
    public static LayerDefinition createWaterPatch() {{
        MeshDefinition mesh = new MeshDefinition();
        mesh.getRoot().addOrReplaceChild("water_patch", CubeListBuilder.create()
{chr(10).join(patch)}
            , PartPose.ZERO);
        return LayerDefinition.create(mesh, 0, 0);
    }}
}}
"""


# ---------------------------------------------------------------- item icons

OUTLINE = (34, 30, 44)


def icon_diag(sc):
    """The item icon (installed; the owner picked it 2026-11-17), in the vanilla boat items' pose and size (14 px wide): a long hull running diagonally from
    the stern at the lower left to the bow at the upper right, seen a little from above. The sheer dips amidships
    and the keel is one convex curve, lowest amidships; between the far and near gunwales a dark band of the
    inside, as on the vanilla boats. Down the near side four clean bands: the capping, the accent band, the blue
    hull (with the V at the bow), then a 1 px white boot-top and a 1 px bottom. Upright posts 3 px tall at both
    ends, a 2 px eye on the bow, one oar in a clean diagonal with its blade to the lower right, and a 1 px dark
    outline, darker at the lower right."""
    W = 16
    c = np.zeros((W, W, 4), dtype=np.uint8)

    def put(x, y, rgb):
        if 0 <= x < W and 0 <= y < W:
            c[y, x] = (*rgb, 255)

    xs = range(1, 15)
    near, keel, inner = {}, {}, {}
    for x in xs:
        t = (x - 7.5) / 6.5
        slope = -0.42 * (x - 7.5)                     # the diagonal: the bow higher on screen
        near[x] = int(round(8.0 + slope - 2.2 * t ** 4 - 0.6 * t * t))   # the sheer, dipping amidships
        keel[x] = int(round(8.0 + slope + 5.6 - 3.6 * t ** 4))           # the keel, one convex curve
        inner[x] = 2 if abs(t) < 0.62 else (1 if abs(t) < 0.85 else 0)
    vee = {11: 1, 12: 1, 13: 2, 14: 1}
    for x in xs:
        yn, yk = near[x], keel[x]
        if inner[x]:
            put(x, yn - inner[x] - 1, shade(sc["cap"], 0.85))   # the far gunwale
            for k in range(1, inner[x] + 1):
                put(x, yn - k, shade(FLOOR, sc.get("icon_inside", 0.62)))   # the inside, one flat dark band
        put(x, yn, sc["cap"])
        rows = [sc["band"]] * sc["band_rows"] + [sc["vee"]] * vee.get(x, 0)
        n = yk - yn                                             # rows below the capping
        body = rows[:max(0, n - 2)]
        body += [sc["hull"]] * max(0, n - 2 - len(body))
        for r, col in enumerate(body + [WHITE, sc["bottom"]], 1):
            put(x, yn + r, col)
    for y in range(near[1] - 3, near[1]):        # the posts, upright, 3 px
        put(1, y, sc["post"])
    for y in range(near[14] - 3, near[14]):
        put(14, y, sc["post"])
    put(12, near[12] + 2, WHITE)                 # the eye
    put(13, near[13] + 2, EYE_D)
    for k in range(7):                           # the oar, one diagonal, blade to the lower right
        put(6 + k, near[6] - 1 + k, sc["oar"])
    bx, by = 6 + 6, near[6] - 1 + 6
    for dx, dy in ((1, 0), (0, 1), (1, 1)):
        put(bx + dx, by + dy, shade(sc["oar"], 0.85))
    alpha = c[:, :, 3] > 0
    out = c.copy()
    for y in range(W):
        for x in range(W):
            if not alpha[y, x] and any(0 <= x + dx < W and 0 <= y + dy < W and alpha[y + dy, x + dx]
                                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                lower_right = any(0 <= x + dx < W and 0 <= y + dy < W and alpha[y + dy, x + dx] for dx, dy in ((-1, 0), (0, -1)))
                out[y, x] = (*(shade(OUTLINE, 0.6) if lower_right else OUTLINE), 255)
    return out


def outline(c):
    """A 1 px dark outline round the shape, darker at the lower right."""
    W = c.shape[0]
    alpha = c[:, :, 3] > 0
    out = c.copy()
    for y in range(W):
        for x in range(W):
            if not alpha[y, x] and any(0 <= x + dx < W and 0 <= y + dy < W and alpha[y + dy, x + dx]
                                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                lower_right = any(0 <= x + dx < W and 0 <= y + dy < W and alpha[y + dy, x + dx] for dx, dy in ((-1, 0), (0, -1)))
                out[y, x] = (*(shade(OUTLINE, 0.6) if lower_right else OUTLINE), 255)
    return out


def icon(sc):
    """A candidate item icon (not installed): the luzzu in profile, bow to the right, long and low. A hull 14 px long and 6 deep
    amidships with a flat convex keel; the sheer rises 2 px to each end, where the posts stand (the bow's
    taller); the top rows are empty apart from the posts. Three bands: the capping and accent band, the blue
    topside, the white boot-top over the dark bottom; a 2 px eye at the bow; one oar slanting behind the hull in
    the accent colour; a 1 px dark outline."""
    W = 16
    c = np.zeros((W, W, 4), dtype=np.uint8)

    def put(x, y, rgb):
        if 0 <= x < W and 0 <= y < W:
            c[y, x] = (*rgb, 255)

    for k in range(12):                          # the oar, behind the hull: drawn first; shaft, then the blade
        put(3 + k, 5 + int(round(k * 0.75)), sc["oar"])
    for x, y in ((15, 14), (15, 13), (14, 14)):
        put(x, y, shade(sc["oar"], 0.85))
    sheer = {1: 7, 2: 8, 3: 8, 4: 9, 5: 9, 6: 9, 7: 9, 8: 9, 9: 9, 10: 9, 11: 9, 12: 8, 13: 8, 14: 7}
    keel = {1: 9, 2: 11, 3: 12, 4: 13, 5: 13, 6: 13, 7: 13, 8: 13, 9: 13, 10: 13, 11: 13, 12: 12, 13: 11, 14: 9}
    for x in range(1, 15):
        rows = [sc["cap"]] + [sc["band"]] * sc["band_rows"]
        n = keel[x] - sheer[x] + 1
        body = rows[:max(1, n - 2)]
        body += [sc["hull"]] * max(0, n - 2 - len(body))
        body += [WHITE, sc["bottom"]][-(n - len(body)):] if n > len(body) else []
        for r, col in enumerate(body):
            put(x, sheer[x] + r, col)
    for y in range(4, 7):                        # the stem post, a short spike, taller
        put(14, y, sc["post"])
    for y in range(5, 7):                        # the stern post
        put(1, y, sc["post"])
    put(12, 9, WHITE)                            # the eye, on the band below the capping: light, then dark forward
    put(13, 9, EYE_D)
    return outline(c)


def seam_check(step=0.125, eps=0.005):
    """Fill the model's cubes into a fine grid and flood the air inside the hull from just above the floorboards
    amidships, kept below 9 px up (under every gunwale). If that air reaches past the beam or below the hull,
    there is a hole through which the sea or the sand shows. Returns the way out of the hull, or None."""
    xs = np.arange(-32, 32, step)
    ys = np.arange(TOP - 2, 6.0, step)   # model y: down is +, the boat's base is at 6
    zs = np.arange(-11, 11, step)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    occ = np.zeros(X.shape, bool)
    for p in parts():
        c, s = math.cos(p["zrot"]), math.sin(p["zrot"])
        dx, dy = X - p["pivot"][0], Y - p["pivot"][1]
        lx, ly = dx * c + dy * s, -dx * s + dy * c
        for _, cx, cy, cz, w, h, d, _ in p["cubes"]:
            occ |= ((lx >= cx - eps) & (lx <= cx + w + eps) & (ly >= cy - eps) & (ly <= cy + h + eps)
                    & (Z >= cz - eps) & (Z <= cz + d + eps))
    free = ~occ & (Y > -3.0)
    seed = (np.abs(xs).argmin(), np.abs(ys - 0.5).argmin(), np.abs(zs).argmin())
    dist = np.full(free.shape, -1, np.int32)
    dist[seed] = 0
    reach, g = dist >= 0, 0
    while True:
        g += 1
        n = reach.copy()
        n[1:] |= reach[:-1]; n[:-1] |= reach[1:]
        n[:, 1:] |= reach[:, :-1]; n[:, :-1] |= reach[:, 1:]
        n[:, :, 1:] |= reach[:, :, :-1]; n[:, :, :-1] |= reach[:, :, 1:]
        n &= free
        new = n & ~reach
        if not new.any():
            break
        dist[new] = g
        reach = n
    leak = reach & ((np.abs(Z) > 10) | (Y > 2.2) | (np.abs(X) > 30))
    if not leak.any():
        return None
    i = np.unravel_index(np.where(leak, dist, 1 << 30).argmin(), dist.shape)
    path = [i]
    while dist[i] > 0:   # walk back to the seed, to say where the air leaves
        for a in range(3):
            j = next((j for j in (i[:a] + (i[a] + e,) + i[a + 1:] for e in (-1, 1))
                      if 0 <= j[a] < dist.shape[a] and dist[j] == dist[i] - 1), None)
            if j:
                i = j
                break
        path.append(i)
    return [(float(xs[a]), float(6 - ys[b]), float(zs[c])) for a, b, c in path[::-1]]


def main():
    way_out = seam_check()
    if way_out:
        sys.exit("the hull has a hole: from amidships the air gets out by " +
                 ", ".join("x %.1f height %.1f z %.1f" % p for p in way_out[-12::3]))
    print("hull sealed: no gap from inside the boat to the outside")
    ps, cubes, oars, pos, tex_h = layout()
    for name, sc in SCHEMES.items():
        p = os.path.join(RES, "textures", "entity", "boat", name + ".png")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        Image.fromarray(build_texture(sc, ps, cubes, oars, pos, tex_h), "RGBA").save(p, optimize=False)
        print("wrote", os.path.relpath(p, ROOT))
        p = os.path.join(RES, "textures", "item", name + ".png")
        Image.fromarray(icon_diag(sc), "RGBA").save(p, optimize=False)   # the diagonal pose, picked by the owner
        print("wrote", os.path.relpath(p, ROOT))
        p = os.path.join(ROOT, "art", "candidates", "luzzu_icons_profile", name + "_profile.png")   # the profile pose, not picked
        os.makedirs(os.path.dirname(p), exist_ok=True)
        Image.fromarray(icon(sc), "RGBA").save(p, optimize=False)
    os.makedirs(os.path.dirname(JAVA), exist_ok=True)
    with open(JAVA, "w", encoding="utf-8") as fh:
        fh.write(java(ps, cubes, oars, pos, tex_h))
    print("wrote", os.path.relpath(JAVA, ROOT), f"({len(cubes)} hull cubes, texture 128x{tex_h})")


if __name__ == "__main__":
    main()
