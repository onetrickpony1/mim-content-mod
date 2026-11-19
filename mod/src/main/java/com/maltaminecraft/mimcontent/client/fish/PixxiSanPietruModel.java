package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The pixxi San Pietru (John Dory): a very tall, thin oval disc, olive-grey to golden with a pale belly, St Peter's
 * dark ringed thumbprint in the middle of each side, a small gold-ringed eye high near the front, a big upturned jaw,
 * long dorsal spines trailing filaments, a low soft dorsal and anal fin, long dark pelvic fins and a rounded tail that
 * sways as it swims. Head toward -z, the ground at y 24.
 * Made by art/src/fish_pixxi_san_pietru_model.py (don't edit by hand). Texture: textures/entity/fish/pixxi_san_pietru.png (64 x 64).
 */
public class PixxiSanPietruModel extends FishModel {
    public PixxiSanPietruModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* col0 */ .texOffs(0, 0).addBox(-0.5F, -2.0F, -11.0F, 1.0F, 1.0F, 1.0F)
            /* col1 */ .texOffs(4, 0).addBox(-0.5F, -2.0F, -10.0F, 1.0F, 2.0F, 1.0F)
            /* col2 */ .texOffs(8, 0).addBox(-0.5F, -2.0F, -9.0F, 1.0F, 3.0F, 1.0F)
            /* col3 */ .texOffs(12, 0).addBox(-0.5F, -3.0F, -8.0F, 1.0F, 6.0F, 1.0F)
            /* col4 */ .texOffs(16, 0).addBox(-1.0F, -4.0F, -7.0F, 2.0F, 8.0F, 1.0F)
            /* col5 */ .texOffs(22, 0).addBox(-1.0F, -4.0F, -6.0F, 2.0F, 9.0F, 1.0F)
            /* col6 */ .texOffs(28, 0).addBox(-1.0F, -5.0F, -5.0F, 2.0F, 10.0F, 1.0F)
            /* col7 */ .texOffs(34, 0).addBox(-1.0F, -5.0F, -4.0F, 2.0F, 11.0F, 5.0F)
            /* col8 */ .texOffs(48, 0).addBox(-1.0F, -5.0F, 1.0F, 2.0F, 10.0F, 1.0F)
            /* col9 */ .texOffs(54, 0).addBox(-1.0F, -4.0F, 2.0F, 2.0F, 9.0F, 2.0F)
            /* col10 */ .texOffs(0, 16).addBox(-0.5F, -3.0F, 4.0F, 1.0F, 7.0F, 1.0F)
            /* col11 */ .texOffs(4, 16).addBox(-0.5F, -2.0F, 5.0F, 1.0F, 5.0F, 1.0F)
            /* col12 */ .texOffs(8, 16).addBox(-0.5F, -1.0F, 6.0F, 1.0F, 3.0F, 1.0F)
            /* soft_dorsal */ .texOffs(34, 12).addBox(0.0F, -7.0F, 2.0F, 0.0F, 5.0F, 4.0F)
            /* anal */ .texOffs(42, 9).addBox(0.0F, 3.0F, -1.0F, 0.0F, 4.0F, 7.0F)
            /* pelvic */ .texOffs(56, 12).addBox(0.0F, 5.0F, -6.0F, 0.0F, 2.0F, 4.0F),
            PartPose.offset(0.0F, 17.0F, 0.0F));
        PartDefinition topfinPart = root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* membrane */ .texOffs(12, 9).addBox(0.0F, -2.0F, 0.0F, 0.0F, 2.0F, 7.0F),
            PartPose.offset(0.0F, 12.0F, -5.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(0, 22).addBox(0.0F, -4.0F, 0.0F, 0.0F, 7.0F, 4.0F),
            PartPose.offset(0.0F, 17.0F, 7.0F));
        topfinPart.addOrReplaceChild("spine_0", CubeListBuilder.create()
            /* spine_0 */ .texOffs(26, 15).addBox(0.0F, -10.0F, 0.0F, 0.0F, 10.0F, 1.0F),
            PartPose.offsetAndRotation(0.0F, -2.0F, 0.0F, -0.785F, 0.0F, 0.0F));
        topfinPart.addOrReplaceChild("spine_1", CubeListBuilder.create()
            /* spine_1 */ .texOffs(28, 15).addBox(0.0F, -9.0F, 0.0F, 0.0F, 9.0F, 1.0F),
            PartPose.offsetAndRotation(0.0F, -2.0F, 2.0F, -0.785F, 0.0F, 0.0F));
        topfinPart.addOrReplaceChild("spine_2", CubeListBuilder.create()
            /* spine_2 */ .texOffs(30, 15).addBox(0.0F, -7.0F, 0.0F, 0.0F, 7.0F, 1.0F),
            PartPose.offsetAndRotation(0.0F, -1.0F, 4.0F, -0.785F, 0.0F, 0.0F));
        topfinPart.addOrReplaceChild("spine_3", CubeListBuilder.create()
            /* spine_3 */ .texOffs(32, 15).addBox(0.0F, -6.0F, 0.0F, 0.0F, 6.0F, 1.0F),
            PartPose.offsetAndRotation(0.0F, -1.0F, 6.0F, -0.785F, 0.0F, 0.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
