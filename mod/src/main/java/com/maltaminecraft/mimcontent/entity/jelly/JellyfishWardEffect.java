package com.maltaminecraft.mimcontent.entity.jelly;

import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;

/**
 * Jellyfish Ward: while active, no jellyfish can sting (no damage, poison or nausea). It does nothing by itself;
 * {@link Jellyfish} checks for it before stinging. The boll's and skorfna's stings are not blocked (an open question
 * for the owner).
 */
public class JellyfishWardEffect extends MobEffect {
    /** A pale sea blue. */
    public static final int COLOUR = 0x8FD3E8;

    public JellyfishWardEffect() {
        super(MobEffectCategory.BENEFICIAL, COLOUR);
    }
}
