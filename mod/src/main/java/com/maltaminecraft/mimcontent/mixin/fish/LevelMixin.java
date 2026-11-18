package com.maltaminecraft.mimcontent.mixin.fish;

import com.maltaminecraft.mimcontent.entity.fish.FishPart;
import com.maltaminecraft.mimcontent.entity.fish.FishParts;
import java.util.List;
import java.util.function.Predicate;
import net.minecraft.util.Continuation;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.entity.EntityTypeTest;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.entity.LevelEntityGetter;
import net.minecraft.world.phys.AABB;
import org.jspecify.annotations.Nullable;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Fish hit boxes: the level's "entities in this box" search (the one that crosshair picking, arrows, tridents and the
 * fishing bobber use) also finds the boxes of our fish's chains (FishParts), as vanilla does for the ender dragon's
 * parts. Vanilla's list of dragon parts is hard-coded to the dragon, so the parts are found through their fish: a
 * second search, widened by how far a part can reach past its fish, for our fish only. Both sides (client picking,
 * server projectiles).
 */
@Mixin(Level.class)
public abstract class LevelMixin {
    @Shadow
    protected abstract LevelEntityGetter<Entity> getEntities();

    @Inject(method = "getEntities(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/phys/AABB;Ljava/util/function/Predicate;)Ljava/util/List;",
        at = @At("RETURN"))
    private void mimcontent$fishParts(@Nullable Entity except, AABB bb, Predicate<? super Entity> selector, CallbackInfoReturnable<List<Entity>> cir) {
        List<Entity> output = cir.getReturnValue();
        getEntities().get(EntityTypeTest.forClass(AbstractFish.class), bb.inflate(FishParts.reach()), fish -> {
            if (fish != except && fish instanceof FishParts.Holder holder && holder.mimcontent$parts() != null) {
                for (FishPart part : holder.mimcontent$parts().parts()) {
                    if (part != except && bb.intersects(part.getBoundingBox()) && selector.test(part)) {
                        output.add(part);
                    }
                }
            }
            return Continuation.CONTINUE;
        });
    }
}
