package com.maltaminecraft.mimcontent.client;

import com.maltaminecraft.mimcontent.MimContent;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.Model;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.AbstractBoatRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.state.BoatRenderState;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.util.Unit;

/** Draws a luzzu with the shared model and its scheme's texture, and keeps the sea out of its hull like vanilla. */
public class LuzzuRenderer extends AbstractBoatRenderer {
    public static final ModelLayerLocation LAYER = new ModelLayerLocation(MimContent.id("boat/luzzu"), "main");
    public static final ModelLayerLocation WATER_PATCH = new ModelLayerLocation(MimContent.id("boat/luzzu"), "water_patch");

    private final EntityModel<BoatRenderState> model;
    private final Model.Simple waterPatch;

    public LuzzuRenderer(EntityRendererProvider.Context context, String scheme) {
        super(context, MimContent.id("textures/entity/boat/" + scheme + ".png"));
        this.model = new LuzzuModel(context.bakeLayer(LAYER));
        this.waterPatch = new Model.Simple(context.bakeLayer(WATER_PATCH), t -> RenderTypes.waterMask());
    }

    @Override
    protected EntityModel<BoatRenderState> model() {
        return model;
    }

    @Override
    protected void submitTypeAdditions(BoatRenderState state, PoseStack poseStack, SubmitNodeCollector collector, int lightCoords) {
        if (!state.isUnderWater) {
            collector.submitModel(waterPatch, Unit.INSTANCE, poseStack, texture, lightCoords, OverlayTexture.NO_OVERLAY, state.outlineColor);
        }
    }
}
