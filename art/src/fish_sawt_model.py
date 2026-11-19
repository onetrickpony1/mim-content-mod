"""The sawt (lesser weever, Echiichthys vipera) as a swimming mob: its 3D model and its texture.

Night job piece 1 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). Drawn from the
photos in art/references/fish_sawt_refonly/ (list.tsv; fresh fish out of water for colour, the Corsica and Limnos
photos for how it lies buried in sand). What makes it a weever, not a goby and not a little cod:
  - a slim body, deepest at the head, the back sloping down to a thin tail stalk, the belly flat on the sand;
  - a blunt, steep face with an upturned, oblique mouth (a pale lip down the front, no dark gape);
  - eyes high on top of the head, on its upper edge, so they show from above as it lies buried;
  - the short, jet-black, spiny first dorsal fin (the venomous one) standing over the shoulders: its key mark;
  - a long, low, pale second dorsal fin behind it;
  - sandy to golden flanks crossed by thin oblique dark lines that run down and back, a pale silvery belly;
  - a square tail, yellow with a black rear edge (the photos of fresh fish);
  - pale fan pectoral fins spread on the sand.
It lies on the sand nearly all the time, so it is judged mostly from above, on the floor. It sits 1 px into the floor
(the belly row is below y 24), so on the sand it looks half buried, with the eyes and the black spine showing.

Every colour is a step lighter than the photos, because the game greys and darkens everything under water. The eyes
are the only near-black marks on the body (the dorsal fin and the tail's edge are black too, but they are fins), and
nothing dark or bright sits beside them, so no face.

Size: 14 px from the snout to the tail's edge (0.88 blocks), 4 px deep at the head (3 of them above the sand), 3 px
wide at the head: smaller and much lower than vanilla cod (15 px long, 4 deep).

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, root
children "body", "top_fin" (the black first dorsal fin) and "tail_fin" (which sways). Extra parts: "left_fin" and
"right_fin" (the pectorals).

Candidates (the same model, three paint jobs): A golden flanks with oblique dark lines (the fresh fish in the Dutch
photos); B sand-grey camouflage (the Corsica and Limnos photos, buried); C golden like A with dotted lines along the
flank instead of oblique strokes. CHOSEN is installed.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/SawtModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/sawt.png    (32 x 32)
  art/candidates/sawt_model/  (candidate textures and offline previews)
With --sheet SCREENSHOT_DIR also writes the review sheet art/candidates/fish_sawt_model.png.

Run:  art/.venv/bin/python art/src/fish_sawt_model.py [--sheet SCREENSHOT_DIR]
"""
import colorsys
import glob
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import fish_cerna_model as CE  # noqa: E402  (the shared texel layout and the offline renderer)

RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "SawtModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "sawt.png")
CAND = os.path.join(ROOT, "art", "candidates", "sawt_model")
TW, TH = 32, 32
CHOSEN = "A"
SINK = 1.0   # px below the ground: the belly row sits in the sand, so it looks half buried


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# Body ramp 0 (pale belly) .. 5 (darkest back); then the features. Measured from the fresh fish (holland, small,
# gemeen: back #6e5c34-#8a7440, flank gold #c8a040, lower flank cream #e0d0a0, belly #ece8dc, tail #e8c030 with a
# black edge, first dorsal #141414) and lifted a step for the water.
PALETTES = {
    "A": {
        # round 4 (critic): warmer, more saturated sand-gold (it read grey-brown in the water), the back a step darker
        "0": "#eee2bc", "1": "#dcc690", "2": "#cdb06a", "3": "#b08a48", "4": "#9c7a3e", "5": "#866834",
        "L": "#8a6a3a",                 # the dotted oblique lines
        "E": "#141414",                 # the eye's pupil, on top of the head
        "J": "#dcc690", "M": "#7a5e34",  # the lip, the mouth's corner (a mid brown, never black)
        "S": "#141210", "s": "#2a2a30",  # the black first dorsal, its shaded top row
        "T": "#f0c020", "t": "#c89818", "K": "#141414", "k": "#4a3a1a",   # tail: yellow, root, black edge, its fade
        "P": "#a08a5a", "p": "#b09455",  # fins: the pectorals, the low second dorsal
        "R": "#e8ddb0",                 # the pale ring pixel on the eye's outer side
    },
    "B": {
        "0": "#f2f0ea", "1": "#dcd4c0", "2": "#c6b89c", "3": "#ac9c7e", "4": "#928266", "5": "#766a54",
        "L": "#544838",
        "E": "#0c0a08",
        "J": "#e6e0d0", "M": "#7e6a52",
        "S": "#141210", "s": "#3a342c",
        "T": "#dcc078", "t": "#c4a862", "K": "#141210",
        "P": "#c4b494", "p": "#ac9c7e",
        "R": "#e6e0d0",
        "k": "#4a3a1a",
    },
    "C": {
        "0": "#eee2bc", "1": "#dcc690", "2": "#cdb06a", "3": "#b08a48", "4": "#9c7a3e", "5": "#866834",
        "L": "#8a6a3a",                 # the dotted oblique lines
        "E": "#141414",                 # the eye's pupil, on top of the head
        "J": "#dcc690", "M": "#7a5e34",  # the lip, the mouth's corner (a mid brown, never black)
        "S": "#141210", "s": "#2a2a30",  # the black first dorsal, its shaded top row
        "T": "#f0c020", "t": "#c89818", "K": "#141414", "k": "#4a3a1a",   # tail: yellow, root, black edge, its fade
        "P": "#a08a5a", "p": "#b09455",  # fins: the pectorals, the low second dorsal
        "R": "#e8ddb0",                 # the pale ring pixel on the eye's outer side
    },
}
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), (xRot, yRot, zRot)). Cubes: (name, part, (U, V), (x0, y0, z0)
# absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+). Every y is moved down by
# SINK. The UVs are packed by pack() below.
S = SINK
PARTS = {
    "body": (None, (0.0, 22.0 + S, 0.0), (0.0, 0.0, 0.0)),
    "top_fin": (None, (0.0, 21.0 + S, -3.0), (0.0, 0.0, 0.0)),
    # the pectoral fans: hinged on the flank just behind the head, swept back and down against the flank (round 2:
    # spread wide they read as legs)
    "right_fin": (None, (-1.0, 22.0 + S, -3.0), (0.0, -0.6, 0.6)),
    "left_fin": (None, (1.0, 22.0 + S, -3.0), (0.0, 0.6, -0.6)),
    "tail_fin": (None, (0.0, 22.5 + S, 5.0), (0.0, 0.0, 0.0)),
}
SPECS = [
    # the deep, blunt head with the eyes on its top edge and the oblique mouth painted on its steep front
    ("head", "body", (-1.5, 20.0 + S, -6.0), (3, 4, 3)),
    # the body: 2 wide, stepping down behind the head and again behind the first dorsal, to a thin stalk
    ("trunk", "body", (-1.0, 21.0 + S, -3.0), (2, 3, 4)),
    ("rear", "body", (-1.0, 22.0 + S, 1.0), (2, 2, 3)),
    ("stalk", "body", (-0.5, 22.0 + S, 4.0), (1, 1, 1)),
    # the long, low, pale second dorsal fin along the rear
    ("dorsal2", "body", (0.0, 21.0 + S, 1.0), (0, 1, 4)),
    # the black venomous first dorsal over the shoulders
    ("dorsal1", "top_fin", (0.0, 19.0 + S, -3.0), (0, 3, 3)),
    # the pectoral fans
    ("pec_r", "right_fin", (-1.0, 22.0 + S, -3.0), (0, 1, 2)),
    ("pec_l", "left_fin", (1.0, 22.0 + S, -3.0), (0, 1, 2)),
    # the square tail
    ("caudal", "tail_fin", (0.0, 20.5 + S, 5.0), (0, 4, 3)),
]


def footprint(size):
    w, h, d = size
    if w == 0:
        return 2 * d, d + h
    if h == 0:
        return d + 2 * w, d
    return 2 * d + 2 * w, d + h


def used_corner(size, x, y):
    w, h, d = size
    if w == 0:
        return x, y + d
    if h == 0:
        return x + d, y
    return x, y


def pack(specs):
    """Shelf-pack every cube's used texture area into the texture, biggest first."""
    order = sorted(specs, key=lambda s: (-footprint(s[3])[1], -footprint(s[3])[0], s[0]))
    uv, x, y, shelf = {}, 0, 0, 0
    for name, _, _, size in order:
        fw, fh = footprint(size)
        if x + fw > TW:
            x, y, shelf = 0, y + shelf + 1, 0
        uv[name] = used_corner(size, x, y)
        x += fw + 1
        shelf = max(shelf, fh)
    assert y + shelf <= TH
    return [(name, part, uv[name], pos, size) for name, part, pos, size in specs]


CUBES = pack(SPECS)

# --- painting ----------------------------------------------------------------------------------------------------------
# Rows below are model rows before the sink (20 = the head's top row with the eyes, 23 = the belly row in the sand).
ROW_SHADE = {20: 3, 21: 3, 22: 2, 23: 0}
EYE = (20, -5)   # (row, z column): on the head's top edge


def hash01(*vals):
    return CE.hash01(*vals)


def line_at(variant, yi, zi):
    """The flank's marks behind the head: A and B oblique strokes running down and back; C dotted lines along."""
    if zi < -3 or yi >= 23:
        return False
    if variant == "C":
        return yi == 21 and zi % 2 == 0 and zi >= -2
    # round 4: single dots in short diagonal runs (one across, one down toward the tail), 2 px of clear flank between
    # runs, on the upper flank only and nothing within 2 px of the eye
    return (yi, zi) in ((21, -2), (22, -1), (22, 2))


def side_colour(pal, variant, y, z, face):
    yi, zi = int(math.floor(y - SINK)), int(math.floor(z))
    if face in ("west", "east"):
        if (yi, zi) == EYE:
            return pal["R"]            # the pale ring on the eye's outer side (the pupil is on the head's top)
        if (yi, zi) == (22, -6):
            return pal["M"]            # the upturned mouth's corner, low on the steep front
    if line_at(variant, yi, zi):
        return pal["L"]
    shade = ROW_SHADE[yi]
    if zi <= -4 and yi < 23:
        shade = 2                      # the head's side plain gold round the eye (round 4)
    return pal[str(max(0, min(5, shade)))]


def top_colour(pal, variant, x, z):
    """The back seen from above, the view seen most as it lies on the sand: sandy, lit from the top left (its right
    flank a step lighter), with a few faint 1 px flecks; the eyes on the head's outer columns, the crown between
    plain."""
    xi, zi = int(math.floor(x)), int(math.floor(z))
    if abs(x) > 0.75 and zi == EYE[1]:
        return pal["E"]
    shade = 4 + (0 if x < 0 else 1)
    if zi <= -4:
        return pal[str(shade - 1)]     # the head's top in the back's colour, plain round the eyes
    r = hash01(7, xi, zi)
    shade += -1 if r < 0.12 else 0
    return pal[str(max(0, min(5, shade)))]


def body_colour(pal, variant, name, face, x, y, z, x0, y0, z0, w, h, d):
    if face == "top":
        return top_colour(pal, variant, x, z)
    if face == "bottom":
        return pal["0"]
    if face == "north":
        # the face seen head on stays plain body tones (no mouth line, no pale muzzle), so it never reads as a face
        yi = int(math.floor(y - SINK))
        return pal[str(max(0, min(5, ROW_SHADE[yi])))]
    if face == "south":
        return side_colour(pal, variant, y, z0 + d - 1, face)
    return side_colour(pal, variant, y, z, face)


# fin outlines, one character per texel, top row first (the plane's own rows and columns, from its corner)
DORSAL1 = [            # rows y 19..21 (21 inside the back), columns z -3..-1: black, the front spines tallest
    "ss.",
    "SSs",
    "SSS",
]
DORSAL2 = ["pppp"]
PECTORAL = [
    "PP",
]
CAUDAL = [             # rows y 21..23, columns z 5..6: yellow, the black rear edge
    "tTk",
    "tTK",
    "TTK",
    "tTk",
]
FINS = {"dorsal1": DORSAL1, "dorsal2": DORSAL2, "pec_r": PECTORAL, "pec_l": PECTORAL, "caudal": CAUDAL}


def fin_colour(pal, name, cube, y, z):
    _, _, _, (x0, y0, z0), _ = cube
    grid = FINS[name]
    r, c = int(math.floor(y - y0)), int(math.floor(z - z0))
    ch = grid[r][c]
    return CLEAR if ch == "." else pal[ch]


def draw_texture(variant):
    pal = {k: hexc(v) for k, v in PALETTES[variant].items()}
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in CUBES:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in CE.face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if w == 0 or h == 0:
                col = fin_colour(pal, name, cube, y, z)
            else:
                col = body_colour(pal, variant, name, face, x, y, z, x0, y0, z0, w, h, d)
            img.putpixel((u, v), col)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def write_java():
    f = CE.f
    lines = []
    for part in ("body", "top_fin", "right_fin", "left_fin", "tail_fin"):
        parent, (px, py, pz), rot = PARTS[part]
        builder = "CubeListBuilder.create()"
        for cube in [c for c in CUBES if c[1] == part]:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = CE.tex_offset(cube)
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %d.0F, %d.0F, %d.0F)" % (
                name, u, v, f(x0 - px), f(y0 - py), f(z0 - pz), w, h, d)
        if any(rot):
            pose = "PartPose.offsetAndRotation(%s, %s, %s, %s, %s, %s)" % (f(px), f(py), f(pz), f(rot[0]), f(rot[1]),
                                                                           f(rot[2]))
        else:
            pose = "PartPose.offset(%s, %s, %s)" % (f(px), f(py), f(pz))
        lines.append("        root.addOrReplaceChild(\"%s\", %s,\n            %s);" % (part, builder, pose))
    src = """package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The sawt (lesser weever): a slim sandy fish, deepest at the head, with an upturned mouth, eyes on top of the head,
 * the short jet-black venomous first dorsal fin over the shoulders, a long low pale second dorsal, pale fan pectorals
 * spread on the sand and a square yellow tail with a black edge that sways. 14 px long, 4 px deep at the head, 3 wide;
 * it sits 1 px into the floor so on the sand it looks half buried. Head toward -z, the ground at y 24.
 * Texture: textures/entity/fish/sawt.png (32 x 32). Made by art/src/fish_sawt_model.py (don't edit by hand).
 */
public class SawtModel extends FishModel {
    public SawtModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
%s
        return LayerDefinition.create(mesh, %d, %d);
    }
}
""" % ("\n".join(lines), TW, TH)
    with open(JAVA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src)


# --- offline previews and the review sheet ------------------------------------------------------------------------
def previews(textures):
    os.makedirs(CAND, exist_ok=True)
    rows = []
    for variant, tex in textures.items():
        tex.save(os.path.join(CAND, "sawt_%s.png" % variant))
        views = [CE.render(CUBES, PARTS, tex, v, 16) for v in ("side", "three", "top")]
        rows.append(views)
    cod = CE.vanilla_texture("cod")
    scale = [CE.render(CUBES, PARTS, textures[CHOSEN], "side", 8)]
    if cod:
        scale.append(CE.render(CE.vanilla_cubes(CE.COD_CUBES), CE.COD_PARTS, cod, "side", 8))
    W = max(sum(i.width for i in r) + 20 * len(r) + 20 for r in rows + [scale])
    H = sum(max(i.height for i in r) + 20 for r in rows + [scale])
    sheet = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for r in rows + [scale]:
        x, hh = 10, max(i.height for i in r)
        for im in r:
            sheet.paste(im, (x, y + hh - im.height), im)
            x += im.width + 20
        y += hh + 20
    sheet.save(os.path.join(CAND, "sawt_offline.png"))
    return sheet


def review_sheet(shots_dir, offline):
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

    title("Offline model, 16x: candidates A, B, C (rows): side, three-quarter, top; last row the chosen beside vanilla cod")
    row([offline])

    def shot(n):
        found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
        return Image.open(found[-1]).convert("RGBA") if found else None

    names = ["fish-sawt-on-sand-side", "fish-sawt-on-sand", "fish-sawt-on-sand-top", "fish-sawt-side",
             "fish-sawt-three-quarter", "fish-sawt-top", "fish-sawt-beside-cod", "fish-sawt-on-land", "fish-sawt-lineup"]
    imgs = [(n, shot(n)) for n in names]
    imgs = [(n, i) for n, i in imgs if i]
    if imgs:
        title("In the game: " + ", ".join(n for n, _ in imgs))
        for k in range(0, len(imgs), 3):
            row([i for _, i in imgs[k:k + 3]], h=330)
        title("Close-ups (the middle of each shot, 2x): on the sand from the side, three-quarter and above; mid-water side")
        crops = []
        for n, i in imgs:
            if n in ("fish-sawt-on-sand-side", "fish-sawt-on-sand", "fish-sawt-on-sand-top", "fish-sawt-side"):
                w, h = i.size
                crops.append(i.crop((w // 4, h // 4, 3 * w // 4, 3 * h // 4)).resize((w, h), Image.NEAREST))
        row(crops[:2], h=440)
        row(crops[2:], h=440)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_sawt_model.png")
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    textures = {v: draw_texture(v) for v in PALETTES}
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    textures[CHOSEN].save(TEXTURE)
    write_java()
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    offline = previews(textures)
    args = sys.argv[1:]
    if "--sheet" in args:
        review_sheet(args[args.index("--sheet") + 1], offline)


if __name__ == "__main__":
    main()
