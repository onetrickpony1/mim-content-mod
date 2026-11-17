package com.maltaminecraft.mimcontent.mixin.client;

import com.maltaminecraft.mimcontent.entity.LuzzuBoat;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.MultiPlayerGameMode;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Riding a luzzu whose fish hold is switched off, the inventory key opens the player's own inventory, as in a
 * vanilla boat (the luzzu always has the chest-boat interface, so without this the key would ask the server for
 * the hold). Touches nothing else: every other vehicle goes through vanilla's check.
 */
@Mixin(MultiPlayerGameMode.class)
public abstract class MultiPlayerGameModeMixin {
    @Shadow
    @Final
    private Minecraft minecraft;

    @Inject(method = "isServerControlledInventory", at = @At("HEAD"), cancellable = true)
    private void mimcontent$luzzuWithoutHold(CallbackInfoReturnable<Boolean> cir) {
        if (minecraft.player != null && minecraft.player.getVehicle() instanceof LuzzuBoat luzzu && !luzzu.hasFishHold()) {
            cir.setReturnValue(false);
        }
    }
}
