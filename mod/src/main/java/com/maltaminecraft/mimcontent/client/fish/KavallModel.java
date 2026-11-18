package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The kavall (chub mackerel): a torpedo with a pointed snout and a big eye, a blue-green back crossed by dark wavy
 * bars, silver sides and a pale belly with faint spots, two dorsal fins set apart, small finlets before a deeply
 * forked olive-yellow tail that sways as it swims. 21 px long, 4 px deep, 3 px wide, head toward -z, the ground at y 24.
 * Made by art/src/fish_kavall_model.py (don't edit by hand). Texture: textures/entity/fish/kavall.png (32 x 32).
 */
public class KavallModel extends FishModel {
    public KavallModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* snout */ .texOffs(22, 7).addBox(-0.5F, -1.0F, -10.0F, 1.0F, 2.0F, 1.0F)
            /* head */ .texOffs(22, 0).addBox(-1.0F, -2.0F, -9.0F, 2.0F, 4.0F, 3.0F)
            /* trunk */ .texOffs(0, 0).addBox(-1.5F, -2.0F, -6.0F, 3.0F, 4.0F, 8.0F)
            /* rear */ .texOffs(0, 12).addBox(-1.0F, -2.0F, 2.0F, 2.0F, 3.0F, 3.0F)
            /* stalk */ .texOffs(10, 12).addBox(-0.5F, -1.0F, 5.0F, 1.0F, 2.0F, 2.0F)
            /* dorsal2 */ .texOffs(24, 13).addBox(0.0F, -4.0F, 1.0F, 0.0F, 2.0F, 1.0F)
            /* anal */ .texOffs(26, 12).addBox(0.0F, 2.0F, 0.0F, 0.0F, 1.0F, 2.0F)
            /* pelvic */ .texOffs(26, 13).addBox(0.0F, 2.0F, -4.0F, 0.0F, 1.0F, 2.0F)
            /* finlets_top */ .texOffs(24, 15).addBox(0.0F, -2.0F, 6.0F, 0.0F, 1.0F, 1.0F)
            /* finlets_bot */ .texOffs(26, 15).addBox(0.0F, 1.0F, 6.0F, 0.0F, 1.0F, 1.0F),
            PartPose.offset(0.0F, 21.0F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* dorsal1 */ .texOffs(24, 9).addBox(0.0F, -2.0F, 0.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offset(0.0F, 19.0F, -5.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(16, 8).addBox(0.0F, -3.0F, 0.0F, 0.0F, 6.0F, 4.0F),
            PartPose.offset(0.0F, 21.0F, 7.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(-2, 18).addBox(-1.0F, 0.0F, 0.0F, 1.0F, 0.0F, 2.0F),
            PartPose.offsetAndRotation(-1.5F, 21.0F, -5.0F, 0.0F, 0.0F, -0.9F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(0, 18).addBox(0.0F, 0.0F, 0.0F, 1.0F, 0.0F, 2.0F),
            PartPose.offsetAndRotation(1.5F, 21.0F, -5.0F, 0.0F, 0.0F, 0.9F));
        return LayerDefinition.create(mesh, 32, 32);
    }
}
