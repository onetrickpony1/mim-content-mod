"""Placeholder art for the jellyfish (2026-11-18), so the mobs can be built and tested before their art.

Plain translucent boxes roughly the right shape and size, and simple icons. Not reviewed art: every file here is meant
to be replaced by the art makers, at the same path, following the jellyfish model contract in
docs/Tools and Process/Art pipeline.md ("Jellyfish models").

Writes, for each jellyfish:
  mod/src/main/java/com/maltaminecraft/mimcontent/client/jelly/<Name>Model.java   (extends JellyfishModel)
  textures/entity/jellyfish/<id>.png                                             (the mob, 64 x 64, with alpha)
  textures/item/<id>_spawn_egg.png                                               (16 x 16)
and the drops and the potion's effect:
  textures/item/jellyfish_venom.png, textures/item/jellyfish_meat.png             (16 x 16)
  textures/mob_effect/jellyfish_ward.png                                          (18 x 18)
plus the item definitions (items/<id>.json, models/item/<id>.json) for the eggs, venom and meat.
Run:  art/.venv/bin/python art/src/jelly_placeholders.py          (all)
      art/.venv/bin/python art/src/jelly_placeholders.py mauve_stinger   (only the ones named)
Never overwrites a file that already exists: a maker may have drawn it first. Delete a file to make its placeholder again.
"""
import json
import math
import os
import sys

from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "jelly")
TEX = 64


def ring(n, radius, y, length, start=0.0):
    """n tentacles round a bell's rim: parts of the root, each a thin plane hanging down."""
    out = []
    for i in range(n):
        a = start + 2 * math.pi * i / n
        out.append((f"tentacle_{i}", None, (round(radius * math.cos(a), 2), y, round(radius * math.sin(a), 2)),
                    [(0, 0, -0.5, 0, length, 1, "tentacle", "tentacle")]))
    return out


# Each jellyfish: colours (with alpha), then parts. A part: (name, parent, pivot (x, y, z), boxes). A box:
# (x, y, z, w, h, d, kind, share) in model pixels (16 = one block), y down, y 24 the bottom of the box; boxes with the
# same share key use the same patch of texture.
JELLY = {
    "mauve_stinger": {
        "name": "MauveStinger", "about": "Pelagia noctiluca: a small mauve bell dotted with warts, four frilly oral arms, eight thin tentacles",
        "colours": {"bell": (184, 106, 168, 190), "spot": (128, 52, 118, 220), "arm": (196, 120, 182, 170),
                    "tentacle": (210, 150, 200, 150)},
        "parts": [
            ("bell", None, (0, 17, 0), [(-4, -3.5, -4, 8, 3.5, 8, "bell spots", None), (-2.5, -4.5, -2.5, 5, 1, 5, "bell spots", None)]),
            ("oral_arms", "bell", (0, 0, 0), [(-1.5, 0, 0, 3, 6.5, 0, "arm", "arm"), (0, 0, -1.5, 0, 6.5, 3, "arm", "arm")]),
        ] + ring(8, 3.5, 17, 7, math.pi / 8),
        "egg": ((192, 122, 176), (110, 46, 102)),
    },
    "fried_egg_jellyfish": {
        "name": "FriedEggJellyfish", "about": "Cotylorhiza tuberculata: a wide, flat cream bell with a raised orange-yellow middle, short knobbed oral arms with violet tips",
        "colours": {"rim": (232, 217, 160, 200), "dome": (238, 200, 110, 215), "yolk": (226, 150, 50, 235),
                    "stem": (220, 200, 150, 200), "knob": (140, 118, 200, 225)},
        "parts": [
            ("bell", None, (0, 19, 0), [(-7, -2, -7, 14, 2, 14, "rim", None), (-5, -3.5, -5, 10, 1.5, 10, "dome", None),
                                       (-3, -4.5, -3, 6, 1, 6, "yolk", None)]),
            ("oral_arms", "bell", (0, 0, 0), [(-2, 0, -2, 4, 3, 4, "stem", None),
                                             (-3.5, 2, -1, 2, 2, 2, "knob", "knob"), (1.5, 2, -1, 2, 2, 2, "knob", "knob"),
                                             (-1, 2, -3.5, 2, 2, 2, "knob", "knob"), (-1, 2, 1.5, 2, 2, 2, "knob", "knob"),
                                             (-1, 3, -1, 2, 1.5, 2, "knob", "knob")]),
        ],
        "egg": ((236, 220, 168), (216, 154, 48)),
    },
    "man_o_war": {
        "name": "ManOWar", "about": "Physalia physalis: a gas-filled float, clear blue to violet, with a pink-edged crest, long dark blue tentacles hanging 3.5 blocks",
        "colours": {"float": (150, 185, 255, 175), "crest": (200, 140, 225, 200), "tentacle": (60, 80, 200, 200)},
        "parts": [
            ("bell", None, (0, 22, 0), [(-2.5, -2, -4.8, 5, 4, 9.6, "float", None), (0, -4.4, -4, 0, 2.4, 8, "crest", None)]),
        ] + [(f"tentacle_{i}", None, (x, 24, z), [(0, 0, -0.5, 0, length, 1, "tentacle", "tentacle")])
             for i, (x, z, length) in enumerate([(-1, -3, 56), (1, -1.5, 50), (-1, 0, 56), (1, 1.5, 52), (-1, 3, 48), (0.5, 3.8, 54)])],
        "egg": ((143, 176, 240), (176, 92, 200)),
    },
}


def box_uv_size(w, h, d):
    w, h, d = math.ceil(w), math.ceil(h), math.ceil(d)
    return 2 * (d + w), d + h


def pack(boxes):
    """Shelf-packs the boxes' UV areas into a TEX x TEX sheet; boxes with the same share key share one patch."""
    out, shared, x, y, row = [], {}, 0, 0, 0
    for b in boxes:
        if b[7] is not None and b[7] in shared:
            out.append(shared[b[7]])
            continue
        bw, bh = box_uv_size(*b[3:6])
        bw, bh = max(bw, 1), max(bh, 1)
        if x + bw > TEX:
            x, y, row = 0, y + row, 0
        out.append((x, y))
        if b[7] is not None:
            shared[b[7]] = (x, y)
        x += bw
        row = max(row, bh)
    assert y + row <= TEX, "texture too small"
    return out


def paint_box(img, jelly, uv, b):
    w, h, d = (math.ceil(v) for v in b[3:6])
    kind = b[6]
    colour = jelly["colours"][kind.split()[0]]
    u, v = uv
    px = img.load()
    for i in range(2 * (d + w)):
        for j in range(d + h):
            # skip the two unused corners of a box's UV layout
            if j < d and (i < d or i >= d + 2 * w):
                continue
            x, y = u + i, v + j
            if not (0 <= x < TEX and 0 <= y < TEX):
                continue
            t = (j - d) / max(1, h - 1) if j >= d else 0.0
            f = 1.0 - 0.18 * t - 0.05 * ((i + j) % 2)
            c = tuple(max(0, min(255, round(cv * f))) for cv in colour[:3]) + (colour[3],)
            if "spots" in kind and (i * 5 + j * 3) % 7 == 0:
                c = jelly["colours"]["spot"]
            px[x, y] = c


def f(x):
    return f"{float(x)}F"


def java_model(jid, jelly, uvs):
    name = jelly["name"]
    lines = [
        "package com.maltaminecraft.mimcontent.client.jelly;",
        "",
        "import net.minecraft.client.model.geom.ModelPart;",
        "import net.minecraft.client.model.geom.PartPose;",
        "import net.minecraft.client.model.geom.builders.CubeListBuilder;",
        "import net.minecraft.client.model.geom.builders.LayerDefinition;",
        "import net.minecraft.client.model.geom.builders.MeshDefinition;",
        "import net.minecraft.client.model.geom.builders.PartDefinition;",
        "",
        "/**",
        f" * PLACEHOLDER model of the {jid} ({jelly['about']}): plain boxes until its art.",
        " * Made by art/src/jelly_placeholders.py; the art makers replace this file, keeping the jellyfish model contract",
        " * (docs/Tools and Process/Art pipeline.md, \"Jellyfish models\"). Texture: textures/entity/jellyfish/" + jid + ".png.",
        " */",
        f"public class {name}Model extends JellyfishModel {{",
        f"    public {name}Model(ModelPart root) {{",
        "        super(root);",
        "    }",
        "",
        "    public static LayerDefinition createBodyLayer() {",
        "        MeshDefinition mesh = new MeshDefinition();",
        "        PartDefinition root = mesh.getRoot();",
    ]
    k = 0
    parents = {p[1] for p in jelly["parts"] if p[1]}
    for pname, parent, pivot, boxes in jelly["parts"]:
        cubes = []
        for b in boxes:
            u, v = uvs[k]
            k += 1
            cubes.append(f".texOffs({u}, {v}).addBox({f(b[0])}, {f(b[1])}, {f(b[2])}, {f(b[3])}, {f(b[4])}, {f(b[5])})")
        var = "PartDefinition " + pname.replace("_", "") + " = " if pname in parents else ""
        owner = parent.replace("_", "") if parent else "root"
        lines.append(f"        {var}{owner}.addOrReplaceChild(\"{pname}\", CubeListBuilder.create()"
                     + "".join("\n            " + c for c in cubes)
                     + f",\n            PartPose.offset({f(pivot[0])}, {f(pivot[1])}, {f(pivot[2])}));")
    lines += [f"        return LayerDefinition.create(mesh, {TEX}, {TEX});", "    }", "}", ""]
    return "\n".join(lines)


def outline(img):
    px = img.load()
    w, h = img.size
    solid = {(x, y) for x in range(w) for y in range(h) if px[x, y][3] > 0}
    for (x, y) in solid:
        if any((x + dx, y + dy) not in solid for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            r, g, b, a = px[x, y]
            px[x, y] = (r // 2, g // 2, b // 2, 255)


def icon_egg(base, spot):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for x in range(16):
        for y in range(16):
            nx, ny = (x + 0.5 - 8) / 5.2, (y + 0.5 - 8.8) / 6.6
            if ny < 0:
                nx *= 1.12
            if nx * nx + ny * ny <= 1:
                px[x, y] = (spot if (x * 3 + y * 5) % 7 == 0 else base) + (255,)
    outline(img)
    return img


def icon_venom():
    """A drop of venom: violet, a pale highlight."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for x in range(16):
        for y in range(16):
            cx, cy = x + 0.5 - 8, y + 0.5 - 10
            r = 4.5
            inside = cx * cx + cy * cy <= r * r or (cy < 0 and abs(cx) <= r * (1 + cy / 8.5) and cy > -8.5)
            if inside:
                px[x, y] = (150, 80, 190, 255)
    for (x, y) in ((6, 8), (6, 9), (7, 7)):
        px[x, y] = (225, 200, 240, 255)
    outline(img)
    return img


def icon_meat():
    """A slab of jellyfish meat: a pale, translucent-looking pinkish strip."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for x in range(2, 14):
        for y in range(5, 12):
            if (x in (2, 13) and y in (5, 11)):
                continue
            wave = 1 if (x + y) % 5 == 0 else 0
            px[x, y] = (232 - 12 * wave, 196 - 10 * wave, 184, 255)
    for x in range(4, 12, 3):
        px[x, 7] = (250, 230, 225, 255)
    outline(img)
    return img


def icon_ward():
    """Jellyfish Ward: a pale blue bell, 18 x 18."""
    img = Image.new("RGBA", (18, 18), (0, 0, 0, 0))
    px = img.load()
    for x in range(18):
        for y in range(18):
            cx, cy = x + 0.5 - 9, y + 0.5 - 9
            if cy <= 1 and cx * cx / 49 + cy * cy / 36 <= 1:
                px[x, y] = (143, 211, 232, 255)
            elif 1 < cy <= 6 and x in (5, 8, 9, 12) and (y + x) % 2 == 0:
                px[x, y] = (110, 170, 210, 255)
    outline(img)
    return img


def fresh(path):
    """True if the file doesn't exist yet; an existing file is kept and reported."""
    if os.path.exists(path):
        print("  kept", os.path.relpath(path, ROOT))
        return False
    return True


def write_json(path, data):
    if fresh(path):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1)
            fh.write("\n")


def item_files(item_id):
    write_json(os.path.join(RES, "items", item_id + ".json"),
               {"model": {"type": "minecraft:model", "model": "mimcontent:item/" + item_id}})
    write_json(os.path.join(RES, "models", "item", item_id + ".json"),
               {"parent": "minecraft:item/generated", "textures": {"layer0": "mimcontent:item/" + item_id}})


def main(ids):
    unknown = [i for i in ids if i not in JELLY]
    if unknown:
        sys.exit("unknown: " + " ".join(unknown) + "  (names: " + " ".join(JELLY) + ")")
    os.makedirs(JAVA, exist_ok=True)
    for sub in ("textures/entity/jellyfish", "textures/item", "textures/mob_effect", "items", "models/item"):
        os.makedirs(os.path.join(RES, sub), exist_ok=True)
    for jid in ids or list(JELLY):
        jelly = JELLY[jid]
        boxes = [b for _, _, _, bs in jelly["parts"] for b in bs]
        uvs = pack(boxes)
        img = Image.new("RGBA", (TEX, TEX), (0, 0, 0, 0))
        done = set()
        for uv, b in zip(uvs, boxes):
            if uv not in done:
                paint_box(img, jelly, uv, b)
                done.add(uv)
        # the model and its texture go together: the texture's layout only fits this model
        tex = os.path.join(RES, "textures/entity/jellyfish", jid + ".png")
        path = os.path.join(JAVA, jelly["name"] + "Model.java")
        if fresh(tex) and fresh(path):
            img.save(tex)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(java_model(jid, jelly, uvs))
        egg = os.path.join(RES, "textures/item", jid + "_spawn_egg.png")
        if fresh(egg):
            icon_egg(*jelly["egg"]).save(egg)
        item_files(jid + "_spawn_egg")
        print("done", jid)
    if not ids:
        for item_id, make in (("jellyfish_venom", icon_venom), ("jellyfish_meat", icon_meat)):
            out = os.path.join(RES, "textures/item", item_id + ".png")
            if fresh(out):
                make().save(out)
            item_files(item_id)
        out = os.path.join(RES, "textures/mob_effect", "jellyfish_ward.png")
        if fresh(out):
            icon_ward().save(out)
        print("done venom, meat, ward")


if __name__ == "__main__":
    main(sys.argv[1:])
