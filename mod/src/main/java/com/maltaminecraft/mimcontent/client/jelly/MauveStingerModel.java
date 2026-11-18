package com.maltaminecraft.mimcontent.client.jelly;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The mauve stinger (Pelagia noctiluca): a small, deep dome bell, 8 px across and 5 tall, rounded in 1 px steps
 * with a scalloped rim; see-through pink-mauve covered in raised dark mauve warts; 8 long thin tentacles from the
 * rim and 4 longer frilly oral arms from the centre. The texture is drawn translucent.
 * Made by art/src/jelly_mauve_stinger_model.py (do not edit by hand); texture
 * textures/entity/jellyfish/mauve_stinger.png. Parts: "bell" (hinged at the rim), "tentacle_0".."tentacle_7"
 * and "oral_arms", children of the bell; the base class pulses the bell and sways the tentacles.
 */
public class MauveStingerModel extends JellyfishModel {
    /** The tentacles are drawn thinner than their 1 px texture: hair-thin. */
    private static final CubeDeformation THIN = new CubeDeformation(-0.3F, 0.0F, -0.3F);

    public MauveStingerModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition bell = root.addOrReplaceChild("bell", CubeListBuilder.create()
            /* cap */ .texOffs(32, 22).addBox(-2.0F, -5.0F, -1.0F, 4.0F, 1.0F, 2.0F)
            /* cap_f */ .texOffs(10, 30).addBox(-1.0F, -5.0F, -2.0F, 2.0F, 1.0F, 1.0F)
            /* cap_b */ .texOffs(16, 30).addBox(-1.0F, -5.0F, 1.0F, 2.0F, 1.0F, 1.0F)
            /* dome */ .texOffs(0, 22).addBox(-3.0F, -4.0F, -2.0F, 6.0F, 1.0F, 4.0F)
            /* dome_f */ .texOffs(48, 27).addBox(-2.0F, -4.0F, -3.0F, 4.0F, 1.0F, 1.0F)
            /* dome_b */ .texOffs(0, 30).addBox(-2.0F, -4.0F, 2.0F, 4.0F, 1.0F, 1.0F)
            /* side */ .texOffs(28, 15).addBox(-3.5F, -3.0F, -2.5F, 7.0F, 2.0F, 5.0F)
            /* side_f */ .texOffs(44, 22).addBox(-2.5F, -3.0F, -3.5F, 5.0F, 2.0F, 1.0F)
            /* side_b */ .texOffs(0, 27).addBox(-2.5F, -3.0F, 2.5F, 5.0F, 2.0F, 1.0F)
            /* lappet */ .texOffs(0, 15).addBox(-4.0F, -1.0F, -3.0F, 8.0F, 1.0F, 6.0F)
            /* lappet_f */ .texOffs(20, 27).addBox(-3.0F, -1.0F, -4.0F, 6.0F, 1.0F, 1.0F)
            /* lappet_b */ .texOffs(34, 27).addBox(-3.0F, -1.0F, 3.0F, 6.0F, 1.0F, 1.0F)
            /* core */ .texOffs(20, 22).addBox(-1.5F, -3.0F, -1.5F, 3.0F, 2.0F, 3.0F),
            PartPose.offset(0.0F, 8.0F, 0.0F));
        bell.addOrReplaceChild("tentacle_0", CubeListBuilder.create()
            /* tentacle_0 */ .texOffs(40, 0).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 9.0F, 1.0F, THIN),
            PartPose.offset(0.0F, 0.0F, -3.5F));
        bell.addOrReplaceChild("tentacle_1", CubeListBuilder.create()
            /* tentacle_1 */ .texOffs(52, 0).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 8.0F, 1.0F, THIN),
            PartPose.offset(2.5F, 0.0F, -2.5F));
        bell.addOrReplaceChild("tentacle_2", CubeListBuilder.create()
            /* tentacle_2 */ .texOffs(32, 0).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 10.0F, 1.0F, THIN),
            PartPose.offset(3.5F, 0.0F, 0.0F));
        bell.addOrReplaceChild("tentacle_3", CubeListBuilder.create()
            /* tentacle_3 */ .texOffs(56, 0).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 8.0F, 1.0F, THIN),
            PartPose.offset(2.5F, 0.0F, 2.5F));
        bell.addOrReplaceChild("tentacle_4", CubeListBuilder.create()
            /* tentacle_4 */ .texOffs(44, 0).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 9.0F, 1.0F, THIN),
            PartPose.offset(0.0F, 0.0F, 3.5F));
        bell.addOrReplaceChild("tentacle_5", CubeListBuilder.create()
            /* tentacle_5 */ .texOffs(36, 0).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 10.0F, 1.0F, THIN),
            PartPose.offset(-2.5F, 0.0F, 2.5F));
        bell.addOrReplaceChild("tentacle_6", CubeListBuilder.create()
            /* tentacle_6 */ .texOffs(60, 0).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 8.0F, 1.0F, THIN),
            PartPose.offset(-3.5F, 0.0F, 0.0F));
        bell.addOrReplaceChild("tentacle_7", CubeListBuilder.create()
            /* tentacle_7 */ .texOffs(48, 0).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 9.0F, 1.0F, THIN),
            PartPose.offset(-2.5F, 0.0F, -2.5F));
        bell.addOrReplaceChild("oral_arms", CubeListBuilder.create()
            /* stalk */ .texOffs(12, 27).addBox(-1.0F, 0.0F, -1.0F, 2.0F, 1.0F, 2.0F)
            /* arm_n */ .texOffs(0, -4).addBox(0.0F, 1.0F, -4.0F, 0.0F, 15.0F, 4.0F)
            /* arm_s */ .texOffs(16, -4).addBox(0.0F, 1.0F, 0.0F, 0.0F, 13.0F, 4.0F)
            /* arm_e */ .texOffs(24, 0).addBox(0.0F, 1.0F, 0.0F, 4.0F, 12.0F, 0.0F)
            /* arm_w */ .texOffs(8, 0).addBox(-4.0F, 1.0F, 0.0F, 4.0F, 14.0F, 0.0F),
            PartPose.offsetAndRotation(0.0F, 0.0F, 0.0F, 0.0F, 0.7854F, 0.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
