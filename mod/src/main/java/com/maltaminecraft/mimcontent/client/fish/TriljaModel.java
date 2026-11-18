package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The trilja (striped red mullet): a steep, blunt head with the eye high on it and two pale chin barbels tucked under
 * the throat, a red back, a yellow line along the flank, a pale pink belly, a tall striped first dorsal fin and a low
 * second one set apart, and a forked rosy tail that sways as it swims. 16 px long, 4 px deep, 3 px wide, head toward
 * -z, the ground at y 24.
 * Made by art/src/fish_trilja_model.py (don't edit by hand). Texture: textures/entity/fish/trilja.png (32 x 32).
 */
public class TriljaModel extends FishModel {
    public TriljaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* snout */ .texOffs(26, 0).addBox(-1.0F, 0.0F, -9.0F, 2.0F, 2.0F, 1.0F)
            /* head */ .texOffs(18, 0).addBox(-1.0F, -1.0F, -8.0F, 2.0F, 3.0F, 2.0F)
            /* trunk */ .texOffs(0, 0).addBox(-1.5F, -2.0F, -6.0F, 3.0F, 4.0F, 6.0F)
            /* rear */ .texOffs(0, 10).addBox(-1.0F, -2.0F, 0.0F, 2.0F, 3.0F, 2.0F)
            /* stalk */ .texOffs(8, 10).addBox(-0.5F, -1.0F, 2.0F, 1.0F, 2.0F, 2.0F)
            /* barbel_r */ .texOffs(20, 10).addBox(-0.5F, 2.0F, -9.0F, 0.0F, 1.0F, 2.0F)
            /* barbel_l */ .texOffs(24, 10).addBox(0.5F, 2.0F, -9.0F, 0.0F, 1.0F, 2.0F)
            /* dorsal2 */ .texOffs(20, 8).addBox(0.0F, -3.0F, 0.0F, 0.0F, 1.0F, 2.0F)
            /* anal */ .texOffs(24, 8).addBox(0.0F, 1.0F, 0.0F, 0.0F, 1.0F, 2.0F),
            PartPose.offset(0.0F, 21.0F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* dorsal1 */ .texOffs(14, 7).addBox(0.0F, -2.0F, 0.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offset(0.0F, 19.0F, -5.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(14, 11).addBox(0.0F, -3.0F, 0.0F, 0.0F, 6.0F, 3.0F),
            PartPose.offset(0.0F, 21.0F, 4.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(20, 20).addBox(-1.0F, 0.0F, 0.0F, 1.0F, 0.0F, 2.0F),
            PartPose.offsetAndRotation(-1.5F, 22.0F, -5.0F, 0.0F, 0.0F, -0.9F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(24, 20).addBox(0.0F, 0.0F, 0.0F, 1.0F, 0.0F, 2.0F),
            PartPose.offsetAndRotation(1.5F, 22.0F, -5.0F, 0.0F, 0.0F, 0.9F));
        return LayerDefinition.create(mesh, 32, 32);
    }
}
