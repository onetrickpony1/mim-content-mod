# Tird (wrasse): night log

Choices made overnight for [[2026-11-18 Night job - the rest of the fish, Claude decides]]. Summary in [[Night fish log 2026-11-19]]. † = not checked.

## Species and name
- **Species:** the ornate wrasse, *Thalassoma pavo*. *Tird* in the species report is the name for the wrasses as a family; this is the one picked to stand for them.
- **Why this wrasse:** a visual census of Maltese rocky reefs found *T. pavo* at high densities, and it is the bright green, busy wrasse snorkellers see everywhere in the shallows. That it is *the* commonest Maltese wrasse is my reading, not a counted fact†. Other wrasses (*Symphodus*, the brown wrasse *Mirli*) could be later versions.
- **Name:** shown as **Tird**. *T. pavo* has its own Maltese names in databases (for example *Lhudi*, *Tirda tal-passa*†), none checked; Tird is the sourced one.

## Size
- **Size in game:** 0.75 blocks long (12 px: 9 of body, 3 of tail), 3 px deep, 2 px wide; body box 0.35 x 0.3 (unchanged). Small and slim, clearly smaller than a vanilla cod. The placeholder was 0.69 blocks; the drawn model came out a pixel longer.
- **Why:** a real one is about 20 cm†. About 3.5 times life size, the same as the other small reef fish.

## Behaviour, spawns, rarity
- **Behaviour:** small and busy, 0.4 to 2.5 blocks over the floor, in groups of up to 3, shies from players, a bit quicker than the others when it swims about. Health 3.
- **Spawns:** over rock or seagrass (any floor). All the shallow seas (`bahar_sea`, `posidonia_meadows`, `qawra_inland_sea`, `dwejra_bahar_sea`, `dwejra_posidonia_meadows`), weight 12, groups of 1 to 3. Vanilla: warm and lukewarm, weight 6.
- **Rarity:** common.
- **Stings:** no.
- **Drops:** itself (1 raw fish, `mimcontent:tird`). Bucket, spawn egg. It is shark bait.

## Art
Made overnight by a maker, judged by a fresh critic each round from pictures only. Photos: free Wikimedia Commons ones (licences in `art/references/fish_tird_refonly/list.tsv`), two of them taken in Malta (Ċirkewwa and Cathedral Cave, Gozo).

**Which look:** the **male** (the "peacock" colours): a turquoise-blue head, a pale cyan bar and a red-orange band just behind it (a "collar"), and a green body. Picked because it reads most clearly at this tiny size. The female (green with red-orange bars, the commoner sight in the Malta photos) has a dark spot on the back that would sit too close to looking like a second eye. She is candidate C of the model, if the owner wants her instead.

**3D model** (`art/src/fish_tird_model.py`): passed in round 4 of 8.
- Three paint jobs tried: A the male, B the male with a bluer head, C the female. **A chosen.**
- **Looks:** small and slim, a short pointed snout, the black eye inside the blue head, one pink-violet pixel on the cheek, then the collar (pale cyan bar, red-orange band two pixels wide), a plain green body with a darker green back and a cream belly, a light teal dorsal fin all along the back, a small anal fin, small pale green pectoral fins and a crescent tail (green at its base, turquoise arms, mid-blue tips).
- **Colours:** head #4aa6c0, bar #b0fcf0, band #ff6a2a, back #64b048, flank #a8e050, belly #e4f0c4, tail tips #5a90c0. All a step lighter and brighter than the photos, because the water greys and blues them.
- Round 1 PASS with fixes (the red lines read as bands, the greens went teal, the belly looked muddy, the tail was stiff). Fixes made, then round 2 PASS with fixes (the eye touched the back line; the tail tips nearly as dark as the eye). Fixes made, then round 3 **FAIL**: the tail looked loose from the body under water, the single red-line pixels turned into maroon squares. So the tail was rebuilt solid on a wider stalk, the red lines were dropped and the band widened. **Round 4 PASS.**
- The real male has thin red lines down the green body. They were dropped: at this size they read as dirty squares under water.
- Round 4's optional polish, not done (left for the owner): lighter tail tips, a fuller crescent tail, a paler belly seen from below.
- A new review shot, `fish-tird-lineup` (tird, cod, cerna, small tonn in one tank), was added to the fish test.

**Item icon** (`art/src/fish_tird_icon.py`): passed in round 2 of 8.
- Head lower left, tail upper right, like vanilla's fish. Candidates: A (plain green body, like the model), B (two thin broken red lines), C (the bluer head). **A chosen** (the critic: B's lines turn into specks).
- **Colours:** the model's own, **not** lifted 1.2x: the model's colours were already pushed brighter for the water, and lifted again they read neon lime and pastel. The back's edge and belly rim are darker, so it has vanilla's darker outline.
- Round 1 PASS with fixes: the greens toned down toward olive, a dimmer belly, a clearer pale bar, the tail tips joined to the fin, the pink pixel moved away from the eye. Round 2 PASS.
- **Blind reads** (three fresh readers, neutral file names, among vanilla items), first lines word for word:
  1. "Slot 4 is a fish: a slim green-blue body with yellow-green stripes and orange fins and spots, like a wrasse or a mackerel."
  2. "**Fourth icon:** a slim, streamlined fish. Its back is blue-green, it has a yellow-green stripe along the side, and its belly and tail fins are pinkish-red."
  3. "Icon 4: a slender fish with a green-to-yellow-green back and a pale blue-grey belly, about the same size as the other fish."
- All three saw a fish; two named a wrasse among their guesses.

**Bucket** (`art/src/fish_tird_bucket.py`): passed in round 8 of 8, the last round allowed (a narrow pass).
- On vanilla's cod bucket, the head rises out of the water at the left, leaning up and left: a turquoise head that widens from its tip down to the water, the black eye inside it, then a near-white bar and the red-orange band stepping down the neck, and a little green at the waterline. The back rim stays dark to the right of the head, over a grey inner wall.
- The bucket uses its own greener turquoise, redder band and near-white bar (not the icon's exact colours): with the icon's colours it looked too much like vanilla's tropical fish bucket and the bar disappeared.
- The critics went back and forth: rounds 1 and 2 FAIL (specks, then "the whole fish lies across the bucket"), round 3 FAIL (rim lost, a blob), round 4 FAIL (an upright head with flat stripes read as a striped lid or a robot head), round 5 FAIL (a small diagonal smear), round 6 FAIL (an upright head on a "neck" read as a duck), round 7 FAIL (a thin leaning wedge read as a beak or a needlefish). **Round 8 PASS**: round 6's bigger head without the neck.
- Round 8's optional polish, not done (left for the owner): a bit more green at the waterline, a clearer pale bar, the band a pixel lighter, the snout tip a pixel further in.
- **Blind reads** of the passed bucket (three fresh readers, neutral file names, among vanilla buckets), first lines word for word:
  1. "Slot 3: a bucket holding a bright green-blue and red/orange fish. It looks like a wrasse, possibly a rainbow wrasse."
  2. "**Third icon (first line):** a bucket with water and a brightly coloured fish in it."
  3. "Icon 3: a bucket of water holding a small, very colourful fish."
- All three saw a fish bucket; all three named a wrasse (two said "ornate or rainbow wrasse").
- The spawn egg is still a placeholder (not part of tonight's job).

**Tests:** the one-fish run passes (swim, hit boxes, shots). The whole fish test (`SMOKE_ONLY=fish`) was run once: the tird's checks passed, and it failed only on the sawt's and the pixxi San Pietru's hit box rows (other makers' fish, still being drawn).


## Not decided (for the owner)
- Nothing here is owner-accepted yet. Change anything you like.

## Sources
- [[Maltese wildlife and flora]] (the species report)
- [EUNIS, *Thalassoma pavo*](https://eunis.eea.europa.eu/species/124408) (the Maltese names, from FishBase)
- the Malta and Lampedusa rocky reef visual census (see the marzpan's log)
- [FishBase, *Thalassoma pavo*](https://www.fishbase.se/summary/Thalassoma-pavo.html)
- Sizes marked † are from memory of FishBase's usual lengths, not re-checked tonight.
