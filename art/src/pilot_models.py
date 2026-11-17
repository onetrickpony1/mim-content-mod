"""Art pilot models (2026-11-17): the kenur (portable limestone stove, one pot) and the borma (terracotta stew pot).

Geometry from the reference photos art/references/kenur_1.jpg, kenur_2.jpg. Writes block models, the kenur's
blockstate, item definitions and the English names into the mod's resources.
Run: art/.venv/bin/python art/src/pilot_models.py
"""
import json
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
NS = "mimcontent"


def uv(face, f, t):
    """Minecraft's own default UV for a face of a box from f to t (so explicit UVs match unshifted boxes)."""
    (x1, y1, z1), (x2, y2, z2) = f, t
    return {
        "north": [16 - x2, 16 - y2, 16 - x1, 16 - y1],
        "south": [x1, 16 - y2, x2, 16 - y1],
        "west": [z1, 16 - y2, z2, 16 - y1],
        "east": [16 - z2, 16 - y2, 16 - z1, 16 - y1],
        "up": [x1, z1, x2, z2],
        "down": [x1, 16 - z2, x2, 16 - z1],
    }[face]


def box(f, t, faces, dy=0, shade=True):
    """faces: {face: texture_var}. UVs are taken from the unshifted box, then the box is moved up by dy."""
    e = {
        "from": [f[0], f[1] + dy, f[2]],
        "to": [t[0], t[1] + dy, t[2]],
        "faces": {k: {"uv": uv(k, f, t), "texture": "#" + v} for k, v in faces.items()},
    }
    if not shade:
        e["shade"] = False
    return e


ALL = ("north", "south", "east", "west")


def kenur_elements():
    """Review r1: wide prongs front and back (5 px), a deep U notch between them, thin in z so the pot clears them;
    walls inset 1 px at the bottom (y 1..3) instead of a floating plinth; an arched mouth."""
    S, T, I, F = "side", "top", "soot", "front"
    e = []
    e.append(box([2, 0, 2], [14, 3, 14], {"north": F, "south": S, "east": S, "west": S, "down": T}))  # tapered foot
    e.append(box([1, 3, 1], [5, 9, 15], {"west": S, "north": F, "south": S, "east": I, "up": T}))    # left wall
    e.append(box([11, 3, 1], [15, 9, 15], {"east": S, "north": F, "south": S, "west": I, "up": T}))  # right wall
    e.append(box([5, 3, 11], [11, 9, 15], {"south": S, "north": I, "up": T}))                        # back wall
    e.append(box([5, 6, 1], [11, 9, 5], {"north": F, "down": I, "south": I, "up": T}))               # lintel
    e.append(box([5, 5, 1], [6, 6, 5], {"north": F, "down": I, "east": I}))                          # arch corners
    e.append(box([10, 5, 1], [11, 6, 5], {"north": F, "down": I, "west": I}))
    e.append(box([5, 2, 2], [11, 3, 11], {"up": "ash"}))                                             # ash bed
    # the rim (y 9..10) with the hole for the pot, and no rim in the notches at front and back
    e.append(box([1, 9, 1], [6, 10, 4], {"up": T, "north": F, "west": S, "east": S, "south": I}))
    e.append(box([10, 9, 1], [15, 10, 4], {"up": T, "north": F, "east": S, "west": S, "south": I}))
    e.append(box([1, 9, 12], [6, 10, 15], {"up": T, "south": S, "west": S, "east": S, "north": I}))
    e.append(box([10, 9, 12], [15, 10, 15], {"up": T, "south": S, "east": S, "west": S, "north": I}))
    e.append(box([1, 9, 4], [3, 10, 12], {"up": T, "west": S, "east": I}))
    e.append(box([13, 9, 4], [15, 10, 12], {"up": T, "east": S, "west": I}))
    # the four prongs: 5 px along the front and back, 2 px deep
    for x in ((1, 6), (10, 15)):
        for z, face in (((1, 3), F), ((13, 15), S)):
            e.append(box([x[0], 10, z[0]], [x[1], 14, z[1]],
                         {"north": face if z[0] == 1 else S, "south": S, "east": S, "west": S, "up": T}))
    return e


def fire_elements():
    out = []
    for angle in (45, -45):
        out.append({
            "from": [5, 2, 4], "to": [11, 8, 4], "shade": False,
            "rotation": {"origin": [8, 4, 4], "axis": "y", "angle": angle},
            "faces": {"north": {"uv": [2, 4, 14, 16], "texture": "#fire"}, "south": {"uv": [2, 4, 14, 16], "texture": "#fire"}},
        })
    return out


def borma_elements(dy, top):
    """Review r1: a wide barrel, mouth nearly as wide as the belly, a 1 px lip, hollow 3 px deep,
    loop handles from the rim down to the shoulder, 1 px thin."""
    C = "clay"
    allc = {**{k: C for k in ALL}, "up": C, "down": C}
    e = []
    e.append(box([4, 0, 4], [12, 1, 12], {**{k: C for k in ALL}, "down": C}, dy))                  # foot
    e.append(box([3, 1, 3], [13, 8, 13], {**{k: C for k in ALL}, "down": C, "up": top}, dy))        # body; inside floor at y 8
    for f, t in (([3, 8, 3], [13, 10, 4]), ([3, 8, 12], [13, 10, 13]), ([3, 8, 4], [4, 10, 12]), ([12, 8, 4], [13, 10, 12])):
        e.append(box(f, t, allc, dy))                                                                 # walls of the mouth
    for f, t in (([2, 10, 2], [14, 11, 3]), ([2, 10, 13], [14, 11, 14]), ([2, 10, 3], [3, 11, 13]), ([13, 10, 3], [14, 11, 13])):
        e.append(box(f, t, allc, dy))                                                                 # the lip
    for f, t in (([1, 9, 8], [2, 10, 9]), ([0, 6, 8], [1, 10, 9]), ([1, 6, 8], [3, 7, 9]),
                 ([14, 9, 8], [15, 10, 9]), ([15, 6, 8], [16, 10, 9]), ([13, 6, 8], [15, 7, 9])):
        e.append(box(f, t, allc, dy))                                                                 # handles
    return e


GUI = {"gui": {"rotation": [30, 225, 0], "translation": [0, 0, 0], "scale": [0.8, 0.8, 0.8]}}


def model(elements, textures, parent="minecraft:block/block"):
    return {"parent": parent, "textures": textures, "elements": elements, "display": GUI}


def write(rel, data):
    p = os.path.join(RES, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("wrote", rel)


def main():
    k_tex = {"particle": f"{NS}:block/kenur_side", "side": f"{NS}:block/kenur_side", "top": f"{NS}:block/kenur_top",
             "soot": f"{NS}:block/kenur_soot", "ash": f"{NS}:block/kenur_ash",
             "front": f"{NS}:block/kenur_front"}
    write("models/block/kenur.json", model(kenur_elements(), k_tex))
    write("models/block/kenur_lit.json", model(kenur_elements() + fire_elements(),
                                               {**k_tex, "ash": f"{NS}:block/kenur_ash_lit", "fire": "minecraft:block/campfire_fire"}))
    clay = {"particle": f"{NS}:block/borma_side", "clay": f"{NS}:block/borma_side"}
    for contents in ("empty", "stuffat"):
        tex = {**clay, "inside": f"{NS}:block/borma_top_{contents}"}
        name = "borma" if contents == "empty" else "borma_stuffat"
        write(f"models/block/{name}.json", model(borma_elements(0, "inside"), tex))
        write(f"models/block/kenur_pot_{contents}.json", {"textures": tex, "elements": borma_elements(10, "inside")})

    rot = {"north": 0, "east": 90, "south": 180, "west": 270}
    parts = []
    for facing, y in rot.items():
        for lit in (False, True):
            parts.append({"when": {"facing": facing, "lit": str(lit).lower()},
                          "apply": {"model": f"{NS}:block/kenur" + ("_lit" if lit else ""), "y": y}})
        for pot in ("empty", "stuffat"):
            parts.append({"when": {"facing": facing, "pot": pot}, "apply": {"model": f"{NS}:block/kenur_pot_{pot}", "y": y}})
    write("blockstates/kenur.json", {"multipart": parts})
    write("blockstates/borma.json", {"variants": {"": {"model": f"{NS}:block/borma"}}})
    write("blockstates/borma_stuffat.json", {"variants": {"": {"model": f"{NS}:block/borma_stuffat"}}})

    for b in ("kenur", "borma", "borma_stuffat"):
        write(f"items/{b}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:block/{b}"}})
    for i in ("hobz_malti", "pastizz_irkotta", "gbejna"):
        write(f"models/item/{i}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{i}"}})
        write(f"items/{i}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:item/{i}"}})

    write("lang/en_us.json", {
        "block.mimcontent.kenur": "Kenur",
        "block.mimcontent.borma": "Borma",
        "block.mimcontent.borma_stuffat": "Borma of Stuffat tal-Fenek",
        "item.mimcontent.hobz_malti": "Ħobż tal-Malti",
        "item.mimcontent.pastizz_irkotta": "Pastizz tal-Irkotta",
        "item.mimcontent.gbejna": "Ġbejna",
    })


if __name__ == "__main__":
    main()
