"""Vanilla's spawn-egg pool, shared by every fish spawn egg of ours (2026-11-18).

Owner 2026-11-18 (docs/Decisions/2026-11-18 Boll egg B; egg pools match vanilla.md): "the pool under the egg should be
the same as vanilla. fix the other eggs if this is the same issue for the other eggs too." This is the owner's own
exception to STYLE rule 3 ("never copy vanilla pixels"), for the pool only: every other pixel of our eggs stays our own.

Measured from art/.vanilla/item (26.x): the pool is the same 30 pixels in the same 5 blues on all four vanilla fish
eggs (cod, salmon, pufferfish, tropical_fish). The tadpole egg has it too, less (2, 13), which its body covers; squid,
glow squid, dolphin, nautilus and elder guardian draw wider pools of their own; the 78 land and other eggs have none.

    row 12  ...#........#...   water showing between the egg and the side fins
    row 13  ..###......###..   the egg's own bottom edge sits at x 5-10
    row 14  ..############..
    row 15  ...##########...

Use: icon = vanilla_pool(render(GRID), old_pool_colours). Our old pool goes (every pixel in one of its colours) and
vanilla's goes in on its 30 pixels wherever the egg's body leaves them open; where the body covers one of them, the
body stays as it is. The copy check then allows exactly these pool pixels and still forbids any other copied pixel.
"""
import os

from PIL import Image

_DARK, _DEEP, _MID, _LIGHT, _BRIGHT = (47, 69, 122), (53, 90, 139), (62, 118, 163), (75, 152, 196), (99, 201, 255)
POOL = {
    (3, 12): _DARK, (12, 12): _DARK,
    (2, 13): _DARK, (3, 13): _MID, (4, 13): _LIGHT, (11, 13): _DEEP, (12, 13): _DEEP, (13, 13): _DARK,
    (2, 14): _DARK, (3, 14): _DEEP, (4, 14): _LIGHT, (5, 14): _BRIGHT, (6, 14): _BRIGHT, (7, 14): _LIGHT,
    (8, 14): _BRIGHT, (9, 14): _LIGHT, (10, 14): _MID, (11, 14): _MID, (12, 14): _DEEP, (13, 14): _DARK,
    (3, 15): _DEEP, (4, 15): _DARK, (5, 15): _DARK, (6, 15): _DARK, (7, 15): _DARK, (8, 15): _DARK,
    (9, 15): _DARK, (10, 15): _DARK, (11, 15): _DARK, (12, 15): _DEEP,
}
POOL_COLOURS = set(POOL.values())
FISH_EGGS = ("cod", "salmon", "pufferfish", "tropical_fish")


def vanilla_pool(icon, old_pool_colours):
    """A copy of icon with our old pool (every pixel in one of old_pool_colours) taken out and vanilla's pool put in
    on its 30 pixels wherever the egg's body leaves them open. Body pixels are never changed."""
    old = {tuple(c[:3]) for c in old_pool_colours}
    assert not old & POOL_COLOURS, "an old pool colour is one of vanilla's"
    im = icon.copy()
    for x in range(16):
        for y in range(16):
            p = im.getpixel((x, y))
            if p[3] and p[:3] in old:
                im.putpixel((x, y), (0, 0, 0, 0))
    for (x, y), c in POOL.items():
        if im.getpixel((x, y))[3] == 0:
            im.putpixel((x, y), c + (255,))
    check_pool(im)
    return im


def is_pool(xy, colour):
    """True for a pixel that is vanilla's own pool pixel, the one copy the owner allows."""
    return POOL.get(xy) == tuple(colour[:3]) and colour[3] == 255


def check_pool(icon):
    """Vanilla's pool exactly: each of its 30 pixels is vanilla's colour or covered by the egg's body, and vanilla's pool
    blues appear nowhere else. Returns (pool pixels shown, pool pixels under the body)."""
    shown = under = 0
    for x in range(16):
        for y in range(16):
            p = icon.getpixel((x, y))
            if (x, y) in POOL:
                if p[3] == 0:
                    raise AssertionError(f"pool pixel ({x},{y}) is empty")
                if is_pool((x, y), p):
                    shown += 1
                else:
                    assert p[:3] not in POOL_COLOURS, f"pool pixel ({x},{y}) has the wrong pool blue"
                    under += 1
            else:
                assert not (p[3] and p[:3] in POOL_COLOURS), f"vanilla pool blue at ({x},{y}), outside the pool"
    return shown, under


def check_against_vanilla(vanilla_item_dir):
    """POOL is what vanilla's fish eggs draw (skipped when the vanilla textures are not unpacked here)."""
    for n in FISH_EGGS:
        f = os.path.join(vanilla_item_dir, n + "_spawn_egg.png")
        if not os.path.exists(f):
            return False
        v = Image.open(f).convert("RGBA")
        for xy, c in POOL.items():
            assert v.getpixel(xy) == c + (255,), f"{n}: pool pixel {xy} is not vanilla's"
        for x in range(16):
            for y in range(16):
                p = v.getpixel((x, y))
                assert (x, y) in POOL or not (p[3] and p[:3] in POOL_COLOURS), f"{n}: more pool at ({x},{y})"
    return True


def pool_line(icon):
    """One line for the sheets: the pool check, and how many of its pixels the body covers."""
    shown, under = check_pool(icon)
    return (f"pool: vanilla's own (owner's exception), {shown} of its 30 pixels shown, {under} under the egg's body; "
            f"no vanilla pool blue anywhere else")
