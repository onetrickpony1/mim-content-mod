# Art

- `src/`: scripts that make every texture and model straight into the mod's resources:
  - `pilot_textures.py` and `pilot_models.py`: the kenur and borma, plus item models, blockstates and the English names;
  - `food_items.py`, `sweets.py` and `bowls.py`: the food icons;
  - `oven_dishes.py`: the dishes eaten in slices.
- `references/*owner*`: the owner's photos (not in git, reference only).
- `candidates/` (not in git): candidate pictures and comparison sheets for each round.
- `tools/measure.py`: style numbers for any 16×16 texture. `tools/sheet.py`: a comparison sheet, ours beside vanilla. `tools/owner_sheet.py`: the hotbar picture for the owner. `tools/font.py`: a label font with the Maltese letters. `tools/doc_pictures.py`: the pictures for `docs/Food/Food progress.md` (icons enlarged, in-game shots of the placed dishes).
- `references/`: reference photos (Wikimedia Commons; licences and authors in `SOURCES.tsv`).
- `STYLE.md`: the style rules, measured from vanilla.
- `preview/` (not in git): sheets, metrics and in-game screenshots for each review round.

Run: `art/.venv/bin/python art/src/pilot_textures.py && art/.venv/bin/python art/src/pilot_models.py` (then `food_items.py`, `sweets.py`, `bowls.py` and `oven_dishes.py`), then `tools/run-art.sh` for the in-game shots (`mod/build/smoke-run/screenshots/`).
The venv is private to this folder: `python3 -m venv art/.venv && art/.venv/bin/pip install pillow numpy`.
