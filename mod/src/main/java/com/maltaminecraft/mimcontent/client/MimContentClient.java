package com.maltaminecraft.mimcontent.client;

import com.maltaminecraft.mimcontent.MimContent;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.ModelLayerRegistry;
import net.minecraft.client.renderer.entity.EntityRenderers;

/** Client entrypoint: the luzzu's model and its renderers, one per colour scheme. */
public class MimContentClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        ModelLayerRegistry.registerModelLayer(LuzzuRenderer.LAYER, LuzzuModel::createBodyLayer);
        ModelLayerRegistry.registerModelLayer(LuzzuRenderer.WATER_PATCH, LuzzuModel::createWaterPatch);
        EntityRenderers.register(MimContent.LUZZU, context -> new LuzzuRenderer(context, "luzzu"));
        EntityRenderers.register(MimContent.LUZZU_RED, context -> new LuzzuRenderer(context, "luzzu_red"));
        EntityRenderers.register(MimContent.LUZZU_BROWN, context -> new LuzzuRenderer(context, "luzzu_brown"));
    }
}
