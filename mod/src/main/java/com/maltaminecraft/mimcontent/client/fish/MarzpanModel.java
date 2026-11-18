package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The marzpan (Mediterranean parrotfish, the red female): an oblong, deep red body, dark along the back and pink below,
 * a blunt snout with a short pale beak, a grey-lilac cheek patch with the eye at its front and a yellow stripe under it,
 * a yellow saddle on the tail stalk, a long low dorsal fin, pale pectoral fins and a square-cut tail that sways as it
 * swims. 17 px long, 7 px deep, 4 px thick, head toward -z, the ground at y 24.
 * Made by art/src/fish_marzpan_model.py (don't edit by hand). Texture: textures/entity/fish/marzpan.png (64 x 64).
 * Parts: body, top_fin, tail_fin, right_fin, left_fin.
 */
public class MarzpanModel extends FishModel {
    public MarzpanModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* snout */ .texOffs(40, 30).addBox(-1.0F, -1.0F, -7.0F, 2.0F, 2.0F, 1.0F)
            /* head_front */ .texOffs(28, 30).addBox(-1.5F, -2.0F, -6.0F, 3.0F, 3.0F, 1.0F)
            /* head */ .texOffs(0, 30).addBox(-2.0F, -3.0F, -5.0F, 4.0F, 5.0F, 2.0F)
            /* trunk */ .texOffs(0, 0).addBox(-2.0F, -4.0F, -3.0F, 4.0F, 7.0F, 4.0F)
            /* rear */ .texOffs(20, 0).addBox(-1.5F, -3.0F, 1.0F, 3.0F, 5.0F, 2.0F)
            /* stalk */ .texOffs(36, 0).addBox(-1.0F, -2.0F, 3.0F, 2.0F, 3.0F, 2.0F)
            /* anal */ .texOffs(52, 1).addBox(0.0F, 2.0F, 1.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offset(0.0F, 19.0F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* dorsal */ .texOffs(0, 39).addBox(0.0F, -1.0F, -4.0F, 0.0F, 2.0F, 7.0F),
            PartPose.offset(0.0F, 15.0F, 0.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(20, 42).addBox(0.0F, -3.5F, -1.0F, 0.0F, 8.0F, 4.0F),
            PartPose.offset(0.0F, 18.5F, 5.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(30, 43).addBox(0.0F, -1.0F, 0.0F, 0.0F, 3.0F, 3.0F),
            PartPose.offsetAndRotation(-2.0F, 19.0F, -3.0F, 0.0F, -0.3F, 0.0F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(38, 43).addBox(0.0F, -1.0F, 0.0F, 0.0F, 3.0F, 3.0F),
            PartPose.offsetAndRotation(2.0F, 19.0F, -3.0F, 0.0F, 0.3F, 0.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
