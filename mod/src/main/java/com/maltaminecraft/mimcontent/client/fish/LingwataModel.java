package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The lingwata (common sole, Solea solea): a thin, oval, tongue-shaped flatfish lying on its blind side. A 1 px
 * fringe plate (the dorsal and anal fins running all round the edge, lighter, with ray ticks) round a 2 px body;
 * both eyes on the upper side near the front, one behind the other on a slant, each ringed; the small raised
 * pectoral fin with its dark tip; a small rounded tail fin that sways. Sandy brown with darker speckles above,
 * white below.
 * Made by art/src/fish_lingwata_model.py (do not edit by hand); texture textures/entity/fish/lingwata.png.
 * Parts: body (with the child pectoral_fin) and tail_fin. Lies flat on land (MimContentClient, liesFlat).
 */
public class LingwataModel extends FishModel {
    public LingwataModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition body = root.addOrReplaceChild("body", CubeListBuilder.create()
            /* c1_x-5_0 */ .texOffs(96, 82).addBox(-5.0F, 0.0F, -8.0F, 1.0F, 1.0F, 10.0F)
            /* c1_x-4_0 */ .texOffs(76, 63).addBox(-4.0F, 0.0F, -10.0F, 1.0F, 1.0F, 15.0F)
            /* c1_x-3_0 */ .texOffs(40, 43).addBox(-3.0F, 0.0F, -11.0F, 1.0F, 1.0F, 18.0F)
            /* c1_x-2_0 */ .texOffs(0, 22).addBox(-2.0F, 0.0F, -12.0F, 1.0F, 1.0F, 20.0F)
            /* c1_x-1_0 */ .texOffs(0, 0).addBox(-1.0F, 0.0F, -12.0F, 1.0F, 1.0F, 21.0F)
            /* c1_x0_0 */ .texOffs(44, 0).addBox(0.0F, 0.0F, -12.0F, 1.0F, 1.0F, 21.0F)
            /* c1_x1_0 */ .texOffs(42, 22).addBox(1.0F, 0.0F, -12.0F, 1.0F, 1.0F, 20.0F)
            /* c1_x2_0 */ .texOffs(78, 43).addBox(2.0F, 0.0F, -11.0F, 1.0F, 1.0F, 18.0F)
            /* c1_x3_0 */ .texOffs(0, 82).addBox(3.0F, 0.0F, -10.0F, 1.0F, 1.0F, 15.0F)
            /* c1_x4_0 */ .texOffs(0, 98).addBox(4.0F, 0.0F, -8.0F, 1.0F, 1.0F, 10.0F)
            /* c2_x-4_0 */ .texOffs(22, 98).addBox(-4.0F, -1.0F, -8.0F, 1.0F, 1.0F, 10.0F)
            /* c2_x-3_0 */ .texOffs(32, 82).addBox(-3.0F, -1.0F, -10.0F, 1.0F, 1.0F, 15.0F)
            /* c2_x-2_0 */ .texOffs(0, 63).addBox(-2.0F, -1.0F, -11.0F, 1.0F, 1.0F, 18.0F)
            /* c2_x-1_0 */ .texOffs(84, 22).addBox(-1.0F, -1.0F, -11.0F, 1.0F, 1.0F, 19.0F)
            /* c2_x0_0 */ .texOffs(0, 43).addBox(0.0F, -1.0F, -11.0F, 1.0F, 1.0F, 19.0F)
            /* c2_x1_0 */ .texOffs(38, 63).addBox(1.0F, -1.0F, -11.0F, 1.0F, 1.0F, 18.0F)
            /* c2_x2_0 */ .texOffs(64, 82).addBox(2.0F, -1.0F, -10.0F, 1.0F, 1.0F, 15.0F)
            /* c2_x3_0 */ .texOffs(44, 98).addBox(3.0F, -1.0F, -8.0F, 1.0F, 1.0F, 10.0F),
            PartPose.offset(0.0F, 23.0F, 0.0F));
        body.addOrReplaceChild("pectoral_fin", CubeListBuilder.create()
            /* pectoral */ .texOffs(90, 98).addBox(-4.0F, 0.0F, 0.0F, 2.0F, 0.0F, 2.0F),
            PartPose.offsetAndRotation(0.0F, -1.02F, -2.0F, 0.42F, 0.0F, 0.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* tail_x-2 */ .texOffs(66, 98).addBox(-2.0F, -0.5F, -0.5F, 1.0F, 1.0F, 2.0F)
            /* tail_x-1 */ .texOffs(72, 98).addBox(-1.0F, -0.5F, 0.5F, 1.0F, 1.0F, 2.0F)
            /* tail_x0 */ .texOffs(78, 98).addBox(0.0F, -0.5F, 0.5F, 1.0F, 1.0F, 2.0F)
            /* tail_x1 */ .texOffs(84, 98).addBox(1.0F, -0.5F, -0.5F, 1.0F, 1.0F, 2.0F),
            PartPose.offset(0.0F, 23.5F, 8.5F));
        return LayerDefinition.create(mesh, 128, 128);
    }
}
