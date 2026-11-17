---
type: "list"
date: "2026-11-17"
status: "open"
---
# Food systems (draft 2)

**State:** design only. Nothing is built.

Written after the owner's decision [[2026-11-17 Food – go bigger, new art and systems, a materially Maltese change]]:

> these foods need to add something to the game. a materially maltese change

[[Food design]] (draft 1) stays as the **catalogue**: what grows, what's made, the 51 dishes. This note is about **how the game changes**: the stations, the land, the year and the sea that make food in Malta feel different from food anywhere else in Minecraft.

Marks: **✓** = checked against a source (listed at the end); **†** = general knowledge, still to check.

---

## The idea in one paragraph

In vanilla Minecraft, food is a solved problem by day two: a wheat farm next to water, a furnace, done. **In Malta, food was always a fight with a dry island:**
- water was dug, stored and lifted by hand;
- grain went to the Knights' windmills, and bread to the village oven;
- the summer was spent salting, drying and bottling against the winter;
- the sea was fished by season.

The mod brings that fight, and the pleasure of winning it, into the game. Players plan around **water, the season, the wind and the pantry**. Their reward is food that's far better than vanilla: dishes that feed for longer, give real bonuses, and are made in places you build and that look Maltese.

## The ten systems

| # | System | What changes in play | Art | Phase |
|---|---|---|---|---|
| 1 | **The dry island**: saqwi and bagħli | Summer farmland dries out unless you irrigate it from wells and cisterns | high | 2 |
| 2 | **The Maltese year** | Crops, fruit, fish, salt and honey each have their season | low | 2 |
| 3 | **The kitchen**: kenur, borma, taġen | Real cooking on a stone stove, in pots you can see, in batches | high | 1 |
| 4 | **Bread**: mitħna and forn | Wheat → windmill → flour → sourdough → the village wood oven | high | 1 / 4 |
| 5 | **The pantry**: salt, sun, brine, oil | Fresh food goes off; preserving it is the summer's work | medium | 3 |
| 6 | **Cheese**: ġbejniet from start to finish | Sheep, rennet, rush baskets, the cane drying cage | medium | 3 |
| 7 | **Olives and wine** | A Roman-style olive press; grape pressing and barrels in a cellar | high | 4 |
| 8 | **Bees** | Clay-jar hives and rock-cut apiaries; honey by flower and season | medium | 4 |
| 9 | **The sea's food** | Cane traps on the seabed; lampuki rafts in autumn | medium | 5 |
| 10 | **Eating well**: il-Mediterran † | A varied Maltese diet is rewarded; eating the same thing all day isn't | low | 6 |

**Every system has an on/off switch in the mod's config** (rule 3 in `CLAUDE.md`). With every switch off, the mod is only the content of draft 1.

---

## 1. The dry island: saqwi and bagħli

**Real Malta:**
- Maltese farmers still divide land into **saqwi** (irrigated) and **bagħli** (rain-fed) ✓.
- Most land is rain-fed. Irrigated land is only about 11% of farmland, but it yields at least 3.5 times as much ✓.
- Water came from **wells and cisterns** (bir, ġiebja ✓). About 137 Maltese places carry "bir" in their name ✓.
- It was lifted by hand, with a pulley on two poles (ġabja ✓), or by the **sienja** ✓, the animal-turned water wheel (norija ✓).
- The round marrow is called *qargħa bagħli*: the rain-fed marrow.

**In the game:**
- **Farmland in the world's Maltese biomes dries out in the dry season** (about May to September). Vanilla "water within 4 blocks" no longer keeps it wet in summer. In the wet season (October to April), rain waters everything, as in vanilla.
- **Bagħli crops** grow on winter rain alone: wheat, barley, broad beans, peas, sulla, cauliflower, cabbage, kohlrabi, onion and garlic. Planted in autumn, they're harvested in spring. They're easy and reliable, but only one harvest a year.
- **Saqwi crops** need watering through the summer: tomato, marrow, melon, aubergine, pepper and herbs. They yield **far more** and allow a second crop. Unwatered, they wilt and stop growing; they don't die at once.
- **Water sources** (new blocks):
  - **Il-bir** (well): dug down to the water table, with a stone well-head (ħorża ✓). Draw water by bucket, or with a pulley frame (ġabja ✓) for a few buckets at a time. **Wells only reach water in the right rock.** That ties to the world's real geology (springs and perched water above the blue clay) and the real valleys: dig in the wrong place and it stays dry.
  - **Il-ġiebja** (cistern) ✓: a dug, lined tank that **fills from rain** falling on a roof or a paved yard above it. Store winter rain and spend it in summer.
  - **Is-sienja** ✓ (animal water wheel): a donkey or mule (vanilla, with a Maltese look) walks a circle and lifts water from a well into **stone channels**. The channels water every field they reach. This is the big build that turns a farm saqwi.
  - **Stone channels and troughs:** carry water along a field edge, as on real terraced fields.
- **The first rain** (life idea 50): the first big storm of autumn resets the dry season, greens the land and starts the bagħli sowing.

**Why it's materially Maltese:** where you farm, and how you get water there, becomes the first real decision of a Maltese game. It's the decision real Maltese farmers made for a thousand years. The rubble-walled terraces and valleys of the 1:1 world become the best land, as they really are.

**Art:** well-head, pulley frame, cistern mouth, the sienja (a wooden wheel with buckets, animated, and the walking animal), stone channels, a wilted look for each saqwi crop.

## 2. The Maltese year

**Real Malta:**
- Lampuki are fished from 15 August to the end of December ✓.
- The Xwejni salt is harvested from mid-May to early September, once a week, and not after storms ✓.
- Thyme honey comes in summer and carob and eucalyptus honey in autumn ✓.
- Broad beans come in spring (kusksu) ✓. The sweets follow the church year: Carnival, Lent, St Joseph, Holy Week, Easter, November, Christmas ✓.

**In the game:** a **Maltese calendar** (life-ideas base B). Every crop, fruit, fish, flower and craft has its months.

| Season | Fields | Trees | Sea and shore | Kitchen |
|---|---|---|---|---|
| **Winter** (Dec–Feb) | bagħli crops growing; cauliflower, cabbage, kohlrabi | oranges, lemons † | | kawlata, minestra; qagħaq tal-għasel and imbuljuta at Christmas ✓ |
| **Spring** (Mar–May) | broad beans, peas, early potatoes ✓; wheat harvest from May † | loquats †, almonds † | | kusksu ✓; Lent and Easter sweets ✓ |
| **Summer** (Jun–Aug) | saqwi crops: tomatoes, marrows, melons (irrigate!) | figs †, grapes from Aug † | **salt pans** ✓; swimming season | sun-drying, kunserva ✓, ħobż biż-żejt ✓; festa qubbajt ✓; thyme honey ✓ |
| **Autumn** (Sep–Nov) | sowing bagħli after the first rain | prickly pears †, carob †, **olives (Oct–Nov)** †, grape harvest † | **lampuki** ✓ | wine pressing, olive pressing; carob honey ✓; għadam tal-mejtin in November ✓ |

- **Out of season, a crop grows slowly or not at all.** Fruit trees only fruit in their months. What you didn't preserve, you go without; that's why system 5 matters.
- **The calendar length is the owner's call** (question 1). The recommendation is an in-game Maltese year whose length players can set. The default is about 10 Minecraft days a month (a 120-day year, about 40 hours of play), with an option to follow the real date.

**Art:** almost none: a wall calendar item (life idea 54) and seasonal leaf and fruit stages on trees.

## 3. The kitchen: kenur, borma and taġen

**Real Malta:** the **kenur** ✓ was the Maltese stone (or clay) stove, carved from Maltese stone and burning wood or coal ✓. Cooks had to **fan the flames** ✓, and the stove often stood in open spaces to keep smoke out of the kitchen ✓. It was in wide use until the early 20th century ✓.

**In the game:**
- **Il-kenur** (new block, 2 wide): a limestone stove with **two or three fire holes**.
  - It burns charcoal or wood.
  - Heat rises when you **fan it** (use a palm-leaf or cane fan) and falls when you don't.
  - It smokes; built indoors without a chimney or an open side, it blackens the ceiling. That's just for look and feel, with no damage.
- **Pots and pans sit on the holes:**
  - **Il-borma** † (stew pot): put ingredients in one by one, by clicking them into the pot. **You can see what's inside**: tomato red, rabbit pieces, beans.
    - Stews need **time and the right heat**: a gentle simmer for stuffat, a quick boil for aljotta.
    - Stir with a ladle (kuċċarun †). Burn it if you leave it on full heat.
    - **One pot makes 4–6 servings,** ladled into bowls or plates. Cooking becomes a batch job for a household or a server.
  - **It-taġen** † (frying pan): fried lampuka, fenek moqli, imqaret, żeppoli, eggs. Fast and hot.
- **Plates and the table:**
  - Finished dishes can be **placed**: a pot of stuffat on the table, a plate of pastizzi, a ftira, a whole timpana, a tray of ġbejniet.
  - People eat from them in turns, and **eating at a set table with others gives the shared-table bonus** (life ideas 72, 79).
- **Maltese dishes need Maltese stations.** The kenur, the forn and the taġen make the dishes of draft 1. The vanilla furnace, smoker and campfire still cook plain meat and fish, but **can't make a Maltese dish** (question 3).
- **The crafting table only prepares** (dough, pastry, sauce, herbs, mince). It no longer makes finished dishes.

**Why it's materially Maltese:** cooking becomes something you **do** in a Maltese kitchen you built, not a crafting grid. The kitchen becomes the heart of a player's house, as it is in a Maltese house.

**Art:** kenur (with fire states), borma with visible contents (several fill and colour states), taġen, ladle, fan, plates, bowls, and **a placed model for each placeable dish** (about 15). This is the biggest art job in the mod.

## 4. Bread: from the field to the windmill to the village oven

**Real Malta:**
- **Most of Malta's windmills were built by the Knights between 1663 and 1773** to grind grain into flour ✓.
- **Ta' Kola** in Xagħra still has its sails and milling machinery ✓. **Xarolla** in Żurrieq ground grain until 1940 ✓.
- **Ħobż tal-Malti** is a sourdough of flour, starter, water and sea salt ✓. It takes **seven to eight hours** from kneading to the oven ✓ and is usually baked in **wood-fired ovens** ✓.
- Few homes had an oven, so on **Sundays families took their dish to the village baker** and collected it cooked ✓.
- Qormi was "Casal Fornaro", the bakers' village ✓, and *furnar* (baker) comes from *forn* (oven) ✓.

**In the game:**
- **No more flour from a crafting table.**
  - A **hand quern** † (two stones; a slow, early option) grinds a little flour with effort.
  - **Il-mitħna** (windmill) is the real way. It's a **player-built multiblock**: a round limestone tower with a cap and **sails that turn with the wind**.
    - The stronger and steadier the wind, the faster it grinds. On a still day it stops.
    - It follows the day's named Maltese wind (life idea 51). If the owner's **Weathery** mod is installed, it reads Weathery's real wind (an optional link, not a requirement).
    - A built mill grinds a whole cart of grain into flour and bran (bran feeds animals).
  - **Barley flour** makes a coarser, older bread † for the bagħli farmer.
- **Il-ħmira** (sourdough starter) ✓: kept alive in a jar.
  - Feed it flour and water every few days or it weakens. A strong starter makes better bread.
  - **You can give a piece of your starter to a friend**: a small, social Maltese thing.
- **Il-forn** (wood-fired oven): a **player-built domed stone oven**.
  - Fire it with bundles of wood (and dry carob or olive prunings †).
  - It heats up slowly, holds its heat for hours and cools down slowly.
  - **Hot:** bread and ftira, **a batch of up to 12 at once**. **Cooling:** the slow oven dishes (timpana, ross il-forn, baked potatoes and meat, lampuki pie).
  - A real baking rhythm: bread at dawn, the Sunday dishes as the oven cools.
- **The village baker:** a villager with a forn of their own. They bake your Sunday dish for you (life idea 80): drop it off in the morning and collect it at noon, better than your own.
- **Fresh bread is best** (system 5): crusty at dawn, fine all day, hard by the third day. Stale bread becomes breadcrumbs, pudina or soup.

**Art:** windmill parts (tower blocks, cap, **animated sails**, the millstones inside), quern, forn (dome, door, fire and heat glow states), the starter jar, the baker's peel (paddle), loaves in the oven, the baker's outfit.

## 5. The pantry: salt, sun, brine and oil

**Real Malta:**
- **The Xwejni salt pans** ✓: sea water evaporates in rock-cut pans in the hot months. The salt is **swept up on harvest days** ✓ and **stored in caves cut into the coastal rock** ✓.
- Rain stops the harvest, and **rough seas that wash over the pans ruin the brine** ✓.
- Tomatoes are salted and **sun-dried** ✓, and **kunserva** is matured in the sun ✓.
- Capers are **brined** for weeks ✓, and peppered ġbejniet are kept **in oil or vinegar** ✓.

**In the game:**
- **Freshness** (switchable). Only **fresh** food goes off: fish, meat, milk, fresh ġbejna, ricotta, bread, ripe fruit, cooked dishes.
  - It goes **fresh → old → spoiled** over a few in-game days. Spoiled food feeds animals or the compost.
  - Grain, flour, salt, oil, dried, salted, brined and bottled food **keeps**.
  - A **cool store** (a room cut into the rock or underground, like a Maltese cellar or the salt caves) slows it down a lot. Malta's limestone and caves become your fridge.
- **Il-melħa** (salt pans; new mechanic on player-cut basins):
  - Cut shallow pans into coastal rock and fill them with sea water by bucket, or from waves on low rock.
  - In the dry season, in full sun, **a crust of salt forms over a few days**. Sweep it with a **broom** for wet salt, then dry it.
  - **A storm or high waves wash the brine away** ✓, so check the sky.
  - Pans in `salina_saltworks` and the real Xwejni coast work best.
  - **Salt is needed everywhere:** bread, cheese, curing, preserving.
- **Sun-drying racks and roof trays** (new blocks):
  - Lay out salted tomatoes, figs, peppers or fish **in full sun** in the dry season, and they dry over days. Rain spoils them unless you take them in.
  - **Kunserva** is reduced in a wide tray in the sun ✓.
- **Jars** (ġarra † for oil, smaller jars for brine; new blocks):
  - Capers in brine (3 weeks ✓), cured olives, anchovies in salt, tuna in oil, peppered ġbejniet in oil ✓, pickled vegetables.
  - A jar shows a timer and is ready when it's ready.
- **Payoff:** preserved food keeps through the lean months. Many dishes need a preserved part: ftira needs capers and anchovies, ħobż biż-żejt needs kunserva.

**Why it's materially Maltese:** the summer becomes harvest and preserving season, and the coast, the roof and the rock cellar all become part of your food. That's the Maltese summer.

**Art:** salt pan texture states (water → crust → swept), broom, salt sacks, drying rack and tray with what's on them, jars in two or three sizes with contents showing, a spoiled look for fresh foods.

## 6. Cheese: ġbejniet from start to finish

**Real Malta:**
- Ġbejniet are made from milk, salt and **rennet** ✓. Since the 2025 EU protected name, the traditional **lamb rennet (tames)** is back ✓, with sheep's milk ✓.
- The curds drain in rush baskets called **qwieleb** ✓, made from dried rush stalks in three sizes ✓.
- They're dried in a **cane cage hung in the kitchen**, "a primitive fridge" ✓; builders even made special windows for drying them ✓.
- They come fresh, dried, or peppered and kept in oil or vinegar ✓.

**In the game:**
1. **Milk your sheep** (vanilla sheep become milkable; draft 1 question 1).
2. **Rennet (tames):** a by-product of lambs (see question 2). There's also a plant rennet † for those who'd rather not.
3. Warm the milk in a borma on the kenur, add rennet and salt, and the curds set.
4. Ladle the curds into **qwieleb** (rush baskets, made from rushes, simar, cut in the wetlands). They drain for a day: **fresh ġbejniet**.
5. Hang them in the **cane cage** (qafas †) **in moving air**: an open window, a roof, a breezy room. Over days they become **half-dried, then dried**. In still, damp air they turn instead, and then the only use is to pepper them ✓ (the real way to save a poor batch).
6. **Peppered ġbejniet:** dried ġbejniet + black pepper, put into a jar of oil or vinegar ✓.

- The whey left in the pot becomes **ricotta** (a second heating).

**Why it matters:** ġbejna is Malta's first protected food ✓ and is in a third of the dishes. Making it well (sheep, rushes, airflow, patience) is a proper Maltese craft and not a crafting-table click.

**Art:** qwieleb basket (empty, full), the cane cage (with 0–12 cheeses showing), cheese stages, the rennet item.

## 7. Olives and wine

**Real Malta:**
- **Roman olive presses** are found across Malta: stone olive crushers (**trapetum**), press beds, and anchor stones for lever and screw presses ✓.
- The Żejtun Roman villa was a major oil producer ✓.
- The **millenary olive trees at Bidnija** are among the oldest on the islands ✓.
- Malta's own grapes are red **Ġellewża** and white **Girgentina** ✓.

**In the game:**
- **The olive press** (multiblock): a **stone crusher** (a round stone basin with a turning crushing stone, pushed by hand or by a donkey) → paste → a **screw or lever press** with an anchor stone → oil runs into a jar.
  - The harvest comes in autumn †; old **Bidni** trees give the best oil.
  - Pomace (the leftovers) feeds animals or the forn fire.
- **Wine:**
  - Tread or press grapes in a stone or wooden press † → must.
  - Pour the must into **barrels** in a **cool cellar** and it becomes wine over in-game weeks.
  - Ġellewża (red) or Girgentina (white) depends on the vine.
  - Warmer cellars make worse wine; cool rock cellars make good wine.
- Both oil and wine are **ingredients for most Maltese dishes**, so these are long-term goals for a farm.

**Art:** crusher (animated stone), press frame with screw, anchor stone, oil jar; grape press, barrels (filling and ageing states).

## 8. Bees

**Real Malta:**
- The **Maltese honey bee** is the national insect.
- Bees were kept in **clay jar hives (qolla)** ✓, extended with an extra pot (zeida ✓). Some beekeepers thought bees did better in them because the pots stay cooler ✓.
- Hives also sat in **rock-cut or stone apiaries (miġbħa)** ✓, like the one at Xemxija, which kept colonies cool in summer and warm in winter ✓.
- Honey changes with the season: **thyme in summer, carob and eucalyptus in autumn** ✓.

**In the game:**
- **Il-qolla** (clay hive; a new block): placed on its side, stacked in a wall. Add a **zeida** pot for more honey.
- **Il-miġbħa** (apiary): a stone wall or rock face with hive niches. Hives inside it **don't suffer in the summer heat or winter cold**; hives in the open give less honey in July and August.
- **The honey is named for what the bees fed on:**
  - **thyme honey** in summer near the garrigue: the best;
  - **carob honey** in autumn near carob trees;
  - **sulla and clover honey** in spring by the fields.
- Each honey suits different sweets and remedies.
- **Oriental hornets** (content list) raid hives from late spring. A **merill** or bee-eater nearby keeps them away (the "worth more alive" rule).

**Art:** qolla (plain, with zeida, full), the miġbħa wall, three honey colours, honeycomb.

## 9. The sea's food

**Real Malta:**
- Maltese fishermen use **cane and wicker traps (nassa)** ✓:
  - the **nassa tal-arznell** of fine cane strips for picarel, **used only on Gozo** ✓, set in the afternoon and lifted after four or five hours ✓;
  - the **nassa tal-qarnit** for octopus, left in the water ✓;
  - the **nassa tal-vopi** for bogue ✓.
- **Kannizzati** ✓ are rafts with **palm fronds** tied to a float and **anchored with limestone**. They draw the lampuki in season ✓, and the method has barely changed since Roman times ✓.

**In the game:**
- **Nassa** (new blocks, woven from cane, the qasba):
  - Drop one onto the seabed with bait and come back hours later.
  - **The kind of trap decides the catch:** arznell for picarel (Gozo waters), qarnit for octopus, vopi for bogue.
  - Lost traps happen in storms.
- **Kannizzati:**
  - Build a raft (a float, palm fronds and a limestone anchor) and set it offshore from **15 August**.
  - Over days, **a shoal of lampuki gathers in its shade**, and you net them.
  - It does nothing out of season.
  - This turns autumn into a real fishing season with its own work.
- Rod fishing gives the right **Maltese fish for the biome**: Posidonia meadows, rocky shore, deep water, the Dwejra waters (the world's own sea biomes).
- Boats (luzzu, kajjik) belong to the Maltese life ideas.

**Art:** three nassa models (with fish inside), the kannizzata raft, a net, palm fronds.

## 10. Eating well

**Real Malta:** a small island's cooking that turns a few things into a lot: bread, oil, beans, vegetables, fish, a little meat, cheese.

**In the game:**
- **Each food belongs to one or two groups:** bread and grain, pulses, vegetables, fruit, fish, meat, cheese, oil, sweets.
- **A varied diet over your last ~20 meals** gives a lasting bonus, **"Mitmugħ tajjeb" †** ("well fed"):
  - more maximum health, faster healing and a little extra saturation;
  - the more groups, the bigger the bonus.
- **Eating the same thing over and over feeds less each time** (it recovers after a while).
- **Big Maltese dishes count as several groups at once:** stuffat tal-fenek is meat, vegetables and oil. That's why cooking properly is worth it.
- **Eating together** at a set table (system 3) adds to it.
- With this switched off, food works as in draft 1.

**Art:** none, apart from an effect icon or two.

---

## How draft 1 changes

| Draft 1 | Draft 2 |
|---|---|
| "No new machines": furnace, smoker, campfire, crafting table | **New Maltese stations:** kenur and borma/taġen, forn, mitħna, olive press, wine press and barrels, salt pans, drying racks, jars, cheese cage, beehives |
| Soups crafted in a bowl on the crafting table | Cooked in a borma on the kenur, 4–6 servings |
| Oven dishes in the furnace | In the forn as it cools, or with the village baker |
| Flour from wheat on the crafting table | Hand quern (slow) or the windmill |
| Sea salt from a cauldron in daylight | Salt pans on the coast, in summer |
| Ġbejniet: milk + salt on the crafting table | The full cheese making of system 6 |
| Wine: grapes + bottle on the crafting table | Press, then barrels in a cool cellar |
| Food values only | + seasons, freshness, the diet bonus, the shared table |

**The dishes, crops and ingredients of draft 1 stay as they are.** Their "made in" column now points to the stations above.

## Art, all together

| Kind | Count (about) | Biggest items |
|---|---|---|
| **Multiblock builds** | 5 | windmill (animated sails), forn, sienja (animated wheel and animal), olive press (animated stone), salt pans |
| **Station blocks** | ~15 | kenur, borma, taġen, jars, barrels, drying rack, cane cage, qwieleb, qolla, miġbħa, nassa ×3, kannizzata, well-head |
| **Placed dish models** | ~15 | pot of stuffat, plate of pastizzi, ftira, timpana, ross il-forn, lampuki pie, ġbejniet tray… |
| **Items** | ~170 | draft 1's ~140 plus tools (fan, ladle, broom, peel), honeys, rennet, starter |
| **Crop and tree stages** | 19 crops + wilted looks; seasonal fruit on 9 trees | |

This is a big mod. That's why the work is cut into **phases** that can each be played on their own.

## Phases (a suggested order; the owner decides)

| Phase | Name | Systems | Playable result |
|---|---|---|---|
| **1** | **Il-Kċina** (the kitchen) | 3, plus the forn of 4, the tier A dishes | Cook Maltese food in a Maltese kitchen; bread from the forn |
| **2** | **L-Għalqa** (the field) | 1, 2 | The dry island and the Maltese year; the saqwi/bagħli choice |
| **3** | **Il-Kantina** (the pantry) | 5, 6 | Freshness, salt pans, drying, jars, ġbejniet |
| **4** | **Il-Mitħna** (mills and presses) | the windmill of 4, plus 7, 8 | Windmills, the olive press, wine, bees |
| **5** | **Il-Baħar** (the sea) | 9 | Traps and lampuki rafts |
| **6** | **L-Ikla** (the meal) | 10, plus the tier B and C dishes | The diet bonus, the full catalogue |

---

## Questions for the owner

1. **The calendar** (this now drives systems 1, 2, 5, 8 and 9): an in-game Maltese year with a length players can set, default about 120 Minecraft days (recommended)? Or the real date? Or both as a choice?
2. **Rennet from lambs:** in reality tames comes from young lambs ✓. Include it (it's real and makes sheep farming matter), offer a plant rennet † as the alternative, or both (recommended)?
3. **Vanilla stations and Maltese dishes:** Maltese dishes **only** on the Maltese stations (recommended; it's what makes the kitchen matter)? Or also on vanilla stations, at a lower value?
4. **Freshness:** on by default, or off by default for a gentler game? (Recommended: on, with a slow default.)
5. **The dry island in other worlds:** systems 1 and 2 only in the Malta world's `maltamc:*` biomes (recommended), or in any world?
6. **Weathery:** let the windmill (and the salt pans' storms) read Weathery's wind and weather when it's installed (recommended), or keep the mods apart?
7. **Where to start:** phase 1 (the kitchen) as suggested, or another phase first?
8. **The first draft's 8 questions** ([[Food design#12. Questions for the owner]]) still stand. Questions 1, 4 and 5 there now overlap with 2, 1 and 3 here.

---

## Sources checked this session (2026-11-17)

- Kenur: [Guide Me Malta, the legacy of the kenur](https://www.guidememalta.com/en/the-legacy-of-the-kenur-a-maltese-traditional-stone-stove-that-serves-as-a-culinary-relic); [Central Bank of Malta, kenur coin](https://www.centralbankmalta.org/1972-kenur-stone-stove); [University of Malta OAR 46534](https://um.edu.mt/library/oar/handle/123456789/46534)
- Windmills: [Guide Me Malta, Xarolla](https://www.guidememalta.com/en/still-standing-strong-spotlight-on-malta-and-gozo-s-only-functioning-windmill-xarolla); [Guide Me Malta, inside Malta's old windmills](https://www.guidememalta.com/en/a-journey-back-in-time-a-rare-look-inside-malta-s-old-windmills); [Ta' Kola Windmill (Google Arts & Culture)](https://artsandculture.google.com/partner/ta-kola-windmill)
- Water, saqwi and bagħli: [Hydria Project, Maltese water galleries](https://hydriaproject.info/en/case-studies/the-late-medieval-water-galleries-in-malta-11th-to-16th-century-ad/waterworks); [CIHEAM paper on Maltese irrigation](https://ressources.ciheam.org/ressources/om/pdf/a83/00800928.pdf); [Agriculture in Malta (Wikipedia)](https://en.wikipedia.org/wiki/Agriculture_in_Malta); [Malta's underground water world (UM)](https://www.um.edu.mt/library/oar/bitstream/123456789/110644/1/Maltas_underground_water_world.pdf)
- Bread and the oven: [National Geographic, Maltese bread](https://www.nationalgeographic.com/travel/article/breaking-bread-dining-maltese-bread-centre-stage); [Saveur, Savoring Malta](https://www.saveur.com/article/Travels/Savoring-Malta/); [Guide Me Malta, wood-fired bakeries](https://www.guidememalta.com/en/these-traditional-wood-fired-oven-bakeries-in-malta-will-make-your-mouth-water); [Maltese bread (Wikipedia)](https://en.wikipedia.org/wiki/Maltese_bread)
- Salt: [Guide Me Malta, Leli tal-Melħ and Xwejni](https://www.guidememalta.com/en/exclusive-the-story-of-leli-tal-melh-the-iconic-xwejni-salt-pans-in-gozo); [Euronews, salt harvesting family](https://www.euronews.com/2018/10/05/maltese-family-keeps-ancient-salt-harvesting-tradition-alive); [University of Malta, Salt pans 2025](https://www.um.edu.mt/library/oar/bitstream/123456789/132226/1/Salt%20pans%202025.pdf)
- Cheese: [MaltaToday, Gozo ġbejniet](https://www.maltatoday.com.mt/gourmet/other/12079/little-cheese-from-the-gozitan-shores-gozo-gbejniet); [EU protected designation 2025](https://malta.representation.ec.europa.eu/news/gbejna-tan-naghag-first-maltese-food-be-registered-geographical-indication-protected-designation-2025-01-28_fi); [Guide Me Malta, the cane cage (in the windmills article)](https://www.guidememalta.com/en/a-journey-back-in-time-a-rare-look-inside-malta-s-old-windmills); [The folklore of an island (UM, 1995)](https://www.um.edu.mt/library/oar/bitstream/123456789/47652/1/The_folklore_of_an_island_1995.pdf)
- Olives: [University of Malta OAR 103211, Roman olive processing](https://um.edu.mt/library/oar/handle/123456789/103211); [Wirt iż-Żejtun, olive cultivation in Roman Malta](https://wirtizzejtun.com/perspectives-on-olive-cultivation-and-processing-in-maltese-roman-antiquity/); [THINK, the Roman villa of Żejtun](https://thinkmagazine.mt/the-roman-villa-of-zejtun/)
- Bees: [Bees for Development Journal 78 (2006)](https://issuu.com/beesfd/docs/78_bfdj_mar2006/6); [Operaipogea 2002, the Xemxija apiary](https://www.operaipogea.it/wp-content/uploads/2002/12/OpIp-03_2002-2-ApicultMalta-pr.pdf); [Guide Me Malta, Maltese honey](https://www.guidememalta.com/en/sweet-as-honey-the-story-of-malta-s-liquid-gold); [Welcome Center Malta, seasonal honey](https://www.welcome-center-malta.com/honey-sea-salt-and-history-gourmet-gifts-from-the-maltese-islands)
- Fishing: [FAO, nassa tal-arznell](https://www.fao.org/fishery/docs/CDrom/ARTFIMED/ArtFiWeb/mlt/metiers/docs\MLTMGA10.doc); [FAO, nassa tal-qarnit](https://www.fao.org/fishery/docs/CDrom/ARTFIMED/ArtFiWeb/mlt/metiers/docs\MLTMMA04.doc); [FAO, nassa tal-vopi](https://www.fao.org/fishery/docs/CDrom/ARTFIMED/ArtFiWeb/mlt/metiers/docs\MLTGNE03.doc); [Lampuki netting (Wikipedia)](https://en.wikipedia.org/wiki/Lampuki_netting)
- The food sources behind the dishes are listed in [[Food design]].
