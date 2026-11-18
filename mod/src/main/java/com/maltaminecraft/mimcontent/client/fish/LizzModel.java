package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The lizz (European barracuda): a long slim torpedo with a long pointed head and a jutting lower jaw, two small dorsal
 * fins set far apart, a dark slate back over silver sides with faint bars, a white belly and a dark forked tail that
 * sways as it swims. 24 px long, 3 px deep, 2 px wide, head toward -z, the ground at y 24.
 * Made by art/src/fish_lizz_model.py (don't edit by hand). Texture: textures/entity/fish/lizz.png (64 x 32).
 */
public class LizzModel extends FishModel {
    public LizzModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* jaw */ .texOffs(0, 0).addBox(-0.5F, 0.0F, -12.0F, 1.0F, 1.0F, 4.0F)
            /* snout */ .texOffs(11, 0).addBox(-0.5F, -1.0F, -11.0F, 1.0F, 1.0F, 3.0F)
            /* head */ .texOffs(20, 0).addBox(-1.0F, -1.0F, -8.0F, 2.0F, 2.0F, 3.0F)
            /* trunk */ .texOffs(31, 0).addBox(-1.0F, -2.0F, -5.0F, 2.0F, 3.0F, 8.0F)
            /* rear */ .texOffs(52, 0).addBox(-1.0F, -2.0F, 3.0F, 2.0F, 2.0F, 3.0F)
            /* stalk */ .texOffs(0, 12).addBox(-0.5F, -1.5F, 6.0F, 1.0F, 2.0F, 1.0F)
            /* pelvic */ .texOffs(5, 10).addBox(0.0F, 1.0F, -1.0F, 0.0F, 1.0F, 2.0F)
            /* anal */ .texOffs(10, 9).addBox(0.0F, 0.0F, 3.0F, 0.0F, 1.0F, 3.0F),
            PartPose.offset(0.0F, 21.0F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* dorsal1 */ .texOffs(17, 9).addBox(0.0F, -2.0F, 0.0F, 0.0F, 2.0F, 3.0F)
            /* dorsal2 */ .texOffs(24, 10).addBox(0.0F, -1.0F, 5.0F, 0.0F, 1.0F, 2.0F),
            PartPose.offset(0.0F, 19.0F, -2.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(29, 7).addBox(0.0F, -2.5F, 0.0F, 0.0F, 5.0F, 5.0F),
            PartPose.offset(0.0F, 20.5F, 7.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(38, 12).addBox(-1.0F, 0.0F, 0.0F, 1.0F, 0.0F, 2.0F),
            PartPose.offsetAndRotation(-1.0F, 22.0F, -5.0F, 0.0F, 0.0F, -0.9F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(41, 12).addBox(0.0F, 0.0F, 0.0F, 1.0F, 0.0F, 2.0F),
            PartPose.offsetAndRotation(1.0F, 22.0F, -5.0F, 0.0F, 0.0F, 0.9F));
        return LayerDefinition.create(mesh, 64, 32);
    }
}
