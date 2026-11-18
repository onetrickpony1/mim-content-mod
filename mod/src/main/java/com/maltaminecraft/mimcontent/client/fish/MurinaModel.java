package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * PLACEHOLDER model of the murina (Mediterranean moray: long, thin, dark brown mottled with yellow): plain boxes until the art round.
 * Made by art/src/fish_placeholders.py; the art makers replace this file, keeping the fish model contract
 * (docs/Tools and Process/Art pipeline.md, "Fish models"). Texture: textures/entity/fish/murina.png.
 */
public class MurinaModel extends FishModel {
    public MurinaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            .texOffs(0, 0).addBox(-1.0F, -1.5F, -9.0F, 2.0F, 3.0F, 9.0F),
            PartPose.offset(0.0F, 22.5F, 0.0F));
        PartDefinition tail = root.addOrReplaceChild("tail", CubeListBuilder.create()
            .texOffs(22, 0).addBox(-1.0F, -1.5F, 0.0F, 2.0F, 3.0F, 8.0F)
            .texOffs(42, 0).addBox(0.0F, -2.5F, 0.0F, 0.0F, 1.0F, 8.0F),
            PartPose.offset(0.0F, 22.5F, 0.0F));
        tail.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            .texOffs(58, 0).addBox(0.0F, -1.5F, 0.0F, 0.0F, 3.0F, 2.0F),
            PartPose.offset(0.0F, 0.0F, 8.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
