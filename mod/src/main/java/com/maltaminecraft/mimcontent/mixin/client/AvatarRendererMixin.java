package com.maltaminecraft.mimcontent.mixin.client;

import com.maltaminecraft.mimcontent.client.LuzzuBenchPose;
import com.maltaminecraft.mimcontent.entity.LuzzuBoat;
import net.minecraft.client.renderer.entity.player.AvatarRenderer;
import net.minecraft.client.renderer.entity.state.AvatarRenderState;
import net.minecraft.world.entity.Entity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Marks a player's render state when the player rides a luzzu, and whether at its helm. */
@Mixin(AvatarRenderer.class)
public abstract class AvatarRendererMixin {
    @Inject(method = "extractRenderState(Lnet/minecraft/world/entity/Avatar;Lnet/minecraft/client/renderer/entity/state/AvatarRenderState;F)V", at = @At("TAIL"))
    private void mimcontent$markLuzzuRider(net.minecraft.world.entity.Avatar entity, AvatarRenderState state, float partialTicks, CallbackInfo ci) {
        Entity rider = (Entity) entity;
        LuzzuBenchPose bench = (LuzzuBenchPose) state;
        boolean onLuzzu = rider.getVehicle() instanceof LuzzuBoat;
        bench.mimcontent$setOnLuzzu(onLuzzu);
        bench.mimcontent$setAtHelm(onLuzzu && ((LuzzuBoat) rider.getVehicle()).isAtHelm(rider));
    }
}
