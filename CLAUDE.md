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
| `mod/` | the Fabric project, **created only when building starts** |

## Rules
1. **Ideas, lists and designs are not a go-ahead.** Build nothing until the owner explicitly says so.
2. **Every owner decision** gets a note in `docs/Decisions/` (template `docs/Templates/Decision.md`).
3. **Keep ways back:** gameplay changes to vanilla behaviour (e.g. milkable sheep) go behind a config option, with vanilla behaviour restorable.
4. **Real Malta first.** Use sourced facts; mark unchecked Maltese names or claims with †. Vanilla items are used only where Malta really uses them.
5. **Git:** stage files by name, never `git add -A docs`. Commits carry **no Co-Authored-By lines and no mention of Claude**; they are the owner's alone. Commit identity for this repo: `MiM <maltainminecraft@gmail.com>`.
6. **Contact details to outside services:** only `https://maltaminecraft.com` or `maltainminecraft@gmail.com`; never the owner's personal details.
7. **The owner** is a Minecraft player, not a developer. Keep updates short, lead with what changes in-game, and use "they/them".
8. **The Malta project** (`~/Apps/Minecraft World`) has its own rules and another session may be working in it. Don't edit it from here unless asked.
