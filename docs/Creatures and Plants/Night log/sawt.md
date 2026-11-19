# Sawt (weever): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** the lesser weever, *Echiichthys vipera*, **Sawt** in the species report: the one in shallow sand at beaches that people step on. (The greater weever, *Traċna*, lives deeper.)

## Size
- **Size in game:** the model is 0.88 blocks long (14 px), 4 px deep at the head and 3 wide; body box 0.35 x 0.2 (unchanged). The first plan was 0.56 blocks (9 px), but at that size the black fin, the eyes on top and the yellow tail could not all be drawn, so it was made longer. It is still low and slim: beside the cod it reads as a small fish lying flat.
- **Why:** a real one is about 10 to 15 cm†. About 4 times life size, so you can see it on the sand if you look.

## Behaviour, spawns, rarity
- **Behaviour:** lies on the sand nearly all the time (rests of 20 to 60 seconds), sandy coloured so it is hard to see. Now and then it moves a little. It doesn't shy from players. Health 3.
- **Buried:** the real fish buries itself with only its eyes showing. The simple version: it lies flat on the floor in sand colours, and its model sits 1 px into the floor so it looks half buried (see Art). Truly digging into the sand is left for later.
- **Spawns:** only over soft floors, in the shallow seas: `bahar_sea`, `dwejra_bahar_sea`, `qawra_inland_sea`, weight 4, alone. Vanilla: warm and lukewarm, weight 2.
- **Stings:** yes. Touching it (stepping or standing on it, bumping into it) or hitting it in melee: 1 heart and Poison for 6 seconds, at most once every 2 seconds, like the skorfna. Mobs that touch it are stung too, other fish not. Arrows don't count. Creative, spectator, peaceful and Jellyfish Ward: never stung.
- **Rarity:** uncommon.
- **Drops:** itself (1 raw fish, `mimcontent:sawt`). Bucket, spawn egg. It is shark bait.

## Art
Made overnight by a maker, judged by a fresh critic each round from pictures only. Photos: free Wikimedia Commons ones (licences in `art/references/fish_sawt_refonly/list.tsv`), colour from fresh fish out of the water, the Corsica and Limnos photos for how it lies buried.

**3D model** (`art/src/fish_sawt_model.py`): passed in round 5 of 8.
- Three paint jobs tried: A golden sand (the fresh Dutch fish), B sand-grey camouflage (the buried Corsica fish), C A's colours with a dotted row instead of oblique dots. **A chosen** (the passing critic: B turns to mud under water, C looks more like a goby).
- **It lies half buried:** the model sits 1 px into the floor, so on the sand its belly row is hidden and only the back, the eyes on top and the black spine show, like the photos. No new behaviour: it is only drawn lower. On land and mid-water the whole fish shows.
- **Looks:** a slim fish, deepest at the blunt head and tapering to a thin stalk. The eyes are on top of the head (a dark pupil on the head's top edge, a pale pixel below it on the side). The short jet-black first dorsal fin stands over the shoulders, then a long low second dorsal. The pectoral fins are swept back against the flank. The tail is square and yellow with a black trailing edge. The flank has short diagonal runs of single dark dots for the oblique lines, the back is a step darker than the gold flank and the belly is cream.
- **Colours:** back #9c7a3e, side top #b08a48, flank #cdb06a, belly #eee2bc, lines #8a6a3a, dorsal #141210, tail #f0c020 with a #141414 edge, eye #141414.
- The mouth is only a lighter lip and one mid-brown pixel low on the front: a darker mouth made a face with the eyes.
- Round 1 FAIL: a dark patch round the eye, a jutting jaw that read as a muzzle, big pale pectoral fins like legs, square camouflage blotches. Round 2 FAIL: black eye bars like goggles, a pale head like a mask, a heavy fin. Round 3 FAIL: eyes the same black as the fin, the body didn't taper, the tail lost its yellow under water. Round 4 FAIL: dark marks near the eye, grey-brown colours in the water. **Round 5 PASS.**
- The critic's polish, not done (left for the owner): from straight above the two pupils at the head's front corners still look a little like frog eyes; it suggested moving them 1 px back and making the pale pixel gold. Also warmer colours, and a darker top on the second dorsal.
- New review shots in the fish test: `fish-sawt-on-sand-side`, `fish-sawt-on-sand`, `fish-sawt-on-sand-top` (on a sand floor in water) and `fish-sawt-lineup` (on the sand under a cod, the cerna and a small tonn).

**Item icon** (`art/src/fish_sawt_icon.py`): passed in round 3 of 8.
- Head lower left, tail upper right, like vanilla's fish. Candidates: A, B (no flank lines), C (a taller black dorsal fin). **C chosen** (the critics: the fin is the weever's key mark).
- The eye is the only true black pixel, set on the back's edge; the fin and the tail's edge are a warm brown-black (#2e241a), so the eye stands apart. Nothing gold or pale sits beside the eye.
- Colours are the model's, lifted less than 1.2x for the pale tones (fully lifted they went white at 1x). It is countershaded, so it is lit a little more from below than vanilla's cod (light measure -0.12, the passing critic accepted it).
- Round 1 FAIL: the eye the same black as the fin, gold under the eye, a stiff outline. Round 2 FAIL: a gap at the tail's base, the fin's base pixel too close to the eye, a pale pixel near the eye. **Round 3 PASS.** Its polish (a closed back outline, a two-spike fin, a hint of mouth) was not done.
- **Blind reads** (three fresh readers, neutral file names, among vanilla fish and food), first lines word for word:
  1. "Slot: a fish item, probably a yellow-tailed Mediterranean fish such as an amberjack/yellowtail (Seriola). It doesn't look like a vanilla fish. I can't tell the species for certain."
  2. "Slot: a raw fish item: a long, slim golden-yellow fish set diagonally (head lower left, tail upper right), with a brownish-olive speckled back and a bright yellow tail. It isn't a vanilla fish. My best guess for the species is a lampuka (dolphinfish, mahi-mahi), with a salpa (golden-striped bream) as the next most likely."
  3. "Slot: a raw fish with a long golden-olive body, most likely a dolphinfish (mahi-mahi, "lampuka") or some other golden Mediterranean fish such as a bream or mullet."
- **Look at it:** all three saw a golden fish with a yellow tail, none said weever. At 16 x 16 the small black fin doesn't carry the species, and two guessed lampuka, which also has a gold body and yellow fins.

**Bucket** (`art/src/fish_sawt_bucket.py`): passed in round 1 of 8.
- On vanilla's cod bucket, the blunt head rises out of the water facing up and left: the pale upturned jaw, the eye on the back's edge, and the short black first dorsal fin standing clear above the water behind the head. The body dives to the lower right with the cream belly, gold flank, sandy back and one oblique line. The back rim outline stays dark except behind the head. Candidates: A, B (no line on the back), C (a taller two-spine fin). **A chosen** (the critic: C's two spines look like cat ears).
- Critic's optional polish, not done: soften the pale snout tip (it can look a little like a duckling's beak at 8x), and blend one dark belly-shadow pixel.
- **Blind reads**, first lines word for word:
  1. "Slot: a bucket holding a tan/golden fish (a bucket-of-fish item). I can't tell the species. My best guess is a sea-bream-type fish, but that is a guess."
  2. "Slot: a bucket of fish, i.e. a fish-in-a-water-bucket item like the vanilla "Bucket of Cod", holding a long, slim, sandy-cream fish with a darker tan-brown back that sticks diagonally up and to the left out of the bucket."
  3. "Slot: a bucket of fish (a water bucket with a fish in it). The fish is long and thin, pale tan to cream with yellow fins, and lies diagonally with its head or tail sticking up out of the top left of the bucket."
- All three saw a bucket with a slim sandy fish; none could name it.

**Egg** (`art/src/fish_sawt_egg.py`, 2026-11-19): passed in round 3 of 3. **Owner 2026-11-19: passes** ([[2026-11-19 Spawn eggs - all eight pass]]).
- Started because the owner approved the bucket ([[2026-11-18 Approving a step starts the next; skorfna bucket]]). A sandy-gold egg in vanilla's outline and vanilla's own pool, in the icon's and model's colours only, lit from the top left, with the cream belly on the lower front. Its features are the short jet-black venomous fin, the fine oblique lines, and the yellow tail with its black edge as the right-hand side fin. No eye, no face.
- Candidates: A (a black fin standing on the egg's top, with lines), B (A without lines), C (the fin further forward). Then D and E from the critics' fixes. **E chosen.**
- Round 1 FAIL, pick A: "it reads as an onion or garlic bulb with its stalk, or a fuse on a bomb". D laid the fin flat on the shoulder. Round 2 FAIL on D: "A compact black blob on that shoulder, with sand all around it, then reads as an eye or a cap". E makes the fin a long slanted run hugging the upper-front outline, with two small spines poking out. Round 3 PASS on E: "E's black is a slanted streak along the upper-left outline." Its optional polish, not done: at most one spine pixel outside the outline, the top spine dark brown rather than black.
- **Blind reads** (three fresh readers, neutral file names, the egg in slot 4 among vanilla eggs), first lines word for word:
  - D: "**bar4:** A pale tan or sand-coloured egg with dark blotches and what looks like an open mouth or head shape at the upper left. I read it as a sandy, camouflaged bottom fish, maybe a weever or a stargazer, or possibly a frog or toad." / "**bar4:** A spawn egg that is sandy tan with dark brown blotches and a dark eye-like mark near the top left." / "**bar4.png:** A sandy tan, lumpy spawn egg with dark brown blotches near the top."
  - E (the pick): "bar2.png, slot 4: My first impression is a spawn egg for a sandy, tan creature with darker brown diagonal stripes and a small black tip at the top." / "bar2.png, slot 4: my first impression is a spawn egg for a sand-coloured fish (beige or tan) with a dark tip or fin on top and dark streaks across the body." / "bar2.png: It's a tan or sandy spawn egg with dark brown diagonal streaks and speckles, and a small dark spike at the top left."
- All three read E as a spawn egg, and none saw an eye. Two read a sandy fish (one named a weever); one said it could also be "a loaf of bread", another "a speckled bread roll or a lizard". It is the least clear egg of this batch.
- Sheet: `art/candidates/fish_sawt_egg.png`.

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [MaltaToday, critters by the seashore](https://www.maltatoday.com.mt/environment/nature/111247/critters_by_the_seashore_watch_out_for_these_dangerous_sea_creatures)
- [FishBase, *Echiichthys vipera*](https://www.fishbase.se/summary/Echiichthys-vipera.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.
