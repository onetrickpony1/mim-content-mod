---
type: item
kind: boat
subject: Maltese Life
status: accepted
tier: 
maltese: Luzzu
english: Maltese fishing boat
id: mimcontent:luzzu
---
# Luzzu

The luzzu is Malta's traditional double-ended fishing boat, brightly painted, with the Eye of Osiris on the bow. In the game it is a **rideable boat with its own 3D model**, placed and steered like a vanilla boat ([[2026-11-17 Luzzu - a rideable boat with its own model]]).

**State (2026-11-17):** **accepted by the owner** after nine rounds (maker, critic, owner), in three colour schemes, with the diagonal item icons ([[2026-11-17 Luzzu accepted, diagonal icons]]).

## How you get it
- Placed from the luzzu item, like a vanilla boat; breaking it gives the item back (and whatever is in the fish hold). Crafting comes later.

## The look
- **Its own model**, not a recoloured vanilla boat: a pointed hull at both ends, a sheer that rises toward bow and stern, tall raked posts (the bow post taller), rubbing strakes, an open middle with end decks.
- **Paint:** banded like the real boats, with the Eye of Osiris on both sides of the bow.
- **The eye** (owner, [[2026-11-18 Luzzu eyes - sharper, smaller, less round]]): redrawn 5 x 2, a sharp almond with a dark brow sweeping back to a point at the stern and a navy iris between white, on the yellow of the bow panel; picked by the third critic; the item icons keep their 2 px eye. Close-ups: `SMOKE_ONLY=luzzu_eye tools/run-art.sh`.
- **The eye on one level** (owner, [[2026-11-18 Luzzu eye - reads badly from the front, on two levels]]): the whole eye now sits on the outer face of the bow panel, rows 2-3 right under the band, with a row of yellow below it, so it no longer splits across the panel's step from the front; on the brown boat the brow lies on the wood band's lower row, like real varnished luzzus; picked by an independent critic over an eye on the inset tier. The close-ups now include head-on views.
- **Owner's notes on version 2** ([[2026-11-17 Luzzu - oars match the accent, a bit wider, several colour schemes]]): oars shaped like real luzzu oars and painted in the boat's accent colour; a little wider; **several colour schemes** (green accent with green oars; red accent, blue at the top, blue oars; more if the photos show them), each its own boat and item like vanilla's wood types.
- **Later notes:** it sits high, with only the bottom paint under water ([[2026-11-17 Luzzu - sits higher in the water]]); both ends come to a point, seen from above and head-on ([[2026-11-17 Luzzu - pointed ends]]).
- **Colour schemes:** green (`mimcontent:luzzu`: yellow capping, red band, green posts and oars), red (`luzzu_red`: blue at the top, red band and posts, blue oars), brown (`luzzu_brown`: a varnished wood band, wooden posts and oars).
- **Item icons:** the diagonal pose of the vanilla boat icons (owner: "theyre cute").

## Buffs (picked by the owner; each behind a config switch, vanilla boats unchanged)
From [[2026-11-17 Luzzu buffs - seats, fish hold, fishing, engine, homing]]. **Built 2026-11-17** (waiting for the owner to try them). Each has its own switch in `config/mimcontent.json`, written with every switch on the first time the game starts. `false` gives that part back its vanilla boat behaviour; restart after editing. On a server, the server's file decides for everyone.

| Buff | Switch | What it does |
|---|---|---|
| More seats | `luzzu_more_seats` | **3 seats** (vanilla 2; owner, 2026-11-17: "max 3 people, without someone in front of the rower"), along the hull, all facing the bow: the helmsman at the oars (the first to board, the only one who steers and rows; a player always takes it before mobs), then two behind. Same hitbox as a vanilla boat. |
| A fish hold | `luzzu_fish_hold` | **27 slots**, like a chest boat, without losing a seat. Use to board; sneak and use (or use a full boat) to open the hold; while riding, the inventory key opens it. Saved with the boat; everything in it drops when the boat breaks (even with the switch off, so nothing is lost). |
| Fishing bonus | (none yet) | **Not built.** Waits for the fish and season systems; a note marks where it goes. |
| Engine speed | `luzzu_engine` | **25% faster** than a vanilla boat on open sea: water all round for 4 blocks and at least 3 deep. Near the shore, in a channel or in shallow water it goes at vanilla speed. The speed eases in and out over a couple of seconds, so there's no jolt. |
| It finds home | `luzzu_finds_home` | Remembers its **harbour**: where it was placed, and where its driver last stepped off at a shore (not at open sea). Steering within **30 degrees** of the harbour, more than 16 blocks away, adds **10%** (on top of the engine). Saved with the boat. |

The seats sit 2 px higher than a vanilla boat's, on the luzzu's raised floor (it rides high in the water).

**How players sit** (owner, [[2026-11-17 Luzzu - fix the gaps, how the player sits, oars only when rowing]]; seating reworked after the critic's full-boat check): in a luzzu a player sits on a thwart, 5 px above the floorboards, with legs down and forward to the floor (60 degrees from straight down, where a vanilla boat's are almost straight out), so their feet stay inside the hull. The helmsman's hands hold the oars all through the stroke (see **Oars** below); a hand whose oar isn't rowing rests on the thigh. The others rest their hands on their thighs. Only players (and mannequins) sit this way, only in a luzzu; mobs keep their own pose and sit on the floor, and vanilla boats are unchanged. Visual only, no switch.

| Seat (boarding order) | Where (blocks from the middle) | Faces |
|---|---|---|
| 1, the helm | 0.28 forward, the forward-most rider (feet inside the bow end of the open well) | the bow |
| 2 | 0.32 aft | the bow |
| 3 | 0.92 aft, clear of the stern deck | the bow |

The seats are 0.6 blocks apart, so heads don't touch seen side on, within the open well (the floor between the end decks, about 1.05 blocks either way of the middle). Each rider's feet go under the thwart ahead. Resting riders' arms hang nearly straight down, hands on their thighs, clear of the rider ahead. Mobs use the same seats.

**Oars** (owner, [[2026-11-18 Luzzu - oars match the rower's arms]]): each oar shows only while it is rowing; a still boat has none out. Visual only, no switch.
- **Thole pins beside the helm:** the oars turn on the gunwale's outer edge 6.5 px ahead of the rower's shoulders (boat model x 11, 8 px out, the shaft riding just above the gunwale), so the handles come inboard to the rower's hands. With `luzzu_more_seats` off the helm seat moves and the pins move with it.
- **The rower pushes, facing the bow**, as is common on Maltese boats† (not yet sourced; the reference photos show no rowing): the blade goes in ahead of the pin with the hands near the chest, the hands push forward while the blade sweeps aft through the water, then the hands come back low with the blade lifted clear. Same phase as vanilla's paddles (`getRowingTime`, each side on its own); the stroke is a little smaller than vanilla's (pitch -50 to -10 degrees, sweep from 20 degrees forward of abeam to 25 aft) so a straight arm can always reach.
- **Hands on the handles:** each hand holds a fixed point 4.5 px in along its oar (the handle runs through the fist and just out the other side). The arm is aimed at that point from the real positions of boat and rider; the player model's arms can't bend, so the shoulder slides up to 2 px forward or back along the body to keep the straight arm on the handle. The in-game check measures every hand against its handle at 16 points of the stroke.
- **One oar** (turning): only that hand rows; the other rests on the thigh and its oar stays in.
- **Seen by others and in third person** the same. In first person the game draws your hand as vanilla does in any boat (vanilla has no rowing arms there either).
- Real luzzu photos (`art/references/luzzu_refonly/`) show moored and slipway boats, none being rowed; the one painting (24, Caruana Dingli) shows long sweeps and a standing crewman, so the bow-facing seat stays.
- Code: `client/LuzzuOars.java` (the stroke, the pins, the arm aim), `LuzzuRenderer`, `AvatarRendererMixin`, `HumanoidModelMixin`; the pins are also in `art/src/luzzu.py` (`OAR_POSE`), which writes the model.

## Art
- Made by `art/src/luzzu.py`, which writes the texture, the item icon and the model code together, so they can't drift apart.
- Reference photos: `art/references/luzzu_refonly/` (web photos, reference only, kept out of git).

## Sources
- [Malta Uncovered: Maltese boats, the luzzu](https://www.maltauncovered.com/culture/maltese-boats-luzzu/)
- Sale listings for the size: length about 7.7 to 8.5 m, beam about 2.8 to 3 m (boatshed, samboat, dailyboats).
