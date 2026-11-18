package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The boll (common stingray): a rhombic disc 16 px wide and 13 long with a bluntly pointed snout and rounded
 * outer corners, gently domed (2 px over the middle, 1 px at the wings), small eyes and spiracles on top, pelvic
 * lobes at the tail root and a 21 px whip tail with a pale serrated spine. Plain olive-brown back, cream underside
 * with the nostrils, mouth and gill slits.
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
            /* l_c0_l1 */ .texOffs(36, 0).addBox(0.0F, -0.5F, -8.0F, 1.0F, 1.0F, 13.0F)
            /* l_c0_l2 */ .texOffs(26, 18).addBox(0.0F, -1.5F, -7.0F, 1.0F, 1.0F, 11.0F)
            /* l_c1_l1 */ .texOffs(92, 0).addBox(1.0F, -0.5F, -7.0F, 1.0F, 1.0F, 12.0F)
            /* l_c1_l2 */ .texOffs(74, 18).addBox(1.0F, -1.5F, -6.0F, 1.0F, 1.0F, 10.0F)
            /* r_c0_l1 */ .texOffs(64, 0).addBox(-1.0F, -0.5F, -8.0F, 1.0F, 1.0F, 13.0F)
            /* r_c0_l2 */ .texOffs(50, 18).addBox(-1.0F, -1.5F, -7.0F, 1.0F, 1.0F, 11.0F)
            /* r_c1_l1 */ .texOffs(0, 18).addBox(-2.0F, -0.5F, -7.0F, 1.0F, 1.0F, 12.0F)
            /* r_c1_l2 */ .texOffs(0, 31).addBox(-2.0F, -1.5F, -6.0F, 1.0F, 1.0F, 10.0F)
            /* l_pelvic1 */ .texOffs(58, 50).addBox(1.0F, -0.5F, 5.0F, 1.0F, 1.0F, 2.0F)
            /* l_pelvic2 */ .texOffs(64, 50).addBox(2.0F, -0.5F, 4.0F, 1.0F, 1.0F, 2.0F)
            /* r_pelvic1 */ .texOffs(70, 50).addBox(-2.0F, -0.5F, 5.0F, 1.0F, 1.0F, 2.0F)
            /* r_pelvic2 */ .texOffs(76, 50).addBox(-3.0F, -0.5F, 4.0F, 1.0F, 1.0F, 2.0F),
            PartPose.offset(0.0F, 23.5F, 0.0F));
        PartDefinition left_wing = body.addOrReplaceChild("left_wing", CubeListBuilder.create()
            /* l_c2_l1 */ .texOffs(96, 18).addBox(0.0F, -0.5F, -6.0F, 1.0F, 1.0F, 10.0F)
            /* l_c2_l2 */ .texOffs(84, 31).addBox(0.0F, -1.5F, -5.0F, 1.0F, 1.0F, 8.0F)
            /* l_c3_l1 */ .texOffs(44, 31).addBox(1.0F, -0.5F, -5.0F, 1.0F, 1.0F, 9.0F)
            /* l_c3_l2 */ .texOffs(32, 42).addBox(1.0F, -1.5F, -4.0F, 1.0F, 1.0F, 6.0F),
            PartPose.offset(2.0F, 0.0F, 0.0F));
        PartDefinition left_wing_tip = left_wing.addOrReplaceChild("left_wing_tip", CubeListBuilder.create()
            /* l_c4_l1 */ .texOffs(0, 42).addBox(0.0F, -0.5F, -4.0F, 1.0F, 1.0F, 7.0F)
            /* l_c4_l2 */ .texOffs(0, 50).addBox(0.0F, -1.5F, -3.0F, 1.0F, 1.0F, 4.0F)
            /* l_c5_l1 */ .texOffs(46, 42).addBox(1.0F, -0.5F, -4.0F, 1.0F, 1.0F, 6.0F)
            /* l_c5_l2 */ .texOffs(46, 50).addBox(1.0F, -1.5F, -2.0F, 1.0F, 1.0F, 2.0F),
            PartPose.offset(2.0F, 0.0F, 0.0F));
        left_wing_tip.addOrReplaceChild("left_wing_edge", CubeListBuilder.create()
            /* l_c6_l1 */ .texOffs(88, 42).addBox(0.0F, -0.5F, -3.0F, 1.0F, 1.0F, 5.0F)
            /* l_c7_l1 */ .texOffs(30, 50).addBox(1.0F, -0.5F, -2.0F, 1.0F, 1.0F, 3.0F),
            PartPose.offset(2.0F, 0.0F, 0.0F));
        PartDefinition right_wing = body.addOrReplaceChild("right_wing", CubeListBuilder.create()
            /* r_c2_l1 */ .texOffs(22, 31).addBox(-1.0F, -0.5F, -6.0F, 1.0F, 1.0F, 10.0F)
            /* r_c2_l2 */ .texOffs(102, 31).addBox(-1.0F, -1.5F, -5.0F, 1.0F, 1.0F, 8.0F)
            /* r_c3_l1 */ .texOffs(64, 31).addBox(-2.0F, -0.5F, -5.0F, 1.0F, 1.0F, 9.0F)
            /* r_c3_l2 */ .texOffs(60, 42).addBox(-2.0F, -1.5F, -4.0F, 1.0F, 1.0F, 6.0F),
            PartPose.offset(-2.0F, 0.0F, 0.0F));
        PartDefinition right_wing_tip = right_wing.addOrReplaceChild("right_wing_tip", CubeListBuilder.create()
            /* r_c4_l1 */ .texOffs(16, 42).addBox(-1.0F, -0.5F, -4.0F, 1.0F, 1.0F, 7.0F)
            /* r_c4_l2 */ .texOffs(10, 50).addBox(-1.0F, -1.5F, -3.0F, 1.0F, 1.0F, 4.0F)
            /* r_c5_l1 */ .texOffs(74, 42).addBox(-2.0F, -0.5F, -4.0F, 1.0F, 1.0F, 6.0F)
            /* r_c5_l2 */ .texOffs(52, 50).addBox(-2.0F, -1.5F, -2.0F, 1.0F, 1.0F, 2.0F),
            PartPose.offset(-2.0F, 0.0F, 0.0F));
        right_wing_tip.addOrReplaceChild("right_wing_edge", CubeListBuilder.create()
            /* r_c6_l1 */ .texOffs(100, 42).addBox(-1.0F, -0.5F, -3.0F, 1.0F, 1.0F, 5.0F)
            /* r_c7_l1 */ .texOffs(38, 50).addBox(-2.0F, -0.5F, -2.0F, 1.0F, 1.0F, 3.0F),
            PartPose.offset(-2.0F, 0.0F, 0.0F));
        PartDefinition tail = root.addOrReplaceChild("tail", CubeListBuilder.create()
            /* tail_root */ .texOffs(112, 42).addBox(-1.0F, -0.5F, 0.0F, 2.0F, 1.0F, 4.0F)
            /* whip */ .texOffs(0, 0).addBox(-0.5F, -0.5F, 4.0F, 1.0F, 1.0F, 17.0F),
            PartPose.offset(0.0F, 23.5F, 5.0F));
        tail.addOrReplaceChild("spine", CubeListBuilder.create()
            /* spine */ .texOffs(20, 50).addBox(-0.5F, -1.0F, 0.0F, 1.0F, 1.0F, 4.0F),
            PartPose.offset(0.0F, -0.5F, 7.0F));
        return LayerDefinition.create(mesh, 128, 64);
    }
}
