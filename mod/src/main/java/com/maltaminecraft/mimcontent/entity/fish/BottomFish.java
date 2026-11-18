package com.maltaminecraft.mimcontent.entity.fish;

import java.util.EnumSet;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.tags.FluidTags;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.goal.AvoidEntityGoal;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.PanicGoal;
import net.minecraft.world.entity.ai.goal.RandomSwimmingGoal;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * A fish that lives near the sea floor, set up by its {@link Habit} (the night job's fish, 2026-11-18: trilja,
 * gallinella, sawt, petriċa, lingwata over a soft floor; marzpan, ħmar and the lionfish over rock; the tird over any
 * floor). It is the boll's and skorfna's way of living, made into one class with numbers instead of one class per fish:
 * <ul>
 * <li>It swims to spots between {@link Habit#swimLow} and {@link Habit#swimHigh} blocks above the floor below them, and
 *     sinks gently back when it drifts higher while idle.</li>
 * <li>Now and then (about every {@link Habit#restEvery} ticks; 0 never) it settles on the bottom and lies still for
 *     {@link Habit#restMin} to {@link Habit#restMax} ticks. A fish that rests a lot (the sawt, the petriċa) is mostly
 *     found lying on the floor.</li>
 * <li>A shy fish ({@link Habit#shy}) swims away from players like vanilla's fish, except while resting; every one panics
 *     when hurt.</li>
 * <li>A flat fish ({@link Habit#flat}: the lingwata, the petriċa) lies flat on land instead of flopping on its side.</li>
 * <li>A venomous one ({@link Habit#sting}: the sawt, the lionfish) stings, like the skorfna: a survival or adventure
 *     player or a mob (not another fish) that touches it (bumps into it, stands or walks on it) or hits it in melee
 *     takes the sting's damage and Poison, at most once per cooldown. Arrows and thrown tridents don't count.
 *     {@link Venom} decides who can be stung (not creative, spectator, peaceful, or under Jellyfish Ward).</li>
 * </ul>
 * It spawns only over its kind of floor ({@link Floor}) no more than {@link #SPAWN_FLOOR_DEPTH} blocks under the spawn
 * point, at any depth below sea level, and a natural spawn is set down near that floor.
 */
public class BottomFish extends MimFish {
    /** How deep under a spawn point its floor may lie, in blocks (as the boll and skorfna). */
    public static final int SPAWN_FLOOR_DEPTH = 16;
    /** How close counts as touching a venomous one, in blocks beyond its body box (as the skorfna). */
    public static final double TOUCH_MARGIN = 0.1;
    /** How far above the top of its band a bottom fish may go before it is held down, in blocks (unless fleeing). */
    public static final double BAND_MARGIN = 0.5;

    /** The floor it lives over. */
    public enum Floor {
        /** Sand, gravel, clay and mud ({@link BollFish#isSoftFloor}). */
        SOFT,
        /** Any other solid block ({@link SkorfnaFish#isRockFloor}). */
        ROCK,
        /** Either. */
        ANY;

        public boolean accepts(BlockState state) {
            return switch (this) {
                case SOFT -> BollFish.isSoftFloor(state);
                case ROCK -> SkorfnaFish.isRockFloor(state);
                case ANY -> state.getFluidState().isEmpty() && state.isSolid();
            };
        }
    }

    /** A venomous fish's sting: damage (2 = 1 heart), Poison seconds, and ticks between two stings. */
    public record Sting(float damage, int poisonSeconds, int cooldown) {
    }

    /**
     * How it lives. swimLow / swimHigh: the band above the floor it swims in, blocks. swimSpeed: times its movement
     * speed when it swims about; swimEvery: about how many ticks between two swims. restEvery: about how many ticks
     * between two rests (0: it never rests); restMin / restMax: how long a rest lasts, ticks. shy: swims away from
     * players. flat: lies flat on land. sting: null if harmless.
     */
    public record Habit(Floor floor, double swimLow, double swimHigh, double swimSpeed, int swimEvery, int restEvery, int restMin,
                        int restMax, boolean shy, boolean flat, @Nullable Sting sting) {
    }

    private final Habit habit;
    /** True while it lies still on the bottom (server side). */
    private boolean resting;
    private long nextSting;

    public BottomFish(EntityType<? extends MimFish> type, Level level, Supplier<Item> bucket, int spawnCluster, Habit habit) {
        super(type, level, bucket, spawnCluster);
        this.habit = habit;
        // registerGoals runs in the super constructor, before the habit is known, so the goals are added here
        addGoals();
    }

    public Habit habit() {
        return habit;
    }

    public boolean isResting() {
        return resting;
    }

    @Override
    protected void registerGoals() {
        // the goals depend on the habit, which isn't set yet here: added in the constructor (addGoals)
    }

    private void addGoals() {
        this.goalSelector.addGoal(0, new PanicGoal(this, 1.25));
        if (habit.shy()) {
            this.goalSelector.addGoal(2, new AvoidEntityGoal<>(this, Player.class, 8.0F, 1.6, 1.4, e -> !e.isSpectator()) {
                @Override
                public boolean canUse() {
                    return !resting && super.canUse();
                }
            });
        }
        if (habit.restEvery() > 0) {
            this.goalSelector.addGoal(3, new RestGoal());
        }
        this.goalSelector.addGoal(4, new BottomSwimGoal());
    }

    // ---- living near the floor ----

    /** Its kind of floor under a water position, within SPAWN_FLOOR_DEPTH blocks, or null (another kind, or too deep). */
    public static @Nullable BlockPos floorBelow(Floor floor, BlockGetter level, BlockPos pos) {
        BlockPos.MutableBlockPos p = pos.mutable();
        for (int i = 0; i <= SPAWN_FLOOR_DEPTH; i++) {
            BlockState state = level.getBlockState(p);
            if (!state.getFluidState().is(FluidTags.WATER)) {
                return floor.accepts(state) ? p.immutable() : null;
            }
            p.move(0, -1, 0);
        }
        return null;
    }

    /**
     * The spawn rule: in open water (water here and above, as vanilla's fish), anywhere below sea level, over its kind
     * of floor within SPAWN_FLOOR_DEPTH blocks. Spawners aren't held to the floor.
     */
    public static boolean checkSpawnRules(Floor floor, ServerLevelAccessor level, EntitySpawnReason reason, BlockPos pos) {
        if (!level.getFluidState(pos).is(FluidTags.WATER) || !level.getBlockState(pos.above()).is(Blocks.WATER)) {
            return false;
        }
        if (reason == EntitySpawnReason.SPAWNER || reason == EntitySpawnReason.TRIAL_SPAWNER) {
            return true;
        }
        return pos.getY() < level.getSeaLevel() && floorBelow(floor, level, pos) != null;
    }

    @Override
    public @Nullable SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, EntitySpawnReason reason,
                                                  @Nullable SpawnGroupData group) {
        if (reason == EntitySpawnReason.NATURAL || reason == EntitySpawnReason.CHUNK_GENERATION) {
            // spawned somewhere in the water column: down to its floor, at the bottom of its band
            BlockPos floor = floorBelow(habit.floor(), level, blockPosition());
            if (floor != null) {
                snapTo(getX(), floor.getY() + 1.0 + habit.swimLow(), getZ(), getYRot(), 0.0F);
            }
        }
        return super.finalizeSpawn(level, difficulty, reason, group);
    }

    @Override
    public void aiStep() {
        if (habit.flat() && !isInWater() && onGround()) {
            // on land a flat fish lies flat instead of flopping about (AbstractFish hops when this is set), as the boll
            this.verticalCollision = false;
        }
        super.aiStep();
        if (!level().isClientSide() && isInWater()) {
            double above = BollFish.heightAboveFloor(level(), position(), 8);
            if (above > habit.swimHigh() + BAND_MARGIN && getLastHurtByMob() == null) {
                // well above its band and not fleeing: it never rises further, and sinks back (a bottom fish stays
                // near its floor whatever its path does)
                Vec3 v = getDeltaMovement();
                setDeltaMovement(v.x, Math.min(v.y, 0.0) - 0.01, v.z);
            } else if (!resting && getNavigation().isDone() && tickCount % 5 == 0 && above > habit.swimHigh()) {
                // idle above its band (water navigation counts a spot as reached up to a block off): sink gently back
                setDeltaMovement(getDeltaMovement().add(0.0, -0.02, 0.0));
            }
        }
    }

    // ---- the sting ----

    @Override
    public void tick() {
        super.tick();
        if (habit.sting() != null && level() instanceof ServerLevel level && isAlive() && level.getGameTime() >= nextSting) {
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
            resting = false;
            // a melee hit (not an arrow or a thrown trident) meets the spines
            if (habit.sting() != null && source.getEntity() instanceof LivingEntity attacker && source.getDirectEntity() == attacker
                && !source.is(DamageTypeTags.IS_PROJECTILE)) {
                sting(level, attacker);
            }
        }
        return hurt;
    }

    /** Stings, if venomous, the cooldown allows and the target can be stung. Returns true if it stung. */
    public boolean sting(ServerLevel level, LivingEntity target) {
        Sting sting = habit.sting();
        long now = level.getGameTime();
        if (sting == null || now < nextSting || !Venom.canSting(target)) {
            return false;
        }
        nextSting = now + sting.cooldown();
        Venom.strike(level, this, target, sting.damage(), sting.poisonSeconds());
        return true;
    }

    // ---- goals ----

    /** Swims to random spots in the water, each within its band above the floor below it. */
    private class BottomSwimGoal extends RandomSwimmingGoal {
        BottomSwimGoal() {
            super(BottomFish.this, habit.swimSpeed(), habit.swimEvery());
        }

        @Override
        public boolean canUse() {
            return !resting && canRandomSwim() && super.canUse();
        }

        @Override
        protected @Nullable Vec3 getPosition() {
            Vec3 spot = super.getPosition();
            // vanilla's pick can give up and hand back a spot out of the water (above the surface): not one for us
            if (spot == null || !level().getFluidState(BlockPos.containing(spot)).is(FluidTags.WATER)) {
                return null;
            }
            double above = BollFish.heightAboveFloor(level(), spot, 24);
            if (above > 24) {
                return null;
            }
            double want = habit.swimLow() + getRandom().nextDouble() * (habit.swimHigh() - habit.swimLow());
            return new Vec3(spot.x, spot.y - above + want, spot.z);
        }
    }

    /** Now and then, near the bottom, it settles onto the floor and lies still. */
    private class RestGoal extends Goal {
        private int ticks;

        RestGoal() {
            setFlags(EnumSet.of(Goal.Flag.MOVE, Goal.Flag.JUMP));
        }

        @Override
        public boolean canUse() {
            return isInWater() && getRandom().nextInt(reducedTickDelay(habit.restEvery())) == 0
                && BollFish.heightAboveFloor(level(), position(), 6) < habit.swimHigh() + 1.0;
        }

        @Override
        public void start() {
            ticks = habit.restMin() + getRandom().nextInt(habit.restMax() - habit.restMin() + 1);
            resting = true;
            getNavigation().stop();
        }

        @Override
        public boolean canContinueToUse() {
            return resting && ticks > 0 && isInWater() && getLastHurtByMob() == null;
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
