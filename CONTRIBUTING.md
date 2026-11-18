# Contributing

Thank you for helping bring Malta to Minecraft. You don't need to write code to help: a single line with an idea is welcome, and every one is read and considered.

A low bar to send an idea doesn't mean every idea goes in. Each one is weighed against the rules below, and some will change on the way or not make it. The quality bar for the mod stays where it is. More ideas just give more to choose from.

## Ways to help

- **An idea:** a Maltese food, animal, plant, tradition or sound the mod should have, or a better way to do something already in it. [Open an idea issue](https://github.com/onetrickpony1/mim-content-mod/issues/new?template=idea.yml). No code, art or Minecraft knowledge needed.
- **Something Maltese that's wrong:** a name, a spelling, a recipe, where a fish lives. [Open a Malta fact issue](https://github.com/onetrickpony1/mim-content-mod/issues/new?template=malta-fact.yml). A source helps a lot: a link, a book, or "my nanna makes it this way".
- **A bug:** [open a bug issue](https://github.com/onetrickpony1/mim-content-mod/issues/new?template=bug.yml). Say what you did, what you expected and what happened, with your Minecraft, Fabric and mod versions.
- **Code or art:** send a pull request. For anything bigger than a small fix, open an issue first, so you know it's wanted before you spend time on it.

## What the mod must stay

These are the project's rules. A pull request that breaks one will be asked to change, however good it is otherwise.

1. **The world is never touched.** Everything the mod adds appears while you play: mobs spawn by the Malta world's own biomes, drops come from vanilla blocks, and everything else is caught, planted, built or cooked. Removing the mod leaves the islands exactly as they were. Don't add world generation or structures.
2. **Bonuses, never penalties.** Vanilla keeps working as it does. Maltese ways of doing things (the right station, good irrigation, the season) give you more. Doing without them never takes anything away. For example: no system that makes vanilla farming harder.
3. **Every change to vanilla behaviour has a switch** in `config/mimcontent.json`, on by default. Turned off, that part behaves exactly like vanilla.
4. **Real Malta first.** Names, dishes, animals and where they live come from sources. Write Maltese names with their proper letters (ħ, ġ, ċ, ż, għ), with the English name beside them. Mark anything you couldn't check with †. A vanilla item or mob is only used where Malta really uses it.
5. **Maltese dishes are made on their Maltese block** (the kenur, the oven and so on), never on vanilla stations.
6. **Animals are worth more alive.** Protected species and birds can be killed, but there is no reason to: alive they are useful, and killing one is mostly a loss. Don't add valuable drops to them.
7. **No links to other mods.** The only dependencies allowed are ones useful in their own right, such as Fabric API or a model or animation library.
8. **Food is one part of the mod.** Creatures, plants and everyday Maltese life matter as much.
9. **Settled decisions stay settled.** Every design decision is a dated note in `docs/Decisions/`. If you think one is wrong, open an issue and say why. Don't change it inside a pull request.

## Art

The art has to sit next to vanilla and look like it belongs.

- **Make it with a script** in `art/src/`, so it can be re-made and tuned. Hand-painted files can't be accepted as they are, but a hand-drawn sketch in an issue is a great start.
- **Start from real photos.** Shapes and colours come from photos of the real thing. Reference photos committed to the repo need a free licence (Creative Commons or public domain), listed in `art/references/SOURCES.tsv`. Photos you only look at can be anything; keep those out of the repo.
- **Never copy or recolour vanilla textures.** Measure them instead: `art/STYLE.md` lists vanilla's numbers (colours, contrast, outline, light direction) and your art should fall inside them. The one exception is the pool under spawn eggs, which matches vanilla's exactly.
- **Spawn eggs are egg-shaped,** with vanilla's outline and the animal's features painted on. They must never read as the whole animal or a ball.
- **Fish buckets show the head** rising out of the water, the way vanilla's do, never the whole fish.
- **Check it in the game**, beside the vanilla things it sits with, and add a screenshot to your pull request. A piece is judged by someone other than the person who made it before it goes in.

## Pull requests

- **One change per pull request.** Say what changes in the game, how you tested it, and include a screenshot for anything visible.
- **Test it in the game.** The mod must build (`cd mod && ./gradlew build`, Java 25) and the change must work in a real game, not only compile.
- **Add a line under `## Unreleased` in `CHANGELOG.md`**, in this form: `- **Short summary.** What the player saw before, and what happens now.`
- **Writing style** for code comments, docs, the changelog and in-game text: British English (colour, behaviour), plain short sentences, and no em dashes (use a full stop, comma, colon or brackets).
- **Using AI is fine.** Most of this mod is made with AI coding tools. You are responsible for what you send: read it, test it in the game, and make sure it follows the rules above.

## For AI agents

If you work with an AI agent, point it at this file first. `AGENTS.md` is written for the owner's own sessions on the owner's PC: its layout of the repo and docs is useful, but the parts about the owner's machine (`env.sh`, `tools/run-art.sh`, the shared Gradle cache, the commit identity, waiting for the owner's photos) don't apply to you. Where the two files differ, this one is what applies to your contribution.

## Licence of your contribution

By sending an issue, idea or pull request, you agree that it may be used in the mod under the same licence as the rest of the repo, [CC BY-NC-SA 4.0](LICENSE), with its extra permission for videos, streams and free modpacks. You will be credited. The Kinnie name and label are a trademark of Simonds Farsons Cisk plc and aren't covered by the licence.
