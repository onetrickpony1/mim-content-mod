# Kavall (chub mackerel): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** Atlantic chub mackerel, *Scomber colias* (listed in the species report under its old name *S. japonicus*). The report gives **Kavall** for it; the Atlantic mackerel is *Pizzintun*, so this is the right one for the name.

## Size
- **Size in game:** the model is 1.3 blocks long (21 px), body box 0.5 x 0.35 (unchanged). The first plan was 1.06 blocks (17 px), but beside the cod in the game it looked the same length, so the model was made longer and slimmer until it read clearly as a longer, slimmer fish than the cod.
- **Why:** a real one is about 25 to 30 cm† (up to about 50†). Life size would be smaller than a cod, so it is drawn bigger than life, like the other small fish.

## Behaviour, spawns, rarity
- **Behaviour:** swims in schools of up to 8, like the sardina (follows a leader, shies from players). Health 4 (2 hearts).
- **Spawns:** deep sea (`fond_deep_sea`, `fond_band_1`-`8`) weight 10, and `bahar_sea`, `dwejra_bahar_sea` weight 6, in groups of 3 to 6. Vanilla oceans (switch on): warm, lukewarm, deep lukewarm, weight 5.
- **Rarity:** common.
- **Stings:** no.
- **Drops:** itself (1 raw fish, `mimcontent:kavall`). Bucket, spawn egg. It is shark bait.

## Art
Made overnight by a maker, judged by a fresh critic each round from pictures only. Photos: free Wikimedia Commons ones (licences in `art/references/fish_kavall_refonly/list.tsv`), colour from fresh fish out of the water.

**3D model** (`art/src/fish_kavall_model.py`): passed in round 4 of 8.
- Three paint jobs tried: A blue-green back, B steel-blue back, C olive back. **A chosen**, as the brief asked for a blue-green back and it sits between the Mediterranean (bluer) and Atlantic (greener) photos.
- **Looks:** a torpedo with a pointed snout and a big black eye ringed in pale silver. Dark tiger bars cross the back every third pixel, starting well behind the eye. Below them are a green-silver upper flank, silver sides and a near-white belly (dark back, pale belly). Two dorsal fins are set apart, with one small finlet on the back and one on the belly just before a deeply forked tail. The fins and tail are dusky olive-yellow, like the photos.
- **Colours:** back #3c7a6e, bars #234a4e, head #4a7c72, cheek #d8dee0, belly #fbfcfa, tail #c2bb7a.
- Round 1 FAIL: a dark bar pixel in the eye's row read as a second eye, the bars looked like a chequerboard, there was no silver band and the back had too many bumps. Round 2 FAIL: too deep, it read as a small tuna, and the fins under the belly looked like legs. Round 3 FAIL: not longer than the cod, the tail broke into specks and the belly was too grey under water. **Round 4 PASS.**
- The critic's optional polish, not done (left for the owner): a lower second dorsal fin (it reads a bit like a stick under water), a lighter first dorsal fin, and bars that zig-zag one row down.
- Spots on the lower flank (the chub mackerel's own mark) were left out: at this size they read as stray specks.
- A new review shot, `fish-kavall-lineup` (kavall, cod, cerna, small tonn in one tank), was added to the fish test.

**Item icon** (`art/src/fish_kavall_icon.py`): passed in round 2 of 8.
- Head lower left, tail upper right, like vanilla's fish. Candidates: A (three bars), B (thinner bars), C (the third bar nearer the head). **A chosen** (the critic: B's bars vanish, C's spacing is uneven).
- The silver and the fins are the model's colours lifted about 1.2x for out of the water. The back keeps the model's own tones, because lifted it read as pale mint at 1x.
- The eye is the only near-black pixel, with soft grey-silver around it. The belly swells a little and shades from bright silver to pale. The first dorsal fin is grey-olive, not cream.
- Round 1 FAIL: a straight tube, a flat white belly, a "googly" eye and bars like specks. Round 2 PASS. Two of its small polish fixes were then applied: no lone dark pixel by the head, and less pure white in the silver line.
- **Blind reads** (three fresh readers, neutral file names, among vanilla items), first lines word for word:
  1. "Slot 3: a slim silver-blue fish with a forked yellow tail. It looks like a mackerel, horse mackerel or sardine, lying on a diagonal like vanilla fish icons."
  2. "Slot 3: a slim silver-blue fish, like a mackerel or sardine, lying diagonally with a pale belly, dark back and a forked yellowish tail at the top right."
  3. "Slot 3: a silvery mackerel or tuna-type fish, dark blue-green back, pale belly, yellow tail and fin tips."

**Bucket** (`art/src/fish_kavall_bucket.py`): passed in round 1 of 8.
- On vanilla's cod bucket, the head rises out of the water facing up and left: steel crown, pointed snout, the ringed eye, pale cheek, then the back with one dark bar diving into the water. The back rim outline stays dark except behind the head. Candidates: A (head high), B (head a row lower), C (a second bar). **A chosen.**
- Critic's optional polish, not done: one more pixel on the crown so the snout tapers.
- **Blind reads**, first lines word for word:
  1. "Slot 3: a bucket holding a pale silvery-teal fish, probably a mackerel- or sardine-like fish."
  2. "Slot 3: a bucket holding a slim, silvery grey-green fish (it looks like a mackerel or sardine), lying diagonally with its head down in blue water."
  3. "Slot 3: a water bucket holding a slim silver-grey fish with a pale green-blue tint."
- Two readers said the species is hard to tell at the smallest size; all three saw a silvery mackerel-like fish.

**Egg** (`art/src/fish_kavall_egg.py`, 2026-11-19): passed in round 3 of 3. **Owner 2026-11-19: passes** ([[2026-11-19 Spawn eggs - all eight pass]]).
- Started because the owner approved the bucket ([[2026-11-18 Approving a step starts the next; skorfna bucket]]). A plain egg in vanilla's outline and vanilla's own pool, in the icon's colours only: the teal back with its dark tiger bars, the silver belly as a patch on the lower front (not a band, which reads as a Pokéball), and olive-yellow side fins. No eye, no face.
- Candidates: A (three thin bars), B (A with the forked olive-yellow tail over the top right), C (wavier bars). Then B2 and B3 from the critics' fixes. **B3 chosen.**
- Round 1 FAIL, pick B: "The bars read as a checker or net pattern, not wavy tiger bars ... almost the same as the incova egg". Round 2 FAIL on B2: "The bars don't read as bars ... At 1x and in the GUI-2 hotbar it turns into teal noise". Round 3 PASS on B3: "the 2-px diagonal bars read as stripes at 1x and in both hotbars". Its optional polish, not done: the outer tail tip a mid olive, the brightest silver one step down.
- A bluer back to set it further apart from the incova egg was asked for in round 1 but not done: it needs a colour the accepted art doesn't have.
- **Blind reads** (three fresh readers, neutral file names, the egg in slot 4 among vanilla eggs), first lines word for word:
  - B2: "A teal-green and white egg with a small fin or tail sticking out at the top right. I'd guess a green-backed fish, maybe a wrasse or a bream." / "A spawn egg: teal-green on top, white underneath, with a thin yellow spike or stalk sticking up from the top right. It reads as a fish, perhaps a mackerel- or dolphinfish-type fish (green back, pale belly)." / "A spawn egg in teal-green with a pale white lower half and a thin yellowish stalk curling from the top."
  - B3 (the pick): "My first impression is a spawn egg for a fish. It is a chunky teal or blue-green fish with a pale underside, sitting on the same blue base as the other eggs." / "bar1.png, slot 4: my first impression is a spawn egg for a teal-green fish with a pale white belly." / "bar1.png: It looks like a spawn egg for a fish. The fish is blue-green on top with a pale white belly, sitting on the blue base like the other slots, and reminds me of a mackerel."
- All three read B3 as a spawn egg for a fish; all three named a mackerel(-type) fish, though none was sure. Two read the tail as a "stalk", "spike" or "lure".
- Sheet: `art/candidates/fish_kavall_egg.png`.

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [FishBase, *Scomber colias*](https://www.fishbase.se/summary/Scomber-colias.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.
