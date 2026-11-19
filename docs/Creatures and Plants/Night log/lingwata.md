# Lingwata (sole): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** common sole, *Solea solea*. The species report gives *Ingwata tar-rig* / *Lingwata komuni*; shown as **Lingwata** as in the content list.

## Size
- **Size in game:** 1.44 blocks long with the tail (23 px), 0.63 wide (10 px with the fringe), 2 px thick (3 at the raised pectoral fin). Body box 0.6 x 0.2 (unchanged).
- **Why:** a real one is about 30 to 40 cm†, so this is about 4 times life size. The critics checked it beside a vanilla cod, the ċerna, a 2-block tonn and the boll: "a sensible size". It is clearly smaller than the boll, which is 2.6 blocks long with its whip tail.
- The placeholder was 1.13 blocks. The drawn sole went up and down between rounds (one critic found it too big, later ones found it too short and round); the installed one is the longest, slimmest oval.

## Behaviour, spawns, rarity
- **Behaviour:** like the boll: swims low over sand (up to 0.8 blocks), and often settles and lies still for 5 to 20 seconds. Shies from players when not resting. Flat: on land it lies flat. Health 4.
- **Spawns:** only over soft floors. `bahar_sea`, `dwejra_bahar_sea`, `qawra_inland_sea` weight 5; `posidonia_meadows`, `dwejra_posidonia_meadows` weight 3; deep sea weight 2; alone. Vanilla: warm and lukewarm, weight 2.
- **Rarity:** fairly common.
- **Stings:** no.
- **Drops:** itself (1 raw fish, `mimcontent:lingwata`). Bucket, spawn egg. It is shark bait.

## Art
Made overnight by a maker, judged by a fresh critic each round from pictures only. Photos: free Wikimedia Commons ones (licences in `art/references/fish_lingwata_refonly/list.tsv`): landed soles on black for the outline and true colour, soles on the sand in water for the eyes, fringe and the raised pectoral fin with its black tip, the white blind side, and an 1890s plate seen from above.

**3D model** (`art/src/fish_lingwata_model.py`): **gave up** after 8 rounds of 8. The best version is installed.
- **Looks:** a thin oval tongue lying on the sand, with a blunt round head, the widest point about a third back and a small rounded tail fan that sways.
  - A lighter fringe fin runs all round the edge with darker ray ticks.
  - Both eyes sit near the front on one side, one behind the other on a slant, so they never sit side by side like a face. Each is a dark pupil flush with the back, with a pale ring.
  - The small pectoral fin is raised a little behind the head, in the body's colour, with one dark brown pixel at its tip (the sole's black spot).
  - Sandy brown with small darker speckles on top. White underneath: the white blind side shows as a pale line along the edge when seen side on.
- **Colours** (before the x1.15 lift for the water): body #a08862, lit #b29a72, shade #8c7554, speckles #6b5544, fringe #b8a07a with ticks #94805f, underside #ece6da, eye ring #d8c8a8.
- **Critic rounds**, all FAIL; the critics kept pulling in opposite directions:
  1. Eyes like the other marks, eye posts, a knob tail, too big.
  2. "A boxy brick" from above.
  3. "A pasty", too short and round, frog eyes.
  4. "A gourd or bottle", a lump on its back.
  5. "Reads clearly as a flatfish, the oval tongue shape is right", but the black fin spot looked like a third eye, and the mottles and fringe were too faint.
  6. Big blotches near the eyes made a face; the tail end was ragged.
  7. The tail looked like a knob, with a phallic risk; only one eye showed.
  8. "Bottle-shaped", googly eyes.
- **Installed:** round 5's shape (the one the critic called right) with round 7's pectoral: the body's colour and one dark brown tip pixel, so it no longer looks like a third eye. This exact mix was not judged by a critic.
- Round 5's, 7's and 8's versions are kept in the script as candidates G, I and J for the owner to try (`--candidate`).
- New review shots were added to the fish test:
  - `fish-lingwata-lineup` and `-lineup-above`: the sole resting on sand beside the boll, a cod, the ċerna and a small tonn.
  - `-close-three-quarter` and `-close-top`.

**Item icon** (`art/src/fish_lingwata_icon.py`): **passed in round 5 of 8.**
- Head lower left, tail upper right, like vanilla's fish. A broad oval about twice as long as wide, with no neck, ending in a small fan.
  - A dark outline that is lighter on the lit top left, then a lighter fringe band with darker ray pixels.
  - Both eyes near the head on the upper side, close together on a slant, each with a pale ring. They are the only near-black pixels.
  - A small pale pectoral fin with a dark tip just behind the eyes on the upper edge, and a few speckles.
- **Colours:** the model's sand, out of water (not lifted again, or it went pale). Body #c4a87e / #b0946c / #97795a, fringe #d2bb92, speckles #7c624a.
- Rounds 1 to 4 FAIL: the eyes and fin spot made a face; "a sausage"; "a short plump cod" with a stalk; "a drumstick". **Round 5 PASS** (candidate I).
- Round 5's optional polish, not done (left for the owner):
  - a wider tail join;
  - a pale pixel beside each eye;
  - a clearer fin tip;
  - the fringe carried along the underside;
  - one pale patch a tone darker.
- **Blind reads** of the passed icon (three fresh readers, neutral file names, among vanilla items), first lines word for word:
  1. "A pale fish, probably a slim cooked or dried fish with a pointed snout (not a mammal or a bird)."
  2. "It looks like a raw fish, a slim grey-brown one like a sardine or mackerel."
  3. "A raw, uncooked whole fish (a pale tan or beige fish, maybe a sea bream or similar)"
- All three saw a fish; none named a flatfish or a sole. Readers in earlier rounds often took the wide end for the tail.

**Bucket** (`art/src/fish_lingwata_bucket.py`): **passed in round 1 of 8; the owner rejected it, see the redo below.**
- On vanilla's cod bucket, the rounded front of the sole rises out of the water at the left, leaning like vanilla's cod, eyed side to the viewer.
  - The fringe is round its edge, and the two eyes sit one above the other on a slant, on its upper left side.
  - Water fills the rest of the mouth, with a shadow and a glint. The back rim stays dark where the fish doesn't cover it.
- Candidates A (the pick), B (bigger, more upright) and C (leaning further). The critic chose A: B's upright head risked a phallic read, and C looked like a lump stuck to the rim.
- Optional polish, not done (left for the owner):
  - an unbroken pale fringe row;
  - a pale pixel beside each eye;
  - fewer speckles.
- **Blind reads** (three fresh readers, neutral file names, among vanilla buckets), first lines word for word:
  1. "A water bucket holding a pale, sandy-coloured fish with darker speckles."
  2. "A bucket of water holding a tan, spotted fish (maybe a pufferfish or a small round fish)."
  3. "A bucket of fish, probably a brownish, mottled fish such as a grouper or a pufferfish."
- All three saw a fish bucket. One of the three guessed "a flatfish" among other options.
- The spawn egg is still a placeholder (not part of tonight's job).

**Bucket redo** (owner, 2026-11-19: "lingwata bucket fails it should fill more of the bucket"; [[2026-11-19 Night fish icons and buckets - most pass; John Dory, gallinella, lingwata bucket redo]]): **G passed in redo round 2 of 3. Waits for the owner.**
- The sole now rises out of the water and spreads wide across the whole opening, tilted so its mottled top side faces you. The head end is at the left with both eyes close together, each with a light pixel touching it. The small darker tail pokes past the rim at the right. The back rim stays dark on the tail side, with some water showing.
- Fill, measured against our accepted buckets (coverage of the finished bucket / fish pixels in the top 6 rows):

| Bucket | Coverage | Fish pixels |
|---|---|---|
| boll | 0.68 | 65 |
| skorfna | 0.66 | 50 |
| kavall | 0.61 | 33 |
| cerna | 0.60 | 30 |
| marzpan | 0.59 | 27 |
| lingwata A (rejected) | 0.62 | 35 |
| **lingwata G (new pick)** | **0.69** | **67** |
| lingwata H (fuller head) | 0.70 | 71 |

- **Redo round 1** (D, E, F): FAIL. D was the best, but the critic said it "reads as a bread roll or muffin top on a bucket, not a fish". Fixes: give it a head end and a small tail past the rim, put both eyes together near the head, lighten the mottles, keep one clean oval top edge with a fringe, and drop E (its dark slit read as a keyhole or a mouth).
  - Blind reads of D, first lines word for word:
    1. "A bucket of fish: a big, pale tan, spotted fish, probably a grouper or a pufferfish-like fish."
    2. "A bucket holding a pale, sandy, speckled fish (maybe a flatfish or a puffer-like bottom fish)."
    3. "A bucket with a fish in it, probably a mottled scorpionfish-type fish."
- **Redo round 2** (G, H, with D for comparison): **PASS, G** (H a close second; D "still reads as a bun"). The critic said G fills the bucket about as much as the boll bucket, matches the sole icon's tan, its eyes sit close together near the head, it shows no face and nothing phallic, and it can't be mixed up with the boll bucket.
  - Optional polish the critic listed, not done (left for the owner): a notch or darker pixel between the tail and the body; flatten the top edge by 1 px with a darker underside shadow; a lighter, unbroken fringe on the top and right; 2-3 more small mottles in the middle.
  - Blind reads of G (three fresh readers, neutral file names, among vanilla buckets), first lines word for word:
    1. "It's a bucket holding a fish: a pale tan, brown-spotted fish with a spiky fin on top, maybe a scorpionfish or grouper."
    2. "A bucket of water holding a sandy-tan fish, maybe a flatfish or a sand-coloured bottom fish like a weever or a sand goby."
    3. "A bucket holding a tan, mottled, big-headed fish (it looks like a bottom fish such as a scorpionfish or gurnard)."
  - All three saw a fish bucket. One guessed "a flatfish". Two read the fringe as a spiny fin or big fins.

**Bucket upright** (owner, 2026-11-19, after seeing G and H: "have the lingwata be like 90 degree vertical in the bucket instead of trying to seat it sideways"; [[2026-11-19 Lingwata bucket - sole standing upright]]): **3 critic rounds, all FAIL. P is installed for the owner to judge.**
- The limit: a bucket's fish can only use the 6 pixel rows above the bucket body, and it must cover where vanilla's cod sits (row 1 columns 4-7, row 2 columns 3-4), so it stands at the left of the opening. Upright, the sole can be at most about 6 px tall, so it can't be taller than it is wide; any upright version shows only the rounded top of the fish.
- Fill: upright fills less than the sideways G. All upright tries pass `check_cover` and `check_rim` and keep the back rim.

| Bucket | Coverage | Fish pixels |
|---|---|---|
| boll (accepted) | 0.68 | 65 |
| G (sideways, passed round 2) | 0.69 | 67 |
| J (upright round 1) | 0.62 | 42 |
| M (upright round 2) | 0.61 | 42 |
| N (M a pixel wider) | 0.61 | 45 |
| **P (upright round 3, installed)** | **0.61** | **31** |
| Q (P a pixel wider) | 0.61 | 37 |

- **Upright round 1** (J, K, L): FAIL. J reads "as a round tan lump with two dark dots poking out of the bucket, more like a potato or a peeking critter's head". Fixes: a pale fringe down both sides, a narrower top, eyes on a slant without pale halos, evenly spread mottles.
  - Blind reads of J, first lines word for word:
    1. "A bucket of water holding a pale, speckled fish (maybe a pufferfish or seahorse-like fish)."
    2. "A bucket holding a brown, speckled fish (it could be a grouper or a seahorse)."
    3. "A water bucket holding a pale, spotted fish, maybe a small grouper or other bottom fish."
- **Upright round 2** (M, N): FAIL. M reads as "a round tan head with two dark eyes peeking over the rim, like a hamster or gopher"; the two eyes near the top of a dome make a face. Fixes: a narrow tongue, a snout mark, eyes a pixel apart on a slant.
  - Blind reads of M, first lines word for word:
    1. "A bucket of fish, probably a pale tan, cod-like fish."
    2. "A bucket of water holding a small sandy-brown mottled fish."
    3. "A bucket of fish: a tan and brown mottled fish, maybe a grouper or a scorpionfish."
- **Upright round 3** (P, Q): FAIL. P reads as "a small brown bird or puppy head peeking over the rim": the top pixel reads as a crest or ear, the dark right edge as fur shading, and the two eyes as a face. Its suggested fixes (not done, the rounds ran out): the eyes as one diagonal pair touching corner to corner, a centred 2 px tip, a pale fringe on both sides instead of the dark right edge, 2-3 mid-brown spots.
  - The critic's view: an upright sole reads only "barely" at this size, "six rows can't show the tongue's length"; a tilt of about 60° (head up and to the left) or the sideways G reads more clearly as a flatfish.
  - Blind reads of P, first lines word for word:
    1. "A bucket holding a fish: a tan, spotted fish with its head pointing up, maybe a seahorse or some kind of goby."
    2. "A bucket of water holding a small tan/brown fish."
    3. "It looks like a bucket holding a small tan-brown fish, head up out of the water."
  - All nine upright readers saw a fish in a bucket; none named a flatfish or a sole. One reader of P said it "could almost pass for a blob or a small mammal's head".

**Tests:** the one-fish run passes (swim, hit boxes, shots, hotbar). The whole fish test (`SMOKE_ONLY=fish`) was run once at the end and passed: all fish, all hit box rows and the flat-on-land check.

## Egg

**Owner 2026-11-19: passes** ([[2026-11-19 Spawn eggs - all eight pass]]).
**Spawn egg** (`art/src/fish_lingwata_egg.py`, shared parts in `art/src/fish_egg_common.py`), 2026-11-19: **passed in round 2 of 3**; C3 (C2 with round 2's polish) installed, waiting for the owner. Started because the upright bucket Q was accepted ([[2026-11-19 Redo verdicts - lizz bucket, lionfish, lingwata Q, gallinella, John Dory]], [[2026-11-18 Approving a step starts the next; skorfna bucket]]).
- **Design:** vanilla's fish-egg outline and vanilla's own pool, nothing breaking it, in the accepted icon I's colours only. Features: the pale fringe fin running right round a sole's body, as a pale band just inside the outline, and the icon's dark speckles on the sandy body, one to a row so no two stand level (no pair of eyes). Lit at the top left; the side flaps are fringe-coloured. No eye, no face, and no dark-tipped pectoral (a dark dot on a pale patch reads as an eye).
- **Candidates:** A, a smooth fringe; B, the fringe two pixels wide on the lit upper left; C, the fringe with its fin rays ticked every other pixel, as on the icon. Before the critic, the maker's own look at 1x darkened the body a step: as pale as the fringe, it was a plain potato.
- **Critic round 1: FAIL, pick C.** "At 1x and in both hotbars, A, B and C look the same: a plain tan egg with faint speckles. ... The egg doesn't say "fish" and doesn't say "sole". ... In all three candidates the pale fringe shows only on the lit left and along the bottom, so it reads as rim light, not as a fin running round the body. The maker's pie-crust worry is real, and it comes from the bottom row (row 12). ... In C it alternates f/1, which reads exactly like a crimped crust edge." Fixes applied (C2): the fringe down the shaded right side (12,8) (12,10) f; the base row one shaded fringe (7,12) (9,12) (11,12) f; the lone tick on the lit upper left (5,6) F. It also suggested the tail fan as a part breaking the outline, for the owner to decide: tried as D.
- **Critic round 2: PASS, pick C2.** "The pale fringe now runs all the way round, and the bottom row is one even f band, so the pie-crust edge is gone." "It's the palest and sandiest of our brown eggs (cerna, skorfna, cawl, ziemel, huta kahla), with speckles where they have stripes or patches, so it's easy to tell apart." "Remaining weakness: at 1x it's still close to a "speckled loaf"." Its polish, applied (C3): a darker shade band t inside the shaded right fringe (10,7) (11,8) (11,9) (11,10), and the lone tick in the lit cap (7,4) F. On D: "the tail at (11,4) to (13,2) is a 1 px stalk that bends into a hook. At 1x and 2x it reads as a potato or pear stem, or a tied sack, not a tail fan. It also puts a tail poking out at the upper right, the same place as our accepted cawl egg". D is not used.
- **Blind reads, round 1** (three fresh readers, A, B and C in slots 2, 5 and 8 among vanilla eggs; none could tell them apart):
  1. "A spawn egg in sandy tan-brown with lighter speckles and a slightly darker top. My first impression is a sand-coloured bottom fish, most likely a flatfish such as a sole. It is fairly plain, so the species is a weak guess."
  2. "A spawn egg in sandy tan with fine darker speckles, like sand or gravel. My guess is a sand-coloured bottom fish such as a sole or flounder, or a weever. On its own it could also be read as a plain brown land animal (a rabbit or a donkey). It is the hardest of the four to name."
  3. "First impression: a sandy tan spawn egg with fine darker speckles. It reads as a sand-coloured seabed creature, most likely a flatfish (sole or flounder) or a weever. The species is hard to pin down from the pattern alone."
- **Blind reads, C2** (alone among eight vanilla water-mob eggs):
  1. "A sandy tan-brown spawn egg with darker speckles. It looks wider at the bottom than the others. It suggests something that lives on sand, like a flatfish (sole or flounder) or a weever. At first glance it also looks a bit like a bread roll."
  2. "A spawn egg in sandy tan-brown with lighter speckles. At first glance it looks more like a loaf of bread or a cookie than a creature. If it is a creature, it would be a mottled bottom-dweller such as a scorpionfish, grouper or comber"
  3. "A spawn egg, sandy tan with fine darker speckles and a broad, flat shape. It reads as a sand-coloured bottom creature, most likely a flatfish (sole or flounder) or a ray lying on sand."
- **Blind reads, D** (the tail fan): "A tan spawn egg with a thin curled stalk at the top right. My first impression was a tied sack or an onion, not a creature." / "... First impression is a seahorse because of the curled tail. ... It reads like a sack as much as a creature." / "... That line reads as a tail, so I take it to be a stingray ... the line could also be the string on a sack."
- **Blind reads, C3** (alone among eight vanilla water-mob eggs; slot 1 beside it is vanilla's cod egg):
  1. "A spawn egg in sandy tan with small brown speckles. ... It reads as a sand-coloured seabed fish, maybe a flatfish (sole or flounder) or a weever, but I can't name a species. It looks too much like slot 1 to tell apart quickly."
  2. "A spawn egg in sandy tan with darker brown speckles and a lighter belly. ... my guess is a flatfish such as a sole or flounder, or maybe a weever."
  3. "A spawn egg in sandy beige-tan with fine darker speckles. It looks like a lighter, sandier copy of slot 1. It reads as a sand-coloured bottom fish, probably a flatfish such as a sole or flounder (a weever is another possibility)"
- Every C3 reader guessed a flatfish (sole or flounder) first; two found it close to vanilla's cod egg.
- **Compare sheet:** `art/candidates/fish_lingwata_egg.png` (not in git).

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.
- The model is the weakest piece. It needs the owner's eye, or the owner's own photos.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [FishBase, *Solea solea*](https://www.fishbase.se/summary/Solea-solea.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.
