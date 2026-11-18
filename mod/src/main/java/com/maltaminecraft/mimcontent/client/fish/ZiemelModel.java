package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The ziemel tal-bahar (seahorse), upright: a horse-like head bent forward on its neck, a long tubular snout, a small
 * crown with a tuft of filaments behind it, a pot belly, bony rings along the body and a thin tail curled forward
 * into a hook. Golden ochre with small pale dots. Bigger than life so its detail shows: 13 px tall (0.81 blocks),
 * 9 px from snout tip to dorsal fin, head toward -z, the ground at y 24.
 * The dorsal fin is the "tail_fin" (it flutters from side to side), the curled tail is the "tail" (it sways gently).
 * Made by art/src/fish_ziemel_model.py (don't edit by hand). Texture: textures/entity/fish/ziemel.png (32 x 32).
 */
public class ZiemelModel extends FishModel {
    public ZiemelModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* coronet */ .texOffs(22, 17).addBox(-0.5F, -7.0F, 1.0F, 1.0F, 1.0F, 1.0F)
            /* head_top */ .texOffs(0, 17).addBox(-1.0F, -6.0F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* head */ .texOffs(12, 8).addBox(-1.0F, -5.0F, -1.0F, 2.0F, 2.0F, 3.0F)
            /* snout */ .texOffs(18, 13).addBox(-0.5F, -4.0F, -4.0F, 1.0F, 1.0F, 3.0F)
            /* neck */ .texOffs(8, 17).addBox(-1.0F, -3.0F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* chest */ .texOffs(0, 8).addBox(-1.0F, -2.0F, -1.0F, 2.0F, 1.0F, 4.0F)
            /* belly */ .texOffs(4, 0).addBox(-1.5F, -1.0F, -2.0F, 3.0F, 2.0F, 5.0F)
            /* belly_lo */ .texOffs(20, 0).addBox(-1.0F, 1.0F, -1.0F, 2.0F, 1.0F, 4.0F)
            /* mane */ .texOffs(0, 0).addBox(0.0F, -7.0F, 2.0F, 0.0F, 6.0F, 2.0F),
            PartPose.offset(0.0F, 18.0F, 0.0F));
        root.addOrReplaceChild("tail", CubeListBuilder.create()
            /* tail1 */ .texOffs(0, 13).addBox(-1.0F, 0.0F, -2.0F, 2.0F, 1.0F, 3.0F)
            /* tail2 */ .texOffs(16, 17).addBox(-0.5F, 1.0F, -1.0F, 1.0F, 1.0F, 2.0F)
            /* tail3 */ .texOffs(26, 17).addBox(-0.5F, 2.0F, -1.0F, 1.0F, 1.0F, 1.0F)
            /* curl */ .texOffs(10, 13).addBox(-0.5F, 3.0F, -3.0F, 1.0F, 1.0F, 3.0F)
            /* tip */ .texOffs(0, 20).addBox(-0.5F, 2.0F, -3.0F, 1.0F, 1.0F, 1.0F),
            PartPose.offset(0.0F, 20.0F, 2.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* dorsal */ .texOffs(22, 8).addBox(0.0F, -1.5F, 0.0F, 0.0F, 3.0F, 2.0F),
            PartPose.offset(0.0F, 19.5F, 3.0F));
        return LayerDefinition.create(mesh, 32, 32);
    }
}
