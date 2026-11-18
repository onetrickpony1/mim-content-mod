package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The cawl (Mediterranean damselfish, the brown adult): small, with a deep, oval, flat-sided body, dark chocolate
 * brown with the large scales showing as a net, a blunt rounded head with a small mouth and a big eye, one long dark
 * dorsal fin, dark anal and pelvic fins, and a deeply forked tail with pale lobe tips that sways as it swims.
 * 14 px long, 5 px deep, 2 px thick, head toward -z, the ground at y 24.
 * Made by art/src/fish_cawl_model.py (don't edit by hand). Texture: textures/entity/fish/cawl.png (32 x 32).
 */
public class CawlModel extends FishModel {
    public CawlModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* lip */ .texOffs(26, 0).addBox(-0.5F, 0.0F, -7.0F, 1.0F, 2.0F, 1.0F)
            /* snout */ .texOffs(20, 4).addBox(-1.0F, -1.0F, -6.0F, 2.0F, 3.0F, 1.0F)
            /* trunk */ .texOffs(0, 0).addBox(-1.0F, -2.0F, -5.0F, 2.0F, 5.0F, 4.0F)
            /* rear */ .texOffs(12, 0).addBox(-1.0F, -2.0F, -1.0F, 2.0F, 4.0F, 2.0F)
            /* stalk */ .texOffs(20, 0).addBox(-0.5F, -1.0F, 1.0F, 1.0F, 2.0F, 2.0F)
            /* dorsal */ .texOffs(8, 2).addBox(0.0F, -4.0F, -4.0F, 0.0F, 3.0F, 7.0F)
            /* anal */ .texOffs(8, 8).addBox(0.0F, 1.0F, -1.0F, 0.0F, 3.0F, 4.0F)
            /* pelvic */ .texOffs(16, 9).addBox(0.0F, 3.0F, -4.0F, 0.0F, 1.0F, 3.0F),
            PartPose.offset(0.0F, 20.0F, 0.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(0, 5).addBox(0.0F, -4.0F, 0.0F, 0.0F, 8.0F, 4.0F),
            PartPose.offset(0.0F, 20.0F, 3.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(16, 10).addBox(0.0F, 0.0F, 0.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offsetAndRotation(-1.05F, 20.0F, -3.0F, 0.0F, -0.4F, 0.0F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(22, 10).addBox(0.0F, 0.0F, 0.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offsetAndRotation(1.05F, 20.0F, -3.0F, 0.0F, 0.4F, 0.0F));
        return LayerDefinition.create(mesh, 32, 32);
    }
}
