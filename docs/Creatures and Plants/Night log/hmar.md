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

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [FishBase, *Balistes capriscus*](https://www.fishbase.se/summary/Balistes-capriscus.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.
