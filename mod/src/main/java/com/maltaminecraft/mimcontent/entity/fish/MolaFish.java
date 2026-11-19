package com.maltaminecraft.mimcontent.entity.fish;

import java.util.EnumSet;
import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.Mth;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.RandomSwimmingGoal;
import net.minecraft.world.entity.animal.fish.WaterAnimal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.phys.Vec3;

/**
 * The mola mola (ocean sunfish, Mola mola; decision 2026-11-18 "Mola mola - start"), the heaviest bony fish: a tall
 * flat disc with no tail, which swims slowly by sculling its tall dorsal and anal fins from side to side together.
 * <ul>
 * <li><b>Extremely rare</b> (owner 2026-11-18: "the mola mola must be EXTREMELY rare, with fishing it with the required
 *     bait being practically the only way to find it unless you are super lucky"): besides the lowest spawn weight,
 *     only one natural spawn try in {@link #SPAWN_CHANCE} that picks it goes ahead ({@link #checkMolaSpawnRules}).
 *     Spawn eggs, spawners and /summon always work.</li>
 * <li><b>Found, never captured</b> (owner 2026-11-19, "Mola mola - can be found, not captured; escapes when hurt;
 *     basks in the sun"): a water bucket does nothing to it (there is no mola bucket), and it drops nothing. The raw
 *     item stays registered for fishing later.</li>
 * <li>Passive, slow ({@link #SPEED}) and harmless. It doesn't shy away from players (real sunfish are known for
 *     letting divers come close).</li>
 * <li><b>Tough:</b> 40 health, and no single hit takes more than {@link #MAX_HIT} ({@link #hurtServer}). /kill and the
 *     void (damage that bypasses invulnerability) are not capped.</li>
 * <li><b>Escapes when hurt</b> ({@link EscapeGoal}): it bursts away from whatever hurt it, a little downward while there
 *     is water below, at {@link #ESCAPE_SPEED} blocks a tick for {@link #ESCAPE_TICKS} ticks, faster than a
 *     sprint-swimming player. Hurt by a player (or a player's arrow, trident, TNT...), it fades out over the last
 *     {@link #FADE_TICKS} ticks with bubbles and is removed: no death, no drop, it never comes back. Hurt by anything
 *     else it only flees; a second hit from a mob (a guardian, a drowned) while it is still fleeing makes it vanish
 *     too. Damage with no attacker (drying out, fire) never makes it vanish.</li>
 * <li><b>Basking:</b> now and then it rises to the surface and lies there on its side for 10 to 30 seconds, as the
 *     real fish does after deep dives, but only in the sun ({@link #sunOut}): by day, in clear weather, with the sky
 *     open above the water. While basking it is drawn and hit on its side (like a fish on land, centred on its
 *     position) and its body box is flat, so it doesn't stand out of the water. Hurting it, nightfall or rain end the
 *     basking.</li>
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
    /** Its health (20 hearts). */
    public static final double HEALTH = 40.0;
    /** The most any one hit takes, whatever the weapon (2 hearts). */
    public static final float MAX_HIT = 4.0F;
    /**
     * How fast it escapes, in blocks a tick (7.5 blocks a second). Vanilla's sprint-swimming player
     * (LivingEntity.travelInWater: 0.02 a tick pushed, 0.9 kept) settles at 0.0196 / 0.1 = 0.196 blocks a tick (3.9 a
     * second); with Depth Strider III 0.265 (5.3 a second). Only Dolphin's Grace (0.49, 9.8 a second) is faster.
     */
    public static final double ESCAPE_SPEED = 0.375;
    /** How fast it sinks while it escapes, in blocks a tick, while there is water under it. */
    public static final double ESCAPE_DIVE = 0.04;
    /** How long the escape lasts (4 seconds: 30 blocks at ESCAPE_SPEED). */
    public static final int ESCAPE_TICKS = 80;
    /** The last part of the escape, in which a fish that vanishes fades out (2 seconds). */
    public static final int FADE_TICKS = 40;
    /** One in this many goal checks (every other tick, so about every 20 seconds) it sets off to bask, if the sun is out. */
    public static final int BASK_CHANCE = 400;

    /** The escape's state, synced: none, fleeing, or fading out (it vanishes at the end). */
    public static final int CALM = 0, FLEEING = 1, FADING = 2;

    /** How many times it has set off for the surface to bask (server side; read by the in-game test). */
    public int baskTrips;

    private static final EntityDataAccessor<Boolean> DATA_BASKING = SynchedEntityData.defineId(MolaFish.class, EntityDataSerializers.BOOLEAN);
    private static final EntityDataAccessor<Integer> DATA_ESCAPE = SynchedEntityData.defineId(MolaFish.class, EntityDataSerializers.INT);

    /** Ticks of escape left (server side); 0 when calm. */
    private int escapeTicks;
    /** Whether this escape ends with it fading out and gone (server side). */
    private boolean vanishes;
    /** Its escape's heading (horizontal, length 1), and which way it turns first round a wall. */
    private Vec3 escapeDir = Vec3.ZERO;
    private int turnSign = 1;
    /** Client side: ticks since it began to fade. */
    private int fadeAge;

    public MolaFish(EntityType<? extends MimFish> type, Level level, Supplier<Item> bucket, int spawnCluster) {
        super(type, level, bucket, spawnCluster);
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(DATA_BASKING, false);
        builder.define(DATA_ESCAPE, CALM);
    }

    /** CALM, FLEEING or FADING (synced). */
    public int escapeState() {
        return entityData.get(DATA_ESCAPE);
    }

    /** How opaque it is drawn: 1, falling to 0 over its fade (client side). */
    public float fadeAlpha(float partialTick) {
        if (escapeState() != FADING) {
            return 1.0F;
        }
        return Mth.clamp(1.0F - (fadeAge + partialTick) / FADE_TICKS, 0.0F, 1.0F);
    }

    /** No bucket: the mola can't be caught (owner 2026-11-19). */
    @Override
    public ItemStack getBucketItemStack() {
        return ItemStack.EMPTY;
    }

    /**
     * A water bucket does nothing to it: no catch, and the bucket is neither used up nor emptied into the water (the
     * action is taken, so the client doesn't go on to pour the bucket out).
     */
    @Override
    protected InteractionResult mobInteract(Player player, InteractionHand hand) {
        if (player.getItemInHand(hand).is(Items.WATER_BUCKET)) {
            return InteractionResult.CONSUME;
        }
        return super.mobInteract(player, hand);
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
        // no shying from players (AbstractFish's AvoidEntityGoal is left out); hurt, it escapes (instead of a panic)
        this.goalSelector.addGoal(0, new EscapeGoal());
        this.goalSelector.addGoal(3, new BaskGoal());
        this.goalSelector.addGoal(4, new RandomSwimmingGoal(this, 0.8, 80) {
            @Override
            public boolean canUse() {
                return !isBasking() && super.canUse();
            }
        });
    }

    /**
     * Every hit is capped at MAX_HIT (melee with any sword and enchantment, crits, sweeps, arrows, tridents,
     * explosions), except /kill and the void. Hurt, it stops basking and escapes.
     */
    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float amount) {
        boolean uncapped = source.is(DamageTypeTags.BYPASSES_INVULNERABILITY);
        boolean hurt = super.hurtServer(level, source, uncapped ? amount : Math.min(amount, MAX_HIT));
        if (hurt) {
            setBasking(false);
            if (!uncapped && isAlive()) {
                escapeFrom(source);
            }
        }
        return hurt;
    }

    /** Starts (or renews) the escape from what hurt it; see the class note for when it vanishes. */
    private void escapeFrom(DamageSource source) {
        if (escapeState() == FADING) {
            return;
        }
        Entity attacker = source.getEntity();
        boolean byPlayer = attacker instanceof Player;
        // a mob hitting it again while it still flees from a mob's hit
        boolean hitsGoOn = attacker != null && escapeTicks > 0;
        if (byPlayer || hitsGoOn) {
            vanishes = true;
        }
        Vec3 from = source.getSourcePosition();
        if (from == null && attacker != null) {
            from = attacker.position();
        }
        Vec3 away = from == null ? Vec3.ZERO : new Vec3(getX() - from.x, 0.0, getZ() - from.z);
        if (away.lengthSqr() < 1.0E-4) {
            float a = getRandom().nextFloat() * Mth.TWO_PI;
            away = new Vec3(Mth.cos(a), 0.0, Mth.sin(a));
        }
        escapeDir = away.normalize();
        turnSign = getRandom().nextBoolean() ? 1 : -1;
        escapeTicks = ESCAPE_TICKS;
        entityData.set(DATA_ESCAPE, FLEEING);
    }

    @Override
    public void tick() {
        super.tick();
        if (level().isClientSide()) {
            clientEscapeTick();
            return;
        }
        if (escapeTicks <= 0) {
            return;
        }
        escapeTicks--;
        if (vanishes && escapeTicks <= FADE_TICKS && escapeState() != FADING) {
            entityData.set(DATA_ESCAPE, FADING);
        }
        if (escapeTicks == 0) {
            if (vanishes) {
                // gone into the blue: no death, no drop
                discard();
                return;
            }
            entityData.set(DATA_ESCAPE, CALM);
        }
    }

    /** Client side: a trail of bubbles while it flees, more while it fades, and the fade's clock. */
    private void clientEscapeTick() {
        int state = escapeState();
        if (state == CALM) {
            fadeAge = 0;
            return;
        }
        if (state == FADING) {
            fadeAge++;
        }
        if (!isInWater()) {
            return;
        }
        int n = state == FADING ? 4 : 1;
        for (int i = 0; i < n; i++) {
            level().addParticle(ParticleTypes.BUBBLE, getRandomX(0.8), getRandomY(), getRandomZ(0.8), 0.0, 0.05, 0.0);
        }
    }

    @Override
    protected void addAdditionalSaveData(ValueOutput output) {
        super.addAdditionalSaveData(output);
        // so a mola saved mid-escape (its chunk unloading) still vanishes when it is back
        if (escapeTicks > 0) {
            output.putInt("EscapeTicks", escapeTicks);
            output.putBoolean("Vanishes", vanishes);
        }
    }

    @Override
    protected void readAdditionalSaveData(ValueInput input) {
        super.readAdditionalSaveData(input);
        escapeTicks = input.getIntOr("EscapeTicks", 0);
        vanishes = input.getBooleanOr("Vanishes", false);
        if (escapeTicks > 0) {
            float a = getRandom().nextFloat() * Mth.TWO_PI;
            escapeDir = new Vec3(Mth.cos(a), 0.0, Mth.sin(a));
            entityData.set(DATA_ESCAPE, vanishes && escapeTicks <= FADE_TICKS ? FADING : FLEEING);
        }
    }

    /**
     * True when the sun is out over it: day, no rain or thunder, and the sky open above the water's surface here
     * (nothing over the water, not even glass or leaves).
     */
    public boolean sunOut(double surface) {
        Level level = level();
        if (Double.isNaN(surface) || !level.isBrightOutside() || level.isRaining() || level.isThundering()) {
            return false;
        }
        BlockPos air = BlockPos.containing(getX(), surface - 0.5, getZ()).above();
        return level.getHeight(Heightmap.Types.MOTION_BLOCKING, air.getX(), air.getZ()) <= air.getY();
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
            if (!isInWater() || getLastHurtByMob() != null || escapeTicks > 0 || getRandom().nextInt(reducedTickDelay(BASK_CHANCE)) != 0) {
                return false;
            }
            surface = surfaceAbove(level(), position(), BASK_REACH);
            return !Double.isNaN(surface) && sunOut(surface);
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
            return ticks > 0 && rising > 0 && isInWater() && getLastHurtByMob() == null && escapeTicks <= 0 && sunOut(surface);
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

    /**
     * The escape: straight away from what hurt it at ESCAPE_SPEED, sinking a little while there is water under it,
     * turning along a wall rather than stopping at it. Nothing else moves it meanwhile (no basking, no wandering).
     */
    private class EscapeGoal extends Goal {
        EscapeGoal() {
            setFlags(EnumSet.of(Goal.Flag.MOVE, Goal.Flag.JUMP, Goal.Flag.LOOK));
        }

        @Override
        public boolean canUse() {
            return escapeTicks > 0;
        }

        @Override
        public void start() {
            getNavigation().stop();
            setBasking(false);
        }

        @Override
        public boolean requiresUpdateEveryTick() {
            return true;
        }

        @Override
        public void tick() {
            getNavigation().stop();
            if (!isInWater()) {
                return;
            }
            escapeDir = steer(escapeDir);
            double dy = waterAt(getX(), getBoundingBox().minY - 1.0, getZ()) ? -ESCAPE_DIVE : 0.0;
            setDeltaMovement(escapeDir.x * ESCAPE_SPEED, dy, escapeDir.z * ESCAPE_SPEED);
            float yaw = (float) (Mth.atan2(escapeDir.z, escapeDir.x) * Mth.RAD_TO_DEG) - 90.0F;
            setYRot(yaw);
            yBodyRot = yaw;
            yHeadRot = yaw;
        }

        /** The heading, or the nearest turn from it (30 degrees at a time) with water ahead. */
        private Vec3 steer(Vec3 dir) {
            if (clearAhead(dir)) {
                return dir;
            }
            for (int step = 1; step <= 6; step++) {
                for (int sign : new int[] {turnSign, -turnSign}) {
                    float a = sign * step * 30.0F * Mth.DEG_TO_RAD;
                    Vec3 turned = new Vec3(dir.x * Mth.cos(a) - dir.z * Mth.sin(a), 0.0, dir.x * Mth.sin(a) + dir.z * Mth.cos(a));
                    if (clearAhead(turned)) {
                        return turned;
                    }
                }
            }
            return dir;
        }

        private boolean clearAhead(Vec3 dir) {
            double reach = getBbWidth() / 2.0 + 1.0;
            double x = getX() + dir.x * reach, z = getZ() + dir.z * reach;
            return waterAt(x, getY() + 0.3, z) && waterAt(x, getY() + Math.max(0.3, getBbHeight() - 0.3), z);
        }

        private boolean waterAt(double x, double y, double z) {
            return level().getFluidState(BlockPos.containing(x, y, z)).is(FluidTags.WATER);
        }
    }

    // ---- test hooks ----

    /** For the in-game test: ticks of escape left (server side), and whether it will vanish. */
    public int escapeTicksLeft() {
        return escapeTicks;
    }

    public boolean willVanish() {
        return vanishes;
    }

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
