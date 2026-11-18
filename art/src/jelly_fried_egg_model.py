"""The fried-egg jellyfish (Cotylorhiza tuberculata) as a mob: its 3D model and its texture.

Drawn from the reference photos in art/references/jelly_fried_egg_refonly/ (list.tsv): fe01-fe03 and fe20 (side
views in open water) for the proportions, fe12 (from above) for the yolk's size, fe26, fe27 and fe35 (clear water,
close) and fe13-fe18 (Basel Zoo, every angle) for the colours and the knobs. What makes it the fried egg:
  - a wide, flat, round bell, 15 px across (0.94 blocks), pale butter-yellow, 2 px thick at the edge with a margin
    that turns down and is ribbed (the real bell's lappets), a raised ring toward the middle and a shallow dip;
  - rising out of the dip a low, rounded dome, 7 px across, in orange-yellow: the "egg yolk", lit on top;
  - under the bell a short, wide drum of oral arms in a deeper ochre, as wide as the bell with its knobs and about a
    third as tall, flat underneath: white button knobs mostly along its upper edge, purple-blue ones in a band along
    its lower edge and under it, the middle left yellow with small painted speckles of both;
  - six short filaments under the drum, 1-2 px, each ending in a purple-blue knob (the real animal's short
    appendages; it has no long trailing tentacles). They are the tentacle_N parts and sway.
The whole model is 13 px tall, its bottom at y 24 (the box's bottom, the JellyfishModel contract).
It is round and symmetrical: no front, no eyes, no face. The knobs are scattered by a fixed hash, in bands
but mixed, so they never line up like eyes or teeth.

Each round layer is built of 1 px wide strips along x, each as deep (z) as the circle at that column, so the disc is
round without any boxes overlapping. The texture is drawn translucent by the game, so every face that lies against
another box is left clear (alpha 0) and the inside never shows through. Shading: the light comes from above; the
yolk's cap is lightest, the bell darkens toward the margin, every side face darkens downward, the undersides are the
darkest and most see-through.

Model contract (the builder's JellyfishModel): a root child "bell" (the base class pulses it), "oral_arms" a child of
"bell", "tentacle_0".. "tentacle_5" children of "bell" (the base class sways them).

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/jelly/FriedEggJellyfishModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/jellyfish/fried_egg_jellyfish.png
With --renders DIR it also writes offline renders (side, three-quarter, above, below) there.

Run:  art/.venv/bin/python art/src/jelly_fried_egg_model.py [--renders DIR]
"""
import colorsys
import hashlib
import math
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA_DIR = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "jelly")
JAVA = os.path.join(JAVA_DIR, "FriedEggJellyfishModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "jellyfish", "fried_egg_jellyfish.png")


def hexc(s, a=255):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), a)


def lift(c, v=1.12, s=1.05):
    """A step lighter for the water (brightness x1.12, saturation x1.05, hue kept); alpha kept."""
    h, sat, val = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, min(1.0, sat * s), min(1.0, val * v))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), c[3])


def hash01(*vals):
    h = hashlib.md5(repr(vals).encode()).digest()
    return h[0] / 255.0


# Colours picked from the photos (fe26, fe27, fe35, fe13-fe18), lifted a step for the water.
# Bell, cream-yellow, light to dark; the margin paler and more see-through.
BELL = [lift(hexc(c)) for c in ("#f4e49a", "#ecd884", "#e2ca70", "#d4b860", "#c4a450")]
MARGIN = [lift(hexc(c)) for c in ("#f4e6a4", "#e6d286", "#d2ba6c")]
# The yolk, orange-yellow, light to dark.
YOLK = [lift(hexc(c)) for c in ("#f8c46a", "#f0a848", "#e4923a", "#d07c30", "#b8682a")]
# The underside of the bell: pale, see-through.
UNDER = [lift(hexc(c)) for c in ("#e8d488", "#d8c070", "#c4a85c")]
# The neck of pale arm bases.
NECK = [lift(hexc(c)) for c in ("#ecdc98", "#dcc87c", "#c8b064")]
# The oral arm mass: ochre-yellow, light to dark.
MASS = [lift(hexc(c)) for c in ("#e2ac42", "#d69c36", "#ca8c30", "#b67a2a", "#a26c26")]
# Knobs: purple-blue and white, light to dark.
PURPLE = [lift(hexc(c)) for c in ("#8a74d0", "#6a54b4", "#54409a", "#3e3080")]
WHITE = [lift(hexc(c)) for c in ("#fbf8ee", "#ece6d6", "#d6cfbc")]
CLEAR = (0, 0, 0, 0)

ALPHA = {"margin": 212, "rim": 232, "shoulder": 238, "dip": 238, "yolk": 255, "cap": 255, "under": 215, "neck": 232,
         "mass": 255, "knob": 255, "tent": 205}


def with_alpha(c, a):
    return (c[0], c[1], c[2], a)


# --- the model -------------------------------------------------------------------------------------------------------
BELL_Y = 16.0      # the bell's pivot (its underside, in the middle), in model pixels; y is down
# Parts: name -> (parent, pivot relative to the parent). Nothing is turned at rest.
PARTS = {"bell": (None, (0.0, BELL_Y, 0.0)), "oral_arms": ("bell", (0.0, 0.0, 0.0))}

# Round layers: (kind, part, radius, y0, y1) relative to the bell's pivot (negative is up).
LAYERS = [
    ("rim", "bell", 7.5, -2, 0),        # the bell, 15 across, 2 thick at the edge
    ("skirt", "bell", 7.5, 0, 1, 6.5),  # its margin turning down: a ring 1 px wide round the edge
    ("shoulder", "bell", 5.5, -3, -2, 4.5),  # a raised ring: the bell thickens toward the middle ...
    ("dip", "bell", 4.5, -3, -2, 3.5),  # ... and dips a little round the yolk
    ("yolk", "bell", 3.5, -4, -2),      # the yolk: a low dome, 7 across, rising out of the dip ...
    ("cap", "bell", 2.5, -5, -4),       # ... with a rounded top 5 across
    ("neck", "oral_arms", 4.5, 0, 1),   # pale arm bases under the bell
    ("mass", "oral_arms", 6.5, 1, 5),   # the oral arm mass: a short, wide drum, as wide as the bell with its knobs ...
    ("mass", "oral_arms", 5.5, 5, 6),   # ... with a flat, rounded-off bottom
]


def column_depth(r, xc):
    """The odd depth (z) of a circle of radius r at the column centred on xc."""
    if abs(xc) >= r:
        return 0
    half = math.sqrt(r * r - xc * xc)
    best = None
    for d in range(1, 64, 2):
        if best is None or abs(d - 2 * half) < abs(best - 2 * half) - 1e-9:
            best = d
    return best


def layer_boxes():
    out = []
    for li, layer in enumerate(LAYERS):
        kind, part, r, y0, y1 = layer[:5]
        rin = layer[5] if len(layer) > 5 else 0.0      # a ring: hollow inside this radius
        n = (column_depth(r, 0) - 1) // 2
        for xc in range(-n, n + 1):
            d = column_depth(r, xc)
            if d <= 0:
                continue
            din = column_depth(rin, xc) if rin else 0
            base = "%s%d_%d" % (kind, li, xc + n)
            if din <= 0:
                out.append((base, kind, part, (xc - 0.5, y0, -d / 2.0), (1, y1 - y0, d)))
            elif d > din:
                k = (d - din) // 2
                out.append((base + "n", kind, part, (xc - 0.5, y0, -d / 2.0), (1, y1 - y0, k)))
                out.append((base + "s", kind, part, (xc - 0.5, y0, din / 2.0), (1, y1 - y0, k)))
    return out


def mass_profile():
    """Map column xc -> list of (y0, y1, half-depth) of the mass layers, for placing knobs."""
    prof = {}
    for kind, part, r, y0, y1 in (l[:5] for l in LAYERS):
        if kind != "mass":
            continue
        n = (column_depth(r, 0) - 1) // 2
        for xc in range(-n, n + 1):
            prof.setdefault(xc, []).append((y0, y1, column_depth(r, xc) / 2.0))
    return prof


# Knob cubes by row of the drum (y below the bell): white ones along the upper edge, purple-blue ones in a band along
# the lower edge, the middle left yellow (fe20, fe35).
KNOB_CHANCE = {1: 0.12, 2: 0.16, 3: 0.05, 4: 0.1, 5: 0.22}


def KNOB_KIND(y, *at):
    """White along the upper rows (one in five purple, so they never line up like teeth), purple below."""
    if y <= 2:
        return "purple" if hash01("kk", y, *at) < 0.2 else "white"
    return "purple"


def knob_boxes():
    """Small button knobs standing out of the mass by 1 px, scattered (by a fixed hash) on its sides and under it;
    about 3 in 5 purple-blue, the rest white."""
    out = []
    prof = mass_profile()
    k = 0
    for xc in sorted(prof):
        for y0, y1, hd in prof[xc]:
            for y in range(y0, y1):
                for sgn in (-1, 1):                       # north (-z) and south (+z) faces of the column
                    if hash01("kz", xc, y, sgn) < KNOB_CHANCE.get(y, 0.0):
                        z0 = sgn * hd if sgn > 0 else -hd - 1
                        out.append(("knob%d" % k, KNOB_KIND(y, xc, sgn),
                                    "oral_arms", (xc - 0.5, y, z0), (1, 1, 1)))
                        k += 1
    # the two end columns: knobs on their west / east faces
    ends = (min(prof), max(prof))
    for xc in ends:
        sgn = -1 if xc < 0 else 1
        for y0, y1, hd in prof[xc]:
            for y in range(y0, y1):
                for zc in range(int(-hd + 0.5), int(hd - 0.5) + 1):
                    if hash01("kx", xc, y, zc) < KNOB_CHANCE.get(y, 0.0):
                        x0 = xc + 0.5 if sgn > 0 else xc - 1.5
                        out.append(("knob%d" % k, KNOB_KIND(y, xc, zc),
                                    "oral_arms", (x0, y, zc - 0.5), (1, 1, 1)))
                        k += 1
    return out


# Short filaments under the mass: (x centre, z centre, length); each is a tentacle_N, pivoted at its top.
TENTACLES = [(-2, -1, 2), (2, 1, 2), (-1, 3, 1), (1, -3, 1), (-4, 1, 1), (4, -1, 1)]


def tentacle_top(xc, zc):
    """The y (relative to the bell) of the bottom of the mass at that cell."""
    bottom = None
    for kind, part, r, y0, y1 in (l[:5] for l in LAYERS):
        if kind == "mass" and abs(xc) < r and abs(zc) <= column_depth(r, xc) / 2.0 - 0.5:
            bottom = y1 if bottom is None else max(bottom, y1)
    return bottom


def all_boxes():
    """Every box as (name, kind, part, origin relative to the part's pivot, size); parts' pivots in PART_PIVOTS."""
    boxes = []
    for name, kind, part, (x0, y0, z0), size in layer_boxes():
        boxes.append((name, kind, part, (x0, y0, z0), size))
    knobs = knob_boxes()
    tent_cells = set()
    for i, (xc, zc, ln) in enumerate(TENTACLES):
        top = tentacle_top(xc, zc)
        PARTS["tentacle_%d" % i] = ("bell", (float(xc), float(top), float(zc)))
        boxes.append(("tent%d" % i, "tent", "tentacle_%d" % i, (-0.5, 0.0, -0.5), (1, ln, 1)))
        tent_cells.add((xc, zc))
    # knobs hanging under the mass, away from the filaments
    for xc in range(-5, 6):
        for zc in range(-5, 6):
            top = tentacle_top(xc, zc)
            if top is None or (xc, zc) in tent_cells:
                continue
            near = any(abs(xc - a) <= 1 and abs(zc - b) <= 1 for a, b in tent_cells)
            edge = math.hypot(xc, zc) > 4.5
            if not near and hash01("kb", xc, zc) < (0.3 if edge else 0.0):
                knobs.append(("knob%d" % len(knobs), "purple",
                              "oral_arms", (xc - 0.5, top, zc - 0.5), (1, 1, 1)))
    # a knob that would overlap a filament or another knob is left out
    for kb in knobs:
        a0, a1 = abs_box(kb)
        clash = False
        for b in boxes:
            b0, b1 = abs_box(b)
            if all(min(a1[k], b1[k]) - max(a0[k], b0[k]) > 1e-6 for k in range(3)):
                clash = True
                break
        if not clash:
            boxes.append(kb)
    return boxes


def part_abs(part):
    parent, (x, y, z) = PARTS[part]
    if parent:
        px, py, pz = part_abs(parent)
        return x + px, y + py, z + pz
    return x, y, z


def abs_box(box):
    name, kind, part, (x0, y0, z0), (w, h, d) = box
    px, py, pz = part_abs(part)
    return (x0 + px, y0 + py, z0 + pz), (x0 + px + w, y0 + py + h, z0 + pz + d)


def check_boxes(boxes):
    """No two boxes may overlap (they would show through each other, the texture being translucent), and every box
    must touch another (every part touches the body). Returns a list of problems."""
    probs = []
    ab = [abs_box(b) for b in boxes]
    touches = [False] * len(boxes)
    for i in range(len(boxes)):
        a0, a1 = ab[i]
        for j in range(i + 1, len(boxes)):
            b0, b1 = ab[j]
            ov = [min(a1[k], b1[k]) - max(a0[k], b0[k]) for k in range(3)]
            if all(o > 1e-6 for o in ov):
                probs.append(("overlap", boxes[i][0], boxes[j][0]))
            elif all(o > -1e-6 for o in ov) and sum(1 for o in ov if o > 1e-6) == 2:
                touches[i] = touches[j] = True
    for i, t in enumerate(touches):
        if not t:
            probs.append(("floating", boxes[i][0]))
    return probs


# --- colour ----------------------------------------------------------------------------------------------------------
def ramp(lst, t):
    """Pick from a light-to-dark list by t in 0..1."""
    t = min(0.999, max(0.0, t))
    return lst[int(t * len(lst))]


def mixed(lst, t, x, y, z, salt, spread=0.18):
    """A ramp pick with a little fixed jitter, so a face is mixed rather than flat (4-6 tones)."""
    return ramp(lst, t + (hash01(salt, round(x * 2), round(y * 2), round(z * 2)) - 0.5) * spread)


def colour(kind, face, x, y, z, box):
    """The colour of a texel at the absolute point (x, y, z) on a face of a box of that kind."""
    rr = math.hypot(x, z)
    yb = y - BELL_Y                       # y relative to the bell's underside
    if kind == "rim":
        if face == "top":
            # cream, darkening to the margin; the outer ring is the pale see-through margin with ribs
            if rr > 6.6:
                rib = (int(math.floor((math.atan2(z, x) + math.pi) / (2 * math.pi) * 28)) % 2)
                return with_alpha(MARGIN[1 + rib], ALPHA["margin"])
            return with_alpha(mixed(BELL, 0.35 + (rr - 5.5) / 3.0, x, y, z, "rt"), ALPHA["rim"])
        if face == "bottom":
            rib = (int(math.floor((math.atan2(z, x) + math.pi) / (2 * math.pi) * 28)) % 2)
            if rr > 6.6:
                return with_alpha(MARGIN[2], ALPHA["margin"] - 15)
            return with_alpha(UNDER[1 + rib] if rr > 4.5 else UNDER[0], ALPHA["under"])
        # the rim's edge: ribbed lappets, light upper row, darker lower row
        rib = (int(math.floor((math.atan2(z, x) + math.pi) / (2 * math.pi) * 28)) % 2)
        return with_alpha(MARGIN[min(2, rib + (1 if yb > -1 else 0))], ALPHA["margin"])
    if kind == "skirt":
        # the down-turned margin: pale, see-through, ribbed like the rim's edge; darker underneath
        rib = (int(math.floor((math.atan2(z, x) + math.pi) / (2 * math.pi) * 28)) % 2)
        if face == "bottom":
            return with_alpha(MARGIN[2], ALPHA["margin"] - 15)
        if face == "top":
            return with_alpha(UNDER[1], ALPHA["under"])
        return with_alpha(MARGIN[1 + rib], ALPHA["margin"])
    if kind == "shoulder":
        if face == "top":
            return with_alpha(mixed(BELL, 0.05 + (rr - 4.5) / 4.0, x, y, z, "st"), ALPHA["shoulder"])
        return with_alpha(BELL[2], ALPHA["shoulder"])
    if kind == "dip":
        # the shallow dip round the yolk: a step darker than the raised ring outside it
        if face == "top":
            return with_alpha(mixed(BELL, 0.45, x, y, z, "dp", 0.15), ALPHA["dip"])
        return with_alpha(BELL[3], ALPHA["dip"])
    if kind == "yolk":
        if face == "top":
            return with_alpha(mixed(YOLK, 0.12 + (rr - 2.5) / 4.0 + (0.08 if x + z > 0 else 0), x, y, z, "yt"),
                              ALPHA["yolk"])
        # sides: lighter above, darker where it meets the bell; the light side a touch brighter
        t = 0.3 + (yb + 4) / 2.0 * 0.45 + (0.12 if x + z > 0 else 0)
        return with_alpha(mixed(YOLK, t, x, y, z, "ys", 0.12), ALPHA["yolk"])
    if kind == "cap":
        if face == "top":
            # a soft highlight toward the upper left (-x, -z), the rest the light yolk
            hl = (x + z) < -0.5 and rr < 2.0
            return with_alpha(YOLK[0] if hl or rr < 1.0 else YOLK[1], ALPHA["cap"])
        return with_alpha(mixed(YOLK, 0.25 + (0.15 if x + z > 0 else 0), x, y, z, "cs", 0.1), ALPHA["cap"])
    if kind == "neck":
        if face == "bottom":
            return with_alpha(NECK[2], ALPHA["neck"])
        return with_alpha(mixed(NECK, 0.3, x, y, z, "n", 0.4), ALPHA["neck"])
    if kind == "mass":
        # ochre, darker toward the bottom; painted knobs between the cube knobs (mixed purple and white clusters)
        # ochre, a light ramp from the top of the drum to its bottom; painted knobs: white along the upper rows,
        # purple-blue along the lower rows, the middle left yellow with light arm tips
        t = 0.05 + (yb - 1) / 5.0 * 0.55
        if face == "top":
            t = 0.05
        elif face == "bottom":
            t = 0.45                       # from below it still reads ochre
        base = mixed(MASS, t, x, y, z, "m", 0.3)
        hsh = hash01("paint", round(x * 2), round(y * 2), round(z * 2), face)
        row = int(math.floor(yb))
        if face == "bottom":
            if rr > 5.0 and hsh < 0.12:
                base = PURPLE[1]
            elif hsh < 0.25:
                base = MASS[1]
        elif face != "top":
            if hsh < (0.2 if row <= 2 else 0.1):
                base = WHITE[1]
            elif hsh < (0.24 if row <= 2 else 0.19):
                base = PURPLE[2]
            elif hsh < 0.3:
                base = MASS[0]             # light arm tips between the knobs
        return with_alpha(base, ALPHA["mass"])
    if kind in ("purple", "white"):
        lst = PURPLE if kind == "purple" else WHITE
        i = {"top": 0, "bottom": len(lst) - 1}.get(face, 1)
        if face not in ("top", "bottom") and y - BELL_Y >= 5:
            i = min(len(lst) - 1, i + 1)
        return with_alpha(lst[i], ALPHA["knob"])
    if kind == "tent":
        # see-through pale filament, its last pixel a purple-blue knob
        (_x0, _y0, _z0), (_x1, y1, _z1) = abs_box(box)
        if y > y1 - 1:
            return with_alpha(PURPLE[1] if face != "bottom" else PURPLE[2], 255)
        return with_alpha(NECK[1] if face != "bottom" else NECK[2], ALPHA["tent"])
    raise ValueError(kind)


# --- texture layout (the vanilla box UV layout) ----------------------------------------------------------------------
def face_texels(u, v, origin, size):
    """Every texel of every face of a box with texOffs (u, v): (face, tu, tv, x, y, z), the texel's centre in the
    box's own coordinates (ModelPart.Cube's layout, as in fish_awrata_model.face_texels)."""
    x0, y0, z0 = origin
    w, h, d = size
    x1, y1, z1 = x0 + w, y0 + h, z0 + d
    out = []
    for c in range(w):
        for r in range(d):
            out.append(("top", u + d + c, v + r, x0 + c + 0.5, y0, z1 - r - 0.5))
            out.append(("bottom", u + d + w + c, v + r, x0 + c + 0.5, y1, z1 - r - 0.5))
    for c in range(d):
        for r in range(h):
            out.append(("west", u + c, v + d + r, x0, y0 + r + 0.5, z1 - c - 0.5))
            out.append(("east", u + d + w + c, v + d + r, x1, y0 + r + 0.5, z0 + c + 0.5))
    for c in range(w):
        for r in range(h):
            out.append(("north", u + d + c, v + d + r, x0 + c + 0.5, y0 + r + 0.5, z0))
            out.append(("south", u + 2 * d + w + c, v + d + r, x1 - c - 0.5, y0 + r + 0.5, z1))
    return out


NORMAL = {"top": (0, -1, 0), "bottom": (0, 1, 0), "west": (-1, 0, 0), "east": (1, 0, 0), "north": (0, 0, -1),
          "south": (0, 0, 1)}


def layout(boxes, tw):
    """Shelf packing, tallest first: (box, (u, v)) for every box, and the texture height used."""
    rects = [(2 * b[4][2] + 2 * b[4][0], b[4][2] + b[4][1]) for b in boxes]
    order = sorted(range(len(boxes)), key=lambda k: (-rects[k][1], -rects[k][0], k))
    pos, x, y, shelf = [None] * len(boxes), 0, 0, 0
    for k in order:
        w, h = rects[k]
        if x + w > tw:
            x, y, shelf = 0, y + shelf, 0
        pos[k] = (x, y)
        x += w
        shelf = max(shelf, h)
    return [(boxes[k], pos[k]) for k in range(len(boxes))], y + shelf


def texture_size(boxes):
    for tw in (64, 128, 256):
        for th in (64, 128, 256):
            placed, used = layout(boxes, tw)
            if used <= th:
                return tw, th, placed
    raise AssertionError("texture too big")


def draw_texture(boxes):
    tw, th, placed = texture_size(boxes)
    img = Image.new("RGBA", (tw, th), CLEAR)
    ab = [abs_box(b) for b in boxes]
    owner = {}
    for idx, (box, (u, v)) in enumerate(placed):
        name, kind, part, origin, size = box
        px, py, pz = part_abs(part)
        for face, tu, tv, x, y, z in face_texels(u, v, origin, size):
            assert owner.setdefault((tu, tv), name) == name, ("texture overlap", name, owner[(tu, tv)])
            X, Y, Z = x + px, y + py, z + pz
            n = NORMAL[face]
            q = (X + n[0] * 0.01, Y + n[1] * 0.01, Z + n[2] * 0.01)
            hidden = any(j != idx and all(lo[k] < q[k] < hi[k] for k in range(3)) for j, (lo, hi) in enumerate(ab))
            if hidden:
                continue                     # lies against another box: left clear so the inside never shows
            img.putpixel((tu, tv), colour(kind, face, X, Y, Z, box))
    return img, placed, (tw, th)


# --- the Java model ---------------------------------------------------------------------------------------------------
def f(v):
    s = ("%.4f" % v).rstrip("0")
    if s.endswith("."):
        s += "0"
    if s == "-0.0":
        s = "0.0"
    return s + "F"


def java_source(placed, size):
    lines = [
        "package com.maltaminecraft.mimcontent.client.jelly;",
        "",
        "import net.minecraft.client.model.geom.ModelPart;",
        "import net.minecraft.client.model.geom.PartPose;",
        "import net.minecraft.client.model.geom.builders.CubeListBuilder;",
        "import net.minecraft.client.model.geom.builders.LayerDefinition;",
        "import net.minecraft.client.model.geom.builders.MeshDefinition;",
        "import net.minecraft.client.model.geom.builders.PartDefinition;",
        "",
        "/**",
        " * The fried-egg jellyfish (Cotylorhiza tuberculata): a wide, flat, cream-yellow bell 15 px across with a raised",
        " * orange-yellow dome in the middle (the \"yolk\"), and under it a short, wide drum of oral arms studded",
        " * with white knobs above and purple-blue ones below, with a few short knobbed filaments hanging under it. Round layers are",
        " * built of 1 px strips, so nothing overlaps; faces against another box are clear in the texture.",
        " * Made by art/src/jelly_fried_egg_model.py (do not edit by hand); texture",
        " * textures/entity/jellyfish/fried_egg_jellyfish.png. Parts: \"bell\" (pulsed by JellyfishModel), \"oral_arms\"",
        " * in it, and \"tentacle_0\".. \"tentacle_5\" in it (swayed by JellyfishModel).",
        " */",
        "public class FriedEggJellyfishModel extends JellyfishModel {",
        "    public FriedEggJellyfishModel(ModelPart root) {",
        "        super(root);",
        "    }",
        "",
        "    public static LayerDefinition createBodyLayer() {",
        "        MeshDefinition mesh = new MeshDefinition();",
        "        PartDefinition root = mesh.getRoot();",
    ]
    order = ["bell", "oral_arms"] + sorted((p for p in PARTS if p.startswith("tentacle_")), key=lambda s: int(s[9:]))
    for part in order:
        parent, (px, py, pz) = PARTS[part]
        builder = "CubeListBuilder.create()"
        for (name, kind, cpart, (x0, y0, z0), (w, h, d)), (u, v) in placed:
            if cpart != part:
                continue
            builder += "\n            .texOffs(%d, %d).addBox(%s, %s, %s, %s, %s, %s)" % (
                u, v, f(x0), f(y0), f(z0), f(w), f(h), f(d))
        has_child = any(p[0] == part for p in PARTS.values())
        var = "PartDefinition %s = " % part if has_child else ""
        lines.append("        %s%s.addOrReplaceChild(\"%s\", %s," % (var, parent or "root", part, builder))
        lines.append("            PartPose.offset(%s, %s, %s));" % (f(px), f(py), f(pz)))
    lines += ["        return LayerDefinition.create(mesh, %d, %d);" % size, "    }", "}", ""]
    return "\n".join(lines)


# --- offline renders --------------------------------------------------------------------------------------------------
SHADE = {"top": 1.0, "bottom": 0.5, "north": 0.8, "south": 0.8, "west": 0.6, "east": 0.6}


def render(placed, texture, yaw, pitch, scale, sub=3, bg=(40, 70, 110, 255)):
    """An orthographic texel splatter with alpha, back to front. pitch 0 = side, 90 = from above, -90 = below."""
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def project(p):
        x, y, z = p
        z2, x2 = z * cy + x * sy, -z * sy + x * cy
        return z2, y * cp - x2 * sp, y * sp + x2 * cp

    pts = []
    for (name, kind, part, origin, size), (u, v) in placed:
        px, py, pz = part_abs(part)
        for face, tu, tv, x, y, z in face_texels(u, v, origin, size):
            col = texture.getpixel((tu, tv))
            if col[3] == 0:
                continue
            k = SHADE[face]
            col = (int(col[0] * k), int(col[1] * k), int(col[2] * k), col[3])
            for i in range(sub):
                for j in range(sub):
                    a, b = (i + 0.5) / sub - 0.5, (j + 0.5) / sub - 0.5
                    if face in ("top", "bottom"):
                        p = (x + a, y, z + b)
                    elif face in ("west", "east"):
                        p = (x, y + a, z + b)
                    else:
                        p = (x + a, y + b, z)
                    pts.append((project((p[0] + px, p[1] + py, p[2] + pz)), col))
    xs = [q[0][0] for q in pts]
    ys = [q[0][1] for q in pts]
    minx, miny = min(xs) - 2, min(ys) - 2
    wpx = int((max(xs) - minx + 2) * scale)
    hpx = int((max(ys) - miny + 2) * scale)
    img = Image.new("RGBA", (wpx, hpx), bg)
    px_ = img.load()
    r = max(1, int(math.ceil(scale / sub / 2 + 0.5)))
    pts.sort(key=lambda q: -q[0][2])          # far first
    for (sx, sy_, sd), col in pts:
        cx, cyy = int((sx - minx) * scale), int((sy_ - miny) * scale)
        a = col[3] / 255.0
        for ox in range(-r, r):
            for oy in range(-r, r):
                kx, ky = cx + ox, cyy + oy
                if 0 <= kx < wpx and 0 <= ky < hpx:
                    o = px_[kx, ky]
                    px_[kx, ky] = (int(o[0] * (1 - a) + col[0] * a), int(o[1] * (1 - a) + col[1] * a),
                                   int(o[2] * (1 - a) + col[2] * a), 255)
    return img


def main():
    boxes = all_boxes()
    probs = check_boxes(boxes)
    for p in probs:
        print("problem:", p)
    assert not probs
    texture, placed, size = draw_texture(boxes)
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    os.makedirs(JAVA_DIR, exist_ok=True)
    texture.save(TEXTURE)
    with open(JAVA, "w", encoding="utf-8") as fh:
        fh.write(java_source(placed, size))
    lo = [min(abs_box(b)[0][k] for b in boxes) for k in range(3)]
    hi = [max(abs_box(b)[1][k] for b in boxes) for k in range(3)]
    print("wrote", os.path.relpath(TEXTURE, ROOT), "(%dx%d)" % size, "and", os.path.relpath(JAVA, ROOT))
    print("%d boxes; extent x %.1f..%.1f, y %.1f..%.1f, z %.1f..%.1f" % (len(boxes), lo[0], hi[0], lo[1], hi[1],
                                                                          lo[2], hi[2]))
    args = sys.argv[1:]
    if "--renders" in args:
        out = args[args.index("--renders") + 1]
        os.makedirs(out, exist_ok=True)
        views = {"side": (0, 0), "three": (35, 25), "above": (0, 90), "below": (0, -90), "low": (20, -20)}
        for n, (yw, pt) in views.items():
            render(placed, texture, yw, pt, 16).save(os.path.join(out, "offline_%s.png" % n))
        texture.resize((size[0] * 4, size[1] * 4), Image.NEAREST).save(os.path.join(out, "texture_4x.png"))
        print("renders:", out)


if __name__ == "__main__":
    main()
