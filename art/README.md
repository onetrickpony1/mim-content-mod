# Art

- `src/`: scripts that make every texture (`pilot_textures.py`) and model (`pilot_models.py`) straight into the mod's resources.
- `tools/measure.py`: style numbers for any 16×16 texture. `tools/sheet.py`: a comparison sheet, ours beside vanilla.
- `references/`: reference photos (Wikimedia Commons; licences and authors in `SOURCES.tsv`).
- `STYLE.md`: the style rules, measured from vanilla.
- `preview/` (not in git): sheets, metrics and in-game screenshots for each review round.

Run: `art/.venv/bin/python art/src/pilot_textures.py && art/.venv/bin/python art/src/pilot_models.py`, then `tools/run-art.sh` for the in-game shots (`mod/build/smoke-run/screenshots/`).
The venv is private to this folder: `python3 -m venv art/.venv && art/.venv/bin/pip install pillow numpy`.
