package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The pixxispad (swordfish): a long, rounded torpedo with a long, flat, straight sword held level with the body, a
 * short lower jaw, a big eye, a tall sickle dorsal fin just behind the head, long sickle pectoral fins set low, a
 * slim keeled tail stalk and a huge crescent tail; a dark purple-bronze back over silvery-brown sides and a pale
 * belly. 44 px long (a 12 px sword and a 32 px body), 8 px deep, 6 px thick, head toward -z, the ground at y 24.
 * The sword is part of "body", so it never bends; "tail" (the stalk) sways gently and "tail_fin" more.
 * Made by art/src/fish_pixxispad_model.py (don't edit by hand). Texture: textures/entity/fish/pixxispad.png (64 x 64).
 */
public class PixxispadModel extends FishModel {
    public PixxispadModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* sword_tip */ .texOffs(32, 46).addBox(-0.5F, 19.0F, -23.0F, 1.0F, 1.0F, 2.0F)
            /* sword */ .texOffs(0, 23).addBox(-1.0F, 19.0F, -21.0F, 2.0F, 1.0F, 7.0F)
            /* sword_root */ .texOffs(14, 41).addBox(-1.5F, 18.5F, -14.0F, 3.0F, 2.0F, 3.0F)
            /* jaw */ .texOffs(56, 41).addBox(-1.0F, 20.5F, -13.0F, 2.0F, 1.0F, 2.0F)
            /* snout */ .texOffs(48, 23).addBox(-2.0F, 18.0F, -11.0F, 4.0F, 4.0F, 2.0F)
            /* snout_top */ .texOffs(0, 46).addBox(-1.0F, 17.0F, -11.0F, 2.0F, 1.0F, 2.0F)
            /* snout_bot */ .texOffs(8, 46).addBox(-1.0F, 22.0F, -11.0F, 2.0F, 1.0F, 2.0F)
            /* head */ .texOffs(0, 14).addBox(-2.5F, 17.5F, -9.0F, 5.0F, 5.0F, 4.0F)
            /* head_top */ .texOffs(0, 36).addBox(-1.5F, 16.5F, -9.0F, 3.0F, 1.0F, 4.0F)
            /* head_bot */ .texOffs(14, 36).addBox(-1.5F, 22.5F, -9.0F, 3.0F, 1.0F, 4.0F)
            /* trunk */ .texOffs(12, 0).addBox(-3.0F, 17.0F, -5.0F, 6.0F, 6.0F, 7.0F)
            /* trunk_top */ .texOffs(18, 14).addBox(-2.0F, 16.0F, -5.0F, 4.0F, 1.0F, 7.0F)
            /* trunk_bot */ .texOffs(40, 14).addBox(-2.0F, 23.0F, -5.0F, 4.0F, 1.0F, 7.0F)
            /* mid */ .texOffs(38, 0).addBox(-3.0F, 17.5F, 2.0F, 6.0F, 5.0F, 4.0F)
            /* mid_top */ .texOffs(0, 31).addBox(-2.0F, 16.5F, 2.0F, 4.0F, 1.0F, 4.0F)
            /* mid_bot */ .texOffs(16, 31).addBox(-2.0F, 22.5F, 2.0F, 4.0F, 1.0F, 4.0F)
            /* rear */ .texOffs(18, 23).addBox(-2.5F, 18.0F, 6.0F, 5.0F, 4.0F, 4.0F)
            /* rear_top */ .texOffs(28, 36).addBox(-1.5F, 17.0F, 6.0F, 3.0F, 1.0F, 4.0F)
            /* rear_bot */ .texOffs(42, 36).addBox(-1.5F, 22.0F, 6.0F, 3.0F, 1.0F, 4.0F)
            /* dorsal */ .texOffs(36, 17).addBox(0.0F, 9.0F, -5.0F, 0.0F, 7.0F, 6.0F)
            /* anal */ .texOffs(16, 42).addBox(0.0F, 23.0F, 6.0F, 0.0F, 3.0F, 4.0F),
            PartPose.offset(0.0F, 0.0F, 0.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* pec_r */ .texOffs(32, 23).addBox(0.0F, 0.0F, 0.0F, 0.0F, 5.0F, 8.0F),
            PartPose.offsetAndRotation(-3.05F, 22.0F, -4.5F, 0.0F, -0.3F, 0.35F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* pec_l */ .texOffs(48, 23).addBox(0.0F, 0.0F, 0.0F, 0.0F, 5.0F, 8.0F),
            PartPose.offsetAndRotation(3.05F, 22.0F, -4.5F, 0.0F, 0.3F, -0.35F));
        PartDefinition tail = root.addOrReplaceChild("tail", CubeListBuilder.create()
            /* rear2 */ .texOffs(0, 41).addBox(-2.0F, -1.0F, 0.0F, 4.0F, 2.0F, 3.0F)
            /* rear2_top */ .texOffs(36, 41).addBox(-1.0F, -2.0F, 0.0F, 2.0F, 1.0F, 3.0F)
            /* rear2_bot */ .texOffs(46, 41).addBox(-1.0F, 1.0F, 0.0F, 2.0F, 1.0F, 3.0F)
            /* stalk */ .texOffs(26, 41).addBox(-1.0F, -1.0F, 3.0F, 2.0F, 2.0F, 3.0F)
            /* keel */ .texOffs(21, 46).addBox(-2.0F, 0.0F, 3.0F, 4.0F, 0.0F, 3.0F),
            PartPose.offset(0.0F, 20.0F, 10.0F));
        tail.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* caudal */ .texOffs(0, -6).addBox(0.0F, -7.0F, 0.0F, 0.0F, 14.0F, 6.0F),
            PartPose.offset(0.0F, 0.0F, 6.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }
}
