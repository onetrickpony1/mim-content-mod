# Petriċa (anglerfish): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** anglerfish, *Lophius* (the report lists *L. piscatorius* and *L. budegassa*, both **Petriċa**). One model for both.
- **Name:** **Petriċa**, with the ċ (id `petrica`).

## Size
- **Size in game:** 1.75 blocks long (28 px), 1.1 blocks wide across the head and its fringe, flat (the head 5 px deep). Body box 0.9 x 0.35 (unchanged). The art maker made it longer than the placeholder (1.38 blocks) after critics found it small beside the ċerna.
- **Why:** anglerfish get big (the larger kind past a metre†). Like the tonn and the shark, it is kept near the size of a big one: a wide, flat head is its look.

## Behaviour, spawns, rarity
- **Behaviour:** sits still on the bottom, rests of 30 to 90 seconds, hardly ever moves. Doesn't shy from players. Flat: on land it lies flat instead of flopping on its side (like the boll). Health 10. Harmless (no bite yet; its lure doesn't do anything).
- **Spawns:** only over soft floors (mud, sand), deep: `fond_deep_sea`, `dwejra_fond_deep_sea`, weight 2, alone. Vanilla: deep lukewarm, weight 1.
- **Rarity:** rare.
- **Stings:** no.
- **Drops:** itself (1 raw fish, `mimcontent:petrica`). Bucket, spawn egg. It is shark bait.

## Art
Made overnight by a maker, judged by a fresh critic each round from pictures only. Photos: free Wikimedia Commons ones (licences in `art/references/fish_petrica_refonly/list.tsv`), colour from landed fish (Norway, a Mediterranean *L. budegassa* at an Algerian market) and a museum fish labelled "Frequent in Maltese waters".

**3D model** (`art/src/fish_petrica_model.py`): **gave up** after 8 of 8 rounds; the last version is installed.
- Three paint jobs tried: A warm mottled brown, B olive brown (the Mediterranean kind), C A with bigger blotches. **A chosen**: the photos of the fish out of water are warm brown.
- **Looks:** a huge, flat head 16 px across (18 with its fringe), nearly half the fish, 5 px deep in the middle stepping down to a 1 px rim, its corners cut so it isn't a square. The lower jaw juts out 1 px with a pale lip, and the gape is one straight dark line right across the front, never curved. Small eyes sit near the head's edges on top, each a dark pupil in a light-brown ring. The rod stands right behind the upper lip, leaning forward, 1 px thin, with a small dull flap at its tip (no glow). Pale skin flaps fringe both sides of the head and the lower jaw. The body tapers 9, 5, 3 px wide and 3, 2, 2 px deep to a small fan tail that sways. Fan pectoral fins lie flat, swept back, at the body's sides, and a low soft fin sits on the back near the tail.
- **Colours:** back #94704a, light #c8a070, dark blotches #5a3c28, ochre blotches #e0b878, cream belly #d8c8aa, gape #1a120c, eye #0c0806. They are set a third lighter than the photos, because under water it went near-black beside the cod.
- **Size:** 1.75 blocks long. That is longer than the placeholder, and the critics found it small beside the ċerna.
- Round 1 FAIL: under water it read as a grey boat with a crane, the rod was too big, and there was no mouth. Round 2 FAIL: it was grey-lavender under water and the eyes made a cute face. Round 3 FAIL: the front read as a cartoon face, the fringe under the chin as teeth, the tail as a knob on a stick, and the camouflage as stripes. Round 4 FAIL: too dark under water, an eel-like side and fins hanging like legs. Round 5 FAIL: the eyes were lost in the blotches and the head was boxy. Round 6 FAIL: the face from the front, and a cream eye ring made googly eyes, so the ring went back to a light brown. Round 7 FAIL: a plain patch above the mouth read as a face, and the eyes were small. Round 8 FAIL, "narrowly": too light and sandy, the flanks striped, a dark bar above the eyes, still smaller than the ċerna.
- The critics pulled the colour both ways: rounds 2 and 4 asked for lighter, round 8 for darker (#6B5A42). The owner should pick the shade.
- **Left for the owner:** whether the head-on view (two eyes above a straight mouth, as on the real fish) reads too much like a face; the back's darkness; a bigger fish (rounds 5 and 8 asked for 1.3-1.5x).
- After round 8 the rod was moved onto its pivot (it had been left 2 px behind it, which lifted the flap to 9 px). The fish now stands at most 7 px tall, so it lies flat on land as the fish test expects. The look is unchanged and was not re-judged.
- A new review shot, `fish-petrica-lineup` (with `-lineup-above` and close-ups `-close-three-quarter`, `-close-top`, `-close-front`), shows it resting on the floor beside a cod, the ċerna and a small tonn.

**Item icon** (`art/src/fish_petrica_icon.py`): **passed in round 6** of 8.
- The caught fish seen from above, as it lies on a market slab: head at the lower left, tail at the upper right, like vanilla's fish.
- **Looks:** a huge, wide head with a straight front: a pale lip line right across it and the dark gape just outside it, both dead straight. The body narrows fast to a small tail, with fan fins at the sides. Two small near-black eyes far apart on top, each with a pale glint. A faint light ridge between them for the rod, and darker skin flaps sticking out at the upper right. Mottled brown in 2 px blotches, outlined in dark brown.
- **Colours:** the model's, only a little lighter (x1.05) for out of water. The lip is a warm pinkish cream (#d9bc9c), the rod ridge #ae8458.
- Three candidates each round: A (chosen), B without the pale lip, C without the rod.
- Round 1 FAIL: it read as a scorpionfish or grouper. Round 2 FAIL: a stingray with a whip tail, though one reader got a monkfish. Round 3 FAIL: a sole. Round 4 FAIL: a stingray. Round 5 FAIL: a sole or scorpionfish; the rod read as a nose. Round 6 PASS, "narrowly"; its polish was then applied: the lip toned down (bright, it read as teeth), the rod ridge darker, the head's top-left corner rounded, the fins 1 px bigger.
- What three readers who knew nothing said, first line each, in round 6: "A raw flatfish, most likely a sole or flounder, shown from above with its head at the lower left and its tail at the upper right." / "Slot 4 is a fish, most likely a flatfish such as a sole or flounder, shown lying flat and pointing diagonally. It might also be a lizardfish or monkfish-type fish with a big head." / "Slot 4 looks like a flatfish (a sole or flounder type), seen from above and lying on the diagonal."
- So it reads as a flat brown fish, but mostly as a sole, not an anglerfish. One reader in round 2 said "a monkfish (anglerfish) item, seen from above", but that design read as a stingray to the others.

**Bucket** (`art/src/fish_petrica_bucket.py`): **passed in round 3** of 8.
- Laid on top of the player's own vanilla cod bucket, like the other fish buckets; the back rim stays dark at its two lower corners.
- **Looks:** the head rises out of the water facing you: a flat slab as wide as the bucket's mouth, two small eyes just under its top edge with an olive glint each, the gape one level very dark brown line right across, the lower jaw below it with two pale skin flaps, mottled brown. Water shows underneath.
- Round 1 FAIL: a diagonal head like the icon's read as a wedge, beak or wood chip, and the pointed tip came near phallic. Round 2 FAIL: a black gape over a pale jaw, with cream beside the eyes, read as a grinning cartoon face or a burger. Round 3 PASS (best A); the critic's polish was applied after: the eyes moved down a row under the outline, the head pulled in to the rim's width, two light flecks made mid brown.
- The round 1 critic asked for a greyer olive brown; tried as a candidate in round 2, the next critic found it "washed out next to the cod bucket", so it stays the icon's warm brown.
- What three readers who knew nothing said, first line each, on the final bucket: "Slot 5 is the non-vanilla item. My guess is a bucket holding a flat, bottom-living fish, something like a flounder, sole or turbot, mottled sandy brown with both eyes on its upper side." / "Slot 3 is the non-vanilla item: a bucket holding a mottled grey-green fish with small reddish-orange patches. My best guess is a Mediterranean rock or reef fish such as a wrasse (or possibly a scorpionfish)." (that reader picked the vanilla salmon bucket, not ours) / "Slot 5 is the non-vanilla item: I think it's a bucket holding a squat brown fish with darker mottling or bands, maybe a grouper or a scorpionfish-type rock fish."
- On the round 3 version (eyes on bumps), one reader said "most likely a stargazer, or possibly a monkfish or anglerfish"; the others said a flatfish or grouper. So it reads as a flat brown bottom fish, rarely as an anglerfish. One reader said it could look like a wooden crate lid at hotbar size.

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [FishBase, *Lophius budegassa*](https://www.fishbase.se/summary/Lophius-budegassa.html)
- [FishBase, *Lophius piscatorius*](https://www.fishbase.se/summary/Lophius-piscatorius.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.
