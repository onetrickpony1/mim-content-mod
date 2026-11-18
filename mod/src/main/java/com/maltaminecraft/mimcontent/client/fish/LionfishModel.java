package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * PLACEHOLDER model of the lionfish (lionfish: red-brown and white bands, tall venomous dorsal spines, big fan pectoral fins): plain boxes until the art round.
 * Made by art/src/fish_placeholders.py; the art makers replace this file, keeping the fish model contract
 * (docs/Tools and Process/Art pipeline.md, "Fish models"). Texture: textures/entity/fish/lionfish.png.
 * Parts, for the art makers to replace: body, top_fin, left_fin, right_fin, tail_fin.
 */
public class LionfishModel extends FishModel {
    public LionfishModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            .texOffs(0, 0).addBox(-1.5F, -2.5F, -6.0F, 3.0F, 5.0F, 11.0F)
            .texOffs(28, 0).addBox(-1.0F, -1.0F, -7.0F, 2.0F, 2.0F, 1.0F),
            PartPose.offset(0.0F, 20.5F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            .texOffs(34, 0).addBox(0.0F, -5.0F, 0.0F, 0.0F, 5.0F, 9.0F),
            PartPose.offset(0.0F, 18.0F, -5.0F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            .texOffs(0, 16).addBox(0.0F, 0.0F, 0.0F, 4.0F, 0.0F, 6.0F),
            PartPose.offset(1.5F, 21.0F, -3.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            .texOffs(20, 16).addBox(-4.0F, 0.0F, 0.0F, 4.0F, 0.0F, 6.0F),
            PartPose.offset(-1.5F, 21.0F, -3.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            .texOffs(40, 16).addBox(0.0F, -2.5F, 0.0F, 0.0F, 5.0F, 3.0F),
            PartPose.offset(0.0F, 20.5F, 5.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
