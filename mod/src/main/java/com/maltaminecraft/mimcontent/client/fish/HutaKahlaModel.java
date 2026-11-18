package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.util.Mth;

/**
 * The huta kahla (blue shark): a long, slender torpedo with a pointed conical snout, big eyes, five gill slits,
 * long sickle-shaped pectoral fins held out like wings, a triangular first dorsal, a small second dorsal and
 * anal fin, and a tail whose upper lobe is far longer than the lower. 42 px long, 6 deep, 5 thick; the body is
 * rounded (cut corners). Deep indigo back, bright blue sides, white belly.
 * Made by art/src/fish_huta_kahla_model.py (do not edit by hand); texture textures/entity/fish/huta_kahla.png.
 * Follows the fish model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): "tail" is the back
 * half, "tail_fin" the tail inside it. A shark swims slowly: the tail sweeps about once a second, the fin a
 * little behind the body, instead of the quick wag of the smaller fish.
 */
public class HutaKahlaModel extends FishModel {
    private final ModelPart tail;
    private final ModelPart tailFin;

    public HutaKahlaModel(ModelPart root) {
        super(root);
        this.tail = root.getChild("tail");
        this.tailFin = tail.getChild("tail_fin");
    }

    @Override
    public void setupAnim(LivingEntityRenderState state) {
        super.setupAnim(state);
        // out of water it flops wider and quicker, as every fish does
        float amplitude = state.isInWater ? 1.0F : 1.4F;
        float speed = state.isInWater ? 1.0F : 1.8F;
        float phase = speed * 0.3F * state.ageInTicks;
        tail.yRot = -amplitude * 0.14F * Mth.sin(phase);
        tailFin.yRot = -amplitude * 0.3F * Mth.sin(phase - 1.0F);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* tip */ .texOffs(52, 40).addBox(-0.5F, 0.0F, -22.0F, 1.0F, 1.0F, 1.0F)
            /* snout */ .texOffs(18, 40).addBox(-1.0F, 0.0F, -21.0F, 2.0F, 2.0F, 2.0F)
            /* eyes */ .texOffs(24, 34).addBox(-1.5F, -1.0F, -19.0F, 3.0F, 3.0F, 2.0F)
            /* head */ .texOffs(48, 15).addBox(-1.0F, -1.0F, -17.0F, 2.0F, 4.0F, 3.0F)
            /* head_r */ .texOffs(34, 34).addBox(-2.0F, 0.0F, -17.0F, 1.0F, 2.0F, 3.0F)
            /* head_l */ .texOffs(42, 34).addBox(1.0F, 0.0F, -17.0F, 1.0F, 2.0F, 3.0F)
            /* gills */ .texOffs(20, 15).addBox(-1.5F, -2.0F, -14.0F, 3.0F, 5.0F, 4.0F)
            /* gills_r */ .texOffs(0, 27).addBox(-2.5F, -1.0F, -14.0F, 1.0F, 3.0F, 4.0F)
            /* gills_l */ .texOffs(10, 27).addBox(1.5F, -1.0F, -14.0F, 1.0F, 3.0F, 4.0F)
            /* trunk */ .texOffs(0, 0).addBox(-1.5F, -2.0F, -10.0F, 3.0F, 6.0F, 9.0F)
            /* trunk_r */ .texOffs(24, 0).addBox(-2.5F, -1.0F, -10.0F, 1.0F, 4.0F, 9.0F)
            /* trunk_l */ .texOffs(44, 0).addBox(1.5F, -1.0F, -10.0F, 1.0F, 4.0F, 9.0F)
            /* belly */ .texOffs(34, 15).addBox(-1.5F, -2.0F, -1.0F, 3.0F, 5.0F, 4.0F)
            /* belly_r */ .texOffs(20, 27).addBox(-2.5F, -1.0F, -1.0F, 1.0F, 3.0F, 4.0F)
            /* belly_l */ .texOffs(30, 27).addBox(1.5F, -1.0F, -1.0F, 1.0F, 3.0F, 4.0F)
            /* dorsal */ .texOffs(8, 35).addBox(0.0F, -6.0F, -6.0F, 0.0F, 4.0F, 5.0F),
            PartPose.offset(0.0F, 19.0F, 0.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(-6, 34).addBox(-6.0F, 0.0F, 0.0F, 6.0F, 0.0F, 6.0F),
            PartPose.offsetAndRotation(-1.5F, 21.0F, -13.0F, 0.0F, 0.0F, -0.6F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(6, 34).addBox(0.0F, 0.0F, 0.0F, 6.0F, 0.0F, 6.0F),
            PartPose.offsetAndRotation(1.5F, 21.0F, -13.0F, 0.0F, 0.0F, 0.6F));
        PartDefinition tail = root.addOrReplaceChild("tail", CubeListBuilder.create()
            /* rear */ .texOffs(40, 27).addBox(-1.0F, -1.0F, 0.0F, 2.0F, 4.0F, 3.0F)
            /* rear_r */ .texOffs(50, 34).addBox(-2.0F, 0.0F, 0.0F, 1.0F, 2.0F, 3.0F)
            /* rear_l */ .texOffs(0, 40).addBox(1.0F, 0.0F, 0.0F, 1.0F, 2.0F, 3.0F)
            /* rear2 */ .texOffs(50, 27).addBox(-1.5F, -1.0F, 3.0F, 3.0F, 3.0F, 3.0F)
            /* stalk */ .texOffs(26, 40).addBox(-1.0F, -1.0F, 6.0F, 2.0F, 2.0F, 2.0F)
            /* dorsal2 */ .texOffs(40, 37).addBox(0.0F, -3.0F, 2.0F, 0.0F, 2.0F, 3.0F)
            /* anal */ .texOffs(46, 37).addBox(0.0F, 2.0F, 3.0F, 0.0F, 2.0F, 3.0F),
            PartPose.offset(0.0F, 19.0F, 3.0F));
        tail.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* lobe */ .texOffs(0, 5).addBox(0.0F, -7.0F, 0.0F, 0.0F, 12.0F, 10.0F)
            /* lobe_root */ .texOffs(34, 40).addBox(-0.5F, -2.0F, 0.0F, 1.0F, 2.0F, 2.0F),
            PartPose.offset(0.0F, 0.0F, 8.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
