package com.maltaminecraft.mimcontent.test.mixin;

import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.GameRenderer;
import net.minecraft.gizmos.Gizmos;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Test only (never in the mod's jar): lets the game test's screenshots show debug boxes (F3+B). Fabric's screenshot
 * draws its frame from inside a client task, where debug boxes go to the per-tick collection and only appear in a
 * later frame; this sends the boxes of each drawn frame to that frame, as a normal frame does.
 */
@Mixin(GameRenderer.class)
public abstract class GameRendererGizmoMixin {
    @Unique
    private Gizmos.TemporaryCollection mimsmoke$gizmos;

    @Inject(method = "extract", at = @At("HEAD"))
    private void mimsmoke$collect(DeltaTracker deltaTracker, boolean advanceGameTime, CallbackInfo ci) {
        mimsmoke$gizmos = Minecraft.getInstance().levelExtractor.collectPerFrameMainThreadGizmos();
    }

    @Inject(method = "extract", at = @At("RETURN"))
    private void mimsmoke$done(DeltaTracker deltaTracker, boolean advanceGameTime, CallbackInfo ci) {
        if (mimsmoke$gizmos != null) {
            mimsmoke$gizmos.close();
            mimsmoke$gizmos = null;
        }
    }
}
