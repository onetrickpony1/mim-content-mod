package com.maltaminecraft.mimcontent;

import com.maltaminecraft.mimcontent.entity.fish.BollFish;
import com.maltaminecraft.mimcontent.entity.fish.HutaKahlaFish;
import com.maltaminecraft.mimcontent.entity.fish.MimFish;
import com.maltaminecraft.mimcontent.entity.fish.MimSchoolingFish;
import com.maltaminecraft.mimcontent.entity.fish.MolaFish;
import com.maltaminecraft.mimcontent.entity.fish.SkorfnaFish;
import com.maltaminecraft.mimcontent.entity.fish.TonnFish;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;
import net.fabricmc.fabric.api.biome.v1.BiomeModifications;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectors;
import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.fabricmc.fabric.api.object.builder.v1.entity.FabricEntityType;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.entity.SpawnPlacements;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import net.minecraft.world.entity.animal.fish.WaterAnimal;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.MobBucketItem;
import net.minecraft.world.item.SpawnEggItem;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.material.Fluids;

/**
 * The tier A fish (owner, 2026-11-17: "begin building all the tier a fish"): each a live mob that swims like vanilla's
 * cod, drops itself as an item (the żiemel tal-baħar drops nothing), and has a spawn egg and a bucket with the fish
 * alive in it. They spawn in the Malta world's sea biomes, and (switch {@code fish_in_vanilla_oceans}, on by default)
 * in vanilla's warm and lukewarm oceans.
 * Sizes are the real fish scaled down the way vanilla scales cod and salmon. Art is placeholder for now.
 */
public final class MimFishes {
    /** One tier A fish: its live mob, the item it drops (null for the żiemel), its bucket and its spawn egg. */
    public record Fish(String id, EntityType<? extends AbstractFish> type, Item item, Item bucket, Item spawnEgg) {
    }

    public static final List<Fish> ALL = new ArrayList<>();

    // Schooling fish (follow a leader like cod). Hitbox width and height in blocks, health, school size.
    public static final Fish SARDINA = schooling("sardina", 0.4F, 0.25F, 3.0, 12, () -> MimContent.item("sardina", Item::new, new Item.Properties()));
    // The tonn comes in mixed sizes, 2 to 4 blocks long (TonnFish); the hitbox and health here are for its model's own
    // length (2.44 blocks) and scale with each fish.
    public static final Fish TONN = schooling("tonn", 1.3F, 0.7F, 12.0, 5, TonnFish::new, () -> MimContent.item("tonn", Item::new, new Item.Properties()));
    public static final Fish LAMPUKA = schooling("lampuka", 1.0F, 0.45F, 6.0, 6, () -> MimContent.LAMPUKA);
    // Fish that swim alone. The last number is how many can spawn together.
    public static final Fish AWRATA = solitary("awrata", 0.7F, 0.45F, 4.0, 4, () -> MimContent.item("awrata", Item::new, new Item.Properties()));
    public static final Fish CERNA = solitary("cerna", 0.9F, 0.7F, 10.0, 1, () -> MimContent.item("cerna", Item::new, new Item.Properties()));
    // TODO murina: bites when disturbed and hides in rock holes (later, with the other behaviours)
    public static final Fish MURINA = solitary("murina", 0.9F, 0.3F, 8.0, 1, () -> MimContent.item("murina", Item::new, new Item.Properties()));
    /** Protected in Malta: drops nothing, only to be looked at (or carried in a bucket). */
    public static final Fish ZIEMEL = solitary("ziemel", 0.4F, 0.8F, 2.0, 2, () -> null);
    // Tier B (owner, 2026-11-18: "send a new agent to work on the swordfish"). Big like the tonn and fast: it swims at
    // twice vanilla's fish speed (movement speed 1.4, vanilla 0.7).
    public static final Fish PIXXISPAD = solitary("pixxispad", 1.3F, 0.6F, 12.0, 1, 1.4, () -> MimContent.item("pixxispad", Item::new, new Item.Properties()));
    // Tier B (owner, 2026-11-18: "start on incova, cawl, and huta kahla/blue shark").
    // The inċova (anchovy): a shoal like the sardina's, a little smaller and slimmer.
    public static final Fish INCOVA = schooling("incova", 0.35F, 0.2F, 3.0, 12, () -> MimContent.item("incova", Item::new, new Item.Properties()));
    // The ċawl (damselfish): small, deep-bodied, in small groups over shallow rock.
    public static final Fish CAWL = solitary("cawl", 0.35F, 0.4F, 3.0, 6, () -> MimContent.item("cawl", Item::new, new Item.Properties()));
    // The ħuta kaħla (blue shark): about 2.75 blocks long, alone, neutral (HutaKahlaFish); bites for 4 (2 hearts).
    public static final Fish HUTA_KAHLA = shark("huta_kahla", 1.3F, 0.7F, 16.0, 0.9, 4.0, () -> MimContent.item("huta_kahla", Item::new, new Item.Properties()));
    // Tier B (owner, 2026-11-18: "Work on the stingray next"). The boll (common stingray): a flat disc 1 block wide with
    // a long whip tail, about 2.1 blocks long; lives on sandy bottoms, alone or in twos, and stings (BollFish).
    public static final Fish BOLL = ray("boll", 1.25F, 0.25F, 10.0, 2, () -> MimContent.item("boll", Item::new, new Item.Properties()));
    // Tier B (owner, 2026-11-18: "get another agent started on the skorfna"). The skorfna (black scorpionfish): stocky
    // and spiny, about 0.8 blocks long; alone, rests on rocky bottoms, and its spines sting (SkorfnaFish).
    // Each version drops its own item (owner 2026-11-18, "Skorfna icon D accepted; each colour drops its own item"): the
    // black one skorfna (Black Skorfna), the red one skorfna_red (Red Skorfna, loot table entities/skorfna_red, picked in
    // SkorfnaFish). Both are registered together so they sit side by side in the creative tab.
    private static final Item[] SKORFNA_RED_HOLDER = new Item[1];
    public static final Fish SKORFNA = scorpionfish("skorfna", 0.5F, 0.4F, 6.0, 1, () -> {
        Item black = MimContent.item("skorfna", Item::new, new Item.Properties());
        SKORFNA_RED_HOLDER[0] = MimContent.item("skorfna_red", Item::new, new Item.Properties());
        return black;
    });
    /** The red skorfna's item, dropped by a red skorfna ({@link SkorfnaFish.Variant#RED}); same properties as skorfna. */
    public static final Item SKORFNA_RED = SKORFNA_RED_HOLDER[0];
    // Owner, 2026-11-18: "begin on the mola mola". The ocean sunfish: a tall flat disc about 1.6 blocks long and 2.4
    // tall fin tip to fin tip (a mature fish, life size like the tonn and shark); slow, harmless, basks at the surface
    // (MolaFish). Extremely rare (owner 2026-11-18): weight 1, alone, and MolaFish's spawn rule lets only one try in
    // 400 through; jellyfish meat will be its bait once fishing is overhauled. The body box (1.3 x 1.8) holds the disc
    // without the fins. Drops itself (a proposal, waiting for the owner).
    public static final Fish MOLA_MOLA = mola("mola_mola", 1.3F, 1.8F, 20.0, () -> MimContent.item("mola_mola", Item::new, new Item.Properties()));

    // The Malta world's sea biomes (from the world's datapack, maltamc namespace).
    static final String[] MALTA_SHALLOW = {"bahar_sea", "posidonia_meadows", "qawra_inland_sea", "dwejra_bahar_sea", "dwejra_posidonia_meadows"};
    static final String[] MALTA_DEEP = {"fond_deep_sea", "fond_band_1", "fond_band_2", "fond_band_3", "fond_band_4",
        "fond_band_5", "fond_band_6", "fond_band_7", "fond_band_8"};

    private MimFishes() {
    }

    /** Loads the class (which registers everything above), then adds the spawns and the creative tab entries. */
    public static void init() {
        // Malta's sea. Weights are relative to the other fish in the same biome; the group is min to max.
        spawn(SARDINA, 25, 4, 8, malta(MALTA_SHALLOW));
        spawn(SARDINA, 15, 4, 8, malta(MALTA_DEEP));
        spawn(AWRATA, 15, 2, 4, malta(MALTA_SHALLOW));
        spawn(CERNA, 5, 1, 1, malta("fond_deep_sea", "dwejra_fond_deep_sea", "dwejra_bahar_sea"));
        spawn(MURINA, 4, 1, 1, malta("bahar_sea", "dwejra_bahar_sea", "dwejra_fond_deep_sea"));
        spawn(TONN, 3, 3, 5, malta(MALTA_DEEP));
        // TODO lampuka: only from mid August to December, once the mod has a calendar (the lampuka season)
        spawn(LAMPUKA, 6, 2, 4, malta(concat(MALTA_DEEP, "bahar_sea", "dwejra_fond_deep_sea")));
        spawn(ZIEMEL, 3, 1, 2, malta("posidonia_meadows", "dwejra_posidonia_meadows"));
        spawn(PIXXISPAD, 1, 1, 1, malta(MALTA_DEEP));
        spawn(INCOVA, 15, 4, 8, malta(MALTA_DEEP));
        spawn(INCOVA, 10, 4, 8, malta("bahar_sea", "dwejra_bahar_sea"));
        spawn(CAWL, 20, 3, 6, malta("bahar_sea", "qawra_inland_sea", "dwejra_bahar_sea"));
        spawn(HUTA_KAHLA, 1, 1, 1, malta(MALTA_DEEP));
        // the boll only spawns over a soft floor (sand, gravel, clay, mud; BollFish), at any depth
        spawn(BOLL, 5, 1, 2, malta("bahar_sea", "dwejra_bahar_sea", "qawra_inland_sea"));
        spawn(BOLL, 4, 1, 2, malta("posidonia_meadows", "dwejra_posidonia_meadows"));
        spawn(BOLL, 2, 1, 2, malta(MALTA_DEEP));
        // the skorfna only spawns over a rock floor (SkorfnaFish), at any depth
        spawn(SKORFNA, 4, 1, 1, malta("bahar_sea", "dwejra_bahar_sea"));
        spawn(SKORFNA, 2, 1, 1, malta("fond_deep_sea", "dwejra_fond_deep_sea"));
        // the mola mola: extremely rare, the deep sea only (and MolaFish's spawn rule lets one try in 400 through)
        spawn(MOLA_MOLA, 1, 1, 1, malta(concat(MALTA_DEEP, "dwejra_fond_deep_sea")));
        if (MimConfig.fishInVanillaOceans) {
            ResourceKey<Biome> warm = Biomes.WARM_OCEAN, luke = Biomes.LUKEWARM_OCEAN, deepLuke = Biomes.DEEP_LUKEWARM_OCEAN;
            spawn(SARDINA, 10, 4, 8, List.of(warm, luke, deepLuke));
            spawn(AWRATA, 8, 2, 4, List.of(warm, luke));
            spawn(CERNA, 3, 1, 1, List.of(warm, deepLuke));
            spawn(MURINA, 2, 1, 1, List.of(warm, luke));
            spawn(TONN, 2, 3, 5, List.of(deepLuke));
            spawn(LAMPUKA, 4, 2, 4, List.of(warm, luke, deepLuke));
            spawn(ZIEMEL, 2, 1, 2, List.of(warm, luke));
            spawn(PIXXISPAD, 1, 1, 1, List.of(warm, luke));
            spawn(INCOVA, 8, 4, 8, List.of(warm, luke, deepLuke, Biomes.OCEAN, Biomes.DEEP_OCEAN));
            spawn(CAWL, 8, 3, 6, List.of(warm, luke));
            spawn(HUTA_KAHLA, 1, 1, 1, List.of(luke, deepLuke, Biomes.DEEP_OCEAN));
            spawn(BOLL, 2, 1, 2, List.of(warm, luke));
            spawn(SKORFNA, 2, 1, 1, List.of(warm, luke));
            // vanilla has no deep warm ocean: the warm ocean and the deep lukewarm one
            spawn(MOLA_MOLA, 1, 1, 1, List.of(warm, deepLuke));
        }

        // Besides the mod's own tab: spawn eggs in vanilla's Spawn Eggs tab, buckets beside vanilla's fish buckets.
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.SPAWN_EGGS).register(out -> ALL.forEach(f -> out.accept(f.spawnEgg())));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.TOOLS_AND_UTILITIES).register(out ->
            out.insertAfter(Items.TROPICAL_FISH_BUCKET, ALL.stream().map(Fish::bucket).toArray(Item[]::new)));
    }

    /** How a schooling fish is made: vanilla's entity factory plus the bucket and the school size. */
    private interface SchoolingMaker {
        MimSchoolingFish make(EntityType<? extends MimSchoolingFish> type, net.minecraft.world.level.Level level, Supplier<Item> bucket, int school);
    }

    private static Fish schooling(String id, float width, float height, double health, int school, Supplier<Item> item) {
        return schooling(id, width, height, health, school, MimSchoolingFish::new, item);
    }

    private static Fish schooling(String id, float width, float height, double health, int school, SchoolingMaker maker, Supplier<Item> item) {
        Item[] bucket = new Item[1];
        EntityType<MimSchoolingFish> type = MimContent.entity(id, FabricEntityType.Builder.<MimSchoolingFish>createMob(
                (t, level) -> maker.make(t, level, () -> bucket[0], school), MobCategory.WATER_AMBIENT,
                b -> b.spawnPlacement(SpawnPlacementTypes.IN_WATER, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, WaterAnimal::checkSurfaceWaterAnimalSpawnRules)
                    .defaultAttributes(() -> AbstractFish.createAttributes().add(Attributes.MAX_HEALTH, health)))
            .sized(width, height).eyeHeight(height * 0.65F).clientTrackingRange(4));
        return finish(id, type, bucket, item);
    }

    private static Fish solitary(String id, float width, float height, double health, int cluster, Supplier<Item> item) {
        return solitary(id, width, height, health, cluster, 0.7, item);
    }

    /** speed: the movement speed attribute, which sets how fast it swims (vanilla's fish 0.7). */
    private static Fish solitary(String id, float width, float height, double health, int cluster, double speed, Supplier<Item> item) {
        Item[] bucket = new Item[1];
        SpawnPlacements.SpawnPredicate<MimFish> rule = id.equals("murina") ? MimFishes::nearRock : WaterAnimal::checkSurfaceWaterAnimalSpawnRules;
        EntityType<MimFish> type = MimContent.entity(id, FabricEntityType.Builder.<MimFish>createMob(
                (t, level) -> new MimFish(t, level, () -> bucket[0], cluster), MobCategory.WATER_AMBIENT,
                b -> b.spawnPlacement(SpawnPlacementTypes.IN_WATER, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, rule)
                    .defaultAttributes(() -> AbstractFish.createAttributes().add(Attributes.MAX_HEALTH, health).add(Attributes.MOVEMENT_SPEED, speed)))
            .sized(width, height).eyeHeight(height * 0.65F).clientTrackingRange(4));
        return finish(id, type, bucket, item);
    }

    /** The blue shark: a solitary fish with a bite (attack damage) that is neutral to players (HutaKahlaFish). */
    private static Fish shark(String id, float width, float height, double health, double speed, double damage, Supplier<Item> item) {
        Item[] bucket = new Item[1];
        EntityType<HutaKahlaFish> type = MimContent.entity(id, FabricEntityType.Builder.<HutaKahlaFish>createMob(
                (t, level) -> new HutaKahlaFish(t, level, () -> bucket[0], 1), MobCategory.WATER_AMBIENT,
                b -> b.spawnPlacement(SpawnPlacementTypes.IN_WATER, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, WaterAnimal::checkSurfaceWaterAnimalSpawnRules)
                    .defaultAttributes(() -> AbstractFish.createAttributes().add(Attributes.MAX_HEALTH, health)
                        .add(Attributes.MOVEMENT_SPEED, speed).add(Attributes.ATTACK_DAMAGE, damage)))
            .sized(width, height).eyeHeight(height * 0.65F).clientTrackingRange(4));
        return finish(id, type, bucket, item);
    }

    /** The stingray: a solitary fish of its own kind (BollFish) with its own spawn rule, over a soft sea floor. */
    private static Fish ray(String id, float width, float height, double health, int cluster, Supplier<Item> item) {
        Item[] bucket = new Item[1];
        EntityType<BollFish> type = MimContent.entity(id, FabricEntityType.Builder.<BollFish>createMob(
                (t, level) -> new BollFish(t, level, () -> bucket[0], cluster), MobCategory.WATER_AMBIENT,
                b -> b.spawnPlacement(SpawnPlacementTypes.IN_WATER, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, BollFish::checkBollSpawnRules)
                    .defaultAttributes(() -> AbstractFish.createAttributes().add(Attributes.MAX_HEALTH, health)))
            .sized(width, height).eyeHeight(height * 0.65F).clientTrackingRange(4));
        return finish(id, type, bucket, item);
    }

    /** The scorpionfish: a solitary fish of its own kind (SkorfnaFish) with its own spawn rule, over a rock floor. */
    private static Fish scorpionfish(String id, float width, float height, double health, int cluster, Supplier<Item> item) {
        Item[] bucket = new Item[1];
        EntityType<SkorfnaFish> type = MimContent.entity(id, FabricEntityType.Builder.<SkorfnaFish>createMob(
                (t, level) -> new SkorfnaFish(t, level, () -> bucket[0], cluster), MobCategory.WATER_AMBIENT,
                b -> b.spawnPlacement(SpawnPlacementTypes.IN_WATER, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, SkorfnaFish::checkSkorfnaSpawnRules)
                    .defaultAttributes(() -> AbstractFish.createAttributes().add(Attributes.MAX_HEALTH, health)))
            .sized(width, height).eyeHeight(height * 0.65F).clientTrackingRange(4));
        return finish(id, type, bucket, item);
    }

    /** The ocean sunfish: a slow solitary fish of its own kind (MolaFish) with its own, extremely rare, spawn rule. */
    private static Fish mola(String id, float width, float height, double health, Supplier<Item> item) {
        Item[] bucket = new Item[1];
        EntityType<MolaFish> type = MimContent.entity(id, FabricEntityType.Builder.<MolaFish>createMob(
                (t, level) -> new MolaFish(t, level, () -> bucket[0], 1), MobCategory.WATER_AMBIENT,
                b -> b.spawnPlacement(SpawnPlacementTypes.IN_WATER, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, MolaFish::checkMolaSpawnRules)
                    .defaultAttributes(() -> AbstractFish.createAttributes().add(Attributes.MAX_HEALTH, health)
                        .add(Attributes.MOVEMENT_SPEED, MolaFish.SPEED)))
            .sized(width, height).eyeHeight(height * 0.5F).clientTrackingRange(6));
        return finish(id, type, bucket, item);
    }

    private static Fish finish(String id, EntityType<? extends AbstractFish> type, Item[] bucket, Supplier<Item> item) {
        Item drop = item.get();
        bucket[0] = MimContent.item(id + "_bucket", p -> new MobBucketItem(type, Fluids.WATER, SoundEvents.BUCKET_EMPTY_FISH, p),
            new Item.Properties().stacksTo(1).component(DataComponents.BUCKET_ENTITY_DATA, CustomData.EMPTY));
        Item egg = MimContent.item(id + "_spawn_egg", SpawnEggItem::new, new Item.Properties().spawnEgg(type));
        Fish fish = new Fish(id, type, drop, bucket[0], egg);
        ALL.add(fish);
        return fish;
    }

    /** The moray: vanilla's fish rule, and only with rock (any solid block) within two blocks, as it lives in holes. */
    private static boolean nearRock(EntityType<MimFish> type, ServerLevelAccessor level, EntitySpawnReason reason, BlockPos pos, RandomSource random) {
        if (!WaterAnimal.checkSurfaceWaterAnimalSpawnRules(type, level, reason, pos, random)) {
            return false;
        }
        for (BlockPos p : BlockPos.betweenClosed(pos.offset(-2, -2, -2), pos.offset(2, 2, 2))) {
            BlockState state = level.getBlockState(p);
            if (!state.isAir() && state.getFluidState().isEmpty() && state.isSolid()) {
                return true;
            }
        }
        return false;
    }

    private static void spawn(Fish fish, int weight, int min, int max, List<ResourceKey<Biome>> biomes) {
        BiomeModifications.addSpawn(BiomeSelectors.includeByKey(biomes), MobCategory.WATER_AMBIENT, fish.type(), weight, min, max);
    }

    static List<ResourceKey<Biome>> malta(String... names) {
        List<ResourceKey<Biome>> keys = new ArrayList<>();
        for (String name : names) {
            keys.add(ResourceKey.create(Registries.BIOME, Identifier.fromNamespaceAndPath("maltamc", name)));
        }
        return keys;
    }

    private static String[] concat(String[] a, String... b) {
        String[] out = java.util.Arrays.copyOf(a, a.length + b.length);
        System.arraycopy(b, 0, out, a.length, b.length);
        return out;
    }
}
