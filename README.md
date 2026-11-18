# Malta in Minecraft: content mod

An optional Fabric 26.3 add-on mod for the [Malta in Minecraft](https://maltaminecraft.com) world. It brings Maltese food, wildlife, crops and everyday life to the islands while you play. The world itself stays pure vanilla, so removing the mod leaves the islands as they were.

![Maltese food in the hotbar beside vanilla food, and baked dishes on a table](docs/images/preview.png)

## Features

The mod is in its art phase. Everything below can be seen in the game, but has no recipes or food values yet.

- **Maltese food:** ħobż tal-Malti, ftira, ħobż biż-żejt, ftira Għawdxija, galletti, four kinds of pastizzi, ġbejna, imqaret, kannoli and qagħaq tal-għasel.
- **Stews and dips** in a Maltese terracotta bowl: stuffat tal-fenek, aljotta, stuffat tal-qarnit and bigilla.
- **Oven dishes you set on a table and eat in slices**, like a cake: ross il-forn, imqarrun il-forn, timpana and torta tal-lampuki.
- **A kitchen:** the kenur (a stone stove) and the borma (a clay stew pot).
- **Fish:** lampuka, tonn, sardina, ċerna, awrata, murina and żiemel tal-baħar (seahorse) swim in the sea, drop themselves as items (the seahorse drops nothing), and have spawn eggs and buckets. The tonn comes in mixed sizes. The lampuka, tonn and sardina have their final art; the others are being drawn.
- **The luzzu**, Malta's fishing boat, in three colour schemes. Unlike the food it already plays: 3 seats, a fish hold, faster on open sea, and a little faster heading back to its harbour.

The full list with item ids is in [docs/Food/Food in the mod.md](docs/Food/Food%20in%20the%20mod.md).

## Install

There's no release yet. To build the mod yourself, you need Java 25:

```
cd mod
./gradlew build
```

On Windows, run `gradlew.bat build` instead. The jar is in `mod/build/libs/`. Put it in your Fabric 26.3 `mods` folder with Fabric API.

## Use

Start a world with the mod and look for the items in the creative inventory. The design docs are an Obsidian vault: open the `docs/` folder in Obsidian and start at `Home.md`.

To see the art in the game, `tools/run-art.sh` builds the mod and takes screenshots on an invisible desktop (Linux, needs `env.sh`; see `env.sh.example`). Several can run at once: give each a name with `ART_RUN=<name> tools/run-art.sh`, and its screenshots go to `.art-runs/<name>/build/smoke-run/screenshots`. `SMOKE_ONLY=fish` (or `luzzu`, `art`, comma-separated) runs only those checks. To watch the art being made in your browser, run `python3 tools/art-viewer.py` and open http://localhost:8765. It shows candidates, the picks, in-game shots, test runs and your decisions as they happen. The art itself is made by the scripts in `art/src/` (see [art/README.md](art/README.md)).

## Settings

The first time the game starts, the mod writes `config/mimcontent.json`. Every gameplay change has a switch there, all on by default; set one to `false` and that part goes back to vanilla behaviour. Restart the game after editing. On a server, the server's file decides.

| Switch | What it turns on |
|---|---|
| `luzzu_more_seats` | 3 seats in a luzzu (vanilla boats: 2) |
| `luzzu_fish_hold` | the luzzu's 27-slot fish hold |
| `luzzu_engine` | the luzzu is 25% faster on open sea |
| `luzzu_finds_home` | the luzzu is 10% faster heading toward its harbour |
| `fish_in_vanilla_oceans` | the Maltese fish also live in vanilla's warm and lukewarm oceans (off: only in the Malta world's seas) |

## Notes

- The mod's id is `mimcontent`, a working name. The final name isn't chosen yet.
- Changes are listed in [CHANGELOG.md](CHANGELOG.md).

## License

Private for now. A licence will be added before any public release.
