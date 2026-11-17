---
type: "topic"
---
# Art pipeline

How the mod's art is made and checked (since the art pilot, 2026-11-17). The details are in `art/README.md` and `art/STYLE.md` in the repo.

1. **Reference photos** of the real thing (Wikimedia Commons, licences recorded).
2. **Scripts make the art**: textures from shape, light, palette and noise rules; models from box geometry. Nothing is painted by hand, so everything can be re-made.
3. **Measured against vanilla**: colours, contrast, outline and light direction are kept inside vanilla's own numbers.
4. **Seen in the game**: `tools/run-art.sh` builds the mod and takes screenshots on an invisible desktop (never on the owner's screens), beside vanilla blocks and items.
5. **Judged by an independent reviewer** (a sub-agent), never by whoever made it (owner, 2026-11-17). Fixes follow the review, then it is reviewed again.

## Since the pilot: maker, critic, owner (2026-11-17)
The owner rejected art that reviewers had passed, and asked for the work to be orchestrated ([[2026-11-17 The pastizz is the flagship, with ricotta and pea kinds]] and the decisions after it).
1. **The owner's photos first.** The owner puts photos in `~/Pictures/<Dish>/`. They're copied to `art/references/*_owner*/`, kept **out of git**, used for reference only and never traced. They outrank web research.
2. **A maker agent** draws candidates (usually two or three) with a re-runnable script: `art/src/food_items.py` (bread, pastizzi, ġbejna), `sweets.py`, `bowls.py`, `oven_dishes.py` (the slice dishes and their icons). The scripts reproduce every accepted texture byte for byte.
3. **A fresh critic agent** judges at true hotbar size and in the game, gives exact pixel fixes, and the maker applies them. This loops until the critic passes it.
4. **The owner decides.** Their picks and corrections are recorded in [[Decisions]] with their exact words.
5. **Rules learnt along the way:**
   - vertical centre about 7.5–8 like vanilla foods;
   - lit from the top-left;
   - Maltese letters in every label (`art/tools/font.py`);
   - a dish's icon shows the whole uncut dish;
   - a dish's container must match its placed block (a square pan).

