"""Placeholder art for the tier A fish (2026-11-17), so the mobs can be built and tested before the art round.

Plain coloured boxes roughly the right shape and size, and simple icons. Not reviewed art: every file here is meant to
be replaced by the art makers, at the same path, following the fish model contract in
docs/Tools and Process/Art pipeline.md ("Fish models").

Writes, for each fish:
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/<Name>Model.java   (extends FishModel)
  textures/entity/fish/<id>.png                                                  (the mob, 64 x 64)
  textures/item/<id>_bucket.png, textures/item/<id>_spawn_egg.png                (16 x 16 icons)
  textures/item/<id>.png                                                          (the caught fish; never the lampuka,
                                                                                   whose icon is accepted art)
Run:  art/.venv/bin/python art/src/fish_placeholders.py pixxispad      (only the fish named)
Never overwrites a file that already exists: most of these files are now drawn, accepted art. Delete a file first to
make its placeholder again.
"""
import math
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from egg_pool import vanilla_pool  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish")
TEX = 64

# Each fish: colours, then parts. A part: (name, parent, pivot (x, y, z), boxes). A box: (x, y, z, w, h, d, kind),
# in model pixels (16 = one block), head toward -z, y down, the root pivot at the ground (y 24) like vanilla.
# kind "body" is shaded back/side/belly; "fin" is one flat colour. "eye": the box gets an eye near its front.
FISH = {
    "sardina": {
        "name": "Sardina", "about": "sardine: small, slim, silver with a blue-green back",
        "back": "#2f5d7a", "side": "#b9c6cf", "belly": "#e8eef0", "fin": "#8fa3ad", "accent": None,
        "parts": [
            ("body", None, (0, 22.5, 0), [(-1, -1.5, -4, 2, 3, 6, "body eye")]),
            ("top_fin", None, (0, 21, -1), [(0, -1, 0, 0, 1, 2, "fin")]),
            ("tail_fin", None, (0, 22.5, 2), [(0, -1.5, 0, 0, 3, 3, "fin")]),
        ],
    },
    "awrata": {
        "name": "Awrata", "about": "gilthead sea bream: deep oval body, silver grey, a gold band between the eyes",
        "back": "#6f7f86", "side": "#b8c0c2", "belly": "#e3e6e2", "fin": "#7d8a8f", "accent": "#d9b84a",
        "parts": [
            ("body", None, (0, 21, 0), [(-1, -3, -5, 2, 6, 8, "body eye accent")]),
            ("top_fin", None, (0, 18, -3), [(0, -1, 0, 0, 1, 6, "fin")]),
            ("tail_fin", None, (0, 21, 3), [(0, -3, 0, 0, 6, 3, "fin")]),
        ],
    },
    "cerna": {
        "name": "Cerna", "about": "dusky grouper: heavy, wide-mouthed, dark brown with pale blotches",
        "back": "#4a3a2c", "side": "#7a5c40", "belly": "#c9b48f", "fin": "#5a4632", "accent": "#b39a74",
        "parts": [
            ("body", None, (0, 20.5, 0), [(-2.5, -3.5, -7, 5, 7, 11, "body eye blotch")]),
            ("top_fin", None, (0, 17, -4), [(0, -1, 0, 0, 1, 9, "fin")]),
            ("tail_fin", None, (0, 20.5, 4), [(0, -3, 0, 0, 6, 4, "fin")]),
        ],
    },
    "tonn": {
        "name": "Tonn", "about": "Atlantic bluefin tuna: big torpedo, dark blue back, silver sides, tall forked tail",
        "back": "#1d2a4a", "side": "#8d99ab", "belly": "#dfe4ea", "fin": "#22304f", "accent": "#d8c048",
        "parts": [
            ("body", None, (0, 20, 0), [(-3, -4, -10, 6, 8, 16, "body eye"), (-1, -1.5, 6, 2, 3, 3, "body accent")]),
            ("top_fin", None, (0, 16, -3), [(0, -2, 0, 0, 2, 4, "fin")]),
            ("tail_fin", None, (0, 20, 9), [(0, -5, 0, 0, 10, 3, "fin fork")]),
        ],
    },
    "lampuka": {
        "name": "Lampuka", "about": "dolphinfish: blunt head, long dorsal fin, blue-green back over golden sides",
        "back": "#2f7d6a", "side": "#d9b938", "belly": "#f0e6a8", "fin": "#3a8f9a", "accent": None,
        "parts": [
            ("body", None, (0, 21, 0), [(-1, -3, -7, 2, 6, 12, "body eye")]),
            ("top_fin", None, (0, 18, -6), [(0, -1, 0, 0, 1, 11, "fin")]),
            ("tail_fin", None, (0, 21, 5), [(0, -3, 0, 0, 6, 4, "fin fork")]),
        ],
    },
    "murina": {
        "name": "Murina", "about": "Mediterranean moray: long, thin, dark brown mottled with yellow",
        "back": "#3a2e1f", "side": "#6b5a2f", "belly": "#a08a4a", "fin": "#4a3c24", "accent": "#c8b25a",
        "parts": [
            ("body", None, (0, 22.5, 0), [(-1, -1.5, -9, 2, 3, 9, "body eye blotch")]),
            ("tail", None, (0, 22.5, 0), [(-1, -1.5, 0, 2, 3, 8, "body blotch"), (0, -2.5, 0, 0, 1, 8, "fin")]),
            ("tail_fin", "tail", (0, 0, 8), [(0, -1.5, 0, 0, 3, 2, "fin")]),
        ],
    },
    "ziemel": {
        "name": "Ziemel", "about": "seahorse: upright, horse head with a long snout, curled tail, sandy brown",
        "back": "#8a6a2c", "side": "#c9a64e", "belly": "#e3cc84", "fin": "#d8c27a", "accent": None,
        "parts": [
            ("body", None, (0, 20.5, 0), [(-1, -3.5, -1, 2, 6, 2, "body"), (-1, -4.5, -1.5, 2, 1, 2, "body eye"),
                                          (-0.5, -4.5, -3.5, 1, 1, 2, "body"), (-0.5, 2.5, 0, 1, 1, 2, "body"),
                                          (-0.5, 3.5, 1, 1, 0, 1, "fin")]),
            ("top_fin", None, (0, 19, 1), [(0, -1, 0, 0, 2, 1, "fin")]),
        ],
    },
    # tier B (2026-11-18): about 2.7 blocks long with the sword, like a real 2-3 m fish scaled as the tonn is
    "pixxispad": {
        "name": "Pixxispad", "about": "swordfish: long flat sword, tall sickle dorsal fin, dark purple-brown back, "
                                       "bronze-silver sides, crescent tail",
        "back": "#2e2a40", "side": "#8e8790", "belly": "#d8d4cc", "fin": "#2a2738", "accent": None,
        "parts": [
            ("body", None, (0, 20, 0), [(-2, -3, -10, 4, 6, 20, "body"), (-1.5, -2.5, -14, 3, 5, 4, "body eye"),
                                        (-0.5, -1.5, -27, 1, 1, 13, "fin"), (-1, -1.5, 10, 2, 3, 4, "body")]),
            ("top_fin", None, (0, 17, -8), [(0, -5, 0, 0, 5, 4, "fin")]),
            ("tail_fin", None, (0, 20, 14), [(0, -6, 0, 0, 12, 4, "fin fork")]),
        ],
    },
    # tier B (2026-11-18): the inċova (a little smaller and slimmer than the sardina), the ċawl and the ħuta kaħla
    "incova": {
        "name": "Incova", "about": "anchovy: small and slim, blue-green back, a silver stripe along bright silver sides",
        "back": "#3d6f86", "side": "#c7d0d4", "belly": "#eef2f2", "fin": "#9aaab2", "accent": None,
        "parts": [
            ("body", None, (0, 22.5, 0), [(-1, -1, -5, 2, 2, 9, "body eye")]),
            ("top_fin", None, (0, 21.5, -1), [(0, -1, 0, 0, 1, 2, "fin")]),
            ("tail_fin", None, (0, 22.5, 4), [(0, -1.5, 0, 0, 3, 3, "fin")]),
        ],
    },
    "cawl": {
        "name": "Cawl", "about": "Mediterranean damselfish: small, deep oval body, dark brown-black, deeply forked tail",
        "back": "#2a2620", "side": "#4a4236", "belly": "#6e6352", "fin": "#3a342b", "accent": None,
        "parts": [
            ("body", None, (0, 20.5, 0), [(-1, -2.5, -4, 2, 5, 7, "body eye")]),
            ("top_fin", None, (0, 18, -3), [(0, -1, 0, 0, 1, 5, "fin")]),
            ("tail_fin", None, (0, 20.5, 3), [(0, -3, 0, 0, 6, 3, "fin fork")]),
        ],
    },
    # about 2.6 blocks long (42 px): a slender blue body, long snout, tall dorsal fin, long pectorals and a heterocercal tail
    # (the upper lobe much longer than the lower)
    "huta_kahla": {
        "name": "HutaKahla", "about": "blue shark: slender, deep blue back, bright blue sides, white belly, long "
                                        "pectoral fins, tall dorsal fin, tail with a long upper lobe",
        "back": "#2b4f9c", "side": "#4f7fd0", "belly": "#e8edf2", "fin": "#2f559e", "accent": None,
        "parts": [
            ("body", None, (0, 20, 0), [(-2.5, -3, -14, 5, 6, 20, "body"), (-1.5, -2, -20, 3, 4, 6, "body eye"),
                                        (-1.5, -2, 6, 3, 4, 8, "body")]),
            ("top_fin", None, (0, 17, -6), [(0, -6, 0, 0, 6, 5, "fin")]),
            ("right_fin", None, (-2.5, 22, -10), [(-6, 0, 0, 6, 0, 5, "fin")]),
            ("left_fin", None, (2.5, 22, -10), [(0, 0, 0, 6, 0, 5, "fin")]),
            ("tail_fin", None, (0, 20, 14), [(0, -9, 0, 0, 8, 8, "fin"), (0, -1, 0, 0, 4, 3, "fin")]),
        ],
    },
    # tier B (2026-11-18, "Stingray next"): the common stingray, a flat disc 16 px (1 block) wide and 14 px long, 2.5 px
    # thick, with a whip tail 20 px long and the spine near its end; 34 px (2.1 blocks) in all. A ray model extends
    # RayModel (its own animation: the wings ripple up and down, the tail trails; no fish wag). Parts, by name, for the
    # art makers: body (middle of the disc), left_wing / right_wing (children of body), left_wing_tip / right_wing_tip
    # (the outer edges, children of the wings), tail (root child, from the back of the disc) and spine (child of tail).
    "boll": {
        "name": "Boll", "base": "RayModel",
        "about": "common stingray: flat rhombic disc, olive grey-brown back, white belly, long thin whip tail with a spine",
        "back": "#6b5f4c", "side": "#86775f", "belly": "#e6e0d4", "fin": "#4f4536", "accent": None,
        "parts": [
            ("body", None, (0, 22.5, 0), [(-3, -1, -7, 6, 2.5, 13, "body eye"), (-2, -0.5, -8, 4, 2, 1, "body")]),
            ("left_wing", "body", (3, 1, 0), [(0, -0.5, -6.5, 3, 1, 11, "body")]),
            ("left_wing_tip", "left_wing", (3, 0, 0), [(0, -0.5, -4.5, 2, 1, 7, "body")]),
            ("right_wing", "body", (-3, 1, 0), [(-3, -0.5, -6.5, 3, 1, 11, "body")]),
            ("right_wing_tip", "right_wing", (-3, 0, 0), [(-2, -0.5, -4.5, 2, 1, 7, "body")]),
            ("tail", None, (0, 23, 6), [(-0.5, -0.5, 0, 1, 1, 20, "fin")]),
            ("spine", "tail", (0, -0.5, 15), [(-0.5, -0.5, 0, 1, 0.5, 4, "fin")]),
        ],
    },
    # tier B (2026-11-18, "Skorfna - start"): the black scorpionfish, stocky and big-headed, 13 px (0.81 blocks) long,
    # a little larger than life so the spines show. A normal FishModel (it wags like the others). Parts, by name, for the
    # art makers: body (cubes: head with the eyes, jaw = the big mouth, trunk, stalk = the tail's base), head_flaps
    # (child of body: the fleshy flaps above the eyes), top_fin (the tall spiny dorsal fin), left_fin / right_fin (the
    # fan-like pectoral fins, spread to rest on), tail_fin (the rounded tail, which sways).
    "skorfna": {
        "name": "Skorfna",
        "about": "black scorpionfish: stocky and big-headed, mottled brown, fleshy flaps over the eyes, big mouth, "
                 "tall spiny dorsal fin, fan-like pectoral fins",
        "back": "#4f3d2c", "side": "#76603f", "belly": "#c2ae8e", "fin": "#5d4a35", "accent": "#a68c62",
        "parts": [
            ("body", None, (0, 21, 0), [(-2.5, -2.5, -6, 5, 5, 4, "body eye blotch"), (-2, 1.5, -6.5, 4, 1, 1, "body"),
                                        (-2, -2.5, -2, 4, 4.5, 4, "body blotch"), (-1, -1.5, 2, 2, 3, 2, "body blotch")]),
            ("head_flaps", "body", (0, -2.5, -5), [(-2, -1, 0, 0, 1, 2, "fin"), (2, -1, 0, 0, 1, 2, "fin")]),
            ("top_fin", None, (0, 18.5, -4), [(0, -3, 0, 0, 3, 8, "fin")]),
            ("right_fin", None, (-2, 22.5, -2), [(-3, 0, 0, 3, 0, 3, "fin")]),
            ("left_fin", None, (2, 22.5, -2), [(0, 0, 0, 3, 0, 3, "fin")]),
            ("tail_fin", None, (0, 21, 4), [(0, -2.5, 0, 0, 5, 3, "fin")]),
        ],
    },
    # tier C (2026-11-18, "Mola mola - start"): the ocean sunfish, a tall flat disc with no tail, very tall dorsal and anal
    # fins far back and the clavus as a rim behind. Extremely rare (owner 2026-11-18). Only its icon, bucket and egg are
    # placeholders: the model and its texture are drawn by art/src/fish_mola_model.py.
    "mola_mola": {
        "name": "MolaMola",
        "about": "ocean sunfish: tall flat disc cut off behind, tall dorsal and anal fins far back, silver-grey",
        "back": "#6a675f", "side": "#a3a196", "belly": "#d8d6cc", "fin": "#57534c", "accent": None,
        "parts": [
            ("body", None, (0, 14, 0), [(-2, -5, -6, 4, 10, 10, "body eye")]),
            ("tail_fin", None, (0, 14, 4), [(0, -9, 0, 0, 18, 2, "fin")]),
        ],
    },
    # ---- the night job (2026-11-18, "Night job - the rest of the fish, Claude decides"): twelve more fish, placeholder
    # art only. Sizes and species are in docs/Creatures and Plants/Night log/<id>.md. Part names, for the art makers:
    # body (the trunk, head and eye), top_fin (the dorsal fin or spines), tail_fin (sways), left_fin / right_fin (the
    # pectorals, where they matter: the gurnard's blue "wings", the lionfish's fans, the anglerfish's fins) and lure
    # (the anglerfish's fishing rod). Rename or add parts freely, keeping the fish model contract.
    "kavall": {
        "name": "Kavall", "about": "chub mackerel: torpedo body, blue-green back with dark wavy bars, silver sides, forked tail",
        "back": "#2f5f6a", "side": "#a9b8b8", "belly": "#e8ece6", "fin": "#5d7a80", "accent": "#20343a",
        "parts": [
            ("body", None, (0, 21, 0), [(-1.5, -2, -8, 3, 4, 13, "body eye blotch")]),
            ("top_fin", None, (0, 19, -4), [(0, -2, 0, 0, 2, 3, "fin")]),
            ("tail_fin", None, (0, 21, 5), [(0, -2.5, 0, 0, 5, 4, "fin fork")]),
        ],
    },
    "lizz": {
        "name": "Lizz", "about": "European barracuda: long and slim, pointed jaw, grey-blue back, silver sides, forked tail",
        "back": "#4a5a66", "side": "#b4bcc0", "belly": "#e6e9e8", "fin": "#6a7880", "accent": None,
        "parts": [
            ("body", None, (0, 21.5, 0), [(-1, -1.5, -11, 2, 3, 18, "body eye"), (-0.5, -0.5, -13, 1, 1.5, 2, "body")]),
            ("top_fin", None, (0, 20, -3), [(0, -2, 0, 0, 2, 3, "fin"), (0, -2, 6, 0, 2, 2, "fin")]),
            ("tail_fin", None, (0, 21.5, 7), [(0, -2.5, 0, 0, 5, 4, "fin fork")]),
        ],
    },
    "marzpan": {
        "name": "Marzpan", "about": "Mediterranean parrotfish (female): oval, red with a yellow saddle, beak-like mouth",
        "back": "#8a3b33", "side": "#c0574a", "belly": "#d9a24e", "fin": "#a8453a", "accent": "#e0c040",
        "parts": [
            ("body", None, (0, 20.5, 0), [(-1.5, -3, -6, 3, 6, 10, "body eye accent"), (-1, -1, -7, 2, 2, 1, "body")]),
            ("top_fin", None, (0, 17.5, -4), [(0, -1, 0, 0, 1, 7, "fin")]),
            ("tail_fin", None, (0, 20.5, 4), [(0, -3, 0, 0, 6, 3, "fin")]),
        ],
    },
    "tird": {
        "name": "Tird", "about": "ornate wrasse: slim, green with blue-red bars on the head, a lyre-like tail",
        "back": "#2f7a5a", "side": "#4fa37a", "belly": "#9fd0a8", "fin": "#3a6fa0", "accent": "#3060b0",
        "parts": [
            ("body", None, (0, 21.5, 0), [(-1, -1.5, -5, 2, 3, 9, "body eye blotch")]),
            ("top_fin", None, (0, 20, -3), [(0, -1, 0, 0, 1, 6, "fin")]),
            ("tail_fin", None, (0, 21.5, 4), [(0, -1.5, 0, 0, 3, 2, "fin")]),
        ],
    },
    "trilja": {
        "name": "Trilja", "about": "striped red mullet: steep head, two chin barbels, red-pink with a yellow stripe",
        "back": "#a8453a", "side": "#d87a5c", "belly": "#f0d4b8", "fin": "#d8a070", "accent": None,
        "parts": [
            ("body", None, (0, 21.5, 0), [(-1, -1.5, -6, 2, 3, 10, "body eye"), (0, 1.5, -6, 0, 1, 1, "fin")]),
            ("top_fin", None, (0, 20, -4), [(0, -2, 0, 0, 2, 3, "fin")]),
            ("tail_fin", None, (0, 21.5, 4), [(0, -2, 0, 0, 4, 3, "fin fork")]),
        ],
    },
    "sawt": {
        "name": "Sawt", "about": "lesser weever: small, sandy, eyes on top, black venomous first dorsal fin",
        "back": "#a89a78", "side": "#c8b994", "belly": "#e8e0cc", "fin": "#2a2a2a", "accent": "#8a7a58",
        "parts": [
            ("body", None, (0, 22.5, 0), [(-1, -1.5, -4, 2, 3, 7, "body eye blotch")]),
            ("top_fin", None, (0, 21, -3), [(0, -1.5, 0, 0, 1.5, 2, "fin")]),
            ("tail_fin", None, (0, 22.5, 3), [(0, -1.5, 0, 0, 3, 2, "fin")]),
        ],
    },
    "pixxi_san_pietru": {
        "name": "PixxiSanPietru", "about": "John Dory: tall, very thin, olive-grey with a dark St Peter's thumbprint spot, "
                                          "long spiny dorsal filaments",
        "back": "#6a6a52", "side": "#a8a48a", "belly": "#d8d4c0", "fin": "#5a5a48", "accent": "#202020",
        "parts": [
            ("body", None, (0, 17, 0), [(-1, -6, -7, 2, 12, 12, "body eye blotch"), (-0.5, -1, -9, 1, 2, 2, "body")]),
            ("top_fin", None, (0, 11, -5), [(0, -3, 0, 0, 3, 9, "fin")]),
            ("tail_fin", None, (0, 17, 5), [(0, -2.5, 0, 0, 5, 3, "fin")]),
        ],
    },
    "petrica": {
        "name": "Petrica", "about": "anglerfish: huge flat head and wide mouth, mottled brown, a fishing-rod lure on the head",
        "back": "#5a4a3a", "side": "#7a6650", "belly": "#d8ccb8", "fin": "#4a3c2e", "accent": "#8c7a5c",
        "parts": [
            ("body", None, (0, 22, 0), [(-5, -2, -10, 10, 4, 10, "body eye blotch"), (-4, 0, -11, 8, 2, 1, "body"),
                                        (-1.5, -1.5, 0, 3, 3, 8, "body blotch")]),
            ("lure", None, (0, 20, -9), [(0, -3, 0, 0, 3, 1, "fin")]),
            ("left_fin", None, (5, 23, -4), [(0, 0, 0, 3, 0, 3, "fin")]),
            ("right_fin", None, (-5, 23, -4), [(-3, 0, 0, 3, 0, 3, "fin")]),
            ("tail_fin", None, (0, 22, 8), [(0, -2, 0, 0, 4, 3, "fin")]),
        ],
    },
    "lingwata": {
        "name": "Lingwata", "about": "common sole: flat oval lying on its side, both eyes on top, brown above, white below",
        "back": "#6a5a44", "side": "#7f6c52", "belly": "#ece6da", "fin": "#5a4c3a", "accent": None,
        "parts": [
            ("body", None, (0, 23.25, 0), [(-4, -0.75, -8, 8, 1.5, 14, "body eye"), (-2.5, -0.75, -9, 5, 1.5, 1, "body")]),
            ("tail_fin", None, (0, 23.25, 6), [(-2.5, 0, 0, 5, 0, 3, "fin")]),
        ],
    },
    "hmar": {
        "name": "Hmar", "about": "grey triggerfish: deep, flat-sided, grey-brown, small mouth, a trigger spine on the back",
        "back": "#5c5a52", "side": "#8a877a", "belly": "#b8b4a4", "fin": "#6a675c", "accent": "#3a5a8a",
        "parts": [
            ("body", None, (0, 19, 0), [(-1.5, -5, -6, 3, 10, 11, "body eye blotch"), (-1, -1, -8, 2, 3, 2, "body")]),
            ("top_fin", None, (0, 14, -4), [(0, -3, 0, 0, 3, 2, "fin"), (0, -2, 3, 0, 2, 5, "fin")]),
            ("tail_fin", None, (0, 19, 5), [(0, -3, 0, 0, 6, 3, "fin")]),
        ],
    },
    "gallinella": {
        "name": "Gallinella", "about": "tub gurnard: big bony head, red body, huge blue-edged pectoral 'wings', walks on "
                                      "its fin rays",
        "back": "#a84a3a", "side": "#cc6e52", "belly": "#ecd2c0", "fin": "#4a7ac8", "accent": None,
        "parts": [
            ("body", None, (0, 21.5, 0), [(-2, -2, -9, 4, 3.5, 4, "body eye"), (-1.5, -1.5, -5, 3, 3, 11, "body")]),
            ("top_fin", None, (0, 20, -5), [(0, -2, 0, 0, 2, 6, "fin")]),
            ("left_fin", None, (2, 22.5, -5), [(0, 0, 0, 5, 0, 5, "fin")]),
            ("right_fin", None, (-2, 22.5, -5), [(-5, 0, 0, 5, 0, 5, "fin")]),
            ("tail_fin", None, (0, 21.5, 6), [(0, -2, 0, 0, 4, 3, "fin")]),
        ],
    },
    "lionfish": {
        "name": "Lionfish", "about": "lionfish: red-brown and white bands, tall venomous dorsal spines, big fan pectoral fins",
        "back": "#7a2a20", "side": "#c8705a", "belly": "#f0e0d0", "fin": "#d8a090", "accent": "#f4ece0",
        "parts": [
            ("body", None, (0, 20.5, 0), [(-1.5, -2.5, -6, 3, 5, 11, "body eye blotch"), (-1, -1, -7, 2, 2, 1, "body")]),
            ("top_fin", None, (0, 18, -5), [(0, -5, 0, 0, 5, 9, "fin")]),
            ("left_fin", None, (1.5, 21, -3), [(0, 0, 0, 4, 0, 6, "fin")]),
            ("right_fin", None, (-1.5, 21, -3), [(-4, 0, 0, 4, 0, 6, "fin")]),
            ("tail_fin", None, (0, 20.5, 5), [(0, -2.5, 0, 0, 5, 3, "fin")]),
        ],
    },
}

# the night job's fish: their spawn eggs sit on vanilla's own pool, like the other new eggs (owner 2026-11-18)
NIGHT_FISH = ("kavall", "lizz", "marzpan", "tird", "trilja", "sawt", "pixxi_san_pietru", "petrica", "lingwata", "hmar",
              "gallinella", "lionfish")


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def shade(c, f):
    return tuple(max(0, min(255, round(v * f))) for v in c)


def box_uv_size(w, h, d):
    w, h, d = math.ceil(w), math.ceil(h), math.ceil(d)
    return 2 * (d + w), d + h


def pack(boxes):
    """Shelf-packs the boxes' UV areas into a TEX x TEX sheet; returns texOffs per box."""
    out, x, y, row = [], 0, 0, 0
    for b in boxes:
        bw, bh = box_uv_size(*b[3:6])
        bw, bh = max(bw, 1), max(bh, 1)
        if x + bw > TEX:
            x, y, row = 0, y + row, 0
        out.append((x, y))
        x += bw
        row = max(row, bh)
    assert y + row <= TEX, "texture too small"
    return out


def paint_box(img, fish, uv, b):
    x0, y0, z0, w, h, d, kind = b
    w, h, d = math.ceil(w), math.ceil(h), math.ceil(d)
    u, v = uv
    px = img.load()
    back, side, belly, fin = rgb(fish["back"]), rgb(fish["side"]), rgb(fish["belly"]), rgb(fish["fin"])
    accent = rgb(fish["accent"]) if fish["accent"] else side

    def fill(x, y, fw, fh, colour_at):
        for i in range(fw):
            for j in range(fh):
                if 0 <= u + x + i < TEX and 0 <= v + y + j < TEX:
                    px[u + x + i, v + y + j] = colour_at(i, j, fw, fh) + (255,)

    if "fin" in kind:
        def fin_colour(i, j, fw, fh):
            if "fork" in kind and fh >= 6 and fh // 3 <= j < fh - fh // 3 and i >= fw - max(1, fw // 2):
                return None
            return shade(fin, 1.0 - 0.15 * (j / max(1, fh - 1)))
        for (fx, fy, fw, fh) in ((d, 0, w, d), (d + w, 0, w, d), (0, d, d, h), (d, d, w, h), (d + w, d, d, h), (2 * d + w, d, w, h)):
            for i in range(fw):
                for j in range(fh):
                    c = fin_colour(i, j, fw, fh)
                    if c is not None and 0 <= u + fx + i < TEX and 0 <= v + fy + j < TEX:
                        px[u + fx + i, v + fy + j] = c + (255,)
        return

    def side_colour(i, j, fw, fh):
        t = j / max(1, fh - 1)
        c = back if t < 0.34 else (side if t < 0.75 else belly)
        if "blotch" in kind and (i * 7 + j * 5) % 11 == 0:
            c = accent
        return shade(c, 1.0 - 0.06 * (i % 2 == j % 2))

    fill(d, 0, w, d, lambda i, j, fw, fh: shade(back, 0.85))      # top
    fill(d + w, 0, w, d, lambda i, j, fw, fh: belly)               # bottom
    fill(0, d, d, h, side_colour)                                  # right side (x-)
    fill(d, d, w, h, lambda i, j, fw, fh: shade(side_colour(i, j, fw, fh), 0.9))   # front (-z): the face
    fill(d + w, d, d, h, side_colour)                              # left side (x+)
    fill(2 * d + w, d, w, h, lambda i, j, fw, fh: shade(side, 0.8))  # back (+z)
    if "accent" in kind and fish["accent"]:
        for i in range(max(1, d // 6)):                             # a band just behind the face
            for j in range(h // 2):
                for sx in (d - 2 - i, d + w + 1 + i):
                    if 0 <= sx - 0 < 2 * d + 2 * w:
                        px[u + sx, v + d + j] = accent + (255,)
    if "eye" in kind:
        # near the front, a little above the middle, on both sides: the right side's front is its right end (u+d-1),
        # the left side's front is its left end (u+d+w)
        ey = v + d + max(0, h // 3 - (1 if h > 4 else 0))
        ex = min(1, d - 1)
        for x in (u + d - 1 - ex, u + d + w + ex):
            px[x, ey] = (16, 16, 16, 255)


def java_model(fid, fish, uvs):
    name = fish["name"]
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
        f" * PLACEHOLDER model of the {fid} ({fish['about']}): plain boxes until the art round.",
        " * Made by art/src/fish_placeholders.py; the art makers replace this file, keeping the fish model contract",
        " * (docs/Tools and Process/Art pipeline.md, \"Fish models\"). Texture: textures/entity/fish/" + fid + ".png.",
    ] + ([f" * Extends {fish['base']}, which animates it; keep its part names: "
          + ", ".join(p[0] for p in fish["parts"]) + "."] if fish.get("base")
       else [" * Parts, for the art makers to replace: " + ", ".join(p[0] for p in fish["parts"]) + "."]
       if fid in NIGHT_FISH else []) + [
        " */",
        f"public class {name}Model extends {fish.get('base', 'FishModel')} {{",
        f"    public {name}Model(ModelPart root) {{",
        "        super(root);",
        "    }",
        "",
        "    public static LayerDefinition createBodyLayer() {",
        "        MeshDefinition mesh = new MeshDefinition();",
        "        PartDefinition root = mesh.getRoot();",
    ]
    k = 0
    for pname, parent, pivot, boxes in fish["parts"]:
        cubes = []
        for b in boxes:
            u, v = uvs[k]
            k += 1
            cubes.append(f".texOffs({u}, {v}).addBox({f(b[0])}, {f(b[1])}, {f(b[2])}, {f(b[3])}, {f(b[4])}, {f(b[5])})")
        var = "PartDefinition " + pname.replace("_", "") + " = " if any(p[1] == pname for p in fish["parts"]) else ""
        owner = (parent.replace("_", "") if parent else "root")
        lines.append(f"        {var}{owner}.addOrReplaceChild(\"{pname}\", CubeListBuilder.create()"
                     + "".join("\n            " + c for c in cubes)
                     + f",\n            PartPose.offset({f(pivot[0])}, {f(pivot[1])}, {f(pivot[2])}));")
    lines += [f"        return LayerDefinition.create(mesh, {TEX}, {TEX});", "    }", "}", ""]
    return "\n".join(lines)


def f(x):
    return f"{float(x)}F"


# ---- icons (16 x 16) ----

def icon_ray(fish):
    """A ray seen from above: the rhombic disc at the bottom left, the whip tail running to the top right."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    back, side, fin = rgb(fish["back"]), rgb(fish["side"]), rgb(fish["fin"])
    cx, cy = 6.0, 10.0
    for x in range(16):
        for y in range(16):
            # the disc's long axis runs along the tail's line (to the top right), so rotate 45 degrees
            u, v = ((x + 0.5 - cx) + (y + 0.5 - cy)) / 1.414, ((x + 0.5 - cx) - (y + 0.5 - cy)) / 1.414
            if abs(u) / 5.6 + abs(v) / 5.0 <= 1.0:
                px[x, y] = (side if abs(u) / 5.6 + abs(v) / 5.0 > 0.6 else back) + (255,)
    outline(img)
    for i in range(6):                              # the tail, then the spine near its end
        px[10 + i, 5 - i] = fin + (255,)
    px[13, 1] = shade(fin, 0.6) + (255,)
    px[5, 9], px[7, 9] = (16, 16, 16, 255), (16, 16, 16, 255)
    return img


def icon_mola(fish):
    """The sunfish placeholder: a round grey disc with a fin above and below at the back, an eye at the front."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for x in range(16):
        for y in range(16):
            nx, ny = (x + 0.5 - 7.0) / 5.0, (y + 0.5 - 8.0) / 4.6
            if nx * nx + ny * ny <= 1:
                px[x, y] = rgb(fish["back"] if ny < -0.45 else (fish["belly"] if ny > 0.45 else fish["side"])) + (255,)
    for (x, y) in ((9, 1), (10, 1), (9, 2), (10, 2), (11, 2), (9, 3), (10, 3), (11, 3),
                   (9, 12), (10, 12), (11, 12), (9, 13), (10, 13), (11, 13), (9, 14), (10, 14)):
        px[x, y] = rgb(fish["fin"]) + (255,)
    for y in range(5, 11):
        px[12, y] = rgb(fish["fin"]) + (255,)
    outline(img)
    px[4, 6] = (16, 16, 16, 255)
    return img


def icon_fish(fish, fid):
    """The caught fish in vanilla's pose: head bottom left, tail top right."""
    if fid == "boll":
        return icon_ray(fish)
    if fid == "mola_mola":
        return icon_mola(fish)
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    thick = {"sardina": 1.6, "incova": 1.3, "cawl": 3.0, "awrata": 3.2, "cerna": 3.4, "tonn": 3.6, "lampuka": 2.6, "murina": 1.4,
             "kavall": 2.4, "lizz": 1.6, "marzpan": 3.0, "tird": 1.9, "trilja": 2.2, "sawt": 1.8,
             "pixxi_san_pietru": 4.2, "petrica": 3.6, "lingwata": 3.0, "hmar": 3.8, "gallinella": 2.6, "lionfish": 2.8}.get(fid, 2.5)
    a, b = (2.5, 13.5), (11.5, 4.5)
    if fid == "murina":
        a, b = (1.5, 14.5), (13.5, 2.5)
    back, side, belly = rgb(fish["back"]), rgb(fish["side"]), rgb(fish["belly"])
    if fid == "pixxispad":                           # a shorter body, leaving room for the sword
        a = (5.5, 10.5)
    for x in range(16):
        for y in range(16):
            cx, cy = x + 0.5, y + 0.5
            dx, dy = b[0] - a[0], b[1] - a[1]
            t = max(0.0, min(1.0, ((cx - a[0]) * dx + (cy - a[1]) * dy) / (dx * dx + dy * dy)))
            qx, qy = a[0] + t * dx, a[1] + t * dy
            dist = math.hypot(cx - qx, cy - qy)
            r = thick * (0.55 + 0.45 * math.sin(math.pi * min(1.0, t * 1.1 + 0.08)))
            if dist <= r:
                above = (cx - qx) - (cy - qy) < 0   # toward the top left = the back
                px[x, y] = (back if above and dist > r * 0.35 else (belly if not above and dist > r * 0.55 else side)) + (255,)
    # tail fin at the top right
    for (x, y) in ((12, 2), (13, 2), (13, 3), (14, 4), (12, 3), (13, 4), (14, 3), (11, 2), (14, 5)):
        if fid != "murina":
            px[x, y] = rgb(fish["fin"]) + (255,)
    outline(img)
    ex, ey = (3, 11) if fid != "murina" else (2, 12)
    if fid == "pixxispad":
        ex, ey = (6, 9)
        for i in range(5):                          # the sword, down to the bottom left corner
            px[4 - i, 11 + i] = rgb(fish["fin"]) + (255,)
    px[ex, ey] = (16, 16, 16, 255)
    return img


def outline(img):
    px = img.load()
    w, h = img.size
    solid = {(x, y) for x in range(w) for y in range(h) if px[x, y][3]}
    for (x, y) in solid:
        if any((x + dx, y + dy) not in solid for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            px[x, y] = shade(px[x, y][:3], 0.6) + (255,)


def icon_bucket(fish):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    metal, dark, light = (150, 150, 150), (70, 70, 70), (205, 205, 205)
    for y in range(5, 15):
        half = 6 - (y - 5) * 2 // 9
        for x in range(8 - half, 8 + half):
            c = light if x == 8 - half + 1 else metal
            if x in (8 - half, 8 + half - 1) or y == 14:
                c = dark
            px[x, y] = c + (255,)
    for x in range(2, 14):                       # the rim, with water inside
        px[x, 4] = dark + (255,)
        px[x, 5] = ((63, 118, 228) if 3 <= x <= 12 else dark) + (255,)
    for (x, y) in ((6, 5), (7, 5), (8, 5), (9, 4), (5, 4)):   # the fish in the water
        px[x, y] = rgb(fish["side"]) + (255,)
    px[9, 5] = rgb(fish["back"]) + (255,)
    for x in range(3, 13):                       # the handle
        y = 1 + round(abs(x - 7.5) ** 2 / 9)
        if y < 4:
            px[x, y] = dark + (255,)
    return img


def icon_egg(fish):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    base, spot = rgb(fish["side"]), rgb(fish["back"])
    for x in range(16):
        for y in range(16):
            nx, ny = (x + 0.5 - 8) / 5.2, (y + 0.5 - 8.8) / 6.6
            if ny < 0:
                nx *= 1.12
            if nx * nx + ny * ny <= 1:
                px[x, y] = (spot if (x * 3 + y * 5) % 7 == 0 else base) + (255,)
    outline(img)
    return img


def fresh(path):
    """True if the file doesn't exist yet; an existing file (drawn art) is kept and reported."""
    if os.path.exists(path):
        print("  kept", os.path.relpath(path, ROOT))
        return False
    return True


def main(ids):
    unknown = [i for i in ids if i not in FISH]
    if not ids or unknown:
        sys.exit("name the fish to make: " + " ".join(FISH) + ("" if not unknown else "  (unknown: " + " ".join(unknown) + ")"))
    os.makedirs(JAVA, exist_ok=True)
    for sub in ("textures/entity/fish", "textures/item"):
        os.makedirs(os.path.join(RES, sub), exist_ok=True)
    for fid in ids:
        fish = FISH[fid]
        boxes = [b for _, _, _, bs in fish["parts"] for b in bs]
        uvs = pack(boxes)
        img = Image.new("RGBA", (TEX, TEX), (0, 0, 0, 0))
        for uv, b in zip(uvs, boxes):
            paint_box(img, fish, uv, b)
        # the model and its texture go together: the texture's layout only fits this model
        tex = os.path.join(RES, "textures/entity/fish", fid + ".png")
        path = os.path.join(JAVA, fish["name"] + "Model.java")
        if fresh(tex) and fresh(path):
            img.save(tex)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(java_model(fid, fish, uvs))
        for kind, make in (("_bucket", icon_bucket), ("_spawn_egg", icon_egg)):
            if kind == "_bucket" and fid == "mola_mola":
                continue    # no mola bucket: it can't be caught (owner 2026-11-19)
            out = os.path.join(RES, "textures/item", fid + kind + ".png")
            if fresh(out):
                icon = make(fish)
                if kind == "_spawn_egg" and (fid == "mola_mola" or fid in NIGHT_FISH):
                    icon = vanilla_pool(icon, [])     # vanilla's own pool under the egg (owner 2026-11-18)
                icon.save(out)
        out = os.path.join(RES, "textures/item", fid + ".png")
        if fid not in ("lampuka", "ziemel") and fresh(out):     # the żiemel has no item
            icon_fish(fish, fid).save(out)
        print("done", fid)


if __name__ == "__main__":
    main(sys.argv[1:])
