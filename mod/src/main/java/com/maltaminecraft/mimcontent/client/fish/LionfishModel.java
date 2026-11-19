package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The lionfish (Pterois miles): a slim, compressed body banded all over in red-brown and cream, a row of long separate
 * banded venomous spines, huge fan pectoral fins hanging down and back from behind the head, a feathery tentacle over
 * each eye and a round banded fan tail that sways. 15 px long, 3 px thick, 5 px deep; head toward -z, the ground at
 * y 24. Texture: textures/entity/fish/lionfish.png (64 x 64).
 * Made by art/src/fish_lionfish_model.py (don't edit by hand).
 */
public class LionfishModel extends FishModel {
    public LionfishModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition body = root.addOrReplaceChild("body", CubeListBuilder.create()
            /* snout */ .texOffs(0, 19).addBox(-1.0F, -1.5F, -7.0F, 2.0F, 2.0F, 1.0F)
            /* head */ .texOffs(0, 11).addBox(-1.0F, -3.0F, -6.0F, 2.0F, 4.0F, 3.0F)
            /* trunk */ .texOffs(45, 0).addBox(-1.0F, -3.0F, -3.0F, 2.0F, 4.0F, 4.0F)
            /* rear */ .texOffs(17, 11).addBox(-1.0F, -2.5F, 1.0F, 2.0F, 3.0F, 3.0F)
            /* stalk */ .texOffs(7, 19).addBox(-0.5F, -2.0F, 4.0F, 1.0F, 2.0F, 1.0F)
            /* pelvic_r */ .texOffs(45, 11).addBox(-0.5F, 1.0F, -4.0F, 0.0F, 2.0F, 3.0F)
            /* pelvic_l */ .texOffs(38, 11).addBox(0.5F, 1.0F, -4.0F, 0.0F, 2.0F, 3.0F)
            /* anal */ .texOffs(31, 11).addBox(0.0F, 0.5F, 1.0F, 0.0F, 2.0F, 3.0F)
            /* soft_dorsal */ .texOffs(52, 11).addBox(0.0F, -4.5F, 1.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offset(0.0F, 20.0F, 0.0F));
        body.addOrReplaceChild("head_flaps", CubeListBuilder.create()
            /* tent_r */ .texOffs(15, 19).addBox(-1.0F, -2.0F, 0.0F, 0.0F, 2.0F, 1.0F)
            /* tent_l */ .texOffs(12, 19).addBox(1.0F, -2.0F, 0.0F, 0.0F, 2.0F, 1.0F),
            PartPose.offset(0.0F, -3.0F, -5.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* spine_1 */ .texOffs(11, 11).addBox(0.0F, -6.0F, -3.0F, 0.0F, 6.0F, 1.0F)
            /* spine_2 */ .texOffs(14, 11).addBox(0.0F, -6.0F, -1.0F, 0.0F, 6.0F, 1.0F)
            /* spine_3 */ .texOffs(28, 11).addBox(0.0F, -5.0F, 1.0F, 0.0F, 5.0F, 1.0F)
            /* spine_4 */ .texOffs(59, 11).addBox(0.0F, -4.0F, 3.0F, 0.0F, 4.0F, 1.0F)
            /* spine_web */ .texOffs(30, 0).addBox(0.0F, -1.0F, -3.0F, 0.0F, 1.0F, 7.0F),
            PartPose.offsetAndRotation(0.0F, 17.0F, -2.0F, -0.22F, 0.0F, 0.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(15, 0).addBox(0.0F, 0.0F, 0.0F, 0.0F, 3.0F, 7.0F),
            PartPose.offsetAndRotation(-1.0F, 19.0F, -3.0F, 0.0F, -0.3F, 0.6F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(0, 0).addBox(0.0F, 0.0F, 0.0F, 0.0F, 3.0F, 7.0F),
            PartPose.offsetAndRotation(1.0F, 19.0F, -3.0F, 0.0F, 0.3F, -0.6F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(58, 0).addBox(0.0F, -2.5F, 0.0F, 0.0F, 5.0F, 3.0F),
            PartPose.offset(0.0F, 19.0F, 5.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
