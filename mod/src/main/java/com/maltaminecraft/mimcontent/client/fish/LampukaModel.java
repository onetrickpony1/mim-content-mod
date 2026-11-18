package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The lampuka (dolphinfish): a steep blunt forehead, one long dorsal fin from the head almost to the tail, a long anal
 * fin, a deeply forked tail, gold flanks under a blue-green back. The back half ("tail") sways gently as it swims, the
 * tail fin more. 35 px long, 7 px deep, head toward -z, the ground at y 24.
 * Made by art/src/fish_lampuka_model.py (don't edit by hand). Texture: textures/entity/fish/lampuka.png (64 x 32).
 */
public class LampukaModel extends FishModel {
    public LampukaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* snout */ .texOffs(56, 0).addBox(-1.0F, -1.0F, -17.0F, 2.0F, 4.0F, 1.0F)
            /* head */ .texOffs(0, 17).addBox(-1.5F, -3.0F, -16.0F, 3.0F, 6.0F, 3.0F)
            /* trunk */ .texOffs(0, 0).addBox(-1.5F, -4.0F, -13.0F, 3.0F, 7.0F, 10.0F)
            /* dorsal_front */ .texOffs(12, 11).addBox(0.0F, -7.0F, -13.0F, 0.0F, 3.0F, 10.0F),
            PartPose.offset(0.0F, 20.0F, 0.0F));
        PartDefinition tail = root.addOrReplaceChild("tail", CubeListBuilder.create()
            /* mid */ .texOffs(26, 0).addBox(-1.0F, -3.0F, 0.0F, 2.0F, 6.0F, 6.0F)
            /* rear */ .texOffs(42, 0).addBox(-1.0F, -2.0F, 6.0F, 2.0F, 4.0F, 5.0F)
            /* stalk */ .texOffs(42, 9).addBox(-0.5F, -1.0F, 11.0F, 1.0F, 2.0F, 4.0F)
            /* dorsal_back */ .texOffs(12, 4).addBox(0.0F, -5.0F, 0.0F, 0.0F, 4.0F, 13.0F)
            /* anal */ .texOffs(38, 8).addBox(0.0F, 2.0F, 2.0F, 0.0F, 2.0F, 9.0F),
            PartPose.offset(0.0F, 20.0F, -3.0F));
        tail.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(38, 14).addBox(0.0F, -4.0F, 0.0F, 0.0F, 8.0F, 6.0F),
            PartPose.offset(0.0F, 0.0F, 15.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(46, 20).addBox(-2.0F, 0.0F, 0.0F, 2.0F, 0.0F, 4.0F),
            PartPose.offsetAndRotation(-1.5F, 21.0F, -12.0F, 0.0F, 0.0F, -0.6F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(50, 20).addBox(0.0F, 0.0F, 0.0F, 2.0F, 0.0F, 4.0F),
            PartPose.offsetAndRotation(1.5F, 21.0F, -12.0F, 0.0F, 0.0F, 0.6F));
        return LayerDefinition.create(mesh, 64, 32);
    }
}
