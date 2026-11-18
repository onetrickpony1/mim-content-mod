package com.maltaminecraft.mimcontent.mixin.fish;

import com.maltaminecraft.mimcontent.entity.fish.FishPart;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.HitResult;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

/**
 * Fish hit boxes: an arrow, trident, snowball or fishing bobber that strikes a fish part (FishPart) strikes the fish,
 * at the same spot, so it is hurt, knocked back or hooked exactly as if it had hit the fish's own box.
 */
@Mixin(Projectile.class)
public abstract class ProjectileMixin {
    @ModifyVariable(method = "onHit", at = @At("HEAD"), argsOnly = true)
    private HitResult mimcontent$hitFish(HitResult hit) {
        if (hit instanceof EntityHitResult entityHit && entityHit.getEntity() instanceof FishPart part) {
            return new EntityHitResult(part.fish, hit.getLocation());
        }
        return hit;
    }
}
