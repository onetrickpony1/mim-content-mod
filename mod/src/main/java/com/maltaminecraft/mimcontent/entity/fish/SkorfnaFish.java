package com.maltaminecraft.mimcontent.entity.fish;

import java.util.EnumSet;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.level.storage.loot.LootTable;
import org.jspecify.annotations.Nullable;

/**
 * The skorfna (black scorpionfish, Scorpaena porcus; decision 2026-11-18 "Skorfna - start"), an ambush hunter that
 * sits camouflaged on rocky bottoms and in caves and barely swims:
 * <ul>
 * <li>It rests on the bottom most of the time ({@link #REST_MIN} to {@link #REST_MAX} ticks at a go) and now and then
 *     moves on in a short hop of up to {@link #HOP_RANGE} blocks, staying on the floor.</li>
 * <li>It trusts its camouflage: it doesn't shy away from players like the other fish. Hurt it and it darts a short
 *     way (up to {@link #DART_RANGE} blocks), once, then settles again.</li>
 * <li>Its spines are venomous. A survival or adventure player or a mob (not another fish) that touches it (bumps into
 *     it, walks onto it) or hits it in melee is stung: {@link #STING_DAMAGE} damage and Poison for
 *     {@link #POISON_SECONDS} seconds, at most once every {@link #STING_COOLDOWN} ticks. Creative and spectator
 *     players, and peaceful difficulty, are never stung ({@link Venom}, shared with the boll).</li>
 * </ul>
 * It spawns only over a rock floor (any solid block that isn't sand, gravel, clay or mud) that lies within
 * {@link #SPAWN_FLOOR_DEPTH} blocks under the spawn point, at any depth below sea level, and is moved down onto that
 * floor when it spawns naturally (like the boll, whose floor is soft instead).
 * <p>
 * It comes in two versions on one model (owner 2026-11-18, "Skorfna - two versions, red and black, as reskins"), only
 * the texture differs, like vanilla's tropical fish patterns: {@link Variant#BLACK} (the black scorpionfish, Scorpaena
 * porcus, the default) and {@link Variant#RED} (the red scorpionfish, Scorpaena scrofa, Ċippullazza), which lives
 * deeper. A new skorfna (natural spawn, spawn egg, /summon without data) picks one ({@link #pickVariant}). The variant
 * is synced to clients, saved with the fish ({@code Variant}: "black" or "red") and kept in the bucket; a skorfna saved
 * before variants existed is black. Each version drops its own item (owner 2026-11-18, "Skorfna icon D accepted; each
 * colour drops its own item"): the black one by the entity's loot table (entities/skorfna, the skorfna item), the red
 * one by entities/skorfna_red (the skorfna_red item); see {@link #dropFromLootTable}.
 */
public class SkorfnaFish extends MimFish {
    /** The sting: damage (1 heart) and how long the poison lasts. */
    public static final float STING_DAMAGE = 2.0F;
    public static final int POISON_SECONDS = 6;
    /** Ticks between two stings (2 seconds). */
    public static final int STING_COOLDOWN = 40;
    /** How close counts as touching it, in blocks beyond its body box. */
    public static final double TOUCH_MARGIN = 0.1;
    /** How long it rests on the bottom between hops, in ticks (10 to 30 seconds). */
    public static final int REST_MIN = 200, REST_MAX = 600;
    /** How far one hop goes, in blocks, and the swim speed of a hop (times its movement speed). */
    public static final int HOP_RANGE = 3;
    public static final double HOP_SPEED = 1.0;
    /** How far it darts when hurt, in blocks, and how fast. */
    public static final int DART_RANGE = 4;
    public static final double DART_SPEED = 1.8;
    /** How long a hop or dart may take before it gives up, in ticks. */
    public static final int MOVE_TICKS = 40;
    /** How deep under a spawn point the rock floor may lie, in blocks. */
    public static final int SPAWN_FLOOR_DEPTH = 16;

    /** The two versions: same model, shape, behaviour and sting; only the texture and the dropped item differ. */
    public enum Variant {
        BLACK("black"), RED("red");

        private final String id;

        Variant(String id) {
            this.id = id;
        }

        /** As saved ({@code Variant}) and in the lang key {@code entity.mimcontent.skorfna.variant.<id>}. */
        public String id() {
            return id;
        }

        public String translationKey() {
            return "entity.mimcontent.skorfna.variant." + id;
        }

        /** The variant saved as this id; anything else (or nothing) is black. */
        public static Variant byId(String id) {
            return RED.id.equals(id) ? RED : BLACK;
        }
    }

    /** The saved key, in the world and in the bucket. */
    public static final String VARIANT_KEY = "Variant";
    /** How often a new skorfna is red: in the deep-sea biomes, where the red one lives, and everywhere else. */
    public static final float RED_CHANCE_DEEP = 0.65F, RED_CHANCE_ELSEWHERE = 0.30F;
    /** The Malta world's deep-sea biomes, where a skorfna is more often red. */
    private static final List<ResourceKey<Biome>> DEEP_BIOMES = List.of(
        ResourceKey.create(Registries.BIOME, Identifier.fromNamespaceAndPath("maltamc", "fond_deep_sea")),
        ResourceKey.create(Registries.BIOME, Identifier.fromNamespaceAndPath("maltamc", "dwejra_fond_deep_sea")));
    /** The red skorfna's loot table (drops skorfna_red); the black one uses the entity's own, entities/skorfna. */
    public static final ResourceKey<LootTable> RED_LOOT = ResourceKey.create(Registries.LOOT_TABLE,
        Identifier.fromNamespaceAndPath("mimcontent", "entities/skorfna_red"));
    private static final EntityDataAccessor<Integer> DATA_VARIANT = SynchedEntityData.defineId(SkorfnaFish.class, EntityDataSerializers.INT);

    /** True while it lies still on the bottom (server side). */
    private boolean resting;
    /** Set when it is hurt: it darts once. */
    private boolean dartPending;
    private long nextSting;

    public SkorfnaFish(EntityType<? extends MimFish> type, Level level, Supplier<Item> bucket, int spawnCluster) {
        super(type, level, bucket, spawnCluster);
    }

    public boolean isResting() {
        return resting;
    }

    // ---- the two versions ----

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(DATA_VARIANT, Variant.BLACK.ordinal());
    }

    public Variant getVariant() {
        int i = entityData.get(DATA_VARIANT);
        return i >= 0 && i < Variant.values().length ? Variant.values()[i] : Variant.BLACK;
    }

    public void setVariant(Variant variant) {
        entityData.set(DATA_VARIANT, variant.ordinal());
    }

    /** A new skorfna's variant: red {@link #RED_CHANCE_DEEP} of the time in the deep-sea biomes, else {@link #RED_CHANCE_ELSEWHERE}. */
    public static Variant pickVariant(RandomSource random, boolean deep) {
        return random.nextFloat() < (deep ? RED_CHANCE_DEEP : RED_CHANCE_ELSEWHERE) ? Variant.RED : Variant.BLACK;
    }

    /** True in the Malta world's deep-sea biomes (fond_deep_sea, dwejra_fond_deep_sea). */
    public static boolean isDeepBiome(ServerLevelAccessor level, BlockPos pos) {
        var biome = level.getBiome(pos);
        return DEEP_BIOMES.stream().anyMatch(biome::is);
    }

    /**
     * The death drop by version: a red skorfna rolls {@link #RED_LOOT} instead of the entity's table. Only the table
     * changes; the kill goes through vanilla's loot code as for every other fish (same context: killer, weapon and its
     * Looting, on fire), so whatever the table says about those applies. A skorfna given its own DeathLootTable (by
     * /summon or a datapack) keeps it.
     */
    @Override
    protected void dropFromLootTable(ServerLevel level, DamageSource source, boolean playerKilled) {
        if (getVariant() == Variant.RED && getLootTable().equals(getType().getDefaultLootTable())) {
            dropFromLootTable(level, source, playerKilled, RED_LOOT);
        } else {
            super.dropFromLootTable(level, source, playerKilled);
        }
    }

    @Override
    protected void addAdditionalSaveData(ValueOutput output) {
        super.addAdditionalSaveData(output);
        output.putString(VARIANT_KEY, getVariant().id());
    }

    @Override
    protected void readAdditionalSaveData(ValueInput input) {
        super.readAdditionalSaveData(input);
        // a skorfna saved before variants existed is black
        setVariant(Variant.byId(input.getStringOr(VARIANT_KEY, Variant.BLACK.id())));
    }

    @Override
    public void saveToBucketTag(ItemStack bucket) {
        super.saveToBucketTag(bucket);
        CustomData.update(DataComponents.BUCKET_ENTITY_DATA, bucket, tag -> tag.putString(VARIANT_KEY, getVariant().id()));
    }

    @Override
    public void loadFromBucketTag(CompoundTag tag) {
        super.loadFromBucketTag(tag);
        // a bucket filled before variants existed holds a black one
        setVariant(Variant.byId(tag.getStringOr(VARIANT_KEY, Variant.BLACK.id())));
    }

    @Override
    protected void registerGoals() {
        // no vanilla panic and no shying from players: one short dart when hurt, short hops, and rest
        this.goalSelector.addGoal(0, new MoveOnGoal(true));
        this.goalSelector.addGoal(2, new MoveOnGoal(false));
        this.goalSelector.addGoal(3, new RestGoal());
    }

    // ---- living on a rock floor ----

    /** True for a rock floor: any solid block that isn't a soft bottom (sand, gravel, clay, mud). */
    public static boolean isRockFloor(BlockState state) {
        return state.getFluidState().isEmpty() && state.isSolid() && !BollFish.isSoftFloor(state);
    }

    /** The rock floor under a water position, within SPAWN_FLOOR_DEPTH blocks, or null (soft, or too deep). */
    public static @Nullable BlockPos rockFloorBelow(BlockGetter level, BlockPos pos) {
        BlockPos.MutableBlockPos p = pos.mutable();
        for (int i = 0; i <= SPAWN_FLOOR_DEPTH; i++) {
            BlockState state = level.getBlockState(p);
            if (!state.getFluidState().is(FluidTags.WATER)) {
                return isRockFloor(state) ? p.immutable() : null;
            }
            p.move(0, -1, 0);
        }
        return null;
    }

    /**
     * The spawn rule: in open water (water below and above, as vanilla's fish), anywhere below sea level, over a rock
     * floor within SPAWN_FLOOR_DEPTH blocks. Spawners and eggs aren't held to the floor.
     */
    public static boolean checkSkorfnaSpawnRules(EntityType<? extends MimFish> type, ServerLevelAccessor level, EntitySpawnReason reason,
                                                 BlockPos pos, RandomSource random) {
        if (!level.getFluidState(pos).is(FluidTags.WATER) || !level.getBlockState(pos.above()).is(Blocks.WATER)) {
            return false;
        }
        if (reason == EntitySpawnReason.SPAWNER || reason == EntitySpawnReason.TRIAL_SPAWNER) {
            return true;
        }
        return pos.getY() < level.getSeaLevel() && rockFloorBelow(level, pos) != null;
    }

    @Override
    public @Nullable SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, EntitySpawnReason reason,
                                                  @Nullable SpawnGroupData group) {
        if (reason == EntitySpawnReason.NATURAL || reason == EntitySpawnReason.CHUNK_GENERATION) {
            // spawned somewhere in the water column: down onto the rock, where it lives
            BlockPos floor = rockFloorBelow(level, blockPosition());
            if (floor != null) {
                snapTo(getX(), floor.getY() + 1.0, getZ(), getYRot(), 0.0F);
            }
        }
        if (reason != EntitySpawnReason.BUCKET) {
            // a new fish picks its version (one let out of a bucket gets the bucket's, loadFromBucketTag)
            setVariant(pickVariant(getRandom(), isDeepBiome(level, blockPosition())));
        }
        return super.finalizeSpawn(level, difficulty, reason, group);
    }

    // ---- the spines ----

    @Override
    public void tick() {
        super.tick();
        if (level() instanceof ServerLevel level && isAlive() && level.getGameTime() >= nextSting) {
            // anyone touching it: bumping into it, standing or walking on it (other fish swim by unharmed)
            AABB box = getBoundingBox().inflate(TOUCH_MARGIN);
            List<LivingEntity> touching = level.getEntitiesOfClass(LivingEntity.class, box,
                e -> e != this && !(e instanceof AbstractFish) && Venom.canSting(e));
            if (!touching.isEmpty()) {
                sting(level, touching.getFirst());
            }
        }
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float amount) {
        boolean hurt = super.hurtServer(level, source, amount);
        if (hurt && isAlive()) {
            dartPending = true;
            resting = false;
            // a melee hit (not an arrow or a thrown trident) meets the spines
            if (source.getEntity() instanceof LivingEntity attacker && source.getDirectEntity() == attacker
                && !source.is(DamageTypeTags.IS_PROJECTILE)) {
                sting(level, attacker);
            }
        }
        return hurt;
    }

    /** Stings: damage and poison, if the cooldown allows and the target can be stung. Returns true if it stung. */
    public boolean sting(ServerLevel level, LivingEntity target) {
        long now = level.getGameTime();
        if (now < nextSting || !Venom.canSting(target)) {
            return false;
        }
        nextSting = now + STING_COOLDOWN;
        Venom.strike(level, this, target, STING_DAMAGE, POISON_SECONDS);
        return true;
    }

    // ---- goals ----

    /** A spot on the floor near it, 1 to range blocks away, just above the floor; or null. */
    private @Nullable Vec3 floorSpotNear(int range) {
        for (int tries = 0; tries < 8; tries++) {
            double angle = getRandom().nextDouble() * Math.PI * 2.0;
            double dist = 1.0 + getRandom().nextDouble() * (range - 1.0);
            Vec3 spot = new Vec3(getX() + Math.cos(angle) * dist, getY() + 0.5, getZ() + Math.sin(angle) * dist);
            if (!level().getFluidState(BlockPos.containing(spot)).is(FluidTags.WATER)) {
                continue;
            }
            double above = BollFish.heightAboveFloor(level(), spot, 4);
            if (above <= 4) {
                return new Vec3(spot.x, spot.y - above + 0.1, spot.z);
            }
        }
        return null;
    }

    /** A short move along the floor: a hop now and then, or (dart) one quick dart after it is hurt. */
    private class MoveOnGoal extends Goal {
        private final boolean dart;
        private @Nullable Vec3 target;
        private int ticks;

        MoveOnGoal(boolean dart) {
            this.dart = dart;
            setFlags(EnumSet.of(Goal.Flag.MOVE));
        }

        @Override
        public boolean canUse() {
            if (!isInWater() || (dart ? !dartPending : getRandom().nextInt(reducedTickDelay((REST_MIN + REST_MAX) / 2)) != 0)) {
                return false;
            }
            target = floorSpotNear(dart ? DART_RANGE : HOP_RANGE);
            if (dart) {
                dartPending = false;
            }
            return target != null;
        }

        @Override
        public void start() {
            ticks = MOVE_TICKS;
            resting = false;
            getNavigation().moveTo(target.x, target.y, target.z, dart ? DART_SPEED : HOP_SPEED);
        }

        @Override
        public boolean canContinueToUse() {
            return ticks > 0 && isInWater() && !getNavigation().isDone();
        }

        @Override
        public void tick() {
            ticks--;
        }

        @Override
        public void stop() {
            getNavigation().stop();
        }
    }

    /** Lies still on the bottom: it settles onto the floor and stays put, for REST_MIN to REST_MAX ticks. */
    private class RestGoal extends Goal {
        private int ticks;

        RestGoal() {
            setFlags(EnumSet.of(Goal.Flag.MOVE, Goal.Flag.JUMP));
        }

        @Override
        public boolean canUse() {
            return isInWater();
        }

        @Override
        public void start() {
            ticks = REST_MIN + getRandom().nextInt(REST_MAX - REST_MIN + 1);
            resting = true;
            getNavigation().stop();
        }

        @Override
        public boolean canContinueToUse() {
            return resting && ticks > 0 && isInWater();
        }

        @Override
        public void tick() {
            ticks--;
            Vec3 v = getDeltaMovement();
            setDeltaMovement(v.x * 0.5, Math.min(v.y, 0.0) - 0.01, v.z * 0.5);
        }

        @Override
        public boolean requiresUpdateEveryTick() {
            return true;
        }

        @Override
        public void stop() {
            resting = false;
        }
    }
}
