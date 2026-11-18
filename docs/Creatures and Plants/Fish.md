---
type: item
kind: mob
subject: Creatures and Plants
status: built
tier: A
maltese: Lampuka, Tonn, Sardina, Ċerna, Awrata, Murina, Żiemel tal-Baħar, Pixxispad, Inċova, Ċawl, Ħuta Kaħla, Boll, Skorfna
english: dolphinfish, Atlantic bluefin tuna, sardine, dusky grouper, gilthead sea bream, Mediterranean moray, seahorse, swordfish, anchovy, Mediterranean damselfish, blue shark, common stingray, black and red scorpionfish
id: mimcontent:lampuka, tonn, sardina, cerna, awrata, murina, ziemel, pixxispad, incova, cawl, huta_kahla, boll, skorfna, skorfna_red
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
| `boll` | Boll (tier B) | alone or in twos, near the sea floor; stings (below) | 1.25 x 0.25 (flat) | 7 boxes, 2.63 long with the tail, 1.25 wide (the disc), 0.19 thick; flat on land too | 10 | 1-2 | `boll` |
| `skorfna` | Skorfna (tier B) | alone; rests on a rock floor, moves in short hops; venomous spines (below) | 0.5 x 0.4 | 3 boxes, 0.84 long, 0.63 wide with the fins, 0.5 tall | 6 | 1 | `skorfna` (black), `skorfna_red` (red) |

Vanilla for scale: cod 0.5 x 0.3 (3 health), salmon 0.7 x 0.4.

**Hit boxes match the fish** ([[2026-11-18 Fish hitboxes match their size]]: "hitboxes for all fish should match their actual size"). Each fish has a chain of small boxes from snout to tail, like the ender dragon's parts, so you hit exactly what you see: the swordfish's sword, the shark's tail and fins, the tuna's tail. A hit, an arrow, a trident or a fishing bobber on any box counts as hitting the fish, and a water bucket, lead or name tag used on any box works as on the fish. Beside the body there is nothing to hit any more, even inside the fish's old square box. The **body box** stays as it was: it is only for swimming and bumping into things, so fish still fit through the same gaps. The boxes follow the fish as it is drawn: turned with its body, lying flat when it flops on land, and along the murina's wave (on your screen exactly; the server's copy of the wave runs on its own clock, so an arrow can be up to about 0.3 blocks off at the murina's tail). The other fish's tails swinging from side to side, and their small body wiggle, are not followed: the boxes stay on the fish's resting line. With F3+B the boxes show in green beside the white body box. How they are sized: [[Art pipeline]], "Fish models".

**The pixxispad** (swordfish, tier B) was started on [[2026-11-18 Swordfish - start]] and built the same way: it swims alone and fast (movement speed 1.4, vanilla's fish 0.7), is as tough as a young tonn and has no cooked drop (there is no cooked swordfish item yet). Its art is placeholder for now.

**The inċova, ċawl and ħuta kaħla** (tier B) were started on [[2026-11-18 Incova, cawl and huta kahla - start]] and built the same way. Their art is placeholder for now.
- **Inċova** (anchovy, *Engraulis encrasicolus*): shoals like the sardina, a little smaller and slimmer, out in open water.
- **Ċawl** (Mediterranean damselfish, *Chromis chromis*): a small, deep-bodied dark fish with a forked tail, in groups of 3 to 6 over the shallow rocky seas all round Malta. Common.
- **Ħuta kaħla** (blue shark, *Prionace glauca*): a big, slender shark, alone and rare in the deep sea. It doesn't shy from players like the other fish do, and **ignores you unless you hurt it or carry fish** (owner, 2026-11-18: "blue shark should ignore you unless you hurt it OR you have fish in your inventory"):
  - **Hurt it** and it bites back (4 damage, 2 hearts) for 15 to 25 seconds, like vanilla's neutral mobs.
  - **Carry fish** anywhere in your inventory, within 16 blocks of it, in survival or adventure, and it hunts you. "Fish" is the item tag `mimcontent:shark_bait`: vanilla's `#minecraft:fishes` (cod, salmon, pufferfish, tropical fish, cooked cod and salmon), our caught fish (lampuka, tonn, sardina, ċerna, awrata, murina, pixxispad, inċova, ċawl, ħuta kaħla, boll, both skorfna), the lampuka moqlija, and every fish bucket, vanilla's and ours. The tag is data, so a datapack can change it. The shark looks at inventories about once a second.
  - **Drop or put away the fish** and it gives up after about 3 seconds, unless you also hurt it.
  - Creative and spectator players, and peaceful difficulty, are left alone. It doesn't hunt other fish (yet).

**The boll** (common stingray, *Dasyatis pastinaca*, tier B) was started on [[2026-11-18 Stingray next - the common stingray]]: of the stingrays recorded in Maltese waters it is the one met most often. It is a flat disc 1.25 blocks wide and 1 long with a thin whip tail 1.63 blocks long carrying a spine, about 2.6 blocks in all: the real proportions, about 2.8 times life size so it reads in game ([[2026-11-18 Boll model - sad face, small, eyes like nostrils; man o' war accepted; ward blocks all stings]]).
- **It lives on the bottom.** It swims a block or two above the sea floor, never up near the surface, and now and then settles on the bottom and lies still for 5 to 20 seconds. While resting it doesn't shy away from players. It swims by rippling the edges of its wings up and down, with no fish wag, and on land it lies flat instead of flopping on its side.
- **It only spawns over a soft floor:** sand, gravel, clay or mud no more than 16 blocks below the spawn point, at any depth below sea level (not only within 13 blocks of it like the other fish, since much of Malta's sandy sea floor is deeper than that). A boll that spawns naturally is set down on the floor.
- **It stings, but it isn't aggressive** (the real ray strikes with its tail spine when stepped on or harassed). It shies away like other fish, but:
  - **hurt it** and it stings the attacker if within 2 blocks: 2 damage (1 heart) and Poison for 5 seconds, then swims off;
  - **stand or walk on it** in survival or adventure (for example wading in shallow water) and it stings you the same way, at most once every 2 seconds.
  - Creative and spectator players, and peaceful difficulty, are never stung.

**The skorfna** (black scorpionfish, *Scorpaena porcus*, *Skorfna sewda* in Maltese, tier B) was started on [[2026-11-18 Skorfna - start]]. Its art is placeholder for now. It is stocky and big-headed, about 0.84 blocks long (a bit larger than a real 15-30 cm fish, so its spines show), with fleshy flaps over the eyes, a big mouth, a tall spiny dorsal fin and fan-like pectoral fins.
- **Which scorpionfish.** Four scorpionfish have long been listed for Malta: the black (*S. porcus*, *Skorfna sewda*), the red (*S. scrofa*, *Ċippullazza*), the small red (*S. notata*, *Skorfnott*) and, deep down, the blackbelly rosefish (*Helicolenus dactylopterus*); all are confirmed in the University of Malta's checklist of Maltese fishes (Borg et al., 2023), and a fifth, the Madeira rockfish (*S. maderensis*), was added in 2011. No survey counts them against each other. We chose the black scorpionfish because it is the one of the long-known four found on shallow rocky bottoms, where people meet it: a snorkelling study along the Maltese shore (Falzon, 2011) found only it and the Madeira rockfish in 0 to 10 m. The red and small red scorpionfish live mostly deeper. **Open point for the owner:** that same study says, tentatively and from one stretch of coast, that the Madeira rockfish "appears" to be "the commonest species of scorpaenid in inshore Maltese waters". It looks much like the black scorpionfish, has no Maltese name of its own, and was only first recorded in Malta in 2011, so we kept the black one.
- **Two versions, black and red** ([[2026-11-18 Skorfna - two versions, red and black, as reskins]]). The skorfna comes in two versions on one model, like vanilla's tropical fish patterns: only the texture differs. Shape, size, behaviour and sting are the same; each drops its own item (below).
  - **Black** (the default): the black scorpionfish, *Scorpaena porcus*, *Skorfna sewda*, mottled brown. Texture `textures/entity/fish/skorfna.png`.
  - **Red**: the red scorpionfish, *Scorpaena scrofa*, *Ċippullazza*. Texture `textures/entity/fish/skorfna_red.png` (a red-tinted placeholder until its art is drawn).
  - **The spawn split.** A new skorfna (natural spawn, spawn egg, `/summon` with no data) is red 65% of the time in the deep-sea biomes (`fond_deep_sea`, `dwejra_fond_deep_sea`) and 30% everywhere else, vanilla's oceans included, because the red one lives deeper: FishBase gives *S. scrofa* a depth range of 20 to 500 m, while *S. porcus* is "common among rocks and algae" in the shallows, and the Maltese shore study (Falzon, 2011) found no red ones in 0 to 10 m. With the Malta spawn weights (4 in the shallow seas, 2 in the deep) that comes to about 58% black and 42% red overall. The numbers are a game choice: no survey counts the two against each other.
  - **Saved and kept.** The version is synced to players, saved with the world (`Variant`: `"black"` or `"red"`) and kept in the bucket, whose tooltip says "Black" or "Red", the way vanilla names a tropical fish's pattern. `/summon mimcontent:skorfna ~ ~ ~ {Variant:"red"}` gives a red one. A skorfna or bucket saved before the versions existed is black, and so is a `/summon` with other data but no `Variant`.
  - **Each colour drops its own item** ([[2026-11-18 Skorfna icon D accepted; each colour drops its own item]]). A black skorfna drops **Black Skorfna** (`mimcontent:skorfna`, the id it always had), a red one drops **Red Skorfna** (`mimcontent:skorfna_red`). The two icons are the same drawing (candidate D of `art/src/fish_skorfna_icon.py`): `textures/item/skorfna.png` in the black skin's colours and `textures/item/skorfna_red.png` in the red skin's, as the owner saw them on the sheet. The red one has its own loot table (`entities/skorfna_red`), which the game picks for a red fish; the kill otherwise goes through vanilla's loot code as for the other fish, so Looting and dying on fire change nothing (one fish, raw). Both items sit side by side in the mod's creative tab and are both shark bait.
  - Sources: depth of *S. scrofa*: [FishBase, *Scorpaena scrofa*](https://www.fishbase.se/summary/Scorpaena-scrofa.html); habitat of *S. porcus*: [FishBase, *Scorpaena porcus*](https://www.fishbase.se/summary/Scorpaena-porcus.html); the Maltese name *Ċippullazza*: the species report ([[Maltese wildlife and flora]]) and Borg et al. (2023) above.
- **It lives on the rocky bottom.** It rests on the floor most of the time (10 to 30 seconds at a go) and now and then moves on in a short hop of up to 3 blocks, staying on the floor. It doesn't shy away from players like other fish: it trusts its camouflage. Hurt it and it darts up to 4 blocks away, once, then settles again.
- **Its spines sting.** A survival or adventure player, or a mob (not another fish), that touches it (bumps into it, stands or walks on it) or hits it in melee takes 2 damage (1 heart) and Poison for 6 seconds, at most once every 2 seconds. Arrows and thrown tridents don't count. Creative and spectator players, and peaceful difficulty, are never stung. (A real scorpionfish's venom stays active after death; the dropped item does nothing yet.)
- **It only spawns over a rock floor:** any solid block that isn't sand, gravel, clay or mud, no more than 16 blocks below the spawn point, at any depth below sea level. A skorfna that spawns naturally is set down on the floor. The Malta world has no sea-cave biome, so caves aren't listed separately; it spawns in sea caves inside the biomes below wherever their floor is rock.
- Sources: [Falzon (2011), *Naturalista sicil.* 35: 419-423](https://www.sssn.it/PDF/PDF%20NS%2035/419-423.pdf); [Borg, Dandria, Evans, Knittweis and Schembri (2023), *Diversity* 15: 225](https://um.edu.mt/library/oar/bitstream/123456789/106136/1/A_critical_checklist_of_the_marine_fishes_of_Malta_and_surrounding_waters%282023%29.pdf); the Maltese name *Skorfna sewda*: [EU fish names database](https://fish-commercial-names.ec.europa.eu/fish-names/species/scorpaena-porcus_en); rocky bottoms and venomous spines: [MaltaToday](https://www.maltatoday.com.mt/environment/nature/111247/critters_by_the_seashore_watch_out_for_these_dangerous_sea_creatures).

The żiemel is drawn about five times life size, 0.81 blocks tall, so its crown, snout, pot belly and curled tail show at vanilla's pixel size ([[2026-11-18 Ziemel - start, bigger than life]]).

### Tonn sizes
Each tonn has its own size ([[2026-11-18 Tonn - mixed sizes]]: "Mixed sizes"), like a real school with young and old fish.
- **Length 2 to 4 blocks**, tail included, most often near 3 (a random pick weighted toward the middle). The accepted model is 2.44 blocks long; the whole fish is scaled from it, so the model, hit boxes, body box, shadow and eyes always match. Body box: 2 blocks long is 1.07 x 0.57, 3 blocks is 1.6 x 0.86, 4 blocks is 2.13 x 1.15.
- **A school is one size class:** fish that spawn together stay within 10% of their leader's length.
- **Health grows with size:** 5 per block of length, so 10 (5 hearts) for a 2-block fish up to 20 (10 hearts) for a 4-block one.
- Natural spawns, the spawn egg and `/summon` all give a random size. **The size stays with the fish:** it is saved with the world, and a tonn caught in a bucket comes out the same size. A tonn from before sizes existed keeps the old size (2.44 blocks).
- It uses vanilla's scale attribute (a modifier named `mimcontent:tonn_size`), so other mods and commands that change a mob's scale still work on top of it. Nothing changes for the other fish.

## Where they spawn
Like vanilla fish, near the surface (within 13 blocks of sea level) in water; the boll instead near a soft sea floor at any depth, and the skorfna near a rock floor at any depth. Weights are relative to the other fish in the same biome.

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
| Boll | `bahar_sea`, `dwejra_bahar_sea`, `qawra_inland_sea`; `posidonia_meadows`, `dwejra_posidonia_meadows` (the sand patches); deep sea. Only over sand, gravel, clay or mud, at any depth (above) | 5; 4; 2 | warm, lukewarm | 2 |
| Skorfna | `bahar_sea`, `dwejra_bahar_sea`; `fond_deep_sea`, `dwejra_fond_deep_sea`. Only over a rock floor, at any depth (above) | 4; 2 | warm, lukewarm (only where the floor is rock) | 2 |

The `fond_band_1`-`8` biomes are the deep-sea copies in the blend toward vanilla's ocean.

## Setting
`fish_in_vanilla_oceans` in `config/mimcontent.json` (on by default): the fish also live in vanilla's warm, lukewarm and deep lukewarm oceans, so they turn up in normal worlds. `false`: only in the Malta world's seas.

## Later
- Murina: bites when disturbed, hides in rock holes, comes out at night.
- Lampuka: only in season (15 Aug to Dec), under floating rafts.
- Food values and recipes, once food gameplay is decided.
