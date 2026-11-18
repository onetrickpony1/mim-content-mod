package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The boll (common stingray): a rhombic disc 20 px wide and 16 long (1.25 blocks wide) with a bluntly pointed
 * snout and rounded outer corners, gently domed (2 px over the middle, 1 px at the wings), small raised eyes with
 * the spiracles behind them, pelvic lobes at the tail root and a 26 px whip tail with a flat pale spine. Plain
 * olive-brown back; cream underside with a straight mouth, the nostrils and nasal curtain, and the gill slits.
 * Made by art/src/fish_boll_model.py (do not edit by hand); texture textures/entity/fish/boll.png.
 * Extends RayModel, which animates it: each wing is three rings (left_wing, left_wing_tip, left_wing_edge),
 * each hinged at the middle of the plate, so the ripple runs out from the body to the rounded corners.
 */
public class BollModel extends RayModel {
    public BollModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition body = root.addOrReplaceChild("body", CubeListBuilder.create()
            /* l_c0_l1 */ .texOffs(44, 0).addBox(0.0F, -0.5F, -10.0F, 1.0F, 1.0F, 16.0F)
            /* l_c0_l2 */ .texOffs(32, 39).addBox(0.0F, -1.5F, -9.0F, 1.0F, 1.0F, 14.0F)
            /* l_c1_l1 */ .texOffs(78, 0).addBox(1.0F, -0.5F, -10.0F, 1.0F, 1.0F, 16.0F)
            /* l_c1_l2 */ .texOffs(62, 39).addBox(1.0F, -1.5F, -9.0F, 1.0F, 1.0F, 14.0F)
            /* l_c2_l1 */ .texOffs(68, 22).addBox(2.0F, -0.5F, -9.0F, 1.0F, 1.0F, 15.0F)
            /* l_c2_l2 */ .texOffs(28, 70).addBox(2.0F, -1.5F, -8.0F, 1.0F, 1.0F, 12.0F)
            /* r_c0_l1 */ .texOffs(0, 22).addBox(-1.0F, -0.5F, -10.0F, 1.0F, 1.0F, 16.0F)
            /* r_c0_l2 */ .texOffs(92, 39).addBox(-1.0F, -1.5F, -9.0F, 1.0F, 1.0F, 14.0F)
            /* r_c1_l1 */ .texOffs(34, 22).addBox(-2.0F, -0.5F, -10.0F, 1.0F, 1.0F, 16.0F)
            /* r_c1_l2 */ .texOffs(0, 55).addBox(-2.0F, -1.5F, -9.0F, 1.0F, 1.0F, 14.0F)
            /* r_c2_l1 */ .texOffs(0, 39).addBox(-3.0F, -0.5F, -9.0F, 1.0F, 1.0F, 15.0F)
            /* r_c2_l2 */ .texOffs(54, 70).addBox(-3.0F, -1.5F, -8.0F, 1.0F, 1.0F, 12.0F)
            /* l_pelvic1 */ .texOffs(120, 95).addBox(1.0F, -0.5F, 6.0F, 1.0F, 1.0F, 3.0F)
            /* l_pelvic2 */ .texOffs(8, 103).addBox(2.0F, -0.5F, 6.0F, 1.0F, 1.0F, 2.0F)
            /* r_pelvic1 */ .texOffs(0, 103).addBox(-2.0F, -0.5F, 6.0F, 1.0F, 1.0F, 3.0F)
            /* r_pelvic2 */ .texOffs(14, 103).addBox(-3.0F, -0.5F, 6.0F, 1.0F, 1.0F, 2.0F)
            /* eye_l */ .texOffs(20, 103).addBox(2.0F, -2.5F, -6.0F, 1.0F, 1.0F, 1.0F)
            /* eye_r */ .texOffs(24, 103).addBox(-3.0F, -2.5F, -6.0F, 1.0F, 1.0F, 1.0F),
            PartPose.offset(0.0F, 23.5F, 0.0F));
        PartDefinition left_wing = body.addOrReplaceChild("left_wing", CubeListBuilder.create()
            /* l_c3_l1 */ .texOffs(30, 55).addBox(0.0F, -0.5F, -8.0F, 1.0F, 1.0F, 13.0F)
            /* l_c3_l2 */ .texOffs(44, 84).addBox(0.0F, -1.5F, -6.0F, 1.0F, 1.0F, 9.0F)
            /* l_c4_l1 */ .texOffs(58, 55).addBox(1.0F, -0.5F, -8.0F, 1.0F, 1.0F, 13.0F)
            /* l_c4_l2 */ .texOffs(0, 95).addBox(1.0F, -1.5F, -5.0F, 1.0F, 1.0F, 7.0F)
            /* l_c5_l1 */ .texOffs(80, 70).addBox(2.0F, -0.5F, -7.0F, 1.0F, 1.0F, 11.0F)
            /* l_c5_l2 */ .texOffs(74, 95).addBox(2.0F, -1.5F, -3.0F, 1.0F, 1.0F, 4.0F),
            PartPose.offset(3.0F, 0.0F, 0.0F));
        PartDefinition left_wing_tip = left_wing.addOrReplaceChild("left_wing_tip", CubeListBuilder.create()
            /* l_c6_l1 */ .texOffs(0, 84).addBox(0.0F, -0.5F, -6.0F, 1.0F, 1.0F, 10.0F)
            /* l_c7_l1 */ .texOffs(84, 84).addBox(1.0F, -0.5F, -5.0F, 1.0F, 1.0F, 8.0F),
            PartPose.offset(3.0F, 0.0F, 0.0F));
        left_wing_tip.addOrReplaceChild("left_wing_edge", CubeListBuilder.create()
            /* l_c8_l1 */ .texOffs(32, 95).addBox(0.0F, -0.5F, -4.0F, 1.0F, 1.0F, 6.0F)
            /* l_c9_l1 */ .texOffs(104, 95).addBox(1.0F, -0.5F, -2.0F, 1.0F, 1.0F, 3.0F),
            PartPose.offset(2.0F, 0.0F, 0.0F));
        PartDefinition right_wing = body.addOrReplaceChild("right_wing", CubeListBuilder.create()
            /* r_c3_l1 */ .texOffs(86, 55).addBox(-1.0F, -0.5F, -8.0F, 1.0F, 1.0F, 13.0F)
            /* r_c3_l2 */ .texOffs(64, 84).addBox(-1.0F, -1.5F, -6.0F, 1.0F, 1.0F, 9.0F)
            /* r_c4_l1 */ .texOffs(0, 70).addBox(-2.0F, -0.5F, -8.0F, 1.0F, 1.0F, 13.0F)
            /* r_c4_l2 */ .texOffs(16, 95).addBox(-2.0F, -1.5F, -5.0F, 1.0F, 1.0F, 7.0F)
            /* r_c5_l1 */ .texOffs(104, 70).addBox(-3.0F, -0.5F, -7.0F, 1.0F, 1.0F, 11.0F)
            /* r_c5_l2 */ .texOffs(84, 95).addBox(-3.0F, -1.5F, -3.0F, 1.0F, 1.0F, 4.0F),
            PartPose.offset(-3.0F, 0.0F, 0.0F));
        PartDefinition right_wing_tip = right_wing.addOrReplaceChild("right_wing_tip", CubeListBuilder.create()
            /* r_c6_l1 */ .texOffs(22, 84).addBox(-1.0F, -0.5F, -6.0F, 1.0F, 1.0F, 10.0F)
            /* r_c7_l1 */ .texOffs(102, 84).addBox(-2.0F, -0.5F, -5.0F, 1.0F, 1.0F, 8.0F),
            PartPose.offset(-3.0F, 0.0F, 0.0F));
        right_wing_tip.addOrReplaceChild("right_wing_edge", CubeListBuilder.create()
            /* r_c8_l1 */ .texOffs(46, 95).addBox(-1.0F, -0.5F, -4.0F, 1.0F, 1.0F, 6.0F)
            /* r_c9_l1 */ .texOffs(112, 95).addBox(-2.0F, -0.5F, -2.0F, 1.0F, 1.0F, 3.0F),
            PartPose.offset(-2.0F, 0.0F, 0.0F));
        PartDefinition tail = root.addOrReplaceChild("tail", CubeListBuilder.create()
            /* tail_root */ .texOffs(60, 95).addBox(-1.0F, -0.5F, 0.0F, 2.0F, 1.0F, 5.0F)
            /* whip */ .texOffs(0, 0).addBox(-0.5F, -0.5F, 5.0F, 1.0F, 1.0F, 21.0F),
            PartPose.offset(0.0F, 23.5F, 6.0F));
        tail.addOrReplaceChild("spine", CubeListBuilder.create()
            /* spine */ .texOffs(94, 95).addBox(-0.5F, -0.05F, 0.0F, 1.0F, 0.0F, 4.0F),
            PartPose.offset(0.0F, -0.5F, 9.0F));
        return LayerDefinition.create(mesh, 128, 128);
    }
}
