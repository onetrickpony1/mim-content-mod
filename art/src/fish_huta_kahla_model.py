"""The huta kahla (blue shark, Prionace glauca) as a swimming mob: its 3D model and its texture.

Drawn from the reference photos in art/references/fish_huta_kahla_refonly/ (list.tsv; bs06, the NOAA side view, for
the proportions; bs01, bs03 and bs07, landed sharks, for the colour). What makes it a blue shark, and not a dolphin:
  - a long, slender torpedo: 42 px long and only 6 deep and 5 thick (depth to length 0.14, as on the real fish),
    deepest under the first dorsal fin and tapering in 1 px steps to a thin tail stalk;
  - a long, pointed, conical snout: it narrows in single steps (6, 5, 4, 3, 2 and 1 px deep) to a point a little
    above the body's middle line, so there is no rounded forehead, no step and no beak;
  - one big dark eye per side, 4 px behind the tip, in bright blue with nothing dark beside it;
  - five gill slits, soft grey-blue lines low on the side, below the eye's row, so they read as slits and never as
    a row of eyes;
  - long, broad, sickle-shaped pectoral fins (a 4 px root on the lower flank, swept back to a point), held out and
    down like wings: solid blades with a lit leading edge, never a thin line (the owner's note on the icon);
  - a triangular first dorsal fin in the middle of the back, a small second dorsal and a small anal fin;
  - a heterocercal tail: an upright fin (not flat flukes) whose upper lobe climbs far up and back, the lower lobe
    short;
  - countershading in soft bands round the body: a deep indigo back, deep blue, then bright blue sides, a lighter
    blue just above a sharp change to the white belly, and a grey-blue shade underneath.
The body is rounded: every thick step is a 3 px wide core with a 1 px narrower slab on each side, so each cross-section
is an octagon (the corners cut by 1 px). Nothing overlaps, and no two faces share a plane facing the same way.
The palette is the accepted item icon's (art/src/fish_huta_kahla_icon.py PAL), each colour lifted one step (brighter
and a touch richer) because under water the game greys and darkens everything. No random speckle: each face is
shaded by where it sits round the body, so the bands follow the form.

Size: the hitbox is 1.3 x 0.7 blocks. The shark is 42 px long (2.6 blocks), the tonn 39 px (2.44 blocks, scaled per
fish from 2 to 4 blocks in the game) and vanilla cod 15 px. The shark is 6 px deep and 5 thick against the tonn's 10
and 7: much slimmer, with a longer snout and a far taller, longer tail.

Swimming (HutaKahlaModel.setupAnim): the back half ("tail", from just behind the first dorsal) and the tail fin
sweep slowly, about once a second (half the speed of the other fish), the fin a little behind the body, so the tail
sweeps rather than wags.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body", "tail" (the back half) holding "tail_fin".

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/HutaKahlaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/huta_kahla.png
With --sheet SCREENSHOT_DIR it also writes the compare sheet art/candidates/fish_huta_kahla_model.png.

Run:  art/.venv/bin/python art/src/fish_huta_kahla_model.py [--sheet SCREENSHOT_DIR]
"""
import colorsys
import glob
import math
import os
import sys
import zipfile

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import fish_awrata_model as AW  # noqa: E402  (the shared offline renderer and model reader)

RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA_DIR = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish")
JAVA = os.path.join(JAVA_DIR, "HutaKahlaModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "huta_kahla.png")
TW, TH = 64, 64


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


def lift(c, v=1.15, s=1.08):
    """One step lighter and a touch richer for the water: brightness x1.15, saturation x1.08 (hue kept)."""
    h, sat, val = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, min(1.0, sat * s), min(1.0, val * v))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


# The accepted icon's colours (art/src/fish_huta_kahla_icon.py PAL), one in-between blue added, each lifted a step.
ICON = {
    "B0": "#262e74",   # the darkest indigo: the ridge of the back, fin tips (icon p)
    "B1": "#303a86",   # indigo back (icon 1)
    "B2": "#3c50a4",   # deep blue, between the back and the side (between icon 1 and 3)
    "B3": "#4a66c0",   # bright blue side (icon 3)
    "B4": "#6e84d4",   # lighter blue just above the white (icon T)
    "D": "#7a90dc",    # lit leading edge of the first dorsal (icon D)
    "W": "#e8ecf6",    # white belly (icon 5)
    "S": "#a8b0cc",    # the belly turning away, grey-blue (icon 6)
    "g": "#6e76a0",    # deeper grey-blue: the mouth, slits in the shade (icon g)
}
PAL = {k: lift(hexc(v)) for k, v in ICON.items()}
PAL["W"] = hexc("#eef1f8")          # the white is already as light as it should go: kept, not lifted
PAL["e"] = hexc("#0a0a16")          # the eye (the icon's, the only near-black, not lifted)
PAL["."] = (0, 0, 0, 0)
CLEAR = PAL["."]
RAMP = ["B0", "B1", "B2", "B3", "B4"]


def darker(key):
    """The next darker colour on the body: one step down the blue ramp, white to shade, shade to deep shade."""
    if key in RAMP:
        return RAMP[max(0, RAMP.index(key) - 1)]
    return {"W": "S", "S": "g", "D": "B4", "g": "g"}[key]


# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot relative to the parent, rotation (x, y, z)). The body and tail are not turned at rest.
TAIL_Z = 3.0       # where the back half hinges: just behind the first dorsal fin and the pelvic region
FIN_Z = 11.0       # where the tail fin hinges: the end of the tail stalk
AXIS = 19.0
PEC_DROOP = 0.6    # how far the pectoral fins are turned down from flat (radians, about 34 degrees)
PEC_PIVOT = (1.5, 21.0, -13.0)   # the inner corner under the shoulder, behind the gills
PARTS = {
    "body": (None, (0.0, AXIS, 0.0), (0.0, 0.0, 0.0)),
    "right_fin": (None, (-PEC_PIVOT[0], PEC_PIVOT[1], PEC_PIVOT[2]), (0.0, 0.0, -PEC_DROOP)),
    "left_fin": (None, PEC_PIVOT, (0.0, 0.0, PEC_DROOP)),
    "tail": (None, (0.0, AXIS, TAIL_Z), (0.0, 0.0, 0.0)),
    "tail_fin": ("tail", (0.0, 0.0, FIN_Z - TAIL_Z), (0.0, 0.0, 0.0)),
}
PART_ORDER = ("body", "right_fin", "left_fin", "tail", "tail_fin")

# The body as steps from the snout tip back to the tail stalk, in absolute model pixels: (name, part, z0, z1, top,
# bottom, width). y is down; 24 is the ground. The back stays level at 17 from the gills to the hinge and the belly
# rises toward the tail; the snout tapers to a point at y 19-20, just above the middle line (the mouth is under it).
SEGMENTS = [
    ("tip", "body", -22, -21, 19, 20, 1),
    ("snout", "body", -21, -19, 19, 21, 2),
    ("eyes", "body", -19, -17, 18, 21, 3),
    ("head", "body", -17, -14, 18, 22, 4),
    ("gills", "body", -14, -10, 17, 22, 5),
    ("trunk", "body", -10, -1, 17, 23, 5),
    ("belly", "body", -1, 3, 17, 22, 5),
    ("rear", "tail", 3, 6, 18, 22, 4),
    ("rear2", "tail", 6, 9, 18, 21, 3),
    ("stalk", "tail", 9, 11, 18, 20, 2),
]
SEG = {s[0]: s for s in SEGMENTS}


def part_abs(part):
    """The part's pivot in absolute model space (parts with children are not turned)."""
    parent, (x, y, z), _ = PARTS[part]
    if parent:
        px, py, pz = part_abs(parent)
        return x + px, y + py, z + pz
    return x, y, z


def body_cubes():
    """Each step as boxes: a full-depth core and, where it is 4 px wide or more, a slab 2 px shorter on each side,
    so the corners are cut and the section is round. Returns (cube name, segment, part, abs origin, size)."""
    out = []
    for name, part, z0, z1, top, bot, w in SEGMENTS:
        d, h = z1 - z0, bot - top
        if w >= 4 and h >= 4:
            core = w - 2
            out.append((name, name, part, (-core / 2, top, z0), (core, h, d)))
            out.append((name + "_r", name, part, (-w / 2, top + 1, z0), (1, h - 2, d)))
            out.append((name + "_l", name, part, (core / 2, top + 1, z0), (1, h - 2, d)))
        else:
            out.append((name, name, part, (-w / 2, top, z0), (w, h, d)))
    return out


# Flat fins: (name, part, abs origin for the body's fins / local origin for the side fins, size). Their outlines are
# cut by the masks below.
FINS = [
    ("dorsal", "body", (0.0, 13.0, -6.0), (0, 4, 5)),        # first dorsal, on the back (top 17) at z -6..-1
    ("dorsal2", "tail", (0.0, 16.0, 5.0), (0, 2, 3)),        # second dorsal, on the stalk's back (top 18)
    ("anal", "tail", (0.0, 21.0, 6.0), (0, 2, 3)),           # anal fin, under the rear (bottom 21)
    ("lobe", "tail_fin", (0.0, 12.0, 11.0), (0, 12, 10)),    # the tail: upper lobe up to y 12, lower to y 23
    ("pec_r", "right_fin", (-6.0, 0.0, 0.0), (6, 0, 6)),     # pectorals: local to their part (out, back)
    ("pec_l", "left_fin", (0.0, 0.0, 0.0), (6, 0, 6)),
]
# A small solid root for the upper tail lobe, so the tail doesn't start as a paper-thin plane behind the stalk.
LOBE_ROOT = ("lobe_root", "tail_fin", (-0.5, 17.0, 11.0), (1, 2, 2))

# Fin outlines, one character per pixel, top row first, front (-z) on the left; colours from PAL, '.' = clear.
# First dorsal, rows y 13..16, columns z -6..-2: a shark's triangle, the lit leading edge climbing back to the apex
# over the rear of the base, the darker trailing edge nearly upright.
DORSAL = [
    "...B1.",
    "..DB2.",
    ".DB2B2B1",
    "DB2B2B2B1",
]
# Second dorsal, rows y 16..17, columns z 5..7; anal fin, rows y 21..22, columns z 6..8.
DORSAL2 = [
    ".B1.",
    "B2B2B1",
]
ANAL = [
    "SSg",
    ".g.",
]
# The tail, rows y 12..23, columns z 11..20, built from its edges (see lobe_mask): the upper lobe climbs from the stalk
# to its tip at z 20, y 12 (a rise of 6 over 9, about 34 degrees), lit along its leading (upper) edge, darker along
# its trailing edge; the lower lobe is a short blade down and back to y 23; the fork's notch is behind it.
LOBE_TOP = [17, 17, 16, 16, 15, 15, 14, 13, 13, 12]      # the upper edge, column by column (z 11..20)
LOBE_UP_BOTTOM = [19, 19, 19, 19, 18, 17, 16, 15, 14, 12]  # the upper lobe's lower edge
LOBE_LOW = {0: 20, 1: 21, 2: 22, 3: 23}                  # the lower lobe hangs to these rows


def lobe_mask():
    rows = []
    for y in range(12, 24):
        row = []
        for c in range(10):
            top, ub = LOBE_TOP[c], LOBE_UP_BOTTOM[c]
            low = LOBE_LOW.get(c)
            if top <= y <= ub:
                if c == 9 or y == top:
                    k = "B4"                       # lit leading edge, and the tip
                elif y == ub and c >= 4:
                    k = "B1"                       # dark trailing edge of the upper lobe
                elif c <= 1:
                    k = "B2"                       # the root, continuing the stalk
                else:
                    k = "B3"
            elif low is not None and ub < y <= low:
                if y == low:
                    k = "B1" if c == 3 else "B2"   # the lower lobe's edge, its tip darkest
                elif c == 3:
                    k = "B2"                       # its trailing edge
                else:
                    k = "B3"
            else:
                k = "."
            row.append(k)
        rows.append(row)
    return rows


# The pectoral fin, rows = back (z 0..5 from its root), columns = out from the body (0..5): a broad blade with a 4 px
# root, swept back to a point. Dark blue like the back (it is seen mostly from above): a bright blue leading edge, a
# deep blue blade, an indigo trailing edge and tip.
PECTORAL = [
    "B3B3....",
    "B2B2B3...",
    "B2B2B2B3..",
    "B1B2B2B2B3.",
    ".B1B1B2B2B3",
    "...B1B1B0",
]


def parse_row(row):
    """A mask row into a list of keys: two-character keys (B0..B4) or one character."""
    out, i = [], 0
    while i < len(row):
        if row[i] == "B":
            out.append(row[i:i + 2])
            i += 2
        else:
            out.append(row[i])
            i += 1
    return out


MASKS = {k: [parse_row(r) for r in v] for k, v in
         {"dorsal": DORSAL, "dorsal2": DORSAL2, "anal": ANAL, "pec": PECTORAL}.items()}
MASKS["lobe"] = lobe_mask()


def mask_key(name, row, col):
    m = MASKS[name]
    if 0 <= row < len(m) and 0 <= col < len(m[row]):
        return m[row][col]
    return "."


# --- colour ----------------------------------------------------------------------------------------------------------
EYE = (-18, 19)                                   # (z, y) cell of the eye on each side
SLITS = (-15, -13, -11, -9, -7)                   # z cells of the five gill slits
SLIT_ROWS = (20, 21)                              # their rows: below the eye's row


def band(f):
    """The colour round the body by height on the flank: f 0 at the top of this step, 1 at the bottom."""
    if f < 0.17:
        return "B1"
    if f < 0.34:
        return "B2"
    if f < 0.52:
        return "B3"
    if f < 0.62:
        return "B4"
    return "W"                 # the white belly; its shade, S, is on the faces turned down (body_key)


def body_key(seg, cube_name, face, x, y, z):
    name, _part, z0, z1, top, bot, w = SEG[seg]
    zi, yi = int(math.floor(z)), int(math.floor(y))
    side_slab = cube_name != seg
    if face == "top":
        if side_slab:
            return "B1"                                     # the rounded shoulder
        if w >= 3 and abs(x) < 0.5:
            return "B0"                                     # the ridge of the back
        return "B1"
    if face == "bottom":
        if side_slab:
            return "S"                                      # the belly turning away
        if seg == "eyes" and zi == -18:
            return "g"                                      # the mouth: a soft crescent under the head
        if seg == "head" and zi == -17 and abs(x) > 0.5:
            return "g"                                      # its corners curve back
        if SEG[seg][1] == "tail" and seg != "rear":
            return "S"                                      # the pale under the stalk, a shade down from the belly
        return "W"
    key = band((y - top) / float(bot - top))
    if face in ("west", "east"):
        if (zi, yi) == EYE:
            return "e"
        if seg == "eyes" and yi == 18:
            return "B2"                                     # nothing dark right above the eye
        if zi in SLITS and yi in SLIT_ROWS and seg in ("head", "gills", "trunk"):
            return darker(key)
    return key


def fin_key(name, x, y, z):
    xi, yi, zi = int(math.floor(x)), int(math.floor(y)), int(math.floor(z))
    if name == "dorsal":
        return mask_key("dorsal", yi - 13, zi + 6)
    if name == "dorsal2":
        return mask_key("dorsal2", yi - 16, zi - 5)
    if name == "anal":
        return mask_key("anal", yi - 21, zi - 6)
    if name == "lobe":
        return mask_key("lobe", yi - 12, zi - 11)
    if name in ("pec_r", "pec_l"):
        out = int(math.floor(abs(x)))
        return mask_key("pec", int(math.floor(z)), out)
    if name == "lobe_root":
        return "B2" if yi == 17 else "B3"
    raise ValueError(name)


# --- texture layout (the vanilla box UV layout) ----------------------------------------------------------------------
def all_cubes():
    """Every cube as (name, segment or None, part, local origin, size)."""
    out = []
    for name, seg, part, (x0, y0, z0), size in body_cubes():
        px, py, pz = part_abs(part)
        out.append((name, seg, part, (x0 - px, y0 - py, z0 - pz), size))
    for name, part, origin, size in FINS:
        if part in ("right_fin", "left_fin"):
            out.append((name, None, part, origin, size))
        else:
            px, py, pz = part_abs(part)
            out.append((name, None, part, (origin[0] - px, origin[1] - py, origin[2] - pz), size))
    name, part, (x0, y0, z0), size = LOBE_ROOT
    px, py, pz = part_abs(part)
    out.append((name, None, part, (x0 - px, y0 - py, z0 - pz), size))
    return out


def used_rect(size):
    w, h, d = size
    if w == 0:
        return (0, d), (2 * d, h)
    if h == 0:
        return (d, 0), (2 * w, d)
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
    for (name, seg, part, (x0, y0, z0), (w, h, d)), (u, v) in layout():
        px, py, pz = part_abs(part)
        for face, tu, tv, x, y, z in AW.face_texels(u, v, (x0, y0, z0), (w, h, d)):
            if w == 0 and face not in ("west", "east"):
                continue
            if h == 0 and face not in ("top", "bottom"):
                continue
            assert 0 <= tu < TW and 0 <= tv < TH, (name, face, tu, tv)
            assert owner.setdefault((tu, tv), name) == name, ("texture overlap", name, owner[(tu, tv)], tu, tv)
            if seg:
                key = body_key(seg, name, face, x + px, y + py, z + pz)
            elif part in ("right_fin", "left_fin"):
                key = fin_key(name, x, y, z)     # local: out along x, back along z
            else:
                key = fin_key(name, x + px, y + py, z + pz)
            if key != ".":
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
        "package com.maltaminecraft.mimcontent.client.fish;",
        "",
        "import net.minecraft.client.model.geom.ModelPart;",
        "import net.minecraft.client.model.geom.PartPose;",
        "import net.minecraft.client.model.geom.builders.CubeListBuilder;",
        "import net.minecraft.client.model.geom.builders.LayerDefinition;",
        "import net.minecraft.client.model.geom.builders.MeshDefinition;",
        "import net.minecraft.client.model.geom.builders.PartDefinition;",
        "import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;",
        "import net.minecraft.util.Mth;",
        "",
        "/**",
        " * The huta kahla (blue shark): a long, slender torpedo with a pointed conical snout, big eyes, five gill slits,",
        " * long sickle-shaped pectoral fins held out like wings, a triangular first dorsal, a small second dorsal and",
        " * anal fin, and a tail whose upper lobe is far longer than the lower. 42 px long, 6 deep, 5 thick; the body is",
        " * rounded (cut corners). Deep indigo back, bright blue sides, white belly.",
        " * Made by art/src/fish_huta_kahla_model.py (do not edit by hand); texture textures/entity/fish/huta_kahla.png.",
        " * Follows the fish model contract (docs/Tools and Process/Art pipeline.md, \"Fish models\"): \"tail\" is the back",
        " * half, \"tail_fin\" the tail inside it. A shark swims slowly: the tail sweeps about once a second, the fin a",
        " * little behind the body, instead of the quick wag of the smaller fish.",
        " */",
        "public class HutaKahlaModel extends FishModel {",
        "    private final ModelPart tail;",
        "    private final ModelPart tailFin;",
        "",
        "    public HutaKahlaModel(ModelPart root) {",
        "        super(root);",
        "        this.tail = root.getChild(\"tail\");",
        "        this.tailFin = tail.getChild(\"tail_fin\");",
        "    }",
        "",
        "    @Override",
        "    public void setupAnim(LivingEntityRenderState state) {",
        "        super.setupAnim(state);",
        "        // out of water it flops wider and quicker, as every fish does",
        "        float amplitude = state.isInWater ? 1.0F : 1.4F;",
        "        float speed = state.isInWater ? 1.0F : 1.8F;",
        "        float phase = speed * 0.3F * state.ageInTicks;",
        "        tail.yRot = -amplitude * 0.14F * Mth.sin(phase);",
        "        tailFin.yRot = -amplitude * 0.3F * Mth.sin(phase - 1.0F);",
        "    }",
        "",
        "    public static LayerDefinition createBodyLayer() {",
        "        MeshDefinition mesh = new MeshDefinition();",
        "        PartDefinition root = mesh.getRoot();",
    ]
    placed = layout()
    for part in PART_ORDER:
        parent, (px, py, pz), (rx, ry, rz) = PARTS[part]
        builder = "CubeListBuilder.create()"
        for (name, _seg, cpart, (x0, y0, z0), (w, h, d)), (u, v) in placed:
            if cpart != part:
                continue
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %s, %s, %s)" % (
                name, u, v, f(x0), f(y0), f(z0), f(w), f(h), f(d))
        if (rx, ry, rz) == (0, 0, 0):
            pose = "PartPose.offset(%s, %s, %s)" % (f(px), f(py), f(pz))
        else:
            pose = "PartPose.offsetAndRotation(%s, %s, %s, %s, %s, %s)" % (f(px), f(py), f(pz), f(rx), f(ry), f(rz))
        has_child = any(p[0] == part for p in PARTS.values())
        var = "PartDefinition %s = " % part if has_child else ""
        lines.append("        %s%s.addOrReplaceChild(\"%s\", %s," % (var, parent or "root", part, builder))
        lines.append("            %s);" % pose)
    lines += ["        return LayerDefinition.create(mesh, %d, %d);" % (TW, TH), "    }", "}", ""]
    return "\n".join(lines)


# --- checks ----------------------------------------------------------------------------------------------------------
def abs_box(cube):
    name, seg, part, (x0, y0, z0), (w, h, d) = cube
    px, py, pz = part_abs(part)
    return (x0 + px, y0 + py, z0 + pz), (x0 + px + w, y0 + py + h, z0 + pz + d)


def check_boxes():
    """The solid body boxes (unturned parts) must not overlap, and no two faces may share a plane facing the same way
    where they overlap (they would flicker). Returns a list of problems."""
    solids = [c for c in all_cubes() if all(c[4]) and c[2] in ("body", "tail", "tail_fin")]
    probs = []
    for i in range(len(solids)):
        a0, a1 = abs_box(solids[i])
        for j in range(i + 1, len(solids)):
            b0, b1 = abs_box(solids[j])
            ov = [min(a1[k], b1[k]) - max(a0[k], b0[k]) for k in range(3)]
            if all(o > 1e-6 for o in ov):
                probs.append(("overlap", solids[i][0], solids[j][0]))
                continue
            for k in range(3):
                for side in (0, 1):
                    pa = (a0, a1)[side][k]
                    pb = (b0, b1)[side][k]
                    if abs(pa - pb) > 1e-6:
                        continue
                    o = [min(a1[m], b1[m]) - max(a0[m], b0[m]) for m in range(3) if m != k]
                    if all(x > 1e-6 for x in o):
                        probs.append(("same plane", solids[i][0], solids[j][0], "xyz"[k]))
    return probs


# --- the compare sheet ------------------------------------------------------------------------------------------------
# vanilla dolphin (26.3 DolphinModel, as numbers, read from the game's class), for "it must not look like a dolphin"
DOLPHIN = ([
    ("body", None, (0, 22, -5), (0, 0, 0), [(22, 0, (-4, -7, 0), (8, 7, 13))]),
    ("back_fin", "body", (0, 0, 0), (1.0471976, 0, 0), [(51, 0, (-0.5, 0, 8), (1, 4, 5))]),
    ("left_fin", "body", (2, -2, 4), (1.0471976, 0, 2.0943952), [(48, 20, (-0.5, -4, 0), (1, 4, 7))]),
    ("right_fin", "body", (-2, -2, 4), (1.0471976, 0, -2.0943952), [(48, 20, (-0.5, -4, 0), (1, 4, 7))]),
    ("tail", "body", (0, -2.5, 11), (-0.10471976, 0, 0), [(0, 19, (-2, -2.5, 0), (4, 5, 11))]),
    ("tail_fin", "tail", (0, 0, 9), (0, 0, 0), [(19, 20, (-5, -0.5, 0), (10, 1, 6))]),
    ("head", "body", (0, -4, -3), (0, 0, 0), [(0, 0, (-4, -3, -3), (8, 7, 6))]),
    ("nose", "head", (0, 0, 0), (0, 0, 0), [(0, 13, (-1, 2, -7), (2, 2, 4))]),
], (64, 64))


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


def load_model(fish, cls):
    model = AW.parse_java(os.path.join(JAVA_DIR, cls + "Model.java"))
    tex = Image.open(os.path.join(RES, "textures", "entity", "fish", fish + ".png")).convert("RGBA")
    return model, tex


def sheet(shots_dir, texture):
    from PIL import ImageFont
    font = ImageFont.load_default()
    W = 1800
    blocks = []
    me = (AW.parse_java(JAVA), texture)

    def title(t):
        im = Image.new("RGBA", (W, 26), (40, 40, 40, 255))
        ImageDraw.Draw(im).text((8, 6), t, fill=(240, 240, 240, 255), font=font)
        blocks.append(im)

    def row(images, h=None, gap=12, align_bottom=False, labels=None):
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images) + (16 if labels else 0)
        im = Image.new("RGBA", (W, hh + 8), (72, 72, 72, 255))
        dr = ImageDraw.Draw(im)
        x = 8
        for n, i in enumerate(images):
            step = max(i.width, 6 * len(labels[n]) if labels else 0) + gap
            if x + i.width > W:
                break
            top = 4 + (hh - (16 if labels else 0) - i.height if align_bottom else 0)
            im.paste(i, (x, top), i)
            if labels:
                dr.text((x, hh - 10), labels[n], fill=(230, 230, 230, 255), font=font)
            x += step
        blocks.append(im)

    ref_dir = os.path.join(ROOT, "art", "references", "fish_huta_kahla_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("bs06.jpg", "bs05.jpg", "bs03.jpg", "bs07.jpg") if os.path.exists(os.path.join(ref_dir, n))]
    title("References (reference only): side view for proportions (NOAA), in water, landed sharks for true colour")
    row(refs, h=230)
    title("Offline model, 14x: side, three-quarter (vanilla face shading only, no water)")
    row([AW.render(me[0], texture, "side", 14), AW.render(me[0], texture, "three", 14)])
    title("Offline model, 14x: from above")
    row([AW.render(me[0], texture, "top", 14)])
    items = [Image.open(os.path.join(RES, "textures", "item", n)).convert("RGBA")
             for n in ("huta_kahla.png", "huta_kahla_bucket.png", "huta_kahla_spawn_egg.png")]
    base = Image.open(os.path.join(ROOT, "art", ".vanilla", "item", "cod_bucket.png")).convert("RGBA")
    bucket = base.copy()
    bucket.alpha_composite(items[1])
    items[1] = bucket
    title("The accepted huta kahla item icon, bucket (over the player's cod bucket) and spawn egg (8x), beside the model "
          "(side and three-quarter, 8x)")
    row([i.resize((128, 128), Image.NEAREST) for i in items]
        + [AW.render(me[0], texture, "side", 8), AW.render(me[0], texture, "three", 8)], align_bottom=True, gap=24)
    models = [("huta kahla", me), ("tonn (accepted)", load_model("tonn", "Tonn"))]
    cod = game_texture("entity/fish/cod.png")
    dol = game_texture("entity/dolphin/dolphin.png")
    if cod:
        models.append(("vanilla cod", (AW.COD, cod)))
    if dol:
        models.append(("vanilla dolphin (must NOT look like it)", (DOLPHIN, dol)))
    labels = []
    for n, (mdl, _) in models:
        ln, dep, depf, thick, blen = AW.extent(mdl)
        labels.append("%s: %d long, %d deep, %d thick" % (n, ln, dep, thick))
    title("Same scale, 6x, side: the huta kahla beside the accepted tonn (2.44 blocks at its base size), vanilla cod "
          "and vanilla dolphin")
    row([AW.render(m[0], m[1], "side", 6) for _, m in models[:2]], align_bottom=True, gap=40, labels=labels[:2])
    row([AW.render(m[0], m[1], "side", 6) for _, m in models[2:]], align_bottom=True, gap=40, labels=labels[2:])
    title("Same scale, 6x, three-quarter, in the same order")
    row([AW.render(m[0], m[1], "three", 6) for _, m in models[:2]], align_bottom=True, gap=40, labels=labels[:2])
    row([AW.render(m[0], m[1], "three", 6) for _, m in models[2:]], align_bottom=True, gap=40, labels=labels[2:])
    title("Same scale, 6x, from above (thickness, pectoral fins), in the same order")
    row([AW.render(m[0], m[1], "top", 6) for _, m in models], align_bottom=True, gap=40, labels=labels)
    title("Texture at 5x and 1x (%d x %d)" % (TW, TH))
    row([texture.resize((TW * 5, TH * 5), Image.NEAREST), texture])
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        names = ("fish-huta-kahla-side", "fish-huta-kahla-three-quarter", "fish-huta-kahla-top",
                 "fish-huta-kahla-on-land", "fish-huta-kahla-beside-cod")
        got = [(n, shot(n)) for n in names]
        got = [(n, i) for n, i in got if i]
        if got:
            title("In the game: the huta kahla alone (side, three-quarter, top), on land, and beside vanilla cod")
            row([i for _, i in got[:3]], h=330)
            row([i for _, i in got[3:]], h=330)
            title("The same, cropped to the fish")
            crops = []
            for n, i in got:
                fx = (0.08, 0.15, 0.92, 0.75)
                box = (int(i.width * fx[0]), int(i.height * fx[1]), int(i.width * fx[2]), int(i.height * fx[3]))
                k = 580.0 / (box[2] - box[0])
                crops.append(i.crop(box).resize((580, int((box[3] - box[1]) * k)), Image.NEAREST))
            row(crops[:3])
            row(crops[3:])
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_huta_kahla_model.png")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out.convert("RGB").save(dest)
    print("sheet:", dest)
    for l in labels:
        print(" ", l)


def main():
    probs = check_boxes()
    for p in probs:
        print("problem:", p)
    assert not probs
    texture = draw_texture()
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    texture.save(TEXTURE)
    with open(JAVA, "w", encoding="utf-8") as fh:
        fh.write(java_source())
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    args = sys.argv[1:]
    if "--sheet" in args:
        i = args.index("--sheet")
        sheet(args[i + 1] if i + 1 < len(args) else None, texture)


if __name__ == "__main__":
    main()
