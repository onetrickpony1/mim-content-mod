package com.maltaminecraft.mimcontent.mixin.fish;

import com.maltaminecraft.mimcontent.entity.fish.FishPart;
import com.maltaminecraft.mimcontent.entity.fish.FishParts;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Fish hit boxes: when a player hits or uses a fish part, the client names the part's id (the fish's id + 1, + 2,
 * ...). Vanilla looks such ids up only among the dragon's parts; this also finds a fish part, through its fish. The
 * server then checks the player's reach against that part's box, as it does for the dragon.
 */
@Mixin(ServerLevel.class)
public abstract class ServerLevelMixin {
    @Inject(method = "getEntityOrPart", at = @At("RETURN"), cancellable = true)
    private void mimcontent$fishPart(int id, CallbackInfoReturnable<Entity> cir) {
        if (cir.getReturnValue() != null) {
            return;
        }
        ServerLevel level = (ServerLevel) (Object) this;
        for (int k = 1; k <= com.maltaminecraft.mimcontent.entity.fish.FishShape.MAX_PARTS; k++) {
            if (level.getEntity(id - k) instanceof FishParts.Holder holder && holder.mimcontent$parts() != null) {
                FishPart[] parts = holder.mimcontent$parts().parts();
                if (k <= parts.length && parts[k - 1].getId() == id) {
                    cir.setReturnValue(parts[k - 1]);
                }
                return;
            }
        }
    }
}
