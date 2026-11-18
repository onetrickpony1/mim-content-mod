package com.maltaminecraft.mimcontent.entity.jelly;

import com.maltaminecraft.mimcontent.MimJellyfish;
import com.maltaminecraft.mimcontent.entity.fish.Venom;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.Mth;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MoverType;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import net.minecraft.world.entity.animal.fish.WaterAnimal;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.material.FluidState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * A jellyfish (owner, 2026-11-18: "get makers started on all 3 jellyfish types"; docs/Creatures and Plants/Jellyfish.md).
 * One class for the three kinds ({@link Kind}); only what the owner has agreed so far:
 * <ul>
 * <li><b>Mauve stinger and fried-egg:</b> drift, slowly sinking, and now and then pulse upward. They are not fish: they
 *     don't flee, and out of water they lie still and die slowly (vanilla's drowning for water animals), without
 *     flopping. The mauve stinger keeps near the surface at night and lower by day.</li>
 * <li><b>Man o' war:</b> floats on the surface and drifts; its tentacles hang about 3.5 blocks below it, and touching
 *     them anywhere in that column stings.</li>
 * <li><b>Stings</b> ({@link Venom#stingGently}): anyone touching one (not fish, not other jellyfish) is stung, at most
 *     once every {@link #STING_COOLDOWN} ticks; a melee hit on it stings the attacker too. Never creative, spectator or
 *     peaceful, and never deadly. The fried-egg doesn't sting.</li>
 * <li><b>Night glow</b> (idea 8): a mauve stinger that is touched or hit, or at random in rain, flashes green glow
 *     particles for {@link #FLASH_TICKS} ticks and is drawn full-bright meanwhile (synced as {@link #isFlashing}).</li>
 * </ul>
 * Drops (loot tables): jellyfish venom and jellyfish meat (owner, 2026-11-18), no bucket. Jellyfish Ward blocks the
 * stings ({@link MimJellyfish#WARD}). Swarms, seasons, beachings and first aid wait for the owner's answers.
 */
public class Jellyfish extends WaterAnimal {
    // ---- stings ----
    /** Mauve stinger: 2 damage (1 heart) and Poison for 5 seconds. */
    public static final float MAUVE_STING_DAMAGE = 2.0F;
    public static final int MAUVE_POISON_SECONDS = 5;
    /** Man o' war: 3 damage (1.5 hearts), Poison for 8 seconds and Nausea for 5 seconds. */
    public static final float MAN_O_WAR_STING_DAMAGE = 3.0F;
    public static final int MAN_O_WAR_POISON_SECONDS = 8;
    public static final int MAN_O_WAR_NAUSEA_SECONDS = 5;
    /** Ticks between two stings from the same jellyfish (2 seconds). */
    public static final int STING_COOLDOWN = 40;
    /** How close counts as touching, in blocks beyond its box. */
    public static final double TOUCH_MARGIN = 0.1;
    /** How far a melee attacker can be and still be stung, in blocks. */
    public static final double MELEE_STING_RANGE = 3.0;
    /** How far the man o' war's tentacles hang below its float, in blocks (the stinging column). */
    public static final double MAN_O_WAR_TENTACLE_LENGTH = 3.5;

    // ---- the mauve stinger's glow ----
    /** How long one flash lasts, in ticks (1.5 seconds). */
    public static final int FLASH_TICKS = 30;
    /** In rain, a mauve stinger flashes on its own about once in this many ticks (20 seconds). */
    public static final int RAIN_FLASH_CHANCE = 400;

    // ---- drifting and pulsing ----
    /** Upward speed a pulse gives, in blocks per tick (one pulse lifts it about 1.4 blocks). */
    public static final double PULSE_UP = 0.12;
    /** Sideways speed a pulse gives, in blocks per tick. */
    public static final double PULSE_SIDE = 0.025;
    /** Ticks between pulses: at least this, plus up to {@link #PULSE_RANDOM_TICKS} more. */
    public static final int PULSE_MIN_TICKS = 30;
    public static final int PULSE_RANDOM_TICKS = 40;
    /** How long the bell's squash and stretch lasts after a pulse, in ticks (the model's animation). */
    public static final int PULSE_ANIMATION_TICKS = 16;
    /** Sinking between pulses: the pull per tick, and the water drag. Sinks at most about 0.2 blocks a second. */
    public static final double SINK = 0.0009;
    public static final double WATER_DRAG = 0.92;
    /** The sinking speed it starts from (vanilla stops anything slower than 0.003 blocks a tick). */
    public static final double SINK_START = 0.004;
    /** Where the bell's top likes to be, in blocks below the surface: {min, max}. */
    public static final double[] MAUVE_NIGHT_DEPTH = {0.4, 2.0};
    public static final double[] MAUVE_DAY_DEPTH = {4.0, 8.0};
    public static final double[] FRIED_EGG_DEPTH = {1.0, 5.0};
    /** The man o' war float: how deep its bottom sits in the water, and how fast it drifts (about 0.15 blocks a second). */
    public static final double FLOAT_DRAFT = 0.15;
    public static final double DRIFT_PUSH = 0.0008;
    /** How far up it looks for the surface, in blocks. */
    private static final int SURFACE_SCAN = 24;
    /** The entity event sent to players' clients on a pulse, so the bell's animation starts with it. */
    public static final byte PULSE_EVENT = 110;

    private static final EntityDataAccessor<Boolean> DATA_FLASHING = SynchedEntityData.defineId(Jellyfish.class, EntityDataSerializers.BOOLEAN);

    /** The three kinds, with what tells them apart. */
    public enum Kind {
        MAUVE_STINGER("mauve_stinger", true, true, false),
        FRIED_EGG("fried_egg_jellyfish", false, false, false),
        MAN_O_WAR("man_o_war", true, false, true);

        private final String id;
        private final boolean stings;
        private final boolean glows;
        private final boolean floats;

        Kind(String id, boolean stings, boolean glows, boolean floats) {
            this.id = id;
            this.stings = stings;
            this.glows = glows;
            this.floats = floats;
        }

        public String id() {
            return id;
        }

        public boolean stings() {
            return stings;
        }

        public boolean glows() {
            return glows;
        }

        public boolean floats() {
            return floats;
        }
    }

    private final Kind kind;
    private long nextSting;
    private int flashTicks;
    private int pulseCooldown;
    /** The way it drifts, in degrees (like an entity's yaw). */
    private float driftYaw;
    private int driftTimer;
    /** Client: the tick of the last pulse (for the animation), or a long time ago. */
    private int pulseTick = -1000;

    public Jellyfish(EntityType<? extends Jellyfish> type, Level level, Kind kind) {
        super(type, level);
        this.kind = kind;
        this.driftYaw = random.nextFloat() * 360.0F;
        this.pulseCooldown = random.nextInt(PULSE_MIN_TICKS + PULSE_RANDOM_TICKS);
    }

    public Kind kind() {
        return kind;
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(DATA_FLASHING, false);
    }

    /** True while a mauve stinger's flash shows (both sides: the renderer draws it full-bright). */
    public boolean isFlashing() {
        return entityData.get(DATA_FLASHING);
    }

    /** Client: 0 to 1 through the bell's squash and stretch after a pulse, or -1 when not pulsing. */
    public float pulseProgress(float partialTick) {
        float t = (tickCount - pulseTick + partialTick) / PULSE_ANIMATION_TICKS;
        return t >= 0.0F && t < 1.0F ? t : -1.0F;
    }

    // ---- moving ----

    /**
     * Sets this tick's speed, then moves. Done here rather than after aiStep, because LivingEntity.aiStep zeroes any
     * speed under 0.003 blocks a tick before it calls travel, which would stop the slow sinking.
     */
    @Override
    public void travel(Vec3 input) {
        if (isNoAi()) {
            // like vanilla's mobs with NoAI: it stays where it was put
            setDeltaMovement(Vec3.ZERO);
            return;
        }
        if (!level().isClientSide()) {
            steer();
        }
        move(MoverType.SELF, getDeltaMovement());
    }

    private void steer() {
        double top = waterTop();
        if (Double.isNaN(top) || !isInWater()) {
            // out of water: it falls and lies still (no flopping); WaterAnimal's drowning kills it slowly
            Vec3 v = getDeltaMovement();
            double slide = onGround() ? 0.5 : 0.98;
            setDeltaMovement(v.x * slide, (v.y - 0.08) * 0.98, v.z * slide);
        } else if (kind.floats()) {
            floatOn(top);
        } else {
            drift(top);
        }
    }

    /** The mauve stinger and fried-egg: sink slowly, and pulse up when they are deeper than they like. */
    private void drift(double top) {
        Vec3 v = getDeltaMovement();
        // vanilla zeroes speeds under 0.003 blocks a tick each tick, so the sink starts just above that and then builds
        double vy = Math.abs(v.y) < 0.003 ? -SINK_START : (v.y - SINK) * WATER_DRAG;
        setDeltaMovement(v.x * WATER_DRAG, vy, v.z * WATER_DRAG);
        if (--pulseCooldown > 0) {
            return;
        }
        pulseCooldown = PULSE_MIN_TICKS + random.nextInt(PULSE_RANDOM_TICKS);
        double depth = top - getBoundingBox().maxY;
        double[] range = preferredDepth();
        boolean up = depth > range[1] || (depth >= range[0] && random.nextFloat() < 0.4F);
        if (up && depth > 0.3) {
            driftYaw += (random.nextFloat() - 0.5F) * 60.0F;
            float yaw = driftYaw * Mth.DEG_TO_RAD;
            setDeltaMovement(getDeltaMovement().add(-Mth.sin(yaw) * PULSE_SIDE, PULSE_UP, Mth.cos(yaw) * PULSE_SIDE));
            level().broadcastEntityEvent(this, PULSE_EVENT);
        }
    }

    /** Where the bell's top likes to be, in blocks below the surface: the mauve stinger rises at night. */
    public double[] preferredDepth() {
        if (kind == Kind.MAUVE_STINGER) {
            return level().isDarkOutside() ? MAUVE_NIGHT_DEPTH : MAUVE_DAY_DEPTH;
        }
        return FRIED_EGG_DEPTH;
    }

    /** The man o' war: held at the surface, drifting slowly one way, now and then another. */
    private void floatOn(double top) {
        double vy = Mth.clamp((top - FLOAT_DRAFT - getY()) * 0.25, -0.06, 0.1);
        if (--driftTimer <= 0) {
            driftYaw += (random.nextFloat() - 0.5F) * 90.0F;
            driftTimer = 200 + random.nextInt(400);
        }
        float yaw = driftYaw * Mth.DEG_TO_RAD;
        Vec3 v = getDeltaMovement();
        setDeltaMovement(v.x * 0.9 - Mth.sin(yaw) * DRIFT_PUSH, vy, v.z * 0.9 + Mth.cos(yaw) * DRIFT_PUSH);
        // the float lies along the way it drifts
        setYRot(Mth.approachDegrees(getYRot(), driftYaw, 2.0F));
        yBodyRot = getYRot();
    }

    /**
     * The water's surface above it (the top of the water column it is in), or NaN if it isn't in water. Looks from
     * a little below its feet, so the man o' war (feet just under the surface) finds it too.
     */
    public double waterTop() {
        BlockPos.MutableBlockPos p = BlockPos.containing(getX(), getY() - 0.5 + (kind.floats() ? 0.0 : 0.5), getZ()).mutable();
        double top = Double.NaN;
        for (int i = 0; i < SURFACE_SCAN; i++) {
            FluidState fluid = level().getFluidState(p);
            if (!fluid.is(FluidTags.WATER)) {
                break;
            }
            top = p.getY() + fluid.getHeight(level(), p);
            p.move(Direction.UP);
        }
        return top;
    }

    // ---- stinging and the glow ----

    @Override
    public void tick() {
        super.tick();
        if (!(level() instanceof ServerLevel level) || !isAlive()) {
            return;
        }
        if (kind.stings() || kind.glows()) {
            List<LivingEntity> touching = level.getEntitiesOfClass(LivingEntity.class, touchBox(),
                e -> e != this && e.isAlive() && !e.isSpectator() && !(e instanceof Jellyfish) && !(e instanceof AbstractFish));
            if (!touching.isEmpty()) {
                if (kind.glows()) {
                    flash(level);
                }
                if (kind.stings() && level.getGameTime() >= nextSting) {
                    boolean stung = false;
                    for (LivingEntity target : touching) {
                        stung |= stingNow(level, target);
                    }
                    if (stung) {
                        nextSting = level.getGameTime() + STING_COOLDOWN;
                    }
                }
            }
        }
        if (kind.glows() && level.isRaining() && random.nextInt(RAIN_FLASH_CHANCE) == 0) {
            double top = waterTop();
            BlockPos sky = Double.isNaN(top) ? blockPosition() : BlockPos.containing(getX(), top + 0.5, getZ());
            if (level.isRainingAt(sky)) {
                flash(level);
            }
        }
        if (flashTicks > 0) {
            flashTicks--;
            if (flashTicks % 2 == 0) {
                glowParticles(level, 2);
            }
            if (flashTicks == 0) {
                entityData.set(DATA_FLASHING, false);
            }
        }
    }

    /** The box that stings when touched: its own box, and for the man o' war the column its tentacles hang in. */
    public AABB touchBox() {
        AABB box = getBoundingBox().inflate(TOUCH_MARGIN);
        return kind.floats() ? box.expandTowards(0.0, -MAN_O_WAR_TENTACLE_LENGTH, 0.0) : box;
    }

    /** The mauve stinger's flash: green glow particles, and full-bright, for {@link #FLASH_TICKS} ticks. */
    public void flash(ServerLevel level) {
        if (!kind.glows()) {
            return;
        }
        if (flashTicks == 0) {
            glowParticles(level, 10);
        }
        flashTicks = FLASH_TICKS;
        entityData.set(DATA_FLASHING, true);
    }

    private void glowParticles(ServerLevel level, int count) {
        double w = getBbWidth() * 0.4, h = getBbHeight() * 0.35;
        level.sendParticles(ParticleTypes.GLOW, getX(), getY() + getBbHeight() * 0.6, getZ(), count, w, h, w, 0.0);
    }

    /** Stings if the cooldown allows and the target can be stung; returns true if it stung. For the test, too. */
    public boolean sting(ServerLevel level, LivingEntity target) {
        if (!kind.stings() || level.getGameTime() < nextSting || !stingNow(level, target)) {
            return false;
        }
        nextSting = level.getGameTime() + STING_COOLDOWN;
        return true;
    }

    private boolean stingNow(ServerLevel level, LivingEntity target) {
        // Jellyfish Ward (the potion brewed from venom) blocks every jellyfish sting: damage, poison and nausea
        if (!Venom.canSting(target) || target.hasEffect(MimJellyfish.WARD)) {
            return false;
        }
        if (kind == Kind.MAN_O_WAR) {
            Venom.stingGently(level, this, target, MAN_O_WAR_STING_DAMAGE,
                new MobEffectInstance(MobEffects.POISON, MAN_O_WAR_POISON_SECONDS * 20, 0),
                new MobEffectInstance(MobEffects.NAUSEA, MAN_O_WAR_NAUSEA_SECONDS * 20, 0));
        } else {
            Venom.stingGently(level, this, target, MAUVE_STING_DAMAGE, new MobEffectInstance(MobEffects.POISON, MAUVE_POISON_SECONDS * 20, 0));
        }
        return true;
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float damage) {
        boolean hurt = super.hurtServer(level, source, damage);
        if (hurt && isAlive()) {
            flash(level);
            // hitting it in melee is touching it (arrows and thrown tridents don't count)
            Entity attacker = source.getEntity();
            if (attacker instanceof LivingEntity living && source.getDirectEntity() == attacker && distanceTo(attacker) <= MELEE_STING_RANGE) {
                sting(level, living);
            }
        }
        return hurt;
    }

    @Override
    public void handleEntityEvent(byte id) {
        if (id == PULSE_EVENT) {
            pulseTick = tickCount;
        } else {
            super.handleEntityEvent(id);
        }
    }

    // ---- sounds: quiet and squishy ----

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.SLIME_HURT_SMALL;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.SLIME_DEATH_SMALL;
    }

    @Override
    protected float getSoundVolume() {
        return 0.4F;
    }
}
