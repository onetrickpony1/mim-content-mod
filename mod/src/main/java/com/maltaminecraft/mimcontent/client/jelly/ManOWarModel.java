package com.maltaminecraft.mimcontent.client.jelly;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The Portuguese man o' war (Physalia physalis): no bell, but a long translucent gas float lying on the water,
 * low and round at the front, rising to a pink tip at the back, with a wavy pink-edged crest along its top,
 * short blue polyps beneath and five thin beaded blue-violet fishing tentacles hanging 1.4 to 3.5 blocks down.
 * The float is the "bell" (pivoted at its middle: the base class bobs and tilts it, no pulse);
 * "tentacle_0".."tentacle_4" are its children, pivoted at their roots, and sway.
 * Made by art/src/jelly_man_o_war_model.py (do not edit by hand); texture textures/entity/jellyfish/man_o_war.png.
 */
public class ManOWarModel extends JellyfishModel {
    public ManOWarModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition bell = root.addOrReplaceChild("bell", CubeListBuilder.create()
            /* front */ .texOffs(28, 14).addBox(-1.0F, 0.0F, -5.0F, 2.0F, 2.0F, 1.0F)
            /* bow */ .texOffs(18, 0).addBox(-1.5F, -1.0F, -4.0F, 3.0F, 4.0F, 1.0F)
            /* main */ .texOffs(0, 0).addBox(-2.0F, -2.0F, -3.0F, 4.0F, 5.0F, 5.0F)
            /* aft */ .texOffs(26, 0).addBox(-1.5F, -2.0F, 2.0F, 3.0F, 4.0F, 1.0F)
            /* rear */ .texOffs(54, 0).addBox(-1.0F, -3.0F, 3.0F, 2.0F, 3.0F, 1.0F)
            /* tip */ .texOffs(34, 14).addBox(-1.0F, -4.0F, 4.0F, 2.0F, 2.0F, 1.0F)
            /* crest_0 */ .texOffs(84, 14).addBox(-0.5F, -3.0F, -3.0F, 1.0F, 1.0F, 1.0F)
            /* crest_1 */ .texOffs(40, 14).addBox(-0.5F, -4.0F, -2.0F, 1.0F, 2.0F, 1.0F)
            /* crest_2 */ .texOffs(60, 0).addBox(-0.5F, -5.0F, -1.0F, 1.0F, 3.0F, 1.0F)
            /* crest_3 */ .texOffs(34, 0).addBox(-0.5F, -6.0F, 0.0F, 1.0F, 4.0F, 1.0F)
            /* crest_4 */ .texOffs(44, 14).addBox(-0.5F, -4.0F, 1.0F, 1.0F, 2.0F, 1.0F)
            /* crest_5 */ .texOffs(88, 14).addBox(-0.5F, -3.0F, 2.0F, 1.0F, 1.0F, 1.0F)
            /* polyp_0 */ .texOffs(92, 14).addBox(-2.0F, 3.0F, -4.0F, 1.0F, 1.0F, 1.0F)
            /* polyp_1 */ .texOffs(48, 14).addBox(-1.0F, 3.0F, -4.0F, 1.0F, 2.0F, 1.0F)
            /* polyp_2 */ .texOffs(96, 14).addBox(0.0F, 3.0F, -4.0F, 1.0F, 1.0F, 1.0F)
            /* polyp_3 */ .texOffs(52, 14).addBox(-2.0F, 3.0F, -3.0F, 1.0F, 2.0F, 1.0F)
            /* polyp_4 */ .texOffs(64, 0).addBox(0.0F, 3.0F, -3.0F, 1.0F, 3.0F, 1.0F)
            /* polyp_5 */ .texOffs(100, 14).addBox(1.0F, 3.0F, -3.0F, 1.0F, 1.0F, 1.0F)
            /* polyp_6 */ .texOffs(104, 14).addBox(-2.0F, 3.0F, -2.0F, 1.0F, 1.0F, 1.0F)
            /* polyp_7 */ .texOffs(56, 14).addBox(-1.0F, 3.0F, -2.0F, 1.0F, 2.0F, 1.0F)
            /* polyp_8 */ .texOffs(60, 14).addBox(1.0F, 3.0F, -2.0F, 1.0F, 2.0F, 1.0F)
            /* polyp_9 */ .texOffs(68, 0).addBox(-2.0F, 3.0F, -1.0F, 1.0F, 3.0F, 1.0F)
            /* polyp_10 */ .texOffs(108, 14).addBox(-1.0F, 3.0F, -1.0F, 1.0F, 1.0F, 1.0F)
            /* polyp_11 */ .texOffs(64, 14).addBox(0.0F, 3.0F, -1.0F, 1.0F, 2.0F, 1.0F)
            /* polyp_12 */ .texOffs(68, 14).addBox(-1.0F, 3.0F, 0.0F, 1.0F, 2.0F, 1.0F)
            /* polyp_13 */ .texOffs(112, 14).addBox(0.0F, 3.0F, 0.0F, 1.0F, 1.0F, 1.0F)
            /* polyp_14 */ .texOffs(72, 0).addBox(1.0F, 3.0F, 0.0F, 1.0F, 3.0F, 1.0F)
            /* polyp_15 */ .texOffs(116, 14).addBox(-2.0F, 3.0F, 1.0F, 1.0F, 1.0F, 1.0F)
            /* polyp_16 */ .texOffs(120, 14).addBox(1.0F, 3.0F, 1.0F, 1.0F, 1.0F, 1.0F),
            PartPose.offset(0.0F, 21.0F, 0.0F));
        bell.addOrReplaceChild("tentacle_0", CubeListBuilder.create()
            /* tentacle_0_0 */ .texOffs(76, 0).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_1 */ .texOffs(80, 0).addBox(-0.5F, 3.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_2 */ .texOffs(84, 0).addBox(-0.5F, 6.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_3 */ .texOffs(38, 0).addBox(-1.5F, 8.0F, -0.5F, 1.0F, 4.0F, 1.0F)
            /* tentacle_0_4 */ .texOffs(88, 0).addBox(-1.5F, 12.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_5 */ .texOffs(92, 0).addBox(-1.5F, 15.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_6 */ .texOffs(96, 0).addBox(-1.5F, 18.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_7 */ .texOffs(100, 0).addBox(-1.5F, 21.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_8 */ .texOffs(104, 0).addBox(-1.5F, 24.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_9 */ .texOffs(108, 0).addBox(-1.5F, 27.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_10 */ .texOffs(112, 0).addBox(-1.5F, 30.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_11 */ .texOffs(116, 0).addBox(-1.5F, 33.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_12 */ .texOffs(120, 0).addBox(-1.5F, 36.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_13 */ .texOffs(124, 0).addBox(-1.5F, 39.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_14 */ .texOffs(0, 10).addBox(-1.5F, 42.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_15 */ .texOffs(4, 10).addBox(-1.5F, 45.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_16 */ .texOffs(8, 10).addBox(-1.5F, 48.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_17 */ .texOffs(12, 10).addBox(-1.5F, 51.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_0_18 */ .texOffs(72, 14).addBox(-1.5F, 54.0F, -0.5F, 1.0F, 2.0F, 1.0F),
            PartPose.offset(-0.5F, 3.0F, -2.5F));
        bell.addOrReplaceChild("tentacle_1", CubeListBuilder.create()
            /* tentacle_1_0 */ .texOffs(16, 10).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_1 */ .texOffs(20, 10).addBox(-0.5F, 3.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_2 */ .texOffs(24, 10).addBox(-0.5F, 6.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_3 */ .texOffs(28, 10).addBox(-0.5F, 9.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_4 */ .texOffs(32, 10).addBox(-0.5F, 12.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_5 */ .texOffs(36, 10).addBox(-0.5F, 15.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_6 */ .texOffs(40, 10).addBox(-0.5F, 18.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_7 */ .texOffs(44, 10).addBox(-0.5F, 21.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_8 */ .texOffs(48, 10).addBox(-0.5F, 24.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_9 */ .texOffs(52, 10).addBox(-0.5F, 27.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_10 */ .texOffs(56, 10).addBox(-0.5F, 30.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_11 */ .texOffs(60, 10).addBox(-0.5F, 33.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_1_12 */ .texOffs(76, 14).addBox(-0.5F, 36.0F, -0.5F, 1.0F, 2.0F, 1.0F),
            PartPose.offset(0.5F, 3.0F, -1.5F));
        bell.addOrReplaceChild("tentacle_2", CubeListBuilder.create()
            /* tentacle_2_0 */ .texOffs(64, 10).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_2_1 */ .texOffs(68, 10).addBox(-0.5F, 3.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_2_2 */ .texOffs(72, 10).addBox(-0.5F, 6.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_2_3 */ .texOffs(76, 10).addBox(-0.5F, 9.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_2_4 */ .texOffs(80, 10).addBox(-0.5F, 12.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_2_5 */ .texOffs(42, 0).addBox(0.5F, 14.0F, -0.5F, 1.0F, 4.0F, 1.0F)
            /* tentacle_2_6 */ .texOffs(84, 10).addBox(0.5F, 18.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_2_7 */ .texOffs(88, 10).addBox(0.5F, 21.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_2_8 */ .texOffs(92, 10).addBox(0.5F, 24.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_2_9 */ .texOffs(124, 14).addBox(0.5F, 27.0F, -0.5F, 1.0F, 1.0F, 1.0F),
            PartPose.offset(1.5F, 3.0F, -0.5F));
        bell.addOrReplaceChild("tentacle_3", CubeListBuilder.create()
            /* tentacle_3_0 */ .texOffs(96, 10).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_3_1 */ .texOffs(100, 10).addBox(-0.5F, 3.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_3_2 */ .texOffs(104, 10).addBox(-0.5F, 6.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_3_3 */ .texOffs(46, 0).addBox(-0.5F, 8.0F, -1.5F, 1.0F, 4.0F, 1.0F)
            /* tentacle_3_4 */ .texOffs(108, 10).addBox(-0.5F, 12.0F, -1.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_3_5 */ .texOffs(112, 10).addBox(-0.5F, 15.0F, -1.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_3_6 */ .texOffs(116, 10).addBox(-0.5F, 18.0F, -1.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_3_7 */ .texOffs(0, 18).addBox(-0.5F, 21.0F, -1.5F, 1.0F, 1.0F, 1.0F),
            PartPose.offset(-1.5F, 3.0F, 0.5F));
        bell.addOrReplaceChild("tentacle_4", CubeListBuilder.create()
            /* tentacle_4_0 */ .texOffs(120, 10).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_4_1 */ .texOffs(124, 10).addBox(-0.5F, 3.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_4_2 */ .texOffs(0, 14).addBox(-0.5F, 6.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_4_3 */ .texOffs(4, 14).addBox(-0.5F, 9.0F, -0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_4_4 */ .texOffs(50, 0).addBox(-0.5F, 11.0F, 0.5F, 1.0F, 4.0F, 1.0F)
            /* tentacle_4_5 */ .texOffs(8, 14).addBox(-0.5F, 15.0F, 0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_4_6 */ .texOffs(12, 14).addBox(-0.5F, 18.0F, 0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_4_7 */ .texOffs(16, 14).addBox(-0.5F, 21.0F, 0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_4_8 */ .texOffs(20, 14).addBox(-0.5F, 24.0F, 0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_4_9 */ .texOffs(24, 14).addBox(-0.5F, 27.0F, 0.5F, 1.0F, 3.0F, 1.0F)
            /* tentacle_4_10 */ .texOffs(80, 14).addBox(-0.5F, 30.0F, 0.5F, 1.0F, 2.0F, 1.0F),
            PartPose.offset(0.5F, 3.0F, 1.5F));
        return LayerDefinition.create(mesh, 128, 64);
    }
}
