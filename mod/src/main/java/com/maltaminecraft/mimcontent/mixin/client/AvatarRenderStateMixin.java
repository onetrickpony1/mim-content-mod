package com.maltaminecraft.mimcontent.mixin.client;

import com.maltaminecraft.mimcontent.client.LuzzuBenchPose;
import net.minecraft.client.renderer.entity.state.AvatarRenderState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;

/** Gives a player's render state the "riding a luzzu" and "at its helm" flags, and the helmsman's grips on the oars. */
@Mixin(AvatarRenderState.class)
public abstract class AvatarRenderStateMixin implements LuzzuBenchPose {
    @Unique
    private boolean mimcontent$onLuzzu;

    @Unique
    private boolean mimcontent$atHelm;

    @Unique
    private final org.joml.Vector3f[] mimcontent$grips = new org.joml.Vector3f[2];

    @Unique
    private boolean mimcontent$slim;

    @Override
    public org.joml.Vector3f mimcontent$grip(int side) {
        return mimcontent$grips[side];
    }

    @Override
    public void mimcontent$setGrip(int side, org.joml.Vector3f grip) {
        mimcontent$grips[side] = grip;
    }

    @Override
    public boolean mimcontent$slimArms() {
        return mimcontent$slim;
    }

    @Override
    public void mimcontent$setSlimArms(boolean slim) {
        this.mimcontent$slim = slim;
    }

    @Override
    public boolean mimcontent$atHelm() {
        return mimcontent$atHelm;
    }

    @Override
    public void mimcontent$setAtHelm(boolean atHelm) {
        this.mimcontent$atHelm = atHelm;
    }

    @Override
    public boolean mimcontent$onLuzzu() {
        return mimcontent$onLuzzu;
    }

    @Override
    public void mimcontent$setOnLuzzu(boolean onLuzzu) {
        this.mimcontent$onLuzzu = onLuzzu;
    }
}
