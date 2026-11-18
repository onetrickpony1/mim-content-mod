package com.maltaminecraft.mimcontent.entity.fish;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.Difficulty;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;

/**
 * The sting of a venomous fish (the boll's tail spine, the skorfna's fin spines): damage from the fish and Poison.
 * Who can be stung is the same for every venomous fish: a living target, not a creative or spectator player, and not
 * on peaceful difficulty. Each fish keeps its own numbers and cooldown.
 */
public final class Venom {
    private Venom() {
    }

    /** True if this one may be stung: alive, not a creative or spectator player, and not on peaceful difficulty. */
    public static boolean canSting(Entity target) {
        if (!(target instanceof LivingEntity living) || !living.isAlive() || target.level().getDifficulty() == Difficulty.PEACEFUL) {
            return false;
        }
        return !(target instanceof Player player) || (!player.isCreative() && !player.isSpectator());
    }

    /** The sting itself: damage from the fish, then Poison (level I) for the given seconds. */
    public static void strike(ServerLevel level, Mob fish, LivingEntity target, float damage, int poisonSeconds) {
        target.hurtServer(level, fish.damageSources().mobAttack(fish), damage);
        target.addEffect(new MobEffectInstance(MobEffects.POISON, poisonSeconds * 20, 0), fish);
    }

    /** A gentle sting (the jellyfish) never takes its target below this health: 2 = 1 heart. */
    public static final float LOWEST_HEALTH_AFTER_GENTLE_STING = 2.0F;

    /**
     * A sting that is never deadly (the jellyfish): damage from the stinger, but never taking the target below
     * {@link #LOWEST_HEALTH_AFTER_GENTLE_STING}, then the given effects. (Poison on its own never kills, as in vanilla.)
     */
    public static void stingGently(ServerLevel level, Mob stinger, LivingEntity target, float damage, MobEffectInstance... effects) {
        float allowed = Math.min(damage, target.getHealth() - LOWEST_HEALTH_AFTER_GENTLE_STING);
        if (allowed > 0.0F) {
            target.hurtServer(level, stinger.damageSources().mobAttack(stinger), allowed);
        }
        for (MobEffectInstance effect : effects) {
            target.addEffect(new MobEffectInstance(effect), stinger);
        }
    }
}
