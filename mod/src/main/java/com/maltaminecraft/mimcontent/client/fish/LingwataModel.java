package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * PLACEHOLDER model of the lingwata (common sole: flat oval lying on its side, both eyes on top, brown above, white below): plain boxes until the art round.
 * Made by art/src/fish_placeholders.py; the art makers replace this file, keeping the fish model contract
 * (docs/Tools and Process/Art pipeline.md, "Fish models"). Texture: textures/entity/fish/lingwata.png.
 * Parts, for the art makers to replace: body, tail_fin.
 */
public class LingwataModel extends FishModel {
    public LingwataModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            .texOffs(0, 0).addBox(-4.0F, -0.75F, -8.0F, 8.0F, 1.5F, 14.0F)
            .texOffs(44, 0).addBox(-2.5F, -0.75F, -9.0F, 5.0F, 1.5F, 1.0F),
            PartPose.offset(0.0F, 23.25F, 0.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            .texOffs(0, 16).addBox(-2.5F, 0.0F, 0.0F, 5.0F, 0.0F, 3.0F),
            PartPose.offset(0.0F, 23.25F, 6.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
