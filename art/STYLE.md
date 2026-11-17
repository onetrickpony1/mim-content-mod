# Art style rules (measured from vanilla 26.3, 2026-11-17)

Measured with `art/tools/measure.py` on the 26.3 client textures. Ours are measured the same way and kept inside these ranges.

## Food items (16×16, 14 vanilla foods)
| Number | Vanilla average | Range seen |
|---|---|---|
| Opaque coverage | 0.43 | 0.29 (stews) – 0.77 (cake) |
| Unique colours | 10 | 6 (egg) – 20 (rabbit stew) |
| Darkest luminance | 0.18 | 0.0 – 0.35 |
| Lightest luminance | 0.74 | 0.32 – 0.99 |
| Outline luminance | 0.32 | about 0.6 × the inside |
| Inside luminance | 0.54 | |
| Top-left minus bottom-right | +0.07 | 0.01 – 0.17: light from the top left, gently |

## Blocks (stone, clay, brick, furnace)
| Number | Vanilla average |
|---|---|
| Unique colours | 7 (4 – 13) |
| Darkest / lightest luminance | 0.43 / 0.69 |
| Top-left minus bottom-right | 0.0: no direction (the game shades faces itself) |

## Rules
1. Every texture is made by a script in `art/src/`, never painted by hand, so it can be re-made and tuned.
2. Shapes and colours come from reference photos in `art/references/` (licences in `SOURCES.tsv`).
3. Vanilla textures are **measured, never copied or recoloured**. The mod's art is original.
4. Every piece is judged by an independent reviewer (a sub-agent), never by whoever made it. Fixes follow the review.
5. Every piece is checked **in the game**, beside the vanilla things it sits with: `tools/run-art.sh` takes the screenshots.
