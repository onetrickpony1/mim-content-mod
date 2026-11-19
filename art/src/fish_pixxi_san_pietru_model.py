"""The pixxi San Pietru (John Dory, Zeus faber) as a swimming mob: its 3D model and its texture.

Night job piece 1 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). Drawn from the
photos in art/references/fish_pixxi_san_pietru_refonly/ (list.tsv, Wikimedia Commons; jd05, jd09 and jd10 out of
water for the true colour, jd02 and jd08 swimming for the shape and the fins). What makes it a John Dory:
  - a very tall, very thin oval body, seen side on almost a disc: 18 px long and 11 tall without the fins, only 2 px
    thick (1 px at the jaw and the tail end); 22 px long with the tail, about 1.4 blocks, and about as tall as the
    cerna with the spines (bigger than life, like the other small fish);
  - St Peter's thumbprint: a soft mid brown-olive smudge a little above the middle of each side, a 3 x 3 core with a
    half-tone edge and no ring, clearly lighter than the eye's pupil, so it reads as a spot, never an eye (owner's
    rule: eyes must look different from all other marks);
  - the eye high on the head near the front: a 2 x 2 near-black pupil in a round 1 px cream ring, the only ringed,
    high-contrast mark on the fish;
  - a big upturned jaw: a wedge of lower jaw jutting up and forward past the upper lip, a short dark gape;
  - a spiny dorsal: a dark membrane strip on the back with four 1 px spines swept back 45 degrees (each its own child
    part of top_fin), the front one longest, ending in thin filaments; a low soft dorsal and anal fin running back to
    a rounded tail, long pelvic fins under the throat;
  - olive-grey to golden: a darker olive back, golden-olive flanks and a pale belly (countershaded).
Every colour is a step lighter than the photos, because the game greys and darkens everything under water.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body", "top_fin" (the spiny dorsal fin, with its spines spine_0..3) and "tail_fin" that sways like vanilla
cod's.

Candidates (the same model, three paint jobs): A the spot with its half-tone edge all round; B the edge only at the
sides and below; C as A with faint wavy flank streaks as in the Mediterranean photo jd02. CHOSEN (B) is installed.
Model critic rounds: 7 (PASS in round 7).

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/PixxiSanPietruModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/pixxi_san_pietru.png    (64 x 64)
  art/candidates/pixxi_san_pietru_model/  (candidate textures and offline previews)
With --sheet SCREENSHOT_DIR also writes the review sheet art/candidates/fish_pixxi_san_pietru_model.png.

Run:  art/.venv/bin/python art/src/fish_pixxi_san_pietru_model.py [--sheet SCREENSHOT_DIR]
"""
import glob
import math
import os
import sys
import zipfile

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fish_sardina_model as sard  # noqa: E402  (the shared box-UV layout, the offline renderer, vanilla cod geometry)

ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "PixxiSanPietruModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "pixxi_san_pietru.png")
CAND = os.path.join(ROOT, "art", "candidates", "pixxi_san_pietru_model")
TW, TH = 64, 64
CHOSEN = "B"
VANILLA_JAR = "/home/cultar/Apps/Minecraft World/tools/gradle-home/caches/fabric-loom/26.3/minecraft-merged.jar"


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# Palette keys:
#   K back edge (dark olive), B back olive, b back to flank midtone, O olive-gold upper flank, G golden flank, L pale lower flank, W belly
#   S spot core, s spot edge, R spot ring, o faint flank streak
#   E eye pupil, I gold iris, c pale cheek, J pale lip, m mouth line, j jaw edge, g gill cover edge
#   d spine membrane, f spine, t filament tip, D soft fin, T tail, r tail ray, P pelvic fin, p pectoral fin
BASE = {
    "K": "#5b5641", "B": "#75704f", "b": "#8f875f", "O": "#ab9d66", "G": "#c3ae70", "L": "#e4ddc2", "W": "#f6f4ea",
    "S": "#6e5e3a", "s": "#9a8b5e", "R": "#cdbd8a", "o": "#958d66",
    "E": "#101010", "I": "#efe6c4", "c": "#d6d0b0", "J": "#d6cfb2", "m": "#4c4537", "j": "#a9a283", "g": "#958e6a",
    "d": "#4a4637", "f": "#5c5746", "t": "#b8b08c", "D": "#aaa27e", "T": "#bfb68c", "u": "#a89f7a", "r": "#807a5e",
    "P": "#7e775a", "n": "#6f6a55", "p": "#8a835f",
}
PALETTES = {"A": dict(BASE), "B": dict(BASE), "C": dict(BASE)}
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), zRot). Absolute: x across, y down (24 = ground), z head (-) to
# tail (+).
PARTS = {
    "body": (None, (0.0, 17.0, 0.0), 0.0),
    "top_fin": (None, (0.0, 12.0, -5.0), 0.0),
    "tail_fin": (None, (0.0, 17.0, 7.0), 0.0),
}
# The spiny dorsal (round 3, critic: loose antennae): a dark membrane sail on the back (top_fin) with four spines, each
# its own child part hinged at its base on the membrane's top edge and swept back 45 degrees, so they stay joined to
# the fin and trail toward the tail. Round 4 (critic: uniform 2 px rods read as a hairbrush): 1 px wide, the front
# one longest (round 5: 10, 9, 7, 6 px), each ending in a thin filament.
# (name, pivot z, pivot y, length)
SPINES = [("spine_0", -5, 10, 10), ("spine_1", -3, 10, 9), ("spine_2", -1, 11, 7), ("spine_3", 1, 11, 6)]
for _n, _z, _y, _l in SPINES:
    PARTS[_n] = ("top_fin", (0.0, float(_y), float(_z)), 0.0)
# The spiny dorsal leans back (a rotation about x, tips toward the tail), so its spines and filaments slant like the
# photos' instead of standing up as a comb. The offline renderer only knows z rotations, so it is taught this one here.
XROT = {n: -0.785 for n, _, _, _ in SPINES}


def _to_world(parts, part, p):
    while part:
        parent, pivot, zrot = parts[part]
        rel = (p[0] - pivot[0], p[1] - pivot[1], p[2] - pivot[2])
        if zrot:
            rel = sard.rot_z(rel, zrot)
        a = XROT.get(part, 0.0)
        if a:
            ca, sa = math.cos(a), math.sin(a)
            rel = (rel[0], rel[1] * ca - rel[2] * sa, rel[1] * sa + rel[2] * ca)
        p = (rel[0] + pivot[0], rel[1] + pivot[1], rel[2] + pivot[2])
        part = parent
    return p


sard.to_world = _to_world

# The body as columns along z: (z0, z1, top y, bottom y, thickness). A lens: 1 px steps top and bottom, the deepest
# from z -5 to 1, 2 px thick in the middle and 1 px at the snout and the tail end.
COLUMNS = [
    (-11, -10, 15, 16, 1),  # the tip of the big lower jaw: a wedge angled up and forward, 1 px deep at the tip
    (-10, -9, 15, 17, 1),   # 2 px deep at its base (round 4, critic: an upright nub read as a stick)
    (-9, -8, 15, 18, 1),    # the upper lip and the gape
    (-8, -7, 14, 20, 1),    # the snout
    (-7, -6, 13, 21, 2),    # the head with the eye
    (-6, -5, 13, 22, 2),    # the gill cover
    (-5, -4, 12, 22, 2),
    (-4, 1, 12, 23, 2),     # the deep middle of the disc (round 2: the belly rounded at both ends)
    (1, 2, 12, 22, 2),
    (2, 4, 13, 22, 2),
    (4, 5, 14, 21, 1),
    (5, 6, 15, 20, 1),
    (6, 7, 16, 19, 1),      # the tail stalk
]
SIDE_Z0, SIDE_Y0 = -11, 12

# The side of the fish, rows y 12..22, columns z -9..6 ('.' outside the body). Painted per candidate below from the
# column bands (countershading by height) plus the marks.
BANDS = {12: "K", 13: "B", 14: "b", 15: "O", 16: "O", 17: "G", 18: "G", 19: "L", 20: "L", 21: "W", 22: "W"}


def side_map(variant):
    rows = {}
    for y in range(12, 23):
        row = []
        for z in range(-11, 7):
            col = [c for c in COLUMNS if c[0] <= z < c[1]][0]
            if not (col[2] <= y < col[3]):
                row.append(".")
                continue
            ch = BANDS[y]
            if y == col[2]:
                ch = "K"                         # every column's top pixel is the dark back edge
            row.append(ch)
        rows[y] = row

    def put(z, y, ch):
        if rows[y][z - SIDE_Z0] != ".":
            rows[y][z - SIDE_Z0] = ch
    # the head: the eye high and forward, just under the dark back (z -7..-6, y 14..15): a 2 x 2 near-black pupil with
    # a pale silver rim on its top and back only, a bright edge the spot never has; no gold on either mark (round 5,
    # critic: the eye vanished under water and the spot read as the eye). A soft pale cheek in front of it.
    for z, y in ((-8, 17), (-7, 17), (-6, 17)):
        put(z, y, "c")
    for z, y in ((-7, 14), (-6, 14), (-7, 15), (-6, 15)):
        put(z, y, "E")
    # round 6 (critic): the rim made a full 1 px cream ring, bright enough to last under water, so the eye is the
    # only ringed, high-contrast mark on the fish
    # (its corners left out, so the ring is round, not a box)
    for z, y in ((-8, 14), (-8, 15), (-7, 13), (-6, 13), (-5, 14), (-5, 15), (-7, 16), (-6, 16)):
        put(z, y, "I")
    # the upturned jaw: a wedge of lower jaw a step darker than the cheek, angled up and forward, 2 px deep at its
    # base and 1 px at the tip, flush with the head; the short dark gape slants down and back above the chin
    put(-11, 15, "j")
    put(-10, 15, "j")
    put(-10, 16, "j")
    put(-9, 15, "c")
    put(-9, 16, "m")
    put(-9, 17, "j")
    put(-8, 18, "j")
    put(-8, 19, "j")
    put(-7, 19, "j")
    put(-7, 20, "j")
    # the gill cover's rear edge, a soft curved line behind the cheek
    for y in (16, 17, 18, 19, 20):
        put(-5, y, "g")
    put(-6, 21, "g")
    # St Peter's thumbprint, a little above the middle and behind the gill (centre z 0, y 16): a mid brown-olive
    # smudge, clearly lighter than the eye's pupil, with no ring (round 6, critic: under water a dark ringed disc
    # read as a second, bigger eye). A and C: a 3 x 3 core with a softer half-tone edge one pixel round it (its
    # corners left to the body, so it steps in); B: the same, the edge only at the sides and below.
    for z in range(-1, 2):
        for y in range(15, 18):
            put(z, y, "S")
    edge = [(-2, 15), (-2, 16), (-2, 17), (2, 15), (2, 16), (2, 17), (-1, 18), (0, 18), (1, 18)]
    if variant != "B":
        edge += [(-1, 14), (0, 14), (1, 14)]
    for z, y in edge:
        put(z, y, "s")
    if variant == "C":
        # faint wavy streaks along the flank, well clear of the eye and the spot
        for z, y in ((1, 14), (2, 14), (3, 15), (4, 15), (2, 19), (3, 19), (4, 18), (-3, 20), (-2, 20), (-1, 21),
                     (0, 21)):
            put(z, y, "o")
    return {y: "".join(r) for y, r in rows.items()}


# Fins: one character per pixel, rows by absolute y, columns by absolute z.
# The membrane strip on the back (top_fin): z -5..1, y 10..11, darker, its top edge stepping down toward the tail.
MEMB_Z0, MEMB_Y0 = -5, 10
MEMB = [
    "dddd...",
    "ddddddd",
]
# each spine, from its base up: dark (f) and 2 px wide for the lower third, then 1 px; the top 3 px a thin, slightly
# lighter filament (n), never a pale cap (round 3, critic: pale tips read as match heads)


def spine_key(length, up, back):
    """up: px above the base (0 = the base row); back: 0 the front column, 1 the back one."""
    return "n" if up >= length - 2 else "f"


# the soft dorsal behind it: z 2..5, low along the sloping back
SOFT_Z0, SOFT_Y0 = 2, 10
SOFT = [
    "DD..",
    "DDD.",
    "DDDD",
    "..DD",
    "...D",
]
# the anal fin under the rear: z -1..5, y 20..23 (a short spiny front, then the soft fin)
ANAL_Z0, ANAL_Y0 = -1, 20
ANAL = [
    "......D",
    ".....DD",
    "..DDDDD",
    "ffDDD..",
]
# the long pelvic fins under the throat, trailing back: z -6..-3, y 22..23 (round 3: thinner and paler)
PELVIC_Z0, PELVIC_Y0 = -6, 22
PELVIC = [
    "PP..",
    ".PPP",
]
# the rounded tail fan: z 7..10, y 13..20
CAUDAL_Z0, CAUDAL_Y0 = 7, 13
CAUDAL = [
    ".TT.",
    "TTT.",
    "TTTr",
    "TTTr",
    "uuur",
    "uuu.",
    ".uu.",
]


def body_cubes():
    out = []
    for i, (z0, z1, top, bot, th) in enumerate(COLUMNS):
        out.append(("col%d" % i, "body", None, (-th / 2.0, float(top), float(z0)), (th, bot - top, z1 - z0)))
    return out


FIN_CUBES = [
    ("membrane", "top_fin", None, (0.0, 10.0, -5.0), (0, 2, 7)),
] + [(n, n, None, (0.0, float(y - l), float(z)), (0, l, 1)) for n, z, y, l in SPINES] + [
    ("soft_dorsal", "body", None, (0.0, 10.0, 2.0), (0, 5, 4)),
    ("anal", "body", None, (0.0, 20.0, -1.0), (0, 4, 7)),
    ("pelvic", "body", None, (0.0, 22.0, -6.0), (0, 2, 4)),
    ("caudal", "tail_fin", None, (0.0, 13.0, 7.0), (0, 7, 4)),
]


def footprint(cube):
    _, _, _, _, (w, h, d) = cube
    w, h, d = int(math.ceil(w)), int(math.ceil(h)), int(math.ceil(d))
    if w == 0:
        return 2 * d, h
    if h == 0:
        return 2 * w, d
    return 2 * d + 2 * w, d + h


def pack(cubes):
    """Shelf-pack the cubes' texture areas into the TW x TH texture, in list order (deterministic)."""
    out, x, y, shelf = [], 0, 0, 0
    for cube in cubes:
        fw, fh = footprint(cube)
        if x + fw > TW:
            x, y, shelf = 0, y + shelf, 0
        assert y + fh <= TH, ("texture full", cube[0])
        out.append((cube[0], cube[1], (x, y), cube[3], cube[4]))
        x += fw
        shelf = max(shelf, fh)
    return out


CUBES = pack(body_cubes() + FIN_CUBES)


def pal(variant):
    return {k: hexc(v) for k, v in PALETTES[variant].items()}


def body_colour(side, P, face, y, z, x0, y0, z0, w, h, d):
    zi, yi = int(math.floor(z)), int(math.floor(y))
    if face == "top":
        return P["K"]
    if face == "bottom":
        return P["L"]          # round 6: the underside a shaded pale, no glowing white pixel under water
    if face in ("west", "east"):
        ch = side[yi][zi - SIDE_Z0]
        return P["G" if ch == "." else ch]
    if face == "north":
        ch = side[yi][int(math.floor(z0)) - SIDE_Z0]
    else:
        ch = side[yi][int(math.floor(z0 + d - 1)) - SIDE_Z0]
    # the ends of a section: its band colour, never a mark
    ch = BANDS[yi] if ch in "EIcJmjgSsRo" else ch
    return P[ch]


def fin_colour(P, name, y, z):
    zi, yi = int(math.floor(z)), int(math.floor(y))
    for n, sz, sy, sl in SPINES:
        if name == n:
            ch = spine_key(sl, sy - 1 - yi, zi - sz)
            return CLEAR if ch == "." else P[ch]
    table = {"membrane": (MEMB, MEMB_Z0, MEMB_Y0), "soft_dorsal": (SOFT, SOFT_Z0, SOFT_Y0),
             "anal": (ANAL, ANAL_Z0, ANAL_Y0), "pelvic": (PELVIC, PELVIC_Z0, PELVIC_Y0),
             "caudal": (CAUDAL, CAUDAL_Z0, CAUDAL_Y0)}
    if name in table:
        grid, gz, gy = table[name]
        ch = grid[yi - gy][zi - gz]
    else:
        ch = "p"
    return CLEAR if ch == "." else P[ch]


def draw_texture(variant):
    P = pal(variant)
    side = side_map(variant)
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in CUBES:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in sard.face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if w == 0 or h == 0:
                c = fin_colour(P, name, y, z)
            else:
                c = body_colour(side, P, face, y, z, x0, y0, z0, w, h, d)
            img.putpixel((u, v), c)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def fnum(v):
    return sard.f(v)


def write_java():
    lines = []
    for part in PARTS:
        parent, (px, py, pz), zrot = PARTS[part]
        builder = "CubeListBuilder.create()"
        for cube in [c for c in CUBES if c[1] == part]:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = sard.tex_offset(cube)
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %s, %s, %s)" % (
                name, u, v, fnum(x0 - px), fnum(y0 - py), fnum(z0 - pz), fnum(w), fnum(h), fnum(d))
        xrot = XROT.get(part, 0.0)
        # a child's pivot is given from its parent's (the parents here are never rotated)
        ox, oy, oz = (0.0, 0.0, 0.0) if parent is None else PARTS[parent][1]
        qx, qy, qz = px - ox, py - oy, pz - oz
        if zrot or xrot:
            pose = "PartPose.offsetAndRotation(%s, %s, %s, %s, 0.0F, %s)" % (fnum(qx), fnum(qy), fnum(qz), fnum(xrot),
                                                                            fnum(zrot))
        else:
            pose = "PartPose.offset(%s, %s, %s)" % (fnum(qx), fnum(qy), fnum(qz))
        holder = "root" if parent is None else parent.replace("_", "") + "Part"
        decl = "PartDefinition %sPart = " % part.replace("_", "") if part == "top_fin" else ""
        lines.append("        %s%s.addOrReplaceChild(\"%s\", %s,\n            %s);" % (decl, holder, part, builder, pose))
    body = "\n".join(lines)
    src = """package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The pixxi San Pietru (John Dory): a very tall, thin oval disc, olive-grey to golden with a pale belly, St Peter's
 * dark ringed thumbprint in the middle of each side, a small gold-ringed eye high near the front, a big upturned jaw,
 * long dorsal spines trailing filaments, a low soft dorsal and anal fin, long dark pelvic fins and a rounded tail that
 * sways as it swims. Head toward -z, the ground at y 24.
 * Made by art/src/fish_pixxi_san_pietru_model.py (don't edit by hand). Texture: textures/entity/fish/pixxi_san_pietru.png (%d x %d).
 */
public class PixxiSanPietruModel extends FishModel {
    public PixxiSanPietruModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
%s
        return LayerDefinition.create(mesh, %d, %d);
    }
}
""" % (TW, TH, body, TW, TH)
    with open(JAVA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src)


# --- previews and the review sheet ------------------------------------------------------------------------------------
def vanilla_png(path):
    try:
        with zipfile.ZipFile(VANILLA_JAR) as z, z.open(path) as fh:
            return Image.open(fh).convert("RGBA").copy()
    except (OSError, KeyError):
        return None


def on_bg(img, bg=(72, 72, 72, 255), pad=4):
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), bg)
    out.alpha_composite(img, (pad, pad))
    return out


def hstack(images, gap=20, bg=(72, 72, 72, 255), bottom=True):
    H = max(i.height for i in images)
    out = Image.new("RGBA", (sum(i.width for i in images) + gap * (len(images) - 1), H), bg)
    x = 0
    for i in images:
        out.alpha_composite(i, (x, H - i.height if bottom else (H - i.height) // 2))
        x += i.width + gap
    return out


def write_candidates():
    os.makedirs(CAND, exist_ok=True)
    cod = vanilla_png("assets/minecraft/textures/entity/fish/cod.png")
    for v in PALETTES:
        tex = draw_texture(v)
        tex.save(os.path.join(CAND, "texture_%s.png" % v))
        views = [on_bg(sard.render(CUBES, PARTS, tex, view, 12)) for view in ("side", "three", "top")]
        hstack(views, bottom=False).save(os.path.join(CAND, "preview_%s.png" % v))
    if cod:
        cc = sard.vanilla_cubes(sard.COD_CUBES)
        row = [on_bg(sard.render(CUBES, PARTS, draw_texture(CHOSEN), "side", 12)),
               on_bg(sard.render(cc, sard.COD_PARTS, cod, "side", 12))]
        hstack(row).save(os.path.join(CAND, "scale_vs_cod.png"))


def sheet(shots_dir):
    from PIL import ImageFont
    try:
        sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
        from font import label_font
        font = label_font(15)
    except Exception:  # noqa: BLE001
        font = ImageFont.load_default()
    W = 1800
    blocks = []

    def title(t):
        im = Image.new("RGBA", (W, 28), (40, 40, 40, 255))
        ImageDraw.Draw(im).text((8, 5), t, fill=(240, 240, 240, 255), font=font)
        blocks.append(im)

    def row(images, h=None, gap=14):
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images)
        im = Image.new("RGBA", (W, hh + 8), (72, 72, 72, 255))
        x = 8
        for i in images:
            if x + i.width > W:
                break
            im.alpha_composite(i, (x, 4 + (hh - i.height) // 2))
            x += i.width + gap
        blocks.append(im)

    title("Candidates A, B, C (offline, 12x: side, three-quarter, top); chosen: " + CHOSEN)
    for v in PALETTES:
        row([Image.open(os.path.join(CAND, "preview_%s.png" % v)).convert("RGBA")])
    if os.path.exists(os.path.join(CAND, "scale_vs_cod.png")):
        title("Same scale offline, 12x: this fish, vanilla cod")
        row([Image.open(os.path.join(CAND, "scale_vs_cod.png")).convert("RGBA")])
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None
        names = ["fish-pixxi_san_pietru-side", "fish-pixxi_san_pietru-three-quarter", "fish-pixxi_san_pietru-top",
                 "fish-pixxi_san_pietru-beside-cod", "fish-pixxi_san_pietru-on-land", "fish-pixxi_san_pietru-lineup"]
        present = [(n, shot(n)) for n in names]
        present = [(n, i) for n, i in present if i]
        if present:
            title("In the game: side, three-quarter, top; beside vanilla cod, on land, lineup (this fish, cod, cerna, small tonn)")
            row([i for _, i in present[:3]], h=330)
            row([i for _, i in present[3:]], h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_pixxi_san_pietru_model.png")
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    texture = draw_texture(CHOSEN)
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    texture.save(TEXTURE)
    write_java()
    write_candidates()
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT), "candidates in",
          os.path.relpath(CAND, ROOT))
    args = sys.argv[1:]
    if "--sheet" in args:
        sheet(args[args.index("--sheet") + 1])


if __name__ == "__main__":
    main()
