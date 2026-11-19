# Pixxi San Pietru (John Dory): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** John Dory, *Zeus faber*, **Pixxi San Pietru** in the species report. The dark spot on its side is "St Peter's thumbprint".

## Size
- **Size in game:** 1.38 blocks long with the tail (22 px; the body alone is 18) and about 1.35 tall from the filament tips to the pelvic fins, only 2 px thick. Body box 0.6 x 0.8 (unchanged). First planned at 1.06 long; the drawn fish came out longer once the jaw and the rounded tail were added.
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
- **Looks:** a tall, very thin oval disc, 2 px thick. A dark olive back, golden-olive flanks and a pale belly. St Peter's thumbprint is a soft mid brown-olive smudge a little above the middle of the side, with no ring. The eye is near the front, high on the head: a 2 x 2 black pupil in a round cream ring, the only ringed, high-contrast mark. A wedge of lower jaw juts up and forward past the upper lip. On the back, five thin dorsal spines swept back, joined by membrane about two thirds of the way up, each ending in a long bare filament trailing back (redone, see below). A low soft dorsal and anal fin run back to a rounded tail, and there are long pelvic fins under the throat.
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

## Redo after the owner's review (2026-11-19)
- **The owner said:** "john dory (its spikes look like graphical glitches and are very thick)". Recorded in [[2026-11-19 Night fish models - nine pass, John Dory and petrica redo]].
- **Why it looked glitchy:** the old spines were flat 1 px sheets in the same spot as the fin behind them, so the game flickered between the two, and turned at 45 degrees they looked thick.
- **Now:** five spines, each a rod about a third of a pixel thick, swept back. At about two thirds of the way up each one bends further back into an even thinner bare filament. A paler olive membrane (#a39668) fills between the spines up to that bend, with one clean edge stepping down toward the tail. Nothing lies flat against anything else, so there is nothing to flicker. The rest of the fish is unchanged.
- **Checked in game** from the side, three-quarter, front, behind and straight above (new close-up shots `fish-pixxi_san_pietru-spines-*` in the fish test): no flicker, gaps or parts poking through.
- **Critic rounds:** passed in round 4 of 8. Round 1 FAIL: blunt ends, membrane too low, too dark. Round 2 FAIL: membrane still low, rods like wires. Round 3 FAIL: the glitch and thickness were fixed, but the membrane only covered the bottom third. **Round 4 PASS:** "no z-fighting, flicker, gaps or wrong-depth faces" from any angle.
- Polish not done: a lighter tip on each filament, and shorter spines toward the tail so the crest looks less like a rake from three-quarter view.
- **Icon and bucket not changed:** at 16 px they already show a few spines standing above a membrane-filled fin, which still matches.

## Icon and bucket redo after the owner's review (2026-11-19)
- **The owner said:** "too flat and fat they dont look like the fish". Recorded in [[2026-11-19 Night fish icons and buckets - most pass; John Dory, gallinella, lingwata bucket redo]].
- **Icon now:** side on, head left, like the hmar. A deep diamond, taller than long with the fins: a steep forehead, a big jaw jutting forward, the eye high on the head (black pupil in a pale ring), four thin spines raked back with light filament tips, the thumbprint behind the middle with a hint of pale ring, a narrow tail stalk and a rounded tail, a pelvic spine under the keel. Shaded from the top left down to a darker rim and belly. **C chosen:** a greyer silver-olive with near-black spines, nearer the photos and the model than the golden A and B.
- **Bucket now:** the head and tall front rise out of the water facing left: the pale jaw, the eye behind it, three dark spines standing up, the thumbprint at the waterline, the back sloping into the water. **C chosen** (the same greyer olive).
- **Critic rounds:** 3 of 3 allowed for each, all FAIL, so it is the owner's call.
  - Icon: round 1 a pale ball with fuzz on top; round 2 close (the spot out-darked the eye, the spines a comb); round 3 close (the spines still a crown at 1x, no long pelvic fins, the spot faint). Not done: spines drawn as joined diagonals, a pelvic spine from the throat, a bigger upturned mouth, a darker spot with part of a ring, a narrower tail base.
  - Bucket: round 1 a crown of teeth, no spot; round 2 the eye and spot merged into one hole; round 3 the jaw reads as a beak with a dark stripe, no clear eye, the spot at the waterline reads as a hole, still a low dome. Not done: a cream jaw joined to the head, the eye at (5,2), a steep forehead as the tallest part, the spot moved up and back.
- **Blind reads** (three fresh readers, neutral names, beside vanilla cod, salmon, pufferfish and tropical fish), first lines word for word:
  1. "Slot 3: A raw fish item: a tall, flat, pale olive-beige fish with long thread-like spines sticking up from its back, a dark mid-body mark and a fan tail. It looks most like a John Dory (Zeus faber)." Bucket: "It looks like a "bucket of John Dory"."
  2. "Slot 3: A raw fish item. It is grey-beige and drawn side-on, with a deep, flat, roundish body, a tall comb of spiny dorsal filaments and a small tail. I think it is a John Dory (Zeus faber), though the dark central spot is not clear." Bucket: "probably a John Dory in a bucket".
  3. "Slot 3: a raw fish item. The fish is flat with a tall, round, pale olive-beige body, long spiky filaments sticking up from the dorsal fin, a darker blotch on the side and a small tail. It reads as a John Dory (Zeus faber)." Bucket: "most likely a bucket of John Dory".
- All three named a John Dory (about 60% sure for the icon, 50-55% for the bucket). Before the redo none did.

## Bucket redo 2 (2026-11-19)
- **The owner said:** icon C accepted; "the mouth looks like a magnet or duck bill" on the bucket. Recorded in [[2026-11-19 Redo verdicts - lizz bucket, lionfish, lingwata Q, gallinella, John Dory]].
- **Now:** redrawn from the accepted icon, in its colours. The head rises out of the water facing up and left, kept inside the bucket's left side. The mouth is only a small dark notch under the snout, with the chin a dark line climbing to it: no pale lips, nothing sticking out. The eye is high on the head (black with a cream pixel above). The three dark spines with light tips match the icon, and the thumbprint is two rows above the water. Two candidates: A (the gape a notch under the snout, chosen) and B (the gape opening upward at the tip).
- **Critic rounds:** round 1 A PASS (B's dark wedge read as a small beak). The blind readers after it all still saw a pale bill: the head stuck out past the bucket's left side. Moved a pixel right and toned down; round 2 A PASS ("the mouth can't read as a beak, duck bill or magnet"; B's tan lower jaw read as a flat open bill).
- **Blind reads** after round 2 (three fresh readers, neutral names, beside vanilla buckets), asked about the mouth, word for word:
  1. "it doesn't look like a beak, duck bill or magnet. The pale blob at the upper left reads loosely as a fish's thick-lipped mouth, but at this size it isn't clear."
  2. "the pale tan bump at the upper left reads more like a small beak or duck bill than a fish's mouth, though at this size it is blurry and unclear."
  3. "The mouth looks more like a fish's blunt mouth than a beak, a duck bill or a magnet, though at this size it isn't very clear."
- All three saw a fish in a bucket (75-85% sure) but none named the species (grouper, scorpionfish, goby; two said it could be a toad). The icon beside it is what names it.
- Polish not done: the chin pixel at (4,3) one step lighter, and a second pale eye pixel if the eye reads as a speck.

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.
- The icon and bucket read as "a spiny fish" (scorpionfish or weever) rather than a John Dory. A clearer thumbprint is the likely fix, but every ringed spot tried tonight read as a second eye.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [FishBase, *Zeus faber*](https://www.fishbase.se/summary/Zeus-faber.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.

## Owner's verdict (2026-11-19)
- "All pass except john dory bucket. That needs a redo, consider very different possible version" ([[2026-11-19 Redos pass - lionfish, lizz bucket, petrica, gallinella icon; John Dory bucket again]]).

## Bucket redo 3 (2026-11-19)
- **What changed in-game:** the bucket now shows the John Dory **lying on the water**, its round side up and head to the left. A dark eye sits high on the head, a row of dark spines with light tips fans along its back and sweeps toward the tail, the dark thumbprint sits below the middle, and a small dark mouth angles up at the front. The bucket's dark back rim still shows at the right. Nothing pale sticks out in front of the head.
- **Six very different versions were drawn** instead of another tweak of the old one. All six are on the sheet `art/candidates/fish_pixxi_san_pietru_bucket.png` (at 1x, 2x and 8x, beside the icon and the rejected redo 2), so the owner can pick any of them:
  - **U, upright:** standing on its tail, head up, with the spines streaming down its side (like the sole's bucket). Critic: "a duck or bird head poking up". Dropped after round 1.
  - **S, sail:** only the spiny fin and the top of the back break the water. A weak pass in round 1, then a fail in round 2: "a tan cap or wedge", with no head to see.
  - **F, one-fin sail:** one big front spine. Critic: "a shark fin or a duckling". Dropped after round 1.
  - **T, tilted tall oval:** the whole deep body, head up and to the right, half out of the water. A pass in round 1. Round 3 failed it ("a lumpy, crumpled pile").
  - **L, lying on the water:** **installed.** Critics passed it in all three rounds and ranked it best each time ("clearly a fish head in a bucket at 1x and 2x ... the spiny fanned dorsal with its filaments is the John Dory signature").
  - **D, wide disc:** the top of a big disc across the whole bucket. It failed rounds 1 and 2 ("a burger bun or a lid", "flat and fat"). Round 3 gave it a weak pass ("a round loaf", no mouth), and a mouth was added after that.
- **Critic rounds:** 3, the new limit ([[2026-11-19 Art rounds capped at 3; blind readers on Sonnet]]). Fixes made along the way:
  - the filaments sweep back;
  - the rim shows beside the fish;
  - the thumbprint is rounder but kept out of the eye's row;
  - the mouth line is angled up;
  - the lit pixel in front of the eye is toned down, so nothing glows there like a beak.
- **Blind reads** were done by three fresh readers **on Sonnet**, the new rule. Each got neutral names and saw L in slot 3 and T in slot 6 among vanilla cod, salmon, pufferfish, tropical fish, water and axolotl buckets. Their answers, word for word, were given before the last small round 3 touch-ups:
  1. "Slot 3: Small pale tan/olive spiny-finned fish with a spiky dorsal fin, likely a scorpionfish or a similar rockfish (possibly gallinella, a gurnard). About 30% sure." "Slot 6: Grey-brown fish with pale mottled patches and a dark head, possibly a lionfish or another spiny fish. About 25% sure."
  2. "Slot 3: Probably a small spiny or crested fish (a scorpionfish/gallinella-type or a wrasse-like fish), pale grey-cream and spotted, about 30% sure." "Slot 6: Probably a grey-brown fish with a long, narrow, tilted head, such as a John Dory or a similar grey fish, about 25% sure."
  3. "Slot 3: Looks like a pale tan or olive-grey, spiny-finned fish with a spiky dorsal fin and a dark eye, so my best guess is a small perch or scorpionfish type (for example a painted comber or a wrasse) at about 25% sure." "Slot 6: A grey-green, mottled fish with a pointed snout and a spiky back, so my best guess is a scorpionfish or goby type at about 20% sure."
- **What the reads say:**
  - For L, no reader saw a beak, bill, magnet or second eye ("no beak, bill, magnet or second eye"), and all three saw a spiny fish.
  - No reader named the John Dory for L. One reader named it for T, but saw T's tilted head as "a pointed bill or snout".
  - So L is the safest choice. As before, it is the icon beside it that names the species.
- **Not decided (for the owner):** which of the six to keep. The script switches between them with one letter (`PICK` in `art/src/fish_pixxi_san_pietru_bucket.py`).

## Owner's verdict (2026-11-19, later)
- "John dory bucket: L, all eggs pass, switch back to opus guessers." ([[2026-11-19 John Dory bucket L; last four eggs pass; blind readers back to Opus]]).
