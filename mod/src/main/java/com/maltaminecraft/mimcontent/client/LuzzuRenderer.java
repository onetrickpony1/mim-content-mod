package com.maltaminecraft.mimcontent.client;

import com.maltaminecraft.mimcontent.MimContent;
import com.maltaminecraft.mimcontent.entity.LuzzuBoat;
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
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.world.entity.vehicle.boat.AbstractBoat;
import net.minecraft.util.Unit;

/**
 * Draws a luzzu with the shared model and its scheme's texture, and keeps the sea out of its hull like vanilla.
 * Each oar shows only while it is rowing (owner, 2026-11-17): a still boat lies with its oars shipped out of sight.
 * The oars turn on thole pins beside the helm and follow {@link LuzzuOars}, so the rower's hands stay on them
 * (owner, 2026-11-18).
 */
public class LuzzuRenderer extends AbstractBoatRenderer {
    public static final ModelLayerLocation LAYER = new ModelLayerLocation(MimContent.id("boat/luzzu"), "main");
    public static final ModelLayerLocation WATER_PATCH = new ModelLayerLocation(MimContent.id("boat/luzzu"), "water_patch");

    private final EntityModel<BoatRenderState> model;
    private final Model.Simple waterPatch;

    public LuzzuRenderer(EntityRendererProvider.Context context, String scheme) {
        super(context, MimContent.id("textures/entity/boat/" + scheme + ".png"));
        this.model = new OarsWhenRowing(context.bakeLayer(LAYER));
        this.waterPatch = new Model.Simple(context.bakeLayer(WATER_PATCH), t -> RenderTypes.waterMask());
    }

    @Override
    protected EntityModel<BoatRenderState> model() {
        return model;
    }

    /** The luzzu model (for the in-game checks, which pose it to measure the oars). */
    public EntityModel<BoatRenderState> luzzuModel() {
        return model;
    }

    @Override
    protected void submitTypeAdditions(BoatRenderState state, PoseStack poseStack, SubmitNodeCollector collector, int lightCoords) {
        if (!state.isUnderWater) {
            collector.submitModel(waterPatch, Unit.INSTANCE, poseStack, texture, lightCoords, OverlayTexture.NO_OVERLAY, state.outlineColor);
        }
    }

    @Override
    public BoatRenderState createRenderState() {
        return new LuzzuRenderState();
    }

    @Override
    public void extractRenderState(AbstractBoat entity, BoatRenderState state, float partialTicks) {
        super.extractRenderState(entity, state, partialTicks);
        if (state instanceof LuzzuRenderState luzzu) {
            luzzu.rowingLeft = entity.getPaddleState(0);
            luzzu.rowingRight = entity.getPaddleState(1);
            luzzu.helmPlace = entity instanceof LuzzuBoat boat ? boat.helmPlace() : LuzzuOars.HELM_PLACE;
        }
    }

    /** Which oars are rowing (the boat's paddle state, true only while a driver rows that side). */
    public static class LuzzuRenderState extends BoatRenderState {
        public boolean rowingLeft;
        public boolean rowingRight;
        /** Where the helm seat is, blocks forward of the middle: the thole pins sit beside it. */
        public float helmPlace = LuzzuOars.HELM_PLACE;
    }

    /** The generated model, with each oar hidden unless it is rowing and swung by LuzzuOars instead of vanilla's
     *  paddle animation. Kept here so the generated file stays as made. */
    private static class OarsWhenRowing extends LuzzuModel {
        private final ModelPart leftOar;
        private final ModelPart rightOar;

        OarsWhenRowing(ModelPart root) {
            super(root);
            this.leftOar = root.getChild("left_paddle");
            this.rightOar = root.getChild("right_paddle");
        }

        @Override
        public void setupAnim(BoatRenderState state) {
            super.setupAnim(state);
            boolean left = state instanceof LuzzuRenderState luzzu ? luzzu.rowingLeft : state.rowingTimeLeft != 0.0F;
            boolean right = state instanceof LuzzuRenderState luzzu ? luzzu.rowingRight : state.rowingTimeRight != 0.0F;
            leftOar.visible = left;
            rightOar.visible = right;
            float helm = state instanceof LuzzuRenderState luzzu ? luzzu.helmPlace : LuzzuOars.HELM_PLACE;
            apply(leftOar, LuzzuOars.pose(state.rowingTimeLeft, 0, helm));
            apply(rightOar, LuzzuOars.pose(state.rowingTimeRight, 1, helm));
        }

        private static void apply(ModelPart oar, LuzzuOars.Pose pose) {
            oar.x = pose.x();
            oar.y = pose.y();
            oar.z = pose.z();
            oar.xRot = pose.xRot();
            oar.yRot = pose.yRot();
            oar.zRot = pose.zRot();
        }
    }
}
