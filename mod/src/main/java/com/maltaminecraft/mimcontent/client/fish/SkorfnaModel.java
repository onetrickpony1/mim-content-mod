package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The skorfna (scorpionfish): long and tapering, not round, with a big broad spiny head (a third of the length), a wide
 * downturned mouth, high eyes under fleshy flaps, a long spiny dorsal fin with a notch, big fan pectoral fins splayed to
 * prop it on the floor, a slim stalk and a rounded banded tail that sways. 15 px long, 5 px deep (8 with the spines),
 * 6 px across the head; head toward -z, the ground at y 24. One model for both kinds: textures/entity/fish/skorfna.png
 * (the black scorpionfish) and skorfna_red.png (the red one) share every UV (64 x 64).
 * Made by art/src/fish_skorfna_model.py (don't edit by hand).
 */
public class SkorfnaModel extends FishModel {
    public SkorfnaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition body = root.addOrReplaceChild("body", CubeListBuilder.create()
            /* lip */ .texOffs(19, 24).addBox(-2.0F, 0.0F, -7.0F, 4.0F, 1.0F, 1.0F)
            /* head_front */ .texOffs(15, 16).addBox(-2.5F, -1.0F, -6.0F, 5.0F, 3.0F, 2.0F)
            /* head_top */ .texOffs(6, 24).addBox(-2.5F, -2.0F, -5.0F, 5.0F, 1.0F, 1.0F)
            /* crown */ .texOffs(30, 24).addBox(-1.5F, -3.0F, -5.0F, 3.0F, 1.0F, 1.0F)
            /* head_back */ .texOffs(46, 0).addBox(-3.0F, -3.0F, -4.0F, 6.0F, 5.0F, 2.0F)
            /* trunk */ .texOffs(0, 16).addBox(-2.0F, -3.0F, -2.0F, 4.0F, 4.0F, 3.0F)
            /* rear */ .texOffs(30, 16).addBox(-1.5F, -2.0F, 1.0F, 3.0F, 3.0F, 2.0F)
            /* stalk */ .texOffs(41, 16).addBox(-1.0F, -1.0F, 3.0F, 2.0F, 2.0F, 2.0F)
            /* pelvic_r */ .texOffs(60, 16).addBox(-1.5F, 1.0F, -4.0F, 0.0F, 2.0F, 2.0F)
            /* pelvic_l */ .texOffs(55, 16).addBox(1.5F, 1.0F, -4.0F, 0.0F, 2.0F, 2.0F)
            /* anal */ .texOffs(50, 16).addBox(0.0F, 0.0F, 1.0F, 0.0F, 2.0F, 2.0F),
            PartPose.offset(0.0F, 21.0F, 0.0F));
        body.addOrReplaceChild("head_flaps", CubeListBuilder.create()
            /* cirrus_r */ .texOffs(3, 24).addBox(-2.5F, -2.0F, 0.0F, 0.0F, 2.0F, 1.0F)
            /* cirrus_l */ .texOffs(0, 24).addBox(2.5F, -2.0F, 0.0F, 0.0F, 2.0F, 1.0F),
            PartPose.offset(0.0F, -2.0F, -5.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* dorsal */ .texOffs(0, 0).addBox(0.0F, -3.0F, -1.0F, 0.0F, 5.0F, 10.0F),
            PartPose.offset(0.0F, 18.0F, -4.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(30, 0).addBox(0.0F, 0.0F, 0.0F, 0.0F, 4.0F, 4.0F),
            PartPose.offsetAndRotation(-2.0F, 19.0F, -2.0F, 0.0F, -0.3F, 0.95F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(21, 0).addBox(0.0F, 0.0F, 0.0F, 0.0F, 4.0F, 4.0F),
            PartPose.offsetAndRotation(2.0F, 19.0F, -2.0F, 0.0F, 0.3F, -0.95F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(39, 0).addBox(0.0F, -2.5F, 0.0F, 0.0F, 5.0F, 3.0F),
            PartPose.offset(0.0F, 21.0F, 5.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
