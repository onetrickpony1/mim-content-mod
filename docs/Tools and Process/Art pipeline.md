---
type: "topic"
---
# Art pipeline

How the mod's art is made and checked (since the art pilot, 2026-11-17). The details are in `art/README.md` and `art/STYLE.md` in the repo.

1. **Reference photos** of the real thing (Wikimedia Commons, licences recorded).
2. **Scripts make the art**: textures from shape, light, palette and noise rules; models from box geometry. Nothing is painted by hand, so everything can be re-made.
3. **Measured against vanilla**: colours, contrast, outline and light direction are kept inside vanilla's own numbers.
4. **Seen in the game**: `tools/run-art.sh` builds the mod and takes screenshots on an invisible desktop (never on the owner's screens), beside vanilla blocks and items.
5. **Judged by an independent reviewer**, never by whoever made it (owner, 2026-11-17). Fixes follow the review, then it is reviewed again.

## Since the pilot: maker, critic, owner (2026-11-17)
The owner rejected art that reviewers had passed, and asked for the work to be orchestrated ([[2026-11-17 The pastizz is the flagship, with ricotta and pea kinds]] and the decisions after it).
1. **The owner's photos first.** The owner puts photos in `~/Pictures/<Dish>/`. They're copied to `art/references/*_owner*/`, kept **out of git**, used for reference only and never traced. They outrank web research.
2. **A maker** draws candidates (usually two or three) with a re-runnable script: `art/src/food_items.py` (bread, pastizzi, ġbejna), `sweets.py`, `bowls.py` (the shared terracotta bowl and the first four bowl dishes), `soppa.py`, `minestra.py`, `kawlata.py`, `brodu.py` (kusksu and the two broths), `oven_dishes.py` (the slice dishes and their icons), `torta_icon_cake.py`, `fish.py` (lampuka), `gbejniet.py` (dried and peppered) and `drinks.py` (Kinnie). The scripts reproduce every accepted texture byte for byte.
3. **A separate critic**, new each round, judges at true hotbar size and in the game, gives exact pixel fixes, and the maker applies them. This loops until the critic passes it.
4. **The owner decides.** Their picks and corrections are recorded in [[Decisions]] with their exact words. Then the item moves to **In the mod** in [[Food in the mod]] and [[Food progress]], and `art/tools/doc_pictures.py` refreshes that page's pictures.
5. **Rules learnt along the way:**
   - vertical centre about 7.5–8 like vanilla foods;
   - lit from the top-left;
   - Maltese letters in every label (`art/tools/font.py`);
   - a dish's icon shows the whole uncut dish;
   - a dish's container must match its placed block (a square pan).

## Fish art: lessons learnt (2026-11-18)
Each lesson came from an owner correction; the decision notes hold their exact words.

**How the work is organised**
- **One maker per piece.** Makers asked for several pieces at once did worse work ([[2026-11-18 Fish art - one maker per piece, three at a time]]).
- **One fish's pieces in series, different fish in parallel**, at most 4 makers at once ([[2026-11-18 Fish art - one fish in series, fish in parallel]]):
  - The **item icon comes first** and sets the fish's look and palette.
  - The bucket, spawn egg and 3D model follow one at a time, each after the owner accepts the one before. They reuse the icon's exact colours.
  - **Nothing moves on without the owner's OK**, whichever piece comes first: if the 3D model is first, the icon waits for the owner to approve the model ([[2026-11-18 Fish art - owner approves each piece before the next]]).
  - When pieces of one fish ran in parallel, a rejected icon forced its bucket and egg to be redone too.
- **Makers find their own reference photos.** Any photo is fine for reference, not only Creative Commons.
- **For true colour, use photos of the fish out of water**: caught, on a boat, at the market. Water tints colour, and the moray turned out violet-brown, not olive ([[2026-11-18 Murina icon - clearer head, check colour out of water]]).

**What the owner looks for**
- **Rounded edges, including the mouth.** Outlines step in 1-3 px runs like vanilla cod and salmon, with no long straight walls and no blocky jaws ([[2026-11-18 Cerna icon - rework, hard edges and flat colours]]).
- **Real shading, not flat fills.** Use a light ramp from the lit top-left back to the shaded belly, with 4-6 mixed body tones. Fins and tail are shaded too. Body tones that sit too close together still read as flat.
- **Changes must show at 1x.** A rework that looks the same at normal size is a failed rework. Show the rejected and new versions side by side, at 1x, 2x and 8x.
- **Builds are compared against each other.** "As fat as the tuna" sent the sardina back. The ċerna is the bulky one, and the awrata must not share its silhouette. Report proportions against the accepted fish.
- **Sizes need not be life-size.** The tonn comes in mixed sizes, 2 to 4 blocks. The seahorse is bigger than life so its detail shows.
- **No second eye, no face.**
  - No dark spot, bright spot, tooth or coloured dot near the eye or in the eye's row.
  - No row of 1 px dark dots on a model that reads as extra eyes.
  - No lone bright specks.
  - Gold or yellow beside the eye reads as a beak.
- **Spawn eggs are stylised eggs.** Keep the egg outline in its own pool and paint the fish's features on it, the vanilla 26.x way: a cap, one eye, a pale belly patch, side fin flaps, and one or two signature parts breaking the outline. A whole fish squeezed into the egg read as "a fat version of the fish" ([[2026-11-18 Sardina egg - a representation, not a fat fish]]).
- **Spawn eggs keep vanilla's EGG outline** ([[2026-11-18 Three eggs rejected - must be egg-shaped; cawl and shark buckets accepted]]): a narrow top widening downwards, about rows 3-15 with the pool. A round ball read as a pufferfish, a whole animal filling the slot read as the animal, and a band across the middle read as a Pokéball. Signature parts may poke out a little, but the silhouette stays an egg. Any pale point sticking out at eye height in front of the head reads as a bird's beak, even a swordfish's sword ([[2026-11-18 Seahorse and incova eggs accepted; swordfish egg reads as a bird]]).
- **The pool under a spawn egg is vanilla's own**, the owner's one exception to "never copy vanilla pixels" (STYLE rule 3) ([[2026-11-18 Boll egg B; egg pools match vanilla]]): the same 30 pixels in the same 5 blues as vanilla's cod, salmon, pufferfish and tropical fish eggs (rows 12-15; the egg's bottom edge sits on row 13, x 5-10). `art/src/egg_pool.py` holds it: egg scripts call `vanilla_pool()`, which keeps the egg as drawn (where its body covers a pool pixel, the body stays), and their copy checks allow those pool pixels and fail on any other copied pixel. Where an egg sits off-centre (the pixxispad), it gets "a full circular pool under it" (owner): vanilla's whole pool and colours, closed into a ring where vanilla's egg would stand, and moved sideways under the egg's own base, keeping inside the slot. The egg stays in front and is not changed.
- **Blind reads settle hard icons.** When critics go round in circles, give the icon to a fresh viewer with no context, alone among vanilla items at 1x and 2x, and ask what animal it is. Send it to the owner only when the first word is the right animal ([[2026-11-18 Blue shark egg accepted]]).
- **Buckets show the head**, rising out of the water, the vanilla way, and never the tail: a whole fish looked "snapped in half" ([[2026-11-18 Cerna bucket - head showing, not the whole fish]]).
  - The bucket is a layered model: the player's own vanilla `cod_bucket` with our fish-only layer on top.
  - The layer must cover every cod pixel, using our own water where the fish doesn't reach (`check_cover()` in the bucket scripts).
  - The layer must copy no vanilla pixel.
  - The lampuka, tonn and sardina buckets still show the whole fish. Check them before publishing.

**3D models**
- **Water greys every colour.** Use a palette a step lighter than the photos, and judge under water beside vanilla cod, which greys the same way.
- **Stay close to the icon's colours.** Lift the icon's palette by about x1.2 at most and keep its hue. Bigger lifts drifted: the ċawl turned ċerna-orange and the inċova's back turned emerald ([[2026-11-18 Cawl model accepted]]).
- **Every fin touches the body**, with solid edges.
- **Upright animals need their own animation.** The seahorse should hover and bob, not wag like a fish.

**Small things**
- **Never copy vanilla pixels** (STYLE rule 3). Spawn eggs are checked with a copy-check script.
- **Progress pages use standard picture links**, `![Lampuka](images/lampuka.png)`, never Obsidian's `![[x.png]]`, which GitHub shows as plain text. Icons are saved at 128x128 (8x, no smoothing) and live shots at 320x180, so they show at a useful size without a size setting, as in [[Food progress]].

## When the game is needed (2026-11-18)
Owner decision: [[2026-11-18 Icons previewed offline; in-game tests for models and per category]].
- **Flat icons** (item icons, buckets, spawn eggs) are judged offline in the real hotbar with `art/tools/hotbar_preview.py`. It pastes them into the vanilla hotbar sprite at the game's GUI scale, over a light and a dark backdrop, next to vanilla items. The game draws a flat item as its 16x16 texture scaled up with no filtering, so the preview matches the in-game hotbar. Layered buckets are composited over the vanilla `cod_bucket`, as the game does. Example: `art/.venv/bin/python art/tools/hotbar_preview.py out.png mc:cod mod:lampuka bucket:cerna_bucket --select 1` (add `--scale 4` for a closer look).
- **Anything that benefits from the game** still gets an in-game run (`tools/run-art.sh`) every time: 3D models, entities, blocks, animation, anything lit or seen in water.
- **When a category is finished** (for example all tier A fish), one in-game run checks all its icons together, to prove they load and work.


## Fish models (contract for the art makers, 2026-11-17)
The tier A fish ([[Fish]]) were built with **placeholder art** (plain boxes, made by `art/src/fish_placeholders.py`) so the mobs could be tested first; the pixxispad and the other tier B fish too; the boll and the skorfna (2026-11-18) started on it too, and their real art has since replaced it piece by piece (the skorfna's model, icon and bucket are accepted; its spawn egg waits for the owner). The script takes the fish to make by name (`fish_placeholders.py pixxispad`) and never overwrites a file that already exists. Real art replaces these files at the same paths:

| What | Path (under `mod/src/main/`) |
|---|---|
| Model | `java/com/maltaminecraft/mimcontent/client/fish/<Name>Model.java` (`LampukaModel`, `TonnModel`, `SardinaModel`, `CernaModel`, `AwrataModel`, `MurinaModel`, `ZiemelModel`, `PixxispadModel`, `IncovaModel`, `CawlModel`, `HutaKahlaModel`, `BollModel`, `SkorfnaModel`; the night job's placeholders `KavallModel`, `LizzModel`, `MarzpanModel`, `TirdModel`, `TriljaModel`, `SawtModel`, `PixxiSanPietruModel`, `PetricaModel`, `LingwataModel`, `HmarModel`, `GallinellaModel`, `LionfishModel`) |
| Mob texture | `resources/assets/mimcontent/textures/entity/fish/<id>.png` |
| Caught fish icon | `resources/assets/mimcontent/textures/item/<id>.png` (none for the żiemel; the lampuka's is accepted art) |
| Bucket icon | `resources/assets/mimcontent/textures/item/<id>_bucket.png` |
| Spawn egg icon | `resources/assets/mimcontent/textures/item/<id>_spawn_egg.png` |

A model class must:
- be `public class <Name>Model extends FishModel` with a constructor `public <Name>Model(ModelPart root) { super(root); }` and `public static LayerDefinition createBodyLayer()` (texture size of your choice);
- have a root child named **`body`** (required);
- optionally have **`tail_fin`**, a child of the root (or of `tail`): it sways like vanilla cod's tail fin;
- optionally have **`tail`**, a child of the root: the back half of a long fish (the murina), swaying more gently, like vanilla salmon's back; put `tail_fin` inside it so the fin follows;
- face **-z** (head toward -z), with y 24 at the ground, like vanilla's `CodModel`. Any other parts (fins, head) are free.

**Rays (the boll) are different** ([[2026-11-18 Stingray next - the common stingray]]): `BollModel` extends **`RayModel`** (itself a `FishModel`), which gives it its own animation instead of the fish wag, the way the seahorse has its own hovering one. A ray model must have:
- **`body`** (root child): the middle of the flat disc, head toward -z, ground at y 24. It stays flat: no yaw wiggle (its renderer's wiggle is 0).
- **`left_wing`** (+x) and **`right_wing`** (-x), children of `body`, pivoted where they join the body: they flap up and down together, mirrored.
- optionally **`left_wing_tip`** and **`right_wing_tip`**, children of the wings, pivoted where they join: the outer edges, flapping a little later and further, so the wing ripples from the body out. The placeholder has them.
- optionally **`left_wing_edge`** and **`right_wing_edge`**, children of the tips: a third ring that follows the tip one step later. At rest and on land the wings only lift upward, so they never dip into the floor.
- **`tail`** (root child), pivoted at the back of the disc and running toward +z: it trails and sways slowly. The spine goes on the tail, near its end, as a child part **`spine`** (the placeholder's; not animated) or as cubes of the tail.
- The ripple is gentle (0.1 radians) while it lies still and grows to about 0.32 as it swims; on land the wings only flutter a little. The renderer keeps a ray **flat on land** (`liesFlat`, not on its side), and its hit boxes are marked flat in `FishShape` to match; the test checks the two agree.

**The skorfna** (black scorpionfish) is a normal `FishModel`. Its model names its parts for the makers: `body` (cubes: head with the eyes, jaw for the big mouth, trunk, and the stalk at the tail's base), `head_flaps` (a child of `body`: the fleshy flaps over the eyes), `top_fin` (the tall spiny dorsal fin), `left_fin` / `right_fin` (the fan-like pectoral fins, spread flat to rest on) and `tail_fin` (the rounded tail, which sways). It mostly lies still on the floor, so the model is seen at rest from above and the side more than swimming.

**The night job's twelve** (2026-11-18) are placeholder `FishModel`s whose parts are named for the makers: `body`, `top_fin`, `tail_fin`, and where they matter `left_fin` / `right_fin` (the gurnard's blue wings, the lionfish's fans, the anglerfish's fins) and `lure` (the anglerfish's rod). The petriċa and the lingwata are flat (`liesFlat`, `flatShape`): they lie flat on land like the boll. Their review shots are `fish-<id>-side`, `-three-quarter`, `-top`, `-beside-cod` and `-on-land` (`placeholderShots` in `FishCheck`); extend them as the art needs. After a new model, paste the row the fish test prints into `FishShape`.

**The mola mola** (ocean sunfish, 2026-11-18) is a `FishModel` with its own animation, like the seahorse: `MolaMolaModel` (made by `art/src/fish_mola_model.py`) has `body` (the disc, eyes, mouth), `dorsal_fin` and `anal_fin` (pivoted at their bases: they scull from side to side together, both tips to the same side), `clavus` (the scalloped rim behind, a slow rudder) and `left_fin` / `right_fin` (the pectorals). It has no `tail` or `tail_fin`. It is far taller than thick, so lying on its side (on land, or basking at the surface) its renderer moves it back along its height by `SIDE_SHIFT` (so its middle, y 4.5, lies over its position); `FishShape` copies that as `sideShift` and the fish test checks the two agree, as for the land lift.

The swimming animation lives in `FishModel` and the body wiggle and flopping on land in `FishRenderer`, so a model only names its parts. Sizes: the model can be its real size; the body box in `MimFishes` is only for swimming (see [[Fish]]). Test with `SMOKE_ONLY=fish ART_RUN=<name> tools/run-art.sh`: the `fish-*` shots show all seven in a glass tank beside vanilla cod and salmon, on land, and the items, buckets and eggs in the hotbar.

**Hit boxes come from the model** ([[2026-11-18 Fish hitboxes match their size]]). Each fish is hit through a chain of boxes measured from its model at rest, fins, sword and tail included: the length from snout to tail is cut into equal slices of about 6 px (at least 2, at most 8), and each slice gets a box as tall as the cubes reaching into it and as wide as they are or as long as the slice, whichever is more. The numbers live in a table in `entity/fish/FishShape.java`, because the server can't read client model classes. **After changing a model, run the fish test** (`SMOKE_ONLY=fish`, or only this part with `SMOKE_ONLY=fish-hitboxes`): it measures every baked model again and fails on any fish whose row no longer matches, printing the new row to paste in. It also checks the land lift in `MimContentClient` against the table (copy a changed lift into `FishShape` too), and the murina's boxes against its wave (a new long fish that bends needs its sections added to `FishShape`'s `Wave`). The `fish-hitbox-*` shots show the chains with F3+B.

## Jellyfish models (contract for the art makers, 2026-11-18)
The three jellyfish ([[Jellyfish]]) are built as mobs. Placeholder art comes from `art/src/jelly_placeholders.py`, which never overwrites a file that already exists (a maker's model or texture is kept). Real art goes at these paths:

| What | Path (under `mod/src/main/`) |
|---|---|
| Model | `java/com/maltaminecraft/mimcontent/client/jelly/<Name>Model.java` (`MauveStingerModel`, `FriedEggJellyfishModel`, `ManOWarModel`) |
| Mob texture | `resources/assets/mimcontent/textures/entity/jellyfish/<id>.png` (`mauve_stinger`, `fried_egg_jellyfish`, `man_o_war`); its size is the model's choice |
| Spawn egg icon | `resources/assets/mimcontent/textures/item/<id>_spawn_egg.png` |
| Drops | `textures/item/jellyfish_venom.png`, `textures/item/jellyfish_meat.png` |
| Jellyfish Ward effect icon | `textures/mob_effect/jellyfish_ward.png` (18 x 18, like vanilla's) |

A model class must:
- be `public class <Name>Model extends JellyfishModel` with a constructor `public <Name>Model(ModelPart root) { super(root); }` and `public static LayerDefinition createBodyLayer()`;
- have a root child named **`bell`** (required): the bell, or for the man o' war the float;
- optionally have **`tentacle_0`** to **`tentacle_N`** (numbered from 0 with no gaps), children of the root or of `bell`: each sways gently, out of phase with the others. Out of water a bell's tentacles splay out from the middle, as the animal lies flat;
- optionally have **`oral_arms`**, a child of `bell`: it sways slowly;
- have y 24 at the bottom of the mob's box. Any other parts are free.

What `JellyfishModel` does: a bell pulses with a slight squash and stretch (wider and lower, then back) each time the jellyfish pulses upward, breathes faintly between pulses, and slumps a little on land, all scaled from the bell's pivot (pivot it at the rim to squash toward the rim). The man o' war's float doesn't pulse: it bobs and tilts on the surface. The renderer draws every jellyfish **translucent** (an entity translucent render type), so a texture's alpha shows; a flashing mauve stinger is drawn full-bright.

**The box comes from the model.** The mob's box is the model's size: as wide as the widest part (x or z), and as tall as from y 24 up to the top, tentacles included. For the man o' war only the float counts (its tentacles hang 3.5 blocks below the box as a stinging column, `Jellyfish.MAN_O_WAR_TENTACLE_LENGTH`). The sizes are in `MimJellyfish`. **After changing a model, run the jelly test** (`SMOKE_ONLY=jelly ART_RUN=<name> tools/run-art.sh`): it measures each baked model and fails if a box is more than about 1 px off, or if the man o' war's tentacles no longer reach about 3.5 blocks. Its `jelly-*` shots show each jellyfish beside a vanilla cod and squid from the side, three-quarters and below, all three together, and the mauve stinger flashing at night.
