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
| `stuffat_fenek` | Stuffat tal-Fenek | bowls (shared terracotta bowl, plain rim) |
| `aljotta` | Aljotta | bowls |
| `stuffat_qarnit` | Stuffat tal-Qarnit | bowls |
| `bigilla` | Bigilla | bowls |
| `soppa_tal_armla` | Soppa tal-Armla | soups (same bowl; each soup has its own look) |
| `minestra` | Minestra | soups |
| `kawlata` | Kawlata | soups |
| `kusksu` | Kusksu | soups |
| `brodu_tat_tigieg` | Brodu tat-Tiġieġ (chicken broth) | soups |
| `brodu_tal_laham` | Brodu tal-Laħam (beef broth) | soups |

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
