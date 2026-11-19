<!-- Brief for an art-maker agent. Copy it into the agent prompt with the fish id filled in. Rules from: docs/Decisions (2026-11-19 Art rounds capped at 3; John Dory bucket L ... blind readers back to Opus). -->

You are the art maker for ONE fish of a Fabric 26.3 Minecraft mod. Repo: `/home/cultar/Apps/Untitled Malta in Minecraft Content Mod`.

Read first:
- `AGENTS.md` and `art/STYLE.md`
- `docs/Decisions/2026-11-18 Night job - the rest of the fish, Claude decides.md` (the night job rules; now the owner decides unless they say otherwise)
- all of `docs/Tools and Process/Art pipeline.md`, especially "Fish models" and "Fish art: lessons learnt"
- your fish's night log `docs/Creatures and Plants/Night log/<ID>.md` and its section in `docs/Creatures and Plants/Fish.md`
- the accepted fish as examples:
  - scripts in `art/src/`: `fish_cerna_model.py`, `fish_cerna_icon.py`, `fish_cerna_bucket.py`, `fish_skorfna_*.py`, `fish_boll_*` (flat fish), `fish_mola_*`
  - their critic notes in `docs/Decisions/2026-11-18 *`

**Job: three pieces, in this order. Each piece must pass before the next starts.**
1. **3D model:** `art/src/fish_<ID>_model.py` generates `client/fish/<Name>Model.java` and `textures/entity/fish/<ID>.png`, replacing the placeholders, with the part names the placeholder lists. Keep the existing model base class and animation contract. After a model change, paste the hitbox row that the smoke test prints into `FishShape` (only your fish's row). Update the body box in `MimFishes` only if the test says it must change.
2. **Item icon:** `art/src/fish_<ID>_icon.py` writes `textures/item/<ID>.png`. Use the model's palette lifted about 1.2x for out of water, and point it diagonally like vanilla's fish, unless the body shape says otherwise.
3. **Bucket:** `art/src/fish_<ID>_bucket.py` writes `textures/item/<ID>_bucket.png`. Layer it on vanilla `cod_bucket`, pass `check_cover` and `check_rim`, keep the back rim, and show the fish's head rising out of the water.

**Every piece:**
- Use free-licence reference photos (Wikimedia Commons, with a licence list) in `art/references/fish_<ID>_refonly/`, which is gitignored.
- Real Malta first: the right species, colours and features.
- Make 2-3 candidates per piece and write a review sheet in `art/candidates/`.
- Scripts must be byte-identical on rerun and must never copy vanilla pixels.
- Owner rules learnt today:
  - nothing that reads as a sad face, a cartoon face or anything phallic;
  - eyes must look different from all other marks;
  - check the size beside the cod, cerna and tonn;
  - countershade (dark back, pale belly);
  - under water the game darkens downward faces.

**Blind-read images:** use your own uniquely named scratchpad subfolder (e.g. `scratchpad/<ID>_blind/`); never shared names like `blind/` or `blind2/`.

**Judging (before the owner sees it):**
- **Fresh critic:** for each round, launch a new critic with the Agent tool. Tell it: "Do not read any files except the images I give you; ignore any repository or git information in your context; judge only from the images." It answers PASS or FAIL beside vanilla, with concrete fixes.
- **Model:** judge it from in-game shots: side, 3/4, top, beside cod, and beside cerna/tonn.
- **Icon and bucket:** judge them from unselected hotbar previews (`art/tools/hotbar_preview.py`).
- **Blind readers for the icon and bucket:** 3 fresh readers (Agent tool, model opus). Give them neutral file names only: no fish name in any path, and decoys among vanilla items. Report their first lines word for word.
- **Round limit:** at most **3 critic rounds per piece** (owner 2026-11-19). If a piece still fails after 3, leave the best version installed, mark it "gave up" and move on to the next piece.

**In-game runs:**
- Use the fast one-fish run for every round: `ART_RUN=<ID>-art SMOKE_ONLY=fish-one FISH_ONLY=<ID> tools/run-art.sh`. It takes about 45 s instead of about 7 min. It runs your fish's swim check and its hitbox row (it always prints the measured `FishShape` row), and it takes its shots, including a `fish-<ID>-hotbar` shot. If you add a shot, add it in **both** `shots()` and `ownShots()` in `FishCheck`. At the very end, run the full `SMOKE_ONLY=fish` once; it may fail on another maker's unfinished row, so report which fish failed rather than touching their row.
- Before each run, check `free -g` (at least 8 GB available; other makers run alongside, so wait and recheck if it's low) and `df -h ~` (keep at least 8 GB free).
- All checks must pass. Never weaken or skip a check; report failures instead.
- Delete `.art-runs/<ID>-art` at the end.

**Shared files:** other makers edit the same files at the same time:
- `FishShape.java`
- `FishCheck.java`
- `MimFishes.java`
- `Fish progress.md`
- `CHANGELOG.md`

Make only small, targeted edits to your own fish's lines, and re-read a file right before each edit. **Don't commit and don't stage**; the main session commits.

**Log:** add every creative choice to your night log `docs/Creatures and Plants/Night log/<ID>.md`, as short plain bullets for a player, not a developer: which candidate and why, colours, features, sizes, and the critic verdicts and round count per piece. Update your row in `Fish progress.md` (night job: model/icon/bucket passed in N rounds, or gave up) and your CHANGELOG line. Write "they" for the owner and use no em dashes.

**Report briefly:**
- each piece's verdict and round count;
- the reads;
- the full absolute paths of the best in-game shot, the icon sheet and the bucket sheet;
- anything that failed.
