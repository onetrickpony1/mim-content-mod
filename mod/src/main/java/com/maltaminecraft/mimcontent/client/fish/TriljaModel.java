package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * PLACEHOLDER model of the trilja (striped red mullet: steep head, two chin barbels, red-pink with a yellow stripe): plain boxes until the art round.
 * Made by art/src/fish_placeholders.py; the art makers replace this file, keeping the fish model contract
 * (docs/Tools and Process/Art pipeline.md, "Fish models"). Texture: textures/entity/fish/trilja.png.
 * Parts, for the art makers to replace: body, top_fin, tail_fin.
 */
public class TriljaModel extends FishModel {
    public TriljaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            .texOffs(0, 0).addBox(-1.0F, -1.5F, -6.0F, 2.0F, 3.0F, 10.0F)
            .texOffs(24, 0).addBox(0.0F, 1.5F, -6.0F, 0.0F, 1.0F, 1.0F),
            PartPose.offset(0.0F, 21.5F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            .texOffs(26, 0).addBox(0.0F, -2.0F, 0.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offset(0.0F, 20.0F, -4.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            .texOffs(32, 0).addBox(0.0F, -2.0F, 0.0F, 0.0F, 4.0F, 3.0F),
            PartPose.offset(0.0F, 21.5F, 4.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
