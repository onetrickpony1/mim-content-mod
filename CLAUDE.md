# Malta in Minecraft content mod: start here

An optional **Fabric 26.3 add-on mod** for the Malta in Minecraft world. It adds Maltese creatures, plants, crops, food and everyday life while people play.
- This is **layer 2** of the owner's three layers. Layer 1 is the vanilla world (`~/Apps/Minecraft World`, generator mod `maltagen`). Layer 3 is a full overhaul at generation: long-term, **don't start it**.
- **The world is never touched.** Everything appears at play time: spawns by the world's `maltamc:*` biomes, drops from vanilla blocks, things players plant or craft. Removing the mod leaves the islands as they were.
- Public name: "Malta in Minecraft" / "MiM". The mod's final name isn't chosen yet (the folder is "Untitled…").

**The docs are an Obsidian vault in `docs/`. Start at `docs/Home.md`, then `docs/STATUS.md`.**

| Path | What it holds |
|---|---|
| `docs/STATUS.md` | where the mod stands, what waits on the owner |
| `docs/Food/` | **`Food design.md`**: crops, ingredients, dishes, drinks, owner questions |
| `docs/Creatures and Plants/` | `Content mod list.md`: animals, sea life, wild plants, trees |
| `docs/Maltese Life/` | `Maltese life ideas.md`: people, festa, language, sounds, seasons |
| `docs/Research/` | the species report and its notes (copied from the Malta project 2026-11-17; work from this copy) |
| `docs/Decisions/` | **every owner decision, one dated note with the owner's exact words; never edited, never re-opened unasked** |
| `docs/Templates/`, `docs/Bases/` | note templates (Decision, Item, List) and the Obsidian tables |
| `docs/Tools and Process/` | **`Keeping the vault up to date.md`**: follow it after every change |
| `mod/` | the Fabric 26.3 project (mod id `mimcontent`, a working name). Since 2026-11-17 it holds only the **art pilot**: the kenur, the borma, three foods, and the in-game screenshot test (`src/smoke`) |
| `art/` | the art: scripts that make every texture and model (`art/src`), the style rules measured from vanilla (`art/STYLE.md`), reference photos with licences; see `docs/Tools and Process/Art pipeline.md` |
| `tools/run-art.sh` | builds the mod and takes in-game screenshots on an invisible desktop (`mod/build/smoke-run/screenshots`); needs `env.sh` (Java 25 + the Gradle cache shared with the Malta project) |

## Rules
1. **Ideas, lists and designs are not a go-ahead.** Build nothing until the owner explicitly says so.
2. **Every owner decision** gets a note in `docs/Decisions/` (template `docs/Templates/Decision.md`).
3. **Keep ways back:** gameplay changes to vanilla behaviour (e.g. milkable sheep) go behind a config option, with vanilla behaviour restorable.
4. **Real Malta first.** Use sourced facts; mark unchecked Maltese names or claims with †. Vanilla items are used only where Malta really uses them.
5. **Git:** stage files by name, never `git add -A docs`. Commits carry **no Co-Authored-By lines and no mention of Claude**; they are the owner's alone. Commit identity for this repo: `onetrickpony1 <311002920+onetrickpony1@users.noreply.github.com>` (the owner's GitHub account, same as their other repos).
6. **Contact details to outside services:** only `https://maltaminecraft.com` or `maltainminecraft@gmail.com`; never the owner's personal details.
7. **The owner** is a Minecraft player, not a developer. Keep updates short, lead with what changes in-game, and use "they/them".
8. **Art is judged by an independent reviewer (a sub-agent), never by whoever made it** (owner 2026-11-17). Check it in-game beside vanilla before review.
9. **Dependencies stay private:** Python tools use `art/.venv`, not system packages; no `pacman -S`.
10. **The Malta project** (`~/Apps/Minecraft World`) has its own rules and another session may be working in it. Don't edit it from here unless asked.
