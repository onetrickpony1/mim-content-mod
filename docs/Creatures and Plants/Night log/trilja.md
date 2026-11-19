# Trilja (red mullet): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** the striped red mullet, *Mullus surmuletus* (*Trilja tal-qawwi*), the one of the two red mullets on sandy and rocky shallows; the plain red mullet (*Trilja tal-ħama*, *M. barbatus*) lives on mud, deeper. Shown as **Trilja**.

## Size
- **Size in game:** the model is 0.94 blocks long (15 px), 4 px deep, 2 px wide: the same length as a vanilla cod, a little slimmer at the rear. Body box 0.45 x 0.3 (unchanged). The first plan was 13 px; the model was drawn at cod length so the barbels and the two dorsal fins have room.
- **Why:** a real one is about 25 cm†. About 4 times life size, like the other small fish.

## Behaviour, spawns, rarity
- **Behaviour:** swims in small groups just over sand (0.2 to 1 block up), as if nosing the bottom with its barbels; shies from players. Health 3.
- **Spawns:** only over sand, gravel, clay or mud. `bahar_sea`, `dwejra_bahar_sea`, `qawra_inland_sea` weight 8; the sand patches of `posidonia_meadows`, `dwejra_posidonia_meadows` weight 4; groups of 2 to 4. Vanilla: warm and lukewarm, weight 4.
- **Rarity:** common.
- **Stings:** no.
- **Drops:** itself (1 raw fish, `mimcontent:trilja`). Bucket, spawn egg. It is shark bait.

## Art
Made overnight by a maker, judged by a fresh critic each round from pictures only. Photos: free Wikimedia Commons ones (licences in `art/references/fish_trilja_refonly/list.tsv`), colour from fresh Mediterranean catches out of the water. The species is *M. surmuletus*, so it has the yellow line and the striped first dorsal fin. Made to look clearly different from the [[Night log/marzpan|marzpan]] (scarlet, deep, grey cheek, square tail): rosy pink, not scarlet, slimmer, a white belly, barbels and a forked tail.

**3D model** (`art/src/fish_trilja_model.py`): **gave up after 8 rounds**; the round 8 version is installed.
- Three paint jobs: A rosy pink-red, B orange-red (the first try), C soft coral. **A chosen**: B was too close to the marzpan's scarlet.
- **Looks:** a steep, blunt head that steps down 1 px at a time from the back to the snout, the eye high on it under a rose row. A red back, a rose upper flank, a gold line along the middle of the flank from behind the head, a pale pink lower flank and a white belly. A first dorsal in two rows (a pale stripe over a dark rose band), a low second dorsal set well behind it, an anal fin under the rear and a forked rosy tail. No pectoral fins: lying on land, their shaded face showed as a grey bar beside the eye.
- **Colours:** back #c44e54, head #d8605e, flank #ec8c86, line #f0c040, belly #fff6f2, barbels #f6ead2, tail #f6aca2, dorsal stripe #c05660.
- **The barbels were the sticking point.** Every critic wanted them readable but not a beard, a moustache, legs or tusks, and they disagreed on the direction: tucked back along the throat (rounds 1 and 5), forward and down (rounds 4 and 6), straight down (round 7). Tried: a 2 px block under the chin (beard), a 2 px hook (beard), a flat strip (chin pad), hanging straight down (one post), angled forward (tusks or legs), lying back (a plank), and finally two 2 px strands, one at each cheek, hanging down and 15 degrees back. At 1 px wide they always read as one solid piece side on.
- Fixed along the way: a duck-bill snout, a checkerboard first dorsal, a grey belly slab, a dark ledge over the eye, the yellow line stopping short, a lone tail pixel, the first dorsal looking like a chimney.
- **Rounds 1 to 8: all FAIL**, each "close". Round 8 still asked for: thinner barbels at the chin tip (not under the eye), the belly paler pink-white and flush with the flank, clearer stripes on the first dorsal, a less saturated back on land, a 1 px smoother step from head to back, and squarer tail lobes.
- A new review shot, `fish-trilja-lineup` (trilja, cod, cerna, small tonn in one tank), was added to the fish test.

**Item icon** (`art/src/fish_trilja_icon.py`): **passed in round 4 of 8.**
- Head lower left, tail upper right, like vanilla's fish. Colours: the model's lifted for out of the water, with a deeper rose back, a dark rose belly rim and a soft gold line, so it is lit from the top left like vanilla's.
- Round 1 FAIL: a straight pink stick, lit from below. Round 2 FAIL: too stubby, a horn over the head, twig-like tail. Round 3 FAIL: washed out, barbels like feet, the line too high. **Round 4 PASS.** Two of its polish fixes were then applied: the dark run under the eye made paler (it could read as a frown), and a lone pale pixel by the anal fin made dark rose.
- Candidates: A (two barbels on a diagonal at the chin), B (one barbel), C (a joined pair). **A chosen** (B loses the barbels, C reads like a beard).
- **Blind reads** (three fresh readers, neutral file names, among vanilla fish, bread and the marzpan), their first lines:
  1. "Slot 3 is a pink fish, probably modded. It is slender and pink, lighter on the belly, with a forked tail. My best guess is a red mullet (Mullus), with a pink seabream or pandora (Pagellus) as the other likely species."
  2. "Slot 3 looks like a slender pink-red fish with pale yellow lines along its side. My best guess is a striped red mullet (Mullus surmuletus), but I'm not sure."
  3. "Slot 3 is a slender pale-pink fish with darker red streaks along its body and a forked tail. My best guess is a mod fish, a red mullet type (Mullus) or possibly a common pandora / pink sea bream."
- All three guessed red mullet first and told it from the marzpan (slimmer, paler, striped). Reader 3 still thought the marzpan looked more like a red mullet; two named a pink sea bream as the second guess.

**Bucket** (`art/src/fish_trilja_bucket.py`): **passed in round 2 of 8.**
- On vanilla's cod bucket, the head rises out of the water facing up and left: a steep forehead, the eye high on it, the rose cheek, a pale blunt chin with one cream barbel hanging straight down, then the body diving into the water with the rose back, the gold line and the pale belly. The back rim outline stays dark except behind the head. Same colours as the icon.
- Candidates: A (one barbel from a blunt chin), B (two barbels), C (the head a row lower). **A chosen** (B's two pale pixels in front of the snout read as a beak; C shows less fish).
- Round 1 FAIL: a barbel pointing forward beside a dark mouth pixel read as a bird's bill. **Round 2 PASS.** Its five small fixes were then applied: plain pink behind the eye (it read 2 px wide), a vertical forehead, a rose edge over the barbel so it shows, and no lone dark pixel at the mouth or the waterline.
- **Blind reads**, first lines:
  1. "Slot 3: a bucket of water with a pale pink fish in it. Its exact species can't be read at this resolution. It looks like a pink, red mullet type of fish, and I can't tell it apart from the vanilla salmon bucket with any confidence."
  2. "Slot 3: a bucket holding a pink fish. It is most likely a red mullet, though it could also be read as the vanilla bucket of salmon."
  3. "Slot 3 is a bucket holding a pink, pale-bellied fish. I can't name the species with confidence. My best guess is a red mullet; a pink sea bream is also possible."
- All three guessed red mullet and all told it from the marzpan's bucket (a deeper red with blue marks). Two said it could be taken for a salmon bucket at this size.
- The spawn egg is still a placeholder (not part of tonight's job).

## Egg

**Owner 2026-11-19: passes** ([[2026-11-19 Spawn eggs - all eight pass]]).
**Spawn egg** (`art/src/fish_trilja_egg.py`, shared parts in `art/src/fish_egg_common.py`), 2026-11-19: **passed in round 1 of 3**; A2 installed, waiting for the owner. Started because the bucket was accepted ([[2026-11-19 Night fish icons and buckets - most pass; John Dory, gallinella, lingwata bucket redo]], [[2026-11-18 Approving a step starts the next; skorfna bucket]]).
- **Design:** vanilla's fish-egg outline and vanilla's own pool, in the accepted icon's colours plus the model's deepest red (#a8424a) for the outline in the shade. Only two features: the gold line along the flank and the striped first dorsal fin. The red back is lit at the top left, the rose flank runs into a pale pink belly, and the side flaps are the pale pink fins. No eye, no face, no barbels (on the model and icon they always read as a beard, tusks or legs).
- **Candidates:** A, the gold line on a diagonal from the lower front up to the back, as on the icon; B, the line as a ring round the egg (a U), with a fainter second line; C, A with a second, paler line under it. Before the critic, the maker's own look at 1x moved the fin: a small fin standing on the egg's tip read as a stem (an onion), so it now lies low over the top and slopes back onto the shoulder, its dark band being the egg's top edge.
- **Critic round 1: PASS, pick A**, with fixes, all applied (A2): "(12,10) -> m, (12,11) -> m: the lower-right flank is still the light rose o right up to the D rim. The measured light balance is TL-BR -0.02, so the lit top-left is no brighter than the lower right"; "(11,12) -> m"; "(7,2) -> K: the pale cream F on row 2 sits nearly centred on the egg's tip. At 1x it reads as a pale nub on a pink dome, which is a mild anatomical-reading risk"; "(4,8) -> h: this widens the lit shoulder by one pixel". On B: "B's U-shaped line, with Y under it, is a band across the middle. The owner rejected that once already because it read as a Pokéball." On C: "C's second, paler line Y blends into the pale belly q at 1x."
- **Blind reads, round 1** (three fresh readers, A, B and C in slots 2, 5 and 8 among vanilla eggs; none could tell them apart), word for word:
  1. "A spawn egg in pink or salmon with a yellow-orange diagonal stripe across it and a paler pink belly. My first impression is a red mullet (Mullus surmuletus, a pink fish with yellow side stripes); a red sea bream is my second guess."
  2. "My first impression is a fish spawn egg, salmon-pink with a wavy yellow-orange band along the side and a paler belly. It reads most like a red mullet (Mullus, Maltese trilja), since that is the pink fish with a yellow side stripe. It could also pass for a pink sea bream."
  3. "First impression: a pink/rose spawn egg with a yellow-orange diagonal stripe along the side and a paler belly. It reads as a sea fish, most likely a red mullet (striped red mullet, Mullus surmuletus), because of the pink body and yellow lateral stripe."
- **Blind reads, A2** (three fresh readers, the egg alone among eight vanilla water-mob eggs):
  1. "A pink spawn egg with a paler pink diagonal band. My first thought was a pink or red fish, probably a red mullet or a pink sea bream, but nothing on it points clearly to one species."
  2. "A spawn egg in pink and salmon with a pale cream diagonal band across the lower half. It reads as a pinkish-red fish. My first guess is red mullet or a pink sea bream, but nothing on it points to one species."
  3. "A spawn egg, pink-salmon with a paler diagonal band across the lower half. It looks like a pink or red fish, maybe a red mullet or a pink sea bream (pandora)."
- All six readers named red mullet first. Alone, the gold line read paler (cream) than beside its two variants.
- **Compare sheet:** `art/candidates/fish_trilja_egg.png` (not in git).

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [FishBase, *Mullus surmuletus*](https://www.fishbase.se/summary/Mullus-surmuletus.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.
