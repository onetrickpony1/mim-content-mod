package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * PLACEHOLDER model of the gallinella (tub gurnard: big bony head, red body, huge blue-edged pectoral 'wings', walks on its fin rays): plain boxes until the art round.
 * Made by art/src/fish_placeholders.py; the art makers replace this file, keeping the fish model contract
 * (docs/Tools and Process/Art pipeline.md, "Fish models"). Texture: textures/entity/fish/gallinella.png.
 * Parts, for the art makers to replace: body, top_fin, left_fin, right_fin, tail_fin.
 */
public class GallinellaModel extends FishModel {
    public GallinellaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            .texOffs(0, 0).addBox(-2.0F, -2.0F, -9.0F, 4.0F, 3.5F, 4.0F)
            .texOffs(16, 0).addBox(-1.5F, -1.5F, -5.0F, 3.0F, 3.0F, 11.0F),
            PartPose.offset(0.0F, 21.5F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            .texOffs(44, 0).addBox(0.0F, -2.0F, 0.0F, 0.0F, 2.0F, 6.0F),
            PartPose.offset(0.0F, 20.0F, -5.0F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            .texOffs(0, 14).addBox(0.0F, 0.0F, 0.0F, 5.0F, 0.0F, 5.0F),
            PartPose.offset(2.0F, 22.5F, -5.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            .texOffs(20, 14).addBox(-5.0F, 0.0F, 0.0F, 5.0F, 0.0F, 5.0F),
            PartPose.offset(-2.0F, 22.5F, -5.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            .texOffs(40, 14).addBox(0.0F, -2.0F, 0.0F, 0.0F, 4.0F, 3.0F),
            PartPose.offset(0.0F, 21.5F, 6.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
