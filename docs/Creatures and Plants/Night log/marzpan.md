# Marzpan (parrotfish): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** Mediterranean parrotfish, *Sparisoma cretense*, **Marzpan** (also *Pappagall*) in the species report.
- **Colour:** the placeholder is the red female with a yellow saddle; the male is grey. One colour for now; a second version (like the two skorfna) is an option.

## Size
- **Size in game:** 0.88 blocks long (14 px), body box 0.5 x 0.4. Like the sardina in length, but deeper. (The art model came out 15 px, 0.94 blocks; the body box is unchanged.)
- **Why:** a real one is about 20 to 30 cm†. About 3 times life size, so it reads beside a cod.

## Behaviour, spawns, rarity
- **Behaviour:** swims 0.5 to 3 blocks above a rock floor, in groups of up to 3, shies from players. Health 4.
- **Spawns:** only over rock. `bahar_sea`, `dwejra_bahar_sea`, `qawra_inland_sea`, weight 8, groups of 1 to 3. Vanilla: warm and lukewarm, weight 3.
- **Rarity:** common in the shallows. A visual census on Maltese reefs found it at high densities (it is a warm-water fish that is doing well).
- **Stings:** no.
- **Drops:** itself (1 raw fish, `mimcontent:marzpan`). Bucket, spawn egg. It is shark bait.

## Art (night job, made in order: model, icon, bucket)
Photos used (reference only, free licences, list in `art/references/fish_marzpan_refonly/list.tsv`): two divers' photos taken off Gozo, a fish market (for the true colours out of water), and divers' photos of red females and a grey male.
- **Which colour:** the red female, which reads best. The grey male could come later as a second version, like the two skorfna.

**3D model: passed in 5 critic rounds**
- Picked candidate A of three. A has the grey cheek patch, the yellow stripe under it and the yellow saddle. B has no cheek stripe, and C has a deeper belly.
- 15 px long (0.94 blocks), 7 px deep, 4 px thick. A little longer and deeper than the cod, much smaller than the awrata and the cerna. The first build was 17 px long; the snout was cut back in round 1 and the beak block came off in round 2.
- Blunt red head, the forehead stepping down 1 px at a time, the chin stepping up. The mouth is a mid-red line across the front of the snout: no pale "beak" block, which read as a tongue.
- Scarlet red, dark along the back and pink toward the belly (dark back, pale belly). Faint scale rows on the flank. The red is lighter and warmer than the photos so it stays red, not purple, under water.
- A grey-lilac cheek patch with a darker back edge (the gill cover). The black eye sits at its front, with a gold ring above, behind and below it and deep red in front.
- A yellow stripe under the cheek, and a yellow saddle on the top of the tail stalk only.
- A long, low dorsal fin, 1 px above the back, with a darker top edge so it shows under water. A small anal fin, small orange-red pectoral fins, and a square-cut tail that sways. No pelvic fin, so the belly is one smooth line.
- Round 1: FAIL (a pig-like snout, a dull eye, purple under water). Round 2: FAIL (a boxy hump, the pale lip, a cartoon eye). Round 3: FAIL (a flat pale block on the belly, a saddle like a collar). Round 4: FAIL (a flat front to the head, the belly as one square). Round 5: PASS.
- Left as suggestions from round 5 (not done): a smoother, less blotchy flank; a paler belly; the grey patch reaching over the top of the head like a hood; a gentler arch to the back.
- **Against the owner's rule "gold beside the eye reads as a beak":** two critics asked for the real gold eye ring on the model. It is there on the 3D model, but kept off the snout side of the eye. Worth a look.
- Size check: in the tank beside a cod, the cerna and a small (2 block) tonn, it is a bit bigger than the cod and well under the cerna and tonn.
- A new review shot, `fish-marzpan-lineup` (marzpan, cod, cerna, small tonn), is in `FishCheck`.

**Item icon: passed in 2 critic rounds**
- Head lower left, tail upper right, like vanilla's fish.
- Picked C of three: A with a small pectoral fin on the flank. A had the cheek stripe; B had none and read as a plain red fish.
- Colours: the model's own. The brief said to lift them about 1.2 times for out of water, but the model's reds are already full red, so a lift only washed them out pale. Two darker red-browns were added for the outline.
- Round 1: FAIL. The light came from below (the brightest red was on the belly), and the snout and belly were straight walls. Fixed: a light run inside the back, the belly side in shade, a 2 px blunt snout with the mouth corner at its foot, and gold behind the eye only. Round 2: PASS.
- The belly is now in shade, as the light from the top left asks, so the icon's countershading is weaker than the model's.
- Blind readers (each among an apple, tropical fish, cooked salmon, pufferfish, beetroot and raw salmon), first lines word for word:
  - "A red-orange fish with a yellow-orange tail, possibly a red mullet (or a goldfish-like red fish)."
  - "A red-orange fish, probably a red mullet, or possibly a raw salmon."
  - "A red-orange whole fish, slim, probably a red mullet (or a similar red sea fish). It looks like the same item as hotbar slot 4."
- All three see a red fish, but none says "parrotfish". They guess the trilja, which is also red. The owner may want the grey cheek bigger so the two don't get mixed up once the trilja is drawn.
- Left as suggestions from round 2 (not done): a less straight right edge and belly, a 2 px start to the dorsal fin, a softer yellow on the saddle, a darker bottom corner on the tail.

**Bucket: passed in 2 critic rounds**
- Only the head comes out of the water at the upper left; no tail. The back of the rim stays visible.
- Picked A over B (no cheek stripe, a plain red fish) and C (its fin covered the rim's corner).
- Round 1: FAIL. The gold ring and the stripe made an L-shaped yellow blob behind the eye, like a beak. Fixed: no gold beside the eye, the stripe moved two columns back and toned down, the mouth lightened so it stands apart from the rim, and the crown lit from the top left. Round 2: PASS.
- Blind readers (each among a water bucket and the salmon, tropical fish, axolotl, lava and pufferfish buckets), first lines word for word:
  - "A bucket of water holding a small red fish, with a red and pink body under the blue water at the top (maybe a red mullet or a red tropical fish)."
  - "A bucket of water holding a red-orange fish with some blue on it, maybe a wrasse or a red mullet. It looks like slot 4."
  - "A bucket of water holding a red fish with a pale grey-lilac head, a black eye and a yellow fin (it looks like a red mullet or a gurnard); it is the same item as hotbar slot 4."
- Left as suggestions from round 2 (not done): a darker fin edge behind the head, a rounder top to the snout, a darker mouth, and a shaded lower edge to the cheek.

**Egg** (`art/src/fish_marzpan_egg.py`, 2026-11-19): passed in round 2 of 3. **Owner 2026-11-19: passes** ([[2026-11-19 Spawn eggs - all eight pass]]).
- Started because the owner approved the bucket ([[2026-11-18 Approving a step starts the next; skorfna bucket]]). A plain scarlet egg in vanilla's outline and vanilla's own pool, in the icon's colours only, lit from the top left. Its features are the grey-lilac cheek patch on the lower front and the yellow stripe under it. No eye, no face, no beak.
- Candidates: A (cheek and stripe only), B (A with the yellow saddle slanting over the upper back), C (A with darker scale marks). Then A2 from the critic's fixes (the back darker toward the upper right, the cheek lighter). **A2 chosen.**
- Round 1 PASS with fixes, pick A: "At 1x it reads as 'red egg, pale mark at bottom-left'. That is enough, but only just." B: "the yellow streak reads as a flame or highlight rather than a tail saddle"; C: "the scales are pale specks scattered over the body". Round 2 PASS on A2: "It is the best of the four". Its optional polish, not done: the darkest back red along the right shoulder.
- **Blind reads** of A2 (three fresh readers, neutral file names, the egg in slot 4 among vanilla eggs), first lines word for word:
  1. "**bar2:** A bright coral-red egg with a small grey-white patch at the lower left. I read it as a red fish: a red mullet, a scorpionfish, or a red bream."
  2. "**bar2:** A spawn egg that is mostly bright red or coral, with a grey patch low on the left and a little yellow at the bottom. It reads as a red fish, most likely a red mullet. A scorpionfish is a second guess."
  3. "**bar2.png:** A rounded coral-red spawn egg with a small grey-white patch low on the left and a bit of yellow at the base. It reads as a red fish, something like a red mullet or a scorpionfish."
- All three read a spawn egg for a red fish; none named a parrotfish (two said red mullet first).
- Sheet: `art/candidates/fish_marzpan_egg.png`.

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- "The rocky reef fish assemblages of Malta and Lampedusa islands (Strait of Sicily, Mediterranean Sea): a visual census study in a changing biogeographical sector", Journal of the Marine Biological Association of the UK (Cambridge, 2013†): *S. cretense* and *T. pavo* at high densities
- [FishBase, *Sparisoma cretense*](https://www.fishbase.se/summary/Sparisoma-cretense.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.
