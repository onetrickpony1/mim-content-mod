package com.maltaminecraft.mimcontent.test.mixin;

import com.maltaminecraft.mimcontent.entity.LuzzuBoat;
import com.maltaminecraft.mimcontent.test.LuzzuOarsCheck;
import net.minecraft.world.entity.vehicle.boat.AbstractBoat;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Test only (never in the mod's jar): holds a luzzu's rowing oars at one point of the stroke, so the oar check can
 * measure and photograph that moment. Only a luzzu, only an oar that is rowing; vanilla boats are left alone.
 */
@Mixin(AbstractBoat.class)
public abstract class LuzzuRowingPhaseMixin {
    @Inject(method = "getRowingTime", at = @At("HEAD"), cancellable = true)
    private void mimsmoke$hold(int side, float partialTicks, CallbackInfoReturnable<Float> cir) {
        AbstractBoat self = (AbstractBoat) (Object) this;
        float held = LuzzuOarsCheck.heldPhase;
        if (!Float.isNaN(held) && self instanceof LuzzuBoat && self.getPaddleState(side)) {
            cir.setReturnValue(held);
        }
    }
}
