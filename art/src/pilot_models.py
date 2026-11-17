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
    """r1: wide prongs, U notch, tapered foot, arched mouth. r2: taller mouth (y 3..7), lighter smoke-stained
    inside walls (not black), prongs 3 tall so the pot's belly clears them."""
    S, T, I, F, N_ = "side", "top", "soot", "front", "inner"
    e = []
    e.append(box([2, 0, 2], [14, 3, 14], {"north": F, "south": S, "east": S, "west": S, "down": T}))   # tapered foot
    e.append(box([1, 3, 1], [5, 9, 15], {"west": S, "north": F, "south": S, "east": N_, "up": T}))     # left wall
    e.append(box([11, 3, 1], [15, 9, 15], {"east": S, "north": F, "south": S, "west": N_, "up": T}))   # right wall
    e.append(box([5, 3, 11], [11, 9, 15], {"south": S, "north": N_, "up": T}))                        # back wall
    e.append(box([5, 7, 1], [11, 9, 5], {"north": F, "down": I, "south": N_, "up": T}))               # lintel
    e.append(box([5, 6, 1], [6, 7, 5], {"north": F, "down": I, "east": I}))                           # arch corners
    e.append(box([10, 6, 1], [11, 7, 5], {"north": F, "down": I, "west": I}))
    e.append(box([5, 2, 2], [11, 3, 11], {"up": "ash"}))                                              # ash bed
    e.append(box([1, 9, 1], [6, 10, 4], {"up": T, "north": F, "west": S, "east": S, "south": N_}))   # rim
    e.append(box([10, 9, 1], [15, 10, 4], {"up": T, "north": F, "east": S, "west": S, "south": N_}))
    e.append(box([1, 9, 12], [6, 10, 15], {"up": T, "south": S, "west": S, "east": S, "north": N_}))
    e.append(box([10, 9, 12], [15, 10, 15], {"up": T, "south": S, "east": S, "west": S, "north": N_}))
    e.append(box([1, 9, 4], [3, 10, 12], {"up": T, "west": S, "east": N_}))
    e.append(box([13, 9, 4], [15, 10, 12], {"up": T, "east": S, "west": N_}))
    for x in ((1, 6), (10, 15)):                                                                       # prongs
        for z in ((1, 3), (13, 15)):
            e.append(box([x[0], 10, z[0]], [x[1], 13, z[1]],
                         {"north": F if z[0] == 1 else S, "south": S, "east": S, "west": S, "up": T}))
    return e


def fire_elements():
    out = []
    for angle in (45, -45):
        out.append({
            "from": [5, 3, 3.5], "to": [11, 9, 3.5], "shade": False,
            "rotation": {"origin": [8, 5, 3.5], "axis": "y", "angle": angle},
            "faces": {"north": {"uv": [2, 4, 14, 16], "texture": "#fire"}, "south": {"uv": [2, 4, 14, 16], "texture": "#fire"}},
        })
    return out


def borma_elements(dy, top, on_kenur=False):
    """r2: a real belly (2..14) over a narrower base, a 2-px lip ring covering the wall tops, hollow 3 px deep,
    loop handles from the lip down to the belly. On a kenur the foot is wider, so it rests on the stove's ledges."""
    C = "clay"
    allc = {**{k: C for k in ALL}, "up": C, "down": C}
    sides = {k: C for k in ALL}
    e = []
    foot = ([3, 0, 3], [13, 1, 13]) if on_kenur else ([4, 0, 4], [12, 1, 12])
    e.append(box(foot[0], foot[1], {**sides, "down": C}, dy))                                         # foot
    e.append(box([3, 1, 3], [13, 3, 13], {**sides, "down": C}, dy))                                   # lower body
    e.append(box([2, 3, 2], [14, 8, 14], {**sides, "down": C, "up": top}, dy))                        # belly; inside floor y 8
    e.append(box([1, 4, 1], [15, 7, 15], {**sides, "up": C, "down": C}, dy))                          # r3: the belly bulge
    for f, t in (([3, 8, 3], [13, 10, 4]), ([3, 8, 12], [13, 10, 13]), ([3, 8, 4], [4, 10, 12]), ([12, 8, 4], [13, 10, 12])):
        e.append(box(f, t, sides, dy))                                                                 # shoulder walls
    for f, t in (([2, 10, 2], [14, 11, 4]), ([2, 10, 12], [14, 11, 14]), ([2, 10, 4], [4, 11, 12]), ([12, 10, 4], [14, 11, 12])):
        e.append(box(f, t, allc, dy))                                                                  # lip ring
    for f, t in (([0, 9, 7.5], [3, 10, 8.5]), ([0, 6, 7.5], [1, 10, 8.5]), ([0, 6, 7.5], [2, 7, 8.5]),
                 ([13, 9, 7.5], [16, 10, 8.5]), ([15, 6, 7.5], [16, 10, 8.5]), ([14, 6, 7.5], [16, 7, 8.5])):
        e.append(box(f, t, allc, dy))                                                                  # handles
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
             "front": f"{NS}:block/kenur_front", "inner": f"{NS}:block/kenur_inner"}
    write("models/block/kenur.json", model(kenur_elements(), k_tex))
    write("models/block/kenur_lit.json", model(kenur_elements() + fire_elements(),
                                               {**k_tex, "ash": f"{NS}:block/kenur_ash_lit", "fire": "minecraft:block/campfire_fire"}))
    clay = {"particle": f"{NS}:block/borma_side", "clay": f"{NS}:block/borma_side"}
    for contents in ("empty", "stuffat"):
        tex = {**clay, "inside": f"{NS}:block/borma_top_{contents}"}
        name = "borma" if contents == "empty" else "borma_stuffat"
        write(f"models/block/{name}.json", model(borma_elements(0, "inside"), tex))
        write(f"models/block/kenur_pot_{contents}.json", {"textures": tex, "elements": borma_elements(10, "inside", on_kenur=True)})

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
    for i in ("hobz_malti", "pastizz_irkotta", "pastizz_pizelli", "pastizz_xema_irkotta", "pastizz_xema_pizelli", "ftira", "hobz_bizzejt", "ftira_ghawdxija", "imqaret", "kannoli", "qaghaq_ghasel", "stuffat_fenek", "aljotta", "stuffat_qarnit", "bigilla", "galletti", "gbejna"):
        write(f"models/item/{i}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{i}"}})
        write(f"items/{i}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:item/{i}"}})

    write("lang/en_us.json", {
        "block.mimcontent.kenur": "Kenur",
        "block.mimcontent.borma": "Borma",
        "block.mimcontent.borma_stuffat": "Borma of Stuffat tal-Fenek",
        "item.mimcontent.hobz_malti": "Ħobż tal-Malti",
        "item.mimcontent.pastizz_irkotta": "Pastizz tal-Irkotta",
        "item.mimcontent.pastizz_pizelli": "Pastizz tal-Piżelli",
        "item.mimcontent.pastizz_xema_irkotta": "Pastizz tax-Xema' tal-Irkotta",
        "item.mimcontent.pastizz_xema_pizelli": "Pastizz tax-Xema' tal-Piżelli",
        "item.mimcontent.ftira": "Ftira",
        "item.mimcontent.hobz_bizzejt": "Ħobż biż-Żejt",
        "item.mimcontent.ftira_ghawdxija": "Ftira Għawdxija",
        "item.mimcontent.imqaret": "Imqaret",
        "item.mimcontent.kannoli": "Kannoli",
        "item.mimcontent.qaghaq_ghasel": "Qagħaq tal-Għasel",
        "item.mimcontent.stuffat_fenek": "Stuffat tal-Fenek",
        "item.mimcontent.aljotta": "Aljotta",
        "item.mimcontent.stuffat_qarnit": "Stuffat tal-Qarnit",
        "item.mimcontent.bigilla": "Bigilla",
        "item.mimcontent.galletti": "Galletti",
        "item.mimcontent.gbejna": "Ġbejna",
    })


if __name__ == "__main__":
    main()
