package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The awrata (gilthead sea bream): an oval, deep but flat body, silver-grey under a blue-grey back with thin darker
 * lines, a gold band across the forehead between the eyes, a dark patch with a red-orange touch at the top of the gill
 * cover, a steep rounded forehead over a small thick-lipped mouth, one long dorsal fin and a forked tail with darker
 * edges that sways as it swims. 23 px long, 8 px deep, 3 px thick, head toward -z, the ground at y 24.
 * Made by art/src/fish_awrata_model.py (don't edit by hand). Texture: textures/entity/fish/awrata.png (64 x 32).
 */
public class AwrataModel extends FishModel {
    public AwrataModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* lips */ .texOffs(58, 6).addBox(-1.0F, 0.0F, -11.0F, 2.0F, 2.0F, 1.0F)
            /* snout */ .texOffs(52, 6).addBox(-1.0F, -1.0F, -10.0F, 2.0F, 4.0F, 1.0F)
            /* face */ .texOffs(52, 0).addBox(-1.5F, -2.0F, -9.0F, 3.0F, 5.0F, 1.0F)
            /* brow */ .texOffs(32, 0).addBox(-1.5F, -3.0F, -8.0F, 3.0F, 6.0F, 1.0F)
            /* head */ .texOffs(56, 11).addBox(-1.5F, -3.0F, -7.0F, 3.0F, 7.0F, 1.0F)
            /* trunk */ .texOffs(0, 0).addBox(-1.5F, -4.0F, -6.0F, 3.0F, 8.0F, 5.0F)
            /* rear */ .texOffs(16, 0).addBox(-1.5F, -3.0F, -1.0F, 3.0F, 6.0F, 4.0F)
            /* rear2 */ .texOffs(32, 10).addBox(-1.0F, -2.0F, 3.0F, 2.0F, 4.0F, 2.0F)
            /* stalk */ .texOffs(24, 10).addBox(-1.0F, -1.0F, 5.0F, 2.0F, 2.0F, 2.0F)
            /* dorsal */ .texOffs(0, 4).addBox(0.0F, -6.0F, -7.0F, 0.0F, 3.0F, 10.0F)
            /* anal */ .texOffs(22, 12).addBox(0.0F, 2.0F, -1.0F, 0.0F, 3.0F, 5.0F)
            /* pelvic */ .texOffs(32, 14).addBox(0.0F, 4.0F, -5.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offset(0.0F, 19.0F, 0.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(42, -5).addBox(0.0F, -5.0F, 0.0F, 0.0F, 10.0F, 5.0F),
            PartPose.offset(0.0F, 19.0F, 7.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(38, 14).addBox(0.0F, 0.0F, 0.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offsetAndRotation(-1.55F, 20.0F, -5.0F, 0.0F, -0.4F, 0.0F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(44, 14).addBox(0.0F, 0.0F, 0.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offsetAndRotation(1.55F, 20.0F, -5.0F, 0.0F, 0.4F, 0.0F));
        return LayerDefinition.create(mesh, 64, 32);
    }
}
