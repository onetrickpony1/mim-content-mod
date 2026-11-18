package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The sardina (sardine): small and slim, a blue-green back over bright silver sides, a row of dark spots behind the
 * gold-tinged gill cover, a big eye, one short dorsal fin mid-back, small pelvic and anal fins and a forked tail that
 * sways as it swims. 14 px long, 3 px deep, head toward -z, the ground at y 24.
 * Made by art/src/fish_sardina_model.py (don't edit by hand). Texture: textures/entity/fish/sardina.png (32 x 32).
 */
public class SardinaModel extends FishModel {
    public SardinaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* snout */ .texOffs(24, 0).addBox(-1.0F, 1.0F, -6.0F, 2.0F, 2.0F, 1.0F)
            /* head */ .texOffs(14, 0).addBox(-1.0F, 0.0F, -5.0F, 2.0F, 3.0F, 3.0F)
            /* trunk */ .texOffs(0, 0).addBox(-1.0F, 0.0F, -2.0F, 2.0F, 3.0F, 5.0F)
            /* rear */ .texOffs(0, 8).addBox(-1.0F, 0.0F, 3.0F, 2.0F, 2.0F, 2.0F)
            /* dorsal */ .texOffs(14, 5).addBox(0.0F, -2.0F, -1.0F, 0.0F, 2.0F, 3.0F)
            /* pelvic */ .texOffs(14, 10).addBox(0.0F, 3.0F, 1.0F, 0.0F, 1.0F, 1.0F)
            /* anal */ .texOffs(18, 9).addBox(0.0F, 2.0F, 3.0F, 0.0F, 1.0F, 2.0F),
            PartPose.offset(0.0F, 20.0F, 0.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(8, 10).addBox(0.0F, -2.5F, 0.0F, 0.0F, 5.0F, 3.0F),
            PartPose.offset(0.0F, 21.0F, 5.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(20, 8).addBox(-1.0F, 0.0F, 0.0F, 1.0F, 0.0F, 2.0F),
            PartPose.offsetAndRotation(-1.0F, 22.5F, -2.0F, 0.0F, 0.0F, -0.7F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(24, 8).addBox(0.0F, 0.0F, 0.0F, 1.0F, 0.0F, 2.0F),
            PartPose.offsetAndRotation(1.0F, 22.5F, -2.0F, 0.0F, 0.0F, 0.7F));
        return LayerDefinition.create(mesh, 32, 32);
    }
}
