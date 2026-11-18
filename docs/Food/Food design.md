---
type: "list"
date: "2026-11-17"
status: "open"
---
# Food design (draft 1, 2026-11-17)

**State:** the art for 24 of these dishes, the lampuka, the three ġbejniet and Kinnie is in the mod; nothing else is drawn, and no gameplay (recipes, food values, cooking) is built. [[Food progress]] shows what's done and what isn't, with a picture of each. Building gameplay waits for the owner's go-ahead.

> **2026-11-17, draft 2:** the owner asked to go bigger ([[2026-11-17 Food – go bigger, new art and systems, a materially Maltese change]]). This note is now **the catalogue** (crops, ingredients, dishes, values). The "no new machines" and low-art rules below are **dropped**, and the "made in" columns now point to the Maltese stations in **[[Food systems]]**, which explains how each one changes.

This is the food part of the **layer 2 add-on mod** ([[2026-11-15 Three layers – vanilla world, add-on mod, overhaul later|the owner's three layers]]). It refines and replaces section 10 ("Food") and section 8c ("Crops") of [[Content mod list]]. The animals, wild plants and trees stay in that list; here they appear only as food sources.

Marks used below:
- **✓** = checked against sources this session (listed at the end).
- **†** = from general knowledge of Maltese food, not yet checked against a source.

---

## 1. Design rules

1. **Maltese first, vanilla where it fits.** Vanilla is used where Malta really uses that thing:
   - rabbit, pork, beef, chicken, eggs, milk, wheat, potato, carrot, pumpkin, melon, honey, sugar.
   - Nothing vanilla is renamed or replaced. Vanilla bread and rabbit stew stay as they are; the Maltese versions are new items next to them.
2. **No new machines.** Everything is made with:
   - the crafting table: preparing and assembling;
   - the furnace, smoker or campfire: cooking, baking and drying;
   - the cauldron: sea salt;
   - bowls, glass bottles and buckets, as in vanilla.
3. **Every recipe fits the 3×3 grid.** Long ingredient lists are made shorter by a few base ingredients (section 5), the way real Maltese cooks start most dishes from the same sauce.
4. **Raw → ingredient → dish.** The more work a food takes, the more it feeds. A dish is always better than its parts eaten one by one.
5. **Effects are rare and gentle.** Most food only feeds. A few dishes have one mild vanilla effect that suits them (section 9). There are no custom effects in the first version.
6. **The world is never touched.**
   - Seeds and wild foods drop from vanilla grass, bushes and leaves in the world's own `maltamc:*` biomes.
   - Fish and animals spawn while you play.
   - Crops and trees grow only where players plant them.
7. **Names:** the item shows the **Maltese name**, and the tooltip shows the English. For example, *Stuffat tal-Fenek* with "Rabbit stew" underneath. This ties to life-ideas question 3 (how much Maltese).

---

## 2. What vanilla gives us (used as is)

| Vanilla | Maltese use |
|---|---|
| **Rabbit** (raw / cooked, hide) | The national dish: stuffat tal-fenek, fenek moqli, the fenkata ✓. Wild rabbits already live in the garrigue. |
| Porkchop | Maltese sausage, kawlata, mince for ross il-forn and timpana |
| Beef | Laħam fuq il-fwar ✓, braġjoli, mince |
| Chicken, egg | Brodu (broth), and egg in almost every baked dish |
| Milk bucket | Ricotta, butter. Ġbejniet need sheep's milk (section 4). |
| Wheat | Flour, the start of all bread and pastry |
| Potato | Patata il-forn, ftira, stews. Malta grows early potatoes for export ✓. |
| Carrot | Kawlata ✓, lampuki pie ✓, broth |
| Pumpkin (qargħa ħamra) | Minestra ✓ |
| Melon slice | Dulliegħ (watermelon), the summer beach fruit |
| Honey bottle, bee | Honey. Thyme and carob honey are added as variants (section 4). |
| Sugar (from sugar cane / qasba) | Every sweet |
| Cocoa beans | Kannoli, imbuljuta, pudina. Malta has no jungle, so cocoa comes as an import (section 6). |
| Cod | Stands for hake (merluzz). Counts as "any fish" in aljotta. |
| Squid | The mod adds a **raw squid** meat drop for klamari mimlija. |
| Sweet berries | Blackberries (għollieq), eaten raw |
| Bowl, glass bottle, bucket | Soups, drinks, sauces, milk |

**Not used:** salmon, tropical fish, kelp, glow berries, chorus fruit, beetroot soup and mushroom dishes. Malta has no documented edible wild mushrooms ✓, so mushrooms play no part.

---

## 3. Crops (new)

Each crop is a vanilla-style farmland crop with 4 growth stages and one 16×16 produce item. **Seeds** come from breaking grass in the farming biomes, the way grass drops wheat seeds.

| # | Crop | Maltese | Seeds from (biome) | Gives | Used in | Tier |
|---|---|---|---|---|---|---|
| C1 | **Tomato** | Tadam | `ghelieqi_fields`, `wied_garden` | tomatoes | kunserva ✓, zalza, ħobż biż-żejt, nearly every stew | A |
| C2 | **Onion** (flat Maltese onion) | Basal | `ghelieqi_fields` | onions | most savoury dishes | A |
| C3 | **Garlic** | Tewm | `ghelieqi_fields` | garlic | aljotta ✓, arjoli ✓, bebbux ✓, bigilla | A |
| C4 | **Broad bean** | Ful | `ghelieqi_fields` | beans | bigilla, kusksu ✓ | A |
| C5 | **Pea** | Piżelli | `ghelieqi_fields` | peas | pastizzi, stuffat, soppa tal-armla | A |
| C6 | **Grapevine** | Dielja † | `vinja_vineyard` (cuttings) | grapes (red Ġellewża, white Girgentina ✓) | wine, raisins | A |
| C7 | Round marrow | Qargħa bagħli | `ghelieqi_fields`, `wied_garden` | marrows | qarabagħli mimli, minestra ✓ | B |
| C8 | Cauliflower | Pastard | `ghelieqi_fields` | cauliflower | lampuki pie ✓, soppa tal-armla | B |
| C9 | **Cabbage** (new to the list) | Kaboċċa | `ghelieqi_fields` | cabbage | kawlata ✓ | B |
| C10 | Kohlrabi | Gidra | `ghelieqi_fields` | kohlrabi | kawlata ✓, soppa tal-armla | B |
| C11 | Artichoke | Qaqoċċ | `wied_garden` | artichokes | qaqoċċ mimli | C |
| C12 | Aubergine | Brunġiel † | `wied_garden` | aubergines | kapunata | B |
| C13 | Sweet pepper | Bżar aħdar † | `wied_garden` | peppers | kapunata | B |
| C14 | Spinach | Spinaċi † | `wied_garden` | spinach | qassatat, lampuki pie ✓ | C |
| C15 | Herbs: **basil, mint, marjoram, parsley** | Ħabaq, Nagħniegħ, Merqtux, Tursin † | `gonna_gardens`, `rahal_town` | herb bunches | ħwawar (section 5). **Basil also grows in a flower pot**: the basil pot on the balcony. | B |
| C16 | Coriander (new) | Kosbor † | `ghelieqi_fields` | seeds | Maltese sausage † | C |
| C17 | Anise | Ħlewwa | `ghelieqi_fields` | seeds | imqaret, qagħaq tal-għasel, qagħaq tal-ħmira ✓ | C |
| C18 | Sesame | Ġulġlien | `ghelieqi_fields` | seeds | qagħaq tal-ħmira ✓, ħelwa tat-Tork ✓ | C |
| C19 | Cumin | Kemmun | `ghelieqi_fields`, Comino | seeds | spice; the Comino name story (unconfirmed) | C |

**Taken out of the food list:**
- **Barley** (xgħir): vanilla wheat already feeds animals.
- **Cotton:** not food; it stays in the main list.
- **Sulla:** fodder and honey only; it stays a wild plant.
- **Chickpea:** no dish needs it.

**Count:** 6 crops in tier A, 7 in tier B and 6 in tier C, with 4 growth stages each.

---

## 4. Trees, wild food, and things from animals and the sea

### 4a. Fruit and nut trees (planted by players; Maltese-shaped trees from vanilla logs and leaves)

| Tree | Maltese | Sapling from | Fruit | Tier |
|---|---|---|---|---|
| **Olive** (Bidni) | Żebbuġ | olive-grove leaves (`zebbug_olive_grove`) | olives: raw olives are bitter; cure them or press them for oil | A |
| **Carob** | Ħarrub | leaves in `xaghri_garrigue`, `wied_valley` | carob pods: a poor raw food; carob syrup; feed for animals | A |
| **Fig** | Tin | leaves in `wied_valley`, `gonna_gardens` | figs; dried figs (smoker) | A |
| **Orange** (Maltese blood orange) | Larinġ | leaves in `gonna_gardens`, `verdala_grove` | oranges, orange peel | A |
| **Lemon** | Lumi | leaves in `gonna_gardens` | lemons | A |
| **Almond** | Lewż | leaves in `ghelieqi_fields` field edges | almonds: snack, intrita, qubbajt | A |
| Pomegranate | Rummien | leaves in `gonna_gardens` | pomegranates | B |
| Mulberry | Ċawsli | leaves in `rahal_town` (farmhouse trees) | mulberries | C |
| Loquat | Naspli | leaves in `gonna_gardens` | loquats | C |

### 4b. Wild food (foraged; nothing planted in the world)

| Food | Maltese | Where | How | Tier |
|---|---|---|---|---|
| **Capers** | Kappar | `rdum_cliffs`, rubble walls, bastions | Break grass or bushes on cliffs for caper buds. A caper cutting planted on stone grows a bush that sits on walls. Raw buds are inedible until **brined** ✓. | A |
| **Prickly pear** | Bajtar tax-Xewk | field edges (`ghelieqi_fields`, `wied_valley`) | Eating one **unpeeled hurts** (1 damage). Peeling it on the crafting table makes it a good fruit. Pads can be planted as a hedge. | A |
| **Wild fennel** | Busbież | field edges, roadsides | fennel fronds and seeds: snails, sausage, roast potatoes † | A |
| Thyme | Sagħtar | `xaghri_garrigue` | Herb. **Bees near thyme make thyme honey** ✓. | A |
| **Snails** | Għakruxa ✓ (edible garden snail) | walls and fennel stalks **after rain** ✓ | Picked up by hand, only for a day after rain | B |
| Wild asparagus | Spraġ | garrigue, spring | foraged vegetable | C |
| Borage | Fidloqqom | fields | edible flower; borage syrup ✓ | C |
| Samphire | Busbies il-Baħar | `xatt_rocky_shore` | pickled | C |

### 4c. From animals (vanilla mobs, new drops or uses)

| Product | From | Notes | Tier |
|---|---|---|---|
| **Sheep's milk** | Vanilla sheep can now be milked with a bucket | The only milk for **ġbejniet**. Ġbejna tan-nagħaġ became Malta's first EU-protected food in 2025 ✓. | A |
| **Thyme honey** | A bee nest or hive with thyme within 8 blocks, May–Aug | Better honey: more food, and clears Poison like vanilla honey | B |
| Carob honey | A hive near carob trees, autumn ✓ | A darker variant | C |
| Squid meat | Vanilla squid | klamari mimlija | B |

### 4d. From the sea (fish come from the content list's sea-life section)

| Catch | Maltese | Raw → cooked | Notes | Tier |
|---|---|---|---|---|
| **Lampuka** | Lampuka | furnace, smoker or campfire | **Spawns only 15 Aug–31 Dec** ✓ (the real season, opening on the Santa Marija feast), offshore under floating rafts (kannizzati ✓) | A |
| **Tuna** | Tonn | big steak; preserved in oil | Feeds ħobż biż-żejt ✓ | A |
| **Sardine** and **anchovy** (two fish) | Sardina, Inċova | anchovies salted → salted anchovies | ftira ✓, arjoli ✓, qaqoċċ mimli | A |
| **Octopus** | Qarnita | stew | | A |
| **Sea bream, grouper** | Awrata, Ċerna | grilled, baked | the common table fish † | A |
| Swordfish | Pixxispad | grilled steak | | B |
| Sea urchin roe | Rizzi | raw; pasta | Gathered from urchin blocks with shears; stepping on urchins still hurts | C |
| Red mullet, mackerel | Trilja, Kavall | grilled | count as "any fish" | C |

---

## 5. Base ingredients (made, not grown)

These keep the dish recipes inside the 3×3 grid.

| Ingredient | Maltese | Recipe → where | Notes |
|---|---|---|---|
| **Sea salt** | Melħ | water cauldron + daylight → salt crust (in about 1 Minecraft day) | **Twice as fast in `salina_saltworks`** and next to the sea. The real salt pans ✓. |
| Flour | Dqiq | 1 wheat → 1 flour (table) | |
| **Dough** | Għaġina | 3 flour + water bottle + salt → 3 dough (table) | Maltese bread is sourdough ✓; a sourdough starter can come later |
| **Pastry** | Għaġina tal-pastizzi † | 2 flour + butter + water bottle → 2 pastry (table) | Real pastizzi pastry is laminated with lard ✓. Lard could be added later as a pork by-product. |
| Pasta | Għaġin | 2 flour + egg → 2 pasta (table). The shape comes from the recipe: macaroni, kusksu beads, ravjul sheets. | Kusksu beads are their own small pasta ✓ |
| Butter | Butir | milk bucket → 2 butter (table; the bucket comes back) | |
| **Ricotta** | Irkotta | milk bucket + salt → 3 ricotta (table) | Any milk |
| **Fresh ġbejna** | Ġbejna friska ✓ | **sheep's** milk bucket + salt → 4 ġbejniet (table) | Edible as is |
| Dried ġbejna | Ġbejna moxxa ✓ | fresh ġbejna → smoker (stands in for drying in the sun) | Edible; keeps |
| Peppered ġbejna | Ġbejna tal-bżar ✓ | dried ġbejna + black pepper + olive oil (table) | Edible; the best of the three |
| **Olive oil** | Żejt taż-żebbuġ | 4 olives + glass bottle → olive oil (table) | |
| Cured olives | Żebbuġ † | 3 olives + salt + water bottle → 3 cured olives | Raw olives give Hunger for 5 s (bitter) |
| **Brined capers** | Kappar | 4 caper buds + salt + water bottle → capers ✓ | |
| **Kunserva** | Kunserva ✓ | 4 tomatoes + salt → smoker → 1 jar | "The red gold of Gozo" ✓ |
| Sun-dried tomatoes | Tadam imqadded ✓ | tomatoes + salt → smoker | Salted and dried ✓ |
| **Zalza** (tomato sauce) | Zalza † | 2 tomatoes + onion + garlic + olive oil → 2 zalza (table) | **The base of most stews**, so one slot stands for four ingredients |
| **Ħwawar** (herbs) | Ħwawar † | any 2 of basil / mint / marjoram / parsley / thyme → 2 ħwawar (table) | One slot for "the herbs" |
| Mince | Laħam ikkappuljat † | 1 raw beef or porkchop → 2 mince (table) | |
| Breadcrumbs | Frak tal-ħobż † | stale Maltese bread → 3 breadcrumbs (table) | A use for old bread |
| Anchovies | Inċova | 3 anchovies + salt → 3 salted anchovies (table); the anchovy is its own fish, not the sardine (owner 2026-11-18) | |
| Tuna in oil | Tonn fiż-żejt † | cooked tuna + olive oil + glass bottle → jar (table) | |
| **Intrita** (almond paste) | Intrita ✓ | 2 almonds + sugar + egg → 2 intrita (table) | Fills figolli and għadam tal-mejtin ✓ |
| Orange peel | Qoxra tal-larinġ † | 1 orange → 2 peel (table) | |
| Raisins | Żbib † | grapes → smoker | |
| Dried figs | Tin imqadded † | figs → smoker | |
| **Carob syrup** | Ġulepp tal-ħarrub ✓ | 3 carob pods + sugar + water bottle → furnace | Also a drink (section 8) |
| Brodu (broth) | Brodu † | cooked chicken + carrot + onion + water bottle + bowl → bowl of broth (table) | Edible too (section 8) |

**About 26 base ingredients.** The lightest ones (flour, butter, mince, peel) could be cut if art time is short.

---

## 6. Imported goods (owner decision 2026-11-15: from the wandering trader and shipwreck chests)

| Good | Maltese | Used in |
|---|---|---|
| Rice | Ross | ross il-forn, aljotta ✓ |
| Black pepper | Bżar | ġbejna tal-bżar ✓, sausage |
| Dates | Tamal † | imqaret |
| Cloves | Qronfol † | qagħaq tal-għasel, imbuljuta ✓ |
| Cinnamon (new) | Kannella † | kwareżimal ✓, imbuljuta ✓ |
| **Dried chestnuts** (new) | Qastan ✓ | imbuljuta ✓ |
| **Cocoa** (vanilla) | Kawkaw † | kannoli, imbuljuta ✓, pudina. The trader sells vanilla cocoa beans. |
| Tea (new) | Te | tea in a glass (life idea 81, the kiosk) |

- **Shipwreck chests** are filled when first opened, so the mod adds these at play time without touching the world.
- **The wandering trader** sells 2–3 of them at a time.
- Later, a grocer villager (tal-ħanut) from the life ideas could sell them too.

---

## 7. Dishes

**Food** is in hunger points (2 points = one drumstick). **Sat** is the saturation band:

| Band | Vanilla modifier | Vanilla example |
|---|---|---|
| Low | 0.3 | cookie, pumpkin pie |
| Normal | 0.6 | bread, baked potato, cooked rabbit |
| Good | 0.8 | cooked beef, cooked porkchop |
| High | 1.0 | between steak and golden carrot |

The best vanilla meal is rabbit stew (10, Normal). Big Maltese dishes go a little above it because they take more work.

**Placeable** = a block set on a table and eaten in slices, like cake. Several people can eat from one dish, which fits the shared table and the fenkata in the life ideas (72, 79).

### 7a. Bread and pastry

| # | Dish | English | Recipe → where | Food / Sat | Extra | Tier |
|---|---|---|---|---|---|---|
| D1 | **Ħobż tal-Malti** ✓ | Maltese bread | dough → furnace | 6 / Good | Crusty round sourdough loaf ✓. Goes **stale** after 3 days (later; life idea 82): stale bread becomes breadcrumbs or pudina. | A |
| D2 | **Ħobż biż-żejt** ✓ | Bread with oil | Maltese bread + kunserva + olive oil + tomato + capers + cured olives (+ tuna in oil: second recipe, +2 food) → table | 10 / Good | The summer beach food ✓ | A |
| D3 | **Ftira Għawdxija** ✓ | Gozo ftira | dough + potato + fresh ġbejna + onion + cured olives + capers + anchovies → raw ftira → furnace | 11 / Good | Potato and ġbejna are the signature ✓. Gozo only? (question 7) | A |
| D4 | **Pastizzi tal-irkotta** ✓ | Ricotta pastizzi | pastry + ricotta → 2 raw → furnace | 4 / Normal | Stack to 64, cheap, the morning snack | A |
| D5 | **Pastizzi tal-piżelli** ✓ | Pea pastizzi | pastry + peas + onion → 2 raw → furnace | 4 / Normal | | A |
| D6 | Qassatat ✓ | Round pastry | pastry + ricotta or peas + spinach → 2 raw → furnace | 5 / Normal | The round, sealed cousin of the pastizz ✓ | C |
| D7 | Galletti † | Water crackers | 2 flour + water bottle + salt → 4 → furnace | 2 / Low | **Never spoils**: sea and travel food. Eaten with bigilla. | B |
| D8 | Qagħaq tal-ħmira ✓ | Aniseed sesame buns | dough + anise + sesame + sugar → 3 → furnace | 4 / Normal | | C |
| D9 | Qagħqa tal-appostli ✓ | Apostles' ring | dough + almonds + anise → furnace | 6 / Normal | Holy Week ✓ | C |

### 7b. Dips and small plates

| # | Dish | English | Recipe → where | Food / Sat | Extra | Tier |
|---|---|---|---|---|---|---|
| D10 | **Bigilla** † | Broad bean dip | 2 broad beans + garlic + olive oil + ħwawar + bowl → table | 5 / Normal | | A |
| D11 | Arjoli ✓ | Arjoli dip | breadcrumbs + garlic + ħwawar + cured olives + anchovies + capers + olive oil + bowl → table | 5 / Normal | Served with snails ✓ | C |
| D12 | **Ġbejniet** ✓ | Cheeselets | (see section 5) | fresh 2 / Low, dried 3 / Normal, peppered 3 / Good | | A |
| D13 | Patata il-forn † | Maltese roast potatoes | 2 potatoes + onion + fennel + olive oil → raw tray → furnace | 7 / Good | | B |
| D14 | Stuffat tal-bebbux ✓ | Snail stew | 2 snails + garlic + zalza + wine + ħwawar + bowl → table | 7 / Good | After rain only (the snails) ✓ | B |

### 7c. Soups (crafted in a bowl, like vanilla stews)

| #   | Dish                  | English                    | Recipe → where                                                                    | Food / Sat | Extra                                   | Tier |
| --- | --------------------- | -------------------------- | --------------------------------------------------------------------------------- | ---------- | --------------------------------------- | ---- |
| D15 | **Aljotta** ✓         | Fish soup                  | 2 any fish + garlic + zalza + rice + lemon + ħwawar (marjoram ✓) + bowl → table   | 8 / Good   | Regeneration I, 5 s. The Lenten soup ✓. | A    |
| D16 | **Soppa tal-armla** ✓ | Widow's soup               | kohlrabi + cauliflower + peas + potato + fresh ġbejna + egg + bowl → table        | 9 / Good   | Regeneration I, 5 s                     | B    |
| D17 | Minestra ✓            | Vegetable soup             | pumpkin + potato + marrow + onion + zalza + pasta + bowl → table                  | 9 / Good   | Regeneration I, 5 s; winter             | B    |
| D18 | **Kawlata** ✓         | Cabbage and pork soup      | cabbage + porkchop or sausage + potato + kohlrabi + carrot + onion + bowl → table | 10 / Good  | Regeneration I, 5 s; winter ✓           | B    |
| D19 | Kusksu ✓              | Kusksu and broad bean soup | kusksu pasta + 2 broad beans + zalza + fresh ġbejna + egg + bowl → table          | 8 / Good   | Spring (fresh beans ✓)                  | B    |
| D20 | Brodu †               | Chicken broth              | (section 5)                                                                       | 6 / Normal | Regeneration I, 5 s                     | B    |

### 7d. Meat

| #   | Dish                    | English                         | Recipe → where                                                                                  | Food / Sat                           | Extra                                                    | Tier |
| --- | ----------------------- | ------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------ | -------------------------------------------------------- | ---- |
| D21 | **Stuffat tal-fenek** ✓ | Rabbit stew (the national dish) | cooked rabbit + zalza + wine + potato + peas + garlic + bowl → table                            | 12 / High                            | Absorption I, 60 s. **The best food in the mod.**        | A    |
| D22 | Fenek moqli ✓           | Fried rabbit                    | raw rabbit + garlic + wine + olive oil → marinated → furnace                                    | 8 / Good                             | The fenkata's second course                              | B    |
| D23 | **Zalzett tal-Malti** † | Maltese sausage                 | 2 mince (pork) + salt + black pepper + coriander + garlic + ħwawar → 3 raw → smoker             | 6 / Good                             | **Kawlata, ftira**                                       | B    |
| D24 | Laħam fuq il-fwar ✓     | Steamed beef                    | raw beef + garlic + ħwawar + olive oil + lemon → smoker                                         | 8 / Good                             | Traditionally steamed over a pot of soup ✓; Sunday lunch | B    |
| D25 | Braġjoli †              | Beef olives                     | raw beef + mince + egg + breadcrumbs + ħwawar + zalza → furnace                                 | 9 / Good                             |                                                          | C    |
| D26 | **Ross il-forn** †      | Baked rice                      | rice + 2 mince + 2 egg + zalza + dried ġbejna → raw dish → furnace                              | **placeable, 6 slices × 4 / Normal** | The Sunday baker's oven dish (life idea 80)              | A    |
| D27 | **Timpana** †           | Pastry-cased macaroni           | 2 pastry + macaroni + 2 mince + zalza + 2 egg → raw dish → furnace                              | **placeable, 6 slices × 5 / Normal** |                                                          | A    |
| D28 | Mqarrun il-forn †       | Baked macaroni                  | macaroni + 2 mince + zalza + 2 egg + dried ġbejna → raw dish → furnace                          | placeable, 6 slices × 4 / Normal     | Timpana without the pastry                               | B    |
| D29 | Ravjul ✓                | Maltese ravioli                 | ravjul pasta + ricotta + parsley + egg → 4 raw ravjul; then 4 raw ravjul + zalza + bowl → table | 8 / Good                             |                                                          | B    |
| D30 | Qarabagħli mimli †      | Stuffed marrows                 | 2 marrows + mince + egg + dried ġbejna + breadcrumbs → furnace                                  | 7 / Good                             |                                                          | B    |
| D31 | Qaqoċċ mimli †          | Stuffed artichokes              | artichoke + breadcrumbs + cured olives + capers + garlic + anchovies → furnace                  | 6 / Good                             |                                                          | C    |
| D32 | Kapunata †              | Kapunata                        | aubergine + pepper + zalza + capers + cured olives + bowl → table                               | 7 / Good                             |                                                          | B    |

### 7e. Fish and sea

| # | Dish | English | Recipe → where | Food / Sat | Extra | Tier |
|---|---|---|---|---|---|---|
| D33 | **Lampuka moqlija** ✓ | Fried lampuka | raw lampuka → furnace / campfire | 6 / Good | Autumn only, because the fish are ✓ | A |
| D34 | **Torta tal-lampuki** ✓ | Lampuki pie | 2 pastry + 2 lampuka + cauliflower or spinach + cured olives + zalza + carrot + capers → raw pie → furnace | **placeable, 6 slices × 5 / Good** | Ingredients from real recipes ✓ | A |
| D35 | **Stuffat tal-qarnit** † | Octopus stew | octopus + zalza + cured olives + capers + wine + potato + bowl → table | 10 / Good | | A |
| D36 | Ħut il-forn † | Baked fish and potatoes | bream or grouper + 2 potatoes + zalza + garlic + olive oil → furnace | 9 / Good | | B |
| D37 | Klamari mimlija † | Stuffed squid | raw squid + breadcrumbs + cured olives + capers + egg + ħwawar → furnace | 7 / Good | | B |
| D38 | Pixxispad † | Grilled swordfish | swordfish steak → campfire; + lemon + olive oil → table | 7 / Good | | B |
| D39 | Għaġin bir-rizzi † | Sea urchin pasta | pasta + 2 urchin roe + garlic + olive oil + bowl → table | 7 / Good | Water Breathing, 30 s | C |

### 7f. Sweets (each tied to its time of year)

| # | Dish | English | Recipe → where | Food / Sat | When ✓ | Tier |
|---|---|---|---|---|---|---|
| D40 | **Imqaret** † | Date pastries | pastry + 2 dates + anise + orange peel → 3 raw → furnace | 3 / Low | all year, street stalls | A |
| D41 | **Qagħaq tal-għasel** ✓ | Honey (treacle) rings | dough + honey + orange peel + anise + cloves → 3 → furnace | 4 / Low | **Christmas** | A |
| D42 | **Kannoli** † | Kannoli | pastry + 2 ricotta + sugar + cocoa + orange peel → 3 → furnace | 4 / Normal | all year | A |
| D43 | Figolla ✓ | Easter almond biscuit | 2 pastry + intrita + sugar + egg → furnace | 6 / Normal | **Easter**; lamb or fish shape ✓ (2 textures) | B |
| D44 | Kwareżimal ✓ | Lent almond biscuits | 2 almonds + honey + flour + orange peel + cinnamon → 4 → furnace | 3 / Normal | **Lent**: no eggs or butter, soaked in honey ✓ | C |
| D45 | Karamelli tal-ħarrub ✓ | Carob sweets | carob syrup + sugar → 4 → furnace | 1 / Low | **Lent** | B |
| D46 | **Qubbajt** ✓ | Nougat | 2 almonds + honey + carob syrup + sugar → 4 (table) | 3 / Low | **Summer festa**: "a festa without qubbajt isn't a festa" ✓ | B |
| D47 | Ħelwa tat-Tork ✓ | Sesame halva | 2 sesame + sugar + almonds → 4 (table) | 3 / Low | all year | C |
| D48 | Għadam tal-mejtin ✓ | "Bones of the dead" | pastry + intrita + sugar → 3 → furnace | 3 / Low | **November** (All Souls) ✓ | C |
| D49 | Prinjolata ✓ | Carnival cake | 2 galletti + 2 egg + sugar + cocoa + sweet berries + almonds → furnace | placeable, like cake | **Carnival** ✓ | C |
| D50 | Żeppoli ✓ | St Joseph's fritters | flour + egg + butter + ricotta + sugar → 3 → furnace | 4 / Normal | **19 March** ✓ | C |
| D51 | Pudina tal-ħobż † | Bread pudding | stale bread + egg + milk + sugar + cocoa + raisins → furnace | placeable, 4 slices × 4 | all year; uses up old bread | C |

**Sweets give Speed I for 10 s** (sugar). Eating several in a row doesn't stack it.

---

### 7g. Added from the owner's list (2026-11-17, ideas only)

The owner pasted a list of Maltese dishes and asked to add the ones not yet here, leaving out the egg dishes, the other ġbejniet and the drinks (except Kinnie, in section 8). Recipes, food values and tiers aren't designed yet. Names are as the owner gave them, from a list of Maltese foods.

| # | Dish | English | Kind | Notes | Tier |
|---|---|---|---|---|---|
| D52 | Żebbuġ mimli | Stuffed olives | small plate | green olives stuffed with a tuna mixture | - |
| D53 | Fażola bajda bit-tewm u t-tursin | White beans with garlic and parsley | small plate | dressed with olive oil | - |
| D54 | Għaġin grieg | "Greek pasta" | pasta | small pasta beads with minced pork and cheese | - |
| D55 | Spagetti biz-zalza tal-fenek | Spaghetti with rabbit sauce | pasta | the fenkata's first course, before the stuffat | - |
| D56 | Falda mimlija | Stuffed flank of pork | meat | | - |
| D57 | Mazzit | Maltese blood sausage | meat | | - |
| D58 | Qarnit bit-tewm | Octopus with garlic | fish and sea | | - |
| D59 | Bżar mimli | Stuffed peppers | vegetables | | - |
| D60 | Tadam mimli | Stuffed tomatoes | vegetables | a cold summer dish: tomatoes filled with rice salad, mayonnaise, olives and capers | - |
| D61 | Torta tal-irkotta | Ricotta pie | savoury pastry | could be a placed dish eaten in wedges, like the torta tal-lampuki | - |
| D62 | Sfineġ | Fritters | savoury pastry | vegetable, fish or cheese | - |
| D63 | Torta tar-ross u l-qargħa ħamra | Rice and pumpkin pie | savoury pastry | | - |
| D64 | Ravjul moqli | Sweet fried ravioli | sweet | | - |
| D65 | Torta tal-marmorat | Almond and chocolate pie | sweet | | - |
| D66 | Ftira tar-Randan | Lenten fried pastry squares with honey | sweet | **Lent** | - |
| D67 | Ħobża ta' San Martin | St Martin's sweet bread roll | sweet | sweetened with mastic; **St Martin's Day** (11 November) | - |
| D68 | Ġelat Malti (ġelat tan-nanna) | Maltese ice cream | sweet | condensed milk, cinnamon, nuts and candied peel | - |
| D69 | Dip tal-ġbejna | Ġbejna dip | dip | peppered dried ġbejna blended with cream cheese, olive oil, garlic and parsley; with galletti (a modern recipe) | - |
| D70 | Dip tat-tonn † | Tuna dip | dip | named as a Maltese classic with no recipe found; tuna also goes into arjoli and żebbuġ mimli | - |
| D71 | Dip tat-tewm † | Garlic dip | dip | named as a Maltese classic with no recipe found | - |

## 8. Drinks

| # | Drink | English | Recipe → where | Effect | Tier |
|---|---|---|---|---|---|
| X1 | **Inbid** ✓ | Wine: red Ġellewża, white Girgentina | 3 grapes + glass bottle → table | Mostly a cooking ingredient. Drinking it gives 2 food and no drunk effect (question 3). | B |
| X2 | **Ġulepp tal-ħarrub** ✓ | Carob syrup | (section 5) | **A remedy:** clears Poison and Hunger, the way it was used for coughs † | B |
| X3 | **Imbuljuta tal-qastan** ✓ | Chestnut and cocoa drink | dried chestnuts + cocoa + sugar + cloves + orange peel + bowl → table | Regeneration I 10 s, and **clears freezing** (Ta' Dmejrek's snowfields). **Christmas Eve** ✓ | B |
| X4 | Likur tal-bajtar ✓ | Prickly pear liqueur | 2 peeled prickly pears + sugar + glass bottle → table | 1 food; a gift item | C |
| X5 | Te † | Tea in a glass | tea + sugar + water bottle → furnace | 1 food; **doubles the food of a qagħqa tal-ħmira or galletti eaten within 10 s** (dunking ✓) | C |
| X6 | Kinnie | Maltese bittersweet soft drink | (added 2026-11-17 from the owner's list; recipe not designed) | to design | - |

---

## 9. Raw foods (eaten as they are)

| Food | Food / Sat | Note |
|---|---|---|
| Tomato, fig, grapes, orange, mulberry, loquat, pomegranate | 2–4 / Low–Normal | |
| Almonds | 2 / Normal | |
| **Peeled prickly pear** | 4 / Normal | Unpeeled: 1 damage, and it isn't eaten |
| Carob pod | 1 / Low | Poor food. People ate it in hard times † |
| Raw olives | 1 / Low | Hunger, 5 s (bitter) |
| Watermelon slice (vanilla) | vanilla | |
| Raw fish | like vanilla raw cod | Except the sea urchin roe (2 / Normal) |

---

## 10. Counts and art

| | Tier A | Tier B | Tier C | Total |
|---|---|---|---|---|
| Crops (4 stages + produce) | 6 | 7 | 6 | **19** |
| Tree fruits | 6 | 1 | 2 | 9 |
| Wild food | 4 | 1 | 3 | 8 |
| Base ingredients | ~16 | ~6 | ~4 | ~26 |
| Imported goods | - | - | - | 8 |
| Dishes | 17 | 21 | 13 | **51** |
| Dishes added 2026-11-17 (7g, not tiered) | - | - | - | 20 |
| Drinks | 0 | 3 | 2 | 5 (+ Kinnie, not tiered) |

- **Tier A alone:**
  - 6 crops, 6 trees and 4 wild foods;
  - about 16 base ingredients and the imports they need (rice, dates, cloves, cocoa);
  - **17 dishes:** bread, ħobż biż-żejt, ftira, two pastizzi, bigilla, ġbejniet, aljotta, stuffat tal-fenek, ross il-forn, timpana, fried lampuka, lampuki pie, octopus stew, imqaret, qagħaq tal-għasel and kannoli.
- **Art:**
  - about 140 item pictures (16×16) in total, about 55 of them for tier A;
  - 19 crop growth sets;
  - **4–6 placeable dish blocks** (timpana, ross il-forn, lampuki pie, mqarrun, prinjolata, pudina): the only real models. They are simple cake-like boxes.
- **No new machines and no new mobs.** The fish and animals come from the main content list.

---

## 11. How it would be built (for later; nothing started)

- **Fabric 26.3**: a separate mod from `maltagen`, with its own mod id.
- **Food items** use the vanilla `food` and `consumable` data components: nutrition, saturation, effects and eating time. Placeable dishes copy the vanilla cake block.
- **Recipes:** data-driven JSON (shapeless crafting, smelting, smoking, campfire). The cauldron salt and the unpeeled prickly pear need a little code.
- **Seeds and fruit drops:** loot-table modifiers on vanilla grass, bushes and leaves, with a `location_check` on the `maltamc:*` biome. If a biome is missing (another world), nothing drops, which is safe.
- **Imports:** Fabric's trade helper for the wandering trader, and a loot-table modifier for `chests/shipwreck_supply`.
- **Seasons** (lampuka spawns, festa sweets): this waits for the calendar decision (life-ideas question 1).

---

## 12. Questions for the owner

1. **Sheep's milk:** make vanilla sheep milkable so **ġbejniet need real sheep's milk** (recommended; the 2025 protected food ✓)? Or allow any milk, which is simpler?
2. **Horse meat** (laħam taż-żiemel ✓ is a real Maltese stew, eaten in Baħrija): **leave it out** (recommended, because horses are companions in Minecraft), or add it as a rare dish?
3. **Wine:** an ingredient you can also drink with **no drunk effect** (recommended)? Or an ingredient only?
4. **Seasonal foods** (festa and feast sweets): **craftable all year with a bonus in season** (recommended)? Or only craftable in season? Lampuki stay seasonal either way, because the fish only spawn then. This depends on the calendar (life-ideas question 1).
5. **Soups in bowls:** stack to 1 like vanilla, or to 16, which is friendlier?
6. **Placeable oven dishes** (timpana, ross il-forn, lampuki pie): eaten in slices from a block, yes or no?
7. **Gozo dishes:** should the Gozo ftira (and later other Gozo foods) be makeable anywhere, or give a bonus only when made or eaten on Gozo?
8. **Where to start:** tier A as listed, or a smaller first slice? For example, **bread, pastizzi, ħobż biż-żejt and stuffat tal-fenek**, with the 6 crops and the base ingredients they need.

---

## Sources checked this session (2026-11-17)

- Dishes overview: [List of Maltese dishes (Wikipedia)](https://Www.wikipedia.org/wiki/List_of_Maltese_dishes); [Maltese cuisine (Wikipedia)](https://en.wikipedia.org/wiki/Maltese_cuisine); [Guide Me Malta, a fool's guide](https://www.guidememalta.com/en/a-fool-s-guide-to-traditional-maltese-food-where-to-find-it)
- Calendar sweets: [Maltese food and the Christian calendar](https://kliemustorja.com/2022/03/31/maltese-food-and-the-christian-calendar/); [Oh My Malta, Easter sweets](https://ohmymalta.com.mt/2023/03/27/traditional-maltese-easter-sweets); [Guide Me Malta, festa sweets](https://www.guidememalta.com/en/must-try-10-traditional-maltese-festa-sweets); [MaltaToday, zeppoli](https://www.maltatoday.com.mt/gourmet/other/93710/watch_the_strange_case_of_the_zeppoli_of_st_joseph); [Apron and Whisk, qagħaq tal-ħmira](https://apronandwhisk.com/qaghaq-tal-hmira-maltese-yeast-rings/)
- Ftira: [MaltaToday, Gozitan ftira](https://maltatoday.com.mt/other/gourmet/12084/recipe-gozitan-ftira); [Food Republic](https://www.foodrepublic.com/1505962/gozo-ftira-maltese-style-pizza-potato)
- Aljotta: [MaltaToday](https://www.maltatoday.com.mt/gourmet/recipes/53253/watch_maltese_aljotta); [Little Rock](https://littlerock.com.mt/food/maltese-traditional-recipe-aljotta-fish-soup)
- Ġbejniet: [MaltaToday](https://www.maltatoday.com.mt/gourmet/other/12079/little-cheese-from-the-gozitan-shores-gozo-gbejniet); [EU protected designation 2025](https://malta.representation.ec.europa.eu/news/gbejna-tan-naghag-first-maltese-food-be-registered-geographical-indication-protected-designation-2025-01-28_fi); [Benna ġbejna guide](https://www.benna.com.mt/the-ultimate-gbejna-guide/)
- Snails and arjoli: [Ch-EAT, stuffat tal-bebbux](https://ch-eat.squarespace.com/recipes/stuffat-tal-bebbux); [Love Malta, snails after rain](https://lovemalta.com/its-raining-in-malta-lets-cook-some-snails/); [Anna Sultana, bebbux bl-arjoli](https://imturning60help.blogspot.ca/2013/08/anna-sultanas-bebbux-bl-arjoli-land.html)
- Soups: [Kawlata (Wikipedia)](https://en.wikipedia.org/wiki/Kawlata); [Apron and Whisk, minestra](https://apronandwhisk.com/minestra-traditional-maltese-vegetable-soup/)
- Imbuljuta: [Imbuljuta tal-Qastan (Wikipedia)](https://en.wikipedia.org/wiki/Imbuljuta_tal-Qastan)
- Horse meat: [Guide Me Malta](https://www.guidememalta.com/en/to-love-or-hate-these-traditional-maltese-foods-have-left-even-locals-divided)
- Lampuki: [Lampuki netting (Wikipedia)](https://en.wikipedia.org/wiki/Lampuki_netting); [Little Rock, torta tal-lampuki](https://littlerock.com.mt/food/maltese-traditional-recipe-torta-tal-lampuki-lampuki-pie); [Oh My Malta](https://ohmymalta.com.mt/2024/09/11/from-sea-to-plate-its-time-for-lampuki)
- Summer and festa: [Lovin Malta, summer tastes](https://lovinmalta.com/sponsored/9-tastes-that-instantly-scream-summer-in-malta); [Guide Me Malta, festa sweets](https://www.guidememalta.com/en/must-try-10-traditional-maltese-festa-sweets)
- Pastizzi pastry: [Guide Me Malta, the secret of pastizzi](https://www.guidememalta.com/en/they-taste-soooo-good-but-what-s-the-secret-behind-perfect-maltese-pastizzi); [Tal-Forn](https://www.tal-forn.com/2013/02/pastizzi-camenzuli-style/)
- Preserves and honey: [Visit Gozo, preserves](https://visitgozo.com/2024/04/24/have-you-tried-all-these-preserves-and-delicacies-on-the-island-of-gozo/); [Welcome Center Malta, honey and salt](https://www.welcome-center-malta.com/honey-sea-salt-and-history-gourmet-gifts-from-the-maltese-islands); [Oh My Malta, capers](https://ohmymalta.com.mt/2023/05/29/foraging-malta-capers/)
- Bread and steamed beef: [Maltese bread (Wikipedia)](https://en.wikipedia.org/wiki/Maltese_bread); [Maltese recipes, laħam taċ-ċanga fuq il-fwar](https://malteserecipes.pages.dev/recipes/laham-tac-canga-fuq-il-fwar)
- Crops, honey plants, the Maltese fungus, edible snails: the project's own research notes ([[Research]]), 2026-11-14.
