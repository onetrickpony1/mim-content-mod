package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The gallinella (tub gurnard): a big boxy bony head with a steep forehead and the eye high up, a red-orange body
 * tapering to a slim stalk, huge fan-like pectoral "wings" spread out sideways (blue-green, a bright blue rim, a dark
 * navy patch), a spiny first dorsal, long low second dorsal and anal fins, and a squared tail that sways.
 * 18 px long, 4 px deep, 15 px across the wings; head toward -z, the ground at y 24.
 * Made by art/src/fish_gallinella_model.py (don't edit by hand). Texture: textures/entity/fish/gallinella.png (64 x 64).
 */
public class GallinellaModel extends FishModel {
    public GallinellaModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* snout */ .texOffs(7, 18).addBox(-1.5F, -1.0F, -9.0F, 3.0F, 2.0F, 1.0F)
            /* head */ .texOffs(0, 0).addBox(-2.0F, -3.0F, -8.0F, 4.0F, 5.0F, 4.0F)
            /* trunk */ .texOffs(17, 0).addBox(-1.5F, -2.0F, -4.0F, 3.0F, 4.0F, 4.0F)
            /* rear */ .texOffs(20, 10).addBox(-1.0F, -1.0F, 0.0F, 2.0F, 3.0F, 4.0F)
            /* stalk */ .texOffs(0, 18).addBox(-0.5F, -0.5F, 4.0F, 1.0F, 2.0F, 2.0F)
            /* dorsal2 */ .texOffs(51, 10).addBox(0.0F, -2.0F, 0.0F, 0.0F, 1.0F, 4.0F)
            /* anal */ .texOffs(33, 10).addBox(0.0F, 2.0F, 0.0F, 0.0F, 1.0F, 4.0F),
            PartPose.offset(0.0F, 21.0F, 0.0F));
        root.addOrReplaceChild("top_fin", CubeListBuilder.create()
            /* dorsal1 */ .texOffs(42, 10).addBox(0.0F, -1.0F, 0.0F, 0.0F, 1.0F, 4.0F),
            PartPose.offset(0.0F, 19.0F, -3.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* wing_r */ .texOffs(0, 10).addBox(-6.0F, 0.0F, 0.0F, 6.0F, 0.0F, 7.0F),
            PartPose.offsetAndRotation(-1.5F, 20.5F, -4.0F, 0.0F, 0.0F, -0.4F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* wing_l */ .texOffs(39, 0).addBox(0.0F, 0.0F, 0.0F, 6.0F, 0.0F, 7.0F),
            PartPose.offsetAndRotation(1.5F, 20.5F, -4.0F, 0.0F, 0.0F, 0.4F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(32, 0).addBox(0.0F, -2.5F, 0.0F, 0.0F, 5.0F, 3.0F),
            PartPose.offset(0.0F, 21.5F, 6.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
