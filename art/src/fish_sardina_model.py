"""The sardina (European sardine, Sardina pilchardus) as a swimming mob: its 3D model and its texture.

Drawn from the reference photos in art/references/fish_sardina_refonly/ (list.tsv). What makes it a sardina:
  - a small, slim, torpedo-shaped body with a straight back and a pointed head (smaller than vanilla cod),
  - a blue-green back over bright silver sides and a white belly,
  - a cyan sheen along the flank with two dark spots just behind the gill cover,
  - a gold-tinged gill cover and a big eye with a pale ring,
  - one short dorsal fin in the middle of the back, small pelvic and anal fins under the belly,
  - a forked tail, darker at the tips.

Size: the hitbox is 0.4 x 0.25 blocks (6.4 x 4 model pixels). Vanilla's models run about 1.9 to 2.2 times their
hitbox width in length (cod 15 px on 8, salmon 25 px on 11.2), so the sardina is 14 px long (11 of body, 3 of tail)
and 3 px deep, 2 px wide like cod: shorter and slimmer than cod's 15 x 4. Body depth to body length is 3 to 11
(0.27), against the tonn's 10 to 26 (0.38) and cod's 4 to 11: the slimmest fish of the three, as the owner asked.
One texture pixel per model pixel, like vanilla's fish.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body" and a "tail_fin" that sways like vanilla cod's.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/SardinaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/sardina.png    (32 x 32)
Also writes offline previews (side, top, three-quarter, beside vanilla cod and salmon) to the scratch folder given
with --preview DIR, and the compare sheet with --sheet SCREENSHOT_DIR.

Run:  art/.venv/bin/python art/src/fish_sardina_model.py [--preview DIR] [--sheet SCREENSHOT_DIR]
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
                    "SardinaModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "sardina.png")
TW, TH = 32, 32


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# Colours picked from the references (the Gervais plate and the photos of live fish), in the family of the sardina
# item icon (textures/item/sardina.png). The silver and the gold are kept light and soft on purpose: under water the
# game tints everything blue-grey and darkens it, and saturated gold turns flat grey there.
BACK_DARK = hexc("#1c3b47")   # along the spine, the darkest blue
BACK = hexc("#24525e")        # the steel-blue back (the icon's back)
BACK_G = hexc("#3a7072")      # blue-green on the back, seen from the side
SILVER_B = hexc("#bccbd2")    # bluish silver shine
SILVER = hexc("#e0eaec")      # the bright silver sides
WHITE = hexc("#f6f8f5")       # the belly
GOLD = hexc("#dcbc62")        # the gold tinge on the gill cover (the icon's gill gold)
GOLD_D = hexc("#a88a44")      # the edge of the gill cover
SPOT = hexc("#5f7684")        # the spots behind the gill cover (the icon's), lighter than the eye so it stays the eye
SHEEN = hexc("#8cc6be")       # the cyan sheen along the flank, behind the gill cover (the icon's)
EYE = hexc("#0c1014")
RING = hexc("#f4f5ef")        # the pale ring round the big eye
MOUTH = hexc("#7d8a8a")
FIN = hexc("#b9c7ca")         # the pale pectoral, pelvic and anal fins
DORS = hexc("#5f8288")        # the dorsal fin, blue-grey like the back
DORS_D = hexc("#3b5862")      # its leading edge
TAIL = hexc("#5d717c")        # the tail near the body
TAIL_D = hexc("#2f3d48")      # the dark tail lobes (the icon's tail)
CLEAR = (0, 0, 0, 0)


# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), zRot). Cubes: (name, part, (U, V) top-left of the used texture
# area, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
PARTS = {
    "body": (None, (0.0, 20.0, 0.0), 0.0),
    "tail_fin": (None, (0.0, 21.0, 5.0), 0.0),
    "right_fin": (None, (-1.0, 22.5, -2.0), -0.7),
    "left_fin": (None, (1.0, 22.5, -2.0), 0.7),
}
CUBES = [
    # a pointed snout, a head with the big eye and gill cover, the trunk, a narrower rear to the tail
    ("snout", "body", (24, 0), (-1.0, 21.0, -6.0), (2, 2, 1)),
    ("head", "body", (14, 0), (-1.0, 20.0, -5.0), (2, 3, 3)),
    ("trunk", "body", (0, 0), (-1.0, 20.0, -2.0), (2, 3, 5)),
    ("rear", "body", (0, 8), (-1.0, 20.0, 3.0), (2, 2, 2)),
    # the short dorsal fin mid-back, the pelvic and anal fins under the belly
    ("dorsal", "body", (14, 8), (0.0, 18.0, -1.0), (0, 2, 3)),
    ("pelvic", "body", (14, 11), (0.0, 23.0, 1.0), (0, 1, 1)),
    ("anal", "body", (18, 11), (0.0, 22.0, 3.0), (0, 1, 2)),
    # the forked tail
    ("caudal", "tail_fin", (8, 13), (0.0, 18.5, 5.0), (0, 5, 3)),
    # the pectoral fins, low behind the gill cover, spread down and out like vanilla cod's
    ("pec_r", "right_fin", (22, 8), (-2.0, 22.5, -2.0), (1, 0, 2)),
    ("pec_l", "left_fin", (26, 8), (1.0, 22.5, -2.0), (1, 0, 2)),
]

# Each body section's side rows, top to bottom.
SECTION_ROWS = {
    "snout": [BACK_G, SILVER],
    "head": [BACK, SILVER, SILVER],
    "trunk": [BACK, SILVER, WHITE],
    "rear": [BACK, SILVER],
}

# Fin outlines, by absolute z (column) and y (row), as text: one character per pixel.
#   o fin colour, d dark tip, .clear
# the dorsal fin, rows y 18..19, columns z -1..1: a tall leading edge, sloping back
DORSAL = [
    "dd.",
    "doo",
]
# the forked tail, rows y 18.5..23.5, columns z 5..7 (z 5 against the rear): solid lobes, dark at the tips
CAUDAL = [
    "..d",
    ".dd",
    "oo.",
    ".dd",
    "..d",
]
# the pectoral fin, columns x (out from the body), rows z (front to back)
PECTORAL = ["o", "o"]


def body_colour(name, face, x, y, z, x0, y0, z0, w, h, d):
    """The colour of one texel of a body section, from where it sits on the fish."""
    rows = SECTION_ROWS[name]
    zi = int(math.floor(z))
    if face == "top":
        # the back seen from above: dark blue along the spine, a little darker every third pixel like scale rows
        if name == "snout":
            return BACK_G
        return BACK_DARK if zi % 3 == 0 else BACK
    if face == "bottom":
        return WHITE
    r = int(y - y0)
    c = rows[r]
    if face == "north":
        if name == "snout":
            return MOUTH if r == 1 else BACK_G
        return c                                        # the head's front, round the snout
    if face == "south":
        return c
    if name == "snout":
        return SILVER_B if r == 1 else BACK_G           # the lower jaw under a blue-green snout
    if name == "head":
        # columns z -5, -4, -3: the big eye with its pale ring, then the soft gold gill cover with a darker edge
        if r == 0:
            return BACK_G
        if r == 1:
            return (EYE, RING, GOLD)[zi + 5]
        return (RING, GOLD, GOLD_D)[zi + 5]
    if name == "trunk":
        if r == 0:
            return BACK_G
        if r == 1:
            # the cyan sheen along the flank, with two spots only, in the columns nearest the gill cover
            return SPOT if zi in (-2, 0) else SHEEN
        return WHITE
    if name == "rear":
        if r == 0:
            return BACK_G
        return SILVER_B                                 # the silver dulls toward the tail
    return c


def fin_colour(name, x, y, z):
    """The colour of one fin texel, or CLEAR outside the fin's outline."""
    zi, yi = int(math.floor(z)), int(math.floor(y))
    if name == "dorsal":
        ch = DORSAL[yi - 18][zi + 1]
        return {"o": DORS, "d": DORS_D, ".": CLEAR}[ch]
    if name in ("pelvic", "anal"):
        return FIN                                      # solid 1 px strips: the pelvic fin under the trunk, the anal fin under the rear
    if name == "caudal":
        ch = CAUDAL[int(math.floor(y - 18.5))][zi - 5]
        return {"o": TAIL, "d": TAIL_D, ".": CLEAR}[ch]
    ch = PECTORAL[zi + 2][0]
    return {"o": FIN, ".": CLEAR}[ch]


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
        parent, (px, py, pz), zrot = PARTS[part]
        builder = "CubeListBuilder.create()"
        for cube in [c for c in CUBES if c[1] == part]:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = tex_offset(cube)
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %d.0F, %d.0F, %d.0F)" % (
                name, u, v, f(x0 - px), f(y0 - py), f(z0 - pz), w, h, d)
        if zrot:
            pose = "PartPose.offsetAndRotation(%s, %s, %s, 0.0F, 0.0F, %s)" % (f(px), f(py), f(pz), f(zrot))
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
 * The sardina (sardine): small and slim, a blue-green back over bright silver sides, a row of dark spots behind the
 * gold-tinged gill cover, a big eye, one short dorsal fin mid-back, small pelvic and anal fins and a forked tail that
 * sways as it swims. 14 px long, 3 px deep, head toward -z, the ground at y 24.
 * Made by art/src/fish_sardina_model.py (don't edit by hand). Texture: textures/entity/fish/sardina.png (32 x 32).
 */
public class SardinaModel extends FishModel {
    public SardinaModel(ModelPart root) {
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
        img.save(os.path.join(out_dir, "sardina_%s16.png" % view))
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
        im.save(os.path.join(out_dir, "sardina_scale8.png"))
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

    ref_dir = os.path.join(ROOT, "art", "references", "fish_sardina_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("drawing_gervais.jpg", "side_3_italy.jpg", "sardinia.jpg", "side_1.jpg", "sardina_galicia.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    title("References (reference only): Gervais plate (fins, colours); a young fish in the hand; spot row; a school; a catch")
    row(refs[:3], h=260)
    row(refs[3:], h=260)
    title("Offline model, 16x: side, three-quarter, top (vanilla face shading only)")
    row([pv["side"], pv["three"], pv["top"]])
    if "scale" in pv:
        title("Same scale, 8x: sardina (hitbox 0.4 x 0.25), vanilla cod (0.5 x 0.3), vanilla salmon (0.7 x 0.4)")
        row(pv["scale"], align_bottom=True, gap=40)
    van = [t for t in (vanilla_texture("cod"), vanilla_texture("salmon")) if t]
    title("Texture at 8x and 1x: sardina (32 x 32), vanilla cod and salmon (32 x 32)")
    row([texture.resize((TW * 8, TH * 8), Image.NEAREST), texture]
        + [t.resize((t.width * 8, t.height * 8), Image.NEAREST) for t in van] + van)
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        names = ("fish-sardina-side", "fish-sardina-three-quarter", "fish-sardina-top", "fish-sardina-on-land",
                 "fish-sardina-beside-cod")
        imgs = [shot(n) for n in names]
        imgs = [i for i in imgs if i]
        if imgs:
            title("In the game: the sardina alone (side close-up, three-quarter, top, on land), and beside vanilla cod")
            row(imgs[:3], h=330)
            row(imgs[3:], h=330)
            title("The same, cropped to the fish (beside cod: sardina left, cod right)")
            boxes = {"fish-sardina-beside-cod": (0.06, 0.25, 0.94, 0.6)}
            crops = []
            for n, i in zip([n for n in names if shot(n)], imgs):
                fx = boxes.get(n, (0.3, 0.25, 0.7, 0.6))
                box = (int(i.width * fx[0]), int(i.height * fx[1]), int(i.width * fx[2]), int(i.height * fx[3]))
                k = 580.0 / (box[2] - box[0])
                crops.append(i.crop(box).resize((580, int((box[3] - box[1]) * k)), Image.NEAREST))
            row(crops[:3])
            row(crops[3:])
        title("In the game: the shared tank (cod, salmon, sardina, ...), and on land")
        imgs = [shot(n) for n in ("fish-02-tank-cod-salmon-sardina", "fish-01-tank-all", "fish-06-on-land")]
        imgs = [i for i in imgs if i]
        if imgs:
            row(imgs, h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_sardina_model.png")
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
        sheet(args[args.index("--sheet") + 1], texture, prev or os.path.join(ROOT, "art", "candidates", "tmp_sardina"))
    elif prev:
        previews(prev, texture)
        print("previews in", prev)


if __name__ == "__main__":
    main()
