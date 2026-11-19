# Lionfish: night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** *Pterois miles* (devil firefish), the lionfish recorded in Malta.
- **Name:** the species report found **no Maltese name**, so it is shown as **Lionfish**†. A Maltese name can replace it once one is sourced.

## Size
- **Size in game:** 0.94 blocks long (15 px), 0.69 wide with its fan fins, 0.63 tall with its spines. Body box 0.5 x 0.55.
- **Why:** a real one is up to about 35 cm†. About 3 times life size; the fins and spines are what make it.

## Behaviour, spawns, rarity
- **Behaviour:** slow (movement speed 0.5), bold: it doesn't shy from players. Hovers 0.3 to 2 blocks over rock and sometimes rests on it. Health 4.
- **Behaviour fix (2026-11-19, with the model redo):** a lone lionfish hardly moved (about 0.002 blocks a tick), so the quick test's swim check failed. The cause: it swam at 0.6 x its speed 0.5 = 0.3, and the fish movement's push grows with the square of the speed, so 0.3 is almost nothing. It now swims at its full speed 0.5 (still slower than vanilla's fish, 0.7) and picks a new spot about every 2 seconds instead of 4. In three quick runs it swam 4.25, 2.03 and 3.92 blocks; the check was not changed.
- **Stings:** yes, its spines. Touching it or hitting it in melee: 1 heart and Poison for 6 seconds, at most once every 2 seconds. Mobs that touch it too, other fish not. Arrows don't count. Creative, spectator, peaceful and Jellyfish Ward: never stung.
- **Spawns:** only over rock. `bahar_sea`, `dwejra_bahar_sea`, weight 1, alone. Vanilla: warm ocean only, weight 1.
- **Rarity:** rare: an invader that has only recently arrived (first seen 2016, a reward offered in 2019, and a first confirmed catch reported in January 2026). The content list's "cull the invader" idea isn't built.
- **Drops:** itself (1 raw fish, `mimcontent:lionfish`). Bucket, spawn egg. It is shark bait.

## Art
Made overnight by a maker, judged by a fresh critic each round from pictures only. Photos: free Wikimedia Commons ones (licences in `art/references/fish_lionfish_refonly/list.tsv`): a specimen out of the water for the true colour, side views and one from above (Red Sea) for the shape.

**3D model** (`art/src/fish_lionfish_model.py`): passed in round 2 of 8.
- **Size:** 15 px long (0.94 blocks), 3 px thick, 5 px deep; about 0.8 blocks tall with the spines. Bigger than a cod, much smaller than the cerna, about as long as the skorfna but taller and thinner. Body box unchanged (0.5 x 0.55).
- **Looks:** a slim, flat-sided body with bold vertical bands: broad dark chocolate red-brown bands with thin cream ones between, darker along the back, a plain off-white belly. Four long, separate spines lean back from the back, banded red-brown and cream with cream tips, joined only by a low strip at their base (the skorfna's are short and joined). The big fan fins hang down and back behind the head, with banded rays sweeping back over a light red-brown membrane and a fringed edge. A small banded tentacle over each eye, a pale snout, a small soft fin behind the spines, small fins underneath and a round banded fan tail.
- **The eye** is the only black mark: a black square in pale skin, with a dark bar down the cheek below it but nothing dark touching it.
- **Colours** (palette C, chosen by the critic as the one that survives the grey water): bands #58281c to #7e3e2c (the darkest on the back), cream #ece0cc, belly #f4ece0, fan membrane #b47058, rays #7c3a2a.
- **Candidates:** three paint jobs on one model: A red-brown, B brighter brick red, C darker chocolate brown. **C chosen**: A and B washed out to pale lilac under water.
- Round 1 FAIL: the body bands vanished under water, no countershading, the tail looked loose, the fans read as checkered wings from above, the dark snout made a frowning face, the tentacles didn't show, the spines' dark bands were as dark as the eye. **Round 2 PASS.**
- Polish not done (left for the owner): the fans from above are thin (the critic suggested widening them toward the tip), the fan rays from the side are a little ladder-like, the tentacles are small, and the tail could fill its corners.
- New review shots `fish-lionfish-lineup` and `-lineup-above` (lionfish, cod, skorfna, cerna and a small tonn in one tank over stone) were added to the fish test.

**3D model redo** (owner 2026-11-19: "its too fat and the colours are very flat", [[2026-11-19 Redo verdicts - lizz bucket, lionfish, lingwata Q, gallinella, John Dory]]): passed in round 2 of 3.
- **Slimmer:** the body is now 2 px thick (was 3) and 4 px deep (was 5), as compressed as the real fish. The length (15 px), the spines, the fans and the tentacles are kept. The fans are 3 px deep (was 4) and spread a little more, so the pale belly shows under them.
- **Colours with depth** (a new palette, D; the accepted icon keeps its own):
  - a dark brown top edge along the whole back, then the bands darkening toward the back and fading to a near-white belly row;
  - two band colours that stay apart under water: near-black brown (#321610 to #4a2014) and a lighter rust (#943a1e to #c4582e), alternating; cream warmed to peach (#f2c8b0) so it stays warm under the blue water;
  - every texel varies by up to 5 % so a band reads as skin, not a print;
  - the fins and spines lit at the top and shaded toward their far edge, the fans' face toward the body a step darker than the outer face, and the spines' and tail's right side a little darker than the left;
  - a pale ring round the eye on every side; in the eye's row the dark bands near it turn rust, so nothing near-black sits beside the eye.
- **Band patterns** tried on the same model: A (brown, then rust in the middle), B (rust, brown, rust), C (mixed). **C chosen** (the critic: the most separation between fan, body and spines).
- Redo round 1 FAIL: slimmer was right, but under water the colours collapsed to two tones (grey-lavender and plum), the fan hid the belly, the eye was close to the dark bands. **Redo round 2 PASS**. After the pass, its first polish point was applied: a near-black square behind the gill at eye height could pass for a second eye, so it is rust.
- Polish not done: continuous bands across the top of the back (from above it looks a little like the cerna's mottling), taller pale tentacles, one more rust row in the tail.

**Item icon** (`art/src/fish_lionfish_icon.py`): passed in round 2 of 8.
- Head lower left, tail upper right, like vanilla's fish. Colours: the model's palette lifted x1.2 for out of the water.
- **Looks:** an oval, diagonal body crossed by 2 px red-brown and 1 px cream bands, darker on the back, pale belly; a tan head with one band in front of the eye and the black eye on its own; a small red-brown tentacle with a cream tip over the eye; three separate spines standing up, red-brown with cream tips; a pinkish fan under the belly with dark rays sweeping back; a banded fan tail.
- **Candidates:** A (2:1 bands), B (wider bands), C (smaller fan, four spines). **A chosen** (B went muddy at 1x, C's spines looked like a comb).
- Round 1 FAIL: it read as a feather duster (thin body, the spines like bristles, a tail on a stick). Redrawn with a proper oval body. **Round 2 PASS (borderline).**
- Polish not done: a banded tail with a darker edge, a darker line along the back under the spines, more countershading, thin rays on the fan, smoother steps on the head's outline.
- **Blind reads** (three fresh readers, a neutral file name, among vanilla items), first lines word for word:
  1. "My best guess is that slot 3 holds a lionfish (Pterois miles, the invasive lionfish now found around Malta), shown as a raw fish item."
  2. "Slot 3 looks like a lionfish (Pterois, the invasive species now found around Malta)."
  3. "Slot 3 looks like a lionfish (Pterois, probably Pterois miles, the species now spreading through the Mediterranean)."
- All three named the lionfish. (They mention Malta, so they probably picked up the project from their surroundings; the stripes and spines were the reasons they gave.)

**Bucket** (`art/src/fish_lionfish_bucket.py`): passed in round 3 of 8.
- On vanilla's cod bucket, the head rises out of the water facing up and left: a mid-pink head with the black eye, a red-brown band behind the eye, a red-brown tentacle with a pale tip over it, and three separate spines behind (only the front one with a cream tip) standing on a back banded red-brown and dark brown that sinks into the water, with a dark fin ray breaking the surface. The back rim outline stays dark except behind the head.
- Round 1: candidates A (head low), B (head a row higher), C (a bigger fan tip). The critic passed A (B crowded the top, C's pink fan tip read as a tongue). But all three blind readers then saw A as a pale fish with **its jaws open and teeth showing** (a lizardfish, a barracuda, a moray): the cream spine tips over a pale band read as teeth. So the work went on.
- Round 2 FAIL (A2: the spines on a dark back, a darker head): the solid dark back now read as an open mouth, and the cream tips as teeth.
- **Round 3 PASS (A3):** the back banded instead of solid, only the front spine tip cream, a mid-pink head with a band behind the eye. One polish point applied after the pass: the cream pixel on the snout (a hint of a lip) is pink.
- Polish not done: a solid band behind the eye (it would touch the eye), one cream stripe in the back's bands, a darker pixel beside the eye.
- **Blind reads of the final bucket** (three fresh readers, a neutral file name, among vanilla items), first lines word for word:
  1. "My best guess is that slot 3 is a bucket holding a lionfish, a fish in water like the vanilla bucket of fish."
  2. "Best guess: slot 3 is a bucket of fish, a water bucket like vanilla's fish buckets, holding a lionfish."
  3. "Slot 3 is a modded bucket of fish: a water bucket with a pinkish-red and white fish poking out."
  (The third went on: "my best guess is a lionfish (Pterois)". The second guess of all three was a red scorpionfish.)
- Round 1's blind reads (version A, replaced), first lines: "Slot 3 holds a modded bucket of fish (styled like vanilla's "Bucket of ..." items)." (a lizardfish), "Slot 3 is a modded fish bucket, a vanilla-style water bucket with a pale, silvery-white fish sticking out of the top." (a barracuda), "Slot 3 is a modded bucket of fish, a water bucket with a pale fish whose head sticks up out of it." (a moray).
- The spawn egg was still a placeholder (not part of tonight's job); it was drawn on 2026-11-19, see "Egg" below.

## Egg

**Spawn egg** (`art/src/fish_lionfish_egg.py`, shared parts in `art/src/fish_egg_common.py`, the line-aware eye check in `art/src/fish_egg_lines.py`), 2026-11-19: **passed in round 3 of 3**; A4 installed, waiting for the owner. Started because the owner passed the redone model ([[2026-11-19 Redos pass - lionfish, lizz bucket, petrica, gallinella icon; John Dory bucket again]], [[2026-11-18 Approving a step starts the next; skorfna bucket]]).
- **Design:** vanilla's fish-egg outline and vanilla's own pool, only the accepted icon's colours. Two features: the bands (wide rust-maroon with thin, broken cream lines wrapped round the egg, fading into a salmon belly) and the long, separate rust spines over the top. The side flaps are banded fan fins. No eye, no face.
- **Candidates:** A diagonal bands, 2 px rust and 2 px cream; B 2 px rust and 1 px cream; C B with the fans breaking the outline. The maker's own first try, bands meeting at the top like a melon, read as a circus tent and was dropped before the critic.
- **Critic round 1: FAIL, pick A:** "in both hotbars the first read is a red-and-white peppermint candy or circus tent with birthday candles on top. 'Lionfish' only comes second." Fixes, all applied (A2): rust spines instead of pale tips ("The pale J tips on the spines read as candle flames"), less white, a salmon belly "so the stripes fade out low down", uneven band widths.
- **Critic round 2: FAIL on A2:** "Still candy. At 1x and in the x2 and x4 hotbars, the body is even, parallel, high-contrast diagonal stripes, all leaning the same way." "(6,2) J is a pale lone speck ... reads as a candle flame or spark." Fixes, all applied (A3): thin 1 px cream lines so the rust takes over, the lower bands bent toward upright, the spines all rust and joined to the outline, banded fans.
- **Critic round 3: PASS on A3:** "it reads as a rust-red egg with pale streaks and thin spines on top. It's a lionfish-coloured spawn egg, not a candy." "Not a jellyfish: It has no dome-plus-tentacles look ... Not the skorfna: ... A3 is banded rust and cream with three separate, spaced spines." Its optional polish applied (A4): the tallest spine's pale tip rust, "This removes the lone pale speck."
- **How the reads were done:** three fresh readers per round, no context, each shown one hotbar per fish at GUI scale 4 (light and dark backdrop) with the egg among vanilla water-mob eggs, under neutral file names. Rounds 1-3 used the usual readers; the final read of the installed egg used **Sonnet readers** (the owner's new rule, [[2026-11-19 Art rounds capped at 3; blind readers on Sonnet]]). In round 1 all three candidates sat in slots 2, 5 and 8; the readers could not tell them apart, so their reads cover all three.
- **Blind reads, round 1** (A, B, C):
  1. "a red/salmon and white egg with diagonal stripes and a few small white dots sticking up from the top. My first impression is a lionfish: red-white stripes plus spines. Second guess: a striped shell or a hermit crab, and if you don't think fish, a peppermint candy."
  2. "My first impression was a candy-cane or peppermint sweet, or a striped circus tent. As an animal, my best guess is a lionfish"
  3. "A spawn egg covered in red and white diagonal stripes, with white specks spraying out of the top like spines. My first guess is a lionfish (Pterois)."
- **Blind reads, round 2** (A2):
  1. "My first impression is a spawn egg for a striped, spiny sea fish. The red-and-white bands and the red spikes on top make me think of a lionfish. ... at a glance it reads as a candy-cane party hat or a striped traffic cone."
  2. "It reads clearly as a lionfish, with the stripes as its bands and the tufts as its venomous spines. ... the clean diagonal candy-cane stripes and the 'bow' on top make it look a little like a candy cane, a wrapped present or a Christmas bag."
  3. "My first impression is a spawn egg for a lionfish. The diagonal red-and-white stripes and the red spiky bits sticking up from the top read clearly as a striped fish with venomous spines."
- **Blind reads, round 3** (A3):
  1. "a red-and-white striped fish with spines, most likely a lionfish (Pterois). ... at hotbar size it also reads as a striped cone, a candy-cane tent or a striped pinecone."
  2. "My first impression is a spawn egg for a lionfish. It is a tall cone with red-brown and white diagonal stripes and thin red spines sticking up and out at the top."
  3. "a spawn egg for a red-and-white striped spiny fish. The diagonal stripes and the thin spines sticking up from the top make me think of a lionfish."
- **Blind reads, final, Sonnet readers** (A4, installed):
  1. "a cream/tan egg with red-brown diagonal stripes and a few small red spikes or antennae on top. It reads as a striped, spiky sea creature, maybe a striped crab or a banded shrimp or lobster. A second guess is a sea urchin or a striped fish."
  2. "My first impression is a striped or banded creature, maybe a red-and-white striped fish (a lionfish-like fish with spines) or a striped shrimp."
  3. "My first impression is a striped sea slug or a striped cone-shaped shell. My second guess is a lionfish."
- Rounds 1-3: all nine readers named the lionfish first, though most also saw a candy or cone. The Sonnet readers were vaguer: one said lionfish first, one second, one a striped crab. No reader saw a jellyfish or the skorfna.
- **Compare sheet:** `art/candidates/fish_lionfish_egg.png` (not in git).

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.
- **A test note:** the quick one-fish test run (`FISH_ONLY=lionfish`) stops at its swim check, because a lionfish alone in the test pool only drifts about 0.35 blocks (it is slow and doesn't flee). In the whole fish test, among the other fish, it swims about 2.5 blocks and passes. The art was checked with the whole fish test instead; the check itself was left as it is.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [Guide Me Malta, lionfish confirmed in Maltese waters](https://www.guidememalta.com/en/spotted-invasive-lionfish-confirmed-in-maltese-waters-for-the-first-time)
- [MaltaToday, first sighting of devil firefish confirmed](https://www.maltatoday.com.mt/environment/nature/142885/scientists_confirm_first_sighting_of_devil_firefish_in_maltese_waters_)
- [divinginfo.mt, reward 2019](https://www.divinginfo.mt/reward-spot-the-lionfish/)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.

## Owner's verdict (2026-11-19)
- "All pass except john dory bucket. That needs a redo, consider very different possible version" ([[2026-11-19 Redos pass - lionfish, lizz bucket, petrica, gallinella icon; John Dory bucket again]]).

## Owner's verdict (2026-11-19, later)
- "John dory bucket: L, all eggs pass, switch back to opus guessers." ([[2026-11-19 John Dory bucket L; last four eggs pass; blind readers back to Opus]]).
