package com.maltaminecraft.mimcontent.mixin.client;

import com.maltaminecraft.mimcontent.entity.fish.FishPart;
import com.maltaminecraft.mimcontent.entity.fish.FishParts;
import net.minecraft.client.renderer.debug.EntityHitboxDebugRenderer;
import net.minecraft.gizmos.GizmoStyle;
import net.minecraft.gizmos.Gizmos;
import net.minecraft.util.ARGB;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.phys.Vec3;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Fish hit boxes: with hit boxes shown (F3+B) our fish's chain of boxes is drawn too, in the colour vanilla uses for
 * the ender dragon's parts, beside the fish's own white box (which is only for moving, not for hitting).
 */
@Mixin(EntityHitboxDebugRenderer.class)
public abstract class EntityHitboxDebugRendererMixin {
    @Inject(method = "showHitboxes", at = @At("TAIL"))
    private void mimcontent$fishParts(Entity entity, float partialTicks, boolean isServerEntity, CallbackInfo ci) {
        if (!isServerEntity && entity instanceof FishParts.Holder holder && holder.mimcontent$parts() != null) {
            for (FishPart part : holder.mimcontent$parts().parts()) {
                Vec3 offset = part.getPosition(partialTicks).subtract(part.position());
                Gizmos.cuboid(part.getBoundingBox().move(offset), GizmoStyle.stroke(ARGB.colorFromFloat(1.0F, 0.25F, 1.0F, 0.0F)));
            }
        }
    }
}
