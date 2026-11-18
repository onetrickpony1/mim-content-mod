"""The ziemel tal-bahar (seahorse: Hippocampus guttulatus and H. hippocampus, both in Malta's Posidonia meadows) as a
swimming mob: its 3D model and its texture. This is the seahorse's first piece: it sets the size, the look and the
palette that the bucket and the spawn egg copy later.

Drawn from the reference photos in art/references/fish_ziemel_refonly/ (list.tsv). What makes it a ziemel:
  - it swims upright, a horse-like head on a bent neck (the throat set back behind the jaw),
  - a long tubular snout coming out of the middle of a 3 px deep head, the eye high and back with a cheek below it,
  - a small crown (the coronet) on top of the head, and single fleshy filaments (the "mane" of H. guttulatus) at
    uneven heights on the back of the head and the neck,
  - a pot belly bulging low and forward, the back nearly straight,
  - bony rings all along the body and tail: a darker band every second row,
  - a thin tail, tapering from 2 px to 1, that curls forward under the belly into a closed loop with an open centre
    (it holds on to seagrass with it),
  - a small fan-shaped dorsal fin on the lower back, with rays and a solid edge, that flutters,
  - brown-ochre, with small white dots (guttulatus means "spotted").
The colours follow the golden-brown fish in the photos (Ria de Vigo, Arrabida, the Gervais plate): lighter than the
photos, since under water the game tints everything blue-grey and darkens it, but not so light that it vanishes on
sand. Every face is shaded like a rounded form: tops lightest, sides mid with a lit front and a darker lower edge,
undersides darkest.

Size: bigger than life, as the owner asked (decision 2026-11-18 "Ziemel - start, bigger than life"). A real
H. guttulatus is at most about 15 to 18 cm, under 3 model pixels, so nothing of it would show. At vanilla's pixel
(1/16 block, one texture pixel per model pixel, like cod and salmon) the smallest seahorse that still shows every
feature and its S-shaped build is 13 px tall: a 1 px crown, a 3 px head, a 4 px trunk (taller than it is deep, the
throat notch on top and the pot belly low and forward) and a 5 px tail ending in a 3 x 3 loop. A 12 px version came
out with a trunk wider than tall and read as a block, not a seahorse. That is 0.81 blocks tall and 0.56 long (snout
tip to dorsal fin), about five times life size: as tall as a vanilla cod is long, but slim (3 px at its widest, cod
2 px, salmon 3 px). Hitbox 0.4 wide x 0.8 tall (MimFishes.ZIEMEL), so it covers the whole animal.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body", the dorsal fin as the "tail_fin" and the curled tail as the "tail". The model has its own swimming on
top of FishModel's: in the water it bobs slowly up and down, the dorsal fin flutters fast and narrow, and the tail
curls in and out a little instead of swinging sideways. Its renderer wiggle is 0 (MimContentClient), so the body
stays still and upright; out of water the shared FishRenderer turns it on its side and it flops like every fish.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/ZiemelModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/ziemel.png    (32 x 32)
Also writes offline previews to the folder given with --preview DIR, and the compare sheet
(art/candidates/fish_ziemel_model.png) with --sheet SCREENSHOT_DIR.

Run:  art/.venv/bin/python art/src/fish_ziemel_model.py [--preview DIR] [--sheet SCREENSHOT_DIR]
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
                    "ZiemelModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "ziemel.png")
TW, TH = 32, 32


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# The body ramp, dark to light: a brown-ochre, one step darker than pure gold so it still shows on sand, and still
# lighter than the photos (the water greys it).
RAMP = [hexc(c) for c in ("#7c5830", "#966c3a", "#b08244", "#c4964f", "#d4a85c", "#e2bb6e", "#eecd86")]
DOT = hexc("#fff2cc")      # the small white dots of guttulatus: single bright texels
EYE = hexc("#2e2016")      # the one dark pupil on each side
FIN = hexc("#fcecc2")      # the dorsal fin's thin membrane, pale
RAY = hexc("#eac47c")      # its rays
EDGE = hexc("#c4924a")     # its solid outer edge
MANE = hexc("#aa7840")     # the filaments
MANE_L = hexc("#d8a862")   # a lighter filament
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels)). No part is turned at rest.
# Cubes: (name, part, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail
# (+). Side profile, head to the left (rows y, columns z; C crown, H head, E eye, S snout, M filament, B body,
# D dorsal fin, T tail, o the open centre of the tail's loop):
#        z  -4 -3 -2 -1  0  1  2  3  4
#   y 11                       C
#     12                 H  H  E  H
#     13     S  S  S     H  H  H  H  M
#     14                 H  H  H
#     15                    B  B  B  M
#     16              B  B  B  B  B
#     17              B  B  B  B  B  D  D
#     18                 B  B  B  B  D  D
#     19                       T  T  D
#     20                       T
#     21                 T  T  T
#     22                 T  o  T
#     23                 T  T  T
PARTS = {
    "body": (None, (0.0, 18.0, 0.0)),
    "tail": (None, (0.0, 19.0, 2.0)),        # where the tail leaves the belly: it curls a little about this line
    "tail_fin": (None, (0.0, 18.5, 3.0)),    # the line where the dorsal fin joins the back
}
CUBES = [
    ("coronet", "body", (-0.5, 11.0, 1.0), (1, 1, 1)),
    ("head", "body", (-1.0, 12.0, -1.0), (2, 2, 4)),
    ("jaw", "body", (-1.0, 14.0, -1.0), (2, 1, 3)),
    ("snout", "body", (-0.5, 13.0, -4.0), (1, 1, 3)),
    ("chest", "body", (-1.0, 15.0, 0.0), (2, 1, 3)),
    ("belly", "body", (-1.5, 16.0, -2.0), (3, 2, 5)),
    ("belly_lo", "body", (-1.0, 18.0, -1.0), (2, 1, 4)),
    ("mane", "body", (0.0, 11.0, 3.0), (0, 6, 1)),
    ("tail1", "tail", (-1.0, 19.0, 1.0), (2, 1, 2)),
    ("tail2", "tail", (-0.5, 20.0, 1.0), (1, 1, 1)),
    ("loop_top", "tail", (-0.5, 21.0, -1.0), (1, 1, 3)),
    ("loop_front", "tail", (-0.5, 22.0, -1.0), (1, 1, 1)),
    ("loop_back", "tail", (-0.5, 22.0, 1.0), (1, 1, 1)),
    ("loop_bottom", "tail", (-0.5, 23.0, -1.0), (1, 1, 3)),
    ("dorsal", "tail_fin", (0.0, 17.0, 3.0), (0, 3, 2)),
]
SOLID = [c for c in CUBES if c[3][0] and c[3][1] and c[3][2]]
RINGED = ("chest", "belly", "belly_lo", "tail1", "tail2", "loop_top", "loop_front", "loop_back", "loop_bottom")

# Plane outlines by absolute row (y) and column (z), one character per pixel. Mane: rows 11..16, column z 3:
# single wisps at uneven heights with gaps between them, one on the back of the head, one on the neck.
#   m filament, l a lighter filament, . clear (texels inside the head and body are cleared anyway)
MANE_MAP = [
    ".",
    ".",
    "l",
    ".",
    "m",
    ".",
]
# The dorsal fin: rows 17..19, columns z 3..4: rays from the base, a solid darker outer edge, the lower outer corner
# rounded off.   f membrane, r ray, e edge
DORSAL_MAP = [
    "re",
    "fe",
    "r.",
]


# Where the white dots sit, by (row y, column z) on the sides: single texels, scattered, none touching another or the
# eye.
DOTS = {(15, 1), (16, -1), (18, 2), (21, 0)}
EYE_AT = (12, 1)     # (row y, column z) on both sides of the head: high and back, with a cheek below it


def body_colour(cube, face, x, y, z):
    """The colour of one texel of a solid part, shaded by face like a rounded form: tops lightest, sides mid with a
    darker lower edge and a lit front, undersides darkest; a darker band every second row for the bony rings of the
    trunk and tail; the white dots and the eye."""
    name, _, (x0, y0, z0), (w, h, d) = cube
    yi, zi = int(math.floor(y)), int(math.floor(z))
    if face == "north" and name == "snout":
        face = "west"                              # the snout's tip in the tube's own side tone: no dark hole face on
    side = face in ("west", "east")
    if side and name == "head" and (yi, zi) == EYE_AT:
        return EYE
    v = 3.2
    v += {"top": 1.8, "north": 0.5, "west": 0.0, "east": 0.0, "south": -0.6, "bottom": -1.8}[face]
    v += -0.08 * (y - 17.0)                        # a little lighter toward the crown, darker toward the tail
    if side:
        if d >= 3 and zi == int(z0):
            v += 0.4                               # the front of the flank catches the light
        elif d >= 3 and zi == int(z0 + d - 1):
            v -= 0.4                               # its back edge turns into shade
        if h >= 2 and yi == int(y0 + h - 1) and name not in RINGED:
            v -= 0.6                               # the lower edge of a deep part turns under
    elif face in ("north", "south", "top", "bottom") and w >= 3:
        v += 0.3 if abs(x - (x0 + w / 2.0)) < 0.5 else -0.2   # a wide face: lighter down its middle
    if name in RINGED and face not in ("top", "bottom") and yi % 2 == 1:
        v -= 0.8                                   # the bony rings: a darker band every second row
    if name in ("head", "jaw") and side and (yi, zi) in ((12, 0), (12, 2), (13, 1)):
        v += 0.8                                   # light round the eye, so nothing dark sits beside it
    if name == "coronet":
        v += 0.5
    if side and (yi, zi) in DOTS:
        return DOT
    return RAMP[max(0, min(6, int(round(v))))]


def plane_colour(cube, y, z):
    """The colour of one texel of a flat part (mane, dorsal fin), or CLEAR outside its outline."""
    name = cube[0]
    yi, zi = int(math.floor(y)), int(math.floor(z))
    if name == "mane":
        ch = MANE_MAP[yi - 11][zi - 3]
        return {"m": MANE, "l": MANE_L, ".": CLEAR}[ch]
    ch = DORSAL_MAP[yi - 17][zi - 3]
    return {"f": FIN, "r": RAY, "e": EDGE, ".": CLEAR}[ch]


# --- hidden faces: a face texel inside another solid part, or pressed against one, is cleared (no flicker) ---------
NORMAL = {"top": (0, -1, 0), "bottom": (0, 1, 0), "west": (-1, 0, 0), "east": (1, 0, 0),
          "north": (0, 0, -1), "south": (0, 0, 1)}


def inside(cube, p, eps=1e-6):
    _, _, (x0, y0, z0), (w, h, d) = cube
    return (x0 + eps < p[0] < x0 + w - eps and y0 + eps < p[1] < y0 + h - eps and z0 + eps < p[2] < z0 + d - eps)


def hidden(cube, face, p):
    n = NORMAL[face]
    q = (p[0] + 0.01 * n[0], p[1] + 0.01 * n[1], p[2] + 0.01 * n[2])
    for other in SOLID:
        if other is cube:
            continue
        if inside(other, p) or inside(other, q):
            return True
    return False


# --- texture layout (the vanilla box UV layout) ----------------------------------------------------------------------
def pack():
    """texOffs for every cube: each gets its full box area ((2d + 2w) x (d + h)), packed in shelves."""
    order = sorted(CUBES, key=lambda c: (-(c[3][2] + c[3][1]), -(2 * c[3][2] + 2 * c[3][0]), c[0]))
    out, u, v, shelf = {}, 0, 0, 0
    for c in order:
        w, h, d = c[3]
        rw, rh = 2 * d + 2 * w, d + h
        if u + rw > TW:
            u, v, shelf = 0, v + shelf, 0
        out[c[0]] = (u, v)
        u += rw
        shelf = max(shelf, rh)
        assert v + rh <= TH, ("texture too small", c[0])
    return out


UV = pack()


def face_texels(cube):
    """Every texel of every face: (face, u, v, x, y, z), with (x, y, z) the texel's centre on the model, absolute.
    The mapping follows ModelPart.Cube: top (u+d, v), bottom (u+d+w, v), west (u, v+d), north (u+d, v+d),
    east (u+d+w, v+d), south (u+2d+w, v+d)."""
    name, _, (x0, y0, z0), (w, h, d) = cube
    u, v = UV[name]
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
        name, _, _, (w, h, d) = cube
        flat = not (w and h and d)
        for face, u, v, x, y, z in face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), (name, face)) == (name, face), ("texture overlap", name, face, owner[(u, v)])
            if flat:
                col = CLEAR if any(inside(o, (x, y, z)) for o in SOLID) else plane_colour(cube, y, z)
            elif hidden(cube, face, (x, y, z)):
                col = CLEAR
            else:
                col = body_colour(cube, face, x, y, z)
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
    for part in ("body", "tail", "tail_fin"):
        _, (px, py, pz) = PARTS[part]
        builder = "CubeListBuilder.create()"
        for name, _, (x0, y0, z0), (w, h, d) in [c for c in CUBES if c[1] == part]:
            u, v = UV[name]
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %d.0F, %d.0F, %d.0F)" % (
                name, u, v, f(x0 - px), f(y0 - py), f(z0 - pz), w, h, d)
        pose = "PartPose.offset(%s, %s, %s)" % (f(px), f(py), f(pz))
        lines.append("        root.addOrReplaceChild(\"%s\", %s,\n            %s);" % (part, builder, pose))
    src = """package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.util.Mth;

/**
 * The ziemel tal-bahar (seahorse), upright: a horse-like head on a bent neck, a long tubular snout from the middle of
 * the head, a small crown, single filaments on the back of the head and neck, a pot belly, bony rings along the body
 * and a thin tail curled forward into a closed loop. Brown-ochre with small white dots. Bigger than life so its detail
 * shows: 13 px tall (0.81 blocks), 9 px from snout tip to dorsal fin, head toward -z, the ground at y 24.
 * Its own swimming: in the water it bobs slowly up and down (0.04 blocks, every 2.5 s), the dorsal fin ("tail_fin")
 * flutters quickly and the tail curls in and out a little; the body doesn't swing (its renderer wiggle is 0).
 * Out of water the shared fish animation flops it as usual.
 * Made by art/src/fish_ziemel_model.py (don't edit by hand). Texture: textures/entity/fish/ziemel.png (%d x %d).
 */
public class ZiemelModel extends FishModel {
    private final ModelPart[] parts;
    private final float[] restY;
    private final ModelPart tail;
    private final ModelPart dorsalFin;

    public ZiemelModel(ModelPart root) {
        super(root);
        this.parts = new ModelPart[] {root.getChild("body"), root.getChild("tail"), root.getChild("tail_fin")};
        this.restY = new float[parts.length];
        for (int i = 0; i < parts.length; i++) {
            restY[i] = parts[i].y;
        }
        this.tail = root.getChild("tail");
        this.dorsalFin = root.getChild("tail_fin");
    }

    @Override
    public void setupAnim(LivingEntityRenderState state) {
        super.setupAnim(state);
        if (!state.isInWater) {
            return;
        }
        float t = state.ageInTicks;
        float bob = 0.65F * Mth.sin(t * 0.1257F);
        for (int i = 0; i < parts.length; i++) {
            parts[i].y = restY[i] + bob;
        }
        dorsalFin.yRot = 0.2F * Mth.sin(t * 2.1F);
        tail.yRot = 0.0F;
        tail.xRot = -0.12F * (0.5F + 0.5F * Mth.sin(t * 0.1257F + 1.5F));
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
%s
        return LayerDefinition.create(mesh, %d, %d);
    }
}
""" % (TW, TH, "\n".join(lines), TW, TH)
    with open(JAVA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src)


# --- offline previews: an orthographic texel splatter with vanilla-like face shading ----------------------------------
SHADE = {"top": 1.0, "bottom": 0.5, "north": 0.8, "south": 0.8, "west": 0.6, "east": 0.6}


def rot_y(p, a):
    x, y, z = p
    c, s = math.cos(a), math.sin(a)
    return (x * c + z * s, y, -x * s + z * c)


def render(cubes, texel_fn, view, scale, yrots=None, sub=4):
    """Draw cubes from 'side' (from -x, head left), 'three' (front three-quarter), 'front' (from -z) or 'top'.
    texel_fn(cube) yields (face, colour, (x, y, z)); yrots: part -> (pivot, angle) to pose a swing frame."""
    yaw, pitch = {"side": (0.0, 0.0), "three": (35.0, 20.0), "front": (90.0, 0.0), "top": (0.0, 90.0)}[view]
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def project(p):
        x, y, z = p
        z2, x2 = z * cy + x * sy, -z * sy + x * cy
        y3, d3 = y * cp - x2 * sp, y * sp + x2 * cp
        return z2, y3, d3

    pts = []
    for cube in cubes:
        part = cube[1]
        for face, col, (x, y, z) in texel_fn(cube):
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
                    if yrots and part in yrots:
                        (px, py, pz), ang = yrots[part]
                        q = rot_y((p[0] - px, p[1] - py, p[2] - pz), ang)
                        p = (q[0] + px, q[1] + py, q[2] + pz)
                    pts.append((project(p), col))
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


def ziemel_texels(texture):
    def fn(cube):
        for face, u, v, x, y, z in face_texels(cube):
            col = texture.getpixel((u, v))
            if col[3] >= 128:
                yield face, col, (x, y, z)
    return fn


# vanilla cod, as measured from the 26.3 client (CodModel), for scale: (pos, size, texOffs); fins left out
COD = [((-1, 20, 0), (2, 4, 7), (0, 0)), ((-1, 20, -3), (2, 4, 3), (11, 0)), ((-1, 20, -4), (2, 3, 1), (0, 0)),
       ((0, 20, 7), (0, 4, 4), (22, 3)), ((0, 19, -1), (0, 1, 6), (20, -6))]


def cod_texels(texture):
    def fn(cube):
        _, _, (x0, y0, z0), (w, h, d), (u, v) = cube
        x1, y1, z1 = x0 + w, y0 + h, z0 + d
        out = []
        for c in range(w):
            for r in range(d):
                out.append(("top", u + d + c, v + r, (x0 + c + 0.5, y0, z1 - r - 0.5)))
        for c in range(d):
            for r in range(h):
                out.append(("west", u + c, v + d + r, (x0, y0 + r + 0.5, z1 - c - 0.5)))
        for c in range(w):
            for r in range(h):
                out.append(("north", u + d + c, v + d + r, (x0 + c + 0.5, y0 + r + 0.5, z0)))
        for face, uu, vv, p in out:
            col = texture.getpixel((uu % texture.size[0], vv % texture.size[1]))
            if col[3] >= 128:
                yield face, col, p
    return fn


def vanilla_texture(name):
    for jar in sorted(glob.glob(os.path.join(ROOT, ".art-runs", "*", ".gradle", "loom-cache", "minecraftMaven", "net",
                                             "minecraft", "minecraft-merged-*", "26.3", "*.jar"))):
        with zipfile.ZipFile(jar) as z:
            try:
                with z.open("assets/minecraft/textures/entity/fish/%s.png" % name) as fh:
                    return Image.open(fh).convert("RGBA").copy()
            except KeyError:
                continue
    return None


def previews(out_dir, texture):
    os.makedirs(out_dir, exist_ok=True)
    fn = ziemel_texels(texture)
    out = {}
    for view in ("side", "three", "front", "top"):
        out[view] = render(CUBES, fn, view, 16)
        out[view].save(os.path.join(out_dir, "ziemel_%s16.png" % view))
    swing = {"tail_fin": (PARTS["tail_fin"][1], -0.2)}
    out["swing"] = render(CUBES, fn, "three", 16, yrots=swing)
    out["swing"].save(os.path.join(out_dir, "ziemel_swing16.png"))
    cod = vanilla_texture("cod")
    if cod:
        row = [render(CUBES, fn, "side", 8),
               render([("c%d" % i, "p", p, s, t) for i, (p, s, t) in enumerate(COD)], cod_texels(cod), "side", 8)]
        im = Image.new("RGBA", (sum(i.width for i in row) + 40, max(i.height for i in row)), (72, 72, 72, 255))
        x = 0
        for i in row:
            im.paste(i, (x, im.height - i.height), i)
            x += i.width + 40
        out["scale"] = im
        im.save(os.path.join(out_dir, "ziemel_scale8.png"))
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
        images = [i for i in images if i is not None]
        if not images:
            return
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

    ref_dir = os.path.join(ROOT, "art", "references", "fish_ziemel_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("h_gervais.jpg", "g_vigo.jpg", "h_arrabida.jpg", "g_aquarium.jpg", "g_head.jpg", "g_long.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    title("References (reference only): Gervais plate (rings, curl, fin); guttulatus golden with pale dots; "
          "hippocampus; filaments; head; full body")
    row(refs[:3], h=280)
    row(refs[3:], h=280)
    title("Offline model, 16x: side, three-quarter, front, top, three-quarter with the dorsal fin mid-flutter")
    row([pv["side"], pv["three"], pv["front"], pv["top"], pv["swing"]], align_bottom=True)
    if "scale" in pv:
        title("Same scale, 8x: ziemel (hitbox 0.4 x 0.8, 13 px tall) beside vanilla cod (0.5 x 0.3, 15 px long)")
        row([pv["scale"]])
    van = [t for t in (vanilla_texture("cod"), vanilla_texture("salmon")) if t]
    title("Texture at 8x and 1x: ziemel (32 x 32), vanilla cod and salmon (32 x 32)")
    row([texture.resize((TW * 8, TH * 8), Image.NEAREST), texture]
        + [t.resize((t.width * 8, t.height * 8), Image.NEAREST) for t in van] + van)
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        names = ("fish-ziemel-side", "fish-ziemel-three-quarter", "fish-ziemel-front", "fish-ziemel-on-land",
                 "fish-ziemel-beside-cod", "fish-ziemel-side-on-sand")
        got = [(n, shot(n)) for n in names]
        got = [(n, i) for n, i in got if i]
        if got:
            title("In the game: side, three-quarter, front, on land, beside vanilla cod (size), side on with the sand behind")
            row([i for _, i in got[:3]], h=330)
            row([i for _, i in got[3:]], h=330)
            title("The same, cropped to the fish")
            boxes = {"fish-ziemel-beside-cod": (0.1, 0.2, 0.9, 0.75), "fish-ziemel-on-land": (0.25, 0.3, 0.75, 0.75)}
            crops = []
            for n, i in got:
                fx = boxes.get(n, (0.3, 0.15, 0.7, 0.75))
                box = (int(i.width * fx[0]), int(i.height * fx[1]), int(i.width * fx[2]), int(i.height * fx[3]))
                k = 560.0 / (box[2] - box[0])
                crops.append(i.crop(box).resize((560, int((box[3] - box[1]) * k)), Image.NEAREST))
            row(crops[:3])
            row(crops[3:])
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_ziemel_model.png")
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
        sheet(args[args.index("--sheet") + 1], texture, prev or os.path.join(ROOT, "art", "candidates", "tmp_ziemel"))
    elif prev:
        previews(prev, texture)
        print("previews in", prev)


if __name__ == "__main__":
    main()
