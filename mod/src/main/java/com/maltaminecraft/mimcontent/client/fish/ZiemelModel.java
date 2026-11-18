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
 * The ziemel tal-bahar (seahorse), upright: a horse-like head on a bent neck, a long tubular snout from the middle of
 * the head, a small crown, single filaments on the back of the head and neck, a pot belly, bony rings along the body
 * and a thin tail curled forward into a closed loop. Brown-ochre with small white dots. Bigger than life so its detail
 * shows: 13 px tall (0.81 blocks), 9 px from snout tip to dorsal fin, head toward -z, the ground at y 24.
 * Its own swimming: in the water it bobs slowly up and down (0.04 blocks, every 2.5 s), the dorsal fin ("tail_fin")
 * flutters quickly and the tail curls in and out a little; the body doesn't swing (its renderer wiggle is 0).
 * Out of water the shared fish animation flops it as usual.
 * Made by art/src/fish_ziemel_model.py (don't edit by hand). Texture: textures/entity/fish/ziemel.png (32 x 32).
 */
public class ZiemelModel extends FishModel {
    private final ModelPart[] parts;
    private final float[] restY;
    private final ModelPart tail;
    private final ModelPart dorsalFin;

    public ZiemelModel(ModelPart root) {
        super(root);
        this.parts = new ModelPart[] {root.getChild("body"), root.getChild("tail"), root.getChild("tail_fin")};
        this.restY = new float[parts.length];
        for (int i = 0; i < parts.length; i++) {
            restY[i] = parts[i].y;
        }
        this.tail = root.getChild("tail");
        this.dorsalFin = root.getChild("tail_fin");
    }

    @Override
    public void setupAnim(LivingEntityRenderState state) {
        super.setupAnim(state);
        if (!state.isInWater) {
            return;
        }
        float t = state.ageInTicks;
        float bob = 0.65F * Mth.sin(t * 0.1257F);
        for (int i = 0; i < parts.length; i++) {
            parts[i].y = restY[i] + bob;
        }
        dorsalFin.yRot = 0.2F * Mth.sin(t * 2.1F);
        tail.yRot = 0.0F;
        tail.xRot = -0.12F * (0.5F + 0.5F * Mth.sin(t * 0.1257F + 1.5F));
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* coronet */ .texOffs(16, 16).addBox(-0.5F, -7.0F, 1.0F, 1.0F, 1.0F, 1.0F)
            /* head */ .texOffs(18, 0).addBox(-1.0F, -6.0F, -1.0F, 2.0F, 2.0F, 4.0F)
            /* jaw */ .texOffs(0, 12).addBox(-1.0F, -4.0F, -1.0F, 2.0F, 1.0F, 3.0F)
            /* snout */ .texOffs(0, 16).addBox(-0.5F, -5.0F, -4.0F, 1.0F, 1.0F, 3.0F)
            /* chest */ .texOffs(16, 7).addBox(-1.0F, -3.0F, 0.0F, 2.0F, 1.0F, 3.0F)
            /* belly */ .texOffs(0, 0).addBox(-1.5F, -2.0F, -2.0F, 3.0F, 2.0F, 5.0F)
            /* belly_lo */ .texOffs(0, 7).addBox(-1.0F, 0.0F, -1.0F, 2.0F, 1.0F, 4.0F)
            /* mane */ .texOffs(16, 0).addBox(0.0F, -7.0F, 3.0F, 0.0F, 6.0F, 1.0F),
            PartPose.offset(0.0F, 18.0F, 0.0F));
        root.addOrReplaceChild("tail", CubeListBuilder.create()
            /* tail1 */ .texOffs(8, 16).addBox(-1.0F, 0.0F, -1.0F, 2.0F, 1.0F, 2.0F)
            /* tail2 */ .texOffs(28, 16).addBox(-0.5F, 1.0F, -1.0F, 1.0F, 1.0F, 1.0F)
            /* loop_top */ .texOffs(18, 12).addBox(-0.5F, 2.0F, -3.0F, 1.0F, 1.0F, 3.0F)
            /* loop_front */ .texOffs(24, 16).addBox(-0.5F, 3.0F, -3.0F, 1.0F, 1.0F, 1.0F)
            /* loop_back */ .texOffs(20, 16).addBox(-0.5F, 3.0F, -1.0F, 1.0F, 1.0F, 1.0F)
            /* loop_bottom */ .texOffs(10, 12).addBox(-0.5F, 4.0F, -3.0F, 1.0F, 1.0F, 3.0F),
            PartPose.offset(0.0F, 19.0F, 2.0F));
        root.addOrReplaceChild("tail_fin", CubeListBuilder.create()
            /* dorsal */ .texOffs(12, 7).addBox(0.0F, -1.5F, 0.0F, 0.0F, 3.0F, 2.0F),
            PartPose.offset(0.0F, 18.5F, 3.0F));
        return LayerDefinition.create(mesh, 32, 32);
    }
}
