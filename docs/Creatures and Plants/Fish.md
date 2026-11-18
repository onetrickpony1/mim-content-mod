---
type: item
kind: mob
subject: Creatures and Plants
status: built
tier: A
maltese: Lampuka, Tonn, Sardina, Ċerna, Awrata, Murina, Żiemel tal-Baħar
english: dolphinfish, Atlantic bluefin tuna, sardine, dusky grouper, gilthead sea bream, Mediterranean moray, seahorse
id: mimcontent:lampuka, tonn, sardina, cerna, awrata, murina, ziemel
---
# Fish

The tier A fish from [[Content mod list]] section 6, built on the owner's go-ahead ([[2026-11-17 Tier A fish - start building]]). Pictures, once the art is accepted, go in [[Fish progress]].

**State (2026-11-17):** built and tested in the game. **Art: placeholder, waiting for the art round** (plain boxes and simple icons; the model contract for the art makers is in [[Art pipeline]], "Fish models").

## What each fish has
- **A live mob** that swims like vanilla's fish: it shies away from players, panics when hurt, flops on land and can be caught in a bucket. No new behaviours yet (the moray's bite and the lampuka season come later).
- **An inventory item**, dropped when it is killed (1 fish). The lampuka drops the existing `mimcontent:lampuka` item, or `lampuka_moqlija` if it dies burning (as vanilla cod drops cooked cod). **The żiemel tal-baħar drops nothing** and has no item.
- **A spawn egg**, also in vanilla's Spawn Eggs tab.
- **A bucket** with the fish alive in water, like vanilla's bucket of cod: use a water bucket on the fish to catch it, empty the bucket to let it out. Buckets are also in the Tools tab after vanilla's fish buckets.
- No food values or recipes: food gameplay isn't decided yet.

| Id | Name | Swims | Size (blocks, w x h) | Health | Group | Item |
|---|---|---|---|---|---|---|
| `lampuka` | Lampuka | in schools of up to 6 | 1.0 x 0.45 | 6 | 2-4 | `lampuka` (fried if burning) |
| `tonn` | Tonn | in schools of up to 5 | 1.07 x 0.57 to 2.13 x 1.15 (mixed sizes, below) | 10 to 20 | 3-5 | `tonn` |
| `sardina` | Sardina | in schools of up to 12 | 0.4 x 0.25 | 3 | 4-8 | `sardina` |
| `cerna` | Ċerna | alone | 0.9 x 0.6 | 10 | 1 | `cerna` |
| `awrata` | Awrata | alone, small groups | 0.7 x 0.45 | 4 | 2-4 | `awrata` |
| `murina` | Murina | alone | 0.9 x 0.3 | 8 | 1 | `murina` |
| `ziemel` | Żiemel tal-Baħar | alone | 0.3 x 0.45 | 2 | 1-2 | nothing |

Vanilla for scale: cod 0.5 x 0.3 (3 health), salmon 0.7 x 0.4.

### Tonn sizes
Each tonn has its own size ([[2026-11-18 Tonn - mixed sizes]]: "Mixed sizes"), like a real school with young and old fish.
- **Length 2 to 4 blocks**, tail included, most often near 3 (a random pick weighted toward the middle). The accepted model is 2.44 blocks long; the whole fish is scaled from it, so the model, hitbox, shadow and eyes always match. Hitbox: 2 blocks long is 1.07 x 0.57, 3 blocks is 1.6 x 0.86, 4 blocks is 2.13 x 1.15.
- **A school is one size class:** fish that spawn together stay within 10% of their leader's length.
- **Health grows with size:** 5 per block of length, so 10 (5 hearts) for a 2-block fish up to 20 (10 hearts) for a 4-block one.
- Natural spawns, the spawn egg and `/summon` all give a random size. **The size stays with the fish:** it is saved with the world, and a tonn caught in a bucket comes out the same size. A tonn from before sizes existed keeps the old size (2.44 blocks).
- It uses vanilla's scale attribute (a modifier named `mimcontent:tonn_size`), so other mods and commands that change a mob's scale still work on top of it. Nothing changes for the other fish.

## Where they spawn
Like vanilla fish, near the surface (within 13 blocks of sea level) in water. Weights are relative to the other fish in the same biome.

| Fish | Malta world (`maltamc:`) | Weight | Vanilla oceans (switch on) | Weight |
|---|---|---|---|---|
| Sardina | `bahar_sea`, `posidonia_meadows`, `qawra_inland_sea`, `dwejra_bahar_sea`, `dwejra_posidonia_meadows`; deep sea (`fond_deep_sea`, `fond_band_1`-`8`) | 25; 15 | warm, lukewarm, deep lukewarm | 10 |
| Awrata | the shallow seas above | 15 | warm, lukewarm | 8 |
| Ċerna | `fond_deep_sea`, `dwejra_fond_deep_sea`, `dwejra_bahar_sea` | 5 | warm, deep lukewarm | 3 |
| Murina | `bahar_sea`, `dwejra_bahar_sea`, `dwejra_fond_deep_sea`, only with rock within 2 blocks | 4 | warm, lukewarm | 2 |
| Tonn | deep sea (`fond_deep_sea`, `fond_band_1`-`8`) | 3 | deep lukewarm | 2 |
| Lampuka | deep sea, `bahar_sea`, `dwejra_fond_deep_sea` (all year for now; the 15 Aug to Dec season waits for the calendar) | 6 | warm, lukewarm, deep lukewarm | 4 |
| Żiemel tal-Baħar | `posidonia_meadows`, `dwejra_posidonia_meadows` | 3 | warm, lukewarm | 2 |

The `fond_band_1`-`8` biomes are the deep-sea copies in the blend toward vanilla's ocean.

## Setting
`fish_in_vanilla_oceans` in `config/mimcontent.json` (on by default): the fish also live in vanilla's warm, lukewarm and deep lukewarm oceans, so they turn up in normal worlds. `false`: only in the Malta world's seas.

## Later
- Murina: bites when disturbed, hides in rock holes, comes out at night.
- Lampuka: only in season (15 Aug to Dec), under floating rafts.
- Food values and recipes, once food gameplay is decided.
