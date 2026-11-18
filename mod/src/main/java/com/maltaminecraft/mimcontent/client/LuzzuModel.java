package com.maltaminecraft.mimcontent.client;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.client.model.object.boat.AbstractBoatModel;

/**
 * The luzzu's model: a double-ended hull whose halves are chains of segments, each tilted a little more than the
 * one inside it, so the sheer sweeps up to raked stem and stern posts; rubbing strakes and two long oars (rowed
 * like a vanilla boat's paddles). Shared by every colour scheme. Made by art/src/luzzu.py together with its
 * textures (textures/entity/boat/luzzu*.png); change the script and run it again rather than editing this file.
 */
public class LuzzuModel extends AbstractBoatModel {
    public LuzzuModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("hull_mid", CubeListBuilder.create()
            .texOffs(0, 51).addBox(-5.0F, 0.0F, 7.0F, 10.0F, 6.0F, 2.0F) // wall
            .texOffs(8, 86).addBox(-5.0F, 6.0F, 6.0F, 10.0F, 1.0F, 2.0F) // wall
            .texOffs(80, 90).addBox(-5.0F, 1.0F, 9.0F, 10.0F, 1.0F, 1.0F) // strake
            .texOffs(24, 51).addBox(-5.0F, 0.0F, -9.0F, 10.0F, 6.0F, 2.0F) // wall
            .texOffs(32, 86).addBox(-5.0F, 6.0F, -8.0F, 10.0F, 1.0F, 2.0F) // wall
            .texOffs(102, 90).addBox(-5.0F, 1.0F, -10.0F, 10.0F, 1.0F, 1.0F) // strake
            .texOffs(48, 24).addBox(-5.0F, 7.0F, -6.0F, 10.0F, 1.0F, 12.0F) // floor
            .texOffs(76, 67).addBox(-9.0F, 8.0F, -1.0F, 18.0F, 4.0F, 2.0F) // keel
            , PartPose.offset(0.0F, -6.0F, 0.0F));
        root.addOrReplaceChild("bow_1", CubeListBuilder.create()
            .texOffs(12, 59).addBox(0.0F, 0.0F, 7.0F, 3.0F, 6.0F, 2.0F) // wall
            .texOffs(104, 86).addBox(0.0F, 6.0F, 6.0F, 3.0F, 1.0F, 2.0F) // wall
            .texOffs(22, 59).addBox(0.0F, 0.0F, -9.0F, 3.0F, 6.0F, 2.0F) // wall
            .texOffs(114, 86).addBox(0.0F, 6.0F, -8.0F, 3.0F, 1.0F, 2.0F) // wall
            .texOffs(92, 24).addBox(0.0F, 7.0F, -6.0F, 3.0F, 1.0F, 12.0F) // floor
            .texOffs(40, 93).addBox(0.0F, 1.0F, 9.0F, 3.0F, 1.0F, 1.0F) // strake
            .texOffs(48, 93).addBox(0.0F, 1.0F, -10.0F, 3.0F, 1.0F, 1.0F) // strake
            , PartPose.offset(5.0F, -6.0F, 0.0F));
        root.addOrReplaceChild("bow_2", CubeListBuilder.create()
            .texOffs(32, 59).addBox(-1.0F, 0.0F, 6.0F, 3.0F, 6.0F, 2.0F) // wall
            .texOffs(0, 90).addBox(-1.0F, 6.0F, 5.0F, 3.0F, 1.0F, 2.0F) // wall
            .texOffs(42, 59).addBox(-1.0F, 0.0F, -8.0F, 3.0F, 6.0F, 2.0F) // wall
            .texOffs(10, 90).addBox(-1.0F, 6.0F, -7.0F, 3.0F, 1.0F, 2.0F) // wall
            .texOffs(30, 38).addBox(-1.0F, 7.0F, -5.0F, 3.0F, 1.0F, 10.0F) // floor
            .texOffs(104, 93).addBox(0.0F, 1.0F, 8.0F, 2.0F, 1.0F, 1.0F) // strake
            .texOffs(110, 93).addBox(0.0F, 1.0F, -9.0F, 2.0F, 1.0F, 1.0F) // strake
            , PartPose.offsetAndRotation(8.0F, -6.0F, 0.0F, 0.0F, 0.0F, -0.10472F));
        root.addOrReplaceChild("bow_3", CubeListBuilder.create()
            .texOffs(84, 51).addBox(-1.0F, 0.0F, 4.0F, 4.0F, 6.0F, 2.0F) // wall
            .texOffs(56, 86).addBox(-1.0F, 6.0F, 3.0F, 4.0F, 1.0F, 2.0F) // wall
            .texOffs(96, 51).addBox(-1.0F, 0.0F, -6.0F, 4.0F, 6.0F, 2.0F) // wall
            .texOffs(68, 86).addBox(-1.0F, 6.0F, -5.0F, 4.0F, 1.0F, 2.0F) // wall
            .texOffs(92, 59).addBox(-1.0F, 7.0F, -3.0F, 4.0F, 1.0F, 6.0F) // floor
            .texOffs(56, 93).addBox(0.0F, 1.0F, 6.0F, 3.0F, 1.0F, 1.0F) // strake
            .texOffs(64, 93).addBox(0.0F, 1.0F, -7.0F, 3.0F, 1.0F, 1.0F) // strake
            , PartPose.offsetAndRotation(9.989044F, -6.209057F, 0.0F, 0.0F, 0.0F, -0.20944F));
        root.addOrReplaceChild("bow_4", CubeListBuilder.create()
            .texOffs(40, 74).addBox(-1.0F, 0.0F, 3.0F, 6.0F, 4.0F, 2.0F) // wall
            .texOffs(56, 74).addBox(-1.0F, 0.0F, -5.0F, 6.0F, 4.0F, 2.0F) // wall
            .texOffs(34, 80).addBox(-1.0F, 4.0F, 2.0F, 6.0F, 2.0F, 2.0F) // wall
            .texOffs(50, 80).addBox(-1.0F, 4.0F, -4.0F, 6.0F, 2.0F, 2.0F) // wall
            .texOffs(0, 74).addBox(-1.0F, 6.0F, -2.0F, 6.0F, 2.0F, 4.0F) // deck
            .texOffs(20, 67).addBox(-1.0F, 6.0F, -3.0F, 1.0F, 1.0F, 6.0F) // deck
            .texOffs(82, 38).addBox(4.0F, 1.0F, -3.0F, 1.0F, 3.0F, 6.0F) // bulkhead
            .texOffs(14, 80).addBox(4.0F, 4.0F, -2.0F, 1.0F, 2.0F, 4.0F) // bulkhead
            .texOffs(0, 93).addBox(0.0F, 1.0F, 5.0F, 4.0F, 1.0F, 1.0F) // strake
            .texOffs(10, 93).addBox(0.0F, 1.0F, -6.0F, 4.0F, 1.0F, 1.0F) // strake
            , PartPose.offsetAndRotation(12.923487F, -6.832792F, 0.0F, 0.0F, 0.0F, -0.349066F));
        root.addOrReplaceChild("bow_5", CubeListBuilder.create()
            .texOffs(48, 51).addBox(-1.0F, 0.0F, -3.0F, 3.0F, 2.0F, 6.0F) // deck
            .texOffs(34, 67).addBox(-1.0F, 2.0F, -2.0F, 3.0F, 3.0F, 4.0F) // deck
            .texOffs(20, 90).addBox(-1.0F, 5.0F, -1.0F, 3.0F, 1.0F, 2.0F) // deck
            , PartPose.offsetAndRotation(17.62195F, -8.542893F, 0.0F, 0.0F, 0.0F, -0.383972F));
        root.addOrReplaceChild("bow_6", CubeListBuilder.create()
            .texOffs(104, 74).addBox(-1.0F, 0.0F, -2.0F, 3.0F, 2.0F, 4.0F) // deck
            .texOffs(98, 80).addBox(-1.0F, 2.0F, -1.0F, 3.0F, 2.0F, 2.0F) // deck
            , PartPose.offsetAndRotation(19.476317F, -9.292106F, 0.0F, 0.0F, 0.0F, -0.488692F));
        root.addOrReplaceChild("bow_7", CubeListBuilder.create()
            .texOffs(118, 80).addBox(-1.0F, 0.0F, -1.0F, 2.0F, 2.0F, 2.0F) // deck
            , PartPose.offsetAndRotation(21.242213F, -10.231049F, 0.0F, 0.0F, 0.0F, -0.593412F));
        root.addOrReplaceChild("stern_1", CubeListBuilder.create()
            .texOffs(52, 59).addBox(-3.0F, 0.0F, 7.0F, 3.0F, 6.0F, 2.0F) // wall
            .texOffs(30, 90).addBox(-3.0F, 6.0F, 6.0F, 3.0F, 1.0F, 2.0F) // wall
            .texOffs(62, 59).addBox(-3.0F, 0.0F, -9.0F, 3.0F, 6.0F, 2.0F) // wall
            .texOffs(40, 90).addBox(-3.0F, 6.0F, -8.0F, 3.0F, 1.0F, 2.0F) // wall
            .texOffs(0, 38).addBox(-3.0F, 7.0F, -6.0F, 3.0F, 1.0F, 12.0F) // floor
            .texOffs(72, 93).addBox(-3.0F, 1.0F, 9.0F, 3.0F, 1.0F, 1.0F) // strake
            .texOffs(80, 93).addBox(-3.0F, 1.0F, -10.0F, 3.0F, 1.0F, 1.0F) // strake
            , PartPose.offset(-5.0F, -6.0F, 0.0F));
        root.addOrReplaceChild("stern_2", CubeListBuilder.create()
            .texOffs(72, 59).addBox(-2.0F, 0.0F, 6.0F, 3.0F, 6.0F, 2.0F) // wall
            .texOffs(50, 90).addBox(-2.0F, 6.0F, 5.0F, 3.0F, 1.0F, 2.0F) // wall
            .texOffs(82, 59).addBox(-2.0F, 0.0F, -8.0F, 3.0F, 6.0F, 2.0F) // wall
            .texOffs(60, 90).addBox(-2.0F, 6.0F, -7.0F, 3.0F, 1.0F, 2.0F) // wall
            .texOffs(56, 38).addBox(-2.0F, 7.0F, -5.0F, 3.0F, 1.0F, 10.0F) // floor
            .texOffs(116, 93).addBox(-2.0F, 1.0F, 8.0F, 2.0F, 1.0F, 1.0F) // strake
            .texOffs(122, 93).addBox(-2.0F, 1.0F, -9.0F, 2.0F, 1.0F, 1.0F) // strake
            , PartPose.offsetAndRotation(-8.0F, -6.0F, 0.0F, 0.0F, 0.0F, 0.10472F));
        root.addOrReplaceChild("stern_3", CubeListBuilder.create()
            .texOffs(108, 51).addBox(-3.0F, 0.0F, 4.0F, 4.0F, 6.0F, 2.0F) // wall
            .texOffs(80, 86).addBox(-3.0F, 6.0F, 3.0F, 4.0F, 1.0F, 2.0F) // wall
            .texOffs(0, 59).addBox(-3.0F, 0.0F, -6.0F, 4.0F, 6.0F, 2.0F) // wall
            .texOffs(92, 86).addBox(-3.0F, 6.0F, -5.0F, 4.0F, 1.0F, 2.0F) // wall
            .texOffs(0, 67).addBox(-3.0F, 7.0F, -3.0F, 4.0F, 1.0F, 6.0F) // floor
            .texOffs(88, 93).addBox(-3.0F, 1.0F, 6.0F, 3.0F, 1.0F, 1.0F) // strake
            .texOffs(96, 93).addBox(-3.0F, 1.0F, -7.0F, 3.0F, 1.0F, 1.0F) // strake
            , PartPose.offsetAndRotation(-9.989044F, -6.209057F, 0.0F, 0.0F, 0.0F, 0.20944F));
        root.addOrReplaceChild("stern_4", CubeListBuilder.create()
            .texOffs(72, 74).addBox(-5.0F, 0.0F, 3.0F, 6.0F, 4.0F, 2.0F) // wall
            .texOffs(88, 74).addBox(-5.0F, 0.0F, -5.0F, 6.0F, 4.0F, 2.0F) // wall
            .texOffs(66, 80).addBox(-5.0F, 4.0F, 2.0F, 6.0F, 2.0F, 2.0F) // wall
            .texOffs(82, 80).addBox(-5.0F, 4.0F, -4.0F, 6.0F, 2.0F, 2.0F) // wall
            .texOffs(20, 74).addBox(-5.0F, 6.0F, -2.0F, 6.0F, 2.0F, 4.0F) // deck
            .texOffs(48, 67).addBox(0.0F, 6.0F, -3.0F, 1.0F, 1.0F, 6.0F) // deck
            .texOffs(96, 38).addBox(-5.0F, 1.0F, -3.0F, 1.0F, 3.0F, 6.0F) // bulkhead
            .texOffs(24, 80).addBox(-5.0F, 4.0F, -2.0F, 1.0F, 2.0F, 4.0F) // bulkhead
            .texOffs(20, 93).addBox(-4.0F, 1.0F, 5.0F, 4.0F, 1.0F, 1.0F) // strake
            .texOffs(30, 93).addBox(-4.0F, 1.0F, -6.0F, 4.0F, 1.0F, 1.0F) // strake
            , PartPose.offsetAndRotation(-12.923487F, -6.832792F, 0.0F, 0.0F, 0.0F, 0.349066F));
        root.addOrReplaceChild("stern_5", CubeListBuilder.create()
            .texOffs(66, 51).addBox(-2.0F, 0.0F, -3.0F, 3.0F, 2.0F, 6.0F) // deck
            .texOffs(62, 67).addBox(-2.0F, 2.0F, -2.0F, 3.0F, 3.0F, 4.0F) // deck
            .texOffs(70, 90).addBox(-2.0F, 5.0F, -1.0F, 3.0F, 1.0F, 2.0F) // deck
            , PartPose.offsetAndRotation(-17.62195F, -8.542893F, 0.0F, 0.0F, 0.0F, 0.383972F));
        root.addOrReplaceChild("stern_6", CubeListBuilder.create()
            .texOffs(0, 80).addBox(-2.0F, 0.0F, -2.0F, 3.0F, 2.0F, 4.0F) // deck
            .texOffs(108, 80).addBox(-2.0F, 2.0F, -1.0F, 3.0F, 2.0F, 2.0F) // deck
            , PartPose.offsetAndRotation(-19.476317F, -9.292106F, 0.0F, 0.0F, 0.0F, 0.488692F));
        root.addOrReplaceChild("stern_7", CubeListBuilder.create()
            .texOffs(0, 86).addBox(-1.0F, 0.0F, -1.0F, 2.0F, 2.0F, 2.0F) // deck
            , PartPose.offsetAndRotation(-21.242213F, -10.231049F, 0.0F, 0.0F, 0.0F, 0.593412F));
        root.addOrReplaceChild("stem_post", CubeListBuilder.create()
            .texOffs(96, 0).addBox(-1.0F, -19.0F, -1.0F, 2.0F, 19.0F, 2.0F) // post
            , PartPose.offsetAndRotation(22.189636F, -1.025352F, 0.0F, 0.0F, 0.0F, 0.20944F));
        root.addOrReplaceChild("stern_post", CubeListBuilder.create()
            .texOffs(104, 0).addBox(-1.0F, -15.0F, -1.0F, 2.0F, 15.0F, 2.0F) // post
            , PartPose.offsetAndRotation(-22.189636F, -1.025352F, 0.0F, 0.0F, 0.0F, -0.139626F));
        root.addOrReplaceChild("left_paddle", CubeListBuilder.create()
            .texOffs(0, 0).addBox(-0.5F, 0.0F, -7.0F, 1.0F, 1.0F, 23.0F)
            .texOffs(0, 24).addBox(-0.501F, -1.0F, 6.0F, 1.0F, 3.0F, 11.0F),
            PartPose.offsetAndRotation(11.0F, -8.5F, 8.0F, 0.0F, 0.0F, (float) (Math.PI / 16)));
        root.addOrReplaceChild("right_paddle", CubeListBuilder.create()
            .texOffs(48, 0).addBox(-0.5F, 0.0F, -7.0F, 1.0F, 1.0F, 23.0F)
            .texOffs(24, 24).addBox(-0.499F, -1.0F, 6.0F, 1.0F, 3.0F, 11.0F),
            PartPose.offsetAndRotation(11.0F, -8.5F, -8.0F, 0.0F, (float) Math.PI, (float) (Math.PI / 16)));
        return LayerDefinition.create(mesh, 128, 128);
    }

    /** Keeps the sea from showing inside the open hull, like vanilla's boat water patch. */
    public static LayerDefinition createWaterPatch() {
        MeshDefinition mesh = new MeshDefinition();
        mesh.getRoot().addOrReplaceChild("water_patch", CubeListBuilder.create()
            .addBox(-5.0F, -3.0F, -7.0F, 10.0F, 3.0F, 14.0F)
            .addBox(5.0F, -3.0F, -7.0F, 3.0F, 3.0F, 14.0F)
            .addBox(-8.0F, -3.0F, -7.0F, 3.0F, 3.0F, 14.0F)
            .addBox(8.0F, -3.0F, -6.0F, 2.0F, 3.0F, 12.0F)
            .addBox(-10.0F, -3.0F, -6.0F, 2.0F, 3.0F, 12.0F)
            .addBox(10.0F, -3.0F, -4.0F, 3.0F, 3.0F, 8.0F)
            .addBox(-13.0F, -3.0F, -4.0F, 3.0F, 3.0F, 8.0F)
            , PartPose.ZERO);
        return LayerDefinition.create(mesh, 0, 0);
    }
}
