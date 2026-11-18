package com.maltaminecraft.mimcontent.mixin.client;

import com.maltaminecraft.mimcontent.client.LuzzuBenchPose;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.entity.state.HumanoidRenderState;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Players (and mannequins) riding a luzzu sit on a thwart: legs down and forward to the floorboards, not straight out like in a
 * vanilla boat, so their feet stay inside the hull. Only the helmsman reaches forward to row; the crew rest their
 * hands on their thighs. Only players in a luzzu; everyone else keeps vanilla's pose.
 * Leg armour and trousers follow the legs as usual.
 */
@Mixin(HumanoidModel.class)
public abstract class HumanoidModelMixin {
    @Shadow
    @Final
    public ModelPart rightLeg;
    @Shadow
    @Final
    public ModelPart leftLeg;
    @Shadow
    @Final
    public ModelPart rightArm;
    @Shadow
    @Final
    public ModelPart leftArm;

    @Inject(method = "setupAnim(Lnet/minecraft/client/renderer/entity/state/HumanoidRenderState;)V", at = @At("TAIL"))
    private void mimcontent$sitOnThwart(HumanoidRenderState state, CallbackInfo ci) {
        if (state.isPassenger && state instanceof LuzzuBenchPose bench && bench.mimcontent$onLuzzu()) {
            rightLeg.xRot = LuzzuBenchPose.LEG_X_ROT;
            rightLeg.yRot = LuzzuBenchPose.LEG_Y_ROT;
            rightLeg.zRot = LuzzuBenchPose.LEG_Z_ROT;
            leftLeg.xRot = LuzzuBenchPose.LEG_X_ROT;
            leftLeg.yRot = -LuzzuBenchPose.LEG_Y_ROT;
            leftLeg.zRot = -LuzzuBenchPose.LEG_Z_ROT;
            if (!bench.mimcontent$atHelm()) {
                // only the helmsman reaches for the oars; the crew rest their hands on their thighs (item poses and
                // swings still add on top, as vanilla's riding reach would)
                float rest = LuzzuBenchPose.RESTING_ARM - LuzzuBenchPose.VANILLA_RIDING_ARM;
                rightArm.xRot += rest;
                leftArm.xRot += rest;
            }
        }
    }
}
