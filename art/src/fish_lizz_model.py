"""The lizz (European barracuda, Sphyraena sphyraena) as a swimming mob: its 3D model and its texture.

Drawn from the reference photos in art/references/fish_lizz_refonly/ (list.tsv): fresh fish out of water on a plate and
a board, the d'Orbigny plate, and divers' photos of schools for the shape. What makes it a lizz:
  - a long, slim torpedo, about eight times as long as it is deep, and narrow (2 px wide);
  - a long pointed head with a jutting lower jaw: the lower jaw reaches one pixel past the upper snout;
  - two small dorsal fins set far apart: a short spiny one mid-back, a small soft one far back over the anal fin;
  - a dark slate back, silver sides and a white belly (countershaded), with faint darker bars on the upper flank;
  - small pale fins below (pectoral, pelvic, anal) and a dark, deeply forked tail.
No teeth and no face marks: one black eye on the head with no spot, bar or bright speck in its row near it.

Tonight the model comes first (night job, 2026-11-18), so its palette is set here, from the fresh-fish photos, lifted one
step for the water (the game greys and darkens everything under water); the item icon then lifts it again.

Size: the hitbox is 0.7 x 0.3 blocks. The lizz is 24 px long (1.5 blocks: 19 px of body from the jaw tip, 5 of tail),
3 px deep (5 with the fins) and 2 px wide, against the cerna's 29 px and 10 deep and vanilla cod's 15 and 4.
One texture pixel per model pixel, like vanilla's fish.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body", the dorsal fins in "top_fin" and the forked tail in "tail_fin", which sways like vanilla cod's.

Candidates (--cand): A slim (3 px trunk, short tapering rear), B deeper (4 px trunk), C slim with a longer head and
more visible bars. The installed one is CHOSEN.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/LizzModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/lizz.png    (64 x 32)
With --sheet [SCREENSHOT_DIR] also writes the review sheet art/candidates/fish_lizz_model.png.

Run:  art/.venv/bin/python art/src/fish_lizz_model.py [--cand A|B|C] [--sheet [SCREENSHOT_DIR]]
"""
import colorsys
import glob
import math
import os
import sys
import zlib

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fish_sardina_model as sard  # noqa: E402  (the shared box-UV layout, previews and vanilla cod geometry)

ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish",
                    "LizzModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "lizz.png")
TW, TH = 64, 32
CHOSEN = "C"


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))


def lift(c, k=1.15, add=0.04):
    """One step lighter for the water: brightness scaled up a little, hue and saturation kept."""
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, v * k + add))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


# The photo palette (fresh fish out of water: side.jpg, barracuda.jpg), before the water lift.
PHOTO = {
    "K": "#2f434c",   # the darkest back, along the spine
    "B": "#475e68",   # the slate back
    "b": "#3b4f58",   # a faint bar on the back
    "G": "#7f9198",   # the grey upper flank, where the back meets the silver
    "g": "#68797f",   # a faint bar on the upper flank
    "S": "#b9c3c6",   # the silver flank
    "W": "#dfe4e4",   # the bright lower flank
    "P": "#eeefea",   # the white belly
    "M": "#5d686c",   # the mouth line between snout and lower jaw
    "J": "#9aa4a8",   # the lower jaw, silver-grey
    "D": "#56656b",   # the dorsal fins, grey
    "d": "#3e4b51",   # their leading edge
    "F": "#a9aca0",   # the small pale fins below (a faintly warm grey in the photos)
    "f": "#8c9088",   # their shaded back edge
    "T": "#4e5a58",   # the forked tail
    "t": "#363f40",   # its darker lobe tips
}
PAL = {k: lift(hexc(v)) for k, v in PHOTO.items()}
PAL["E"] = (12, 14, 16, 255)    # the eye, black, not lifted
PAL["."] = (0, 0, 0, 0)
CLEAR = PAL["."]


def noise(*key):
    """A fixed pseudo-random number in [0, 1) for a texel, so every run draws the same texture."""
    return (zlib.crc32(repr(key).encode()) & 0xFFFFFF) / float(0x1000000)


# --- the candidates --------------------------------------------------------------------------------------------------
# Cubes: (name, part, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail
# (+). Texture places are packed automatically.
def geometry(cand):
    deep = cand == "B"
    long_head = cand == "C"
    top = 18.0 if deep else 19.0           # the trunk's back
    hz = -8.0 if long_head else -7.0       # where the head meets the snout
    cubes = [
        # the long pointed head: the lower jaw juts one pixel past the upper snout
        ("jaw", "body", (-0.5, 21.0, hz - 4.0), (1, 1, 4)),
        ("snout", "body", (-0.5, 20.0, hz - 3.0), (1, 1, 3)),
        ("head", "body", (-1.0, 20.0, hz), (2, 2, -5.0 - hz)),
        # the trunk, the narrowing rear and the slim tail stalk
        ("trunk", "body", (-1.0, top, -5.0), (2, 22 - int(top), 8)),
        ("rear", "body", (-1.0, 19.0, 3.0), (2, 2 if not deep else 3, 3)),
        ("stalk", "body", (-0.5, 19.5, 6.0), (1, 2, 1)),
        # the small pale fins below: pelvic under the trunk, anal under the rear (both touch the body)
        ("pelvic", "body", (0.0, 22.0, -1.0), (0, 1, 2)),
        ("anal", "body", (0.0, 21.0 if not deep else 22.0, 3.0), (0, 1, 3)),
        # the two dorsal fins, far apart: spiny one mid-back, small soft one far back
        ("dorsal1", "top_fin", (0.0, top - 2.0, -2.0), (0, 2, 3)),
        ("dorsal2", "top_fin", (0.0, 18.0, 3.0), (0, 1, 2)),
        # the forked tail
        ("caudal", "tail_fin", (0.0, 18.0, 7.0), (0, 5, 5)),
        # the small pectoral fins, low behind the gill cover, hanging down and out
        ("pec_r", "right_fin", (-2.0, 22.0, -5.0), (1, 0, 2)),
        ("pec_l", "left_fin", (1.0, 22.0, -5.0), (1, 0, 2)),
    ]
    parts = {
        "body": (None, (0.0, 21.0, 0.0), 0.0),
        "top_fin": (None, (0.0, top, -2.0), 0.0),
        "tail_fin": (None, (0.0, 20.5, 7.0), 0.0),
        "right_fin": (None, (-1.0, 22.0, -5.0), -0.9),
        "left_fin": (None, (1.0, 22.0, -5.0), 0.9),
    }
    return pack(cubes), parts


def footprint(w, h, d):
    if w == 0:
        return 2 * d, h
    if h == 0:
        return 2 * w, d
    return 2 * d + 2 * w, d + h


def pack(cubes):
    """Shelf-pack every cube's texture area into the 64 x 32 sheet: (name, part, (U, V), pos, size)."""
    out, x, y, shelf = [], 0, 0, 0
    for name, part, pos, (w, h, d) in cubes:
        d = int(d)
        fw, fh = footprint(w, h, d)
        if x + fw > TW:
            x, y, shelf = 0, y + shelf + 1, 0
        out.append((name, part, (x, y), pos, (w, h, d)))
        x += fw + 1
        shelf = max(shelf, fh)
    assert y + shelf <= TH, "texture too small"
    return out


# --- the colours -----------------------------------------------------------------------------------------------------
def side_key(cand, name, y, z, top, bottom):
    """The side colour (a PAL key) of a body texel at row y, column z, on a section spanning rows top..bottom."""
    yi, zi = int(math.floor(y)), int(math.floor(z))
    r = int(math.floor(y - top))
    n = int(round(bottom - top))   # rows in this section
    hz = -8 if cand == "C" else -7
    if name == "jaw":
        return "J"
    if name == "snout":
        return "B"
    if name == "head":
        # top row: the slate back and the eye; bottom row: the mouth line under the front, silver behind
        if r == 0:
            if zi == hz + 1:
                return "E"
            return "G"                      # round 2: pale grey round the eye, so it never merges into the back
        return "M" if zi < hz + 1 else "S"
    if name == "stalk":
        return "G"
    # trunk and rear: back, upper flank, silver, bright lower flank
    rows = {2: ["B", "W"], 3: ["B", "S", "W"], 4: ["K", "B", "S", "W"]}[n]
    key = rows[r]
    # faint dark bars on the back and upper flank, every third column, from behind the pectoral fin
    bars = cand == "C"
    if zi >= -3 and zi % 3 == 0:          # round 2: straight vertical bars, one column wide
        if key == "B":
            return "b"
        if key == "K":
            return "B"
        if key == "S" and bars:
            return "g"
    # a soft mix where the back meets the silver
    if key == "S" and noise(name, y, z) < 0.08:
        return "G"
    if key == "W" and noise(name, "w", y, z) < 0.2:
        return "S"
    return key


def body_colour(cand, name, face, x, y, z, x0, y0, z0, w, h, d):
    zi = int(math.floor(z))
    if face == "top":
        if name in ("jaw",):
            return PAL["J"]
        n = noise(name, "top", x, z)
        return PAL["K"] if n < 0.7 else PAL["B"]
    if face == "bottom":
        if name == "snout":
            return PAL["M"]                     # the gape, under the upper snout
        if name == "jaw":
            return PAL["J"]
        return PAL["P"] if noise(name, "bot", x, z) < 0.85 else PAL["W"]
    if face in ("west", "east"):
        return PAL[side_key(cand, name, y, z, y0, y0 + h)]
    # the ends of each section: the colour of the side beside them, never the eye's
    zz = z0 + 0.5 if face == "north" else z0 + d - 0.5
    k = side_key(cand, name, y, zz, y0, y0 + h)
    if k == "E":
        k = "B"
    return PAL[k]


DORSAL1 = [".d.", "dDD"]          # rows y top-2..top-1, z -2..0: a small low triangle (round 2: no tall spike)
DORSAL2 = ["dD"]                  # one row: the smaller soft fin far back
CAUDAL = [                         # rows y 18..22, z 7..11: a deep fork with thick lobes, dark tips
    "...Tt",
    "..TT.",
    "TTT..",
    "..TT.",
    "...Tt",
]


def fin_colour(name, x, y, z, y0, z0):
    zi, yi = int(math.floor(z - z0)), int(math.floor(y - y0))
    if name == "dorsal1":
        return PAL[DORSAL1[yi][zi]]
    if name == "dorsal2":
        return PAL[DORSAL2[yi][zi]]
    if name == "caudal":
        return PAL[CAUDAL[yi][zi]]
    if name == "pelvic":
        return PAL["S"] if zi == 0 else PAL["G"]      # round 2: belly silver, so it no longer reads as a peg
    if name == "anal":
        return PAL["F"] if zi == 0 else PAL["f"]
    return PAL["F"] if zi == 0 else PAL["f"]       # the pectorals


def draw_texture(cand, cubes):
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in cubes:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in sard.face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if w == 0 or h == 0:
                c = fin_colour(name, x, y, z, y0, z0)
            else:
                c = body_colour(cand, name, face, x, y, z, x0, y0, z0, w, h, d)
            img.putpixel((u, v), c)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def write_java(cubes, parts):
    f = sard.f
    lines = []
    for part in ("body", "top_fin", "tail_fin", "right_fin", "left_fin"):
        parent, (px, py, pz), zrot = parts[part]
        builder = "CubeListBuilder.create()"
        for cube in [c for c in cubes if c[1] == part]:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = sard.tex_offset(cube)
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
 * The lizz (European barracuda): a long slim torpedo with a long pointed head and a jutting lower jaw, two small dorsal
 * fins set far apart, a dark slate back over silver sides with faint bars, a white belly and a dark forked tail that
 * sways as it swims. 24 px long, 3 px deep, 2 px wide, head toward -z, the ground at y 24.
 * Made by art/src/fish_lizz_model.py (don't edit by hand). Texture: textures/entity/fish/lizz.png (64 x 32).
 */
public class LizzModel extends FishModel {
    public LizzModel(ModelPart root) {
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


# --- the review sheet -------------------------------------------------------------------------------------------------
def on_bg(img, bg=(72, 72, 72, 255), pad=4):
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), bg)
    out.alpha_composite(img, (pad, pad))
    return out


def sheet(shots_dir):
    from PIL import ImageFont
    try:
        sys.path.insert(0, os.path.join(ROOT, "art", "tools"))
        from font import label_font
        font = label_font(15)
    except Exception:  # noqa: BLE001
        font = ImageFont.load_default()
    import fish_cerna_model as cerna
    W = 1800
    blocks = []

    def title(t):
        im = Image.new("RGBA", (W, 28), (40, 40, 40, 255))
        ImageDraw.Draw(im).text((8, 5), t, fill=(240, 240, 240, 255), font=font)
        blocks.append(im)

    def row(images, h=None, gap=14, align_bottom=False):
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images)
        im = Image.new("RGBA", (W, hh + 8), (72, 72, 72, 255))
        x = 8
        for i in images:
            if x + i.width > W:
                break
            im.alpha_composite(i, (x, 4 + (hh - i.height if align_bottom else (hh - i.height) // 2)))
            x += i.width + gap
        blocks.append(im)

    ref_dir = os.path.join(ROOT, "art", "references", "fish_lizz_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA") for n in ("side.jpg", "barracuda.jpg", "fmib.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    if refs:
        title("References (reference only): fresh European barracuda on a plate and on a board, the d'Orbigny plate")
        row(refs, h=200)
    cod = sard.vanilla_texture("cod")
    cc = sard.vanilla_cubes(sard.COD_CUBES)
    ctex = Image.open(cerna.TEXTURE).convert("RGBA")
    for cand in ("A", "B", "C"):
        cubes, parts = geometry(cand)
        tex = draw_texture(cand, cubes)
        title("Candidate %s%s: side, three-quarter, top at 12x; texture at 4x" % (cand, " (installed)" if cand == CHOSEN else ""))
        row([on_bg(sard.render(cubes, parts, tex, v, 12)) for v in ("side", "three", "top")]
            + [on_bg(tex.resize((TW * 4, TH * 4), Image.NEAREST), (139, 139, 139, 255))])
    cubes, parts = geometry(CHOSEN)
    tex = draw_texture(CHOSEN, cubes)
    title("Same scale, 8x: lizz %s (1.5 blocks), the accepted cerna (1.81), vanilla cod" % CHOSEN)
    imgs = [sard.render(cubes, parts, tex, "side", 8), cerna.render(cerna.CUBES, cerna.PARTS, ctex, "side", 8)]
    if cod:
        imgs.append(sard.render(cc, sard.COD_PARTS, cod, "side", 8))
    row([on_bg(i) for i in imgs], align_bottom=True, gap=40)

    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None

        names = ("fish-lizz-side", "fish-lizz-three-quarter", "fish-lizz-top", "fish-lizz-beside-cod",
                 "fish-lizz-on-land", "fish-lizz-beside-cerna-tonn")
        present = [(n, shot(n)) for n in names]
        present = [(n, i) for n, i in present if i]
        if present:
            title("In the game: side, three-quarter, top, beside cod, on land, beside the cerna and a small tonn")
            row([i for _, i in present[:3]], h=330)
            row([i for _, i in present[3:]], h=330)
            title("The same, cropped to the fish")
            boxes = {"fish-lizz-beside-cod": (0.06, 0.25, 0.94, 0.6), "fish-lizz-on-land": (0.3, 0.35, 0.7, 0.65),
                     "fish-lizz-beside-cerna-tonn": (0.0, 0.2, 1.0, 0.7)}
            crops = []
            for n, i in present:
                fx = boxes.get(n, (0.2, 0.25, 0.8, 0.6))
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
    dest = os.path.join(ROOT, "art", "candidates", "fish_lizz_model.png")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    args = sys.argv[1:]
    cand = args[args.index("--cand") + 1] if "--cand" in args else CHOSEN
    cubes, parts = geometry(cand)
    texture = draw_texture(cand, cubes)
    os.makedirs(os.path.dirname(TEXTURE), exist_ok=True)
    texture.save(TEXTURE)
    write_java(cubes, parts)
    print("wrote", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT), "(candidate %s)" % cand)
    if "--sheet" in args:
        i = args.index("--sheet")
        sheet(args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith("--") else None)


if __name__ == "__main__":
    main()
