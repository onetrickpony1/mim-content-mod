package com.maltaminecraft.mimcontent.mixin.client;

import com.maltaminecraft.mimcontent.client.LuzzuBenchPose;
import com.maltaminecraft.mimcontent.client.LuzzuOars;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.entity.state.HumanoidRenderState;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Players (and mannequins) riding a luzzu sit on a thwart: legs down and forward to the floorboards, not straight out like in a
 * vanilla boat, so their feet stay inside the hull. The helmsman's hands hold the oars through the stroke (each arm
 * aimed at its oar's grip, see LuzzuOars) and rest on the thighs while an oar isn't rowing; the crew rest their
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

    @Unique
    private static void mimcontent$holdOar(ModelPart arm, org.joml.Vector3f grip, float across, float rest) {
        if (grip == null) {
            arm.xRot += rest;
            return;
        }
        float[] pose = LuzzuOars.armPose(grip, arm.x, arm.y, arm.z, across);
        arm.xRot = pose[0];
        arm.yRot = pose[1];
        arm.zRot = 0.0F;
        arm.z = pose[2];
    }

    @Inject(method = "setupAnim(Lnet/minecraft/client/renderer/entity/state/HumanoidRenderState;)V", at = @At("TAIL"))
    private void mimcontent$sitOnThwart(HumanoidRenderState state, CallbackInfo ci) {
        if (state.isPassenger && state instanceof LuzzuBenchPose bench && bench.mimcontent$onLuzzu()) {
            rightLeg.xRot = LuzzuBenchPose.LEG_X_ROT;
            rightLeg.yRot = LuzzuBenchPose.LEG_Y_ROT;
            rightLeg.zRot = LuzzuBenchPose.LEG_Z_ROT;
            leftLeg.xRot = LuzzuBenchPose.LEG_X_ROT;
            leftLeg.yRot = -LuzzuBenchPose.LEG_Y_ROT;
            leftLeg.zRot = -LuzzuBenchPose.LEG_Z_ROT;
            float rest = LuzzuBenchPose.RESTING_ARM - LuzzuBenchPose.VANILLA_RIDING_ARM;
            if (!bench.mimcontent$atHelm()) {
                // only the helmsman reaches for the oars; the crew rest their hands on their thighs (item poses and
                // swings still add on top, as vanilla's riding reach would)
                rightArm.xRot += rest;
                leftArm.xRot += rest;
                return;
            }
            // the helmsman: each hand holds its oar while it rows (LuzzuOars), and rests on the thigh while it
            // doesn't, rather than reaching for an oar that isn't out
            float across = bench.mimcontent$slimArms() ? 0.5F : 1.0F;
            mimcontent$holdOar(leftArm, bench.mimcontent$grip(0), across, rest);
            mimcontent$holdOar(rightArm, bench.mimcontent$grip(1), -across, rest);
        }
    }
}
