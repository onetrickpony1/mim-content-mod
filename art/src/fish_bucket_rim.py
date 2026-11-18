"""The bucket's back outline, shared by every fish bucket script (art/src/fish_<id>_bucket.py), 2026-11-18.

Owner: "the back of the bucket is weird in the seahorse one, and that made me realise that in some of other ones the
back outline disappears of the bucket" (docs/Decisions/2026-11-18 Buckets - keep the back outline.md).

Our bucket layers sit over vanilla's cod_bucket, whose bucket is drawn ONE ROW LOWER than the empty bucket and the
water bucket (its mouth's front lip is row 6, its bottom row 15; the empty bucket's are rows 5 and 14). So in our
composites the back rim's dark outline is:
- row 2, x5-10 (the far edge of the mouth);
- row 3, x3-4 and x11-12 (its corners);
- rows 4-5, x2 and x13 (the sides down to the front lip, which is vanilla's own row 6 and never ours).
check_rim() asserts that each of these is dark in the composite unless the fish itself sits in front of it (listed
per script), and that our water never sits outside the mouth: row 3 x5-10 behind the far edge, rows 4-5 x3-12.
Where our layer has to paint the outline itself (over a cod pixel), it uses RIM, our own dark grey near vanilla's
#353535 but never equal to it.
"""
import os

from PIL import Image

RIM = (0x38, 0x38, 0x38)  # our back-rim outline tone (vanilla's is #353535)
WATER = {(0x2a, 0x55, 0xc4), (0x1d, 0x3c, 0x96), (0x6a, 0x92, 0xea)}  # our water shades, shared by every bucket

OUTLINE = ([(x, 2) for x in range(5, 11)] + [(3, 3), (4, 3), (11, 3), (12, 3)]
           + [(2, 4), (13, 4), (2, 5), (13, 5)])
MOUTH = {(x, 3) for x in range(5, 11)} | {(x, y) for y in (4, 5) for x in range(3, 13)}


def _dark(p):
    return p[3] == 255 and max(p[:3]) < 0x40 and max(p[:3]) - min(p[:3]) < 6


def check_rim(layer, cod_bucket, fish_over=()):
    """Assert the back-rim outline shows in layer-over-cod_bucket, except at fish_over (pixels the fish covers)."""
    if not os.path.exists(cod_bucket):
        print("note: art/.vanilla missing, rim not checked")
        return
    comp = Image.open(cod_bucket).convert("RGBA")
    comp.alpha_composite(layer)
    fish_over = set(fish_over)
    assert fish_over <= set(OUTLINE), f"not outline pixels: {sorted(fish_over - set(OUTLINE))}"
    lost = [p for p in OUTLINE if p not in fish_over and not _dark(comp.getpixel(p))]
    assert not lost, f"back-rim outline lost at {lost}"
    over = [p for p in fish_over if layer.getpixel(p)[3] == 0 or layer.getpixel(p)[:3] in WATER
            or _dark(layer.getpixel(p))]
    assert not over, f"listed as fish but not fish at {over}"
    spill = [(x, y) for y in range(16) for x in range(16)
             if layer.getpixel((x, y))[3] and layer.getpixel((x, y))[:3] in WATER and (x, y) not in MOUTH]
    assert not spill, f"water outside the bucket mouth at {spill}"
    print(f"rim ok: {len(OUTLINE) - len(fish_over)} outline pixels dark, {len(fish_over)} behind the fish, no water spills")
