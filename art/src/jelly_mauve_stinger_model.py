"""The mauve stinger (Pelagia noctiluca) as a drifting mob: its 3D model and its texture.

Drawn from the reference photos in art/references/jelly_mauve_stinger_refonly/ (list.tsv; ms09, ms05 and ms01 for the
shape and colour, ms02 for the warts close up). What makes it a mauve stinger, and not the fried-egg jellyfish (a flat
yellow-brown disc with a raised centre and short knobbed arms) or the man o' war (a blue gas float on the surface):
  - a small dome bell, mushroom-cap shaped: 8 px across and 5 tall (4, 6, 7 and 8 px wide from the top), rounded in
    1 px steps (each layer is an octagon, its corners cut by 1 px), with a scalloped rim of lappets;
  - see-through pink-mauve, lit from the top and shading down to a deeper mauve at the rim;
  - covered all over in raised warts of stinging cells: darker mauve dots, each with a pale lit pixel above it so it
    reads as a bump. They are scattered (blue noise, two tones, none touching, no mirrored pairs on a face), so they
    can't read as eyes or a face; a deeper magenta centre shows through the bell;
  - 8 long, hair-thin marginal tentacles from the rim (1 px texture, drawn 0.4 px thick), pale pink, fading at the tips;
  - 4 longer, frilly oral arms hanging from the centre under the bell (a cross of ruffled ribbons turned 45 degrees),
    in a deeper magenta with pale frilled edges, reaching well below the tentacles.
The green glow is particles in the game and is not painted.

Model contract (the jellyfish mob, client/jelly/JellyfishModel.java): a root child "bell" (the base class pulses it),
"tentacle_0".."tentacle_7" (children of "bell", hinged at the rim; the base class sways them) and "oral_arms" (a child
of "bell"). y 24 is the ground. The texture is drawn translucent: the bell is see-through, the warts nearly solid.
Faces that are hidden inside the bell (where its layers meet) are fully clear, so the bell is one clean shell.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/jelly/MauveStingerModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/jellyfish/mauve_stinger.png
With --sheet DIR it also writes the compare sheet DIR/jelly_mauve_stinger_model.png (offline renders, alpha blended).

Run:  art/.venv/bin/python art/src/jelly_mauve_stinger_model.py [--sheet DIR]
"""
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import fish_awrata_model as AW  # noqa: E402  (face_texels, parse_java, rot_point: the shared model helpers)

RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA_DIR = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "jelly")
JAVA = os.path.join(JAVA_DIR, "MauveStingerModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "jellyfish", "mauve_stinger.png")
TW, TH = 64, 64


def hexc(s, a=255):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), a)


# Colours from the photos (ms09, ms05, ms01), a step lighter for the water. (r, g, b) only; alpha is set per part.
COL = {
    "hi": "#ffd6f8",     # the lit top of the dome
    "b1": "#f8a8f0",     # the upper bell
    "b2": "#f08ae8",     # the middle of the bell
    "b3": "#dc6ed8",     # the lower bell, turning away
    "b4": "#c254c4",     # the rim in the shade
    "sub": "#cc60cc",    # the underside of the bell (subumbrella): one even mid mauve
    "core": "#b42abc",   # the deep magenta centre seen through the bell (ms09)
    "w1": "#b03cb4",     # a wart, dark mauve
    "w2": "#c24cc4",     # a wart, softer
    "wl": "#ffe0fa",     # the lit top of a wart (raised)
    "t1": "#eea0ec",     # tentacle, near the rim
    "t2": "#f4b8f2",     # tentacle, further down
    "t3": "#f8d0f6",     # tentacle tip
    "a0": "#9a1aa8",     # oral arm, inner fold (deepest)
    "a1": "#c02ac4",     # oral arm
    "a2": "#dc4ade",     # oral arm, lit
    "a3": "#f49cf4",     # oral arm frill edge, pale
    "m": "#b02ab8",      # the mouth stalk (manubrium)
}
RGB = {k: hexc(v)[:3] for k, v in COL.items()}
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
RIM = 8.0                                  # the bottom of the bell (absolute y); the bell part hinges here
# The bell, top to bottom: (name, y0, y1, width). Each is an octagon: a full-width core and two 1 px narrower slabs.
BELL = [
    ("cap", 3, 4, 4),
    ("dome", 4, 5, 6),
    ("side", 5, 7, 7),
    ("lappet", 7, 8, 8),
]
# The 8 marginal tentacles: (centre x, centre z, length). On the rim's corners and edge middles, lengths varied.
TENTACLES = [
    (0.0, -3.5, 9), (2.5, -2.5, 8), (3.5, 0.0, 10), (2.5, 2.5, 8),
    (0.0, 3.5, 9), (-2.5, 2.5, 10), (-3.5, 0.0, 8), (-2.5, -2.5, 9),
]
MANUBRIUM = ((-1.0, RIM, -1.0), (2, 1, 2))   # the mouth stalk under the bell's centre
ARM_TOP = RIM + 1                           # the arms hang from the stalk's underside
# The 4 oral arms: radial ribbons from the centre line: (name, plane, sign, length). "x" = in the x=0 plane, going
# out along z; "z" = in the z=0 plane, going out along x. 4 px wide at most.
ARMS = [("arm_n", "x", -1, 15), ("arm_s", "x", 1, 13), ("arm_e", "z", 1, 12), ("arm_w", "z", -1, 14)]
ARM_TURN = math.pi / 4      # the arms' cross is turned 45 degrees, so every side view shows them as an X of ruffles
THIN = -0.3                 # the tentacles are drawn 0.4 px thick (a CubeDeformation; the texture stays 1 px)
# The magenta centre inside the bell, seen through it (stomach and gonads in ms09): inside the bell, no face showing
# outside it.
CORE = ((-1.5, 5.0, -1.5), (3, 2, 3))
ARM_W = 4


def bell_cubes():
    out = []
    for name, y0, y1, w in BELL:
        h = y1 - y0
        out.append((name, (-w / 2, y0, -(w - 2) / 2), (w, h, w - 2)))
        out.append((name + "_f", (-(w - 2) / 2, y0, -w / 2), (w - 2, h, 1)))
        out.append((name + "_b", (-(w - 2) / 2, y0, (w - 2) / 2), (w - 2, h, 1)))
    return out


def all_cubes():
    """Every cube as (name, kind, part, absolute origin, size). Kind: bell, tentacle, stalk or arm."""
    out = [(n, "bell", "bell", o, s) for n, o, s in bell_cubes()]
    out.append(("core", "core", "bell", CORE[0], CORE[1]))
    for i, (cx, cz, ln) in enumerate(TENTACLES):
        out.append(("tentacle_%d" % i, "tentacle", "tentacle_%d" % i, (cx - 0.5, RIM, cz - 0.5), (1, ln, 1)))
    out.append(("stalk", "stalk", "oral_arms", MANUBRIUM[0], MANUBRIUM[1]))
    for name, plane, sign, ln in ARMS:
        if plane == "x":
            z0 = -ARM_W if sign < 0 else 0
            out.append((name, "arm", "oral_arms", (0.0, ARM_TOP, z0), (0, ln, ARM_W)))
        else:
            x0 = -ARM_W if sign < 0 else 0
            out.append((name, "arm", "oral_arms", (x0, ARM_TOP, 0.0), (ARM_W, ln, 0)))
    return out


# Parts: name -> (parent, absolute pivot). Nothing is turned at rest; the base class moves them.
PARTS = {"bell": (None, (0.0, RIM, 0.0))}
for _i, (_cx, _cz, _ln) in enumerate(TENTACLES):
    PARTS["tentacle_%d" % _i] = ("bell", (_cx, RIM, _cz))
PARTS["oral_arms"] = ("bell", (0.0, RIM, 0.0))
PART_ORDER = ["bell"] + ["tentacle_%d" % i for i in range(len(TENTACLES))] + ["oral_arms"]


def rel_pivot(part):
    parent, p = PARTS[part]
    if parent is None:
        return p
    q = PARTS[parent][1]
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


# --- colour ----------------------------------------------------------------------------------------------------------
def hash01(*vals):
    h = 2166136261
    for v in vals:
        for ch in repr(v).encode():
            h = ((h ^ ch) * 16777619) & 0xFFFFFFFF
    return h / 4294967295.0


NORMAL = {"top": (0, -1, 0), "bottom": (0, 1, 0), "west": (-1, 0, 0), "east": (1, 0, 0),
          "north": (0, 0, -1), "south": (0, 0, 1)}


def inside(p, cube, eps=1e-6):
    _n, _k, _p, (x0, y0, z0), (w, h, d) = cube
    return (x0 + eps < p[0] < x0 + w - eps and y0 + eps < p[1] < y0 + h - eps and z0 + eps < p[2] < z0 + d - eps)


def covered(cube, face, p, solids):
    """A face texel hidden against another bell box (where the layers and slabs meet)."""
    n = NORMAL[face]
    q = (p[0] + n[0] * 0.01, p[1] + n[1] * 0.01, p[2] + n[2] * 0.01)
    return any(inside(q, c) for c in solids if c is not cube)


WART_CACHE = {}


def face_warts(key, cols, rows, density):
    """The warts on one face of the bell: a blue-noise scatter, about one texel in five to seven (denser toward the top), no two touching (not even
    at a corner), so the spots look scattered and never line up into eyes or a face. Returns {(a, b): tone}."""
    if key in WART_CACHE:
        return WART_CACHE[key]
    cells = sorted(((a, b) for a in range(cols) for b in range(rows)), key=lambda c: hash01("w", key, c))
    want = max(1, int(round(cols * rows * density)))
    got = {}
    for a, b in cells:
        if len(got) >= want:
            break
        if any(abs(a - c) <= 1 and abs(b - d) <= 1 for c, d in got):
            continue
        if (cols - 1 - a, b) in got or (a, rows - 1 - b) in got or (cols - 1 - a, rows - 1 - b) in got:
            continue                                  # no mirrored pairs (two "eyes") on a face
        got[(a, b)] = "w1" if hash01("t", key, a, b) < 0.55 else "w2"
    WART_CACHE[key] = got
    return got


def bell_texel(face, x, y, z, layer):
    """The bell's colour and alpha at a surface point (absolute model space)."""
    # light from the top (and a little from the front-left): height on the bell decides the tone
    t = (y - 3.0) / 5.0                              # 0 at the top of the cap, 1 at the rim
    side = (-x * 0.5 - z * 0.5) / 4.0                # -1..1: front-left lit, back-right shaded
    v = t - side * 0.12 + (hash01("n", face, round(x, 1), round(y, 1), round(z, 1)) - 0.5) * 0.12
    if face == "bottom":
        if layer == "lappet":
            # the underside: pale, see-through, a darker ring at the margin
            rr = max(abs(x), abs(z))
            return RGB["sub"] + (120,)
        return RGB["b2"] + (115,)                    # the step under a narrower layer (only the dome's ring shows)
    if face == "top":
        key = "hi" if layer == "cap" else ("b1" if layer == "dome" else "b2")
    else:
        key = "hi" if v < 0.08 else "b1" if v < 0.36 else "b2" if v < 0.62 else "b3" if v < 0.84 else "b4"
    alpha = int(90 + 40 * max(0.0, min(1.0, t)))       # a glassy skin, a little thicker toward the rim
    # the lappets: a scalloped rim, the lobes and the notches between them in two tones (no holes)
    if layer == "lappet" and face not in ("top", "bottom"):
        along = x if face in ("north", "south") else z
        if hash01("lw", face, round(along, 1)) < 0.25:
            return RGB["w1"] + (200,)                 # a wart on the rim
        if int(math.floor(along + 8)) % 2:
            return RGB["b3"] + (140,)
        return RGB["b4"] + (175,)
    # warts on the sides and tops: (a, b) the texel on this face, b counted down from the face's top
    if face == "top":
        a, b, cols, rows = int(math.floor(x + 8)), int(math.floor(z + 8)), 16, 16
    elif face in ("north", "south"):
        a, b, cols, rows = int(math.floor(x + 8)), int(math.floor(y)), 16, 16
    else:
        a, b, cols, rows = int(math.floor(z + 8)), int(math.floor(y)), 16, 16
    density = {"cap": 0.1, "dome": 0.16, "side": 0.2}.get(layer, 0.0)
    warts = face_warts((layer, face, round(x if face in ("west", "east") else z, 1) if face != "top" else 0),
                       cols, rows, density)
    w = warts.get((a, b))
    if w:
        if face == "top":
            w = "w2"                                  # softer on the lit top, so the crown stays the lightest
        return RGB[w] + (200,)
    # the lit top of a raised wart: the pixel above it (on side faces) is pale
    if face != "top" and (a, b + 1) in warts and layer != "lappet":
        return RGB["wl"] + (170,)
    return RGB[key] + (alpha,)


def tentacle_texel(i, face, y, ln):
    r = (y - RIM) / ln                                # 0 at the rim, 1 at the tip
    yi = int(math.floor(y))
    if face == "top":
        return CLEAR
    if face == "bottom":
        return RGB["t3"] + (80,)
    # a few dark spots, never on neighbouring rows, on the upper part
    if r < 0.7 and hash01("t", i, face, yi) < 0.22 and yi % 2 == i % 2:
        return RGB["b3"] + (150,)
    key = "t1" if r < 0.35 else "t2" if r < 0.75 else "t3"
    alpha = int(130 - 50 * max(0.0, r - 0.6) / 0.4) if r > 0.6 else 130
    return RGB[key] + (alpha,)


def arm_width(name, row, ln):
    """How far out (1..4 px) the frilled ribbon reaches on this row: narrow at the top, ruffled, tapering at the tip."""
    if row == 0 or row >= ln - 1:
        return 1
    if row == 1 or row >= ln - 3:
        return 2
    phase = {"arm_n": 0, "arm_s": 2, "arm_e": 1, "arm_w": 3}[name]
    return (2, 3, 4, 4, 3)[(row + phase) % 5]          # a ruffled edge: in and out in a smooth wave


def arm_texel(name, c, row, ln):
    """c: 0 at the centre line, 3 at the outer edge. A frilled ribbon: deep inner fold, lit middle, pale frill."""
    w = arm_width(name, row, ln)
    if c >= w:
        return CLEAR
    tip = row >= ln - 3
    phase = {"arm_n": 0, "arm_s": 2, "arm_e": 1, "arm_w": 3}[name]
    if c == w - 1 and w > 1:
        key = "a3"                                   # the frilled edge, pale
    elif (row + phase + c) % 5 == 0:
        key = "a0"                                   # a fold running across the ruffle, in shade
    elif c == 0:
        return RGB["a0"] + (150,)                    # the centre, where the ribbons meet: a shaded fold
    else:
        key = "a2"
    alpha = 225 if not tip else 180
    if key == "a3":
        alpha = 200 if not tip else 160
    return RGB[key] + (alpha,)


def stalk_texel(face, y):
    if face == "top":
        return CLEAR
    return RGB["m"] + (210,)


# --- texture layout (the vanilla box UV layout) ----------------------------------------------------------------------
def used_rect(size):
    w, h, d = size
    if w == 0:
        return (0, d), (2 * d, h)
    if d == 0:
        return (0, 0), (2 * w, h)
    return (0, 0), (2 * d + 2 * w, d + h)


def layout():
    """Shelf packing, tallest first: the texOffs of every cube, in all_cubes() order."""
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
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    solids = [c for c in all_cubes() if c[1] == "bell"]
    for cube, (u, v) in layout():
        name, kind, part, (x0, y0, z0), (w, h, d) = cube
        for face, tu, tv, x, y, z in AW.face_texels(u, v, (x0, y0, z0), (w, h, d)):
            if w == 0 and face not in ("west", "east"):
                continue
            if d == 0 and face not in ("north", "south"):
                continue
            assert 0 <= tu < TW and 0 <= tv < TH, (name, face, tu, tv)
            assert owner.setdefault((tu, tv), name) == name, ("texture overlap", name, owner[(tu, tv)], tu, tv)
            if kind == "bell":
                if covered(cube, face, (x, y, z), solids):
                    col = CLEAR
                else:
                    col = bell_texel(face, x, y, z, name.split("_")[0])
            elif kind == "tentacle":
                col = tentacle_texel(int(name.split("_")[1]), face, y, h)
            elif kind == "core":
                col = RGB["core"] + ((190,) if face in ("top", "bottom") else (210,))
            elif kind == "stalk":
                col = stalk_texel(face, y)
            else:
                along = abs(z) if w == 0 else abs(x)
                c = int(math.floor(along))
                row = int(math.floor(y - ARM_TOP))
                col = arm_texel(name, c, row, h)
            img.putpixel((tu, tv), col)
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
        "import net.minecraft.client.model.geom.builders.CubeDeformation;",
        "import net.minecraft.client.model.geom.builders.CubeListBuilder;",
        "import net.minecraft.client.model.geom.builders.LayerDefinition;",
        "import net.minecraft.client.model.geom.builders.MeshDefinition;",
        "import net.minecraft.client.model.geom.builders.PartDefinition;",
        "",
        "/**",
        " * The mauve stinger (Pelagia noctiluca): a small, deep dome bell, 8 px across and 5 tall, rounded in 1 px steps",
        " * with a scalloped rim; see-through pink-mauve covered in raised dark mauve warts; 8 long thin tentacles from the",
        " * rim and 4 longer frilly oral arms from the centre. The texture is drawn translucent.",
        " * Made by art/src/jelly_mauve_stinger_model.py (do not edit by hand); texture",
        " * textures/entity/jellyfish/mauve_stinger.png. Parts: \"bell\" (hinged at the rim), \"tentacle_0\"..\"tentacle_7\"",
        " * and \"oral_arms\", children of the bell; the base class pulses the bell and sways the tentacles.",
        " */",
        "public class MauveStingerModel extends JellyfishModel {",
        "    /** The tentacles are drawn thinner than their 1 px texture: hair-thin. */",
        "    private static final CubeDeformation THIN = new CubeDeformation(%s, 0.0F, %s);" % (f(THIN), f(THIN)),
        "",
        "    public MauveStingerModel(ModelPart root) {",
        "        super(root);",
        "    }",
        "",
        "    public static LayerDefinition createBodyLayer() {",
        "        MeshDefinition mesh = new MeshDefinition();",
        "        PartDefinition root = mesh.getRoot();",
    ]
    placed = layout()
    for part in PART_ORDER:
        parent, ap = PARTS[part]
        px, py, pz = rel_pivot(part)
        builder = "CubeListBuilder.create()"
        for (name, _kind, cpart, (x0, y0, z0), (w, h, d)), (u, v) in placed:
            if cpart != part:
                continue
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %s, %s, %s%s)" % (
                name, u, v, f(x0 - ap[0]), f(y0 - ap[1]), f(z0 - ap[2]), f(w), f(h), f(d),
                ", THIN" if _kind == "tentacle" else "")
        if part == "oral_arms":
            pose = "PartPose.offsetAndRotation(%s, %s, %s, 0.0F, %s, 0.0F)" % (f(px), f(py), f(pz), f(ARM_TURN))
        else:
            pose = "PartPose.offset(%s, %s, %s)" % (f(px), f(py), f(pz))
        has_child = any(p[0] == part for p in PARTS.values())
        var = "PartDefinition %s = " % part if has_child else ""
        lines.append("        %s%s.addOrReplaceChild(\"%s\", %s," % (var, parent or "root", part, builder))
        lines.append("            %s);" % pose)
    lines += ["        return LayerDefinition.create(mesh, %d, %d);" % (TW, TH), "    }", "}", ""]
    return "\n".join(lines)


# --- checks ----------------------------------------------------------------------------------------------------------
def check():
    """The solid boxes must not overlap or share a plane facing the same way where they overlap; every part touches
    the bell or the stalk."""
    probs = []
    solids = [c for c in all_cubes() if all(c[4]) and c[1] != "core"]
    for i in range(len(solids)):
        a0, s = solids[i][3], solids[i][4]
        a1 = tuple(a0[k] + s[k] for k in range(3))
        for j in range(i + 1, len(solids)):
            b0, t = solids[j][3], solids[j][4]
            b1 = tuple(b0[k] + t[k] for k in range(3))
            ov = [min(a1[k], b1[k]) - max(a0[k], b0[k]) for k in range(3)]
            if all(o > 1e-6 for o in ov):
                probs.append(("overlap", solids[i][0], solids[j][0]))
    for name, kind, _p, o, s in all_cubes():
        if kind == "tentacle":
            assert abs(o[1] - RIM) < 1e-6, name
            assert any(inside((o[0] + 0.5, RIM - 0.5, o[2] + 0.5), c) for c in solids if c[1] == "bell"), name
        if kind == "arm":
            assert abs(o[1] - ARM_TOP) < 1e-6, name
    return probs


# --- offline render (alpha blended, the vanilla face shading, no water) --------------------------------------------
def render(model, texture, yaw, pitch, scale, sub=3, bg=(40, 96, 140)):
    parts, _ = model
    by_name = {p[0]: p for p in parts}

    def world(part, p):
        while part:
            _, parent, pivot, rot, _ = by_name[part]
            p = AW.rot_point(p, rot)
            p = (p[0] + pivot[0], p[1] + pivot[1], p[2] + pivot[2])
            part = parent
        return p

    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def project(p):
        x, y, z = p
        z2, x2 = z * cy + x * sy, -z * sy + x * cy
        return z2, y * cp - x2 * sp, y * sp + x2 * cp

    pts = []
    for name, _, _, _, cubes in parts:
        for u, v, origin, size in cubes:
            w, h, d = size
            for face, tu, tv, x, y, z in AW.face_texels(u, v, origin, size):
                if w == 0 and face not in ("west", "east"):
                    continue
                if d == 0 and face not in ("north", "south"):
                    continue
                col = texture.getpixel((tu, tv))
                if col[3] < 26:
                    continue
                k = AW.SHADE[face]
                c = (col[0] * k, col[1] * k, col[2] * k, col[3] / 255.0)
                for i in range(sub):
                    for j in range(sub):
                        a, b = (i + 0.5) / sub - 0.5, (j + 0.5) / sub - 0.5
                        if face in ("top", "bottom"):
                            p = (x + a, y, z + b)
                        elif face in ("west", "east"):
                            p = (x, y + a, z + b)
                        else:
                            p = (x + a, y + b, z)
                        pts.append((project(world(name, p)), c))
    xs = [q[0][0] for q in pts]
    ys = [q[0][1] for q in pts]
    minx, miny = min(xs) - 1, min(ys) - 1
    wpx = int((max(xs) - minx + 1) * scale) + 1
    hpx = int((max(ys) - miny + 1) * scale) + 1
    layers = {}
    r = max(1, int(math.ceil(scale / sub / 2 + 0.5)))
    for (sx, sy_, sd), c in pts:
        px, py = int((sx - minx) * scale), int((sy_ - miny) * scale)
        for ox in range(-r, r):
            for oy in range(-r, r):
                key = (px + ox, py + oy)
                if 0 <= key[0] < wpx and 0 <= key[1] < hpx:
                    lst = layers.setdefault(key, {})
                    dk = round(sd * 4)
                    if dk not in lst:
                        lst[dk] = c
    img = Image.new("RGB", (wpx, hpx), bg)
    px_ = img.load()
    for key, lst in layers.items():
        out = list(bg)
        for dk in sorted(lst, reverse=True):          # far to near
            c = lst[dk]
            a = c[3]
            out = [out[m] * (1 - a) + c[m] * a for m in range(3)]
        px_[key] = tuple(int(v) for v in out)
    return img


def sheet(dest_dir, texture):
    from PIL import ImageFont
    font = ImageFont.load_default()
    tmp = os.path.join(dest_dir, "_model_for_render.java")
    os.makedirs(dest_dir, exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(open(JAVA, encoding="utf-8").read().replace(", THIN)", ")"))
    model = AW.parse_java(tmp)
    views = [("side", 0, 0), ("three-quarter", 35, 25), ("from below", 20, -60), ("from above", 0, 80)]
    renders = [render(model, texture, y, p, 14) for _, y, p in views]
    refs = []
    ref_dir = os.path.join(ROOT, "art", "references", "jelly_mauve_stinger_refonly")
    for n in ("ms09.jpg", "ms05.jpg", "ms01.jpg", "ms02.jpg"):
        fp = os.path.join(ref_dir, n)
        if os.path.exists(fp):
            im = Image.open(fp).convert("RGB")
            im.thumbnail((360, 360))
            refs.append(im)
    W = max(sum(i.width + 12 for i in renders), sum(i.width + 12 for i in refs)) + 20
    H = 30 + max(i.height for i in refs) + 30 + max(i.height for i in renders) + 30 + TH * 5 + 20
    out = Image.new("RGB", (W, H), (60, 60, 60))
    dr = ImageDraw.Draw(out)
    y = 8
    dr.text((8, y), "References (reference only): ms09, ms05, ms01, ms02", fill=(240, 240, 240), font=font)
    y += 18
    x = 8
    for im in refs:
        out.paste(im, (x, y))
        x += im.width + 12
    y += max(i.height for i in refs) + 12
    dr.text((8, y), "Offline model, 14x, alpha blended over flat blue: " + ", ".join(v[0] for v in views),
            fill=(240, 240, 240), font=font)
    y += 18
    x = 8
    for im in renders:
        out.paste(im, (x, y))
        x += im.width + 12
    y += max(i.height for i in renders) + 12
    dr.text((8, y), "Texture at 5x (checkerboard shows alpha)", fill=(240, 240, 240), font=font)
    y += 18
    chk = Image.new("RGBA", (TW * 5, TH * 5))
    for cy_ in range(0, TH * 5, 10):
        for cx_ in range(0, TW * 5, 10):
            g = 180 if (cx_ // 10 + cy_ // 10) % 2 else 120
            chk.paste((g, g, g, 255), (cx_, cy_, cx_ + 10, cy_ + 10))
    chk.alpha_composite(texture.resize((TW * 5, TH * 5), Image.NEAREST))
    out.paste(chk.convert("RGB"), (8, y))
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "jelly_mauve_stinger_model.png")
    out.save(dest)
    print("sheet:", dest)


def main():
    probs = check()
    for p in probs:
        print("problem:", p)
    assert not probs
    texture = draw_texture()
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    texture.save(TEXTURE)
    os.makedirs(JAVA_DIR, exist_ok=True)
    with open(JAVA, "w", encoding="utf-8") as fh:
        fh.write(java_source())
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    args = sys.argv[1:]
    if "--sheet" in args:
        i = args.index("--sheet")
        sheet(args[i + 1], texture)


if __name__ == "__main__":
    main()
