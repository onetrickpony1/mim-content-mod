# Pixxi San Pietru (John Dory): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** John Dory, *Zeus faber*, **Pixxi San Pietru** in the species report. The dark spot on its side is "St Peter's thumbprint".

## Size
- **Size in game:** 1.38 blocks long with the tail (22 px; the body alone is 18) and 1.32 tall from the spine tips to the pelvic fins, only 2 px thick. Body box 0.6 x 0.8 (unchanged). First planned at 1.06 long; the drawn fish came out longer once the jaw and the rounded tail were added.
- **Why:** a real one is about 40 cm† long and very tall for its length. About 3 times life size, like the other small fish; beside the cerna it is a little shorter and about as tall with its spines, and much bigger than a cod.

## Behaviour, spawns, rarity
- **Behaviour:** alone, slow (movement speed 0.45, other fish 0.7), shies from players like vanilla fish. Health 6.
- **Spawns:** mid-depth: in open water at least 5 blocks below sea level, any floor. Deep sea (`fond_deep_sea`, `fond_band_1`-`8`, `dwejra_fond_deep_sea`), weight 3, alone. Vanilla: lukewarm and deep lukewarm, weight 2.
- **Rarity:** uncommon.
- **Stings:** no.
- **Drops:** itself (1 raw fish, `mimcontent:pixxi_san_pietru`). Bucket, spawn egg. It is shark bait.

## Art
Made overnight by a maker, judged by a fresh critic each round from pictures only. Photos: free Wikimedia Commons ones (licences in `art/references/fish_pixxi_san_pietru_refonly/list.tsv`), colour from fish out of the water at the market and on the boat, shape from fish swimming in the Mediterranean.

**3D model** (`art/src/fish_pixxi_san_pietru_model.py`): passed in round 7 of 8.
- Three paint jobs tried, all on the same model: A the spot with a soft edge all round, B the edge only at the sides and below, C as A with faint wavy streaks on the flank (like the Mediterranean photo). **B chosen** (the critic: the smoothest belly; C's streaks looked like teeth under the spot).
- **Looks:** a tall, very thin oval disc, 2 px thick. A dark olive back, golden-olive flanks and a pale belly. St Peter's thumbprint is a soft mid brown-olive smudge a little above the middle of the side, with no ring. The eye is near the front, high on the head: a 2 x 2 black pupil in a round cream ring, the only ringed, high-contrast mark. A wedge of lower jaw juts up and forward past the upper lip. On the back there is a dark membrane strip with four thin spines swept back at 45 degrees, the front one longest, ending in filaments. A low soft dorsal and anal fin run back to a rounded tail, and there are long pelvic fins under the throat.
- **Colours:** back #5b5641 to #8f875f, flank #ab9d66 / #c3ae70, belly #e4ddc2 / #f6f4ea, spot #6e5e3a with a #9a8b5e edge, eye ring #efe6c4.
- **The hard part was the spot.** Every critic in rounds 1 to 6 read it as a second eye or a face, in different ways:
  - a dark centre in a gold ring read as an iris;
  - a flat 4 x 4 square read as a pupil;
  - a cut-corner disc read as a cross;
  - a 6 x 6 disc filled half the body.
  What finally worked was to make the eye stand out instead (bigger, black, cream ring) and the spot a softer, lighter smudge with no ring.
- Round 1 FAIL: spot like a big pupil, spines like a comb, pale pectoral fin under the spot like a mouth (fins removed). Round 2 FAIL: spot still an eye, spines like a rake. Round 3 FAIL: square spot, spines like antennae, jaw a nub. Round 4 FAIL: spot a cross, eye googly, jaw like a stick. Round 5 FAIL: spot too big and gold like the eye. Round 6 FAIL: eye and spot both dark blobs under water. **Round 7 PASS.**
- The critic's optional polish, not done (left for the owner): a taller, angled 2 px jaw with a mouth line (the critic called it "close to blocking"), a rounder arch on the flat top of the back, a faint halo round the spot, a shorter back spine, and a lighter tail edge.
- The critics disagreed with each other several times (a gold ring asked for, then rejected; 2 px spines asked for, then 1 px). Each round followed the latest critic.
- A new review shot, `fish-pixxi_san_pietru-lineup` (this fish, cod, cerna, small tonn in one tank), was added to the fish test.

**Item icon** (`art/src/fish_pixxi_san_pietru_icon.py`): passed in round 8 of 8, the last allowed round.
- Head lower left, tail upper right, like vanilla's fish. Candidates: A golden olive (the Mediterranean photo), B a greyer olive (the market photos), C as A with a lighter spot. **A chosen** (B looked washed out).
- Round 1's level, side-on version read as a round cartoon face or a pufferfish, so it was redrawn on the diagonal.
- **Looks:** a thin oval, lit from the top left, with a dark olive outline. The eye is one black pixel with a pale gold pixel above it. The spot is a flat warm dark 2 x 2 (#504228) with no ring. There are three slanted spines joined by membrane on the back half, a dark jutting lip with a gape, a forked tail on a short stalk, and small anal spines and a pelvic fin underneath.
- Round 1 FAIL: a face and a pufferfish, no jaw, lit backwards, too heavy. Round 2 FAIL: lit backwards, the spines like insect legs, the tail like antlers. Round 3 FAIL: the eye and spot like two eyes, too pale. Round 4 FAIL: the ringed spot an iris. Round 5 FAIL: a round bean with a crown of spikes. Round 6 FAIL: spines like hair, the tail loose. Round 7 FAIL (narrowly): the ring back on the spot, grey spines. **Round 8 PASS (narrowly).** After the pass, one of its polish points was applied: the spot made one flat dark so it shows at 1x.
- Polish not done: a protruding upper lip, a gap between the last spine and the tail, and a slimmer belly.
- **Blind reads** (three fresh readers, neutral file names, among vanilla items), first lines word for word:
  1. "Slot 3: a fish, olive-tan with dark speckles and a spiky, ragged fin along its back. It looks like a scorpionfish or a weever, though it could be a small grouper. It's the only item that doesn't look like a vanilla one."
  2. "Slot 3: a fish, olive-tan with darker mottling and a spiky dorsal fin. It has a stocky, perch-like body. My best guess is a scorpionfish or a small grouper, possibly a comber."
  3. "Slot 3: a fish, olive-green with darker mottling and a spiny, ragged dorsal fin. It looks like a scorpionfish or a small grouper/rockfish, not a smooth fish like cod."
- All three saw a spiny fish. None named the John Dory: the spot reads as mottling, not as the thumbprint.

**Bucket** (`art/src/fish_pixxi_san_pietru_bucket.py`): passed in round 2 of 8.
- On vanilla's cod bucket, the head rises out of the water facing up and left. It has the dark jutting jaw with its upper edge lit, the black eye with a pale gold pixel, the spiny fin standing up behind the head, and the body diving to the lower right with the dark spot at the waterline. The back rim outline stays dark except behind the head. Candidates: A (head high), B (head a row lower), C (a taller fin). **A chosen** (the critic: B's fin is too flat and C's spikes read as ears).
- Round 1 FAIL: the jaw vanished on the dark slot, and the two spines read as ears. **Round 2 PASS.**
- Polish not done: a darker jaw tip, more gold in the mid-tones, and a fuller spine row.
- **Blind reads**, first lines word for word:
  1. "Slot 3: A bucket of water holding a fish. The fish is pale sandy tan with a spiky, ragged fin on top, so it is probably a weever or a scorpionfish. I can't be sure at this size."
  2. "Slot 3: a bucket of water holding a sandy-tan fish with a spiky raised dorsal fin and mottled markings. It looks most like a weever or a pale scorpionfish, but I can't be sure."
  3. "Slot 3: bucket of water holding a pale sandy-tan fish with a spiky, raised fin on its back. My best guess is a weever, or possibly a pale scorpionfish. I can't be sure at this size."
- The spawn egg is still a placeholder (not part of tonight's job).

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.
- The icon and bucket read as "a spiny fish" (scorpionfish or weever) rather than a John Dory. A clearer thumbprint is the likely fix, but every ringed spot tried tonight read as a second eye.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [FishBase, *Zeus faber*](https://www.fishbase.se/summary/Zeus-faber.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.
