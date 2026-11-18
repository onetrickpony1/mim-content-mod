package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The incova (anchovy): a slim, round cigar with a long pointed snout overhanging an underslung mouth that reaches
 * back past the big, forward-set eye, a green back over a bright silver band, no spots, a small dorsal fin mid-back
 * and a forked tail that sways as it swims. 13 px long, 2 px deep and wide, head toward -z, the ground at y 24.
 * Made by art/src/fish_incova_model.py (don't edit by hand). Texture: textures/entity/fish/incova.png (32 x 32).
 */
public class IncovaModel extends FishModel {
    public IncovaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* tip */ .texOffs(26, 0).addBox(-0.5F, 0.0F, -5.0F, 1.0F, 1.0F, 1.0F)
            /* snout */ .texOffs(18, 0).addBox(-1.0F, 0.0F, -4.0F, 2.0F, 1.0F, 2.0F)
            /* chin */ .texOffs(26, 2).addBox(-0.5F, 1.0F, -3.0F, 1.0F, 1.0F, 1.0F)
            /* head */ .texOffs(10, 0).addBox(-1.0F, 0.0F, -2.0F, 2.0F, 2.0F, 2.0F)
            /* trunk */ .texOffs(0, 0).addBox(-1.0F, 0.0F, 0.0F, 2.0F, 2.0F, 3.0F)
            /* rear */ .texOffs(0, 5).addBox(-0.5F, 0.0F, 3.0F, 1.0F, 2.0F, 1.0F)
            /* stalk */ .texOffs(4, 5).addBox(-0.5F, 0.5F, 4.0F, 1.0F, 1.0F, 1.0F)
            /* dorsal */ .texOffs(8, 2).addBox(0.0F, -2.0F, 0.0F, 0.0F, 2.0F, 3.0F)
            /* pelvic */ .texOffs(20, 4).addBox(0.0F, 2.0F, 0.0F, 0.0F, 1.0F, 1.0F)
            /* anal */ .texOffs(22, 4).addBox(0.0F, 2.0F, 3.0F, 0.0F, 1.0F, 1.0F),
            PartPose.offset(0.0F, 21.0F, 0.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(14, 2).addBox(0.0F, -2.0F, 0.0F, 0.0F, 4.0F, 3.0F),
            PartPose.offset(0.0F, 22.0F, 5.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(22, 5).addBox(-1.0F, 0.0F, 0.0F, 1.0F, 0.0F, 2.0F),
            PartPose.offsetAndRotation(-1.0F, 23.0F, -1.0F, 0.0F, 0.0F, -1.2F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(24, 5).addBox(0.0F, 0.0F, 0.0F, 1.0F, 0.0F, 2.0F),
            PartPose.offsetAndRotation(1.0F, 23.0F, -1.0F, 0.0F, 0.0F, 1.2F));
        return LayerDefinition.create(mesh, 32, 32);
    }
}
