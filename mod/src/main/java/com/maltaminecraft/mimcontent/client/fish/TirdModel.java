package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The tird (ornate wrasse, the male): small and slim, a turquoise-blue head with pink-violet lines, a bright turquoise
 * bar and a red-orange band behind the head, a green body with thin red lines and a pale belly, a long low dorsal fin
 * and a lunate tail with dark-tipped points that sways as it swims. 13 px long, 3 px deep, 2 px wide, head toward
 * -z, the ground at y 24.
 * Made by art/src/fish_tird_model.py (don't edit by hand). Texture: textures/entity/fish/tird.png (32 x 32).
 */
public class TirdModel extends FishModel {
    public TirdModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* snout */ .texOffs(22, 0).addBox(-0.5F, -0.5F, -6.0F, 1.0F, 1.0F, 1.0F)
            /* head */ .texOffs(0, 0).addBox(-1.0F, -1.5F, -5.0F, 2.0F, 3.0F, 2.0F)
            /* trunk */ .texOffs(0, 6).addBox(-1.0F, -1.5F, -3.0F, 2.0F, 2.0F, 5.0F)
            /* belly */ .texOffs(8, 0).addBox(-1.0F, 0.5F, -3.0F, 2.0F, 1.0F, 3.0F)
            /* stalk */ .texOffs(22, 3).addBox(-0.5F, -1.5F, 2.0F, 1.0F, 2.0F, 1.0F)
            /* anal */ .texOffs(0, 15).addBox(0.0F, 0.5F, 0.0F, 0.0F, 1.0F, 2.0F),
            PartPose.offset(0.0F, 21.5F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* dorsal */ .texOffs(0, 10).addBox(0.0F, -1.0F, 0.0F, 0.0F, 1.0F, 5.0F),
            PartPose.offset(0.0F, 20.0F, -3.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(16, 11).addBox(0.0F, -2.5F, 0.0F, 0.0F, 5.0F, 4.0F),
            PartPose.offset(0.0F, 21.0F, 3.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(-1, 20).addBox(-1.0F, 0.0F, 0.0F, 1.0F, 0.0F, 1.0F),
            PartPose.offsetAndRotation(-1.0F, 21.5F, -2.0F, 0.0F, 0.0F, -0.9F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(1, 20).addBox(0.0F, 0.0F, 0.0F, 1.0F, 0.0F, 1.0F),
            PartPose.offsetAndRotation(1.0F, 21.5F, -2.0F, 0.0F, 0.0F, 0.9F));
        return LayerDefinition.create(mesh, 32, 32);
    }
}
