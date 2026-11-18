"""The cerna (dusky grouper, Epinephelus marginatus) as a swimming mob: its 3D model and its texture.

Drawn from the reference photos in art/references/fish_cerna_refonly/ (list.tsv). What makes it a cerna:
  - the bulkiest fish of the set: a big, heavy, deep and thick body, deepest just behind a big head,
  - a large mouth, rounded by single steps, with the lower jaw jutting past the upper lip, pale lips,
  - a small eye high on the head, just under the profile, and a gill cover with a soft rim,
  - one long dorsal fin from above the gill cover almost to the tail: low with dark spines in front, longer behind,
  - a rounded tail (not forked), a rounded anal fin, broad rounded pectoral fins on the flanks; every fin has a solid
    pale rim,
  - a mottled reddish-brown body, dark along the back, warm on the flanks, light toward the belly, with irregular
    pale blotches (each a lit pixel over a shaded one, like the icon's).
The palette is the accepted item icon's (art/src/fish_cerna_icon.py PAL), each colour lifted one step toward a warm
pale tan, because under water the game greys and darkens everything. No face is a flat fill: every body texel is
shifted one shade lighter or darker at random (a fixed hash, so reruns are byte-identical).

Size: the hitbox is 0.9 x 0.6 blocks (14.4 x 9.6 model pixels). Vanilla's models run about 1.9 to 2.2 times their
hitbox width in length (cod 15 px on 8, salmon 25 px on 11.2), so the cerna is 29 px long (24 of body from the tip of
the lower jaw, 5 of tail), 10 px deep (12 with the dorsal fin) and 6 px thick. Body depth to body length is 10 to 24
(0.42), against the tonn's 10 to 26 (0.38), the sardina's 3 to 11 (0.27) and the lampuka's 7 to about 30 (0.23);
thickness to depth is 0.6 (the tonn's and the sardina's slimmer). The cerna's depth runs right up to the big head and
down to a short, thick tail stalk, so it is the heaviest of the four.
One texture pixel per model pixel, like vanilla's fish.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body" and a "tail_fin" that sways like vanilla cod's. The body is rigid, like cod's: the cerna lurks and moves
slowly.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/CernaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/cerna.png    (64 x 64)
Also writes offline previews (side, top, three-quarter, beside vanilla cod and salmon) to the scratch folder given
with --preview DIR, and the compare sheet with --sheet SCREENSHOT_DIR.

Run:  art/.venv/bin/python art/src/fish_cerna_model.py [--preview DIR] [--sheet SCREENSHOT_DIR]
"""
import glob
import math
import os
import sys
import zipfile

from PIL import Image, ImageDraw

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "CernaModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "cerna.png")
TW, TH = 64, 64


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


def lift(c, k=0.10):
    """One step lighter than the icon, toward a warm pale tan: under water the game greys and darkens every colour."""
    t = (242, 220, 192)
    return tuple(int(round(c[i] + (t[i] - c[i]) * k)) for i in range(3)) + (255,)


# The palette of the accepted cerna item icon (art/src/fish_cerna_icon.py PAL), each lifted one step for the water.
ICON = {
    "h": "#c8956a",                                                 # the brightest light
    "1": "#b27a55", "2": "#a66c4a", "3": "#93593f", "4": "#7a4434", "5": "#5e3228",   # the body, light to dark
    "k": "#7a4632",                                                 # rim: the gill cover's edge
    "C": "#ccac88", "c": "#a8866a",                                 # pale blotches: in the light, partly shaded
    "L": "#b07a5e", "l": "#8a5844",                                 # lips and jutting lower jaw: lit, shaded
    "M": "#4e2a1e",                                                 # the corner of the mouth (brown, not black)
    "D": "#5a3224", "f": "#8a5440",                                 # dorsal fin: dark spines, lit membrane
    "A": "#5a3426",                                                 # pectoral and anal fins
    "T": "#9a5e48", "t": "#7a4838", "u": "#4a2a20",                 # the rounded tail: lit, mid, shaded rim
}
PAL = {k: lift(hexc(v), 0.14) for k, v in ICON.items()}
# the blotches lifted further, so the pale pattern still stands out from the mottled body in the blue of the water
PAL["C"], PAL["c"] = lift(hexc(ICON["C"]), 0.4), lift(hexc(ICON["c"]), 0.3)
PAL["E"] = hexc("#0a0a0a")      # the small eye, high on the head (the only black, not lifted)
PAL["."] = (0, 0, 0, 0)
CLEAR = PAL["."]
RAMP = [PAL[k] for k in "h12345"]   # body shades, 0 lightest to 5 darkest


# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), (xRot, yRot, zRot)). Cubes: (name, part, (U, V) top-left of
# the used texture area, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to
# tail (+).
PARTS = {
    "body": (None, (0.0, 20.0, 0.0), (0.0, 0.0, 0.0)),
    "tail_fin": (None, (0.0, 19.0, 11.0), (0.0, 0.0, 0.0)),
    # the pectoral fins: upright fans hinged on the flank behind the gill cover, their back edges turned out
    "right_fin": (None, (-3.0, 19.0, -5.0), (0.0, -0.4, 0.0)),
    "left_fin": (None, (3.0, 19.0, -5.0), (0.0, 0.4, 0.0)),
}
CUBES = [
    # the mouth, rounded by stepping: the jutting lower jaw (a narrow tip, then the full jaw), the upper lip (a narrow
    # tip, then the snout), so the front of the face narrows and drops in single steps instead of ending in a block
    ("jaw_tip", "body", (54, 21), (-1.0, 21.0, -13.0), (2, 2, 1)),
    ("jaw", "body", (46, 17), (-1.5, 21.0, -12.0), (3, 2, 2)),
    ("lip_tip", "body", (54, 24), (-1.0, 19.0, -12.0), (2, 2, 1)),
    ("snout", "body", (46, 21), (-1.5, 18.0, -11.0), (3, 3, 1)),
    # the big head (the forehead, then the cheeks and gill cover), the deep trunk, the rear, the short thick stalk
    ("head_front", "body", (0, 17), (-2.0, 16.0, -10.0), (4, 7, 2)),
    ("head", "body", (26, 0), (-2.5, 15.0, -8.0), (5, 8, 3)),
    ("trunk", "body", (0, 0), (-3.0, 14.0, -5.0), (6, 10, 7)),
    ("rear", "body", (42, 0), (-2.5, 15.0, 2.0), (5, 8, 4)),
    ("stalk", "body", (12, 17), (-2.0, 16.0, 6.0), (4, 6, 3)),
    ("stalk2", "body", (26, 17), (-1.5, 17.0, 9.0), (3, 4, 2)),
    # the long dorsal fin and the rounded anal fin, flat planes down the middle
    ("dorsal", "body", (0, 30), (0.0, 12.0, -7.0), (0, 4, 16)),
    ("anal", "body", (0, 26), (0.0, 22.0, 3.0), (0, 3, 5)),
    # the rounded tail
    ("caudal", "tail_fin", (36, 17), (0.0, 15.0, 11.0), (0, 9, 5)),
    # the pectoral fins
    ("pec_r", "right_fin", (10, 26), (-3.0, 18.0, -5.0), (0, 3, 4)),
    ("pec_l", "left_fin", (18, 26), (3.0, 18.0, -5.0), (0, 3, 4)),
]

# The side of the fish: the shade of each row (0 lightest .. 5 darkest; dark back, warm flank, light belly), then the
# features painted over it, one character per pixel: columns z -13..10, rows y 14..23 ('.' = plain mottled body).
SIDE_Z0, SIDE_Y0 = -13, 14
ROW_SHADE = {14: 4, 15: 4, 16: 3, 17: 3, 18: 2, 19: 2, 20: 2, 21: 1, 22: 1, 23: 0}
FEATURES = [
    # z: 1   1  1                             1 1
    #    3   2  1 0 9 8 7 6 5 4 3 2 1 0 1 2 3 4 5 6 7 8 9 0
    "......." "....Cc.." ".........",   # y 14
    "......." "...cCC.." ".........",   # y 15
    "......." "..CC...." ".........",   # y 16
    "....E.." "k..c...." "CC.......",   # y 17
    "......." "k...CC.." ".c..cC...",   # y 18
    "....C.." "k...cC.." ".CC..c...",   # y 19
    ".LLlc.k" "..C....." "..c......",   # y 20
    "LLLM..k" "..c...CC" "......c..",   # y 21
    "lll.l.." "......c." ".........",   # y 22
    "......." "........" ".........",   # y 23
]

# Fin outlines, as text: one character per pixel; colours from PAL. Every fin has a solid rim.
# the long dorsal fin, rows y 12..15, columns z -7..8: low and spiny in front (dark spines), longer behind
DORSAL_Z0, DORSAL_Y0 = -7, 12
DORSAL = [
    "..cccccccccc....",
    ".cDfDfDfDffffc..",
    "cf.......ffffc..",
    ".............fc.",
]
# the rounded tail, rows y 15..23, columns z 11..15: lit above, darker below, a pale trailing rim
CAUDAL_Z0, CAUDAL_Y0 = 11, 15
CAUDAL = [
    "..Tc.",
    ".TTtc",
    "TTTtc",
    "TTttc",
    "ttttc",
    "ttttc",
    "tttuc",
    ".ttuc",
    "..uc.",
]
# the rounded anal fin, rows y 22..24, columns z 3..7 (only what hangs below the rear and the stalk shows)
ANAL_Z0, ANAL_Y0 = 3, 22
ANAL = [
    "...Ac",
    "AAAAc",
    ".ccc.",
]
# the pectoral fin, rows y 18..20, columns z -5..-2 (before it is turned out): a rounded fan, a pale back edge
PEC_Z0, PEC_Y0 = -5, 18
PECTORAL = [
    "Afc.",
    "AAfc",
    "Acc.",
]


def hash01(*vals):
    """A repeatable pseudo-random number in [0, 1) from integers (no floating-point maths, so every run is the same)."""
    h = 2166136261
    for v in vals:
        h = ((h ^ (v & 0xffffffff)) * 16777619) & 0xffffffff
    h ^= h >> 13
    h = (h * 0x5bd1e995) & 0xffffffff
    h ^= h >> 15
    return h / 4294967296.0


def mottle(shade, *key):
    """Shift a shade one step lighter or darker at random, so no face is a flat fill."""
    r = hash01(*key)
    if r < 0.16:
        shade -= 1
    elif r > 0.82:
        shade += 1
    return RAMP[max(0, min(5, shade))]


FACE_SALT = {"top": 1, "bottom": 2, "north": 3, "south": 4, "west": 5, "east": 6}


def side_colour(y, z, face, x):
    yi, zi = int(math.floor(y)), int(math.floor(z))
    ch = FEATURES[yi - SIDE_Y0][zi - SIDE_Z0]
    if ch != ".":
        return PAL[ch]
    return mottle(ROW_SHADE[yi], FACE_SALT[face], int(math.floor(x * 2)), yi, zi)


def body_colour(name, face, x, y, z, x0, y0, z0, w, h, d):
    """The colour of one texel of a body section, from where it sits on the fish."""
    zi, xi = int(math.floor(z)), int(math.floor(x * 2))
    if face == "top":
        if name in ("jaw_tip", "jaw"):
            return PAL["L"]
        # the back seen from above: darkest along the spine, mottled, with a few pale blotches
        r = hash01(7, xi, zi)
        if name in ("head", "trunk", "rear") and r > 0.88:
            return PAL["C"] if r > 0.95 else PAL["c"]
        centre = abs(x) < 1.0
        return mottle(5 if centre else 4, 1, xi, zi)
    if face == "bottom":
        if name in ("jaw_tip", "jaw"):
            return PAL["l"]
        return mottle(0, 2, xi, zi)
    if face == "north":
        return side_colour(y, z0, face, x)
    if face == "south":
        return side_colour(y, z0 + d - 1, face, x)
    return side_colour(y, z, face, x)


def fin_colour(name, x, y, z):
    """The colour of one fin texel, or CLEAR outside the fin's outline."""
    grids = {"dorsal": (DORSAL, DORSAL_Y0, DORSAL_Z0), "anal": (ANAL, ANAL_Y0, ANAL_Z0),
             "caudal": (CAUDAL, CAUDAL_Y0, CAUDAL_Z0), "pec_r": (PECTORAL, PEC_Y0, PEC_Z0),
             "pec_l": (PECTORAL, PEC_Y0, PEC_Z0)}
    grid, gy, gz = grids[name]
    return PAL[grid[int(math.floor(y)) - gy][int(math.floor(z)) - gz]]


# --- texture layout (the vanilla box UV layout) ----------------------------------------------------------------------
def tex_offset(cube):
    """texOffs for a cube whose used texture area starts at (U, V): planes leave out the faces they don't have."""
    _, _, (U, V), _, (w, h, d) = cube
    if w == 0:
        return U, V - d
    if h == 0:
        return U - d, V
    return U, V


def face_texels(cube):
    """Every texel of every face: (face, u, v, x, y, z), with (x, y, z) the texel's centre on the model, absolute.
    The mapping follows ModelPart.Cube: top (u+d, v), bottom (u+d+w, v), west (u, v+d), north (u+d, v+d),
    east (u+d+w, v+d), south (u+2d+w, v+d)."""
    _, _, _, (x0, y0, z0), (w, h, d) = cube
    u, v = tex_offset(cube)
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


def draw_texture():
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in CUBES:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if w == 0 or h == 0:
                col = fin_colour(name, x, y, z)
            else:
                col = body_colour(name, face, x, y, z, x0, y0, z0, w, h, d)
            img.putpixel((u, v), col)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def f(v):
    s = ("%.4f" % v).rstrip("0")
    if s.endswith("."):
        s += "0"
    if s == "-0.0":
        s = "0.0"
    return s + "F"


def write_java():
    lines = []
    for part in ("body", "tail_fin", "right_fin", "left_fin"):
        parent, (px, py, pz), rot = PARTS[part]
        builder = "CubeListBuilder.create()"
        for cube in [c for c in CUBES if c[1] == part]:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = tex_offset(cube)
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %d.0F, %d.0F, %d.0F)" % (
                name, u, v, f(x0 - px), f(y0 - py), f(z0 - pz), w, h, d)
        if any(rot):
            pose = "PartPose.offsetAndRotation(%s, %s, %s, %s, %s, %s)" % (
                f(px), f(py), f(pz), f(rot[0]), f(rot[1]), f(rot[2]))
        else:
            pose = "PartPose.offset(%s, %s, %s)" % (f(px), f(py), f(pz))
        lines.append("        root.addOrReplaceChild(\"%s\", %s,\n            %s);" % (part, builder, pose))
    body = "\n".join(lines)
    src = """package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The cerna (dusky grouper): big, heavy and deep, mottled reddish-brown with pale blotches and a light belly, a big
 * head with a rounded mouth, a jutting lower jaw and a small eye high up, one long dorsal fin, broad rounded pectoral
 * fins and a rounded tail that sways as it swims. 29 px long, 10 px deep, 6 px thick, head toward -z, the ground at y 24.
 * Made by art/src/fish_cerna_model.py (don't edit by hand). Texture: textures/entity/fish/cerna.png (64 x 64).
 */
public class CernaModel extends FishModel {
    public CernaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
%s
        return LayerDefinition.create(mesh, %d, %d);
    }
}
""" % (body, TW, TH)
    with open(JAVA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src)


# --- offline previews: an orthographic texel splatter with vanilla-like face shading ----------------------------------
SHADE = {"top": 1.0, "bottom": 0.5, "north": 0.8, "south": 0.8, "west": 0.6, "east": 0.6}


def rotate(p, rot):
    """ModelPart order: z, then y, then x (applied to the point in that order)."""
    x, y, z = p
    rx, ry, rz = rot
    if rz:
        c, s = math.cos(rz), math.sin(rz)
        x, y = x * c - y * s, x * s + y * c
    if ry:
        c, s = math.cos(ry), math.sin(ry)
        x, z = x * c + z * s, -x * s + z * c
    if rx:
        c, s = math.cos(rx), math.sin(rx)
        y, z = y * c - z * s, y * s + z * c
    return (x, y, z)


def to_world(parts, part, p):
    """Absolute rest position -> posed position (rotations about each part's pivot, parents last)."""
    while part:
        parent, pivot, rot = parts[part]
        if isinstance(rot, float):
            rot = (0.0, 0.0, rot)
        if any(rot):
            rel = (p[0] - pivot[0], p[1] - pivot[1], p[2] - pivot[2])
            rel = rotate(rel, rot)
            p = (rel[0] + pivot[0], rel[1] + pivot[1], rel[2] + pivot[2])
        part = parent
    return p


def render(cubes, parts, texture, view, scale, sub=4):
    """Draw a model from 'side' (from -x, head left), 'top' (from above, head left) or 'three' (front three-quarter).
    Returns an RGBA image cropped to the fish, with `scale` screen pixels per model pixel."""
    yaw, pitch = {"side": (0.0, 0.0), "top": (0.0, 90.0), "three": (35.0, 25.0)}[view]
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def project(p):
        x, y, z = p
        z2, x2 = z * cy + x * sy, -z * sy + x * cy
        y3, d3 = y * cp - x2 * sp, y * sp + x2 * cp
        return z2, y3, d3

    pts = []
    for cube in cubes:
        name, part, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in face_texels(cube):
            col = texture.getpixel((u % texture.size[0], v % texture.size[1]))
            if col[3] < 128:
                continue
            k = SHADE[face]
            col = (int(col[0] * k), int(col[1] * k), int(col[2] * k))
            for i in range(sub):
                for j in range(sub):
                    a, b = (i + 0.5) / sub - 0.5, (j + 0.5) / sub - 0.5
                    if face in ("top", "bottom"):
                        p = (x + a, y, z + b)
                    elif face in ("west", "east"):
                        p = (x, y + a, z + b)
                    else:
                        p = (x + a, y + b, z)
                    pts.append((project(to_world(parts, part, p)), col))
    xs = [q[0][0] for q in pts]
    ys = [q[0][1] for q in pts]
    minx, miny = min(xs) - 1, min(ys) - 1
    wpx = int((max(xs) - minx + 1) * scale) + 1
    hpx = int((max(ys) - miny + 1) * scale) + 1
    img = Image.new("RGBA", (wpx, hpx), CLEAR)
    depth = {}
    r = max(1, int(math.ceil(scale / sub / 2 + 0.5)))
    for (sx, sy_, sd), col in pts:
        px, py = int((sx - minx) * scale), int((sy_ - miny) * scale)
        for ox in range(-r, r):
            for oy in range(-r, r):
                key = (px + ox, py + oy)
                if 0 <= key[0] < wpx and 0 <= key[1] < hpx and sd < depth.get(key, 1e9):
                    depth[key] = sd
                    img.putpixel(key, col + (255,))
    return img


# vanilla cod and salmon, as measured from the 26.3 client (CodModel, SalmonModel), for scale in the previews
COD_PARTS = {"p": (None, (0, 0, 0), 0.0), "rf": (None, (-1, 23, 0), -0.7854), "lf": (None, (1, 23, 0), 0.7854)}
COD_CUBES = [
    ("body", "p", None, (-1, 20, 0), (2, 4, 7), (0, 0)),
    ("head", "p", None, (-1, 20, -3), (2, 4, 3), (11, 0)),
    ("nose", "p", None, (-1, 20, -4), (2, 3, 1), (0, 0)),
    ("tail", "p", None, (0, 20, 7), (0, 4, 4), (22, 3)),
    ("top", "p", None, (0, 19, -1), (0, 1, 6), (20, -6)),
    ("rf", "rf", None, (-3, 23, -1), (2, 0, 2), (22, 1)),
    ("lf", "lf", None, (1, 23, -1), (2, 0, 2), (22, 4)),
]
SAL_PARTS = {"p": (None, (0, 0, 0), 0.0), "rf": (None, (-1.5, 21.5, -7.2), -0.7854),
             "lf": (None, (1.5, 21.5, -7.2), 0.7854)}
SAL_CUBES = [
    ("front", "p", None, (-1.5, 17.5, -7.2), (3, 5, 8), (0, 0)),
    ("back", "p", None, (-1.5, 17.5, 0.8), (3, 5, 8), (0, 13)),
    ("head", "p", None, (-1, 18, -10.2), (2, 4, 3), (22, 0)),
    ("tail", "p", None, (0, 17.5, 8.8), (0, 5, 6), (20, 10)),
    ("topf", "p", None, (0, 15.5, -2.2), (0, 2, 3), (2, 1)),
    ("topb", "p", None, (0, 15.5, -0.2), (0, 2, 4), (0, 2)),
    ("rf", "rf", None, (-3.5, 21.5, -7.2), (2, 0, 2), (-4, 0)),
    ("lf", "lf", None, (1.5, 21.5, -7.2), (2, 0, 2), (0, 0)),
]


def vanilla_cubes(spec):
    """Vanilla cubes given with their real texOffs: convert to this script's (U, V) form."""
    out = []
    for name, part, _, pos, (w, h, d), (u, v) in spec:
        if w == 0:
            U, V = u, v + d
        elif h == 0:
            U, V = u + d, v
        else:
            U, V = u, v
        out.append((name, part, (U, V), pos, (w, h, d)))
    return out


def vanilla_texture(name):
    jar_dir = os.path.join(ROOT, ".art-runs")
    for jar in sorted(glob.glob(os.path.join(jar_dir, "*", ".gradle", "loom-cache", "minecraftMaven", "net", "minecraft",
                                             "minecraft-merged-*", "26.3", "*.jar"))):
        with zipfile.ZipFile(jar) as z:
            try:
                with z.open("assets/minecraft/textures/entity/fish/%s.png" % name) as fh:
                    return Image.open(fh).convert("RGBA").copy()
            except KeyError:
                continue
    return None


def previews(out_dir, texture):
    os.makedirs(out_dir, exist_ok=True)
    out = {}
    for view in ("side", "top", "three"):
        img = render(CUBES, PARTS, texture, view, 16)
        img.save(os.path.join(out_dir, "cerna_%s16.png" % view))
        out[view] = img
    cod, sal = vanilla_texture("cod"), vanilla_texture("salmon")
    if cod and sal:
        row = [render(CUBES, PARTS, texture, "side", 8),
               render(vanilla_cubes(COD_CUBES), COD_PARTS, cod, "side", 8),
               render(vanilla_cubes(SAL_CUBES), SAL_PARTS, sal, "side", 8)]
        out["scale"] = row
        im = Image.new("RGBA", (sum(i.width for i in row) + 40, max(i.height for i in row)), (72, 72, 72, 255))
        x = 0
        for i in row:
            im.paste(i, (x, im.height - i.height), i)
            x += i.width + 20
        im.save(os.path.join(out_dir, "cerna_scale8.png"))
    return out


# --- the compare sheet ------------------------------------------------------------------------------------------------
def sheet(shots_dir, texture, prev_dir):
    from PIL import ImageFont
    pv = previews(prev_dir, texture)
    font = ImageFont.load_default()
    W = 1800
    blocks = []

    def title(t):
        im = Image.new("RGBA", (W, 26), (40, 40, 40, 255))
        ImageDraw.Draw(im).text((8, 6), t, fill=(240, 240, 240, 255), font=font)
        blocks.append(im)

    def row(images, h=None, gap=12, align_bottom=False):
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images)
        im = Image.new("RGBA", (W, hh + 8), (72, 72, 72, 255))
        x = 8
        for i in images:
            if x + i.width > W:
                break
            im.paste(i, (x, 4 + (hh - i.height if align_bottom else 0)), i)
            x += i.width + gap
        blocks.append(im)

    ref_dir = os.path.join(ROOT, "art", "references", "fish_cerna_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("side_1.jpg", "side_2.jpg", "drawing_1.jpg", "side_4.jpg", "head_1.jpg", "fins_1.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    title("References (reference only): side views in water, the jutting jaw and small high eye, the fins and blotches")
    row(refs[:3], h=260)
    row(refs[3:], h=260)
    title("Offline model, 16x: side, three-quarter, top (vanilla face shading only)")
    row([pv["side"], pv["three"]])
    row([pv["top"]])
    if "scale" in pv:
        title("Same scale, 8x: cerna (hitbox 0.9 x 0.6), vanilla cod (0.5 x 0.3), vanilla salmon (0.7 x 0.4)")
        row(pv["scale"], align_bottom=True, gap=40)
    van = [t for t in (vanilla_texture("cod"), vanilla_texture("salmon")) if t]
    items = [Image.open(os.path.join(RES, "textures", "item", n)).convert("RGBA")
             for n in ("cerna.png", "cerna_bucket.png", "cerna_spawn_egg.png")
             if os.path.exists(os.path.join(RES, "textures", "item", n))]
    title("Texture at 4x and 1x: cerna (64 x 64); vanilla cod and salmon (32 x 32) at 8x; the accepted items below")
    row([texture.resize((TW * 4, TH * 4), Image.NEAREST), texture]
        + [t.resize((t.width * 8, t.height * 8), Image.NEAREST) for t in van] + van
        )
    title("The accepted cerna item icon, bucket and spawn egg (8x), beside the model (side, 8x)")
    row([i.resize((128, 128), Image.NEAREST) for i in items] + [render(CUBES, PARTS, texture, "side", 8)],
        align_bottom=True, gap=24)
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        names = ("fish-cerna-side", "fish-cerna-three-quarter", "fish-cerna-top", "fish-cerna-on-land",
                 "fish-cerna-beside-cod")
        imgs = [shot(n) for n in names]
        imgs = [i for i in imgs if i]
        if imgs:
            title("In the game: the cerna alone (side close-up, three-quarter, top, on land), and beside vanilla cod")
            row(imgs[:3], h=330)
            row(imgs[3:], h=330)
            title("The same, cropped to the fish (beside cod: cerna left, cod right)")
            boxes = {"fish-cerna-beside-cod": (0.04, 0.2, 0.96, 0.7)}
            crops = []
            for n, i in zip([n for n in names if shot(n)], imgs):
                fx = boxes.get(n, (0.2, 0.2, 0.8, 0.7))
                box = (int(i.width * fx[0]), int(i.height * fx[1]), int(i.width * fx[2]), int(i.height * fx[3]))
                k = 580.0 / (box[2] - box[0])
                crops.append(i.crop(box).resize((580, int((box[3] - box[1]) * k)), Image.NEAREST))
            row(crops[:3])
            row(crops[3:])
        title("In the game: the shared tank (awrata, lampuka, cerna, ...), and on land")
        imgs = [shot(n) for n in ("fish-03-tank-awrata-lampuka-cerna", "fish-01-tank-all", "fish-06-on-land")]
        imgs = [i for i in imgs if i]
        if imgs:
            row(imgs, h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_cerna_model.png")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    texture = draw_texture()
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    texture.save(TEXTURE)
    write_java()
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    args = sys.argv[1:]
    prev = args[args.index("--preview") + 1] if "--preview" in args else None
    if "--sheet" in args:
        sheet(args[args.index("--sheet") + 1], texture, prev or os.path.join(ROOT, "art", "candidates", "tmp_cerna"))
    elif prev:
        previews(prev, texture)
        print("previews in", prev)


if __name__ == "__main__":
    main()
