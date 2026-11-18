package com.maltaminecraft.mimcontent.mixin.client;

import com.maltaminecraft.mimcontent.client.LuzzuBenchPose;
import com.maltaminecraft.mimcontent.client.LuzzuOars;
import com.maltaminecraft.mimcontent.entity.LuzzuBoat;
import net.minecraft.client.renderer.entity.player.AvatarRenderer;
import net.minecraft.client.renderer.entity.state.AvatarRenderState;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.PlayerModelType;
import org.joml.Matrix4f;
import org.joml.Vector3f;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Marks a player's render state when the player rides a luzzu, and whether at its helm. For the helmsman it also
 * works out where each rowing oar's grip is, in the player model's own pixels, from the boat's and the rider's drawn
 * positions, so the arms can be aimed at it (HumanoidModelMixin).
 */
@Mixin(AvatarRenderer.class)
public abstract class AvatarRendererMixin {
    @Inject(method = "extractRenderState(Lnet/minecraft/world/entity/Avatar;Lnet/minecraft/client/renderer/entity/state/AvatarRenderState;F)V", at = @At("TAIL"))
    private void mimcontent$markLuzzuRider(net.minecraft.world.entity.Avatar entity, AvatarRenderState state, float partialTicks, CallbackInfo ci) {
        Entity rider = (Entity) entity;
        LuzzuBenchPose bench = (LuzzuBenchPose) state;
        boolean onLuzzu = rider.getVehicle() instanceof LuzzuBoat;
        boolean atHelm = onLuzzu && ((LuzzuBoat) rider.getVehicle()).isAtHelm(rider);
        bench.mimcontent$setOnLuzzu(onLuzzu);
        bench.mimcontent$setAtHelm(atHelm);
        bench.mimcontent$setSlimArms(state.skin.model() == PlayerModelType.SLIM);
        for (int side = 0; side < 2; side++) {
            Vector3f grip = null;
            if (atHelm) {
                LuzzuBoat boat = (LuzzuBoat) rider.getVehicle();
                if (boat.getPaddleState(side)) {
                    grip = mimcontent$gripInPlayerModel(boat, side, state, partialTicks);
                }
            }
            bench.mimcontent$setGrip(side, grip);
        }
    }

    /** The oar's grip (LuzzuOars), from the boat model to the world to this player's model, both as drawn. */
    private static Vector3f mimcontent$gripInPlayerModel(LuzzuBoat boat, int side, AvatarRenderState state, float partialTicks) {
        float yRot = boat.getYRot(partialTicks);
        LuzzuOars.Pose pose = LuzzuOars.pose(boat.getRowingTime(side, partialTicks), side, boat.helmPlace());
        Vector3f grip = LuzzuOars.boatModelToWorld(yRot).transformPosition(LuzzuOars.gripInModel(pose));
        // from the boat's drawn position to the rider's
        grip.add((float) (Mth.lerp(partialTicks, boat.xOld, boat.getX()) - state.x),
            (float) (Mth.lerp(partialTicks, boat.yOld, boat.getY()) - state.y),
            (float) (Mth.lerp(partialTicks, boat.zOld, boat.getZ()) - state.z));
        Matrix4f toModel = LuzzuOars.playerModelToWorld(state.bodyRot, state.scale).invert();
        return toModel.transformPosition(grip);
    }
}
