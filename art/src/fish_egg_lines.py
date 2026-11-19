"""A line-aware eye-pair check for the striped and barred fish eggs (lionfish, lizz, petrica, gallinella), 2026-11-19.

fish_egg_common.check_marks() fails on any two dark pixels level with each other 2-4 px apart, which every egg with
stripes or bars has. This one, like the kavall egg's own check (art/src/fish_kavall_egg.py), only looks at lone dark
dots: a dark pixel touching another dark pixel (8-neighbour) is part of a line, a bar or the outline, not an eye. Two
lone dark dots level with each other 2-4 px apart still fail, as they read as a pair of eyes. The scripts that use it
set common.check_marks = check_marks before calling common.run().
"""
from fish_egg_common import EGG


def check_marks(name, rows, dark):
    def is_dark(x, y):
        return 0 <= y < 16 and 0 <= x < 16 and rows[y][x] in dark

    def lone(x, y):
        return is_dark(x, y) and not any(is_dark(x + a, y + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b)

    for y in range(4, 13):
        lo, hi = EGG[y]
        dots = [x for x in range(lo + 1, hi) if lone(x, y)]
        for p in dots:
            for q in dots:
                if 2 <= q - p <= 4:
                    raise AssertionError(f"{name}: dark dots at ({p},{y}) and ({q},{y}) read as a pair of eyes")
