package com.maltaminecraft.mimcontent.client.jelly;

import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;

/** What a jellyfish model needs to animate, beside vanilla's (age, in water, ...). */
public class JellyfishRenderState extends LivingEntityRenderState {
    /** 0 to 1 through the bell's squash and stretch after a pulse, or -1 between pulses. */
    public float pulse = -1.0F;
    /** True for the man o' war: its float bobs and tilts on the surface instead of pulsing. */
    public boolean floats;
    /** True while a mauve stinger's flash shows (drawn full-bright). */
    public boolean flashing;
}
