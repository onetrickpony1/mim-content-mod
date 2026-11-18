package com.maltaminecraft.mimcontent.entity.fish;

import java.util.EnumSet;
import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.PanicGoal;
import net.minecraft.world.entity.ai.goal.RandomSwimmingGoal;
import net.minecraft.world.entity.animal.fish.WaterAnimal;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.phys.Vec3;

/**
 * The mola mola (ocean sunfish, Mola mola; decision 2026-11-18 "Mola mola - start"), the heaviest bony fish: a tall
 * flat disc with no tail, which swims slowly by sculling its tall dorsal and anal fins from side to side together.
 * <ul>
 * <li><b>Extremely rare</b> (owner 2026-11-18: "the mola mola must be EXTREMELY rare, with fishing it with the required
 *     bait being practically the only way to find it unless you are super lucky"): besides the lowest spawn weight,
 *     only one natural spawn try in {@link #SPAWN_CHANCE} that picks it goes ahead ({@link #checkMolaSpawnRules}).
 *     Spawn eggs, buckets, spawners and /summon always work.</li>
 * <li>Passive, slow ({@link #SPEED}) and harmless. It doesn't shy away from players (real sunfish are known for
 *     letting divers come close); hurt, it swims off, slowly.</li>
 * <li><b>Basking:</b> now and then it rises to the surface and lies there on its side for 10 to 30 seconds, as the
 *     real fish does after deep dives. While basking it is drawn and hit on its side (like a fish on land, centred on
 *     its position) and its body box is flat, so it doesn't stand out of the water. Hurting it ends the basking.</li>
 * </ul>
 */
public class MolaFish extends MimFish {
    /** One natural spawn try in this many that picks the mola goes ahead (the spawn weight is already the lowest, 1). */
    public static final int SPAWN_CHANCE = 400;
    /** Its swimming speed (the movement speed attribute; vanilla's fish 0.7). */
    public static final double SPEED = 0.35;
    /** How long it basks, in ticks (10 to 30 seconds). */
    public static final int BASK_MIN = 200, BASK_MAX = 600;
    /** Basking, its body box lies flat: as wide as the fish lying on its side, as thin as the fish (blocks). */
    public static final float BASK_WIDTH = 1.7F, BASK_HEIGHT = 0.5F;
    /** Basking, its position sits this far under the water's surface, so its upper side just breaks the surface. */
    public static final double BASK_DEPTH = 0.42;
    /** How far below the surface it can be and still go up to bask (blocks). */
    public static final int BASK_REACH = 16;

    /** How many times it has set off for the surface to bask (server side; read by the in-game test). */
    public int baskTrips;

    private static final EntityDataAccessor<Boolean> DATA_BASKING = SynchedEntityData.defineId(MolaFish.class, EntityDataSerializers.BOOLEAN);

    public MolaFish(EntityType<? extends MimFish> type, Level level, Supplier<Item> bucket, int spawnCluster) {
        super(type, level, bucket, spawnCluster);
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(DATA_BASKING, false);
    }

    /** True while it lies on its side at the surface (synced to clients, which draw it so). */
    public boolean isBasking() {
        return entityData.get(DATA_BASKING);
    }

    public void setBasking(boolean basking) {
        entityData.set(DATA_BASKING, basking);
    }

    @Override
    public void onSyncedDataUpdated(EntityDataAccessor<?> accessor) {
        super.onSyncedDataUpdated(accessor);
        if (DATA_BASKING.equals(accessor)) {
            refreshDimensions();
        }
    }

    @Override
    protected EntityDimensions getDefaultDimensions(Pose pose) {
        if (isBasking()) {
            return EntityDimensions.scalable(BASK_WIDTH, BASK_HEIGHT).withEyeHeight(BASK_HEIGHT * 0.5F);
        }
        return super.getDefaultDimensions(pose);
    }

    @Override
    protected void registerGoals() {
        // no shying from players (AbstractFish's AvoidEntityGoal is left out); a slow panic when hurt
        this.goalSelector.addGoal(0, new PanicGoal(this, 1.2));
        this.goalSelector.addGoal(3, new BaskGoal());
        this.goalSelector.addGoal(4, new RandomSwimmingGoal(this, 0.8, 80) {
            @Override
            public boolean canUse() {
                return !isBasking() && super.canUse();
            }
        });
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float amount) {
        boolean hurt = super.hurtServer(level, source, amount);
        if (hurt) {
            setBasking(false);
        }
        return hurt;
    }

    /**
     * The spawn rule: vanilla's fish rule (water, within 13 blocks of sea level), and for a natural spawn only one try
     * in {@link #SPAWN_CHANCE}. Spawners and trial spawners aren't held back.
     */
    public static boolean checkMolaSpawnRules(EntityType<? extends MimFish> type, ServerLevelAccessor level, EntitySpawnReason reason,
                                              BlockPos pos, RandomSource random) {
        if (!WaterAnimal.checkSurfaceWaterAnimalSpawnRules(type, level, reason, pos, random)) {
            return false;
        }
        return rareRoll(reason, random);
    }

    /** The extra roll: a natural spawn (or one at chunk generation) goes ahead one time in SPAWN_CHANCE; others always. */
    public static boolean rareRoll(EntitySpawnReason reason, RandomSource random) {
        if (reason == EntitySpawnReason.NATURAL || reason == EntitySpawnReason.CHUNK_GENERATION) {
            return random.nextInt(SPAWN_CHANCE) == 0;
        }
        return true;
    }

    /** The height of the water's surface above a point (the top of the highest water block in the column), or NaN. */
    public static double surfaceAbove(BlockGetter level, Vec3 at, int max) {
        BlockPos.MutableBlockPos p = BlockPos.containing(at).mutable();
        if (!level.getFluidState(p).is(FluidTags.WATER)) {
            return Double.NaN;
        }
        for (int i = 0; i <= max; i++) {
            p.move(0, 1, 0);
            if (!level.getFluidState(p).is(FluidTags.WATER)) {
                if (!level.getBlockState(p).isAir()) {
                    // under a ceiling (ice, a block, a boat's hull is an entity so it doesn't count): nowhere to bask
                    return Double.NaN;
                }
                BlockPos top = p.below();
                return top.getY() + level.getFluidState(top).getHeight(level, top);
            }
        }
        return Double.NaN;
    }

    /** Now and then it rises to the surface, lies on its side there for a while, then swims on. */
    private class BaskGoal extends Goal {
        private int ticks;
        /** How long it may take to rise to the surface before it gives up (30 seconds). */
        private int rising;
        private double surface;

        BaskGoal() {
            setFlags(EnumSet.of(Goal.Flag.MOVE, Goal.Flag.JUMP));
        }

        @Override
        public boolean canUse() {
            if (!isInWater() || getLastHurtByMob() != null || getRandom().nextInt(reducedTickDelay(400)) != 0) {
                return false;
            }
            surface = surfaceAbove(level(), position(), BASK_REACH);
            return !Double.isNaN(surface);
        }

        @Override
        public void start() {
            ticks = BASK_MIN + getRandom().nextInt(BASK_MAX - BASK_MIN + 1);
            rising = 600;
            baskTrips++;
            getNavigation().stop();
        }

        @Override
        public boolean canContinueToUse() {
            return ticks > 0 && rising > 0 && isInWater() && getLastHurtByMob() == null;
        }

        @Override
        public void tick() {
            double want = surface - BASK_DEPTH;
            double dy = want - getY();
            Vec3 v = getDeltaMovement();
            if (!isBasking()) {
                // rising: straight up, slowly, then it turns onto its side once there
                setDeltaMovement(v.x * 0.8, Math.max(-0.04, Math.min(0.06, dy * 0.15)) + 0.01, v.z * 0.8);
                if (Math.abs(dy) < 0.35) {
                    setBasking(true);
                }
                rising--;
                return;
            }
            ticks--;
            // lying still at the surface: held there, drifting a little (the 0.01 makes up for the fish's slow sinking)
            setDeltaMovement(v.x * 0.5, Math.max(-0.05, Math.min(0.05, dy * 0.3)) + 0.01, v.z * 0.5);
        }

        @Override
        public boolean requiresUpdateEveryTick() {
            return true;
        }

        @Override
        public void stop() {
            setBasking(false);
            ticks = 0;
        }
    }

    // ---- test hooks ----

    /** For the in-game test: starts basking at once where it is (the surface must be above it). */
    public boolean baskNow() {
        double surface = surfaceAbove(level(), position(), BASK_REACH);
        if (Double.isNaN(surface)) {
            return false;
        }
        snapTo(getX(), surface - BASK_DEPTH, getZ(), getYRot(), 0.0F);
        setBasking(true);
        return true;
    }
}
