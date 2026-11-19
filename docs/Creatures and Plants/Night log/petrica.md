# Petriċa (anglerfish): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** anglerfish, *Lophius* (the report lists *L. piscatorius* and *L. budegassa*, both **Petriċa**). One model for both.
- **Name:** **Petriċa**, with the ċ (id `petrica`).

## Size
- **Size in game:** 1.88 blocks long (30 px), 0.9 blocks wide across the head and jaw, 0.81 tall with its rod (the redo; the night job's flat version was 1.75 long and 5 px deep). On land it is squashed to 45% of its height. Body box 0.9 x 0.35 (unchanged).
- **Why:** anglerfish get big (the larger kind past a metre†). Like the tonn and the shark, it is kept near the size of a big one: a wide, flat head is its look.

## Behaviour, spawns, rarity
- **Behaviour:** sits still on the bottom, rests of 30 to 90 seconds, hardly ever moves. Doesn't shy from players. Flat: on land it lies flat instead of flopping on its side (like the boll). Health 10. Harmless (no bite yet; its lure doesn't do anything).
- **Spawns:** only over soft floors (mud, sand), deep: `fond_deep_sea`, `dwejra_fond_deep_sea`, weight 2, alone. Vanilla: deep lukewarm, weight 1.
- **Rarity:** rare.
- **Stings:** no.
- **Drops:** itself (1 raw fish, `mimcontent:petrica`). Bucket, spawn egg. It is shark bait.

## Art
Made overnight by a maker, judged by a fresh critic each round from pictures only. Photos: free Wikimedia Commons ones (licences in `art/references/fish_petrica_refonly/list.tsv`), colour from landed fish (Norway, a Mediterranean *L. budegassa* at an Algerian market) and a museum fish labelled "Frequent in Maltese waters".

**3D model, night job** (`art/src/fish_petrica_model.py`): **gave up** after 8 of 8 rounds; the owner then asked for a redo (below).
- Three paint jobs tried: A warm mottled brown, B olive brown (the Mediterranean kind), C A with bigger blotches. **A chosen**: the photos of the fish out of water are warm brown.
- **Looks:** a huge, flat head 16 px across (18 with its fringe), nearly half the fish, 5 px deep in the middle stepping down to a 1 px rim, its corners cut so it isn't a square. The lower jaw juts out 1 px with a pale lip, and the gape is one straight dark line right across the front, never curved. Small eyes sit near the head's edges on top, each a dark pupil in a light-brown ring. The rod stands right behind the upper lip, leaning forward, 1 px thin, with a small dull flap at its tip (no glow). Pale skin flaps fringe both sides of the head and the lower jaw. The body tapers 9, 5, 3 px wide and 3, 2, 2 px deep to a small fan tail that sways. Fan pectoral fins lie flat, swept back, at the body's sides, and a low soft fin sits on the back near the tail.
- **Colours:** back #94704a, light #c8a070, dark blotches #5a3c28, ochre blotches #e0b878, cream belly #d8c8aa, gape #1a120c, eye #0c0806. They are set a third lighter than the photos, because under water it went near-black beside the cod.
- **Size:** 1.75 blocks long. That is longer than the placeholder, and the critics found it small beside the ċerna.
- Round 1 FAIL: under water it read as a grey boat with a crane, the rod was too big, and there was no mouth. Round 2 FAIL: it was grey-lavender under water and the eyes made a cute face. Round 3 FAIL: the front read as a cartoon face, the fringe under the chin as teeth, the tail as a knob on a stick, and the camouflage as stripes. Round 4 FAIL: too dark under water, an eel-like side and fins hanging like legs. Round 5 FAIL: the eyes were lost in the blotches and the head was boxy. Round 6 FAIL: the face from the front, and a cream eye ring made googly eyes, so the ring went back to a light brown. Round 7 FAIL: a plain patch above the mouth read as a face, and the eyes were small. Round 8 FAIL, "narrowly": too light and sandy, the flanks striped, a dark bar above the eyes, still smaller than the ċerna.
- The critics pulled the colour both ways: rounds 2 and 4 asked for lighter, round 8 for darker (#6B5A42). The owner should pick the shade.
- **Left for the owner:** whether the head-on view (two eyes above a straight mouth, as on the real fish) reads too much like a face; the back's darkness; a bigger fish (rounds 5 and 8 asked for 1.3-1.5x).
- After round 8 the rod was moved onto its pivot (it had been left 2 px behind it, which lifted the flap to 9 px). The fish now stands at most 7 px tall, so it lies flat on land as the fish test expects. The look is unchanged and was not re-judged.
- A new review shot, `fish-petrica-lineup` (with `-lineup-above` and close-ups `-close-three-quarter`, `-close-top`, `-close-front`), shows it resting on the floor beside a cod, the ċerna and a small tonn.

**3D model redo** (2026-11-19, daytime; owner: "petrica which looks absolutely nothing like an anglerfish. pertricia on the floor is close, but it only really looks that flat OUT of the water. in the water it has a normal fish shape"): **gave up** after 8 of 8 critic rounds; round 8 ("FAIL (narrowly)") is installed.
- Drawn from photos of the live fish in aquariums (Norway, head on; Finisterrae, resting on sand) and a side drawing of *L. budegassa*, all from Wikimedia Commons (`list.tsv`).
- **In the water, a normal fish's depth:** a broad head 14 px wide and 8 deep with bevelled top and front edges; the body deep behind it, narrowing in 3 steps to a squared tail fin with a darker edge; 1.88 blocks long, 0.81 tall with the rod.
- **Mouth:** one dark gape line right across; the lower jaw juts 2 px and is 1 px wider each side, with a pale lip edge and a few short uneven teeth standing on it.
- **Rod and spine:** a 1 px rod on the snout with a ragged fleshy flap (no glow), a shorter second spine behind it leaning back.
- **Fins and flaps:** big pectoral fans on short arms, angled out and down; a low soft second dorsal fin; ragged light and dark skin flaps along the head's lower sides.
- **Eyes:** small and dark, half sunk on top of the head near its edges, a pale pixel beside and behind each.
- **On land it lies flattened:** squashed to 45% of its height (new in the code: `FishRenderer.withLandSquash`, with the hit boxes squashed the same way in `FishShape`; the test checks the two agree, and the land check still wants it no more than 7 px thick: it is about 6).
- Paint A (warm mottled brown) was best in every round; B (olive) washed out to grey in the water, C read pink.
- What the critics said, round by round: 1 a box with a radiator grille; 2 a crate, the head no deeper than the body; 3 a tadpole, the yellow eyes a frog face; 4 a ziggurat or tank turret, white side tabs like a comb; 5 a smiley mark on the head, the jaw a white tray; 6 a flat crate from the side; 7 a stepped brick, the lure a mallet; 8 "FAIL (narrowly)": "the side view now reads as a monkfish", but from three-quarter the head still reads as a stacked box and from the front as a toad face.
- The critics kept contradicting each other (round 4 said drop the stacked tiers, round 6 asked for a dome on top, round 8 for a narrower top step again; rounds 3 and 6 asked for gold eye rims, round 8 called the rim googly).
- **Left for the owner:** whether the head reads as an anglerfish's or a box; whether the head-on view is too much of a face; the squash on land (one critic wanted it flatter).
- The icon and bucket were not changed (the owner passed them). They still fit: the icon is the landed fish from above, the bucket the head-on mouth.

**Item icon** (`art/src/fish_petrica_icon.py`): **passed in round 6** of 8.
- The caught fish seen from above, as it lies on a market slab: head at the lower left, tail at the upper right, like vanilla's fish.
- **Looks:** a huge, wide head with a straight front: a pale lip line right across it and the dark gape just outside it, both dead straight. The body narrows fast to a small tail, with fan fins at the sides. Two small near-black eyes far apart on top, each with a pale glint. A faint light ridge between them for the rod, and darker skin flaps sticking out at the upper right. Mottled brown in 2 px blotches, outlined in dark brown.
- **Colours:** the model's, only a little lighter (x1.05) for out of water. The lip is a warm pinkish cream (#d9bc9c), the rod ridge #ae8458.
- Three candidates each round: A (chosen), B without the pale lip, C without the rod.
- Round 1 FAIL: it read as a scorpionfish or grouper. Round 2 FAIL: a stingray with a whip tail, though one reader got a monkfish. Round 3 FAIL: a sole. Round 4 FAIL: a stingray. Round 5 FAIL: a sole or scorpionfish; the rod read as a nose. Round 6 PASS, "narrowly"; its polish was then applied: the lip toned down (bright, it read as teeth), the rod ridge darker, the head's top-left corner rounded, the fins 1 px bigger.
- What three readers who knew nothing said, first line each, in round 6: "A raw flatfish, most likely a sole or flounder, shown from above with its head at the lower left and its tail at the upper right." / "Slot 4 is a fish, most likely a flatfish such as a sole or flounder, shown lying flat and pointing diagonally. It might also be a lizardfish or monkfish-type fish with a big head." / "Slot 4 looks like a flatfish (a sole or flounder type), seen from above and lying on the diagonal."
- So it reads as a flat brown fish, but mostly as a sole, not an anglerfish. One reader in round 2 said "a monkfish (anglerfish) item, seen from above", but that design read as a stingray to the others.

**Bucket** (`art/src/fish_petrica_bucket.py`): **passed in round 3** of 8.
- Laid on top of the player's own vanilla cod bucket, like the other fish buckets; the back rim stays dark at its two lower corners.
- **Looks:** the head rises out of the water facing you: a flat slab as wide as the bucket's mouth, two small eyes just under its top edge with an olive glint each, the gape one level very dark brown line right across, the lower jaw below it with two pale skin flaps, mottled brown. Water shows underneath.
- Round 1 FAIL: a diagonal head like the icon's read as a wedge, beak or wood chip, and the pointed tip came near phallic. Round 2 FAIL: a black gape over a pale jaw, with cream beside the eyes, read as a grinning cartoon face or a burger. Round 3 PASS (best A); the critic's polish was applied after: the eyes moved down a row under the outline, the head pulled in to the rim's width, two light flecks made mid brown.
- The round 1 critic asked for a greyer olive brown; tried as a candidate in round 2, the next critic found it "washed out next to the cod bucket", so it stays the icon's warm brown.
- What three readers who knew nothing said, first line each, on the final bucket: "Slot 5 is the non-vanilla item. My guess is a bucket holding a flat, bottom-living fish, something like a flounder, sole or turbot, mottled sandy brown with both eyes on its upper side." / "Slot 3 is the non-vanilla item: a bucket holding a mottled grey-green fish with small reddish-orange patches. My best guess is a Mediterranean rock or reef fish such as a wrasse (or possibly a scorpionfish)." (that reader picked the vanilla salmon bucket, not ours) / "Slot 5 is the non-vanilla item: I think it's a bucket holding a squat brown fish with darker mottling or bands, maybe a grouper or a scorpionfish-type rock fish."
- On the round 3 version (eyes on bumps), one reader said "most likely a stargazer, or possibly a monkfish or anglerfish"; the others said a flatfish or grouper. So it reads as a flat brown bottom fish, rarely as an anglerfish. One reader said it could look like a wooden crate lid at hotbar size.

## Egg

**Spawn egg** (`art/src/fish_petrica_egg.py`, shared parts in `art/src/fish_egg_common.py`, the line-aware eye check in `art/src/fish_egg_lines.py`), 2026-11-19: **passed in round 3 of 3**; B4 installed, waiting for the owner. Started because the owner passed the redone model ([[2026-11-19 Redos pass - lionfish, lizz bucket, petrica, gallinella icon; John Dory bucket again]], [[2026-11-18 Approving a step starts the next; skorfna bucket]]).
- **Design:** vanilla's fish-egg outline and vanilla's own pool, only the accepted icon's colours. It follows the icon and the fish's normal shape in water, not the flat look on land. Features: the mottled khaki camouflage (a darker mottled back, a small cream underside low on the front, 2x2 dark blotches never level with each other) and the fishing rod (a thin dark crook growing out of the front shoulder and reaching up and forward, with a small pale lure hanging from its tip), plus pale fan fins on both sides. The wide mouth is left out because it would make a face.
- **Candidates:** A a short rod arching forward; B A with a pale fan fin at the lower left; C A with a longer lure.
- **Critic round 1: FAIL, pick B:** "At 1x it does not read as a petriča egg. It reads as a brown potato or tied sack. ... Nothing about it is phallic ... The real problem is that it is invisible." Fixes, all applied (B2): a longer, darker rod, a 2 px lure "hanging straight down" clear of the egg, a lit khaki upper left with 2 px blotches, fins on both sides.
- **Critic round 2: FAIL on B2:** the rod "makes a closed arch, which reads as a handbag strap, or a sack with a drawstring tag", and "B2 is nearly the same as the cod egg at 1x". Fixes, all applied (B3): the rod opened so only one end touches the egg, a darker mottled back over a small cream belly, bigger 2x2 blotches, dimmer fins. The maker then moved one blotch that sat level with the new 2x2 one, because together they made two eyes over a mouth.
- **Critic round 3: PASS on B3:** "It is a mottled khaki egg with a thin dark stalk and a pale lure hanging in front. ... No face. ... No band, nothing phallic." Its fixes applied (B4): "(4,0) -> `.`. The rod becomes one clean crook" (the knot at its top "is most of the remaining 'drawstring' read"); the lure a small bulb lit from above; a darker pixel where the rod leaves the shoulder.
- **How the reads were done:** three fresh readers per round, no context, each shown one hotbar per fish at GUI scale 4 (light and dark backdrop) with the egg among vanilla water-mob eggs, under neutral file names. Rounds 1-3 used the usual readers; the final read of the installed egg used **Sonnet readers** (the owner's new rule, [[2026-11-19 Art rounds capped at 3; blind readers on Sonnet]]). In round 1 all three candidates sat in slots 2, 5 and 8; the readers could not tell them apart, so their reads cover all three.
- **Blind reads, round 1** (A, B, C):
  1. "a brown, speckled egg with a thin stalk curving up and over to the left ... My first impression is an anglerfish: a brown lumpy body with a lure on a stalk. ... at a glance it reads strongly as a burlap sack or money bag tied at the top"
  2. "the shape and colour say sack, fig or coconut before they say animal. ... As an animal, my guess is an anglerfish (the line as its lure)"
  3. "A mottled brown egg with a curved stalk or filament hooking over the top. My first guess is an anglerfish or a scorpionfish ... out of context it looks a lot like a brown sack tied with string"
- **Blind reads, round 2** (B2):
  1. "a spawn egg for a mottled brown bottom fish with a thin dark stalk curling off the top. That stalk makes me think of an anglerfish or monkfish with its lure."
  2. "It reads as an anglerfish, with the stalk as its lure. ... at a glance the item could read as a tied burlap sack, a potato or a turnip with a stem."
  3. "My first impression is a spawn egg for an anglerfish (monkfish). ... it strongly reads as a drawstring sack or money bag ... That was honestly my very first impression before 'fish'."
- **Blind reads, round 3** (B3):
  1. "probably a scorpionfish. Second guess: an anglerfish, because of the thin dark stalk at the top-left that could be its lure."
  2. "probably a scorpionfish (or a lizardfish). ... the thin dark stalk at the top left reads like a stray stick, a sprout or an antenna"
  3. "a mottled brown, sand-coloured bottom-dwelling fish with a thin spine or lure on top. That suggests a scorpionfish or weever, or an anglerfish because of the 'stick.'"
- **Blind reads, final, Sonnet readers** (B4, installed):
  1. "It reads as a brown, rough-textured animal, maybe a hedgehog, a porcupine, a rock crab or a brown frog or toad."
  2. "My first impression is a crab or a hermit crab. My second guess is a toad or a sea cucumber. ... The small tendril at the top left looks like a stray pixel."
  3. "My first impression is a crab or a toad. My second guess is a hedgehog or a mole. The mottled brown surface looks more like a pile of dirt or a potato than a clear animal."
- **Mixed result for the owner:** B2, the round-2 egg (a rod arching over the top), was named an anglerfish first by all three readers, but critics read it as a sack or handbag strap. The opened rod of B3/B4 fixed the critics' complaints, but readers then named a scorpionfish first and an anglerfish second. The Sonnet readers didn't see a fish in B4. B2 is still in the script if the owner prefers it.
- **Compare sheet:** `art/candidates/fish_petrica_egg.png` (not in git).

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [FishBase, *Lophius budegassa*](https://www.fishbase.se/summary/Lophius-budegassa.html)
- [FishBase, *Lophius piscatorius*](https://www.fishbase.se/summary/Lophius-piscatorius.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.

## Owner's verdict (2026-11-19)
- "All pass except john dory bucket. That needs a redo, consider very different possible version" ([[2026-11-19 Redos pass - lionfish, lizz bucket, petrica, gallinella icon; John Dory bucket again]]).

## Owner's verdict (2026-11-19, later)
- "John dory bucket: L, all eggs pass, switch back to opus guessers." ([[2026-11-19 John Dory bucket L; last four eggs pass; blind readers back to Opus]]).
