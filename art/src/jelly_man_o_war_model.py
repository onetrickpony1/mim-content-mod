"""The Portuguese man o' war (Physalia physalis) as a floating mob: its 3D model and its texture.

Drawn from the reference photos in art/references/jelly_man_o_war_refonly/ (list.tsv; mw20, mw22, mw29 and mw31,
stranded on beaches, for the true colour; mw30 and mw13, afloat, for the shape and how it sits; mw08 and mw09 for the
polyps and the tentacles). What makes it a man o' war, and not a jellyfish:
  - no bell: a long, translucent gas float lying on the water, 10 px long (0.63 blocks): a rounded loaf, 4 wide and
    5 deep in the middle, stepping in by 1 px in width and height at both ends (never stacked tiers, which read as a
    layered cake), lopsided like the real float: the front end low and round, the back end rising to a 2x2 tip;
  - the crest (the "sail") along the top: a 1 px thick wall inside the float's outline, one wave of uneven heights
    (1-2-3-4-2-1 px), a blue-lilac membrane with only its top edge pink;
  - the float shaded round its body: a light lilac highlight on top, violet along the crest's foot, pale lilac-blue
    to cornflower and blue down the sides to the waterline, a deep blue underneath, violet towards the pink tip;
  - under the front two thirds, a grid of short mid-blue to teal polyps, 1-3 px long;
  - five thin fishing tentacles in blue and blue-violet with small, soft beads 2-5 px apart: one 3.5 blocks long, the
    others 1.4 to 2.4, three with a 1 px kink near the float.
It is drawn translucent: the float lets the water show through it (alpha about 0.65-0.9, clearer on top); the crest
a little clearer; polyps and tentacles nearly solid. Faces between two of the float's (or crest's) boxes are left
clear, so the float reads as one balloon with no seams inside. The box is 0.625 x 0.5625 blocks, so float and crest
stay within 9 px above the feet. Three rounds of independent critics in the game (2026-11-18); this version has the third round's fixes.

Not like the mauve stinger (a mauve-pink dome bell with long arms, pulsing) or the fried-egg jellyfish (a flat yellow
disc with a raised centre): the man o' war is a horizontal blue balloon with a pink crest, sitting on the surface.

Model contract (the jellyfish builder's, 2026-11-18): `ManOWarModel extends JellyfishModel`, a root child "bell" (here
the float, pivoted at its middle so the base class can bob and tilt it), children "tentacle_0".."tentacle_4" of
"bell", pivoted at their roots (the base class sways them). y 24 is the entity's feet, the float's underside.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/jelly/ManOWarModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/jellyfish/man_o_war.png    (128 x 64)
With --sheet OUT.png [SCREENSHOT_DIR] it also writes a compare sheet (offline renders with alpha, the references, the
texture and, if given, the in-game shots).

Run:  art/.venv/bin/python art/src/jelly_man_o_war_model.py [--sheet OUT.png [SCREENSHOT_DIR]]
"""
import glob
import math
import os
import sys
import zipfile

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import fish_awrata_model as AW  # noqa: E402  (face_texels, parse_java, rot_point)

RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA_DIR = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "jelly")
JAVA = os.path.join(JAVA_DIR, "ManOWarModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "jellyfish", "man_o_war.png")
REF_DIR = os.path.join(ROOT, "art", "references", "jelly_man_o_war_refonly")
TW, TH = 128, 64


def hexc(s, a=255):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), a)


# Colours from the stranded floats (mw20, mw22, mw29, mw31) and the afloat ones (mw13, mw30), a step lighter for the
# parts that hang in the water (polyps, tentacles), which the game greys. (colour, alpha)
PAL = {
    # the float: pale blue-white on top, violet along the crest, cyan-blue at the waterline (critic rounds 1 and 2: the
    # paler ramps greyed to white and then mauve in the game)
    "F0": hexc("#c8ccf8", 175),    # the top: a light lilac highlight, not white
    "F1": hexc("#a8b4f4", 192),    # upper side, pale lilac-blue
    "F2": hexc("#8ea0f0", 205),    # side, lavender-blue
    "F3": hexc("#6e8cec", 218),    # cornflower blue
    "F4": hexc("#4a7ce4", 230),    # blue, the waterline
    "F5": hexc("#3a5cc8", 240),    # underneath
    "V1": hexc("#b8b0f4", 185),    # violet along the crest's foot
    "V2": hexc("#a894ee", 210),    # violet, the back towards the knob
    "P1": hexc("#d080e0", 230),    # the pink knob at the tip
    # the crest: a blue-lilac membrane with only its top edge pink (critic round 3)
    "C0": hexc("#e86cd8", 235),    # the pink edge, 1 px
    "C1": hexc("#b4a8f0", 200),    # the membrane, blue-lilac
    "C2": hexc("#a8acf0", 200),    # its foot
    # polyps: mid blue to teal
    "Q0": hexc("#3460c8", 250),
    "Q1": hexc("#3c78dc", 250),
    "Q2": hexc("#5aa4ea", 250),
    "Q3": hexc("#5a6ad4", 250),
    # tentacles: blue and blue-violet with small darker beads
    "T0": hexc("#6c8af2", 240),
    "T1": hexc("#7c7cf0", 240),
    "T2": hexc("#5c6ae0", 240),    # the beads, half the contrast of round 3
    ".": (0, 0, 0, 0),
}

# --- the model -------------------------------------------------------------------------------------------------------
BELL_PIVOT = (0.0, 21.0, 0.0)     # the middle of the float: it bobs and tilts about here

# The float: one main box with stepped ends, never stacked tiers (critic round 2: the cut corners and stepped tops read
# as a layered cake). Lopsided like the real float: the front end low and round, the back end rising to the pink knob.
# (name, z0, z1, top, bottom, width), absolute model pixels, y down, 24 the entity's feet.
FLOAT = [
    ("front", -5, -4, 21, 23, 2),
    ("bow", -4, -3, 20, 24, 3),
    ("main", -3, 2, 19, 24, 4),
    ("aft", 2, 3, 19, 23, 3),
    ("rear", 3, 4, 18, 21, 2),
    ("tip", 4, 5, 17, 19, 2),      # the raised 2x2 tip
]
SEG = {s[0]: s for s in FLOAT}

# The crest: a 1 px thick wall of single columns on the float's middle line, z -3..3, one continuous wavy edge.
# The box is 0.5625 tall, so its highest point is y 15 (9 px above the feet).
CREST_Z0 = -3
CREST_TOP = [18, 17, 16, 15, 17, 18]               # z -3 .. 2: heights 1-2-3-4-2-1, no tooth alone
CREST_FOOT = [19, 19, 19, 19, 19, 19]              # it stands on the main box, inside the float's outline

# Polyps: a grid of 1x1 columns hanging from the main box's underside (y 24), x cells -2..1, z -4..1; the number is the
# length (1-3), 0 is empty and "T" a tentacle's root.
POLYP_GRID = [            # x: -2  -1   0   1
    [1, 2, 1, 0],         # z -4
    [2, "T", 3, 1],       # z -3
    [1, 2, "T", 2],       # z -2
    [3, 1, 2, "T"],       # z -1
    ["T", 2, 1, 3],       # z 0
    [1, 0, "T", 1],       # z 1
]
POLYPS = [(xi - 2.0, zi - 4, 24, n) for zi, row in enumerate(POLYP_GRID) for xi, n in enumerate(row)
          if n not in (0, "T")]
# Fishing tentacles: (x0, z0, length, top, kinks). Uneven lengths: one 3.5 blocks, the others 1.4 to 2.4. Kinks:
# {bead index: (dx, dz)}: from that bead on, the line steps 1 px sideways (the new bead starts a row higher, beside
# the last one, so the two touch).
TENTACLES = [
    (-1.0, -3, 56, 24, {3: (-1, 0)}),      # the long one
    (0.0, -2, 38, 24, {}),
    (1.0, -1, 28, 24, {5: (1, 0)}),
    (-2.0, 0, 22, 24, {3: (0, -1)}),
    (0.0, 1, 32, 24, {4: (0, 1)}),
]
BEAD = 3


def float_cubes():
    return [(name, name, (-w / 2, top, z0), (w, bot - top, z1 - z0)) for name, z0, z1, top, bot, w in FLOAT]


def all_cubes():
    """Every cube as (name, kind, part, abs origin, size)."""
    out = [(n, ("float", seg), "bell", o, s) for n, seg, o, s in float_cubes()]
    for c, (top, foot) in enumerate(zip(CREST_TOP, CREST_FOOT)):
        out.append(("crest_%d" % c, ("crest", c), "bell", (-0.5, float(top), float(CREST_Z0 + c)), (1, foot - top, 1)))
    for i, (x0, z0, top, ln) in enumerate(POLYPS):
        out.append(("polyp_%d" % i, ("polyp", i), "bell", (x0, float(top), float(z0)), (1, ln, 1)))
    for i, (x0, z0, ln, top, kinks) in enumerate(TENTACLES):
        y, k, dx, dz = float(top), 0, 0, 0
        while y < top + ln:
            h = min(BEAD, top + ln - y)
            if k in kinks:
                dx, dz = dx + kinks[k][0], dz + kinks[k][1]
                y -= 1
                h += 1
            out.append(("tentacle_%d_%d" % (i, k), ("tentacle", i, k), "tentacle_%d" % i,
                        (x0 + dx, y, z0 + dz), (1, int(h), 1)))
            y += h
            k += 1
    return out


def part_pivot(part):
    """Absolute pivot of each part."""
    if part == "bell":
        return BELL_PIVOT
    i = int(part.split("_")[1])
    x0, z0, _ln, top, _k = TENTACLES[i]
    return (x0 + 0.5, float(top), z0 + 0.5)


PARTS = ["bell"] + ["tentacle_%d" % i for i in range(len(TENTACLES))]


# --- colour ----------------------------------------------------------------------------------------------------------
def inside_other(name, kind, p):
    """True if point p (abs) lies inside another box of the same kind (float or crest): that face is hidden and left
    clear, so the translucent float shows no seams inside."""
    for n, k, _part, (x0, y0, z0), (w, h, d) in all_cubes():
        if n == name or k[0] != kind:
            continue
        if x0 < p[0] < x0 + w and y0 < p[1] < y0 + h and z0 < p[2] < z0 + d:
            return True
    return False


NORMAL = {"top": (0, -1, 0), "bottom": (0, 1, 0), "west": (-1, 0, 0), "east": (1, 0, 0),
          "north": (0, 0, -1), "south": (0, 0, 1)}


def side_band(f):
    """The colour down the float's side, f 0 at the top of this step to 1 at its bottom."""
    if f < 0.2:
        return "F1"
    if f < 0.4:
        return "F2"
    if f < 0.6:
        return "F3"
    return "F4"


def float_key(cube, seg, face, x, y, z):
    _n, z0, z1, top, bot, w = SEG[seg]
    if seg == "tip":
        return "P1" if face in ("top", "south") or y < 18 else "V2"   # pink only at the very end, blended in
    if face == "top":
        if abs(x) < 1.0:
            return "V1"                 # violet along the crest's foot
        return "F0"
    if face == "bottom":
        return "F5"
    if seg in ("rear", "aft") and y < 20:
        return "V2"                     # the back turning violet towards the knob
    return side_band((y - top) / float(bot - top))


def crest_key(c, face, y):
    yi = int(math.floor(y))
    top, foot = CREST_TOP[c], CREST_FOOT[c]
    if face == "bottom":
        return "."
    if face == "top" or yi == top:
        return "C0"                     # the pale pink edge
    if yi == foot - 1:
        return "C2"                     # the foot, cooler, into the float
    return "C1"


def polyp_key(i, face, y, top, ln):
    r = int(math.floor(y)) - top
    base = ("Q1", "Q2", "Q3", "Q1", "Q0")[i % 5]
    if face == "top":
        return "."
    if face == "bottom" or r == ln - 1:
        return "Q2" if base != "Q2" else "Q1"   # the tips a step lighter
    return base


BEAD_GAPS = [3, 2, 5, 4, 2, 3, 5]   # rows between beads, uneven (critic round 3)


def bead_rows(i, length):
    rows, r, k = set(), 2 + i % 2, i
    while r < length:
        rows.add(r)
        r += BEAD_GAPS[k % len(BEAD_GAPS)]
        k += 1
    return rows


def tentacle_key(i, k, face, y, top):
    base = "T1" if i % 2 else "T0"
    _x0, _z0, ln, t_top, _kinks = TENTACLES[i]
    r = int(math.floor(y)) - t_top
    if face in ("west", "east", "north", "south") and r in bead_rows(i, ln):
        return "T2"                     # a small, softer bead at uneven spacing
    return base


def texel_key(cube, face, x, y, z):
    name, kind, _part, (x0, y0, z0), (w, h, d) = cube
    if kind[0] in ("float", "crest"):
        n = NORMAL[face]
        if inside_other(name, kind[0], (x + n[0] * 0.01, y + n[1] * 0.01, z + n[2] * 0.01)):
            return "."
    if kind[0] == "float":
        return float_key(name, kind[1], face, x, y, z)
    if kind[0] == "crest":
        return crest_key(kind[1], face, y)
    if kind[0] == "polyp":
        return polyp_key(kind[1], face, y, int(y0), h)
    if kind[0] == "tentacle":
        return tentacle_key(kind[1], kind[2], face, y, int(y0))
    raise ValueError(kind)


# --- texture layout --------------------------------------------------------------------------------------------------
def used_rect(size):
    w, h, d = size
    if w == 0:
        return (0, d), (2 * d, h)
    return (0, 0), (2 * d + 2 * w, d + h)


def layout():
    cubes = all_cubes()
    rects = [used_rect(c[4]) for c in cubes]
    order = sorted(range(len(cubes)), key=lambda k: (-rects[k][1][1], -rects[k][1][0], k))
    pos, x, y, shelf = [None] * len(cubes), 0, 0, 0
    for k in order:
        w, h = rects[k][1]
        if x + w > TW:
            x, y, shelf = 0, y + shelf, 0
        pos[k] = (x, y)
        x += w
        shelf = max(shelf, h)
    assert y + shelf <= TH, ("texture too small", y + shelf)
    return [(cubes[k], (pos[k][0] - rects[k][0][0], pos[k][1] - rects[k][0][1])) for k in range(len(cubes))]


def draw_texture():
    img = Image.new("RGBA", (TW, TH), PAL["."])
    owner = {}
    for cube, (u, v) in layout():
        name, _kind, _part, (x0, y0, z0), (w, h, d) = cube
        for face, tu, tv, x, y, z in AW.face_texels(u, v, (0, 0, 0), (w, h, d)):
            if w == 0 and face not in ("west", "east"):
                continue
            assert 0 <= tu < TW and 0 <= tv < TH, (name, face, tu, tv)
            assert owner.setdefault((tu, tv), name) == name, ("texture overlap", name, owner[(tu, tv)], tu, tv)
            key = texel_key(cube, face, x + x0, y + y0, z + z0)
            img.putpixel((tu, tv), PAL[key])
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def f(v):
    s = ("%.4f" % v).rstrip("0")
    if s.endswith("."):
        s += "0"
    if s == "-0.0":
        s = "0.0"
    return s + "F"


def java_source():
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
        " * The Portuguese man o' war (Physalia physalis): no bell, but a long translucent gas float lying on the water,",
        " * low and round at the front, rising to a pink tip at the back, with a wavy pink-edged crest along its top,",
        " * short blue polyps beneath and five thin beaded blue-violet fishing tentacles hanging 1.4 to 3.5 blocks down.",
        " * The float is the \"bell\" (pivoted at its middle: the base class bobs and tilts it, no pulse);",
        " * \"tentacle_0\"..\"tentacle_4\" are its children, pivoted at their roots, and sway.",
        " * Made by art/src/jelly_man_o_war_model.py (do not edit by hand); texture textures/entity/jellyfish/man_o_war.png.",
        " */",
        "public class ManOWarModel extends JellyfishModel {",
        "    public ManOWarModel(ModelPart root) {",
        "        super(root);",
        "    }",
        "",
        "    public static LayerDefinition createBodyLayer() {",
        "        MeshDefinition mesh = new MeshDefinition();",
        "        PartDefinition root = mesh.getRoot();",
    ]
    placed = layout()
    for part in PARTS:
        pv = part_pivot(part)
        parent = "root" if part == "bell" else "bell"
        ppv = (0.0, 0.0, 0.0) if part == "bell" else BELL_PIVOT
        builder = "CubeListBuilder.create()"
        for (name, _kind, cpart, (x0, y0, z0), (w, h, d)), (u, v) in placed:
            if cpart != part:
                continue
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %s, %s, %s)" % (
                name, u, v, f(x0 - pv[0]), f(y0 - pv[1]), f(z0 - pv[2]), f(w), f(h), f(d))
        pose = "PartPose.offset(%s, %s, %s)" % (f(pv[0] - ppv[0]), f(pv[1] - ppv[1]), f(pv[2] - ppv[2]))
        var = "PartDefinition bell = " if part == "bell" else ""
        lines.append("        %s%s.addOrReplaceChild(\"%s\", %s," % (var, parent, part, builder))
        lines.append("            %s);" % pose)
    lines += ["        return LayerDefinition.create(mesh, %d, %d);" % (TW, TH), "    }", "}", ""]
    return "\n".join(lines)


# --- checks ----------------------------------------------------------------------------------------------------------
def check():
    """Solid boxes must not overlap, and every box must touch another (nothing floats free)."""
    cubes = [c for c in all_cubes() if all(c[4])]
    probs = []

    def box(c):
        (x0, y0, z0), (w, h, d) = c[3], c[4]
        return (x0, y0, z0), (x0 + w, y0 + h, z0 + d)

    for i in range(len(cubes)):
        a0, a1 = box(cubes[i])
        touches = False
        for j in range(len(cubes)):
            if i == j:
                continue
            b0, b1 = box(cubes[j])
            ov = [min(a1[k], b1[k]) - max(a0[k], b0[k]) for k in range(3)]
            if all(o > 1e-6 for o in ov):
                probs.append(("overlap", cubes[i][0], cubes[j][0]))
            if all(o > -1e-6 for o in ov) and sum(o > 1e-6 for o in ov) >= 2:
                touches = True
        if not touches:
            probs.append(("floats free", cubes[i][0]))
    return probs


# --- offline renderer with alpha ------------------------------------------------------------------------------------
SHADE = {"top": 1.0, "bottom": 0.5, "north": 0.8, "south": 0.8, "west": 0.6, "east": 0.6}


def render(model, texture, view, scale, sub=3, bg=(0, 0, 0, 0)):
    """Draw a parsed model with alpha blending (back to front). Views: 'side' (from -x, front left), 'three' (front
    three-quarter from above), 'top', 'below' (from under, looking up)."""
    parts, _ = model
    by_name = {p[0]: p for p in parts}

    def world(part, p):
        while part:
            _, parent, pivot, rot, _ = by_name[part]
            p = AW.rot_point(p, rot)
            p = (p[0] + pivot[0], p[1] + pivot[1], p[2] + pivot[2])
            part = parent
        return p

    yaw, pitch = {"side": (0.0, 0.0), "top": (0.0, 90.0), "three": (35.0, 25.0), "below": (30.0, -35.0),
                  "front": (90.0, 15.0)}[view]
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def project(p):
        x, y, z = p
        z2, x2 = z * cy + x * sy, -z * sy + x * cy
        return z2, y * cp - x2 * sp, y * sp + x2 * cp

    pts = []
    for name, _, _, _, cubes in parts:
        for u, v, origin, size in cubes:
            for face, tu, tv, x, y, z in AW.face_texels(u, v, origin, size):
                if size[0] == 0 and face not in ("west", "east"):
                    continue
                if not (0 <= tu < texture.size[0] and 0 <= tv < texture.size[1]):
                    continue
                col = texture.getpixel((tu, tv))
                if col[3] == 0:
                    continue
                k = SHADE[face]
                col = (col[0] * k, col[1] * k, col[2] * k, col[3] / 255.0)
                for i in range(sub):
                    for j in range(sub):
                        a, b = (i + 0.5) / sub - 0.5, (j + 0.5) / sub - 0.5
                        if face in ("top", "bottom"):
                            p = (x + a, y, z + b)
                        elif face in ("west", "east"):
                            p = (x, y + a, z + b)
                        else:
                            p = (x + a, y + b, z)
                        pts.append((project(world(name, p)), col))
    xs = [q[0][0] for q in pts]
    ys = [q[0][1] for q in pts]
    minx, miny = min(xs) - 1, min(ys) - 1
    wpx = int((max(xs) - minx + 1) * scale) + 1
    hpx = int((max(ys) - miny + 1) * scale) + 1
    frags = {}
    r = max(1, int(math.ceil(scale / sub / 2 + 0.5)))
    for (sx, sy_, sd), col in pts:
        px, py = int((sx - minx) * scale), int((sy_ - miny) * scale)
        for ox in range(-r, r):
            for oy in range(-r, r):
                key = (px + ox, py + oy)
                if 0 <= key[0] < wpx and 0 <= key[1] < hpx:
                    lst = frags.setdefault(key, {})
                    # one fragment per surface position (depth rounded): splats of the same face don't stack
                    dk = round(sd * 2)
                    if dk not in lst:
                        lst[dk] = col
    img = Image.new("RGBA", (wpx, hpx), bg)
    px_ = img.load()
    for key, lst in frags.items():
        r_, g_, b_, a_ = [c / 255.0 for c in bg]
        for dk in sorted(lst, reverse=True):      # far to near
            cr, cg, cb, ca = lst[dk]
            r_ = r_ * (1 - ca) + cr / 255.0 * ca
            g_ = g_ * (1 - ca) + cg / 255.0 * ca
            b_ = b_ * (1 - ca) + cb / 255.0 * ca
            a_ = a_ * (1 - ca) + ca
        if a_ > 0:
            if bg[3] == 0:
                # unpremultiply for a transparent background
                px_[key] = (int(min(255, r_ / a_ * 255)), int(min(255, g_ / a_ * 255)), int(min(255, b_ / a_ * 255)),
                            int(a_ * 255))
            else:
                px_[key] = (int(r_ * 255), int(g_ * 255), int(b_ * 255), 255)
    return img


def game_texture(path):
    for jar in sorted(glob.glob(os.path.join(ROOT, ".art-runs", "*", ".gradle", "loom-cache", "minecraftMaven", "net",
                                             "minecraft", "minecraft-merged-*", "26.3", "*.jar"))):
        with zipfile.ZipFile(jar) as z:
            try:
                with z.open("assets/minecraft/textures/" + path) as fh:
                    return Image.open(fh).convert("RGBA").copy()
            except KeyError:
                continue
    return None


def sheet(dest, shots_dir, texture):
    from PIL import ImageFont
    font = ImageFont.load_default()
    W = 1800
    blocks = []
    me = (AW.parse_java(JAVA), texture)

    def title(t):
        im = Image.new("RGBA", (W, 26), (40, 40, 40, 255))
        ImageDraw.Draw(im).text((8, 6), t, fill=(240, 240, 240, 255), font=font)
        blocks.append(im)

    def row(images, h=None, gap=16):
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images)
        im = Image.new("RGBA", (W, hh + 8), (72, 72, 72, 255))
        x = 8
        for i in images:
            if x + i.width > W:
                break
            im.paste(i, (x, 4), i)
            x += i.width + gap
        blocks.append(im)

    refs = [Image.open(os.path.join(REF_DIR, n)).convert("RGBA")
            for n in ("mw29.jpg", "mw30.jpg", "mw22.jpg", "mw20.jpg", "mw09.jpg")
            if os.path.exists(os.path.join(REF_DIR, n))]
    title("References (reference only): stranded floats for true colour, afloat for shape, polyps and tentacles")
    row(refs, h=230)
    water = (52, 92, 150, 255)
    sand = (214, 200, 160, 255)
    title("Offline, float only (tentacles cut), 16x: side, three-quarter, top, from below, front - over water blue")
    float_only = ([p for p in me[0][0] if not p[0].startswith("tentacle")], me[0][1])
    row([render(float_only, texture, v, 16, bg=water) for v in ("side", "three", "top")])
    row([render(float_only, texture, v, 16, bg=water) for v in ("below", "front")]
        + [render(float_only, texture, "three", 16, bg=sand)])
    title("Offline, whole animal, 5x: side, three-quarter, from below (over water blue and over sand)")
    row([render(me[0], texture, v, 5, bg=water) for v in ("side", "three", "below")]
        + [render(me[0], texture, "side", 5, bg=sand)])
    title("Texture at 6x and 1x (%d x %d)" % (TW, TH))
    bgt = Image.new("RGBA", (TW * 6, TH * 6), (90, 90, 90, 255))
    bgt.alpha_composite(texture.resize((TW * 6, TH * 6), Image.NEAREST))
    row([bgt, texture])
    if shots_dir and os.path.isdir(shots_dir):
        shots = sorted(glob.glob(os.path.join(shots_dir, "*man*war*.png")) + glob.glob(os.path.join(shots_dir,
                                                                                                  "*manowar*.png")))
        if shots:
            title("In the game")
            for k in range(0, len(shots), 3):
                row([Image.open(s).convert("RGBA") for s in shots[k:k + 3]], h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    probs = check()
    for p in probs:
        print("problem:", p)
    assert not probs
    texture = draw_texture()
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    os.makedirs(JAVA_DIR, exist_ok=True)
    texture.save(TEXTURE)
    with open(JAVA, "w", encoding="utf-8") as fh:
        fh.write(java_source())
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    args = sys.argv[1:]
    if "--sheet" in args:
        i = args.index("--sheet")
        sheet(args[i + 1], args[i + 2] if i + 2 < len(args) else None, texture)


if __name__ == "__main__":
    main()
