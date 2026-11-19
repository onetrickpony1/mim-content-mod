# Gallinella (gurnard): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** tub gurnard, *Chelidonichthys lucerna*, **Gallinella** in the species report (gurnards in general: *Gallini*). Its big pectoral fins are blue-edged "wings", and it walks on separate fin rays.

## Size
- **Size in game:** 1.13 blocks long (18 px), 0.88 wide with the wings spread. Body box 0.6 x 0.35.
- **Why:** a real one is about 40 cm†. About 2.5 times life size.

## Behaviour, spawns, rarity
- **Behaviour:** "walks" on the sand: it keeps within half a block of the floor, moves slowly, and now and then stops for 3 to 10 seconds. Shies from players. Health 5. (No real walking animation yet; a maker can add one.)
- **Spawns:** only over soft floors. `bahar_sea`, `dwejra_bahar_sea` weight 4; `fond_deep_sea`, `dwejra_fond_deep_sea` weight 3; groups of 1 to 2. Vanilla: warm, lukewarm, deep lukewarm, weight 2.
- **Rarity:** uncommon.
- **Stings:** no.
- **Drops:** itself (1 raw fish, `mimcontent:gallinella`). Bucket, spawn egg. It is shark bait.

## Art
Made overnight by a maker, judged by a fresh critic each round from pictures only. Photos: free Wikimedia Commons ones (licences in `art/references/fish_gallinella_refonly/list.tsv`): a market stall and fish on a boat deck for colour, two from above with the wings spread, aquarium and sea-floor shots for the shape.

**3D model** (`art/src/fish_gallinella_model.py`): passed in round 5 of 8.
- Three paint jobs tried: A red-orange like the market fish, B paler pinkish tan like the fish on the boat deck, C A with greener wings. **A chosen**: the market photos are the fish people know, and it stays clearly apart from the pink trilja.
- **Looks:** a big boxy head, the tallest and broadest part (4 x 5 px), with a steep forehead stepping down to a low snout and the eye high on it. The body steps down twice to a slim stalk and a squared orange tail with a small nick. One low spiny dorsal fin behind the head, a long low second dorsal and a pale anal strip.
- **The wings:** two flat fans, 6 px out each side (15 px across), hinged high on the flank just behind the head and angled about 23 degrees down, so they show from the side and from above. Turquoise with darker rays, a bright blue rim on the outer edge and an irregular mid-blue blotch at the inner rear, as on the real fish.
- **Finger rays left out:** the three "walking" rays read as legs at this size.
- **Colours:** back #e8703e, darker back #d85a34, flank #fab27e, belly #fff0e0 (a hard split along the mid-flank, so the pale belly still shows in water), wings #58b4aa / #88d6c6, rim #4cb0ff, blotch #4a78c0, tail #f8925c. Red fish turn mauve under water, so the body was pushed to a bright orange for the in-game look.
- **Size:** 18 px long (1.13 blocks), a bit longer than vanilla cod, much smaller than the cerna and tonn.
- Round 1 FAIL: the first dorsal read as two ears, pale skin beside the eye, mauve in water, a box with no taper, the wings a blue mat under the belly. Round 2 FAIL: a dorsal hump, no taper, flat colour. Round 3 FAIL: on land the wing's dark patch read as a bird's head with an eye, the tail looked cut off in water, the wings flat from the side. Round 4 FAIL: the blotch in the middle of the fan read as an eyespot. **Round 5 PASS.**
- The critic's optional polish, not done (left for the owner): flatten the wing that sticks up when it flops on land, and a slightly paler belly.
- New review shots in the fish test: `fish-gallinella-lineup` and `fish-gallinella-lineup-above` (gallinella on sand, cod, cerna, small tonn).

**Item icon** (`art/src/fish_gallinella_icon.py`): **gave up** after 8 rounds; the round 8 version is installed.
- Head lower left, tail upper right, like vanilla's fish: a red-orange fish with a blunt head, the eye high on it, a narrow stalk, a notched tail, and the blue-green wing fanning out under the belly behind the head.
- The first tries used the model's very light colours and read as a prawn; the body was made redder and darker, lit from the top left.
- Every critic round found something: round 1 "prawn", the fin a blue ball; then a dragon-like head, a puddle-like fin, a goldfish shape, spots near the eye, straight edges. The last critics called it "close". Round 8 still said the body was too deep (goldfish-like) and the fin read as a puddle.
- **Blind reads of the installed version** (three fresh readers, neutral file names, among vanilla items), first lines word for word:
  1. "Red mullet"
  2. "Red gurnard"
  3. "Red gurnard"
- **For the owner:** this is the piece to look at first. Round 8's unapplied fixes: a slimmer, more diagonal body and a fin that fans out to the lower right rather than hanging under the belly.

**Bucket** (`art/src/fish_gallinella_bucket.py`): passed in round 1 of 8.
- On vanilla's cod bucket, the head rises out of the water facing up and left: the blunt orange head, the eye high on it, and the turquoise wing spread on the water beside it. The back rim outline stays dark except behind the head. Candidates: A (head high, wing showing), B (head a row lower), C (no wing). **A chosen** (the critic: without the wing it is a generic orange fish).
- The critic's one polish was applied: no lit pixel at the end of the eye's row.
- **Blind reads**, first lines word for word:
  1. "Bucket of red fish (maybe a gurnard)"
  2. "Red gurnard in a bucket"
  3. "Bucket of red fish (a gurnard?)"
- The spawn egg was still a placeholder (not part of tonight's job); it was drawn on 2026-11-19, see "Egg" below.

## Icon and bucket redo (2026-11-19)
The owner accepted the 3D model but rejected the icon and the bucket: "too flat and fat they dont look like the fish" ([[2026-11-19 Night fish icons and buckets - most pass; John Dory, gallinella, lingwata bucket redo]]). Both were redrawn, with up to 3 fresh critic rounds each, then stopped for the owner. Both review sheets show the rejected night version and the accepted model (side and three-quarter, in the game) beside the new candidates.

**Item icon, redone:** a big boxy head at the lower left, then a slim body tapering diagonally to a forked tail at the upper right (no longer a deep goldfish body). Light from the top left with a darker back and edge for volume. The wing is a real fan behind the head: dark teal root, teal rays, a bright blue rim. Candidates: A (the wing spread wide like a wing), B (the wing lower and wider), C (a smaller wing). **A chosen.**
- Round 1 FAIL: a straight belly wall, a stripe inside the back, dark blue near the eye's row. Round 2 FAIL: still the belly wall, a checkered fin with a dark hole, pale pixels in the eye's row, the head not boxy. Round 3 FAIL: no tail fin (a blunt stub, so at 1x it read as a prawn or carrot), the head too round.
- Round 3's main fixes are applied, **not judged again** (the round limit): a forked tail fan out of a thin stalk, and a flat brow for the boxy head. Its cheek-line idea was left out, to keep marks away from the eye.
- **Blind reads** (three fresh readers each round, neutral file names, among vanilla items), first lines word for word:
  - round 1: "Red mullet", "Red fish (maybe a gurnard)", "Gurnard (a red fish with blue wing-like fins)"
  - round 2: "Red fish", "Gurnard", "Red shrimp/prawn"
  - round 3 (before the tail fix): "Red gurnard", "Red gurnard", "Red gurnard"

**Bucket, redone:** the boxy orange head rises out of the water at the left with one high eye; the wing spreads up and to the right as a fan (dark root, paler rays, bright blue tips poking past the bucket's side). The back rim outline stays dark. Candidates: A (head left, wing right), B (the wing fanning down over the water), C (the head centred, a wing each side). **A chosen.**
- Round 1 FAIL: a checkered fin, its blue rim lost in the water. Round 2 FAIL: a pale pixel under the eye read as a mouth; the fin a teal lump. **Round 3 PASS.** Optional polish not done (for the owner): a blue pixel on the fin's lower edge, a sloped snout corner.
- **Blind reads**, first lines word for word:
  - round 1: "A bucket of tropical fish (orange fish in a bucket).", "Red gurnard (a red fish with big blue pectoral 'wings') in a bucket", "Bucket of red fish with blue fins"
  - round 2: "A bucket with an orange-red fish in it.", "Red fish with blue-green 'wings' in a bucket (looks like a gurnard)", "A bucket holding a red fish with blue fins."
  - round 3: "A bucket of tropical fish (a blue and red fish).", "Red fish with big blue fins in a bucket (looks like a sea robin, or gurnard)", "A gurnard (a red fish with blue-green wing fins)."

## Icon, second redo (2026-11-19)
The owner accepted the redone bucket; the icon failed: "the fin looks too disconnected from the body" ([[2026-11-19 Redo verdicts - lizz bucket, lionfish, lingwata Q, gallinella, John Dory]]).
- **What changed:** the slim body, boxy head and forked tail stay. The wing's root now sits on the side just behind the head, with no gap or outline between them. From there it spreads as a fan over the lower body, like the accepted model and bucket: dark teal at the root, paler outward, a few darker rays, the bright blue rim on the outer edge.
- Candidates: A (the fan spread right and down over the lower side), B (the root lower, the fan swept back under the belly). **A chosen** (the critic: B's fin starts under the belly and looks stuck on, like the rejected one).
- **Critic round 1 PASS.** Optional polish, not done (for the owner): round the fin's bottom-left corner, carry the blue rim along its bottom edge, soften one dark outline pixel beside the fin's top.
- **Blind reads** (three fresh readers, neutral file names, among vanilla items), first lines word for word: "Red snapper", "red gurnard", "Gurnard (tub gurnard)".
- The review sheet shows both rejected icons, the new one and the accepted bucket side by side, and the accepted model in the game.

## Egg

**Spawn egg** (`art/src/fish_gallinella_egg.py`, shared parts in `art/src/fish_egg_common.py`, the line-aware eye check in `art/src/fish_egg_lines.py`), 2026-11-19: **failed all 3 rounds, narrowly in rounds 2 and 3**; B4 installed with round 3's fixes (best version, as the rules say), waiting for the owner. Started because the owner passed the icon ([[2026-11-19 Redos pass - lionfish, lizz bucket, petrica, gallinella icon; John Dory bucket again]], [[2026-11-18 Approving a step starts the next; skorfna bucket]]).
- **Design:** vanilla's fish-egg outline and vanilla's own pool. The colours are the icon's plus the model's pale peach (#fcc8a0). The key feature, per the owner, is the big turquoise "wing" (the pectoral fin) with its bright blue scalloped rim, spread as a fan over the egg's lower right: three dark rays meet at one root, and it breaks the outline a little at the right. The red-orange egg around it is lit from the top left, with a small pale belly low on the front.
- **Candidates:** A the wing on the right; B a bigger wing on the right, breaking the outline more; C the wing on the left.
- **Critic round 1: FAIL, pick B:** "At 8x it reads as a flat teal patch, not a fin with rays. ... it looks stuck on like a sticking plaster." "The pale belly ... puts a pale lower-left patch on a red egg, which is marzpan's exact recipe." Fixes, all applied (B2): the wing light turquoise with three dark rays from one root, the root tapered, the belly shrunk to two pixels, one more blue scallop.
- **Critic round 2: narrow FAIL on B2:** "The rays read as a checker or diamond net, not a fan." "The wing's top edge is still a straight horizontal line", and the rim's lowest pixel blends into the pool. Fixes, all applied (B3).
- **Critic round 3: narrow FAIL on B3:** "the 'separate sticker' problem is still there, at the fin's root. The dark-teal pixels ... make a hard L-shaped dark frame". It says "It is clearly different from the marzpan egg ... and the tird egg". Its three fixes applied (B4): the body takes back both root corners, so the wing grows from one point, and the fan's top-left is tapered. The critic said "It passes with the three pixel fixes below", but no fourth round was allowed to confirm it.
- **How the reads were done:** three fresh readers per round, no context, each shown one hotbar per fish at GUI scale 4 (light and dark backdrop) with the egg among vanilla water-mob eggs, under neutral file names. Rounds 1-3 used the usual readers; the final read of the installed egg used **Sonnet readers** (the owner's new rule, [[2026-11-19 Art rounds capped at 3; blind readers on Sonnet]]). In round 1 all three candidates sat in slots 2, 5 and 8; the readers could not tell them apart, so their reads cover all three.
- **Blind reads, round 1** (A, B, C):
  1. "a red/orange-red dome with a bright teal patch on the lower right. ... I'd guess a gurnard (the tub gurnard has red body and blue-edged 'wings'). ... the teal patch doesn't read as a fin. It looks like a pasted-on blob, a bandage or a spill of water"
  2. "The species that fits best is the red gurnard (tub gurnard) ... the teal patch looks stuck on, like a bubble, a plaster or a second object in front"
  3. "My first guess is a gurnard (tub gurnard, Chelidonichthys lucerna, known for its blue-edged 'wing' fins)."
- **Blind reads, round 2** (B2):
  1. "a spawn egg for a red fish with a bright teal-green fin on its lower side. That combination makes me think of a gurnard, most likely a tub gurnard"
  2. "It reads as a red gurnard (tub gurnard), with the blue patch as its blue-edged pectoral fin. ... It can read as mould on a strawberry"
  3. "My first impression is a spawn egg for a red gurnard, probably a tub gurnard. ... the teal patch looks like a separate blob stuck to the side, like mould or a sticker"
- **Blind reads, round 3** (B3):
  1. "a red fish with a bright blue-green fin on its lower right side, which strongly suggests a tub gurnard (Chelidonichthys lucerna) ... This was the clearest of the four."
  2. "most likely a red gurnard, since the bright teal patch reads like a gurnard's coloured pectoral fin. ... the teal blob at the lower right looks like a separate object stuck onto the egg"
  3. "I'd guess a red gurnard because of the blue-green pectoral fin on a red body. ... the turquoise patch looks like a separate blob or gem stuck onto the egg rather than a fin"
- **Blind reads, final, Sonnet readers** (B4, installed):
  1. "a coral-red and orange blob with a small turquoise or teal patch at its lower right ... Its likeliest reading is a red scorpionfish or a red mullet, or a crab or lobster."
  2. "My first impression is a red fish (a red mullet or a scorpionfish) with a green fin. ... The green patch at the lower right makes it read as a separate gem or a second object stuck on the body"
  3. "My first impression is a red crab, a lobster or a shrimp. My second guess is a red scorpionfish or a similar red fish."
- Rounds 1-3: all nine readers named the tub gurnard first, but most said the wing looks stuck on. The Sonnet readers didn't name it: they saw a red fish or a crab.
- **Compare sheet:** `art/candidates/fish_gallinella_egg.png` (not in git).

## Not decided (for the owner)
- The icon's second redo waits for the owner. Change anything you like.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [FishBase, *Chelidonichthys lucerna*](https://www.fishbase.se/summary/Chelidonichthys-lucerna.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.

## Owner's verdict (2026-11-19)
- "All pass except john dory bucket. That needs a redo, consider very different possible version" ([[2026-11-19 Redos pass - lionfish, lizz bucket, petrica, gallinella icon; John Dory bucket again]]).

## Owner's verdict (2026-11-19, later)
- "John dory bucket: L, all eggs pass, switch back to opus guessers." ([[2026-11-19 John Dory bucket L; last four eggs pass; blind readers back to Opus]]).
