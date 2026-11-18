# Contributing

Thank you for helping bring Malta to Minecraft. Every idea is read and considered, even a single line with no code.

## Ways to help

- **An idea:** a Maltese food, animal, plant, tradition or sound the mod should have, or a better way to do something already in it. [Open an idea issue](https://github.com/onetrickpony1/mim-content-mod/issues/new?template=idea.yml). No code, art or Minecraft knowledge needed.
- **Something Maltese we got wrong:** a name, a spelling, a recipe, where a fish lives. [Open a Malta fact issue](https://github.com/onetrickpony1/mim-content-mod/issues/new?template=malta-fact.yml). A source (a link, a book, "my nanna makes it this way") helps a lot.
- **A bug:** [open a bug issue](https://github.com/onetrickpony1/mim-content-mod/issues/new?template=bug.yml).
- **Code or art:** send a pull request. For anything big, open an issue first so we can agree on it before you spend time.

## How the project works

- **The owner decides.** Ideas go on the lists in `docs/`. Nothing is built until the owner says yes, and every decision is written down in `docs/Decisions/`, in the owner's own words.
- **Real Malta first.** Maltese names and facts come from sources. Anything not yet checked is marked with †.
- **The world is never touched.** Everything the mod adds appears while you play: removing the mod leaves the islands as they were.
- **Gameplay changes to vanilla** go behind a switch in `config/mimcontent.json`, so they can be turned off.
- **Art is made by scripts** in `art/src/` (see `art/README.md` and `art/STYLE.md`), never by copying vanilla textures, and is judged in the game beside vanilla before the owner accepts it.
- **Start here:** `AGENTS.md` and `docs/Home.md` explain the layout of the repo and the docs.

## Pull requests

- Keep each pull request to one change, and say what changes in the game.
- Add a line under `## Unreleased` in `CHANGELOG.md`.
- The mod must still build: `cd mod && ./gradlew build` (Java 25).

## Licence of your contribution

By sending an issue, idea or pull request, you agree that it may be used in the mod under the same licence as the rest of the repo, [CC BY-NC-SA 4.0](LICENSE). You will be credited.
