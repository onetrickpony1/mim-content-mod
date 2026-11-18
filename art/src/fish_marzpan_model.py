"""The marzpan (Mediterranean parrotfish, Sparisoma cretense, the red female) as a swimming mob: its 3D model and texture.

Drawn from the reference photos in art/references/fish_marzpan_refonly/ (list.tsv; two of them taken off Gozo). What
makes it a marzpan (the female, the colourful one; the male is plain grey):
  - an oblong, deep-bodied wrasse shape, deepest just behind the head, on a thick tail stalk (not the awrata's oval bream
    shape with a narrow stalk, nor the cawl's small fork-tailed disc),
  - a blunt, rounded snout that ends in a short beak (the fused teeth), pale at the tip, the mouth a small dark corner,
  - scarlet red all over, dark red along the back, paling to pink toward the belly (countershaded),
  - a grey-lilac patch over the cheek and gill cover, with the eye at its front edge, and a yellow stripe along its
    lower edge from under the eye back to the gill cover,
  - a yellow saddle on top of the tail stalk, just before the tail,
  - one long low red dorsal fin, a short anal fin, pale pink pectoral fins, and a square-cut (truncate) red tail.
The eye is the only black, set in the grey patch with only grey and red around it, so nothing else reads as an eye.

Size: the body box is 0.5 x 0.4 blocks (8 x 6.4 model pixels). The model is 17 px long (14 of body from the beak tip,
3 of tail), 7 px deep (9 with the dorsal and anal fins, 8 with the tail) and 4 px thick. Body depth to body length is
7 to 14 (0.5 with the beak, 0.39 of the whole fish); a little longer and slimmer than the cawl, much smaller than the
awrata (23 px) and the cerna (29 px), a little longer than vanilla cod (15 px).

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body", "top_fin" (the dorsal) and a "tail_fin" that sways like vanilla cod's; "left_fin" / "right_fin" are the
pectorals. Uses the generic helpers of the accepted cerna script (face layout, preview renderer, vanilla cod's shape).

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/MarzpanModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/marzpan.png    (64 x 64)
With --variant B or C it writes nothing to the mod and only previews that candidate. With --sheet DIR it writes the
review sheet art/candidates/fish_marzpan_model.png with the in-game shots from DIR.

Run:  art/.venv/bin/python art/src/fish_marzpan_model.py [--variant A|B|C] [--preview DIR] [--sheet SCREENSHOT_DIR]
"""
import glob
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fish_cerna_model import (COD_CUBES, COD_PARTS, face_texels, f, hash01, render, tex_offset,  # noqa: E402
                              vanilla_cubes)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "MarzpanModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "marzpan.png")
TW, TH = 64, 64

ARGS = sys.argv[1:]
VARIANT = ARGS[ARGS.index("--variant") + 1] if "--variant" in ARGS else "A"


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


def darker(c, k=0.85):
    return (int(round(c[0] * k)), int(round(c[1] * k)), int(round(c[2] * k)), c[3])


# The model's palette: a step lighter than the photos, because under water the game greys and darkens everything.
# The icon takes these lifted about x1.2 for out of water (art/src/fish_marzpan_icon.py).
PAL = {
    # the red body, palest (belly) to darkest (back): a warm scarlet, so it stays red, not purple, under water
    "0": hexc("#ffa890"), "1": hexc("#ff9470"), "2": hexc("#ff7048"), "3": hexc("#f45a38"), "4": hexc("#dc4630"),
    "5": hexc("#bc3828"),
    # the grey-lilac cheek patch: lit, mid, shaded (its back edge is the gill cover), a little warm so it stays lilac
    "H": hexc("#d8c4d0"), "G": hexc("#bca4b6"), "g": hexc("#9c8498"),
    "k": hexc("#86707e"),   # the darker back border of the patch: the edge of the gill cover
    # yellow: the stripe under the patch and the saddle on the tail stalk; lit and shaded
    "Y": hexc("#fff05a"), "y": hexc("#f2d23c"),
    "b": hexc("#ffd8cc"),   # the small pale beak at the tip (the fused teeth)
    "M": hexc("#b03a2c"),   # the mouth: a mid red line, never near black
    "E": hexc("#0a0a0a"),   # the eye: the only black
    "O": hexc("#ff9a2c"),   # the gold-orange ring above and behind the eye (warmer than the yellow stripe, a gap between)
    # fins: dorsal and anal membrane (light, translucent red) and their thin darker edge; the tail lit, mid, rim
    "D": hexc("#a02c20"),   # the dorsal fin's darker top edge, so it shows above the back under water
    "f": hexc("#ff8c6c"), "F": hexc("#ec6446"), "r": hexc("#cc4a34"),
    "T": hexc("#ff7a56"), "t": hexc("#f0603e"), "u": hexc("#cc4632"),
    # the pectoral fins, a light red with a darker rim
    "P": hexc("#ff7a50"), "p": hexc("#e05a3a"),
    ".": (0, 0, 0, 0),
}
CLEAR = PAL["."]
RAMP = [PAL[k] for k in "012345"]

# --- the model -------------------------------------------------------------------------------------------------------
PARTS = {
    "body": (None, (0.0, 19.0, 0.0), (0.0, 0.0, 0.0)),
    "top_fin": (None, (0.0, 15.0, 0.0), (0.0, 0.0, 0.0)),
    "tail_fin": (None, (0.0, 18.5, 5.0), (0.0, 0.0, 0.0)),
    # the pectoral fins: hinged on the flank behind the gill cover, laid back along the body
    "right_fin": (None, (-2.0, 19.0, -3.0), (0.0, -0.3, 0.0)),
    "left_fin": (None, (2.0, 19.0, -3.0), (0.0, 0.3, 0.0)),
}
# deeper candidate C: the trunk one pixel deeper below
TRUNK_Y0, TRUNK_H = (15.0, 7) if VARIANT != "C" else (15.0, 8)
CUBES = [
    # the blunt head: the forehead stepping down 1 px a column to the beak-like snout, the chin stepping up 1 px a column
    ("snout", "body", (40, 30), (-1.0, 18.0, -7.0), (2, 2, 1)),
    ("head_front", "body", (28, 30), (-1.5, 17.0, -6.0), (3, 3, 1)),
    ("head", "body", (0, 30), (-2.0, 16.0, -5.0), (4, 5, 2)),
    ("trunk", "body", (0, 0), (-2.0, TRUNK_Y0, -3.0), (4, TRUNK_H, 4)),
    ("rear", "body", (20, 0), (-1.5, 16.0, 1.0), (3, 5, 2)),
    ("stalk", "body", (36, 0), (-1.0, 17.0, 3.0), (2, 3, 2)),
    # the anal fin under the rear (no pelvic fin, so the belly is one smooth line)
    ("anal", "body", (52, 4), (0.0, 21.0, 1.0), (0, 2, 3)),
    # the long low dorsal fin, from the nape to just before the yellow saddle
    ("dorsal", "top_fin", (0, 46), (0.0, 14.0, -4.0), (0, 2, 7)),
    # the square-cut tail
    ("caudal", "tail_fin", (20, 46), (0.0, 15.0, 4.0), (0, 8, 4)),
    # the pectoral fins
    ("pec_r", "right_fin", (30, 46), (-2.0, 18.0, -3.0), (0, 3, 3)),
    ("pec_l", "left_fin", (38, 46), (2.0, 18.0, -3.0), (0, 3, 3)),
]

# The side of the fish: each row's red shade (0 palest .. 5 darkest: dark back, pale belly), then the features painted
# over it, one character per pixel: columns z -8..4, rows y 15..21 ('.' = plain mottled red with scale flecks).
SIDE_Z0, SIDE_Y0 = -8, 15
ROW_SHADE = {15: 5, 16: 5, 17: 4, 18: 3, 19: 2, 20: 1, 21: 0}
FEATURES = {
    # A: the eye ringed with pale grey at the front of the grey cheek patch, the yellow stripe under the patch, the
    # yellow saddle on the stalk
    "A": [
        #  z: -8 ... 4
        ".............",   # y 15
        ".............",   # y 16
        "..OGGk.....YY",   # y 17  (only the top row of the stalk's sides is yellow)
        ".4EOGk.......",   # y 18  (the gold ring above, behind and below the eye; deep red in front)
        ".MOGgk.......",   # y 19  (the mouth corner on the snout, a row under the eye)
        "..YYYY.......",   # y 20  (the yellow stripe, 1 px, ending behind the gill cover)
        ".............",   # y 21
    ],
    # B: no yellow stripe under the patch (only the saddle)
    "B": [
        ".............",
        "..........y..",
        "..OGGg.....yy",
        "..EOGg.......",
        ".MGGGg.......",
        "..Gggg.......",
        ".............",
    ],
}
FEATURES["C"] = FEATURES["A"]
GRID = FEATURES[VARIANT]

# Fin outlines (one character per pixel, colours from PAL); every fin has a solid rim.
# the long low dorsal, rows y 14..15, columns z -4..2: a light translucent strip, 1 px above the back, darker at its ends
DORSAL_Z0, DORSAL_Y0 = -4, 14
DORSAL = [
    "DDDDDDD",
    "fffffff",
]
# the square-cut tail, rows y 15..22, columns z 4..7: red like the body, a slightly darker trailing rim, soft corners
CAUDAL_Z0, CAUDAL_Y0 = 4, 15     # the first column overlaps the stalk, so the tail clearly joins it
CAUDAL = [
    "....",
    "..Tu",
    "TTTu",
    "TTTu",
    "TTtu",
    ".ttu",
    "..tu",
    "....",
]
# the anal fin, rows y 21..22, columns z 1..3
ANAL_Z0, ANAL_Y0 = 1, 21
ANAL = [
    "Fff",
    ".fF",
]
# the small pelvic fin under the throat, row y 22, columns z -4..-3
PELVIC_Z0, PELVIC_Y0 = -4, 22
PELVIC = ["fF"]
# the pectoral fin, rows y 18..20, columns z -3..-1 (before it is turned out): a translucent orange-red fan with rays
PEC_Z0, PEC_Y0 = -3, 18
PECTORAL = [
    "PpP",
    "pPp",
    "Pp.",
]


def mottle(shade, *key):
    """Shift a shade one step lighter or darker at random, so no face is a flat fill."""
    r = hash01(*key)
    if r < 0.07:
        shade -= 1
    elif r > 0.93:
        shade += 1
    return RAMP[max(0, min(5, shade))]


FACE_SALT = {"top": 1, "bottom": 2, "north": 3, "south": 4, "west": 5, "east": 6}


def side_colour(y, z, face, x):
    yi, zi = int(math.floor(y)), int(math.floor(z))
    ch = "."
    if 0 <= yi - SIDE_Y0 < len(GRID) and 0 <= zi - SIDE_Z0 < len(GRID[0]):
        ch = GRID[yi - SIDE_Y0][zi - SIDE_Z0]
    if ch == "E" and face in ("north", "south"):
        ch = "H"                        # the eye only on the sides
    if ch != ".":
        return PAL[ch]
    shade = ROW_SHADE[min(21, yi)]
    if zi >= -3 and face in ("west", "east") and (zi + 2 * yi) % 4 == 0:
        shade += 1                      # the scale rows: a loose diagonal lattice of darker flecks on the flank
    return mottle(shade, FACE_SALT[face], int(math.floor(x * 2)), yi, zi)


def body_colour(name, face, x, y, z, x0, y0, z0, w, h, d):
    col = body_texel(name, face, x, y, z, x0, y0, z0, w, h, d)
    if name == "head_front" and face == "north" and (x - x0 < 1 or x0 + w - x < 1) and col != PAL["E"]:
        return darker(col, 0.92)        # the front corners of the head, so it grades round
    return col


def body_texel(name, face, x, y, z, x0, y0, z0, w, h, d):
    zi, xi = int(math.floor(z)), int(math.floor(x * 2))
    if face == "top":
        if name == "stalk":
            return PAL["Y"] if abs(x) < 1.0 else PAL["y"]    # the yellow saddle across the top of the stalk
        return mottle(5 if abs(x) < 1.0 else 4, 1, xi, zi)
    if face == "bottom":
        # the pale belly ends at the throat; the chin and the stalk are a mid red
        shade = {"trunk": 1, "rear": 1, "head": 1}.get(name, 2)
        if abs(x) >= 1.0:
            shade += 1                  # the belly rounds off toward the flanks
        if (zi + xi) % 3 == 0:
            shade += 1                  # scale marks
        return mottle(shade, 2, xi, zi)
    if face == "north":
        if name in ("head_front", "head", "trunk"):
            return mottle(ROW_SHADE[min(21, int(math.floor(y)))], 3, xi, int(math.floor(y)))   # the front faces red
        if name == "snout" and y > 19:
            return PAL["M"]             # the mouth: a mid-red line across the front of the beak-like snout
        return side_colour(y, z0, face, x)
    if face == "south":
        return side_colour(y, z0 + d - 1, face, x)
    return side_colour(y, z, face, x)


def fin_colour(name, x, y, z):
    grids = {"dorsal": (DORSAL, DORSAL_Y0, DORSAL_Z0), "anal": (ANAL, ANAL_Y0, ANAL_Z0),
             "caudal": (CAUDAL, CAUDAL_Y0, CAUDAL_Z0), "pelvic": (PELVIC, PELVIC_Y0, PELVIC_Z0),
             "pec_r": (PECTORAL, PEC_Y0, PEC_Z0), "pec_l": (PECTORAL, PEC_Y0, PEC_Z0)}
    grid, gy, gz = grids[name]
    return PAL[grid[int(math.floor(y)) - gy][int(math.floor(z)) - gz]]


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


def write_java():
    lines = []
    for part in ("body", "top_fin", "tail_fin", "right_fin", "left_fin"):
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
 * The marzpan (Mediterranean parrotfish, the red female): an oblong, deep red body, dark along the back and pink below,
 * a blunt snout with a short pale beak, a grey-lilac cheek patch with the eye at its front and a yellow stripe under it,
 * a yellow saddle on the tail stalk, a long low dorsal fin, pale pectoral fins and a square-cut tail that sways as it
 * swims. 17 px long, 7 px deep, 4 px thick, head toward -z, the ground at y 24.
 * Made by art/src/fish_marzpan_model.py (don't edit by hand). Texture: textures/entity/fish/marzpan.png (64 x 64).
 * Parts: body, top_fin, tail_fin, right_fin, left_fin.
 */
public class MarzpanModel extends FishModel {
    public MarzpanModel(ModelPart root) {
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


def vanilla_cod():
    for p in (os.path.join(ROOT, "art", ".vanilla", "entity", "fish", "cod.png"),):
        if os.path.exists(p):
            return Image.open(p).convert("RGBA")
    return None


def previews(out_dir, texture, tag):
    os.makedirs(out_dir, exist_ok=True)
    out = {}
    for view in ("side", "top", "three"):
        img = render(CUBES, PARTS, texture, view, 16)
        img.save(os.path.join(out_dir, "marzpan_%s_%s16.png" % (tag, view)))
        out[view] = img
    cod = vanilla_cod()
    row = [render(CUBES, PARTS, texture, "side", 8)]
    if cod:
        row.append(render(vanilla_cubes(COD_CUBES), COD_PARTS, cod, "side", 8))
    im = Image.new("RGBA", (sum(i.width for i in row) + 40, max(i.height for i in row)), (72, 72, 72, 255))
    x = 0
    for i in row:
        im.paste(i, (x, im.height - i.height), i)
        x += i.width + 20
    im.save(os.path.join(out_dir, "marzpan_%s_scale8.png" % tag))
    out["scale"] = im
    return out


def sheet(shots_dir, texture):
    from PIL import ImageFont
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

    ref_dir = os.path.join(ROOT, "art", "references", "fish_marzpan_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("side_2.jpg", "big_red.jpg", "market_1.jpg", "red_1.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    if refs:
        title("References (reference only): the red female, in water and at the market")
        row(refs, h=240)
    title("Offline model, 16x: side, three-quarter, top (vanilla face shading only)")
    row([render(CUBES, PARTS, texture, v, 16) for v in ("side", "three")])
    row([render(CUBES, PARTS, texture, "top", 16), texture.resize((TW * 4, TH * 4), Image.NEAREST)])
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        names = ("fish-marzpan-side", "fish-marzpan-three-quarter", "fish-marzpan-top", "fish-marzpan-beside-cod",
                 "fish-marzpan-on-land", "fish-marzpan-lineup")
        imgs = [(n, shot(n)) for n in names]
        imgs = [(n, i) for n, i in imgs if i]
        if imgs:
            title("In the game: side, three-quarter, top, beside cod, on land, lineup (cod, marzpan, cerna, tonn)")
            row([i for _, i in imgs[:3]], h=330)
            row([i for _, i in imgs[3:]], h=330)
            crops = []
            for n, i in imgs:
                fx = (0.2, 0.2, 0.8, 0.7) if "lineup" not in n and "beside" not in n else (0.02, 0.15, 0.98, 0.8)
                box = (int(i.width * fx[0]), int(i.height * fx[1]), int(i.width * fx[2]), int(i.height * fx[3]))
                k = 580.0 / (box[2] - box[0])
                crops.append(i.crop(box).resize((580, int((box[3] - box[1]) * k)), Image.NEAREST))
            title("The same, cropped")
            row(crops[:3])
            row(crops[3:])
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_marzpan_model.png")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    texture = draw_texture()
    prev = ARGS[ARGS.index("--preview") + 1] if "--preview" in ARGS else None
    if VARIANT == "A":
        os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
        texture.save(TEXTURE)
        write_java()
        print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    if "--sheet" in ARGS:
        sheet(ARGS[ARGS.index("--sheet") + 1], texture)
    if prev:
        previews(prev, texture, VARIANT)
        print("previews in", prev)


if __name__ == "__main__":
    main()
