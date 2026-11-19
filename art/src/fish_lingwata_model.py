"""The lingwata (common sole, Solea solea) as a swimming mob: its 3D model and its texture.

Drawn from the reference photos in art/references/fish_lingwata_refonly/ (list.tsv): solea and solea1 (landed soles
on black, eyed side, for the outline and the true colour out of water), ifremer (out of water), brest1 and brest3
(on the sand in water: the eyes, the fringe fins and the raised pectoral fin with its black tip), blind (the white
blind side), caudal (the small rounded tail), plate1 (an 1890s plate seen from above). What makes it a sole, and
not the boll (a ray) or the petrica (an anglerfish):
  - an oval, tongue-shaped body, about two and a half times as long as wide, with a blunt rounded head and a slow
    taper back to a small rounded tail; no wings, no whip tail, no big head;
  - very thin: a 1 px fringe plate all round and a 2 px body inside it (the fringe of the dorsal and anal fins runs
    all round the edge, from the snout to the tail), with 1 px raised eyes on top (3 px at the eyes);
  - both eyes on the upper side near the front, close together and one behind the other on a slant, off the middle
    toward one edge (as on the real fish), so they never sit side by side like a face; each a near-black pupil on a
    1 px bump with a pale ring round it; nothing else on top is that dark or ringed;
  - the fringe a little lighter and warmer than the body, with faint fin rays (one soft step, never a row of dots);
  - the small pectoral fin on the eyed side, behind the head on the other side of the middle from the eyes, raised a
    little, with the black spot at its tip that marks Solea solea;
  - sandy brown with soft darker mottles (2-3 px blotches, one or two steps darker, none on the head by the eyes),
    shaded from the lit middle to darker edges and tail; a white blind side underneath (dark back, pale belly).
The palette is a step lighter than the photos (x1.15 brightness, hue kept: water greys everything).

Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): a plain FishModel, head toward -z, y 24 at
the ground; root children "body" (the plate, the body, the eyes, and the child "pectoral_fin") and "tail_fin" (the
rounded tail, which sways). The renderer gives it no body wiggle and lays it flat on land (MimContentClient, liesFlat).

Writes (byte-identical on every run):
  mod/src/main/java/com/maltaminecraft/mimcontent/client/fish/LingwataModel.java
  mod/src/main/resources/assets/mimcontent/textures/entity/fish/lingwata.png   (128 x 128)
With --candidate X it installs candidate X instead of the chosen one. With --sheet [SCREENSHOT_DIR] it writes the
review sheet art/candidates/fish_lingwata_model.png (all candidates offline, and the in-game shots if given).

Run:  art/.venv/bin/python art/src/fish_lingwata_model.py [--candidate A|B|C] [--sheet [SCREENSHOT_DIR]]
"""
import colorsys
import glob
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import fish_awrata_model as AW  # noqa: E402  (the shared texel walker, model reader and rotation)

RES = os.path.join(ROOT, "mod", "src", "main", "resources", "assets", "mimcontent")
JAVA_DIR = os.path.join(ROOT, "mod", "src", "main", "java", "com", "maltaminecraft", "mimcontent", "client", "fish")
JAVA = os.path.join(JAVA_DIR, "LingwataModel.java")
TEXTURE = os.path.join(RES, "textures", "entity", "fish", "lingwata.png")
TW, TH = 128, 128
CHOSEN = "K"


def hexc(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16), 255)


def lift(c, v=1.15):
    h, s, val = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, min(1.0, val * v))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), 255)


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3)) + (255,)


# The out-of-water colours, measured from solea1 and solea (#9a8070 #8a7160 #6e5b4e #4b3832 on the eyed side, a
# little warmer and sandier here) and the blind side (#ece6da). The browns are lifted x1.15 for the water; the
# creams, the pupils and the fin spot are not.
BASES = {
    # A: sandy brown (the solea1 fish, pushed a little toward sand)
    "A": {"L": "#a58d72", "1": "#927b63", "2": "#806a55", "3": "#6c5847", "4": "#544337",
          "F": "#a89076", "f": "#9a8268", "r": "#715d4b", "P": "#b09a7e"},
    # B: greyer brown, nearer the photos' grey-brown
    # D: sandier and yellower (critic round 1: the old A greyed to a pinkish grey under water), mottles #6b5544
    "D": {"L": "#b29a72", "1": "#a08862", "2": "#8c7554", "3": "#6b5544", "4": "#574535",
          "F": "#af9c81", "f": "#988468", "r": "#7d6849", "P": "#bca986"},
    # F: D's sand, the fringe a little greyer and darker than the body with darker ray ticks (critic round 3)
    "F": {"L": "#b29a72", "1": "#a08862", "2": "#8c7554", "3": "#6b5544", "4": "#574535",
          "F": "#8f8068", "f": "#76684f", "r": "#7d6849", "P": "#bca986"},
    # G: F's sand, the fringe about 15 % lighter than the body with darker ray ticks every 2 px (critic round 4)
    "G": {"L": "#b29a72", "1": "#a08862", "2": "#8c7554", "3": "#6b5544", "4": "#574535",
          "F": "#b8a07a", "f": "#94805f", "r": "#7d6849", "P": "#9c8562"},
    # H: G's sand; the fringe one step darker than the body with soft lighter ray ticks; mottles #7a5f45 on the
    # #a88a6a base before the lift (critic round 5)
    "H": {"L": "#b29a72", "1": "#a88a6a", "2": "#94785a", "3": "#7a5f45", "4": "#5f4a37",
          "F": "#94785a", "f": "#a08566", "r": "#7d6849", "P": "#8a7052"},
    "B": {"L": "#9c8c7e", "1": "#8a7a6c", "2": "#79695c", "3": "#66574c", "4": "#4e423a",
          "F": "#a09083", "f": "#928174", "r": "#6b5c51", "P": "#aa9b8e"},
}
FIXED = {"R": "#d8c8a8", "W": "#ece6da", "w": "#d9d0c0", "s": "#bdb3a1", "e": "#1e1a18", "H": "#c2ad86", "k": "#3a2e26",
         "G": "#d8c89a"}


def palette(base):
    pal = {k: lift(hexc(v)) for k, v in BASES[base].items()}
    pal.update({k: hexc(v) for k, v in FIXED.items()})
    pal["m"] = mix(pal["1"], pal["2"], 0.5)
    pal["n"] = mix(pal["2"], pal["3"], 0.5)
    pal["o"] = mix(pal["3"], pal["4"], 0.5)
    pal["h"] = mix(pal["L"], pal["1"], 0.5)
    pal["."] = (0, 0, 0, 0)
    return pal


BODY_RAMP = ["L", "h", "1", "m", "2", "n", "3", "o", "4"]
FIN_RAMP = ["P", "F", "f", "r", "3"]

# --- the shapes ------------------------------------------------------------------------------------------------------
# Columns are texel x indices: column i covers x i..i+1 (i from -half to half-1). OUTLINE[i] = (front z, back z) of
# the 1 px plate (the fringe included); the body (2 px) is the plate eroded by 1 px; TAIL[i] the rounded tail fin.
# EYES are texel (x, z) on the body's top; PEC the pectoral fin's base (x0, z) and size (w, d).
GEOM = {
    # 20 px long (1.25 blocks) with the tail, 8 wide (0.5 block)
    "A": {"half": 4,
          "outline": {0: (-10, 7), 1: (-10, 6), 2: (-9, 4), 3: (-8, 1)},
          "tail": {0: (7, 10), 1: (7, 9)}, "tail_z": 7,
          "eyes": [(0, -8), (1, -6)], "pec": (-3, -4, 2, 2)},
    # 22 px long (1.38 blocks), 10 wide: a bigger sole
    "C": {"half": 5,
          "outline": {0: (-11, 8), 1: (-11, 7), 2: (-10, 6), 3: (-9, 4), 4: (-8, 1)},
          "tail": {0: (8, 11), 1: (8, 10)}, "tail_z": 8,
          "eyes": [(0, -9), (1, -7)], "pec": (-4, -5, 2, 2)},
    # critic round 1: 19 px long (about 15 % smaller), 8 wide; the tail joint as wide as the body minus 2 px, the
    # fringe running on into it, its back edge rounded; a 1 px hump over the middle third; low eyes, the upper eye
    # (toward the dorsal edge) 1 px further forward; the pectoral 2 px further back
    # critic round 2: a tongue from above, not a brick: a blunt nose 4 px wide, the widest point about 40 % back,
    # tapering in 1-2 px steps both ways; a small 4 x 3 rounded tail running on from the fringe; the eyes in the
    # front quarter, off the middle; a 3 x 2 pale pectoral round its spot
    "D": {"half": 5,
          "outline": {0: (-10, 6), 1: (-10, 6), 2: (-9, 5), 3: (-8, 3), 4: (-6, 0)},
          "tail": {0: (6, 9), 1: (6, 8)}, "tail_z": 6,
          "hump": {0: (-3, 2), 1: (-2, 1)},
          "eyes": [(1, -8), (2, -6)], "pec": (-4, -3, 3, 2)},
    # critic round 3: a longer tongue, about 2.3 : 1 without the fins (6 px body, 15 long), widest a third back,
    # tapering evenly into a small rounded tail with no neck; flush eyes one behind the other, off the middle; the
    # pectoral spot 5 px behind the eyes, at the other edge
    "F": {"half": 4,
          "outline": {0: (-10, 7), 1: (-10, 6), 2: (-9, 4), 3: (-7, 1)},
          "tail": {0: (7, 10), 1: (6, 9)}, "tail_z": 6.5,
          "hump": {0: (-4, 2), 1: (-3, 1)},
          "eyes": [(1, -8), (1, -6)], "flush_eyes": True, "pec": (-3, -2, 2, 2)},
    # critic round 4: wider again (10 px with the fringe) and longer (23 px), a blunt half-round head, an even taper
    # with no waist into a small round tail sitting right on the oval; one even 2 px slab (no hump); the pectoral
    # spot further back and out toward the edge
    "G": {"half": 5,
          "outline": {0: (-12, 9), 1: (-12, 8), 2: (-11, 7), 3: (-10, 5), 4: (-8, 2)},
          "tail": {0: (9, 11), 1: (8, 10)}, "tail_z": 8.5,
          "eyes": [(1, -9), (2, -7)], "flush_eyes": True, "pec": (-4, -2, 2, 2), "spot_out": True},
    # critic round 5: G's shape with the eyes on a slant (the upper eye, nearer the edge, 1 px further forward), a
    # 1 px hook at the snout to break the symmetry, and the pectoral fin 2-3 px behind the eyes, a 2 x 3 fin, dark
    # brown with a black tip, never a round dot
    "H": {"half": 5,
          "outline": {0: (-12, 9), 1: (-12, 8), 2: (-11, 7), 3: (-10, 5), 4: (-8, 2)},
          "extra_plate": [(-2, -13)],
          "tail": {0: (9, 11), 1: (8, 10)}, "tail_z": 8.5,
          "eyes": [(2, -9), (1, -7)], "flush_eyes": True, "pec": (-2, -5, 2, 3), "spot_out": True,
          "fin_tip": True, "big_mottles": True, "ring": "R"},
    # critic round 6: H's slant eyes and snout hook, a smoother oval rear and a small separate tail fan (darker, pale
    # edge); a 2 px edge (the 1 px fringe, then 1 px of plate in the body's darker tone) round a body that rises
    # gently to the middle; fine 1-2 px speckles, none within 3 px of the eyes; the pectoral 4 px behind the eyes,
    # in the body's tone with only its tip dark
    "I": {"half": 5,
          "outline": {0: (-12, 8), 1: (-12, 8), 2: (-11, 7), 3: (-10, 5), 4: (-8, 3)},
          "extra_plate": [(-2, -13)],
          "tail": {0: (8, 11), 1: (8, 10)}, "tail_z": 8,
          "eyes": [(2, -9), (1, -7)], "flush_eyes": True, "pec": (-2, -4, 2, 3), "spot_out": True,
          "fin_tip": True, "plain_fin": True, "ring": "R", "inset": 2, "clear": 3},
    # gave up after 8 rounds: the installed pick is round 5's G (the critic: "the oval tongue shape is right"),
    # with round 7's pectoral (the body's tone, one dark brown texel at its tip), since round 5's only rule problem
    # was a black spot that looked like a third eye
    "K": {"half": 5,
          "outline": {0: (-12, 9), 1: (-12, 8), 2: (-11, 7), 3: (-10, 5), 4: (-8, 2)},
          "tail": {0: (9, 11), 1: (8, 10)}, "tail_z": 8.5,
          "eyes": [(1, -9), (2, -7)], "flush_eyes": True, "pec": (-4, -2, 2, 2), "spot_out": True,
          "soft_spot": True},
    # critic round 7: I with the widest point in the front third, a smooth round snout (no hook), a flared tail fan
    # (6 px across behind a 4 px stalk, straight back edge) in the body's sand with darker ray stripes, darker 2 x 2
    # and 2 x 3 mottles that survive the water, and the pectoral just behind the eyes on the other side
    "J": {"half": 5,
          "outline": {0: (-12, 8), 1: (-12, 8), 2: (-11, 6), 3: (-10, 4), 4: (-9, 1)},
          "tail": {0: (8, 11), 1: (8, 11), 2: (9, 11)}, "tail_z": 8, "fan": True,
          "eyes": [(2, -9), (1, -7)], "flush_eyes": True, "pec": (-2, -6, 2, 3), "spot_out": True,
          "fin_tip": True, "plain_fin": True, "ring": "R", "inset": 2, "clear": 3, "big_mottles": True,
          "mottle": "3", "mottle_count": 7},
}
CANDIDATES = {"K": ("K", "G"), "G": ("G", "G"), "I": ("I", "G"), "J": ("J", "G")}   # candidate -> (shape, paint)


class Fish:
    def __init__(self, cand):
        self.cand = cand
        g = GEOM[CANDIDATES[cand][0]]
        self.pal = palette(CANDIDATES[cand][1])
        self.half = g["half"]
        self.tail_z = g["tail_z"]
        self.eyes = g["eyes"]
        self.pec = g["pec"]
        self.flush_eyes = g.get("flush_eyes", False)
        self.spot_out = g.get("spot_out", False)
        self.fin_tip = g.get("fin_tip", False)
        self.big_mottles = g.get("big_mottles", False)
        self.ring = g.get("ring", None)
        self.hump = set()
        for c, (z0, z1) in g.get("hump", {}).items():
            for xi in (c, -c - 1):
                for z in range(z0, z1):
                    self.hump.add((xi, z))
        self.plate = set()
        for c, (z0, z1) in g["outline"].items():
            for xi in (c, -c - 1):
                for z in range(z0, z1):
                    self.plate.add((xi, z))
        for q in g.get("extra_plate", []):
            self.plate.add(q)                     # the snout's little hook (round 5), on the plate only
        self.body = {(x, z) for (x, z) in self.plate
                     if all(n in self.plate for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)))}
        self.fringe = self.plate - self.body          # the 1 px fin all round
        self.shoulder = set()
        for _ in range(g.get("inset", 1) - 1):
            inner = {(x, z) for (x, z) in self.body
                     if all(n in self.body for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)))}
            self.shoulder |= self.body - inner        # plate in the body's tone, a step lower than the body
            self.body = inner
        self.clear = g.get("clear", 1)
        self.plain_fin = g.get("plain_fin", False)
        self.fan = g.get("fan", False)
        self.soft_spot = g.get("soft_spot", False)
        self.mottle = g.get("mottle", "3")
        self.mottle_count = g.get("mottle_count", 9)
        self.tail = set()
        for c, (z0, z1) in g["tail"].items():
            for xi in (c, -c - 1):
                for z in range(z0, z1):
                    self.tail.add((xi, z))
        zs = [z for _, z in self.plate]
        self.snout, self.rear = min(zs), max(zs) + 1
        self.tail_end = max(z for _, z in self.tail) + 1
        self.blotch = self.make_blotches()

    # the mottles: irregular 2-3 px blotches (critic round 1: not a grid, not stripes), from scattered seeds, each a
    # small shape; none on the head by the eyes
    SHAPES = [((0, 0), (1, 0), (0, 1)), ((0, 0), (0, 1), (1, 1)), ((0, 0), (1, 0)), ((0, 0), (0, 1), (0, 2)),
              ((0, 0), (1, 1), (1, 0)), ((0, 0), (1, 0), (1, 1), (0, 1))]

    SMALL = [((0, 0),), ((0, 0), (1, 0)), ((0, 0), (0, 1)), ((0, 0), (1, 1))]

    def make_blotches(self):
        out = {}
        if self.big_mottles:
            # critic round 5: 6-10 blotches of 2 x 2 to 3 x 2 px, about 20 % darker, that survive the water
            r = self.clear
            keep_clear = {(ex + dx, ez + dz) for ex, ez in self.eyes for dx in range(-r, r + 1) for dz in range(-r, r + 1)}
            px, pz, pw, pd = self.pec
            keep_clear |= {(px + dx, pz + dz) for dx in range(-1, pw + 1) for dz in range(-1, pd + 1)}
            shapes = [((0, 0), (1, 0), (0, 1), (1, 1)), ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1)),
                      ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2)), ((0, 0), (1, 0), (1, 1), (2, 1))]
            if self.fan:
                shapes = [((0, 0), (1, 0), (0, 1), (1, 1)), ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2))]
            area = self.body | self.shoulder
            seeds = 0
            for (x, z) in sorted(area if self.fan else self.body, key=lambda q: (AW.hash01(q[0], q[1], 71), q)):
                if seeds >= self.mottle_count:
                    break
                shape = shapes[int(AW.hash01(x, z, 73) * len(shapes))]
                cells = [(x + dx, z + dz) for dx, dz in shape]
                if any(c not in (area if self.fan else self.body) or c in keep_clear or c in out for c in cells):
                    continue
                if any((c[0] + a, c[1] + b) in out for c in cells for a in (-1, 0, 1) for b in (-1, 0, 1)):
                    continue                      # blotches apart, so they stay 2-3 px shapes
                for c in cells:
                    out[c] = 3
                seeds += 1
            return out
        if self.flush_eyes:
            # critic round 3: small 1-2 px spots scattered over the sand, not big blocks
            r = self.clear
            keep_clear = {(ex + dx, ez + dz) for ex, ez in self.eyes for dx in range(-r, r + 1) for dz in range(-r, r + 1)}
            for (x, z) in sorted(self.body | self.shoulder):
                if AW.hash01(x, z, 53) > 0.2:
                    continue
                shape = self.SMALL[int(AW.hash01(x, z, 59) * len(self.SMALL))]
                for dx, dz in shape:
                    q = (x + dx, z + dz)
                    if q in (self.body | self.shoulder) and q not in keep_clear:
                        out[q] = 1 if self.plain_fin else 2
            return out
        keep_clear = {(ex + dx, ez + dz) for ex, ez in self.eyes for dx in (-1, 0, 1) for dz in (-2, -1, 0, 1, 2)}
        for (x, z) in sorted(self.body):
            if AW.hash01(x, z, 31) > 0.16:
                continue
            shape = self.SHAPES[int(AW.hash01(x, z, 37) * len(self.SHAPES))]
            deep = 2 if AW.hash01(x, z, 41) < 0.4 else 1
            for dx, dz in shape:
                q = (x + dx, z + dz)
                if q in self.body and q not in keep_clear and q[1] >= self.eyes[0][1]:
                    out[q] = max(out.get(q, 0), deep)
        return out

    # --- cubes: (name, kind, part, abs origin, size)
    def cubes(self):
        out = []
        for layer, mask, y0 in ((1, self.plate, 23), (2, self.body, 22), (3, self.hump, 21)):
            for xi in range(-self.half, self.half):
                zs = sorted(z for x, z in mask if x == xi)
                runs = []
                for z in zs:
                    if runs and runs[-1][1] == z:
                        runs[-1][1] = z + 1
                    else:
                        runs.append([z, z + 1])
                for k, (z0, z1) in enumerate(runs):
                    out.append(("c%d_x%d_%d" % (layer, xi, k), "plate" if layer == 1 else "body", "body",
                                (xi, y0, z0), (1, 1, z1 - z0)))
        for xi in range(-self.half, self.half):
            zs = sorted(z for x, z in self.tail if x == xi)
            if zs:
                out.append(("tail_x%d" % xi, "tail", "tail_fin", (xi, 23, zs[0]), (1, 1, zs[-1] + 1 - zs[0])))
        for i, (ex, ez) in enumerate(self.eyes if not self.flush_eyes else []):
            out.append(("eye%d" % i, "eye", "body", (ex, 21, ez), (1, 1, 1)))
        px, pz, pw, pd = self.pec
        out.append(("pectoral", "pec", "pectoral_fin", (px, 22 - 0.02, pz), (pw, 0, pd)))
        return out

    def parts(self):
        px, pz, pw, pd = self.pec
        return {"body": (None, (0.0, 23.0, 0.0), (0.0, 0.0, 0.0)),
                # raised a little; the 3 px fin less, so the fish stays within 3 px of the ground (FishHitboxCheck)
                "pectoral_fin": ("body", (0.0, 22.0 - 0.02, float(pz)), (0.3 if pd >= 3 else 0.42, 0.0, 0.0)),
                "tail_fin": (None, (0.0, 23.5, float(self.tail_z)), (0.0, 0.0, 0.0))}

    # --- colours
    def body_key(self, x, z, face):
        xi, zi = int(math.floor(x)), int(math.floor(z))
        r = abs(xi + 0.5) / (self.half - 1)
        along = (zi + 0.5 - self.snout) / float(self.rear - self.snout)
        v = 0.08 + 0.42 * r * r + 0.35 * max(0.0, along - 0.45) + 0.08 * along
        idx = int(round(v * (len(BODY_RAMP) - 1)))
        if face == "top" and (xi, zi) in self.blotch and self.big_mottles:
            return self.mottle
        if face == "top" and (xi, zi) in self.blotch:
            # mid-brown mottles, never as dark as the eyes (critic round 2): one or two steps, at most "n"
            idx = min(BODY_RAMP.index("n"), idx + self.blotch[(xi, zi)] + 1)
        if face == "top" and self.flush_eyes and (xi, zi) in self.eyes:
            return "e"                                    # a flush eye: the pupil on the body's top
        if face == "top" and (xi, zi) in self.hump and self.flush_eyes:
            idx -= 1                                      # the lighter middle ridge (critic round 3)
        if face == "top" and self.spot_out:
            if xi in (-1, 0):
                idx -= 1                                  # a soft lighter band along the middle (critic round 4)
            if (xi, zi) in self.shoulder or (not self.shoulder and any(
                    n not in self.body for n in ((xi + 1, zi), (xi - 1, zi), (xi, zi + 1), (xi, zi - 1)))):
                idx += 1                                  # the outer px inside the fringe darker: a domed back
        if face == "top":
            for ex, ez in self.eyes:
                if (xi, zi) != (ex, ez) and abs(xi - ex) <= 1 and abs(zi - ez) <= 1 and abs(xi - ex) + abs(zi - ez) == 1:
                    # the pale ring round each eye, its front corner a light gold-cream highlight (critic round 1)
                    return self.ring or ("G" if zi == ez - 1 else "L")
        if face == "south":
            idx += 1
        if face == "north":
            idx -= 1
        return BODY_RAMP[max(1, min(len(BODY_RAMP) - 1, idx))]

    def fin_key(self, x, z, face, tail=False):
        xi, zi = int(math.floor(x)), int(math.floor(z))
        along = (zi + 0.5 - self.snout) / float(self.tail_end - self.snout)
        i = 1 if along < 0.6 else 2
        # faint fin rays: every other texel along the fringe one soft step darker, on the sides only (not at the head)
        side = abs(xi + 0.5) >= self.half - 1
        if face == "top" and side and zi % 2 == 0 and along > 0.15:
            i += 1
        if tail:
            t = (zi - self.tail_z) / float(self.tail_end - self.tail_z)
            if self.flush_eyes:
                # the tail in the body's own colour, its rim a step darker, with the fringe's ray ticks (round 3)
                if face == "top":
                    if self.fan:
                        # the fan in the body's sand with darker ray stripes, its back edge a step darker (round 7)
                        if zi == self.tail_end - 1:
                            return "n"
                        return "n" if xi % 2 == 0 else "m"
                    if self.plain_fin:
                        return "F" if zi == self.tail_end - 1 or (abs(xi + 0.5) > 1 and zi == self.tail_end - 2) \
                            else ("3" if zi % 2 == 0 else "n")   # a darker fan with a pale edge (round 6)
                    return "n" if t >= 0.6 or zi % 2 == 0 else "2"
                return "3"
            i = 2 if t < 0.7 else 3
        if self.plain_fin and face == "top" and not tail:
            # a lighter 1 px band all round with darker ray ticks every second px (round 6)
            return "f" if zi % 2 == 0 and side else ("f" if xi % 2 == 0 and not side else "F")
        if self.big_mottles and face == "top" and not tail and along >= 0.2:
            # one step darker than the body, soft lighter ray ticks every 2 px all round (critic round 5)
            return "f" if zi % 2 == 0 else "F"
        if self.flush_eyes and face == "top" and along < 0.2:
            return "m"                            # round the head the rim is the body's mid brown, no dark bar
        if face in ("east", "west", "north", "south"):
            return "w" if not tail else "r"       # edge-on, the plate shows the white blind side (critic round 1)
        return FIN_RAMP[min(len(FIN_RAMP) - 1, i)]

    def belly_key(self, x, z):
        xi, zi = int(math.floor(x)), int(math.floor(z))
        if (xi, zi) not in self.body:
            return "s"
        r = abs(xi + 0.5) / (self.half - 1)
        return "W" if r < 0.6 else "w"

    def key(self, cube, face, x, y, z):
        name, kind, part, origin, size = cube
        if kind == "eye":
            # a dark pupil on top; the sides of the bump in the body's own tone, so side on they are low bumps, not
            # pale posts (critic round 1), with the front face lit
            if face == "top":
                return "e"
            return "h" if face == "north" else "m"
        if kind == "pec":
            zi = int(math.floor(z)) - origin[2]
            xi = int(math.floor(x)) - origin[0]
            if self.soft_spot:
                return "o" if zi == size[2] - 1 and xi == 0 else "m"
            if self.fin_tip:
                if self.plain_fin:
                    # the body's tone, only one dark brown texel at the tip, toward the edge (round 6)
                    return "o" if zi == size[2] - 1 and xi == 0 else "m"
                return "k" if zi == size[2] - 1 else ("o" if zi == size[2] - 2 else "P")
            if zi == size[2] - 1 and xi == (0 if self.spot_out else size[0] // 2):
                return "k"                              # the black spot, at the tip, with pale fin round it
            return "P"
        if kind == "tail":
            if face == "bottom":
                return "w"
            return self.fin_key(x, z, face, tail=True)
        if face == "bottom":
            return self.belly_key(x, z)
        if kind == "plate":
            if face == "top" and (int(math.floor(x)), int(math.floor(z))) in self.shoulder:
                return self.body_key(x, z, face)        # the 1 px shoulder inside the fringe, a step darker
            return self.fin_key(x, z, face)
        return self.body_key(x, z, face)

    # --- texture and java
    def placed(self):
        cubes = self.cubes()
        parts = self.parts()
        rel = []
        for c in cubes:
            name, kind, part, (x0, y0, z0), size = c
            # the pivots: body (0, 23, 0), the fin and the tail their own
            px, py, pz = self.abs_pivot(part, parts)
            rel.append((c, (x0 - px, y0 - py, z0 - pz)))
        rects = [(2 * c[4][2] + 2 * c[4][0], c[4][2] + c[4][1]) for c, _ in rel]
        order = sorted(range(len(rel)), key=lambda k: (-rects[k][1], -rects[k][0], k))
        pos, x, y, shelf = [None] * len(rel), 0, 0, 0
        for k in order:
            w, h = rects[k]
            if x + w > TW:
                x, y, shelf = 0, y + shelf, 0
            pos[k] = (x, y)
            x += w
            shelf = max(shelf, h)
        assert y + shelf <= TH, ("texture too small", y + shelf)
        return [(rel[k][0], rel[k][1], pos[k]) for k in range(len(rel))]

    def abs_pivot(self, part, parts):
        parent, pivot, _ = parts[part]
        return pivot  # pivots are given in absolute model px (the fin's parent, the body, sits at the origin's x/z)

    def texture(self):
        img = Image.new("RGBA", (TW, TH), self.pal["."])
        owner = {}
        parts = self.parts()
        for cube, origin, (u, v) in self.placed():
            px, py, pz = self.abs_pivot(cube[2], parts)
            for face, tu, tv, x, y, z in AW.face_texels(u, v, origin, cube[4]):
                assert owner.setdefault((tu, tv), cube[0]) == cube[0], ("overlap", cube[0], owner[(tu, tv)])
                img.putpixel((tu, tv), self.pal[self.key(cube, face, x + px, y + py, z + pz)])
        return img

    def java(self):
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
            " * The lingwata (common sole, Solea solea): a thin, oval, tongue-shaped flatfish lying on its blind side. A 1 px",
            " * fringe plate (the dorsal and anal fins running all round the edge, lighter, with ray ticks) round a 2 px body;",
            " * both eyes on the upper side near the front, one behind the other on a slant, each ringed; the small raised",
            " * pectoral fin with its dark tip; a small rounded tail fin that sways. Sandy brown with darker speckles above,",
            " * white below.",
            " * Made by art/src/fish_lingwata_model.py (do not edit by hand); texture textures/entity/fish/lingwata.png.",
            " * Parts: body (with the child pectoral_fin) and tail_fin. Lies flat on land (MimContentClient, liesFlat).",
            " */",
            "public class LingwataModel extends FishModel {",
            "    public LingwataModel(ModelPart root) {",
            "        super(root);",
            "    }",
            "",
            "    public static LayerDefinition createBodyLayer() {",
            "        MeshDefinition mesh = new MeshDefinition();",
            "        PartDefinition root = mesh.getRoot();",
        ]
        parts = self.parts()
        placed = self.placed()
        for part in ("body", "pectoral_fin", "tail_fin"):
            parent, (ax, ay, az), rot = parts[part]
            if parent:
                bx, by, bz = parts[parent][1]
                ox, oy, oz = ax - bx, ay - by, az - bz
            else:
                ox, oy, oz = ax, ay, az
            builder = "CubeListBuilder.create()"
            for (name, _k, cpart, _o, (w, h, d)), (x0, y0, z0), (u, v) in placed:
                if cpart != part:
                    continue
                builder += "\n            /* %s */ .texOffs(%d, %d).addBox(%s, %s, %s, %s, %s, %s)" % (
                    name, u, v, f(x0), f(y0), f(z0), f(w), f(h), f(d))
            has_child = any(p[0] == part for p in parts.values())
            var = "PartDefinition %s = " % part if has_child else ""
            lines.append("        %s%s.addOrReplaceChild(\"%s\", %s," % (var, parent or "root", part, builder))
            if any(rot):
                lines.append("            PartPose.offsetAndRotation(%s, %s, %s, %s, %s, %s));" % (
                    f(ox), f(oy), f(oz), f(rot[0]), f(rot[1]), f(rot[2])))
            else:
                lines.append("            PartPose.offset(%s, %s, %s));" % (f(ox), f(oy), f(oz)))
        lines += ["        return LayerDefinition.create(mesh, %d, %d);" % (TW, TH), "    }", "}", ""]
        return "\n".join(lines)


def f(v):
    s = ("%.4f" % v).rstrip("0")
    if s.endswith("."):
        s += "0"
    if s == "-0.0":
        s = "0.0"
    return s + "F"


# --- offline preview -------------------------------------------------------------------------------------------------
SHADE = {"top": 1.0, "bottom": 0.5, "north": 0.8, "south": 0.8, "west": 0.6, "east": 0.6}


def render(model, texture, yaw, pitch, scale, sub=3, bg=None):
    parts, _ = model
    by_name = {p[0]: p for p in parts}

    def world(part, p):
        while part:
            _, parent, pivot, rot, _ = by_name[part]
            p = AW.rot_point(p, rot)
            p = (p[0] + pivot[0], p[1] + pivot[1], p[2] + pivot[2])
            part = parent
        return p

    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def project(p):
        x, y, z = p
        z2, x2 = z * cy + x * sy, -z * sy + x * cy
        return z2, y * cp - x2 * sp, y * sp + x2 * cp

    pts = []
    for name, _, _, _, cubes in parts:
        for u, v, origin, size in cubes:
            for face, tu, tv, x, y, z in AW.face_texels(u, v, origin, size):
                col = texture.getpixel((tu, tv))
                if col[3] < 128:
                    continue
                k = SHADE[face]
                col = (int(col[0] * k), int(col[1] * k), int(col[2] * k))
                for i in range(sub):
                    for j in range(sub):
                        a, b = (i + 0.5) / sub - 0.5, (j + 0.5) / sub - 0.5
                        if face in ("top", "bottom"):
                            p = (x + a, y, z + b)
                        elif face in ("west", "east"):
                            p = (x, y + a, z + b)
                        else:
                            p = (x + a, y + b, z)
                        pts.append((project(world(name, p)), col))
    xs = [q[0][0] for q in pts]
    ys = [q[0][1] for q in pts]
    minx, miny = min(xs) - 1, min(ys) - 1
    wpx = int((max(xs) - minx + 1) * scale) + 1
    hpx = int((max(ys) - miny + 1) * scale) + 1
    img = Image.new("RGBA", (wpx, hpx), bg or (0, 0, 0, 0))
    depth = {}
    r = max(1, int(math.ceil(scale / sub / 2 + 0.5)))
    px_ = img.load()
    for (sx, sy_, sd), col in pts:
        px, py = int((sx - minx) * scale), int((sy_ - miny) * scale)
        for ox in range(-r, r):
            for oy in range(-r, r):
                key = (px + ox, py + oy)
                if 0 <= key[0] < wpx and 0 <= key[1] < hpx and sd < depth.get(key, 1e9):
                    depth[key] = sd
                    px_[key] = col + (255,)
    return img


VIEWS = {"side": (0, 0), "three": (35, 25), "top": (0, 90), "below": (0, -90), "front": (90, 20)}


def sheet(shots_dir):
    from PIL import ImageFont
    import tempfile
    font = ImageFont.load_default()
    W = 1800
    BG = (72, 72, 72, 255)
    blocks = []

    def title(t):
        im = Image.new("RGBA", (W, 26), (40, 40, 40, 255))
        ImageDraw.Draw(im).text((8, 6), t, fill=(240, 240, 240, 255), font=font)
        blocks.append(im)

    def row(images, h=None, gap=16, labels=None):
        images = [i for i in images if i is not None]
        if not images:
            return
        if h:
            images = [i.resize((max(1, int(i.width * h / i.height)), h), Image.LANCZOS) for i in images]
        hh = max(i.height for i in images) + (16 if labels else 0)
        im = Image.new("RGBA", (W, hh + 8), BG)
        dr = ImageDraw.Draw(im)
        x = 8
        for n, i in enumerate(images):
            if x + i.width > W:
                break
            im.paste(i, (x, 4 + (hh - (16 if labels else 0) - i.height)), i)
            if labels:
                dr.text((x, hh - 10), labels[n], fill=(230, 230, 230, 255), font=font)
            x += max(i.width, 6 * len(labels[n]) if labels else 0) + gap
        blocks.append(im)

    ref_dir = os.path.join(ROOT, "art", "references", "fish_lingwata_refonly")
    refs = [Image.open(os.path.join(ref_dir, n)).convert("RGBA")
            for n in ("solea1.jpg", "solea.jpg", "brest1.jpg", "brest3.jpg", "blind.jpg", "plate1.jpg")
            if os.path.exists(os.path.join(ref_dir, n))]
    title("References (reference only): landed soles (outline, colour), on the sand (eyes, fringe, raised pectoral with "
          "its black tip), the blind side, an old plate from above")
    row(refs, h=220)
    tmp = tempfile.mkdtemp()
    models = {}
    for cand in CANDIDATES:
        fsh = Fish(cand)
        jp = os.path.join(tmp, cand + ".java")
        open(jp, "w").write(fsh.java())
        models[cand] = (AW.parse_java(jp), fsh.texture())
    boll = (AW.parse_java(os.path.join(JAVA_DIR, "BollModel.java")),
            Image.open(os.path.join(RES, "textures", "entity", "fish", "boll.png")).convert("RGBA"))
    cod_dir = os.path.join(tmp, "cod")
    for view in ("top", "three", "side", "below"):
        title("Offline, 8x, %s: %s (installed: %s; the others are critic rounds 5-8's), and the accepted boll at "
              "the same scale" % (view, ", ".join(CANDIDATES), CHOSEN))
        row([render(models[c][0], models[c][1], *VIEWS[view], 8) for c in CANDIDATES]
            + [render(boll[0], boll[1], *VIEWS[view], 8)], labels=list(CANDIDATES) + ["boll"])
    title("Textures at 4x: " + ", ".join(CANDIDATES))
    row([models[c][1].resize((TW * 4, TH * 4), Image.NEAREST) for c in CANDIDATES], labels=list(CANDIDATES))
    if shots_dir and os.path.isdir(shots_dir):
        def shot(n):
            found = sorted(glob.glob(os.path.join(shots_dir, "*" + n + ".png")))
            return Image.open(found[-1]).convert("RGBA") if found else None
        title("In the game (candidate %s installed): side, three-quarter, top" % CHOSEN)
        row([shot("fish-lingwata-" + n) for n in ("side", "three-quarter", "top")], h=330)
        title("In the game: beside cod, on land, and the size line-up (lingwata on the sand, boll, cod, cerna, tonn)")
        row([shot("fish-lingwata-" + n) for n in ("beside-cod", "on-land", "lineup")], h=330)
        row([shot("fish-lingwata-" + n) for n in ("lineup-above", "close-three-quarter", "close-top")], h=330)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), BG)
    y = 0
    for b in blocks:
        out.paste(b, (0, y))
        y += b.height
    dest = os.path.join(ROOT, "art", "candidates", "fish_lingwata_model.png")
    out.convert("RGB").save(dest)
    print("sheet:", dest)


def main():
    args = sys.argv[1:]
    cand = CHOSEN
    if "--candidate" in args:
        cand = args[args.index("--candidate") + 1]
    fsh = Fish(cand)
    tex = fsh.texture()
    tex.save(TEXTURE)
    with open(JAVA, "w", encoding="utf-8") as fh:
        fh.write(fsh.java())
    print("installed candidate", cand, ":", os.path.relpath(TEXTURE, ROOT), "and", os.path.relpath(JAVA, ROOT))
    if "--sheet" in args:
        i = args.index("--sheet")
        rest = [a for a in args[i + 1:] if not a.startswith("--")]
        sheet(rest[0] if rest else None)


if __name__ == "__main__":
    main()
