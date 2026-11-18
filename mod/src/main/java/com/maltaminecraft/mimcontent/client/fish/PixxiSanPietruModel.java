package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * PLACEHOLDER model of the pixxi_san_pietru (John Dory: tall, very thin, olive-grey with a dark St Peter's thumbprint spot, long spiny dorsal filaments): plain boxes until the art round.
 * Made by art/src/fish_placeholders.py; the art makers replace this file, keeping the fish model contract
 * (docs/Tools and Process/Art pipeline.md, "Fish models"). Texture: textures/entity/fish/pixxi_san_pietru.png.
 * Parts, for the art makers to replace: body, top_fin, tail_fin.
 */
public class PixxiSanPietruModel extends FishModel {
    public PixxiSanPietruModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            .texOffs(0, 0).addBox(-1.0F, -6.0F, -7.0F, 2.0F, 12.0F, 12.0F)
            .texOffs(28, 0).addBox(-0.5F, -1.0F, -9.0F, 1.0F, 2.0F, 2.0F),
            PartPose.offset(0.0F, 17.0F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            .texOffs(34, 0).addBox(0.0F, -3.0F, 0.0F, 0.0F, 3.0F, 9.0F),
            PartPose.offset(0.0F, 11.0F, -5.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            .texOffs(52, 0).addBox(0.0F, -2.5F, 0.0F, 0.0F, 5.0F, 3.0F),
            PartPose.offset(0.0F, 17.0F, 5.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
