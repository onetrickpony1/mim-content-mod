package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.util.Mth;

/**
 * The murina (Mediterranean moray): a long eel, round in front and flattened toward the tail, violet-brown with dense
 * cream spots; a big head with a raised crown, a long snout with tube nostrils, a wide open mouth, a jutting lower jaw
 * and a small pale eye near the front; no pectoral fins, one low fin from behind the head round the tail to mid-belly.
 * 32 px long, 4 px deep and 3 px thick (the head 5 and 4), head toward -z, the ground at y 24.
 * Its own swimming: the body is a chain of five sections (body, seg1, seg2, seg3, tail), each the child of the one
 * before, and a sideways wave runs down it, each section turning further and later than the one in front, so an S
 * travels from the neck to the tail while the head stays nearly still. Out of water the wave is wider and quicker, as
 * vanilla fish flop. The renderer's whole-body wiggle is 0.
 * Made by art/src/fish_murina_model.py (don't edit by hand). Texture: textures/entity/fish/murina.png (64 x 64).
 */
public class MurinaModel extends FishModel {
    /** How far each section turns from the swimming line, in radians, from the head back. */
    private static final float[] AMPLITUDE = {0.05F, 0.15F, 0.26F, 0.36F, 0.46F};
    private final ModelPart[] sections;

    public MurinaModel(ModelPart root) {
        super(root);
        ModelPart body = root.getChild("body");
        ModelPart seg1 = body.getChild("seg1");
        ModelPart seg2 = seg1.getChild("seg2");
        ModelPart seg3 = seg2.getChild("seg3");
        this.sections = new ModelPart[] {body, seg1, seg2, seg3, seg3.getChild("tail")};
    }

    @Override
    public void setupAnim(LivingEntityRenderState state) {
        super.setupAnim(state);
        float amplitude = state.isInWater ? 1.0F : 1.2F;
        float speed = state.isInWater ? 1.0F : 1.8F;
        float phase = speed * 0.33F * state.ageInTicks;
        float before = 0.0F;
        for (int i = 0; i < sections.length; i++) {
            float angle = amplitude * AMPLITUDE[i] * Mth.sin(phase - i * 1.05F);
            sections[i].yRot = angle - before;
            before = angle;
        }
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition body = root.addOrReplaceChild("body", CubeListBuilder.create()
            /* nose */ .texOffs(36, 16).addBox(-1.0F, -2.0F, -14.0F, 2.0F, 1.0F, 1.0F)
            /* snout */ .texOffs(48, 9).addBox(-1.0F, -2.0F, -13.0F, 2.0F, 2.0F, 2.0F)
            /* upjaw */ .texOffs(22, 9).addBox(-1.5F, -2.0F, -11.0F, 3.0F, 2.0F, 3.0F)
            /* brow */ .texOffs(42, 16).addBox(-1.5F, -3.0F, -9.0F, 3.0F, 1.0F, 1.0F)
            /* head */ .texOffs(0, 0).addBox(-2.0F, -3.0F, -8.0F, 4.0F, 5.0F, 4.0F)
            /* mouth */ .texOffs(0, 16).addBox(-1.0F, 0.0F, -11.0F, 2.0F, 1.0F, 3.0F)
            /* lojaw_tip */ .texOffs(50, 16).addBox(-1.0F, 1.0F, -12.0F, 2.0F, 1.0F, 1.0F)
            /* lojaw */ .texOffs(10, 16).addBox(-1.5F, 1.0F, -11.0F, 3.0F, 1.0F, 3.0F)
            /* neck */ .texOffs(46, 0).addBox(-1.5F, -2.0F, -4.0F, 3.0F, 4.0F, 4.0F)
            /* fin_neck */ .texOffs(56, 12).addBox(0.0F, -3.0F, -4.0F, 0.0F, 1.0F, 4.0F),
            PartPose.offset(0.0F, 21.0F, 0.0F));
        PartDefinition seg1 = body.addOrReplaceChild("seg1", CubeListBuilder.create()
            /* seg1 */ .texOffs(16, 0).addBox(-1.5F, -2.0F, 0.0F, 3.0F, 4.0F, 5.0F)
            /* collar1 */ .texOffs(34, 9).addBox(-1.5F, -2.0F, -1.0F, 3.0F, 4.0F, 1.0F, new CubeDeformation(-0.05F))
            /* fin_seg1 */ .texOffs(0, 15).addBox(0.0F, -3.0F, 0.0F, 0.0F, 1.0F, 5.0F),
            PartPose.offset(0.0F, 0.0F, 0.0F));
        PartDefinition seg2 = seg1.addOrReplaceChild("seg2", CubeListBuilder.create()
            /* seg2 */ .texOffs(32, 0).addBox(-1.0F, -2.0F, 0.0F, 2.0F, 4.0F, 5.0F)
            /* collar2 */ .texOffs(42, 9).addBox(-1.0F, -2.0F, -1.0F, 2.0F, 4.0F, 1.0F, new CubeDeformation(-0.05F))
            /* fin_seg2 */ .texOffs(10, 15).addBox(0.0F, -3.0F, 0.0F, 0.0F, 1.0F, 5.0F)
            /* anal_seg2 */ .texOffs(20, 16).addBox(0.0F, 2.0F, 1.0F, 0.0F, 1.0F, 4.0F),
            PartPose.offset(0.0F, 0.0F, 5.0F));
        PartDefinition seg3 = seg2.addOrReplaceChild("seg3", CubeListBuilder.create()
            /* seg3 */ .texOffs(0, 9).addBox(-1.0F, -1.5F, 0.0F, 2.0F, 3.0F, 4.0F)
            /* collar3 */ .texOffs(22, 16).addBox(-1.0F, -1.5F, -1.0F, 2.0F, 3.0F, 1.0F, new CubeDeformation(-0.05F))
            /* fin_seg3 */ .texOffs(28, 16).addBox(0.0F, -2.5F, 0.0F, 0.0F, 1.0F, 4.0F)
            /* anal_seg3 */ .texOffs(36, 16).addBox(0.0F, 1.5F, 0.0F, 0.0F, 1.0F, 4.0F),
            PartPose.offset(0.0F, 0.0F, 5.0F));
        PartDefinition tailPart = seg3.addOrReplaceChild("tail", CubeListBuilder.create()
            /* tail */ .texOffs(12, 9).addBox(-0.5F, -1.0F, -1.0F, 1.0F, 2.0F, 4.0F)
            /* fin_tail */ .texOffs(28, 12).addBox(0.0F, -2.0F, 0.0F, 0.0F, 4.0F, 4.0F),
            PartPose.offset(0.0F, 0.0F, 4.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
