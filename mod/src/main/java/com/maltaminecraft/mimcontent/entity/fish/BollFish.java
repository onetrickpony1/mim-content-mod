package com.maltaminecraft.mimcontent.entity.fish;

import java.util.EnumSet;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.goal.AvoidEntityGoal;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.PanicGoal;
import net.minecraft.world.entity.ai.goal.RandomSwimmingGoal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.VoxelShape;
import org.jspecify.annotations.Nullable;

/**
 * The boll (common stingray, Dasyatis pastinaca), a flat ray that lives on sandy bottoms
 * (decision 2026-11-18 "Stingray next"). It lies half buried in sand and is not aggressive, but strikes with the spine
 * on its tail when stepped on or harassed:
 * <ul>
 * <li>It swims a block or two above the sea floor, never up near the surface like the other fish, and now and then
 *     settles on the bottom and lies still for a while. A resting boll doesn't shy away from players.</li>
 * <li>Hurt it and it stings the attacker if within {@link #STING_REACH} blocks ({@link #STING_DAMAGE} damage and
 *     Poison for {@link #POISON_SECONDS} seconds), then swims off (it panics like any fish).</li>
 * <li>A survival or adventure player whose feet touch it (standing or walking on it, e.g. wading in shallow water) is
 *     stung the same way, at most once every {@link #STING_COOLDOWN} ticks.</li>
 * <li>Creative and spectator players, and peaceful difficulty, are never stung ({@link Venom}, shared with the skorfna).</li>
 * </ul>
 * It spawns only over a soft bottom (sand, gravel, clay, mud) that lies within {@link #SPAWN_FLOOR_DEPTH} blocks
 * under the spawn point, at any depth below sea level (the vanilla fish rule, within 13 blocks of sea level, would
 * keep it off the deeper Malta sea floor), and is moved down onto that floor when it spawns naturally.
 */
public class BollFish extends MimFish {
    /** The sting: damage (1 heart) and how long the poison lasts. */
    public static final float STING_DAMAGE = 2.0F;
    public static final int POISON_SECONDS = 5;
    /** How far the tail reaches an attacker, in blocks between the two boxes. */
    public static final double STING_REACH = 2.0;
    /** Ticks between two stings (2 seconds). */
    public static final int STING_COOLDOWN = 40;
    /** How far above the floor it likes to swim, in blocks (it aims between these). */
    public static final double SWIM_LOW = 0.3, SWIM_HIGH = 1.6;
    /** How deep under a spawn point the soft floor may lie, in blocks. */
    public static final int SPAWN_FLOOR_DEPTH = 16;

    /** True while it lies still on the bottom (server side). */
    private boolean resting;
    private long nextSting;

    public BollFish(EntityType<? extends MimFish> type, Level level, Supplier<Item> bucket, int spawnCluster) {
        super(type, level, bucket, spawnCluster);
    }

    public boolean isResting() {
        return resting;
    }

    @Override
    protected void registerGoals() {
        // vanilla fish's panic and shyness, but not while resting on the bottom; its own swimming near the floor
        this.goalSelector.addGoal(0, new PanicGoal(this, 1.25));
        this.goalSelector.addGoal(2, new AvoidEntityGoal<>(this, Player.class, 8.0F, 1.6, 1.4, e -> !e.isSpectator()) {
            @Override
            public boolean canUse() {
                return !resting && super.canUse();
            }
        });
        this.goalSelector.addGoal(3, new RestGoal());
        this.goalSelector.addGoal(4, new BottomSwimGoal());
    }

    // ---- living on the bottom ----

    /** How far the floor (the first block that isn't water) lies below a point, up to max blocks; max + 1 if deeper. */
    public static double heightAboveFloor(BlockGetter level, Vec3 at, int max) {
        BlockPos.MutableBlockPos p = BlockPos.containing(at).mutable();
        for (int i = 0; i <= max; i++) {
            BlockState state = level.getBlockState(p);
            if (!state.getFluidState().is(FluidTags.WATER) || state.isSolid()) {
                VoxelShape shape = state.getCollisionShape(level, p);
                return at.y - (p.getY() + (shape.isEmpty() ? 0.0 : shape.max(Direction.Axis.Y)));
            }
            p.move(0, -1, 0);
        }
        return max + 1;
    }

    /** True for the soft bottoms a stingray lies on: sand, gravel, clay and mud. */
    public static boolean isSoftFloor(BlockState state) {
        return state.is(BlockTags.SAND) || state.is(Blocks.GRAVEL) || state.is(Blocks.SUSPICIOUS_GRAVEL) || state.is(Blocks.CLAY)
            || state.is(Blocks.MUD) || state.is(Blocks.PACKED_MUD);
    }

    /** The soft floor under a water position, within SPAWN_FLOOR_DEPTH blocks, or null (rock, or too deep). */
    public static @Nullable BlockPos softFloorBelow(BlockGetter level, BlockPos pos) {
        BlockPos.MutableBlockPos p = pos.mutable();
        for (int i = 0; i <= SPAWN_FLOOR_DEPTH; i++) {
            BlockState state = level.getBlockState(p);
            if (!state.getFluidState().is(FluidTags.WATER)) {
                return isSoftFloor(state) ? p.immutable() : null;
            }
            p.move(0, -1, 0);
        }
        return null;
    }

    /**
     * The spawn rule: in open water (water below and above, as vanilla's fish), anywhere below sea level, over a soft
     * floor within SPAWN_FLOOR_DEPTH blocks. Spawners and eggs aren't held to the floor.
     */
    public static boolean checkBollSpawnRules(EntityType<? extends MimFish> type, ServerLevelAccessor level, EntitySpawnReason reason,
                                              BlockPos pos, RandomSource random) {
        if (!level.getFluidState(pos).is(FluidTags.WATER) || !level.getBlockState(pos.above()).is(Blocks.WATER)) {
            return false;
        }
        if (reason == EntitySpawnReason.SPAWNER || reason == EntitySpawnReason.TRIAL_SPAWNER) {
            return true;
        }
        return pos.getY() < level.getSeaLevel() && softFloorBelow(level, pos) != null;
    }

    @Override
    public @Nullable SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, EntitySpawnReason reason,
                                                  @Nullable SpawnGroupData group) {
        if (reason == EntitySpawnReason.NATURAL || reason == EntitySpawnReason.CHUNK_GENERATION) {
            // spawned somewhere in the water column: down onto the floor, where it lives
            BlockPos floor = softFloorBelow(level, blockPosition());
            if (floor != null) {
                snapTo(getX(), floor.getY() + 1.0, getZ(), getYRot(), 0.0F);
            }
        }
        return super.finalizeSpawn(level, difficulty, reason, group);
    }

    @Override
    public void aiStep() {
        if (!isInWater() && onGround()) {
            // on land it lies flat instead of flopping about like a fish (AbstractFish hops when this is set)
            this.verticalCollision = false;
        }
        super.aiStep();
        if (!level().isClientSide() && isInWater() && !resting && getNavigation().isDone() && tickCount % 5 == 0
            && heightAboveFloor(level(), position(), 6) > SWIM_HIGH) {
            // idle and above its band: sink gently back toward the bottom. Vanilla's water navigation counts a spot as
            // reached up to a block above it and the fish then floats where it is, so without this a boll aiming for
            // the top of its band could park up to SWIM_HIGH + 1 blocks up until it next rested (the cause of the
            // flaky "should stay near the bottom" check, 2026-11-18)
            setDeltaMovement(getDeltaMovement().add(0.0, -0.02, 0.0));
        }
    }

    // ---- the sting ----

    @Override
    public void tick() {
        super.tick();
        if (level() instanceof ServerLevel level && isAlive()) {
            // a player whose feet touch it: standing or walking on it, or wading onto it
            AABB box = getBoundingBox();
            List<Player> on = level.getEntitiesOfClass(Player.class, box.inflate(0.0, 0.2, 0.0), p -> p.getY() >= box.minY - 0.1
                && p.getY() <= box.maxY + 0.2 && !p.hasPose(Pose.SWIMMING));
            for (Player player : on) {
                sting(level, player);
            }
        }
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float amount) {
        boolean hurt = super.hurtServer(level, source, amount);
        if (hurt && isAlive() && source.getEntity() instanceof LivingEntity attacker
            && getBoundingBox().inflate(STING_REACH).intersects(attacker.getBoundingBox())) {
            sting(level, attacker);
        }
        return hurt;
    }

    /** Strikes with the tail spine: damage and poison, if the cooldown allows. Returns true if it stung. */
    public boolean sting(ServerLevel level, LivingEntity target) {
        long now = level.getGameTime();
        if (now < nextSting || !Venom.canSting(target)) {
            return false;
        }
        nextSting = now + STING_COOLDOWN;
        resting = false;
        Venom.strike(level, this, target, STING_DAMAGE, POISON_SECONDS);
        return true;
    }

    // ---- goals ----

    /** Swims to random spots, each a block or two above the floor below it. */
    private class BottomSwimGoal extends RandomSwimmingGoal {
        BottomSwimGoal() {
            super(BollFish.this, 0.8, 60);
        }

        @Override
        public boolean canUse() {
            return !resting && canRandomSwim() && super.canUse();
        }

        @Override
        protected @Nullable Vec3 getPosition() {
            Vec3 spot = super.getPosition();
            // vanilla's pick gives up after ten tries and may hand back a spot out of the water (above the surface),
            // which would send the boll up to the top: not one for it
            if (spot == null || !level().getFluidState(BlockPos.containing(spot)).is(FluidTags.WATER)) {
                return null;
            }
            double above = heightAboveFloor(level(), spot, 24);
            if (above > 24) {
                return null;
            }
            double want = SWIM_LOW + getRandom().nextDouble() * (SWIM_HIGH - SWIM_LOW);
            return new Vec3(spot.x, spot.y - above + want, spot.z);
        }
    }

    /** Now and then, near the bottom, it settles and lies still for 5 to 20 seconds. */
    private class RestGoal extends Goal {
        private int ticks;

        RestGoal() {
            setFlags(EnumSet.of(Goal.Flag.MOVE, Goal.Flag.JUMP));
        }

        @Override
        public boolean canUse() {
            return isInWater() && getRandom().nextInt(reducedTickDelay(160)) == 0 && heightAboveFloor(level(), position(), 4) < 2.5;
        }

        @Override
        public void start() {
            ticks = 100 + getRandom().nextInt(300);
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
            // settle onto the floor and stay put
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
