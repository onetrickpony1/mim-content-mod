---
type: item
kind: mob
subject: Creatures and Plants
status: built
tier: A
maltese: Lampuka, Tonn, Sardina, Ċerna, Awrata, Murina, Żiemel tal-Baħar, Pixxispad, Inċova, Ċawl, Ħuta Kaħla
english: dolphinfish, Atlantic bluefin tuna, sardine, dusky grouper, gilthead sea bream, Mediterranean moray, seahorse, swordfish, anchovy, Mediterranean damselfish, blue shark
id: mimcontent:lampuka, tonn, sardina, cerna, awrata, murina, ziemel, pixxispad, incova, cawl, huta_kahla
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

| Id | Name | Swims | Body box (blocks, w x h) | Hit boxes (blocks, the model's size) | Health | Group | Item |
|---|---|---|---|---|---|---|---|
| `lampuka` | Lampuka | in schools of up to 6 | 1.0 x 0.45 | 6 boxes, 2.19 long, 0.39 wide, 0.69 tall | 6 | 2-4 | `lampuka` (fried if burning) |
| `tonn` | Tonn | in schools of up to 5 | 1.07 x 0.57 to 2.13 x 1.15 (mixed sizes, below) | 7 boxes, 2 to 4 long (the whole fish scales) | 10 to 20 | 3-5 | `tonn` |
| `sardina` | Sardina | in schools of up to 12 | 0.4 x 0.25 | 3 boxes, 0.88 long, 0.22 wide, 0.38 tall | 3 | 4-8 | `sardina` |
| `cerna` | Ċerna | alone | 0.9 x 0.6 | 5 boxes, 1.81 long, 0.57 wide, 0.81 tall | 10 | 1 | `cerna` |
| `awrata` | Awrata | alone, small groups | 0.7 x 0.45 | 4 boxes, 1.44 long, 0.34 wide, 0.75 tall | 4 | 2-4 | `awrata` |
| `murina` | Murina | alone | 0.9 x 0.3 | 6 boxes, 2.0 long, 0.25 wide, 0.38 tall; they bend with its body | 8 | 1 | `murina` |
| `ziemel` | Żiemel tal-Baħar | alone | 0.4 x 0.8 (upright, bigger than life) | 2 boxes, 0.56 long, 0.19 wide, 0.81 tall | 2 | 1-2 | nothing |
| `pixxispad` | Pixxispad (tier B) | alone, fast (twice vanilla's fish speed) | 1.3 x 0.6 | 8 boxes, 2.81 long with the sword, 0.87 wide with the fins, 1.13 tall | 12 | 1 | `pixxispad` |
| `incova` | Inċova (tier B) | in schools of up to 12 | 0.35 x 0.2 | 3 boxes, 0.81 long, 0.17 wide, 0.31 tall | 3 | 4-8 | `incova` |
| `cawl` | Ċawl (tier B) | in small groups | 0.35 x 0.4 | 3 boxes, 0.88 long, 0.28 wide, 0.5 tall | 3 | 3-6 | `cawl` |
| `huta_kahla` | Ħuta Kaħla (tier B) | alone; neutral, bites for 4 (2 hearts) | 1.3 x 0.7 | 8 boxes, 2.69 long, 0.81 wide with the fins, 0.77 tall | 16 | 1 | `huta_kahla` (shark meat) |

Vanilla for scale: cod 0.5 x 0.3 (3 health), salmon 0.7 x 0.4.

**Hit boxes match the fish** ([[2026-11-18 Fish hitboxes match their size]]: "hitboxes for all fish should match their actual size"). Each fish has a chain of small boxes from snout to tail, like the ender dragon's parts, so you hit exactly what you see: the swordfish's sword, the shark's tail and fins, the tuna's tail. A hit, an arrow, a trident or a fishing bobber on any box counts as hitting the fish, and a water bucket, lead or name tag used on any box works as on the fish. Beside the body there is nothing to hit any more, even inside the fish's old square box. The **body box** stays as it was: it is only for swimming and bumping into things, so fish still fit through the same gaps. The boxes follow the fish as it is drawn: turned with its body, lying flat when it flops on land, and along the murina's wave (on your screen exactly; the server's copy of the wave runs on its own clock, so an arrow can be up to about 0.3 blocks off at the murina's tail). The other fish's tails swinging from side to side, and their small body wiggle, are not followed: the boxes stay on the fish's resting line. With F3+B the boxes show in green beside the white body box. How they are sized: [[Art pipeline]], "Fish models".

**The pixxispad** (swordfish, tier B) was started on [[2026-11-18 Swordfish - start]] and built the same way: it swims alone and fast (movement speed 1.4, vanilla's fish 0.7), is as tough as a young tonn and has no cooked drop (there is no cooked swordfish item yet). Its art is placeholder for now.

**The inċova, ċawl and ħuta kaħla** (tier B) were started on [[2026-11-18 Incova, cawl and huta kahla - start]] and built the same way. Their art is placeholder for now.
- **Inċova** (anchovy, *Engraulis encrasicolus*): shoals like the sardina, a little smaller and slimmer, out in open water.
- **Ċawl** (Mediterranean damselfish, *Chromis chromis*): a small, deep-bodied dark fish with a forked tail, in groups of 3 to 6 over the shallow rocky seas all round Malta. Common.
- **Ħuta kaħla** (blue shark, *Prionace glauca*): a big, slender shark, alone and rare in the deep sea. It doesn't shy from players like the other fish do, and **ignores you unless you hurt it or carry fish** (owner, 2026-11-18: "blue shark should ignore you unless you hurt it OR you have fish in your inventory"):
  - **Hurt it** and it bites back (4 damage, 2 hearts) for 15 to 25 seconds, like vanilla's neutral mobs.
  - **Carry fish** anywhere in your inventory, within 16 blocks of it, in survival or adventure, and it hunts you. "Fish" is the item tag `mimcontent:shark_bait`: vanilla's `#minecraft:fishes` (cod, salmon, pufferfish, tropical fish, cooked cod and salmon), our caught fish (lampuka, tonn, sardina, ċerna, awrata, murina, pixxispad, inċova, ċawl, ħuta kaħla), the lampuka moqlija, and every fish bucket, vanilla's and ours. The tag is data, so a datapack can change it. The shark looks at inventories about once a second.
  - **Drop or put away the fish** and it gives up after about 3 seconds, unless you also hurt it.
  - Creative and spectator players, and peaceful difficulty, are left alone. It doesn't hunt other fish (yet).

The żiemel is drawn about five times life size, 0.81 blocks tall, so its crown, snout, pot belly and curled tail show at vanilla's pixel size ([[2026-11-18 Ziemel - start, bigger than life]]).

### Tonn sizes
Each tonn has its own size ([[2026-11-18 Tonn - mixed sizes]]: "Mixed sizes"), like a real school with young and old fish.
- **Length 2 to 4 blocks**, tail included, most often near 3 (a random pick weighted toward the middle). The accepted model is 2.44 blocks long; the whole fish is scaled from it, so the model, hit boxes, body box, shadow and eyes always match. Body box: 2 blocks long is 1.07 x 0.57, 3 blocks is 1.6 x 0.86, 4 blocks is 2.13 x 1.15.
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
| Pixxispad | deep sea (`fond_deep_sea`, `fond_band_1`-`8`), rare | 1 | warm, lukewarm | 1 |
| Inċova | deep sea (`fond_deep_sea`, `fond_band_1`-`8`); `bahar_sea`, `dwejra_bahar_sea` | 15; 10 | warm, lukewarm, deep lukewarm, ocean, deep ocean | 8 |
| Ċawl | `bahar_sea`, `qawra_inland_sea`, `dwejra_bahar_sea` | 20 | warm, lukewarm | 8 |
| Ħuta kaħla | deep sea (`fond_deep_sea`, `fond_band_1`-`8`), rare | 1 | lukewarm, deep lukewarm, deep ocean | 1 |

The `fond_band_1`-`8` biomes are the deep-sea copies in the blend toward vanilla's ocean.

## Setting
`fish_in_vanilla_oceans` in `config/mimcontent.json` (on by default): the fish also live in vanilla's warm, lukewarm and deep lukewarm oceans, so they turn up in normal worlds. `false`: only in the Malta world's seas.

## Later
- Murina: bites when disturbed, hides in rock holes, comes out at night.
- Lampuka: only in season (15 Aug to Dec), under floating rafts.
- Food values and recipes, once food gameplay is decided.
