package com.maltaminecraft.mimcontent.mixin.fish;

import com.maltaminecraft.mimcontent.entity.fish.FishParts;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

/**
 * Fish hit boxes: hitting or using a fish part (FishPart) acts on the fish itself, so a hit on the tail is a hit on
 * the fish in every way (damage, knockback, enchantments, sweeping, crits, stats), and a water bucket, a lead or a
 * name tag used on any part works as on the fish. The reach was already checked against the part's box. Both sides.
 */
@Mixin(Player.class)
public abstract class PlayerMixin {
    @ModifyVariable(method = "attack", at = @At("HEAD"), argsOnly = true)
    private Entity mimcontent$attackFish(Entity entity) {
        return FishParts.owner(entity);
    }

    @ModifyVariable(method = "interactOn", at = @At("HEAD"), argsOnly = true)
    private Entity mimcontent$useOnFish(Entity entity) {
        return FishParts.owner(entity);
    }
}
