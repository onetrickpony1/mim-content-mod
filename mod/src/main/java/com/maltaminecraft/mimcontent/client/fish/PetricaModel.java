package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The petrica (anglerfish): a huge, broad head about half the fish, with a very wide straight mouth, the lower jaw
 * jutting out and teeth along both jaws; small eyes on top; the fishing-rod lure leaning forward from the snout with a
 * dull flap at its tip and a second spine behind it; a fringe of skin flaps along the head; big fleshy pectoral fins on
 * arms reaching to the floor; the body tapering to a slim tail stalk and a squared tail fin that sways. Mottled brown
 * above, cream below. Head toward -z, the ground at y 24. No body wiggle; on land it lies flat on its belly, squashed
 * (FishRenderer.withLandSquash). Texture 128 x 64: textures/entity/fish/petrica.png. Made by
 * art/src/fish_petrica_model.py (don't edit by hand).
 */
public class PetricaModel extends FishModel {
    public PetricaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* head */ .texOffs(0, 0).addBox(-7.0F, -3.0F, -13.0F, 14.0F, 7.0F, 9.0F)
            /* cap */ .texOffs(0, 17).addBox(-6.0F, -4.0F, -12.0F, 12.0F, 1.0F, 8.0F)
            /* head_front */ .texOffs(97, 17).addBox(-6.0F, -2.0F, -14.0F, 12.0F, 6.0F, 1.0F)
            /* jaw */ .texOffs(29, 27).addBox(-8.0F, 1.0F, -16.0F, 16.0F, 3.0F, 2.0F)
            /* teeth */ .texOffs(29, 35).addBox(-7.0F, 0.0F, -15.5F, 14.0F, 1.0F, 0.0F)
            /* eye_l */ .texOffs(19, 35).addBox(4.0F, -4.5F, -8.0F, 1.0F, 1.0F, 1.0F)
            /* eye_r */ .texOffs(24, 35).addBox(-5.0F, -4.5F, -8.0F, 1.0F, 1.0F, 1.0F)
            /* trunk */ .texOffs(89, 0).addBox(-5.0F, -3.0F, -4.0F, 10.0F, 7.0F, 5.0F)
            /* mid */ .texOffs(41, 17).addBox(-3.5F, -1.0F, 1.0F, 7.0F, 5.0F, 4.0F)
            /* rear */ .texOffs(0, 27).addBox(-2.0F, 0.0F, 5.0F, 4.0F, 4.0F, 3.0F)
            /* stalk */ .texOffs(0, 35).addBox(-1.5F, 1.0F, 8.0F, 3.0F, 2.0F, 2.0F)
            /* fringe_l */ .texOffs(64, 17).addBox(7.0F, 1.0F, -13.0F, 1.0F, 0.0F, 9.0F)
            /* fringe_r */ .texOffs(76, 17).addBox(-8.0F, 1.0F, -13.0F, 1.0F, 0.0F, 9.0F)
            /* flap_l */ .texOffs(47, 0).addBox(7.5F, 1.0F, -14.0F, 0.0F, 3.0F, 10.0F)
            /* flap_r */ .texOffs(68, 0).addBox(-7.5F, 1.0F, -14.0F, 0.0F, 3.0F, 10.0F)
            /* dorsal */ .texOffs(15, 27).addBox(0.0F, -3.0F, 1.0F, 0.0F, 2.0F, 5.0F),
            PartPose.offset(0.0F, 20.0F, 0.0F));
        root.addOrReplaceChild("lure", CubeListBuilder.create()
            /* rod */ .texOffs(26, 27).addBox(0.0F, -5.0F, -0.5F, 0.0F, 5.0F, 1.0F)
            /* esca */ .texOffs(11, 35).addBox(0.0F, -7.0F, -1.5F, 0.0F, 2.0F, 2.0F),
            PartPose.offsetAndRotation(0.0F, 18.0F, -13.0F, 0.2F, 0.0F, 0.0F));
        root.addOrReplaceChild("spine2", CubeListBuilder.create()
            /* spine */ .texOffs(16, 35).addBox(0.0F, -2.0F, -0.5F, 0.0F, 2.0F, 1.0F),
            PartPose.offsetAndRotation(0.0F, 16.0F, -10.0F, -0.6F, 0.0F, 0.0F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* arm_l */ .texOffs(102, 27).addBox(-1.0F, -1.0F, -1.0F, 3.0F, 2.0F, 2.0F)
            /* pec_l */ .texOffs(66, 27).addBox(2.0F, 0.0F, -2.5F, 6.0F, 0.0F, 5.0F),
            PartPose.offsetAndRotation(5.0F, 20.0F, -1.0F, 0.0F, 0.4F, 0.45F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* arm_r */ .texOffs(113, 27).addBox(-2.0F, -1.0F, -1.0F, 3.0F, 2.0F, 2.0F)
            /* pec_r */ .texOffs(84, 27).addBox(-8.0F, 0.0F, -2.5F, 6.0F, 0.0F, 5.0F),
            PartPose.offsetAndRotation(-5.0F, 20.0F, -1.0F, 0.0F, -0.4F, -0.45F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(88, 17).addBox(0.0F, -2.5F, 0.0F, 0.0F, 5.0F, 4.0F),
            PartPose.offset(0.0F, 21.5F, 10.0F));
        return LayerDefinition.create(mesh, 128, 64);
    }
}
