package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * PLACEHOLDER model of the petrica (anglerfish: huge flat head and wide mouth, mottled brown, a fishing-rod lure on the head): plain boxes until the art round.
 * Made by art/src/fish_placeholders.py; the art makers replace this file, keeping the fish model contract
 * (docs/Tools and Process/Art pipeline.md, "Fish models"). Texture: textures/entity/fish/petrica.png.
 * Parts, for the art makers to replace: body, lure, left_fin, right_fin, tail_fin.
 */
public class PetricaModel extends FishModel {
    public PetricaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            .texOffs(0, 0).addBox(-5.0F, -2.0F, -10.0F, 10.0F, 4.0F, 10.0F)
            .texOffs(40, 0).addBox(-4.0F, 0.0F, -11.0F, 8.0F, 2.0F, 1.0F)
            .texOffs(0, 14).addBox(-1.5F, -1.5F, 0.0F, 3.0F, 3.0F, 8.0F),
            PartPose.offset(0.0F, 22.0F, 0.0F));
        root.addOrReplaceChild("lure", CubeListBuilder.create()
            .texOffs(22, 14).addBox(0.0F, -3.0F, 0.0F, 0.0F, 3.0F, 1.0F),
            PartPose.offset(0.0F, 20.0F, -9.0F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            .texOffs(24, 14).addBox(0.0F, 0.0F, 0.0F, 3.0F, 0.0F, 3.0F),
            PartPose.offset(5.0F, 23.0F, -4.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            .texOffs(36, 14).addBox(-3.0F, 0.0F, 0.0F, 3.0F, 0.0F, 3.0F),
            PartPose.offset(-5.0F, 23.0F, -4.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            .texOffs(48, 14).addBox(0.0F, -2.0F, 0.0F, 0.0F, 4.0F, 3.0F),
            PartPose.offset(0.0F, 22.0F, 8.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
