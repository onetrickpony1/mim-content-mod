# Mola mola: night log (2026-11-18)

Creative choices made by Claude on the night job ([[2026-11-18 Night job - the rest of the fish, Claude decides]]), for the owner to review. Nothing here is owner-accepted yet.

## Bucket (`art/src/fish_mola_bucket.py`, installed: candidate E)
**Retired 2026-11-19:** the mola has no bucket any more ([[2026-11-19 Mola mola - can be found, not captured; escapes when hurt; basks in the sun]]); the script is kept for history.
- **What shows:** only the front of the disc rising out of the water: a round, blunt dome with one eye high on it, a small beak mouth on the front edge low down, and the tip of the dorsal fin. No clavus, no anal fin, no tail.
- **Colours:** only icon A's palette (the model's hues a step darker), plus the shared bucket water and rim shades. No new colours.
- **Pale, smooth disc:** the dark grey-brown back band and the blotches were dropped after blind readers called a darker, mottled version a "grey-green mottled" bottom fish. The disc is now silver above and pale below, as in the out-of-water photos (mm07). The fin and the outline stay dark.
- **Narrow, round head:** a 12 px wide head read as a "flat, broad fish", so the head is 9-10 px wide and 6 tall.
- **Fin grown from the back:** a fin standing apart in the water behind the head (candidate D) was read as a tail, so in E the fin rises out of the dome's own back and leans back slightly.
- **No face:** the mouth is a dark nub on the outline with one pale lip pixel, two rows below and four pixels before the eye. Nothing dark touches the eye. The script checks both.
- **Kept the back rim:** the bucket's far rim shows at the right (11,2 / 11,3 / 12,3 / 13,4-5). The fish covers the rest.
- **Rounds:** five critic rounds. Round 1 picked B from A, B and C, with fixes (B2). Rounds 2-5 each passed (B2, B3, D, E), but blind reads kept failing, so each pass was redone until round 5.
- **Blind reads are weak evidence:** the readers can see the repo's git log, which names the mola. In the first test all three answered "Bucket of Mola Mola" but could not tell the three candidates apart, so that test was thrown out. Later tests used decoy buckets, or the bucket alone among vanilla items.
- **E's reads:** one "Bucket of Mola Mola (Sunfish)" (cue: deep, rounded body, no tail); two "a grey fish", with mola only as a fallback guess. Not a clean "sunfish" read. The owner should judge at 1x.
- **Compare sheet:** `art/candidates/fish_mola_bucket.png` (all candidates; not in git).

## Egg (`art/src/fish_mola_mola_egg.py`, installed: candidate B4)

**Owner 2026-11-19: passes** ([[2026-11-19 Spawn eggs - all eight pass]]).
2026-11-19, shared parts in `art/src/fish_egg_common.py`: **passed in round 3 of 3**; B4 (B3 with round 3's two fixes) waits for the owner. Started because the model and icon A were accepted ([[2026-11-18 Skorfna egg and mola mola model accepted]], [[2026-11-19 Night fish icons and buckets - most pass; John Dory, gallinella, lingwata bucket redo]]); it has no bucket ([[2026-11-19 Mola mola - can be found, not captured; escapes when hurt; basks in the sun]]).
- **Design:** vanilla's fish-egg outline and vanilla's own pool, in icon A's colours only. Features: the tall dorsal fin, swept back, rising from the egg's back shoulder (on the egg's top it made the egg come to a point, a garlic bulb); the clavus, a pale scalloped rim down the egg's back edge; and in B on, the anal fin as a short blade out of the lower back, mirroring the dorsal, so the egg carries the sunfish's outline (fin up, fin down, clavus between). Grey-brown back, silver side, pale belly, lit at the top left; the side flaps are the pectoral and the clavus. No eye, no face, no mouth.
- **Candidates:** A, the dorsal and the clavus; B, both fins; C, both fins a pixel shorter.
- **Critic round 1: FAIL (close), pick B.** "a dorsal fin above and an anal fin below is the sunfish's own outline, and a shark doesn't have it. That pair is the best way to separate this egg from the pixxispad. The trouble is that in B the anal fin is a dark G/H smudge on the pool at rows 12-13, so it doesn't show at 1x." "No reader mentioned the clavus." Fixes applied (B2): the fold darker U (11,9) (11,10), the clavus brighter W (12,9) (12,10) (11,7), the anal fin lifted (15,11) G with a lit edge (14,11) f, its tip (15,13) o.
- **Critic round 2: FAIL (close).** "Round 1's clavus fix works. The W pixels at (11,7), (12,9) and (12,10) now show as a pale rim down the back edge at 1x and 2x." "The anal fin is still a blob. ... a 2x3 square stub." "There is a lone pale speck outside the rim at (14,10)c." Fixes applied (B3): (15,11) cleared, (14,12) F, (15,13) H, (14,10) k, a diagonal blade down and back.
- **Critic round 3: PASS.** "The anal fin: fixed. It is now a diagonal blade down and back ... It mirrors the dorsal, so "fin up, fin down" reads at 1x on both the dark slot and the hotbar. On the light grey slot it is fainter, but you can still see it." "It is the only pale grey egg with a fin on top and a fin below." Its two fixes, applied (B4): (14,10) f, so no pale bump sits level with the pectoral; (12,4) G, so the dorsal is a broad triangle: "At 1x the dorsal fin is a 2 px wide diagonal blade with a 1 px tip, and it reads a little like a stem (a garlic bulb)."
- **Blind reads, round 1** (three fresh readers, A, B and C in slots 2, 5 and 8 among vanilla eggs; none could tell them apart):
  1. "A spawn egg in pale silvery grey-white, with a darker grey fin or spike sticking up at the top right. My first impression is a big grey fish with a tall dorsal fin, possibly a sunfish (Mola mola). A silvery fish such as a horse mackerel seen with its fin up is the other possibility. The spike could also be read as a shark fin."
  2. "A spawn egg in pale silvery grey-white, with a dark pointed tip at the top-right like a fin or beak. My first read is a large grey fish with a tall fin, most likely an ocean sunfish (mola mola), or possibly a shark. Without the fin it would just look like a pale stone or silverfish egg."
  3. "First impression: a pale silvery-grey/white spawn egg with a pointed flap sticking up at the top right. The flap reads like a dorsal fin, so it suggests a silvery fish such as a sea bream or horse mackerel. My second thought was a shark fin, because of the grey colour and the fin shape. Of the four, this is the least specific."
- **Blind reads, B2** (alone among eight vanilla water-mob eggs):
  1. "A pale silvery-grey spawn egg with darker grey streaks and a pointed fin or tail sticking out at the top right. It reads as a silver fish, perhaps a sea bass or a mackerel-type fish. My very first impression was a shark fin."
  2. "A whitish-grey, silvery spawn egg with a darker grey tail or fin flicking off the top right. It reads as a silver fish, perhaps a sea bream, sardine or mackerel-type fish."
  3. "A spawn egg, pale grey-white with a hooked point curling up at the top right, like a fin or tail tip. My first impression is a pale fish with a prominent fin, maybe a small shark or dogfish. The hook also made me think of a squid."
- **Blind reads, B3** (alone among eight vanilla water-mob eggs):
  1. "A spawn egg, pale silvery white with a darker grey top and a thin dark spike poking up and out at the upper right. My first impression is a swordfish, with the spike as its bill."
  2. "A spawn egg in light grey-beige with one sharp spike or fin sticking up at the top right ... My first impression is a fish with a tall pointed dorsal fin or a bill, so a swordfish or a shark fin."
  3. "A spawn egg in pale silver-grey, darker grey across the top, with a pointed fin sticking up at the top right. The fin reads first as a shark's dorsal fin, so I'd guess a grey shark, or else a dolphin."
- **Not a clean sunfish read.** Two of three named a sunfish in round 1, none since; no reader mentioned the anal fin or the clavus, and the dorsal reads as a shark fin or a bill. B4 (the broader fin) had no blind read. The owner should judge at 1x.
- **Compare sheet:** `art/candidates/fish_mola_mola_egg.png` (not in git).
