package com.maltaminecraft.mimcontent.mixin.client;

import com.maltaminecraft.mimcontent.client.LuzzuBenchPose;
import net.minecraft.client.renderer.entity.state.AvatarRenderState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;

/** Gives a player's render state the "riding a luzzu" and "at its helm" flags. */
@Mixin(AvatarRenderState.class)
public abstract class AvatarRenderStateMixin implements LuzzuBenchPose {
    @Unique
    private boolean mimcontent$onLuzzu;

    @Unique
    private boolean mimcontent$atHelm;

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
