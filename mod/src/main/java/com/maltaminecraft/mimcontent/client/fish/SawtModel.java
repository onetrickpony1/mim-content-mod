package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The sawt (lesser weever): a slim sandy fish, deepest at the head, with an upturned mouth, eyes on top of the head,
 * the short jet-black venomous first dorsal fin over the shoulders, a long low pale second dorsal, pale fan pectorals
 * spread on the sand and a square yellow tail with a black edge that sways. 14 px long, 4 px deep at the head, 3 wide;
 * it sits 1 px into the floor so on the sand it looks half buried. Head toward -z, the ground at y 24.
 * Texture: textures/entity/fish/sawt.png (32 x 32). Made by art/src/fish_sawt_model.py (don't edit by hand).
 */
public class SawtModel extends FishModel {
    public SawtModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* head */ .texOffs(0, 0).addBox(-1.5F, -2.0F, -6.0F, 3.0F, 4.0F, 3.0F)
            /* trunk */ .texOffs(13, 0).addBox(-1.0F, -1.0F, -3.0F, 2.0F, 3.0F, 4.0F)
            /* rear */ .texOffs(7, 8).addBox(-1.0F, 0.0F, 1.0F, 2.0F, 2.0F, 3.0F)
            /* stalk */ .texOffs(5, 15).addBox(-0.5F, 0.0F, 4.0F, 1.0F, 1.0F, 1.0F)
            /* dorsal2 */ .texOffs(18, 8).addBox(0.0F, -1.0F, 1.0F, 0.0F, 1.0F, 4.0F),
            PartPose.offset(0.0F, 23.0F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* dorsal1 */ .texOffs(0, 8).addBox(0.0F, -2.0F, 0.0F, 0.0F, 3.0F, 3.0F),
            PartPose.offset(0.0F, 22.0F, -3.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(0, 15).addBox(0.0F, 0.0F, 0.0F, 0.0F, 1.0F, 2.0F),
            PartPose.offsetAndRotation(-1.0F, 23.0F, -3.0F, 0.0F, -0.6F, 0.6F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(27, 8).addBox(0.0F, 0.0F, 0.0F, 0.0F, 1.0F, 2.0F),
            PartPose.offsetAndRotation(1.0F, 23.0F, -3.0F, 0.0F, 0.6F, -0.6F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(26, 0).addBox(0.0F, -2.0F, 0.0F, 0.0F, 4.0F, 3.0F),
            PartPose.offset(0.0F, 23.5F, 5.0F));
        return LayerDefinition.create(mesh, 32, 32);
    }
}
