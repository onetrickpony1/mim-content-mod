"""The trilja (striped red mullet, Mullus surmuletus) as a swimming mob: its 3D model and its texture.

Night job piece 1 of 3 (docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md). Drawn from the
photos in art/references/fish_trilja_refonly/ (list.tsv; fresh Mediterranean catches out of water for colour). The
striped red mullet (Trilja tal-qawwi) lives on sand and rock in the shallows round Malta; the plain red mullet
(M. barbatus) lives deeper on mud. What makes it a trilja:
  - a steep, blunt head: the profile drops in steps from the back to a low, rounded snout, with the eye high on it;
  - two pale chin barbels, one at each cheek, hanging from under the chin;
  - a pinkish-red body: a deeper red back, a yellow line along the middle of the flank from behind the head to the
    tail, a pale pink-white lower flank and belly (countershaded);
  - two separate dorsal fins: the first tall and striped with dark red-brown, the second low, well behind it;
  - a forked, rosy tail.
Every colour is a step lighter than the photos, because the game greys and darkens everything under water.

Size: 15 px long (12 of body from the snout tip, 3 of tail), 4 px deep, 2 px wide: 0.94 blocks, as long as vanilla
cod (15 px) but slimmer at the rear, much smaller than the cerna. One texture pixel per model pixel.

Review: 8 critic rounds, all FAIL ("close"); the night job's rule is to leave the round 8 version installed and move on
(gave up). The barbels were the sticking point: see docs/Creatures and Plants/Night log/trilja.md.

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): head toward -z, y 24 at the ground, a root
child "body", "top_fin" (the first dorsal fin) and a "tail_fin" that sways like vanilla cod's.

Candidates (the same model, three paint jobs): A rosy pink-red with a white belly (pinker than the scarlet marzpan);
B orange-red (the first try); C a softer coral-pink fish with a paler line. CHOSEN is installed.

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/TriljaModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/trilja.png    (32 x 32)
  art/candidates/trilja_model/  (candidate textures and offline previews)
With --sheet SCREENSHOT_DIR also writes the review sheet art/candidates/fish_trilja_model.png.

Run:  art/.venv/bin/python art/src/fish_trilja_model.py [--sheet SCREENSHOT_DIR]
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
                    "TriljaModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "trilja.png")
CAND = os.path.join(ROOT, "art", "candidates", "trilja_model")
TW, TH = 32, 32
CHOSEN = "A"
VANILLA_JAR = "/home/cultar/Apps/Minecraft World/tools/gradle-home/caches/fabric-loom/26.3/minecraft-merged.jar"


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


# Palettes. Keys:
#   H head top (red), c cheek and snout (coral), E eye, j mouth corner, B barbel (cream)
#   m back (red), M spine seen from above (deeper red), o upper flank (orange-red), y the yellow line, Y its soft end
#   p pink lower flank, w belly (pale pink-white)
#   F first dorsal pale rays, K its dark stripe, f second dorsal and small fins, a anal fin, P pectoral
#   T tail lit, u tail base, t tail shade
PALETTES = {
    # A: rosy pink-red, not scarlet (the marzpan, the red parrotfish, is the scarlet one): a pink-red back, a rose
    # upper flank, the yellow line, a white belly
    "A": {
        "H": "#d8605e", "c": "#eca096", "E": "#110c0c", "j": "#e0908a", "B": "#f6ead2",
        "m": "#c44e54", "M": "#a8424a", "o": "#ec8c86", "y": "#f0c040", "Y": "#f0b47e",
        "p": "#fce0da", "w": "#fff6f2", "q": "#ffeae2",
        "F": "#f8e6b0", "K": "#c05660", "f": "#f4c0b8", "a": "#eeb6ae", "P": "#fbe2dc",
        "T": "#f6aca2", "u": "#f09e94", "t": "#e88e86",
    },
    # B: the first try, an orange-red fish (it read near the marzpan's scarlet)
    "B": {
        "H": "#d8644a", "c": "#ee9a80", "E": "#110c0c", "j": "#c8705e", "B": "#f6efd6",
        "m": "#c8513f", "M": "#b04536", "o": "#e47a5c", "y": "#f2cc5e", "Y": "#eeb46c",
        "p": "#f4bfb2", "w": "#fcf0ea", "q": "#f8e4dc",
        "F": "#f4dccc", "K": "#9e4a3c", "f": "#eda88c", "a": "#f6d6c6", "P": "#f0b8a2",
        "T": "#f09272", "u": "#e48068", "t": "#d8705c",
    },
    "C": {
        "H": "#e27a62", "c": "#f2ac94", "E": "#110c0c", "j": "#cc806e", "B": "#f6efd6",
        "m": "#d66650", "M": "#c05844", "o": "#eb917a", "y": "#f0d084", "Y": "#eebe8a",
        "p": "#f6cbc0", "w": "#fdf4ef", "q": "#fbeae4",
        "F": "#f6e0d2", "K": "#a8584a", "f": "#f0b49c", "a": "#f6dcce", "P": "#f2c0ac",
        "T": "#f2a088", "u": "#e88e78", "t": "#dc806c",
    },
}
CLEAR = (0, 0, 0, 0)

# --- the model -------------------------------------------------------------------------------------------------------
# Parts: name -> (parent, pivot (absolute model pixels), zRot). Cubes: (name, part, (U, V) top-left of the used texture
# area, (x0, y0, z0) absolute, (w, h, d)). Absolute: x across, y down (24 = ground), z head (-) to tail (+).
PARTS = {
    "body": (None, (0.0, 21.0, 0.0), 0.0),
    "top_fin": (None, (0.0, 19.0, -5.0), 0.0),
    "tail_fin": (None, (0.0, 21.0, 4.0), 0.0),
    # the chin barbels, each its own part hinged flush under the chin 1 px behind the snout tip, one at each cheek
    # with body colour between, hanging down and 15 degrees back (XROT, Java only: the offline preview draws them
    # straight down)
    "barbel_r": (None, (-0.9, 23.0, -7.0), 0.0),
    "barbel_l": (None, (0.9, 23.0, -7.0), 0.0),
    # no pectoral fins (round 3: lying on land, the pectoral's shaded face showed as a grey bar just behind the eye)
}
XROT = {"barbel_r": 0.26, "barbel_l": 0.26}
CUBES = [
    # round 2 (critic: the snout read as a duck bill): the mouth only 2 px ahead of the eye; round 4 (critic: a ledge
    # over the eye, then a box): the forehead steps down 1 px a column, back, head, snout, a steep staircase; the eye
    # in the trunk's first column under a rose row. 2 px wide like vanilla cod, so the yellow line stays on one row
    # seen from any side. The rear keeps the straight back and lifts the belly, then the thin stalk.
    ("head", "body", (18, 0), (-1.0, 20.0, -8.0), (2, 3, 2)),
    ("trunk", "body", (0, 0), (-1.0, 19.0, -6.0), (2, 4, 5)),
    ("rear", "body", (0, 10), (-1.0, 19.0, -1.0), (2, 3, 3)),
    ("stalk", "body", (10, 10), (-0.5, 20.0, 2.0), (1, 2, 2)),
    # the two chin barbels, one each side with a 1 px gap: thin cream strands rooted at the lower lip, lying back
    # along the throat 1 px below it (round 2: hanging 2 px down they read as a beard; round 3: one row under the
    # head read as a chin pad; round 4: hanging straight down, one post; round 5: two thin 2 px strands near each
    # cheek, tilted forward and down: tusks or legs; round 6: 2 px back and down, a plank hanging apart from the chin;
    # round 7: lying back, one pale slab apart from the jaw; round 8: two strands 2 px long hanging from the chin,
    # one at each cheek, 15 degrees back, cream)
    ("barbel_r", "barbel_r", (22, 14), (-0.9, 23.0, -7.0), (0, 2, 1)),
    ("barbel_l", "barbel_l", (26, 14), (0.9, 23.0, -7.0), (0, 2, 1)),
    # the first dorsal fin (tall, in horizontal stripes), its own part as the contract names it; the low second
    # dorsal set well behind it; the anal fin under the rear, flush to the body
    ("dorsal1", "top_fin", (16, 10), (0.0, 17.0, -5.0), (0, 2, 3)),
    ("dorsal2", "body", (22, 10), (0.0, 18.0, 0.0), (0, 1, 2)),
    ("anal", "body", (26, 10), (0.0, 22.0, 0.0), (0, 1, 2)),
    # the forked tail
    ("caudal", "tail_fin", (16, 14), (0.0, 18.0, 4.0), (0, 6, 3)),
]

# The side of the fish, rows y 19..22, columns z -8..3. '.' where no section reaches.
# Row 19: the back, from the forehead to the end of the rear: a rose row over the eye.
# Row 20: the head's top (H), the eye in the trunk's first column, then the rose upper flank and the stalk's back.
# Row 21: the coral cheek, then the yellow line, 1 px tall, from two pixels behind the eye, fading out 2 px before the
#         tail (never beside the eye: yellow by the eye reads as a beak).
# Row 22: the mouth's corner, the pale chin and the pink-white lower flank (countershading: red, rose, yellow, pale).
SIDE_Z0 = -8
SIDES = {
    "A": {
        19: "..mmmmmmmm..",
        20: "HHEooooooo" + "HH",
        21: "cccoyyyyyyoo",
        22: "jcpppppp....",
    },
}
SIDES["B"] = SIDES["A"]
SIDES["C"] = SIDES["A"]
# The back seen from above: three rows across the trunk (head, rear and stalk take the outer rows), columns z -8..3:
# the red head, the red back with a deeper red spine line down the middle.
TOPS = {v: ["HHmmmmmmmmmm", "HHMMMMMMMMmm", "HHmmmmmmmmmm"] for v in PALETTES}
# The belly seen from below (round 2, critic: it read as a grey slab, as the game darkens downward faces): the palest
# pink-white in the middle, a rosier rim at the edges.
# Round 8 (critic: a grey sled under the head too): the pale belly from 1 px behind the eye; pink under the head.
BOTTOM_MID = "ccqqqqqqqqqq"
BOTTOM_RIM = "ccpppppppppp"

# Fin outlines: one character per pixel, rows by absolute y, columns by absolute z.
# Round 2 (critic: a checkerboard): whole rows, pale, dark rose, pale, the base row full width on the back.
# Round 3 (critic: a 3-tier stack with a grey tip; its dark row lay beside the eye on land): two tiers, a rose top
# and a pale base row, so it shows stripes without any dark mark.
# Round 5 (critic: solid under water): three rows, a rose tip, a dark red band, a pale base, the base full width.
# Round 6 (critic: a chimney) and 7 (a dark spire on top): two rows raked back, a pale top row of 2 and a dark
# rose base band of 3 on the back.
DORSAL1_Z0, DORSAL1_Y0 = -5, 17
DORSAL1 = [
    ".FF",
    "KKK",
]
CAUDAL_Z0, CAUDAL_Y0 = 4, 18
CAUDAL = [
    ".TT",
    "uT.",
    "uu.",
    "uu.",
    "ut.",
    ".tt",
]
# the barbels: from under the chin down and back, each pixel sharing an edge with the next
BARBEL_Z0, BARBEL_Y0 = -7, 23
BARBEL = [
    "B",
    "B",
]
DORSAL2 = ["ff"]   # row y 18 over z 0, 1
ANAL = "aa"


def pal(variant):
    return {k: hexc(v) for k, v in PALETTES[variant].items()}


def body_colour(variant, P, name, face, x, y, z, x0, y0, z0, w, h, d):
    """The colour of one texel of a body section, from where it sits on the fish. Faces hidden inside the fish get
    the body colour around them, so no stray colour hides anywhere in the texture."""
    side = SIDES[variant]
    zi, yi = int(math.floor(z)), int(math.floor(y))
    col = zi - SIDE_Z0
    if face == "top":
        rows = TOPS[variant]
        xi = int(math.floor(x + 1.5))           # 0..2 across the trunk
        if w < 3:
            xi = 0 if x < 0 else 2
        if w == 1:
            xi = 1
        return P[rows[min(2, max(0, xi))][col]]
    if face == "bottom":
        rim = w >= 2 and (x < x0 + 1 or x > x0 + w - 1)
        return P[(BOTTOM_RIM if rim else BOTTOM_MID)[col]]
    if face in ("west", "east"):
        ch = side[yi][col]
        return P["c" if ch == "." else ch]
    if face == "north":
        if name in ("head", "snout"):
            return P[{20: "H", 21: "c"}.get(yi, "j")]
        # the step of each section in front of the one behind: the side colour of its first column, never the eye's
        ch = side[yi][int(math.floor(z0)) - SIDE_Z0]
        return P[{"E": "H", ".": "H"}.get(ch, ch)]
    # south: the back end of a section, the colour of its last side column
    ch = side[yi][int(math.floor(z0 + d - 1)) - SIDE_Z0]
    return P[{"E": "c", ".": "m"}.get(ch, ch)]


def fin_colour(P, name, x, y, z):
    zi, yi = int(math.floor(z)), int(math.floor(y))
    if name == "dorsal1":
        ch = DORSAL1[yi - DORSAL1_Y0][zi - DORSAL1_Z0]
    elif name == "caudal":
        ch = CAUDAL[yi - CAUDAL_Y0][zi - CAUDAL_Z0]
    elif name == "dorsal2":
        ch = DORSAL2[yi - 18][zi]
    elif name == "anal":
        ch = ANAL[zi]
    elif name.startswith("barbel"):
        ch = BARBEL[yi - BARBEL_Y0][zi - BARBEL_Z0]
    else:
        ch = "P"                               # the pectorals: a pale pink, never a bright or dark spot
    return CLEAR if ch == "." else P[ch]


def draw_texture(variant):
    P = pal(variant)
    img = Image.new("RGBA", (TW, TH), CLEAR)
    owner = {}
    for cube in CUBES:
        name, _, _, (x0, y0, z0), (w, h, d) = cube
        for face, u, v, x, y, z in sard.face_texels(cube):
            assert 0 <= u < TW and 0 <= v < TH, (name, face, u, v)
            assert owner.setdefault((u, v), name) == name, ("texture overlap", name, owner[(u, v)], u, v)
            if w == 0 or h == 0:
                c = fin_colour(P, name, x, y, z)
            else:
                c = body_colour(variant, P, name, face, x, y, z, x0, y0, z0, w, h, d)
            img.putpixel((u, v), c)
    return img


# --- the Java model ---------------------------------------------------------------------------------------------------
def write_java():
    f = sard.f
    lines = []
    for part in ("body", "top_fin", "tail_fin", "barbel_r", "barbel_l"):
        parent, (px, py, pz), zrot = PARTS[part]
        builder = "CubeListBuilder.create()"
        for cube in [c for c in CUBES if c[1] == part]:
            name, _, _, (x0, y0, z0), (w, h, d) = cube
            u, v = sard.tex_offset(cube)
            builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %d.0F, %d.0F, %d.0F)" % (
                name, u, v, f(x0 - px), f(y0 - py), f(z0 - pz), w, h, d)
        if part in XROT:
            pose = "PartPose.offsetAndRotation(%s, %s, %s, %s, 0.0F, 0.0F)" % (f(px), f(py), f(pz), f(XROT[part]))
        elif zrot:
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
 * The trilja (striped red mullet): a steep, blunt head with the eye high on it and two pale chin barbels hanging
 * from under the chin, a red back, a yellow line along the flank, a pale pink belly, a striped first dorsal fin and a
 * low second one set apart, and a forked rosy tail that sways as it swims. 15 px long, 4 px deep, 2 px wide, head
 * toward -z, the ground at y 24.
 * Made by art/src/fish_trilja_model.py (don't edit by hand). Texture: textures/entity/fish/trilja.png (32 x 32).
 */
public class TriljaModel extends FishModel {
    public TriljaModel(ModelPart root) {
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
        views = [on_bg(sard.render(CUBES, PARTS, tex, view, 16)) for view in ("side", "three", "top")]
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

    title("Candidates A, B, C (offline, 16x: side, three-quarter, top); chosen: " + CHOSEN)
    for v in PALETTES:
        row([Image.open(os.path.join(CAND, "preview_%s.png" % v)).convert("RGBA")])
    if os.path.exists(os.path.join(CAND, "scale_vs_cod.png")):
        title("Same scale offline, 12x: trilja, vanilla cod")
        row([Image.open(os.path.join(CAND, "scale_vs_cod.png")).convert("RGBA")])
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None
        names = ["fish-trilja-side", "fish-trilja-three-quarter", "fish-trilja-top", "fish-trilja-beside-cod",
                 "fish-trilja-on-land", "fish-trilja-lineup"]
        present = [(n, shot(n)) for n in names]
        present = [(n, i) for n, i in present if i]
        if present:
            title("In the game: side, three-quarter, top; beside vanilla cod, on land, lineup (trilja, cod, cerna, small tonn)")
            row([i for _, i in present[:3]], h=330)
            row([i for _, i in present[3:]], h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (72, 72, 72, 255))
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_trilja_model.png")
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    for v, side in SIDES.items():
        for y, r in side.items():
            assert len(r) == 12, (v, y, len(r))
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
