---
type: item
kind: boat
subject: Maltese Life
status: open
tier: 
maltese: Luzzu
english: Maltese fishing boat
id: mimcontent:luzzu
---
# Luzzu

The luzzu is Malta's traditional double-ended fishing boat, brightly painted, with the Eye of Osiris on the bow. In the game it is a **rideable boat with its own 3D model**, placed and steered like a vanilla boat ([[2026-11-17 Luzzu - a rideable boat with its own model]]).

**State (2026-11-17):** in the mod as a work in progress; the look is being redrawn round by round (maker, critic, owner). Not accepted yet.

## How you get it
- Placed from the luzzu item, like a vanilla boat; breaking it gives the item back. Crafting comes later.

## The look
- **Its own model**, not a recoloured vanilla boat: a pointed hull at both ends, a sheer that rises toward bow and stern, tall raked posts (the bow post taller), rubbing strakes, an open middle with end decks.
- **Paint:** banded like the real boats, with the Eye of Osiris on both sides of the bow.
- **Owner's notes on version 2** ([[2026-11-17 Luzzu - oars match the accent, a bit wider, several colour schemes]]): oars shaped like real luzzu oars and painted in the boat's accent colour; a little wider; **several colour schemes** (green accent with green oars; red accent, blue at the top, blue oars; more if the photos show them), each its own boat and item like vanilla's wood types.

## Buffs (picked by the owner; each behind a config switch, vanilla boats unchanged)
From [[2026-11-17 Luzzu buffs - seats, fish hold, fishing, engine, homing]]:
1. **More seats:** 3 to 4 players.
2. **A fish hold:** storage without losing a seat.
3. **Fishing bonus:** better catches, and the lampuka under the kannizzati in season. Waits for the fish and season systems.
4. **Engine speed:** about 20 to 30% faster than a vanilla boat on open sea, normal near the shore.
5. **It finds home:** a small speed boost toward the harbour it last set out from.
Building the buffs starts once the current round of the look is done (owner: "you can start on them").

## Art
- Made by `art/src/luzzu.py`, which writes the texture, the item icon and the model code together, so they can't drift apart.
- Reference photos: `art/references/luzzu_refonly/` (web photos, reference only, kept out of git).

## Sources
- [Malta Uncovered: Maltese boats, the luzzu](https://www.maltauncovered.com/culture/maltese-boats-luzzu/)
- Sale listings for the size: length about 7.7 to 8.5 m, beam about 2.8 to 3 m (boatshed, samboat, dailyboats).
