package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The trilja (striped red mullet): a steep, blunt head with the eye high on it and two pale chin barbels hanging
 * from under the chin, a red back, a yellow line along the flank, a pale pink belly, a striped first dorsal fin and a
 * low second one set apart, and a forked rosy tail that sways as it swims. 15 px long, 4 px deep, 2 px wide, head
 * toward -z, the ground at y 24.
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
            /* head */ .texOffs(18, 0).addBox(-1.0F, -1.0F, -8.0F, 2.0F, 3.0F, 2.0F)
            /* trunk */ .texOffs(0, 0).addBox(-1.0F, -2.0F, -6.0F, 2.0F, 4.0F, 5.0F)
            /* rear */ .texOffs(0, 10).addBox(-1.0F, -2.0F, -1.0F, 2.0F, 3.0F, 3.0F)
            /* stalk */ .texOffs(10, 10).addBox(-0.5F, -1.0F, 2.0F, 1.0F, 2.0F, 2.0F)
            /* dorsal2 */ .texOffs(22, 8).addBox(0.0F, -3.0F, 0.0F, 0.0F, 1.0F, 2.0F)
            /* anal */ .texOffs(26, 8).addBox(0.0F, 1.0F, 0.0F, 0.0F, 1.0F, 2.0F),
            PartPose.offset(0.0F, 21.0F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* dorsal1 */ .texOffs(16, 7).addBox(0.0F, -2.0F, 0.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offset(0.0F, 19.0F, -5.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(16, 11).addBox(0.0F, -3.0F, 0.0F, 0.0F, 6.0F, 3.0F),
            PartPose.offset(0.0F, 21.0F, 4.0F));
        root.addOrReplaceChild("barbel_r", CubeListBuilder.create()
            /* barbel_r */ .texOffs(22, 13).addBox(0.0F, 0.0F, 0.0F, 0.0F, 2.0F, 1.0F),
            PartPose.offsetAndRotation(-0.9F, 23.0F, -7.0F, 0.26F, 0.0F, 0.0F));
        root.addOrReplaceChild("barbel_l", CubeListBuilder.create()
            /* barbel_l */ .texOffs(26, 13).addBox(0.0F, 0.0F, 0.0F, 0.0F, 2.0F, 1.0F),
            PartPose.offsetAndRotation(0.9F, 23.0F, -7.0F, 0.26F, 0.0F, 0.0F));
        return LayerDefinition.create(mesh, 32, 32);
    }
}
