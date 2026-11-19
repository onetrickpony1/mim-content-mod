# Ħmar (triggerfish): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** grey triggerfish, *Balistes capriscus*, **Ħmar** in the species report. Id `hmar`.

## Size
- **Size in game:** the model is 1 block long with the tail (16 px), 8 px deep in the body and 13 px (0.81 blocks) from the trigger's tip to the anal fin, 3 px thick. Body box 0.55 x 0.7 (unchanged). A first model 19 px long stood taller than the cerna in the lineup, so it was made smaller.
- **Why:** a real one is about 40 cm†, deep-bodied. About 2.5 times life size: deeper and a little longer than the cod, smaller than the cerna.

## Behaviour, spawns, rarity
- **Behaviour:** over rock, 0.5 to 3 blocks up, alone or in twos, shies from players. Health 6. (Real triggerfish can nip divers when guarding a nest; not done.)
- **Spawns:** only over rock. `bahar_sea`, `dwejra_bahar_sea`, weight 5, groups of 1 to 2. Vanilla: warm and lukewarm, weight 2.
- **Rarity:** uncommon.
- **Stings:** no.
- **Drops:** itself (1 raw fish, `mimcontent:hmar`). Bucket, spawn egg. It is shark bait.

## Art
Made overnight by a maker, judged by a fresh critic each round from pictures only. Photos: free Wikimedia Commons ones (licences in `art/references/fish_hmar_refonly/list.tsv`); colour from the two FDA photos of fresh fish out of the water, shape also from photos taken under water in Sicily and the Atlantic.

**3D model** (`art/src/fish_hmar_model.py`): passed in round 5 of 8.
- Three paint jobs tried: A olive-grey, B cooler blue-grey (like the aquarium photos), C warmer brown-grey (like the FDA photo). **A chosen**: the critic found B melts into the water and C reads as a bream.
- **Looks:** a deep diamond. A long straight forehead runs down to a small mouth (one darker grey pixel at the tip, the lips grey, no mouth line). The eye is high and far back, the only black pixel, with plain grey round it. The trigger is a stout dark spine raked back with a pixel of membrane behind it. Behind a gap come the long soft dorsal and anal fins, mirror images, ending at the tail's base, paler than the back with a paler trailing edge. Two faint darker saddles cross the back, the back is dark olive-grey and the belly pale cream (dark back, pale belly). The lyre tail has a solid fan, a curved-in back edge and pointed tips.
- **Colours:** back #74725e, crown #6c6a56, saddles #686654, flank #aeaa94, belly #e0dbc9, fins #a5a08a (trailing edge #c2bda7), trigger #626052, tail #8f8b77, eye #0e0f0f.
- **No pectoral fins:** the real ones are small and pale. As a pale bar under the eye they read as an eye and a mouth, and on land as a dark dash by the eye, so they were left out.
- Round 1 FAIL: the pectoral fin made a face, the eye sat low near the snout, the snout was a blunt wall and the belly too grey under water. Round 2 FAIL: round, like a piranha, and the trigger and soft dorsal read as two horns. Round 3 FAIL: the trigger was a straight post (a chimney) and the tail lobes read as antennae. Round 4 FAIL: the eye got lost among the dark saddles under water, and the fish was taller than the cerna. **Round 5 PASS.**
- Optional polish the critic suggested, not done (left for the owner): soft fins that mirror each other even more closely, the trigger a pixel narrower at its tip, slightly stronger saddles on the flank, longer tail tips, and one shade softer on the grey line under the pale belly, which from above on land reads "slightly like a grin".
- A new review shot, `fish-hmar-lineup` (hmar, cod, cerna, small tonn in one tank), was added to the fish test.

**Item icon** (`art/src/fish_hmar_icon.py`): passed in round 3 of 8.
- **Pose: side on, head left, not diagonal** like vanilla's fish. Drawn on the diagonal first, the diamond became a square blob (the forehead and back turned into a vertical and a horizontal wall). The critics agreed side on is right for this shape. The icon is the passed model's own side view, one pixel per model pixel.
- Colours: the model's own tones, not lifted x1.2: lifted, the fish read white in the hotbar (lighter than every vanilla fish). Then the whole fish about 10% darker and a little greener (round 1), with a darker olive edge round the fins and tail tips (round 2).
- Candidates A, B, C differ only in the blotches. **A chosen** (two soft blotches; the critic: C's looked like bars).
- Round 1 FAIL: the eye too near the mouth, a flat belly stripe, the palest fish in the hotbar, light coming from the wrong side. Round 2 FAIL: still pale and flat on the light backdrop, a straight belly edge, the eye merging with the blotches, a slight "piranha" open jaw. **Round 3 PASS.** Optional polish not done: smoother steps along the dorsal and anal fins, darker tail tips, fewer colours (it uses 20, vanilla's top).
- **Blind reads** (three fresh readers, neutral file names, among vanilla fish), first lines word for word:
  1. "Slot 3: a fish, most likely a sea bream (my best guess is a white seabream / sargo), though I'm not sure of the species."
  2. "Slot 3: a fish, most likely a spiny-finned Mediterranean rockfish such as a scorpionfish or a small grouper. I can't name the species with confidence."
  3. "Slot 3: a raw fish, a dull grey-olive spiny-finned sea fish, most likely a sea bream type (porgy/bream). It could also be a grey mullet or a dull scorpionfish; I can't tell which species for sure."
- All three saw a deep, grey-olive, spiny-backed sea fish; **none named a triggerfish.** For the owner to judge.

**Bucket** (`art/src/fish_hmar_bucket.py`): passed in round 1 of 8.
- On vanilla's cod bucket, the head rises out of the water facing up and left: the small dark mouth at the snout's tip, the forehead running down to the right, the eye high and far back with grey round it, the trigger spine up from the back, a faint blotch, then the body diving into the water with the pale belly on the left. The back rim stays dark except behind the head. Candidates: A (head high, trigger showing), B (head a row lower), C (no trigger). **A chosen** (the critic: B looks like a frog peeking out, C loses the spine).
- After the pass, two of the critic's small polish fixes were applied: one more pixel joins the trigger to the back (it stood alone like an antenna), and the belly's edge at the waterline is a softer dark, so the eye is the only dark dot. Not done: moving the eye a pixel further back.
- **Blind reads**, first lines word for word:
  1. "Slot 3: a bucket of fish. The fish is a pale grey-olive (sandy) one, maybe a small bottom fish like a goby or a sea bream, but I can't tell which species."
  2. "Slot 3: a bucket with a live fish in it, a drab olive-grey, blotchy fish standing head-up. My best guess is a dusky grouper or a similar mottled rock or bottom fish, but I'm not confident about the species."
  3. "Slot 3: a bucket holding a fish, most likely a dull grey-olive fish such as a grey mullet or a grouper. I can't be sure which kind."
- All three saw a bucket with a plain grey-olive fish; none could name the species.
- The spawn egg is still a placeholder (not part of tonight's job).

## Egg

**Owner 2026-11-19: passes** ([[2026-11-19 Spawn eggs - all eight pass]]).
**Spawn egg** (`art/src/fish_hmar_egg.py`, shared parts in `art/src/fish_egg_common.py`), 2026-11-19: **failed all 3 critic rounds**; the best try, C4 (round 3's fixes, not judged again), is installed and waits for the owner. Started because the bucket was accepted ([[2026-11-19 Night fish icons and buckets - most pass; John Dory, gallinella, lingwata bucket redo]], [[2026-11-18 Approving a step starts the next; skorfna bucket]]).
- **Design:** vanilla's fish-egg outline and vanilla's own pool, in the accepted icon's colours only. Features: the trigger spine, and two soft darker saddles (never level, so no pair of eyes) on the olive-grey flank over a pale belly. Lit at the top left; the side flaps are the soft fins. No eye, no face.
- **Candidates:** A, two soft blotches; B, the same blotches bigger and darker; C, A with a darker back cap. Before the critic, the maker's own look at 1x dropped long saddle bands that ran up to the top (a striped garlic bulb).
- **Critic round 1: FAIL, pick C.** "No candidate reads as a triggerfish at 1x. Blind readers saw camouflage mottling, and the "trigger" shows only as a 1 px dark stalk on the egg's pointed tip. The sail behind it is pale `f`, about the same as the slot grey, so it disappears at 1x and 2x. The top reads as an onion or garlic point, not a fin. Next to the skorfna egg it is the same kind of thing (a mottled bottom-dweller egg with a spike on top), just in grey." Fixes applied (C2): a 2 px dark base to the spine (7,2) o and a step down to the back (8,2) U; the blotches' dark cores softened (6,6) (9,9) q; three pale specks on the flank made s (4,8) (3,9) (7,10).
- **Critic round 2: FAIL.** "It is still an onion with a point on top. At 1x and 2x, in both hotbars, C2's outline runs straight up from the egg into the spine. ... Making (7,2) o and (8,2) U just thickened the cone." "The changes don't show at 1x." "What already works: the mottling is calmer, it is clearly not the skorfna (different colour, no comb), there is no face or level dark pair, it is lit from the top left and the pool is correct." Fixes applied (C3): vanilla's rounded top back, the trigger moved onto the front shoulder (5,2) (5,3) o, the crown lit (6,3) (6,4) L.
- **Critic round 3: FAIL.** "At 1x and 2x the spine at (5,2) and (5,3) is invisible as a trigger. It sits straight above the left outline at (5,4) and (4,5), so it reads as that outline carrying on upward. The egg then looks like a lopsided cone with its tip off to the left, which is still the onion/garlic read with the point moved, not a spine." "At 1x, C3 is almost the same as A, B, C and C2." Fixes applied (C4, installed): the spine a 2 px thorn raked back over the crown (5,3) (6,2) o with a dark root (5,4) o; a wider pale belly (6,10) (6,11) W. Its optional fix, darker K cores in both saddles, was not done.
- **Blind reads, round 1** (three fresh readers, A, B and C in slots 2, 5 and 8 among vanilla eggs; none could tell them apart):
  1. "A spawn egg in grey-olive, mottled with darker green-grey blotches like camouflage. My first impression is a fish that hides on rocks, such as a scorpionfish or a young grouper; it could also be an octopus or cuttlefish. Nothing about it points clearly to a species."
  2. "A spawn egg in mottled grey-olive with darker blotches, like camouflage. It suggests a rock-dwelling or bottom fish such as a dusky grouper or a scorpionfish. It could also be read as a cuttlefish or octopus, and nothing on it clearly says "fish"."
  3. "First impression: a dull olive/grey-green spawn egg with darker mottled blotches. It reads as a camouflaged bottom fish, my guess being a grouper or a scorpionfish. It could also be a cuttlefish or octopus, since there is no clear fish feature."
- **Blind reads, C2** (alone among eight vanilla water-mob eggs):
  1. "A dull grey-olive spawn egg with darker blotches. It reads as a camouflaged bottom fish, maybe a grouper or a scorpionfish. It could also be a mola mola, but I'm not confident."
  2. "A spawn egg in dull olive-khaki with darker grey-green speckles. It reads as a camouflaged, sandy-bottom creature, my first guess a flatfish such as a sole or flounder, or possibly a toad."
  3. "A spawn egg, dull grey-olive with darker blotches. My first impression is a camouflaged bottom fish, maybe a scorpionfish or grouper. It could also be a cuttlefish or octopus."
- **Blind reads, C3** (alone among eight vanilla water-mob eggs):
  1. "A spawn egg in pale grey-khaki with darker olive speckles and a slightly pointed, lumpy top. It reads as a camouflaged bottom creature. My first guess is a scorpionfish (rockfish), and my second is a mottled cuttlefish or octopus."
  2. "A spawn egg, pale olive-grey with darker mottling and no clear features ... My first impression is a stone or rock colour. I can't pin down the creature; my best guess is a bottom fish that hides against rock, such as a scorpionfish"
  3. "At first glance it's a spawn egg ..., mottled olive-grey and khaki with a rough, rocky look. It most likely stands for a camouflaged rock-dwelling fish, perhaps a scorpionfish or a grouper ... at normal size it could pass for a plain stone or a mossy rock."
- **No reader named a triggerfish**, as with the icon and bucket. C4 had no blind read. For the owner to judge at 1x; a different idea may be needed (the trigger is too small to carry the egg at 16 x 16).
- **Compare sheet:** `art/candidates/fish_hmar_egg.png` (not in git).

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [FishBase, *Balistes capriscus*](https://www.fishbase.se/summary/Balistes-capriscus.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.
