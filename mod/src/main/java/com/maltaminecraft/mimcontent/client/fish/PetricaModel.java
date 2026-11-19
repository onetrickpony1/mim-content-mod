package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The petrica (anglerfish): a huge, wide, flattened head (14 px across, 16 with its fringe of skin flaps, nearly half
 * the 22 px length) with an enormous straight mouth right across the front and the lower jaw jutting out, small eyes
 * on top, the fishing-rod lure (illicium) leaning forward from the snout with a small dull flap at its tip, big fan
 * pectoral fins flat on the floor, and a body tapering fast to a small rounded tail that sways. Mottled brown above,
 * cream below. Head toward -z, the ground at y 24; flat, so it lies flat on land (no wiggle). Texture 64 x 64:
 * textures/entity/fish/petrica.png. Made by art/src/fish_petrica_model.py (don't edit by hand).
 */
public class PetricaModel extends FishModel {
    public PetricaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* jaw */ .texOffs(0, 56).addBox(-6.0F, 0.0F, -14.0F, 12.0F, 2.0F, 1.0F)
            /* head */ .texOffs(0, 0).addBox(-5.0F, -3.0F, -13.0F, 10.0F, 5.0F, 12.0F)
            /* shoulder_l */ .texOffs(0, 18).addBox(5.0F, -1.0F, -13.0F, 1.0F, 3.0F, 11.0F)
            /* shoulder_r */ .texOffs(25, 18).addBox(-6.0F, -1.0F, -13.0F, 1.0F, 3.0F, 11.0F)
            /* rim_l */ .texOffs(0, 33).addBox(6.0F, 1.0F, -11.0F, 2.0F, 1.0F, 7.0F)
            /* rim_r */ .texOffs(19, 33).addBox(-8.0F, 1.0F, -11.0F, 2.0F, 1.0F, 7.0F)
            /* rim_lf */ .texOffs(40, 56).addBox(6.0F, 1.0F, -12.0F, 1.0F, 1.0F, 1.0F)
            /* rim_rf */ .texOffs(50, 56).addBox(-7.0F, 1.0F, -12.0F, 1.0F, 1.0F, 1.0F)
            /* rim_lb */ .texOffs(35, 56).addBox(6.0F, 1.0F, -4.0F, 1.0F, 1.0F, 1.0F)
            /* rim_rb */ .texOffs(45, 56).addBox(-7.0F, 1.0F, -4.0F, 1.0F, 1.0F, 1.0F)
            /* trunk */ .texOffs(38, 33).addBox(-4.5F, -1.0F, -1.0F, 9.0F, 3.0F, 4.0F)
            /* rear */ .texOffs(27, 42).addBox(-2.5F, 0.0F, 3.0F, 5.0F, 2.0F, 4.0F)
            /* stalk */ .texOffs(46, 42).addBox(-1.5F, 0.0F, 7.0F, 3.0F, 2.0F, 3.0F)
            /* fringe_l */ .texOffs(0, 42).addBox(8.0F, 1.5F, -11.0F, 1.0F, 0.0F, 7.0F)
            /* fringe_r */ .texOffs(10, 42).addBox(-9.0F, 1.5F, -11.0F, 1.0F, 0.0F, 7.0F)
            /* fringe_f */ .texOffs(0, 60).addBox(-6.0F, 1.5F, -15.0F, 12.0F, 0.0F, 1.0F)
            /* dorsal */ .texOffs(0, 50).addBox(0.0F, -1.0F, 4.0F, 0.0F, 1.0F, 4.0F),
            PartPose.offset(0.0F, 22.0F, 0.0F));
        root.addOrReplaceChild("lure", CubeListBuilder.create()
            /* rod */ .texOffs(32, 56).addBox(0.0F, -2.0F, -0.5F, 0.0F, 2.0F, 1.0F)
            /* rod_x */ .texOffs(55, 56).addBox(-0.5F, -2.0F, 0.0F, 1.0F, 2.0F, 0.0F)
            /* esca */ .texOffs(27, 56).addBox(0.0F, -3.0F, -2.0F, 0.0F, 1.0F, 2.0F),
            PartPose.offsetAndRotation(0.0F, 19.0F, -12.5F, 0.9F, 0.0F, 0.0F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(9, 50).addBox(0.0F, 0.0F, -1.5F, 5.0F, 0.0F, 4.0F),
            PartPose.offsetAndRotation(4.5F, 22.5F, 0.5F, 0.0F, 0.6F, 0.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(24, 50).addBox(-5.0F, 0.0F, -1.5F, 5.0F, 0.0F, 4.0F),
            PartPose.offsetAndRotation(-4.5F, 22.5F, 0.5F, 0.0F, -0.6F, 0.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(20, 42).addBox(0.0F, -2.5F, 0.0F, 0.0F, 4.0F, 3.0F),
            PartPose.offset(0.0F, 22.5F, 10.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
