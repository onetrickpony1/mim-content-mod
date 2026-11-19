---
type: item
kind: mob
subject: Creatures and Plants
status: building
tier: C
maltese: Pixxiluna, Qamar, Pixxitanbur (all three used; "pixxi qamar" †)
english: ocean sunfish (mola mola)
id: mimcontent:mola_mola
---
# Mola mola (ocean sunfish)

The heaviest bony fish in the world, a tall flat disc that looks cut off behind. It is seen now and then off Malta and Gozo, often lazing at the surface. In the game it is **extremely rare** in the wild: fishing with jellyfish meat, once fishing is overhauled, will be practically the only way to get one ([[2026-11-18 Mola mola - extremely rare]]). Started on [[2026-11-18 Mola mola - start]]; [[Content mod list]] no. 75a.

**State (2026-11-19): building.** The mob is built and tested in the game. The **3D model** is accepted ([[2026-11-18 Skorfna egg and mola mola model accepted]]). The **item icon** was accepted ([[2026-11-19 Night fish icons and buckets - most pass; John Dory, gallinella, lingwata bucket redo]]). The spawn egg is a placeholder ([[2026-11-18 Fish art - owner approves each piece before the next]]). **It can be found but not captured** ([[2026-11-19 Mola mola - can be found, not captured; escapes when hurt; basks in the sun]]): no bucket, no drop, tough, and it escapes when hurt.

## In Malta
- **It does turn up.** The University of Malta's checklist of Maltese fishes lists *Mola mola* as confirmed in Maltese waters, and the slender sunfish *Ranzania laevis* too [1]. No other *Mola* species is listed.
- **Recent sightings** are all news reports, not counts:
  - off Wied il-Mielaħ, Gozo, August 2014, filmed by a diver who called it "a once in a lifetime experience" [2];
  - off Żurrieq, April 2024, photographed with marine biologist Alan Deidun [3];
  - off Xlendi, Gozo, August 2024 [4];
  - at Reqqa Point, Gozo, June 2025, at about 40 m deep, "roughly two metres from tip to tip" [5];
  - off the south-east coast, August 2025: "Encounters in Maltese waters, while not unheard of, are always special" [6].
- **Season:** the dated sightings fall between April and August. That is a handful of news reports, not a study, so it isn't used yet.

## Maltese name
- **Qamar** ("moon"): "one of the common Maltese names for the species is 'qamar'", Alan Deidun, marine biologist [4].
- **Pixxiluna** and **pixxitanbur**: given in two articles, the first also with qamar [3][6].
- **"Pixxi qamar"** was not found in any source. It is marked †.
- The game calls it **Pixxiluna** for now: it is in two sources, it can only mean this fish, and "qamar" alone would read as "moon". The owner may prefer another (question below).

## The real fish
- **Size:** mature fish average about 1.8 m long and about 2.5 m from fin tip to fin tip; the largest on record was 3.3 m long and 2,300 kg [7]. The Gozo diver's fish was about 2 m tip to tip [5].
- **Shape:** flattened from side to side, with **no true tail**. The tail is replaced by the **clavus**, a rounded pseudotail made from the dorsal and anal fins, which steers like a rudder. Tall dorsal and anal fins sit far back, and small fan-shaped pectoral fins sit low on the body [7].
- **Mouth:** small, with the teeth fused into a beak, so it can't close fully [7].
- **Colour:** brown to silvery grey or white, mottled; darker above and lighter below [7]. Fish out of water (reference photos) are grey to grey-brown above, silvery on the sides and pale below with soft grey blotches.
- **Swimming:** it sculls its dorsal and anal fins from side to side **together**, 0.3 to 0.6 times a second, at 0.4 to 0.7 m a second [8].
- **Basking:** it often lies on its side at the surface. One idea is that it warms up there after dives into cold water; seabirds and small fish also pick its parasites off [7]. Maltese reports describe it "often seen basking near the surface" [6].
- **Depth and food:** adults hunt mostly below 200 m. Jellyfish were long thought to be its main food; genetic studies show it eats mostly small fish, squid and crustaceans, with jellyfish and salps only about 15% of its diet [7]. It is a big bycatch of the Mediterranean swordfish fishery [7].

## In the game (built 2026-11-18)
| | |
|---|---|
| Id | `mimcontent:mola_mola`, shown as **Pixxiluna** |
| Size | 1.63 blocks long and 2.4 blocks tall fin tip to fin tip, the disc as tall as it is long (life size, like the tonn and the blue shark) |
| Body box | 1.3 x 1.8 (the disc without the fins); while basking 1.7 x 0.5, lying flat |
| Hit boxes | 5 boxes from mouth to clavus, the tall fins included ([[Fish]], "Hit boxes match the fish") |
| Health | 40 (20 hearts); no single hit takes more than 4 (2 hearts) |
| Speed | 0.35 (half vanilla's fish, 0.7); escaping, 0.375 blocks a tick (7.5 a second) for 4 seconds |
| Damage | none: harmless |
| Spawns | alone, the lowest weight (1), deep sea only; see "Extremely rare" |

- **Slow and calm.** Left alone, it drifts and swims slowly, and doesn't shy away from players (real sunfish let divers come close [5]).
- **It basks, in the sun only.** Now and then (about once every 20 seconds it may set off) it rises to the surface and lies on its side there for 10 to 30 seconds, its upper side just breaking the water, tilted 12 degrees off flat so one fin rises at an angle. Only **by day, with no rain or thunder, and with open sky above the water** where it is (not under ice, a ceiling, glass or leaves). At night or in rain it just swims slowly, and nightfall or rain ends any basking. Its box lies flat (1.7 x 0.5) and its hit boxes lie on their side, centred over it. Hurting it ends the basking.
- **Tough.** 40 health, and every hit is capped at 4, whatever the weapon: swords with any enchantment, crits, sweeps, arrows, tridents, explosions. `/kill` and the void still kill it.
- **It escapes when hurt.** It bursts straight away from whatever hurt it, sinking a little while there is water under it and turning along walls, at 7.5 blocks a second for 4 seconds (about 30 blocks). That outswims a sprint-swimming player (vanilla: about 3.9 blocks a second; 5.3 with Depth Strider III); only Dolphin's Grace (about 9.8) is faster. It doesn't stop to bask.
  - **Hurt by a player** (a hit, an arrow, a trident, TNT the player lit): in the last 2 seconds of the escape it fades out into the blue with a stream of bubbles, and is gone (removed: no death, no drop). That fish never comes back.
  - **Hurt by anything else:** it flees the same way but doesn't vanish. If a mob (a guardian, a drowned) hits it again while it still flees, it vanishes as well. Damage with no attacker (drying out on land, fire) never makes it vanish.
- **No bucket.** A water bucket does nothing to it: it isn't caught, and the bucket stays full. There is no mola bucket item.
- **Drops: nothing.** Its raw fish item, `mimcontent:mola_mola`, stays in the game (creative tab, `/give`), kept for fishing later.
- **It sculls.** Its dorsal and anal fins swing from side to side together; the clavus steers a little.
- **A spawn egg**, in vanilla's Spawn Eggs tab too, sitting in vanilla's pool. Spawn eggs and `/summon` still work.
- It counts as fish for the blue shark (its item is shark bait).

### Extremely rare
Owner, 2026-11-18: "the mola mola must be EXTREMELY rare, with fishing it with the required bait being practically the only way to find it unless you are super lucky" ([[2026-11-18 Mola mola - extremely rare]]).
- **Malta world:** only the deep sea (`fond_deep_sea`, `fond_band_1`-`8`, `dwejra_fond_deep_sea`), weight 1 (the lowest), always alone.
- **Vanilla oceans** (behind `fish_in_vanilla_oceans`): the warm ocean and the deep lukewarm ocean, weight 1. Vanilla has no deep warm ocean.
- **An extra roll:** even when the game picks it, a natural spawn goes ahead only **1 time in 400** (`MolaFish.SPAWN_CHANCE`). Spawn eggs, spawners and `/summon` always work.
- **How rare that is (an estimate):** in the deep sea about 1 natural fish spawn in 50 picks the mola, the game tries up to about 4 spots for it, and 1 in 400 of those go ahead: about **1 fish in 5,000 to 6,500**. A player sailing the deep sea sees perhaps 1,000 to 3,000 fish spawn an hour, so **about one mola every 2 to 6 hours of sailing**, and fewer in vanilla oceans, where it shares the spawns with more fish. This is a rough figure from how vanilla's spawner works; it wasn't measured over hours of play.
- **Fishing comes later.** Jellyfish meat will be its bait once fishing is overhauled ([[2026-11-18 Jellyfish drops - venom and meat; mola mola later]]). No fishing or bait behaviour is built yet.

### Art
- **3D model** (`art/src/fish_mola_model.py`, `MolaMolaModel`): first piece, made from the reference photos in `art/references/fish_mola_refonly/` (Wikimedia Commons, licences in `list.tsv`). A round disc 21 px long and 21 tall, squared off behind, with a scalloped clavus, slim tall fins far back, a small round mouth and a dark eye in a paler ring. Judged by independent critics in the game (three rounds). Waiting for the owner. Screenshots: `art/candidates/fish_mola_model_shots/` (not in git).
- **Item icon** (`art/src/fish_mola_icon.py`, A accepted 2026-11-19): the model's hues a step darker for out of water, with a dark rim. Three poses: A upright side view (installed), B tilted about 20 degrees, C about 40 degrees. Three blind readers named all three "sunfish" and found A the clearest. Compare sheet: `art/candidates/fish_mola_icon.png`.
- **Spawn egg:** a placeholder (`art/src/fish_placeholders.py mola_mola`).
- **Bucket: removed** (2026-11-19). The drawn bucket (`art/src/fish_mola_bucket.py`, night job candidate E, accepted the same morning) is retired: the script is kept for history and no longer installs anything.
- **Fading:** while it fades out the game draws it see-through, from fully seen to gone over 2 seconds; its shadow fades with it.

## Questions for the owner
1. ~~**Drops:**~~ answered 2026-11-19: **none**. It can't be captured until fishing is overhauled ([[2026-11-19 Mola mola - can be found, not captured; escapes when hurt; basks in the sun]]).
2. **Size:** a mature fish at life size (1.63 blocks long, 2.4 tall)? Or mixed sizes like the tonn, or bigger?
3. **Name:** Pixxiluna, Qamar or Pixxitanbur in the game?
4. **Rarity:** about one every 2 to 6 hours of deep-sea sailing (estimate). Rarer, or right?
5. ~~**Bucket:**~~ answered 2026-11-19: **none**. A water bucket does nothing to it, and the bucket item is removed.
6. **Season:** Maltese sightings fall between April and August. Only then, once the mod has a calendar?

## Sources
1. Borg, Dandria, Evans, Knittweis and Schembri (2023), "A critical checklist of the marine fishes of Malta and surrounding waters", *Diversity* 15: 225, List A1 (confirmed), Family Molidae. [PDF](https://um.edu.mt/library/oar/bitstream/123456789/106136/1/A_critical_checklist_of_the_marine_fishes_of_Malta_and_surrounding_waters%282023%29.pdf)
2. MaltaToday, "Huge Mola Mola filmed off Gozo's coast", 24 August 2014. [link](https://www.maltatoday.com.mt/environment/nature/42617/huge_mola_mola_filmed_off_gozoz_coast)
3. Malta Daily, "Local photographer snaps majestic sun fish off coast of Żurrieq", 19 April 2024. [link](https://maltadaily.mt/local-photographer-snaps-majestic-sun-fish-off-coast-of-zurrieq)
4. Lovin Malta, "Watch: ocean sunfish spotted off Gozo's coast near Xlendi", 4 August 2024. [link](https://lovinmalta.com/news/news-video/watch-ocean-sunfish-spotted-off-gozos-coast-near-xlendi)
5. Lovin Malta, "Sunfish spotted 40 metres deep in Maltese waters", 18 June 2025. [link](https://lovinmalta.com/lifestyle/pets/sunfish-spotted-40-metres-deep-in-maltese-waters)
6. GuideMe Malta, "Gentle giant of the sea: massive ocean sunfish makes appearance in Maltese waters", 14 August 2025. [link](https://www.guidememalta.com/en/gentle-giant-of-the-sea-massive-ocean-sunfish-makes-appearance-in-maltese-waters)
7. Wikipedia, "Ocean sunfish" (size, shape, colour, basking, diet, depth, Mediterranean bycatch). [link](https://en.wikipedia.org/wiki/Ocean_sunfish)
8. Watanabe and Sato (2008), "Functional dorsoventral symmetry in relation to lift-based swimming in the ocean sunfish *Mola mola*", *PLoS ONE* 3(10): e3446. [link](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0003446)
