package com.maltaminecraft.mimcontent.client.fish;

import com.maltaminecraft.mimcontent.MimContent;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.resources.Identifier;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.animal.fish.AbstractFish;

/**
 * Draws a tier A fish like vanilla draws cod: the whole body wiggles a little as it swims, and out of water it lies on
 * its side and flops. Texture: textures/entity/fish/&lt;id&gt;.png.
 */
public class FishRenderer extends MobRenderer<AbstractFish, LivingEntityRenderState, FishModel> {
    private final Identifier texture;
    private final float wiggle;

    /** wiggle: how far the body turns from side to side as it swims, in degrees (vanilla cod 4.3). */
    public FishRenderer(EntityRendererProvider.Context context, FishModel model, String id, float shadow, float wiggle) {
        super(context, model, shadow);
        this.texture = MimContent.id("textures/entity/fish/" + id + ".png");
        this.wiggle = wiggle;
    }

    @Override
    public Identifier getTextureLocation(LivingEntityRenderState state) {
        return texture;
    }

    @Override
    public LivingEntityRenderState createRenderState() {
        return new LivingEntityRenderState();
    }

    @Override
    protected void setupRotations(LivingEntityRenderState state, PoseStack poseStack, float bodyRot, float entityScale) {
        super.setupRotations(state, poseStack, bodyRot, entityScale);
        poseStack.rotateDegrees(Axis.YP, wiggle * Mth.sin(0.6F * state.ageInTicks));
        if (!state.isInWater) {
            poseStack.translate(0.1F, 0.1F, -0.1F);
            poseStack.rotateDegrees(Axis.ZP, 90.0F);
        }
    }
}
