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
- The spawn egg is still a placeholder (not part of tonight's job).

## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.
- **A test note:** the quick one-fish test run (`FISH_ONLY=lionfish`) stops at its swim check, because a lionfish alone in the test pool only drifts about 0.35 blocks (it is slow and doesn't flee). In the whole fish test, among the other fish, it swims about 2.5 blocks and passes. The art was checked with the whole fish test instead; the check itself was left as it is.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [Guide Me Malta, lionfish confirmed in Maltese waters](https://www.guidememalta.com/en/spotted-invasive-lionfish-confirmed-in-maltese-waters-for-the-first-time)
- [MaltaToday, first sighting of devil firefish confirmed](https://www.maltatoday.com.mt/environment/nature/142885/scientists_confirm_first_sighting_of_devil_firefish_in_maltese_waters_)
- [divinginfo.mt, reward 2019](https://www.divinginfo.mt/reward-spot-the-lionfish/)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.
