package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The tonn (Atlantic bluefin tuna): a big torpedo with a pointed snout, a short spiny first dorsal fin and a pointed
 * second one, yellow finlets toward the tail, a slim keeled tail stalk and a tall crescent tail. 39 px long.
 * Made by art/src/fish_tonn_model.py (do not edit by hand); texture textures/entity/fish/tonn.png. Follows the fish
 * model contract (docs/Tools and Process/Art pipeline.md, "Fish models"): "tail" is the slim back end,
 * "tail_fin" the crescent inside it.
 */
public class TonnModel extends FishModel {
    public TonnModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            .texOffs(12, 33).addBox(-1.5F, -1.5F, -19.0F, 3.0F, 3.0F, 2.0F) // nose
            .texOffs(18, 21).addBox(-2.5F, -3.5F, -17.0F, 5.0F, 7.0F, 4.0F) // head
            .texOffs(36, 0).addBox(-3.5F, -4.5F, -13.0F, 7.0F, 9.0F, 4.0F) // shoulder
            .texOffs(0, 0).addBox(-3.5F, -5.0F, -9.0F, 7.0F, 10.0F, 11.0F) // main
            .texOffs(0, 21).addBox(-2.5F, -4.0F, 2.0F, 5.0F, 8.0F, 4.0F) // rear1
            .texOffs(46, 21).addBox(-2.0F, -3.0F, 6.0F, 4.0F, 6.0F, 4.0F) // rear2
            .texOffs(38, 26).addBox(0.0F, -8.0F, -9.0F, 0.0F, 3.0F, 7.0F) // dorsal1
            .texOffs(22, 29).addBox(0.0F, -8.0F, 1.0F, 0.0F, 4.0F, 4.0F) // dorsal2
            .texOffs(52, 29).addBox(0.0F, 4.0F, 2.0F, 0.0F, 3.0F, 4.0F) // anal
            .texOffs(44, 35).addBox(0.0F, -4.0F, 5.0F, 0.0F, 1.0F, 5.0F) // finlets_top
            .texOffs(54, 36).addBox(0.0F, 3.0F, 6.0F, 0.0F, 1.0F, 4.0F) // finlets_bottom
            , PartPose.offset(0.0F, 19.0F, 0.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            .texOffs(20, 36).addBox(0.0F, 0.0F, 0.0F, 0.0F, 2.0F, 4.0F) // pectoral
            , PartPose.offsetAndRotation(-3.55F, 18.0F, -12.5F, 0.0F, -0.3F, 0.0F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            .texOffs(28, 36).addBox(0.0F, 0.0F, 0.0F, 0.0F, 2.0F, 4.0F) // pectoral
            , PartPose.offsetAndRotation(3.55F, 18.0F, -12.5F, 0.0F, 0.3F, 0.0F));
        PartDefinition tail = root.addOrReplaceChild("tail", CubeListBuilder.create()
            .texOffs(0, 33).addBox(-1.5F, -2.0F, 0.0F, 3.0F, 4.0F, 3.0F) // rear3
            .texOffs(30, 33).addBox(-1.0F, -1.0F, 3.0F, 2.0F, 2.0F, 2.0F) // stalk
            .texOffs(34, 40).addBox(-2.0F, 0.0F, 3.0F, 4.0F, 0.0F, 2.0F) // keel
            .texOffs(0, 35).addBox(0.0F, -3.0F, 0.0F, 0.0F, 2.0F, 5.0F) // finlets_top_t
            .texOffs(10, 35).addBox(0.0F, 1.0F, 0.0F, 0.0F, 2.0F, 5.0F) // finlets_bottom_t
            , PartPose.offset(0.0F, 19.0F, 10.0F));
        tail.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            .texOffs(36, 16).addBox(0.0F, -5.5F, 0.0F, 0.0F, 11.0F, 5.0F) // tail_fin
            , PartPose.offset(0.0F, 0.0F, 5.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
