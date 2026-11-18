package com.maltaminecraft.mimcontent.entity.fish;

import com.maltaminecraft.mimcontent.MimContent;
import java.util.function.Supplier;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.TagKey;
import net.minecraft.util.TimeUtil;
import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.Difficulty;
import net.minecraft.world.entity.EntityReference;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.NeutralMob;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomSwimmingGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.ai.goal.target.ResetUniversalAngerTargetGoal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import org.jspecify.annotations.Nullable;

/**
 * The ħuta kaħla (blue shark). Neutral, like vanilla's polar bear (owner 2026-11-18: "blue shark should ignore you
 * unless you hurt it OR you have fish in your inventory"):
 * <ul>
 * <li>It doesn't shy away from players, and leaves them alone.</li>
 * <li>Hurt it and it bites back for 15 to 25 seconds, then calms down.</li>
 * <li>A player within 16 blocks (survival or adventure, not on peaceful) carrying anything in the item tag
 *     {@code mimcontent:shark_bait} (vanilla's fish, our fish, fish buckets) is hunted. The inventory is looked at
 *     about once a second. Once the bait is gone it gives up after 3 seconds, unless it was also hurt.</li>
 * </ul>
 */
public class HutaKahlaFish extends MimFish implements NeutralMob {
    public static final TagKey<Item> BAIT = TagKey.create(Registries.ITEM, MimContent.id("shark_bait"));
    private static final UniformInt ANGER_TIME = TimeUtil.rangeOfSeconds(15, 25);
    /** How long it keeps after a player who no longer carries bait, in ticks. */
    private static final int GIVE_UP_TICKS = 60;

    private long angerEndTime = NO_ANGER_END_TIME;
    private @Nullable EntityReference<LivingEntity> angerTarget;
    /** True while the bait goal holds the target: that chase is not anger, so it isn't remembered as anger. */
    private boolean chasingBait;

    public HutaKahlaFish(EntityType<? extends MimFish> type, Level level, Supplier<Item> bucket, int spawnCluster) {
        super(type, level, bucket, spawnCluster);
    }

    /** True if this is a player the shark may hunt for the fish they carry. */
    public static boolean carriesBait(LivingEntity entity) {
        return entity instanceof Player player && !player.isCreative() && !player.isSpectator()
            && player.level().getDifficulty() != Difficulty.PEACEFUL && player.getInventory().contains(BAIT);
    }

    public boolean isChasingBait() {
        return chasingBait;
    }

    @Override
    protected void registerGoals() {
        // not vanilla fish's goals: no panic and no shying from players
        this.goalSelector.addGoal(1, new MeleeAttackGoal(this, 1.3, true));
        this.goalSelector.addGoal(4, new RandomSwimmingGoal(this, 1.0, 40) {
            @Override
            public boolean canUse() {
                return HutaKahlaFish.this.canRandomSwim() && super.canUse();
            }
        });
        this.targetSelector.addGoal(1, new HurtByTargetGoal(this));
        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, 10, true, false, this::isAngryAt));
        this.targetSelector.addGoal(3, new BaitGoal());
        this.targetSelector.addGoal(4, new ResetUniversalAngerTargetGoal<>(this, false));
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (!level().isClientSide() && !chasingBait) {
            updatePersistentAnger((ServerLevel) level(), false);
        }
    }

    @Override
    protected void addAdditionalSaveData(ValueOutput output) {
        super.addAdditionalSaveData(output);
        addPersistentAngerSaveData(output);
    }

    @Override
    protected void readAdditionalSaveData(ValueInput input) {
        super.readAdditionalSaveData(input);
        readPersistentAngerSaveData(level(), input);
    }

    @Override
    public void startPersistentAngerTimer() {
        setTimeToRemainAngry(ANGER_TIME.sample(this.random));
    }

    @Override
    public long getPersistentAngerEndTime() {
        return angerEndTime;
    }

    @Override
    public void setPersistentAngerEndTime(long endTime) {
        this.angerEndTime = endTime;
    }

    @Override
    public @Nullable EntityReference<LivingEntity> getPersistentAngerTarget() {
        return angerTarget;
    }

    @Override
    public void setPersistentAngerTarget(@Nullable EntityReference<LivingEntity> target) {
        this.angerTarget = target;
    }

    /** Hunts the nearest player carrying bait; looks about once a second, gives up a while after the bait is gone. */
    private class BaitGoal extends NearestAttackableTargetGoal<Player> {
        private long nextCheck;
        private long baitGoneSince = -1;

        BaitGoal() {
            super(HutaKahlaFish.this, Player.class, 20, true, false, (target, level) -> carriesBait(target));
        }

        @Override
        public void start() {
            super.start();
            chasingBait = true;
            baitGoneSince = -1;
            nextCheck = level().getGameTime() + 20;
        }

        @Override
        public boolean canContinueToUse() {
            if (!super.canContinueToUse()) {
                return false;
            }
            long now = level().getGameTime();
            if (now >= nextCheck) {
                nextCheck = now + 20;
                LivingEntity target = mob.getTarget();
                if (target != null && carriesBait(target)) {
                    baitGoneSince = -1;
                } else if (baitGoneSince < 0) {
                    baitGoneSince = now;
                }
            }
            return baitGoneSince < 0 || now - baitGoneSince < GIVE_UP_TICKS;
        }

        @Override
        public void stop() {
            super.stop();
            chasingBait = false;
        }
    }
}
