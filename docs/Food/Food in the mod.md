---
type: "topic"
---
# Food in the mod

What exists in `mod/` so far (2026-11-17). Each entry is **art only**: it has its texture or model, a name and an id, and can be seen in the game. **There's no gameplay yet**: no recipes, no food values (except placeholders on the slice dishes), and no cooking. That waits for the owner's go-ahead. Every entry was accepted by the owner; the decision notes are in [[Decisions]]. The same list with pictures, beside everything not drawn yet, is [[Food progress]].

## Items (16×16 icons)
| Id (`mimcontent:`) | Name | Batch |
|---|---|---|
| `hobz_malti` | Ħobż tal-Malti | bread |
| `ftira` | Ftira | bread |
| `hobz_bizzejt` | Ħobż biż-Żejt | bread |
| `ftira_ghawdxija` | Ftira Għawdxija | bread |
| `galletti` | Galletti | bread |
| `qassata_irkotta` | Qassata tal-Irkotta | pastries |
| `qassata_pizelli` | Qassata tal-Piżelli | pastries |
| `qaghaq_hmira` | Qagħqa tal-Ħmira (sesame bread ring) | bread rings |
| `qaghqa_appostli` | Qagħqa tal-Appostli (Holy Week ring with almonds) | bread rings |
| `pastizz_irkotta` | Pastizz tal-Irkotta | pastizzi (the flagship) |
| `pastizz_pizelli` | Pastizz tal-Piżelli | pastizzi |
| `pastizz_xema_irkotta` | Pastizz tax-Xema' tal-Irkotta (round) | pastizzi |
| `pastizz_xema_pizelli` | Pastizz tax-Xema' tal-Piżelli (half-moon) | pastizzi |
| `gbejna` | Ġbejna (fresh) | cheese |
| `gbejna_niexfa` | Ġbejna Niexfa (dried) | cheese |
| `gbejna_tal_bzar` | Ġbejna tal-Bżar (peppered) | cheese |
| `lampuka` | Lampuka (the caught fish) | fish |
| `lampuka_moqlija` | Lampuka Moqlija (fried, on a plate) | fish |
| `kinnie` | Kinnie (bottle) | drinks (real label; plain fallback in `drinks.py`) |
| `kinnie_can` | Kinnie Can | drinks |
| `kinnie_glass` | Glass of Kinnie | drinks |
| `imqaret` | Imqaret | sweets |
| `kannoli` | Kannoli (plain ricotta) | sweets |
| `qaghaq_ghasel` | Qagħaq tal-Għasel | sweets |
| `gelat_malti` | Ġelat Malti (ġelat tan-nanna) | sweets |
| `fenek_moqli` | Fenek Moqli (fried rabbit, on a plate) | meat |
| `stuffat_fenek` | Stuffat tal-Fenek | bowls (shared terracotta bowl, plain rim) |
| `aljotta` | Aljotta | bowls |
| `stuffat_qarnit` | Stuffat tal-Qarnit | bowls |
| `bigilla` | Bigilla | dips (low terracotta dish) |
| `dip_gbejna` | Dip tal-Ġbejna | dips |
| `dip_tonn` | Dip tat-Tonn (the pink creamy kind) | dips |
| `dip_tewm` | Dip tat-Tewm | dips |
| `soppa_tal_armla` | Soppa tal-Armla | soups (same bowl; each soup has its own look) |
| `minestra` | Minestra | soups |
| `kawlata` | Kawlata | soups |
| `kusksu` | Kusksu | soups |
| `brodu_tat_tigieg` | Brodu tat-Tiġieġ (chicken broth) | soups |
| `brodu_tal_laham` | Brodu tal-Laħam (beef broth) | soups |
| `stuffat_bebbux` | Stuffat tal-Bebbux (snail stew) | soups |

## The golden pastizz (design started 2026-11-18)
A gold pastizz based on the Pastizz tal-Irkotta ([[2026-11-18 The golden pastizz - design]]). Its icon `golden_pastizz` is the accepted ricotta pastizz's exact shape, turned gold the way vanilla turns the apple and carrot gold, in three candidates that differ only in the ricotta (gold, cream, pale gold): `art/candidates/food_golden_pastizz.png`, made by `art/src/food_golden_pastizz.py`. **Decided** ([[2026-11-18 Golden pastizz - C, 8 ingots, like golden carrot, enchanted as rare loot]]): art C (pale-gold ricotta); recipe a Pastizz tal-Irkotta in 8 gold ingots; eating it is like the golden carrot for now, with a distinctly Maltese effect later; an enchanted golden pastizz exists as rare loot, its loot tables not designed yet. The questions below are answered by that note. The item isn't registered in the mod yet, so it doesn't show in the game.

**Proposal only, nothing is decided: what it could do in the game.** By analogy to vanilla's golden apple (an emergency heal) and golden carrot (the best everyday food):
- **Owner question 1, the recipe:** a pastizz in the middle of the crafting grid with 8 **gold nuggets** around it (like the golden carrot, cheap enough to eat often) or 8 **gold ingots** (like the golden apple, a rare treat)? Either kind of pastizz, or only tal-irkotta, as the art shows?
- **Owner question 2, what eating it does:** like the golden carrot (lots of hunger and saturation, no effects), or like the golden apple (a few seconds of Regeneration II and 2 minutes of Absorption)? A third idea: a Maltese twist, such as a short Speed or Haste boost, "fuelled for the day".
- **Owner question 3, an enchanted version:** vanilla has an enchanted golden apple (found in chests, no recipe since 1.9, with the glint and strong effects). Should there be an enchanted golden pastizz, for example as rare loot or a festa prize, or only the one golden pastizz with no glint?
- **Owner question 4, other uses:** anything else, e.g. a trade with villagers, a gift that tames or heals an animal, or a festa prize?

## Placed dishes, eaten in 6 slices like a cake
| Id | Name | Dish | State |
|---|---|---|---|
| `ross_il_forn` | Ross il-Forn | foil tray | placed dish "tentatively works"; icon v6 |
| `imqarrun_il_forn` | Imqarrun il-Forn | white ceramic dish with grip lips, 3D penne top | done; icon v5a |
| `timpana` | Timpana | foil tray, pastry lid and walls | done |
| `torta_lampuki` | Torta tal-Lampuki | round pie in a terracotta dish, eaten in wedges; icon in the cake view | done |

These use one block class, `SliceDishBlock`. Its food values are placeholders.

## Kitchen blocks (the art pilot)
`kenur` (the stone stove, with a pot on it), `borma` and `borma_stuffat`. The owner said these "can pass for now".

## Still to draw for phase 1
- Phase 1 dishes are all drawn.
- **Then:** ingredients, crops with growth stages, fruit, and the station blocks (forn, quern, taġen).
- **Before each batch, wait for the owner's photos** ([[2026-11-17 Bigilla v6b and galletti accepted; wait for photos before each batch]]).
