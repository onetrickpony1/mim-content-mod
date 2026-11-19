package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The hmar (grey triggerfish): a deep, flat-sided rhomboid body in olive-grey with faint darker saddles and a pale
 * belly, a small pale-lipped mouth at the tip of a long sloping snout, an eye set high and far back, the stout trigger
 * spine, long matching soft dorsal and anal fins far back, and a lyre tail with pointed tips that sways as it swims.
 * 17 px long, 9 px deep (13 with the fins), 3 px thick, head toward -z, the ground at y 24.
 * Made by art/src/fish_hmar_model.py (don't edit by hand). Texture: textures/entity/fish/hmar.png (64 x 32).
 */
public class HmarModel extends FishModel {
    public HmarModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* body0 */ .texOffs(0, 0).addBox(-0.5F, 0.0F, -7.0F, 1.0F, 2.0F, 1.0F)
            /* body1 */ .texOffs(4, 0).addBox(-1.0F, -1.0F, -6.0F, 2.0F, 3.0F, 1.0F)
            /* body2 */ .texOffs(10, 0).addBox(-1.0F, -2.0F, -5.0F, 2.0F, 5.0F, 1.0F)
            /* body3 */ .texOffs(16, 0).addBox(-1.0F, -3.0F, -4.0F, 2.0F, 6.0F, 1.0F)
            /* body4 */ .texOffs(22, 0).addBox(-1.5F, -4.0F, -3.0F, 3.0F, 8.0F, 2.0F)
            /* body5 */ .texOffs(32, 0).addBox(-1.5F, -4.0F, -1.0F, 3.0F, 7.0F, 1.0F)
            /* body6 */ .texOffs(40, 0).addBox(-1.5F, -3.0F, 0.0F, 3.0F, 6.0F, 1.0F)
            /* body7 */ .texOffs(48, 0).addBox(-1.0F, -3.0F, 1.0F, 2.0F, 6.0F, 1.0F)
            /* body8 */ .texOffs(54, 0).addBox(-1.0F, -2.0F, 2.0F, 2.0F, 4.0F, 1.0F)
            /* body9 */ .texOffs(0, 10).addBox(-1.0F, -2.0F, 3.0F, 2.0F, 3.0F, 2.0F)
            /* dorsal */ .texOffs(0, 10).addBox(0.0F, -6.0F, 0.0F, 0.0F, 4.0F, 5.0F)
            /* anal */ .texOffs(10, 10).addBox(0.0F, 1.0F, 0.0F, 0.0F, 5.0F, 5.0F),
            PartPose.offset(0.0F, 16.0F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* trigger */ .texOffs(28, 15).addBox(-0.5F, -2.0F, 0.0F, 1.0F, 2.0F, 1.0F)
            /* trigger_tip */ .texOffs(32, 15).addBox(-0.5F, -3.0F, 1.0F, 1.0F, 3.0F, 1.0F)
            /* membrane */ .texOffs(36, 14).addBox(0.0F, -1.0F, 2.0F, 0.0F, 1.0F, 1.0F),
            PartPose.offset(0.0F, 12.0F, -3.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(20, 11).addBox(0.0F, -4.0F, 0.0F, 0.0F, 9.0F, 4.0F),
            PartPose.offset(0.0F, 15.0F, 5.0F));
        return LayerDefinition.create(mesh, 64, 32);
    }
}
