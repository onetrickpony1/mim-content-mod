"""The lampuka (dolphinfish, Coryphaena hippurus) as a swimming mob: its 3D model and its texture.

Drawn from the reference photos in art/references/fish_lampuka_refonly/ (list.tsv): a young autumn fish, the size
Malta lands from August to December. What makes it a lampuka:
  - a steep, blunt forehead (stepped down from the back to the snout in three steps),
  - one long dark blue-green dorsal fin from just behind the head almost to the tail,
  - a long anal fin under the back half,
  - a deeply forked tail with long slim lobes, wider than the body is deep,
  - a tall, narrow body tapering to a slim tail stalk,
  - gold flanks under a blue-green back, small dark spots, a pale belly, dark sickle pectoral fins.
The palette is the accepted item icon's (textures/item/lampuka.png).

Size: the hitbox is 1.0 x 0.45 blocks (16 x 7.2 model pixels). Vanilla's models run about 2 to 2.2 times their hitbox
width in length (cod 15 px on 8, salmon 25 px on 11.2), so the lampuka is 35 px long and 7 px deep (9 with fins).
One texture pixel per model pixel, like vanilla's fish.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body", the back half in "tail" (it sways gently, like vanilla salmon's back) with "tail_fin" inside it.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/LampukaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/lampuka.png    (64 x 32)
Also writes offline previews (side, top, three-quarter, beside vanilla cod and salmon) to the scratch folder given
with --preview DIR, and the compare sheet with --sheet SCREENSHOT_DIR.

Run:  art/.venv/bin/python art/src/fish_lampuka_model.py [--preview DIR] [--sheet SCREENSHOT_DIR]
"""
import math
import os
import sys
import zlib

from PIL import Image, ImageDraw

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "LampukaModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "lampuka.png")
TW, TH = 64, 32


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# The icon's palette (textures/item/lampuka.png), plus two in-betweens.
BACK_DARK = hexc("#1c5158")   # the dorsal fin, the darkest back
BACK = hexc("#2f7a68")        # the blue-green back
TEAL = hexc("#5cbc9e")        # upper flank
MINT = hexc("#9ae2bc")        # the shine on the upper flank
LIME = hexc("#a8c03c")        # where green turns to gold
GOLD = hexc("#e6c12c")        # the flank
GOLD_D = hexc("#a67c18")      # gill cover edge, shade
BROWN = hexc("#786024")       # the mouth
OLIVE = hexc("#c4b43a")       # the fins
OLIVE_D = hexc("#5e5a1c")     # fin edges
SPOT = hexc("#26382c")        # dark spots on the gold
SPOT_B = hexc("#2c4a48")      # dark blue spots on the green
BELLY = hexc("#f6eecb")       # the belly
PALE = hexc("#eedb84")        # lower flank, gold paling to the belly (between GOLD and BELLY)
EYE = hexc("#101010")
CLEAR = (0, 0, 0, 0)


def noise(*key):
    """A fixed pseudo-random number in [0, 1) for a texel, so every run draws the same texture."""
    return (zlib.crc32(repr(key).encode()) & 0xFFFFFF) / float(0x1000000)


# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), zRot). Cubes: (name, part, (U, V) top-left of the used texture
# area, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
PARTS = {
    "body": (None, (0.0, 20.0, 0.0), 0.0),
    "tail": (None, (0.0, 20.0, -3.0), 0.0),
    "tail_fin": ("tail", (0.0, 20.0, 12.0), 0.0),
    "right_fin": (None, (-1.5, 21.0, -12.0), -0.6),
    "left_fin": (None, (1.5, 21.0, -12.0), 0.6),
}
CUBES = [
    # the front half, which holds still: snout, head, trunk and the front of the dorsal fin
    ("snout", "body", (56, 0), (-1.0, 19.0, -17.0), (2, 4, 1)),
    ("head", "body", (0, 17), (-1.5, 17.0, -16.0), (3, 6, 3)),
    ("trunk", "body", (0, 0), (-1.5, 16.0, -13.0), (3, 7, 10)),
    ("dorsal_front", "body", (12, 21), (0.0, 13.0, -13.0), (0, 3, 10)),
    # the back half, which sways: narrowing body, the rest of the dorsal fin, the anal fin
    ("mid", "tail", (26, 0), (-1.0, 17.0, -3.0), (2, 6, 6)),
    ("rear", "tail", (42, 0), (-1.0, 18.0, 3.0), (2, 4, 5)),
    ("stalk", "tail", (42, 9), (-0.5, 19.0, 8.0), (1, 2, 4)),
    ("dorsal_back", "tail", (12, 17), (0.0, 15.0, -3.0), (0, 4, 13)),
    ("anal", "tail", (38, 17), (0.0, 22.0, -1.0), (0, 2, 9)),
    # the forked tail
    ("caudal", "tail_fin", (38, 20), (0.0, 16.0, 12.0), (0, 8, 6)),
    # the pectoral fins, spread down and out like vanilla cod's
    ("pec_r", "right_fin", (50, 20), (-3.5, 21.0, -12.0), (2, 0, 4)),
    ("pec_l", "left_fin", (54, 20), (1.5, 21.0, -12.0), (2, 0, 4)),
]

# Each body section's side rows, top to bottom: the back, then green to gold to pale.
SECTION_ROWS = {
    "snout": [TEAL, GOLD, PALE, PALE],
    "head": [BACK, TEAL, GOLD, PALE, PALE, PALE],
    "trunk": [BACK, TEAL, GOLD, GOLD, PALE, PALE, PALE],
    "mid": [BACK, TEAL, GOLD, PALE, PALE, PALE],
    "rear": [BACK, TEAL, GOLD, PALE],
    "stalk": [BACK, OLIVE],
}

# Fin outlines, by absolute z (column) and y (row), as text: one character per pixel.
#   o fin colour, d dark edge, l light base, . clear
# dorsal fin: the topmost row each column reaches (it runs down into the body, hidden there)
DORSAL_TOP = {}
for _z in range(-13, 10):
    if _z == -13:
        DORSAL_TOP[_z] = 15     # rises from just behind the head
    elif _z <= -4:
        DORSAL_TOP[_z] = 14     # 2 px above the trunk (top 16)
    elif _z <= 2:
        DORSAL_TOP[_z] = 15     # 2 px above the narrower middle (top 17)
    elif _z <= 5:
        DORSAL_TOP[_z] = 16     # 2 px above the rear (top 18)
    elif _z <= 7:
        DORSAL_TOP[_z] = 17     # 1 px, tapering
    else:
        DORSAL_TOP[_z] = 18     # 1 px over the tail stalk (top 19)
# anal fin: the lowest row each column reaches, under the back half
ANAL_BOTTOM = {}
for _z in range(-1, 8):
    if _z <= 5:
        ANAL_BOTTOM[_z] = 23    # 1 px under the middle (bottom 23), 2 px under the rear (bottom 22)
    else:
        ANAL_BOTTOM[_z] = 22    # 1 px, tapering toward the tail
# the forked tail, rows y 16..23, columns z 12..17 (z 12 against the tail stalk)
CAUDAL = [
    "....od",
    "...od.",
    ".ooo..",
    "loo...",
    "loo...",
    ".ooo..",
    "...od.",
    "....od",
]
# the pectoral fin, columns x (out from the body), rows z (front to back)
PECTORAL = [
    "lo",
    "oo",
    "oo",
    ".d",
]


def body_colour(name, face, x, y, z, x0, y0, z0, w, h, d):
    """The colour of one texel of a body section, from where it sits on the fish."""
    rows = SECTION_ROWS[name]
    if face == "top":
        # the back seen from above: deep blue-green, darkest along the spine, a little teal at the edges
        n = noise(name, "top", x, z)
        centre = abs(x) < 0.6 or (w == 2 and n < 0.35)
        if name == "snout":
            return TEAL if n < 0.5 else LIME
        if name == "head":
            return BACK if n < 0.7 else TEAL
        if centre:
            return BACK_DARK
        if n < 0.15:
            return SPOT_B
        return BACK if n < 0.8 else TEAL
    if face == "bottom":
        n = noise(name, "bottom", x, z)
        return BELLY if n < 0.8 else PALE
    r = int(y - y0)
    c = rows[r]
    n = noise(name, face, x, y, z)
    side = face in ("west", "east")
    if face == "north" and name == "snout" and r == 2:
        return BROWN                                       # the mouth, seen from the front
    if side:
        # the head: eye, mouth, gill cover
        if name == "head" and abs(z + 15.5) < 0.1 and r == 2:
            return EYE
        if name in ("head", "snout") and r == (4 if name == "head" else 2) and z < -14.9:
            return BROWN                                   # the mouth line runs back under the eye
        if name == "head" and abs(z + 13.5) < 0.1 and 2 <= r <= 4:
            return GOLD_D                                  # the edge of the gill cover
        # a soft mix where green meets gold, a shine on the teal, small dark spots
        if c is TEAL and n < 0.25:
            return MINT
        if c is LIME and n < 0.3:
            return TEAL if noise("lime", x, y, z) < 0.5 else GOLD
        if c is GOLD and r > 0 and rows[r - 1] is not GOLD and n < 0.3:
            return LIME
        if name in ("trunk", "mid", "rear") and z > -12:
            # a few small spots, most on the green upper flank, never two side by side
            if c in (TEAL, LIME) and n > 0.9 and noise("spot", x, y, z - 1) <= 0.9:
                return SPOT_B
            if c is GOLD and rows[r - 1] is not GOLD and n > 0.93:
                return SPOT
        if c is GOLD and n > 0.96 and name != "head":
            return GOLD_D
        if c is PALE and rows[r - 1] is GOLD and n < 0.25:
            return GOLD
    return c


def fin_colour(name, x, y, z):
    """The colour of one fin texel, or CLEAR outside the fin's outline."""
    zi, yi = int(math.floor(z)), int(math.floor(y))
    if name in ("dorsal_front", "dorsal_back"):
        top = DORSAL_TOP.get(zi)
        if top is None or yi < top:
            return CLEAR
        # the edge row darkest, the rest dark blue-green with faint rays
        if yi == top:
            return BACK_DARK
        return SPOT_B if zi % 4 == 0 else BACK_DARK
    if name == "anal":
        bottom = ANAL_BOTTOM.get(zi)
        if bottom is None or yi > bottom:
            return CLEAR
        # one solid strip: olive, its outer edge a shade darker only at the tapering back end
        return OLIVE_D if zi >= 6 else OLIVE
    if name == "caudal":
        ch = CAUDAL[yi - 16][zi - 12]
    else:
        ch = PECTORAL[int(math.floor(z)) + 12][int(math.floor(abs(x) - 1.5))]
        return {"o": BACK, "l": TEAL, "d": BACK_DARK, ".": CLEAR}[ch]
    return {"o": OLIVE, "l": LIME, "d": OLIVE_D, ".": CLEAR}[ch]


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
    order = ["body", "tail", "tail_fin", "right_fin", "left_fin"]
    var = {"body": None, "tail": "tail", "tail_fin": None, "right_fin": None, "left_fin": None}
    for part in order:
        parent, (px, py, pz), zrot = PARTS[part]
        if parent:
            ppx, ppy, ppz = PARTS[parent][1]
            ox, oy, oz = px - ppx, py - ppy, pz - ppz
            target = parent
        else:
            ox, oy, oz = px, py, pz
            target = "root"
        builder = "CubeListBuilder.create()"
        cubes = [c for c in CUBES if c[1] == part]
        for cube in cubes:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = tex_offset(cube)
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %d.0F, %d.0F, %d.0F)" % (
                name, u, v, f(x0 - px), f(y0 - py), f(z0 - pz), w, h, d)
        if zrot:
            pose = "PartPose.offsetAndRotation(%s, %s, %s, 0.0F, 0.0F, %s)" % (f(ox), f(oy), f(oz), f(zrot))
        else:
            pose = "PartPose.offset(%s, %s, %s)" % (f(ox), f(oy), f(oz))
        prefix = ("PartDefinition %s = " % var[part]) if var[part] else ""
        lines.append("        %s%s.addOrReplaceChild(\"%s\", %s,\n            %s);" % (prefix, target, part, builder, pose))
    body = "\n".join(lines)
    src = """package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The lampuka (dolphinfish): a steep blunt forehead, one long dorsal fin from the head almost to the tail, a long anal
 * fin, a deeply forked tail, gold flanks under a blue-green back. The back half ("tail") sways gently as it swims, the
 * tail fin more. 35 px long, 7 px deep, head toward -z, the ground at y 24.
 * Made by art/src/fish_lampuka_model.py (don't edit by hand). Texture: textures/entity/fish/lampuka.png (64 x 32).
 */
public class LampukaModel extends FishModel {
    public LampukaModel(ModelPart root) {
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


def rot_z(p, a):
    x, y, z = p
    ca, sa = math.cos(a), math.sin(a)
    return (x * ca - y * sa, x * sa + y * ca, z)


def to_world(parts, part, p):
    """Absolute rest position -> posed position (rotations about each part's pivot, parents last)."""
    while part:
        parent, pivot, zrot = parts[part]
        if zrot:
            rel = (p[0] - pivot[0], p[1] - pivot[1], p[2] - pivot[2])
            rel = rot_z(rel, zrot)
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
        # looking from -x toward +x: screen right = +z, screen down = +y, depth = +x
        z2, x2 = z * cy + x * sy, -z * sy + x * cy
        y3, d3 = y * cp - x2 * sp, y * sp + x2 * cp
        return z2, y3, d3

    pts = []
    for cube in cubes:
        name, part, _, (x0, y0, z0), (w, h, d) = cube
        u0, v0 = tex_offset(cube)
        for face, u, v, x, y, z in face_texels(cube):
            col = texture.getpixel((u % texture.size[0], v % texture.size[1]))
            if col[3] < 128:
                continue
            k = SHADE[face]
            col = (int(col[0] * k), int(col[1] * k), int(col[2] * k))
            # the texel's square in its face plane
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
    import glob
    import zipfile
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
        img.save(os.path.join(out_dir, "lampuka_%s16.png" % view))
        out[view] = img
    cod, sal = vanilla_texture("cod"), vanilla_texture("salmon")
    if cod and sal:
        row = [render(CUBES, PARTS, texture, "side", 8),
               render(vanilla_cubes(SAL_CUBES), SAL_PARTS, sal, "side", 8),
               render(vanilla_cubes(COD_CUBES), COD_PARTS, cod, "side", 8)]
        out["scale"] = row
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

    def row(images, h=None, gap=12):
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

    ref_dir = os.path.join(ROOT, "art", "references", "fish_lampuka_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("dolphinfish.jpg", "side_tunisia.png", "water_school.jpg", "ifremer.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    title("References (photos, reference only): young fish, side; Mediterranean catch; colours; market crate")
    row(refs, h=220)
    title("Offline model, 16x: side, top, three-quarter (no lighting but vanilla face shading)")
    row([pv["side"], pv["three"]])
    row([pv["top"]])
    if "scale" in pv:
        title("Same scale, 8x: lampuka (hitbox 1.0 x 0.45), vanilla salmon (0.7 x 0.4), vanilla cod (0.5 x 0.3)")
        row(pv["scale"])
    van = [t for t in (vanilla_texture("cod"), vanilla_texture("salmon")) if t]
    title("Texture at 8x and 1x: lampuka (64 x 32), vanilla cod and salmon (32 x 32)")
    row([texture.resize((TW * 8, TH * 8), Image.NEAREST), texture]
        + [t.resize((t.width * 8, t.height * 8), Image.NEAREST) for t in van] + van)
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            import glob
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        title("In the game: the lampuka alone (side close-up, three-quarter, top, on land)")
        imgs = [shot(n) for n in ("fish-lampuka-side", "fish-lampuka-three-quarter", "fish-lampuka-top",
                                  "fish-lampuka-on-land")]
        imgs = [i for i in imgs if i]
        if imgs:
            row(imgs[:2], h=400)
            row(imgs[2:], h=400)
            title("The same, cropped to the fish (about 1.9x)")
            crops = []
            for i in imgs:
                box = (int(i.width * 0.2), int(i.height * 0.2), int(i.width * 0.75), int(i.height * 0.6))
                k = 880.0 / (box[2] - box[0])
                crops.append(i.crop(box).resize((880, int((box[3] - box[1]) * k)), Image.NEAREST))
            row(crops[:2])
            row(crops[2:])
        title("In the game: beside vanilla cod and salmon (the shared tank, all seven fish)")
        imgs = [shot(n) for n in ("fish-01-tank-all", "fish-02-tank-cod-salmon-sardina", "fish-03-tank-awrata-lampuka-cerna")]
        imgs = [i for i in imgs if i]
        if imgs:
            row(imgs[:2], h=400)
            row(imgs[2:], h=400)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_lampuka_model.png")
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
        sheet(args[args.index("--sheet") + 1], texture, prev or os.path.join(ROOT, "art", "candidates", "tmp_lampuka"))
    elif prev:
        previews(prev, texture)
        print("previews in", prev)


if __name__ == "__main__":
    main()
