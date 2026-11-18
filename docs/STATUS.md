---
type: "topic"
---
# Status (2026-11-18)

## Now
- **Food art phase.** Phase 1's food is being drawn and checked in the game: 40 items and 4 dishes placed on a table and eaten in slices, all accepted by the owner. The full list is in [[Food in the mod]]; [[Food progress]] shows it with pictures beside everything not drawn yet. **No gameplay is built:** no recipes, cooking or food values. That waits for the owner's go-ahead.
- **Food, draft 3** (2026-11-17): [[Food systems]] holds six Maltese food systems in five phases. They give **bonuses only**, and vanilla farming is untouched. [[Food design]] (draft 1) is the catalogue of crops and dishes. Food is one part of the mod, not all of it.

- **Dishes are paused** for now (owner, 2026-11-17).
- **The luzzu** ([[Luzzu]]): a rideable Maltese fishing boat with its own model. **Accepted** (2026-11-17) in three colour schemes, with diagonal icons. The buffs the owner picked are built, each with a config switch: 3 seats, a 27-slot fish hold, 25% faster on open sea, 10% faster heading home (the fishing bonus waits for the fish and season systems).
- **Fish** ([[Fish]], [[Fish progress]]): eleven Maltese fish are built as mobs that swim, drop themselves (the seahorse drops nothing), and have spawn eggs and buckets. Tier A is the lampuka, tonn, sardina, ċerna, awrata, murina and żiemel tal-baħar; tier B is the pixxispad, inċova, ċawl and ħuta kaħla. They spawn in the Malta world's seas and, behind the switch `fish_in_vanilla_oceans` (on), in vanilla's warm oceans. The tonn comes in mixed sizes (2 to 4 blocks), the seahorse hovers, and the blue shark is neutral unless you hurt it or carry fish. **Art: all eleven are accepted in full** (2026-11-18): icon, bucket, spawn egg and swimming model. **Hitboxes** match each fish's size: a chain of boxes from snout to tail, built and tested in the game, waiting for the owner's look ([[2026-11-18 Fish hitboxes match their size]]; screenshots `fish-hitbox-*`).
- **Boll** (common stingray, *Dasyatis pastinaca*, the most common ray in Maltese waters; [[2026-11-18 Stingray next - the common stingray]]): built with placeholder art and tested in the game. It lives on the sandy sea floor, ripples its wings, and stings (2 damage + 5 s poison) when hurt or stepped on. **Art:** item icon C and bucket N2 accepted ([[2026-11-18 Boll icon C accepted]], [[2026-11-18 Boll bucket N2 instead of N3]]); spawn egg B accepted with vanilla's pool ([[2026-11-18 Boll egg B; egg pools match vanilla]]); the 3D model is being made; bucket, egg and model wait for the owner's OK on the icon.
- **Skorfna** (black scorpionfish, *Scorpaena porcus*; [[2026-11-18 Skorfna - start]]): built with placeholder art and tested in the game. It sits still on rocky floors, hops now and then, darts when hurt, and its spines sting (2 damage + 6 s poison) when touched or hit. **Owner questions:** keep *S. porcus* or the Madeira rockfish (one paper calls it the commonest inshore, tentatively); spawn in the Blue Hole too? **Art:** the 3D model with black and red skins is accepted ([[2026-11-18 Skorfna model approved]]); the item icon is being drawn.
- **Grocery delivery** ([[Grocery delivery ideas]]): 19 ideas for ordering imported ingredients to your door; ideas only, waiting for the owner's picks.
- **How art is made:** a maker draws from the owner's photos, a separate critic judges it, and the owner has the final say ([[Art pipeline]]). The owner's photos come first: **wait for them before each batch**.

## Waiting on the owner
- **Trying the luzzu's buffs** in the game, and the oars now held in the rower's hands ([[2026-11-18 Luzzu - oars match the rower's arms]]).
- **Which creatures come next** after the eleven fish (tier C fish, sea life, land animals: [[Content mod list]]).
- **Before publishing:** check the lampuka, tonn and sardina buckets, which show the whole fish with its tail; newer buckets show the head rising out of the water ([[2026-11-18 Cerna bucket accepted; older buckets checked before release]]).
- **Jellyfish** ([[Jellyfish]]): research and 19 hazard ideas (seasons, wind-driven swarms, stings, Maltese first aid, nets, the purple flag). Which to build, and the 8 questions in the note.
- **Grocery delivery:** which ideas to take forward, and the 8 questions in [[Grocery delivery ideas]].
- **Photos for the next food batch** when dishes start again: ingredients, crops, fruit and the station blocks.
- **Decided 2026-11-17:** calendar both; start with phase 1 and its art ([[2026-11-17 Calendar both, start with phase 1 and its art]]). Earlier answers: rennet both, Maltese dishes only on Maltese blocks, freshness off, no dry-island system, no other-mod links ([[2026-11-17 Food – bonuses not penalties, food is one part of the mod, no other-mod links|decision]]).
- The 8 draft 1 food questions: [[Food design#12. Questions for the owner]] (some overlap with the systems questions).
- The 8 Maltese life questions: [[Maltese life ideas#Questions for the owner]]. The calendar question (real date or a faster year) also decides how seasonal food works.

## Decided
![[Decisions.base]]

## Parked
- **Layer 3**, the full overhaul at generation: long-term, don't start ([[2026-11-15 Three layers – vanilla world, add-on mod, overhaul later|decision]]).

## Set up
- The Fabric project (`mod/`, id `mimcontent`, a working name) holds the food art ([[Food in the mod]]), the kitchen blocks, the luzzu with its buffs (switches in `config/mimcontent.json`) and the in-game test (`src/smoke`: the art screenshots and the luzzu buffs check, run by `tools/run-art.sh`).
