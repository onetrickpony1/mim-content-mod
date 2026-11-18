package com.maltaminecraft.mimcontent;

import com.maltaminecraft.mimcontent.entity.jelly.Jellyfish;
import com.maltaminecraft.mimcontent.entity.jelly.JellyfishWardEffect;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.biome.v1.BiomeModifications;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectors;
import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.fabricmc.fabric.api.object.builder.v1.entity.FabricEntityType;
import net.fabricmc.fabric.api.resource.conditions.v1.ResourceCondition;
import net.fabricmc.fabric.api.resource.conditions.v1.ResourceConditionType;
import net.fabricmc.fabric.api.resource.conditions.v1.ResourceConditions;
import net.minecraft.core.Holder;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.RegistryOps;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.fish.WaterAnimal;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.SpawnEggItem;
import net.minecraft.world.item.alchemy.Potion;
import net.minecraft.world.item.component.Consumables;
import net.minecraft.world.item.consume_effects.ApplyStatusEffectsConsumeEffect;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.levelgen.Heightmap;

/**
 * The jellyfish (owner, 2026-11-18: "get makers started on all 3 jellyfish types"): the mauve stinger, the fried-egg
 * jellyfish and the Portuguese man o' war ({@link Jellyfish}), each with a spawn egg and no bucket; their drops, venom
 * and meat (owner, 2026-11-18, "Jellyfish drops - venom and meat"); the Jellyfish Ward effect and its potion.
 * They spawn in the Malta world's seas and (switch {@code fish_in_vanilla_oceans}) vanilla's warm and lukewarm ones.
 * The venom brews (Poison, Jellyfish Ward) are data recipes behind the switch {@code jellyfish_venom_recipes}.
 */
public final class MimJellyfish {
    /** One jellyfish: its mob and its spawn egg. */
    public record Jelly(Jellyfish.Kind kind, EntityType<Jellyfish> type, Item spawnEgg) {
        public String id() {
            return kind.id();
        }
    }

    public static final List<Jelly> ALL = new ArrayList<>();

    // Box width and height in blocks: the size of the model (the smoke test measures the baked models), health.
    /** Bell 8 px (0.5 blocks) wide; with its tentacles and oral arms 21 px (1.31 blocks) from the bell's top down. */
    public static final Jelly MAUVE_STINGER = jelly(Jellyfish.Kind.MAUVE_STINGER, 0.5F, 1.3125F, 4.0);
    /** Bell 15 px (0.94 blocks) wide, flat; with the knobbed oral arms under it 13 px (0.81 blocks) tall. */
    public static final Jelly FRIED_EGG = jelly(Jellyfish.Kind.FRIED_EGG, 0.9375F, 0.8125F, 6.0);
    /** The float, 10 px (0.63 blocks) long and 9 px (0.56) tall with its crest, from the waterline up; the polyps and
     *  tentacles below are not hit, but they sting (the column under it, Jellyfish.MAN_O_WAR_TENTACLE_LENGTH). */
    public static final Jelly MAN_O_WAR = jelly(Jellyfish.Kind.MAN_O_WAR, 0.625F, 0.5625F, 6.0);

    // ---- the drops ----
    /** An ingredient: brews Poison (awkward potion + venom) and Jellyfish Ward (thick potion + venom). */
    public static final Item VENOM = MimContent.item("jellyfish_venom", Item::new, new Item.Properties());
    /** Jellyfish meat: poor food, 2 hunger, low saturation; a 15% chance of Poison for 4 seconds. Can't be cooked. */
    public static final int MEAT_NUTRITION = 2;
    public static final float MEAT_SATURATION = 0.1F;
    public static final float MEAT_POISON_CHANCE = 0.15F;
    public static final int MEAT_POISON_SECONDS = 4;
    public static final Item MEAT = MimContent.item("jellyfish_meat", Item::new, new Item.Properties().food(
        new FoodProperties.Builder().nutrition(MEAT_NUTRITION).saturationModifier(MEAT_SATURATION).build(),
        Consumables.defaultFood().onConsume(new ApplyStatusEffectsConsumeEffect(
            new MobEffectInstance(MobEffects.POISON, MEAT_POISON_SECONDS * 20, 0), MEAT_POISON_CHANCE)).build()));

    // ---- Jellyfish Ward ----
    /** While active, no jellyfish can sting: no damage, poison or nausea (Jellyfish checks it). */
    public static final Holder<MobEffect> WARD = Registry.registerForHolder(BuiltInRegistries.MOB_EFFECT, MimContent.id("jellyfish_ward"),
        new JellyfishWardEffect());
    /** The potion: 3 minutes, or 8 with redstone. */
    public static final int WARD_SECONDS = 180;
    public static final int LONG_WARD_SECONDS = 480;
    public static final Holder<Potion> WARD_POTION = Registry.registerForHolder(BuiltInRegistries.POTION, MimContent.id("jellyfish_ward"),
        new Potion("jellyfish_ward", new MobEffectInstance(WARD, WARD_SECONDS * 20)));
    public static final Holder<Potion> LONG_WARD_POTION = Registry.registerForHolder(BuiltInRegistries.POTION, MimContent.id("long_jellyfish_ward"),
        new Potion("jellyfish_ward", new MobEffectInstance(WARD, LONG_WARD_SECONDS * 20)));

    /**
     * A load condition for data files: {@code {"condition": "mimcontent:config", "switch": "jellyfish_venom_recipes"}}
     * loads the file only while that switch is on.
     */
    public record ConfigCondition(String name) implements ResourceCondition {
        public static final MapCodec<ConfigCondition> CODEC = Codec.STRING.fieldOf("switch").xmap(ConfigCondition::new, ConfigCondition::name);
        public static final ResourceConditionType<ConfigCondition> TYPE = ResourceConditionType.create(MimContent.id("config"), CODEC);

        @Override
        public ResourceConditionType<?> getType() {
            return TYPE;
        }

        @Override
        public boolean test(RegistryOps.RegistryInfoLookup registryInfo) {
            return switch (name) {
                case "jellyfish_venom_recipes" -> MimConfig.jellyfishVenomRecipes;
                case "fish_in_vanilla_oceans" -> MimConfig.fishInVanillaOceans;
                default -> false;
            };
        }
    }

    private MimJellyfish() {
    }

    /** Loads the class (which registers everything above), then adds the spawns, the load condition and the tab entries. */
    public static void init() {
        ResourceConditions.register(ConfigCondition.TYPE);
        // Malta's sea: uncommon (the sardina is 25, the awrata 15); the man o' war rare, only in the deep sea.
        spawn(MAUVE_STINGER, 4, 2, 4, MimFishes.malta(MimFishes.MALTA_SHALLOW));
        spawn(MAUVE_STINGER, 4, 2, 4, MimFishes.malta(MimFishes.MALTA_DEEP));
        spawn(FRIED_EGG, 3, 1, 2, MimFishes.malta(MimFishes.MALTA_SHALLOW));
        spawn(FRIED_EGG, 2, 1, 2, MimFishes.malta(MimFishes.MALTA_DEEP));
        spawn(MAN_O_WAR, 1, 1, 1, MimFishes.malta(MimFishes.MALTA_DEEP));
        // TODO seasons (winter and spring mauve stingers, spring man o' war, late-summer fried-eggs) once the calendar exists
        if (MimConfig.fishInVanillaOceans) {
            spawn(MAUVE_STINGER, 3, 2, 4, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN, Biomes.DEEP_LUKEWARM_OCEAN));
            spawn(FRIED_EGG, 2, 1, 2, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN));
            spawn(MAN_O_WAR, 1, 1, 1, List.of(Biomes.DEEP_LUKEWARM_OCEAN));
        }
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.SPAWN_EGGS).register(out -> ALL.forEach(j -> out.accept(j.spawnEgg())));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.INGREDIENTS).register(out -> out.insertAfter(Items.SPIDER_EYE, VENOM));
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FOOD_AND_DRINKS).register(out -> out.insertAfter(Items.ROTTEN_FLESH, MEAT));
    }

    private static Jelly jelly(Jellyfish.Kind kind, float width, float height, double health) {
        EntityType<Jellyfish> type = MimContent.entity(kind.id(), FabricEntityType.Builder.<Jellyfish>createMob(
                (t, level) -> new Jellyfish(t, level, kind), MobCategory.WATER_AMBIENT,
                b -> b.spawnPlacement(SpawnPlacementTypes.IN_WATER, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, WaterAnimal::checkSurfaceWaterAnimalSpawnRules)
                    .defaultAttributes(() -> Mob.createMobAttributes().add(Attributes.MAX_HEALTH, health)))
            .sized(width, height).eyeHeight(height * 0.6F).clientTrackingRange(kind.floats() ? 8 : 4));
        Item egg = MimContent.item(kind.id() + "_spawn_egg", SpawnEggItem::new, new Item.Properties().spawnEgg(type));
        Jelly jelly = new Jelly(kind, type, egg);
        ALL.add(jelly);
        return jelly;
    }

    private static void spawn(Jelly jelly, int weight, int min, int max, List<ResourceKey<Biome>> biomes) {
        BiomeModifications.addSpawn(BiomeSelectors.includeByKey(biomes), MobCategory.WATER_AMBIENT, jelly.type(), weight, min, max);
    }
}
