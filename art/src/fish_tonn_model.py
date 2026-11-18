"""The tonn (Atlantic bluefin tuna, Thunnus thynnus): the swimming model and its texture.

Shape and colours from the reference photos in art/references/fish_tonn_refonly/ (list.tsv): a big, thick torpedo,
deepest a little before the middle, a pointed snout; a deep blue-black back, a metallic blue line along the side,
silver lower sides with faint pale streaks and a silver-white belly; a short spiny first dorsal fin (dull gold), a short
pointed second dorsal (dark brown) and an anal fin below it; a row of small yellow finlets along the back and belly
toward the tail; a slim tail stalk with dark keels; a stiff, tall crescent tail; short dark pectoral fins.

Size: vanilla models are about 1.75 (cod) to 2.2 (salmon) times as long as their hitbox is wide, and their body about
0.8 of the hitbox height. The tonn's hitbox is 1.3 x 0.7, so the model is 39 px long (2.4 blocks) and 10 px deep.

The body is a row of boxes stepping down toward both ends; the fins are flat planes whose outline is cut by the
texture. Every texel is painted from where it sits on the fish (model coordinates), so the steps share one colour
scheme. Follows the fish model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): root child "body",
"tail" (the slim back end, swaying gently) holding "tail_fin" (the crescent, swaying more).

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/TonnModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/tonn.png      (64 x 64)
Run:   art/.venv/bin/python art/src/fish_tonn_model.py
Sheet: art/.venv/bin/python art/src/fish_tonn_model.py --sheet <vanilla fish textures dir> <in-game screenshots dir>
       -> art/candidates/fish_tonn_model.png
"""
import math
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish", "TonnModel.java")
PNG = os.path.join(RES, "textures", "entity", "fish", "tonn.png")
TEX = 64
AXIS = 19.0  # the body's middle line (model y, down); the belly touches the ground at 24 like vanilla cod


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


C = {k: hexrgb(v) for k, v in {
    "back_dark": "#111a2c",   # the ridge of the back, blue-black
    "back": "#18264a",        # deep blue back
    "back_lit": "#1f3058",
    "line": "#3a68a6",        # the metallic blue line
    "line_lit": "#5788c2",
    "fade": "#6d8098",        # blue-grey where the back meets the silver
    "silver": "#a7b2bd",
    "streak": "#c8d0d7",      # the faint pale streaks of the lower sides
    "belly": "#e2e6e7",
    "belly_shade": "#cdd4d8",
    "cheek": "#9aa6b1",       # the gill cover, a little greyer
    "gill": "#7d8a98",
    "mouth": "#3b4350",
    "eye": "#0c0d12",
    "iris": "#b9ad7e",
    "d1": "#9a8550",          # first dorsal: dull gold, with darker spines
    "d1_spine": "#6a5a36",
    "d2": "#4e3d33",          # second dorsal: dark brown
    "d2_edge": "#33292a",
    "anal": "#cdc8aa",        # anal fin: silvery yellow (light enough to read under water), darker edge
    "anal_edge": "#77735f",
    "finlet": "#fae26e",      # the yellow finlets: light and soft so they stay yellow under water
    "finlet_dark": "#a8861c",
    "keel": "#191c24",
    "tail": "#283247",        # tail: dark slate blue
    "tail_lit": "#37445c",
    "tail_edge": "#1b2232",
    "pec": "#1d2940",
    "pec_lit": "#2d3b56",
}.items()}


def hash01(x, y, seed=0):
    v = math.sin(x * 127.1 + y * 311.7 + seed * 74.7) * 43758.5453
    return v - math.floor(v)


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---------------------------------------------------------------- shape
# A part: name, parent, pivot (x, y, z), rotation (x, y, z) in radians, cubes. A cube: (role, x, y, z, w, h, d), in the
# part's own space, model pixels (16 = one block), head toward -z, y down.

def parts():
    a = AXIS
    body = [
        ("nose", -1.5, -1.5, -19, 3, 3, 2),
        ("head", -2.5, -3.5, -17, 5, 7, 4),
        ("shoulder", -3.5, -4.5, -13, 7, 9, 4),
        ("main", -3.5, -5, -9, 7, 10, 11),
        ("rear1", -2.5, -4, 2, 5, 8, 4),
        ("rear2", -2, -3, 6, 4, 6, 4),
        # fins: flat planes on the middle line (x 0), outline cut by the texture
        ("dorsal1", 0, -8, -9, 0, 3, 7),        # on the back (y 14): 3 px of short spines, lower toward the back
        ("dorsal2", 0, -8, 1, 0, 4, 4),         # behind it: short, pointed, swept back
        ("anal", 0, 4, 2, 0, 3, 4),             # under the belly, matching the second dorsal
        ("finlets_top", 0, -4, 5, 0, 1, 5),     # the yellow finlets, one row above the back...
        ("finlets_bottom", 0, 3, 6, 0, 1, 4),   # ...and one below the belly
    ]
    tail = [
        ("rear3", -1.5, -2, 0, 3, 4, 3),
        ("stalk", -1, -1, 3, 2, 2, 2),
        ("keel", -2, 0, 3, 4, 0, 2),            # the keels on the tail stalk: a flat plate sticking out each side
        ("finlets_top_t", 0, -3, 0, 0, 2, 5),
        ("finlets_bottom_t", 0, 1, 0, 0, 2, 5),
    ]
    fin = [("tail_fin", 0, -5.5, 0, 0, 11, 5)]
    pec = 0.3
    return [
        {"name": "body", "parent": None, "pivot": (0, a, 0), "rot": (0, 0, 0), "cubes": body},
        {"name": "right_fin", "parent": None, "pivot": (-3.55, a - 1, -12.5), "rot": (0, -pec, 0),
         "cubes": [("pectoral", 0, 0, 0, 0, 2, 4)]},
        {"name": "left_fin", "parent": None, "pivot": (3.55, a - 1, -12.5), "rot": (0, pec, 0),
         "cubes": [("pectoral", 0, 0, 0, 0, 2, 4)]},
        {"name": "tail", "parent": None, "pivot": (0, a, 10), "rot": (0, 0, 0), "cubes": tail},
        {"name": "tail_fin", "parent": "tail", "pivot": (0, 0, 5), "rot": (0, 0, 0), "cubes": fin},
    ]


# Fin outlines, as rows of the plane (top row first) and columns from front (-z) to back. "#" = fin, "s" = spine,
# "e" = edge, "y" = yellow finlet, "." = clear.
MASKS = {
    "dorsal1": [
        "s.s....",
        "s#s#s..",
        "s#s#s#s",
    ],
    "dorsal2": [
        "..e.",
        ".e#.",
        "e##.",
        "e###",
    ],
    "anal": [
        "e###",
        ".e##",
        "..e.",
    ],
    "finlets_top": [".y.y.", ],                 # z 5..10 above the back (y 15 over rear1 ends at z 6, then y 15 over rear2)
    "finlets_bottom": [".y.y"],                 # z 6..10 below the belly (y 22)
    "finlets_top_t": ["y.y..", "....y"],         # z 10..15: over rear3 (top 17) then the stalk (top 18)
    "finlets_bottom_t": ["...y.", ".y..."],      # under the stalk (bottom 20), then rear3 (bottom 21)
    "tail_fin": [
        "...ee",
        "...e#",
        "..e##",
        "..e#.",
        ".e##.",
        "e##..",
        ".e##.",
        "..e#.",
        "..e##",
        "...e#",
        "...ee",
    ],
    "pectoral": [
        "eeee",
        "##..",
    ],
    "keel": None,   # the keel plate: drawn by rule (outside the stalk only)
}


def mask_at(role, row, col):
    m = MASKS[role]
    if row < 0 or row >= len(m) or col < 0 or col >= len(m[row]):
        return "."
    return m[row][col]


# ---------------------------------------------------------------- texture

def face_texels(u, v, w, h, d):
    """Each face of a cube as (face, rect, texel -> local coords from the cube's min corner), following Minecraft's
    cube UV layout (ModelPart.Cube). Model y points down; "top" is the face at min y (the fish's back)."""
    return [
        ("top", (u + d, v, w, d), lambda i, j: (i + .5, 0.0, d - j - .5)),
        ("bottom", (u + d + w, v, w, d), lambda i, j: (i + .5, h, d - j - .5)),
        ("-x", (u, v + d, d, h), lambda i, j: (0.0, j + .5, d - i - .5)),
        ("-z", (u + d, v + d, w, h), lambda i, j: (i + .5, j + .5, 0.0)),
        ("+x", (u + d + w, v + d, d, h), lambda i, j: (w, j + .5, i + .5)),
        ("+z", (u + d + w + d, v + d, w, h), lambda i, j: (w - i - .5, j + .5, d)),
    ]


def side_colour(t, gz, gy, seed):
    """The flank, by height t (0 = the top of this step, 1 = its bottom) and place along the fish."""
    zc, yc = math.floor(gz), math.floor(gy)
    n = hash01(zc, yc, seed)
    if t < 0.13:
        return C["back_dark"]
    if t < 0.38:
        return C["back_lit"] if n > 0.78 else C["back"]
    if t < 0.48:
        return C["line_lit"] if (zc % 4 == 1 and n > 0.3) else C["line"]
    if t < 0.58:
        return C["fade"]
    if t < 0.79:
        return C["streak"] if (zc % 3 == 0 and n > 0.25) else C["silver"]
    return C["belly"]


def body_colour(role, face, lx, ly, lz, cube, gx, gy, gz):
    _r, _x, _y, _z, w, h, d = cube
    if face == "top":
        edge = abs(lx - w / 2) > w / 2 - 1
        n = hash01(math.floor(gx), math.floor(gz), 3)
        if edge and w > 2:
            return C["back_lit"] if n > 0.6 else C["back"]
        return C["back"] if n > 0.8 else C["back_dark"]
    if face == "bottom":
        edge = abs(lx - w / 2) > w / 2 - 1
        return C["belly_shade"] if edge and w > 2 else C["belly"]
    t = ly / h
    zc, yc = math.floor(gz), math.floor(gy)
    if face in ("-x", "+x"):
        # the eye, a little above the middle line, a third of the way back along the head
        if role == "head" and zc == -16 and yc == 18:
            return C["eye"]
        if role == "head" and zc == -15 and yc == 18:
            return C["iris"]
        # the mouth: a dark line from the snout tip back under the eye
        if role == "nose" and yc == 20:
            return C["mouth"]
        if role == "head" and zc == -17 and yc == 20:
            return C["mouth"]
        # the gill cover: greyer cheek, its back edge a darker curve
        if role == "head" and t > 0.45:
            return C["gill"] if zc == -14 and yc >= 19 else C["cheek"]
        if role == "shoulder" and zc == -13 and yc == 18:
            return C["gill"]
    if face == "-z" and role == "nose":
        return C["mouth"] if yc == 20 else side_colour(t, gz, gy, 5)
    return side_colour(t, gz, gy, 5)


def fin_colour(role, face, lx, ly, lz, gz, gy):
    if role == "keel":
        # a flat plate at the stalk's middle line, seen only where it sticks out past the stalk (x beyond +-1)
        if abs(lx - 2) <= 1:
            return None
        return C["keel"]
    k = mask_at(role, math.floor(ly), math.floor(lz))
    if k == ".":
        return None
    if role == "dorsal1":
        return C["d1_spine"] if k == "s" else C["d1"]
    if role == "dorsal2":
        return C["d2_edge"] if k == "e" else C["d2"]
    if role == "anal":
        return C["anal_edge"] if k == "e" else C["anal"]
    if role.startswith("finlets"):
        return C["finlet"]
    if role == "tail_fin":
        if k == "e":
            return C["tail_edge"]
        return C["tail_lit"] if math.floor(ly) in (4, 5, 6) else C["tail"]
    if role == "pectoral":
        return C["pec"] if k == "e" else C["pec_lit"]
    raise ValueError(role)


FLAT = ("dorsal1", "dorsal2", "anal", "finlets_top", "finlets_bottom", "finlets_top_t", "finlets_bottom_t",
        "tail_fin", "pectoral", "keel")


def used_rect(cube):
    """The part of the cube's UV footprint that holds visible faces (a flat plane uses only two faces)."""
    _r, _x, _y, _z, w, h, d = cube
    if w == 0:
        return (0, d), (2 * d, h)        # offset inside the footprint, size
    if h == 0:
        return (d, 0), (2 * w, d)
    return (0, 0), (2 * d + 2 * w, d + h)


def pack(sizes, width):
    """Shelf packing, tallest first; returns positions in input order and the height used."""
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


def layout():
    ps = parts()
    cubes = [(pi, c) for pi, p in enumerate(ps) for c in p["cubes"]]
    rects = [used_rect(c) for _pi, c in cubes]
    pos, height = pack([r[1] for r in rects], TEX)
    assert height <= TEX, height
    offs = [(pos[k][0] - rects[k][0][0], pos[k][1] - rects[k][0][1]) for k in range(len(cubes))]
    return ps, cubes, offs


def part_origin(ps, p):
    """The part's pivot in model space (no rotation for the parts that have children)."""
    x, y, z = p["pivot"]
    if p["parent"]:
        q = next(pp for pp in ps if pp["name"] == p["parent"])
        px, py, pz = part_origin(ps, q)
        return x + px, y + py, z + pz
    return x, y, z


def build_texture():
    ps, cubes, offs = layout()
    img = np.zeros((TEX, TEX, 4), dtype=np.uint8)
    for k, (pi, cube) in enumerate(cubes):
        role, cx, cy, cz, w, h, d = cube
        ox, oy, oz = part_origin(ps, ps[pi])
        u, v = offs[k]
        for face, (fu, fv, fw, fh), m in face_texels(u, v, w, h, d):
            if fw == 0 or fh == 0:
                continue
            for j in range(fh):
                for i in range(fw):
                    lx, ly, lz = m(i, j)
                    gx, gy, gz = ox + cx + lx, oy + cy + ly, oz + cz + lz
                    if role in FLAT:
                        rgb = fin_colour(role, face, lx, ly, lz, gz, gy)
                        if rgb is None:
                            continue
                    else:
                        rgb = body_colour(role, face, lx, ly, lz, cube, gx, gy, gz)
                    img[fv + j, fu + i] = (*rgb, 255)
    return img


# ---------------------------------------------------------------- Java model

def f(v):
    return f"{float(v)}F"


def java():
    ps, cubes, offs = layout()
    lines = [
        "package com.maltaminecraft.mimcontent.client.fish;",
        "",
        "import net.minecraft.client.model.geom.ModelPart;",
        "import net.minecraft.client.model.geom.PartPose;",
        "import net.minecraft.client.model.geom.builders.CubeListBuilder;",
        "import net.minecraft.client.model.geom.builders.LayerDefinition;",
        "import net.minecraft.client.model.geom.builders.MeshDefinition;",
        "import net.minecraft.client.model.geom.builders.PartDefinition;",
        "",
        "/**",
        " * The tonn (Atlantic bluefin tuna): a big torpedo with a pointed snout, a short spiny first dorsal fin and a pointed",
        " * second one, yellow finlets toward the tail, a slim keeled tail stalk and a tall crescent tail. 39 px long.",
        " * Made by art/src/fish_tonn_model.py (do not edit by hand); texture textures/entity/fish/tonn.png. Follows the fish",
        " * model contract (docs/Tools and Process/Art pipeline.md, \"Fish models\"): \"tail\" is the slim back end,",
        " * \"tail_fin\" the crescent inside it.",
        " */",
        "public class TonnModel extends FishModel {",
        "    public TonnModel(ModelPart root) {",
        "        super(root);",
        "    }",
        "",
        "    public static LayerDefinition createBodyLayer() {",
        "        MeshDefinition mesh = new MeshDefinition();",
        "        PartDefinition root = mesh.getRoot();",
    ]
    for pi, p in enumerate(ps):
        cl = []
        for k, (cpi, c) in enumerate(cubes):
            if cpi != pi:
                continue
            u, v = offs[k]
            role, x, y, z, w, h, d = c
            cl.append(f".texOffs({u}, {v}).addBox({f(x)}, {f(y)}, {f(z)}, {f(w)}, {f(h)}, {f(d)}) // {role}")
        px, py, pz = p["pivot"]
        rx, ry, rz = p["rot"]
        pose = (f"PartPose.offsetAndRotation({f(px)}, {f(py)}, {f(pz)}, {f(rx)}, {f(ry)}, {f(rz)})"
                if (rx, ry, rz) != (0, 0, 0) else f"PartPose.offset({f(px)}, {f(py)}, {f(pz)})")
        has_child = any(q["parent"] == p["name"] for q in ps)
        var = f"PartDefinition {p['name']} = " if has_child else ""
        owner = p["parent"] or "root"
        lines.append(f"        {var}{owner}.addOrReplaceChild(\"{p['name']}\", CubeListBuilder.create()")
        for c in cl:
            lines.append("            " + c)
        lines.append(f"            , {pose});")
    lines += [f"        return LayerDefinition.create(mesh, {TEX}, {TEX});", "    }", "}", ""]
    # a trailing comment before the comma would swallow it: put the comma on the pose line (done above)
    return "\n".join(lines)


# ---------------------------------------------------------------- offline views for the compare sheet

def rot_y(p, a):
    x, y, z = p
    c, s = math.cos(a), math.sin(a)
    return (x * c + z * s, y, -x * s + z * c)


def world_points():
    """Every visible texel as (model point, colour, outward normal), the model at rest."""
    ps, cubes, offs = layout()
    img = build_texture()
    out = []
    for k, (pi, cube) in enumerate(cubes):
        role, cx, cy, cz, w, h, d = cube
        p = ps[pi]
        ox, oy, oz = part_origin(ps, p)
        ry = p["rot"][1]
        u, v = offs[k]
        for face, (fu, fv, fw, fh), m in face_texels(u, v, w, h, d):
            if fw == 0 or fh == 0:
                continue
            nrm = {"top": (0, -1, 0), "bottom": (0, 1, 0), "-x": (-1, 0, 0), "+x": (1, 0, 0),
                   "-z": (0, 0, -1), "+z": (0, 0, 1)}[face]
            for j in range(fh):
                for i in range(fw):
                    a = img[fv + j, fu + i]
                    if a[3] == 0:
                        continue
                    lx, ly, lz = m(i, j)
                    q = rot_y((cx + lx, cy + ly, cz + lz), ry)
                    out.append(((ox + q[0], oy + q[1], oz + q[2]), tuple(int(c) for c in a[:3]), rot_y(nrm, ry)))
    return out


def flat_view(view, scale=16):
    """An orthographic picture: 'side' seen from +x (head to the left... flipped so the head is on the left), 'top'."""
    pts = world_points()
    W, H = 44 * scale, 24 * scale
    im = np.full((H, W, 3), 245, dtype=np.uint8)
    depth = np.full((H, W), -1e9)
    shade = {"side": {(1, 0, 0): 1.0, (0, -1, 0): 1.0, (0, 1, 0): 0.6, (0, 0, -1): 0.8, (0, 0, 1): 0.8},
             "top": {(0, -1, 0): 1.0, (1, 0, 0): 0.7, (-1, 0, 0): 0.7, (0, 0, -1): 0.8, (0, 0, 1): 0.8}}[view]
    for (x, y, z), rgb, n in pts:
        nn = tuple(round(c) for c in n)
        if view == "side":
            if n[0] < 0.5:
                continue
            sx, sy, dep = z + 21, y - 6, x
        else:
            if n[1] > -0.5:
                continue
            sx, sy, dep = z + 21, x + 12, -y
        f_ = shade.get(nn, 0.85)
        x0, y0 = int(round((sx - 0.5) * scale)), int(round((sy - 0.5) * scale))
        if x0 < 0 or y0 < 0 or x0 + scale > W or y0 + scale > H:
            continue
        reg = depth[y0:y0 + scale, x0:x0 + scale]
        mask = dep >= reg
        reg[mask] = dep
        col = np.array([min(255, int(c * f_)) for c in rgb], dtype=np.uint8)
        im[y0:y0 + scale, x0:x0 + scale][mask] = col
    return Image.fromarray(im, "RGB")


def sheet(vanilla_dir, shots_dir):
    from PIL import ImageDraw
    sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
    from font import label_font
    font = label_font(16)
    blocks = []

    def title(text, w):
        t = Image.new("RGB", (w, 28), (255, 255, 255))
        ImageDraw.Draw(t).text((6, 4), text, fill=(0, 0, 0), font=font)
        return t

    refdir = os.path.join(ROOT, "art", "references", "fish_tonn_refonly")
    refs = []
    for n in ("tonn_02.jpg", "tonn_06.jpg", "tonn_04.jpg", "tonn_13.jpg"):
        r = Image.open(os.path.join(refdir, n)).convert("RGB")
        r.thumbnail((340, 230))
        refs.append(r)
    blocks.append(("references (reference only): illustration, aquarium, on deck (back), finlets", refs))
    blocks.append(("offline flat views at 16x: side, top", [flat_view("side"), flat_view("top")]))
    tex = Image.open(PNG).convert("RGBA")
    vt = []
    for n in ("cod", "salmon"):
        v = Image.open(os.path.join(vanilla_dir, n + ".png")).convert("RGBA")
        vt.append(v)
    row = []
    for t in [tex] + vt:
        bg = Image.new("RGBA", (t.width * 8, t.height * 8), (200, 200, 200, 255))
        bg.alpha_composite(t.resize((t.width * 8, t.height * 8), Image.NEAREST))
        row.append(bg.convert("RGB"))
    for t in [tex] + vt:
        bg = Image.new("RGBA", (t.width, t.height), (200, 200, 200, 255))
        bg.alpha_composite(t)
        row.append(bg.convert("RGB"))
    blocks.append(("texture at 8x: tonn (64 x 64) | vanilla cod | vanilla salmon (32 x 32); then each at 1x", row))
    crops = []
    if shots_dir and os.path.isdir(shots_dir):
        names = {n.split("_", 1)[-1]: n for n in sorted(os.listdir(shots_dir))}
        # the same camera distance in both tank shots: vanilla cod and salmon (fish-02), the tonn (fish-04), same scale
        band = (0, 170, 854, 270)
        same = [Image.open(os.path.join(shots_dir, names[k])).convert("RGB").crop(band).resize((854 * 2 // 2, 100))
                for k in ("fish-02-tank-cod-salmon-sardina.png", "fish-04-tank-tonn-murina-ziemel.png") if k in names]
        if same:
            blocks.append(("in game, same scale: cod, salmon, sardina (fish-02) | lampuka, tonn, murina, ziemel (fish-04)", same))
        for k in sorted(names):
            if k.startswith("fish-tonn-") or k.startswith("fish-06"):
                s = Image.open(os.path.join(shots_dir, names[k])).convert("RGB")
                s.thumbnail((620, 360))
                crops.append((k, s))
    for i in range(0, len(crops), 3):
        grp = crops[i:i + 3]
        blocks.append(("in game: " + ", ".join(n[:-4] for n, _ in grp), [s for _, s in grp]))
    W = max(sum(im.width + 10 for im in ims) + 10 for _, ims in blocks)
    H = sum(28 + max(im.height for im in ims) + 14 for _, ims in blocks)
    out = Image.new("RGB", (W, H), (255, 255, 255))
    y = 0
    for text, ims in blocks:
        out.paste(title(text, W), (0, y))
        y += 28
        x = 10
        for im in ims:
            out.paste(im, (x, y))
            x += im.width + 10
        y += max(im.height for im in ims) + 14
    path = os.path.join(ROOT, "art", "candidates", "fish_tonn_model.png")
    out.save(path)
    print("wrote", path)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--sheet":
        sheet(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
        return
    Image.fromarray(build_texture(), "RGBA").save(PNG)
    with open(JAVA, "w", encoding="utf-8") as fh:
        fh.write(java())
    print("wrote", os.path.relpath(PNG, ROOT), "and", os.path.relpath(JAVA, ROOT))


if __name__ == "__main__":
    main()
