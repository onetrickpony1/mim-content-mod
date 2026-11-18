# Changelog

## Unreleased

### Features
- **Tier A fish.** Seven Maltese fish now swim in the sea: lampuka, tonn (bluefin tuna), sardina, ċerna (grouper), awrata (sea bream), murina (moray eel) and żiemel tal-baħar (seahorse). They behave like vanilla fish: sardines, tuna and lampuki swim in schools, the others alone, and all flop on land. Each drops itself when killed (a lampuka that dies burning drops a fried one), except the seahorse, which is protected and drops nothing. Each has a spawn egg and can be caught alive in a water bucket and let out again. They live in the Malta world's seas: sardines and sea bream in the shallows, groupers and morays round the rocks, tuna and lampuki out in deep water, seahorses in the posidonia meadows. They also turn up in vanilla's warm and lukewarm oceans; set `fish_in_vanilla_oceans` to `false` in `config/mimcontent.json` to keep them to Malta. The lampuka, tonn and sardina have their final art (item, bucket, spawn egg and swimming model); the ċerna, awrata, murina and seahorse are being drawn, one piece at a time. Fish buckets from the ċerna on show the fish's head rising out of the water, as vanilla's do.
- **Tonn in mixed sizes.** Each tuna is now its own size, from 2 to 4 blocks long, most often about 3, like a real school with young and old fish. Fish in one school are about the same size. Bigger tuna are tougher (from 5 to 10 hearts), the hitbox grows with the fish, and a tuna keeps its size when you save the game or carry it in a bucket.
- **The luzzu.** Malta's painted fishing boat, with its own model, in three colour schemes (green, red and brown). Place it and ride it like a vanilla boat. It has four extras, each one switchable in `config/mimcontent.json` (set one to `false` and that part works like a vanilla boat again; vanilla boats never change):
  - **3 seats** instead of 2. The first one aboard rows and steers; the other two sit behind.
  - **A fish hold** with 27 slots, like a chest boat, without giving up a seat. Sneak and use the boat to open it, or press your inventory key while riding. Whatever is in it drops when the boat breaks.
  - **An engine:** 25% faster than a vanilla boat out on open sea, normal speed near the shore and in shallow water.
  - **It finds home:** 10% faster when you steer toward the harbour it last set out from (where you placed it, or where its driver last stepped off at a shore).
  - **Players sit on a bench.** In a luzzu you sit on a thwart with your feet on the floorboards, so legs no longer poke out through the front of the hull. Only the one at the helm reaches for the oars; the others rest their hands on their knees. Everyone faces the bow, nobody sits in front of the rower, and the seats are spaced out so a full boat doesn't run together.
  - **Oars only while rowing.** A luzzu lying still shows no oars; each one appears while it rows.
- **Maltese food in the game.** ħobż tal-Malti, ftira, ħobż biż-żejt, ftira Għawdxija, galletti, pastizzi tal-irkotta, tal-piżelli and the two tax-xema' kinds, ġbejna (fresh, dried and peppered), imqaret, kannoli and qagħaq tal-għasel, each with its own icon.
- **Qassatat and bread rings.** Qassata tal-irkotta and tal-piżelli, round pleated pastries with the filling showing on top, and two sesame bread rings: the everyday qagħqa tal-ħmira and the big Holy Week qagħqa tal-appostli with almonds.
- **Ġelat Malti.** Grandma's ice cream: cream scoops with toasted almonds and glacé cherries in a cream fluted bowl.
- **Fenek moqli.** Fried rabbit with garlic and fried potatoes, on the same plate as the lampuka moqlija.
- **Kinnie.** A bottle, a can and a glass of Malta's bittersweet orange soft drink.
- **Lampuka.** The caught fish, beside vanilla cod and salmon, and lampuka moqlija, a whole fried lampuka on a plate with lemon. They have no recipes or food values yet.
- **Stews and soups in a terracotta bowl.** Stuffat tal-fenek, aljotta, stuffat tal-qarnit, soppa tal-armla, minestra, kawlata, kusksu, brodu tat-tiġieġ, brodu tal-laħam and stuffat tal-bebbux (snail stew). Each soup has its own look so they're easy to tell apart, and the bowls have a plain terracotta rim.
- **Dips in a low terracotta dish.** Bigilla, dip tal-ġbejna, a pink creamy tuna dip and a thick garlic dip, each a rough spooned heap, so dips and soups can't be confused.
- **Oven dishes you eat in slices.** Ross il-forn in a foil tray, imqarrun il-forn in a white ceramic dish with baked penne on top, timpana in a foil tray with a pastry lid, and torta tal-lampuki, a round fish pie in a terracotta dish that you eat in wedges. Place one on a table and use it to eat a slice. Six slices per dish.
- **A Maltese kitchen.** The kenur, a limestone stove that can be lit and hold a pot, and the borma, a clay stew pot, empty or full of stuffat.
- **Labels with Maltese letters.** Comparison pictures now show ħ, ż and ġ instead of boxes.

### Fixes
- **Imqarrun il-forn:** the penne on top of the placed dish no longer cut into each other or flicker, whole or part-eaten. They now lie in a slightly looser heap (a few fewer tubes) that never overlaps.

### Documentation
- **Fish art lessons.** The art pipeline doc now lists what the owner's corrections taught: rounded edges and real shading, comparing fish with each other, no second eye, stylised spawn eggs, buckets that show the head, and true colours from photos out of water.
- **Fish progress page.** Every fish and sea creature planned, with the in-game icon, spawn egg and a live shot added as each fish's art is accepted. The anchovy now has its own entry, apart from the sardine, and the bogue sits with the sea breams.
- **Faster art checks.** Flat icons (item icons, buckets and spawn eggs) are now checked in a true-to-size copy of the hotbar made by `art/tools/hotbar_preview.py`, without starting Minecraft. 3D models still get a full in-game test, and each finished category gets one in-game test of all its icons.
- **Food progress page.** Every food in the plan, split into what's in the mod and what isn't yet, with a picture of each: the mod's own icons and in-game shots, and free photos for the rest.
