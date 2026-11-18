package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The cerna (dusky grouper): big, heavy and deep, mottled reddish-brown with pale blotches and a light belly, a big
 * head with a rounded mouth, a jutting lower jaw and a small eye high up, one long dorsal fin, broad rounded pectoral
 * fins and a rounded tail that sways as it swims. 29 px long, 10 px deep, 6 px thick, head toward -z, the ground at y 24.
 * Made by art/src/fish_cerna_model.py (don't edit by hand). Texture: textures/entity/fish/cerna.png (64 x 64).
 */
public class CernaModel extends FishModel {
    public CernaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* jaw_tip */ .texOffs(54, 21).addBox(-1.0F, 1.0F, -13.0F, 2.0F, 2.0F, 1.0F)
            /* jaw */ .texOffs(46, 17).addBox(-1.5F, 1.0F, -12.0F, 3.0F, 2.0F, 2.0F)
            /* lip_tip */ .texOffs(54, 24).addBox(-1.0F, -1.0F, -12.0F, 2.0F, 2.0F, 1.0F)
            /* snout */ .texOffs(46, 21).addBox(-1.5F, -2.0F, -11.0F, 3.0F, 3.0F, 1.0F)
            /* head_front */ .texOffs(0, 17).addBox(-2.0F, -4.0F, -10.0F, 4.0F, 7.0F, 2.0F)
            /* head */ .texOffs(26, 0).addBox(-2.5F, -5.0F, -8.0F, 5.0F, 8.0F, 3.0F)
            /* trunk */ .texOffs(0, 0).addBox(-3.0F, -6.0F, -5.0F, 6.0F, 10.0F, 7.0F)
            /* rear */ .texOffs(42, 0).addBox(-2.5F, -5.0F, 2.0F, 5.0F, 8.0F, 4.0F)
            /* stalk */ .texOffs(12, 17).addBox(-2.0F, -4.0F, 6.0F, 4.0F, 6.0F, 3.0F)
            /* stalk2 */ .texOffs(26, 17).addBox(-1.5F, -3.0F, 9.0F, 3.0F, 4.0F, 2.0F)
            /* dorsal */ .texOffs(0, 14).addBox(0.0F, -8.0F, -7.0F, 0.0F, 4.0F, 16.0F)
            /* anal */ .texOffs(0, 21).addBox(0.0F, 2.0F, 3.0F, 0.0F, 3.0F, 5.0F),
            PartPose.offset(0.0F, 20.0F, 0.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(36, 12).addBox(0.0F, -4.0F, 0.0F, 0.0F, 9.0F, 5.0F),
            PartPose.offset(0.0F, 19.0F, 11.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(10, 22).addBox(0.0F, -1.0F, 0.0F, 0.0F, 3.0F, 4.0F),
            PartPose.offsetAndRotation(-3.0F, 19.0F, -5.0F, 0.0F, -0.4F, 0.0F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(18, 22).addBox(0.0F, -1.0F, 0.0F, 0.0F, 3.0F, 4.0F),
            PartPose.offsetAndRotation(3.0F, 19.0F, -5.0F, 0.0F, 0.4F, 0.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
