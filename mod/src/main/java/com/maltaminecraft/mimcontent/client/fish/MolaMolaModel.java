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
 * The mola mola (ocean sunfish): a tall, flat round disc 21 px long and 21 tall that looks cut off behind, with no tail but
 * the clavus (a narrow rim with a scalloped edge), very tall dorsal and anal fins far back, small rounded pectoral
 * fins, a small round mouth and a small dark eye in a mid-grey ring. Grey-brown above, silver-grey sides, a pale
 * belly with soft grey blotches. 26 px long and 38 tall fin tip to fin tip (1.63 x 2.38 blocks, life size).
 * Made by art/src/fish_mola_model.py (do not edit by hand); texture textures/entity/fish/mola_mola.png.
 * Its own swimming: the dorsal and anal fins scull from side to side together (both tips to the same side), as the
 * real fish swims; the clavus steers a little and the pectoral fins flutter. The body doesn't wag (its renderer
 * wiggles it under a degree). Basking on its side at the surface (MolaFish), the fins only stir; on land they flap.
 */
public class MolaMolaModel extends FishModel {
    /** The renderer's lift when it lies on its side: half its thickness with the eyes, + 0.5 px (FishShape copies it). */
    public static final float LAND_LIFT = 0.3125F;
    /** Lying on its side, it is moved back along its height by this much, so its middle (y 4.5) lies over its position. */
    public static final float SIDE_SHIFT = 1.21975F;
    private final ModelPart dorsal;
    private final ModelPart anal;
    private final ModelPart clavus;
    private final ModelPart leftFin;
    private final ModelPart rightFin;
    private final float finYaw;

    public MolaMolaModel(ModelPart root) {
        super(root);
        this.dorsal = root.getChild("dorsal_fin");
        this.anal = root.getChild("anal_fin");
        this.clavus = root.getChild("clavus");
        this.leftFin = root.getChild("left_fin");
        this.rightFin = root.getChild("right_fin");
        this.finYaw = leftFin.yRot;
    }

    @Override
    public void setupAnim(LivingEntityRenderState state) {
        super.setupAnim(state);
        float t = state.ageInTicks;
        boolean basking = state instanceof FishRenderer.FishRenderState fish && fish.basking;
        float amplitude;
        float rate;
        if (!state.isInWater) {
            amplitude = 0.35F;
            rate = 0.5F;
        } else if (basking) {
            amplitude = 0.08F;
            rate = 0.06F;
        } else {
            // 0.14 radians while still, up to 0.4 swimming; one beat about every 2.2 s (the real fish 0.3 to 0.6 Hz)
            float moving = Mth.clamp(state.walkAnimationSpeed * 2.0F, 0.0F, 1.0F);
            amplitude = 0.14F + 0.26F * moving;
            rate = 0.14F;
        }
        float scull = amplitude * Mth.sin(rate * t);
        // +zRot swings the dorsal fin's tip one way and the anal fin's tip the other, so the anal fin turns the
        // opposite way: both tips go to the same side together
        dorsal.zRot = scull;
        anal.zRot = -scull;
        clavus.yRot = (state.isInWater ? 0.06F : 0.15F) * Mth.sin(0.05F * t + 0.7F);
        float flutter = (basking ? 0.05F : 0.15F) * Mth.sin(0.3F * t);
        // on land they lie nearly flat against the body (critic round 2: one stuck out like a handle)
        float yaw = state.isInWater ? finYaw : 0.25F * finYaw;
        leftFin.yRot = yaw + flutter;
        rightFin.yRot = -yaw - flutter;
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create()
            /* body00 */ .texOffs(192, 15).addBox(-2.0F, -10.5F, -6.0F, 4.0F, 1.0F, 7.0F)
            /* body01 */ .texOffs(176, 0).addBox(-1.5F, -10.5F, 1.0F, 3.0F, 2.0F, 8.0F)
            /* body02 */ .texOffs(50, 41).addBox(-1.5F, -9.5F, -8.0F, 3.0F, 1.0F, 1.0F)
            /* body03 */ .texOffs(220, 0).addBox(-2.0F, -9.5F, -7.0F, 4.0F, 1.0F, 8.0F)
            /* body04 */ .texOffs(58, 41).addBox(-1.5F, -8.5F, -9.0F, 3.0F, 1.0F, 1.0F)
            /* body05 */ .texOffs(246, 38).addBox(-2.0F, -8.5F, -8.0F, 4.0F, 1.0F, 1.0F)
            /* body06 */ .texOffs(124, 0).addBox(-2.5F, -8.5F, -7.0F, 5.0F, 2.0F, 8.0F)
            /* body07 */ .texOffs(156, 24).addBox(-2.0F, -8.5F, 1.0F, 4.0F, 2.0F, 4.0F)
            /* body08 */ .texOffs(188, 24).addBox(-1.5F, -8.5F, 5.0F, 3.0F, 2.0F, 4.0F)
            /* body09 */ .texOffs(66, 41).addBox(-1.5F, -7.5F, -10.0F, 3.0F, 1.0F, 1.0F)
            /* body10 */ .texOffs(232, 32).addBox(-2.0F, -7.5F, -9.0F, 4.0F, 1.0F, 2.0F)
            /* body11 */ .texOffs(112, 32).addBox(-1.5F, -6.5F, -11.0F, 3.0F, 3.0F, 1.0F)
            /* body12 */ .texOffs(84, 32).addBox(-2.0F, -6.5F, -10.0F, 4.0F, 1.0F, 3.0F)
            /* body13 */ .texOffs(222, 38).addBox(-2.5F, -6.5F, -7.0F, 5.0F, 1.0F, 1.0F)
            /* body14 */ .texOffs(140, 15).addBox(-3.0F, -6.5F, -6.0F, 6.0F, 1.0F, 7.0F)
            /* body15 */ .texOffs(32, 24).addBox(-2.5F, -6.5F, 1.0F, 5.0F, 3.0F, 4.0F)
            /* body16 */ .texOffs(68, 24).addBox(-2.0F, -6.5F, 5.0F, 4.0F, 3.0F, 4.0F)
            /* body17 */ .texOffs(0, 41).addBox(-2.0F, -5.5F, -10.0F, 4.0F, 1.0F, 1.0F)
            /* body18 */ .texOffs(176, 32).addBox(-2.5F, -5.5F, -9.0F, 5.0F, 1.0F, 2.0F)
            /* body19 */ .texOffs(68, 0).addBox(-3.0F, -5.5F, -7.0F, 6.0F, 2.0F, 8.0F)
            /* body20 */ .texOffs(152, 32).addBox(-1.0F, -4.5F, -12.0F, 2.0F, 3.0F, 1.0F)
            /* body21 */ .texOffs(52, 32).addBox(-2.5F, -4.5F, -10.0F, 5.0F, 1.0F, 3.0F)
            /* body22 */ .texOffs(10, 41).addBox(-2.0F, -3.5F, -11.0F, 4.0F, 1.0F, 1.0F)
            /* body23 */ .texOffs(190, 32).addBox(-2.5F, -3.5F, -10.0F, 5.0F, 1.0F, 2.0F)
            /* body24 */ .texOffs(194, 38).addBox(-3.0F, -3.5F, -8.0F, 6.0F, 1.0F, 1.0F)
            /* body25 */ .texOffs(0, 0).addBox(-3.5F, -3.5F, -7.0F, 7.0F, 7.0F, 8.0F)
            /* body26 */ .texOffs(30, 0).addBox(-3.0F, -3.5F, 1.0F, 6.0F, 7.0F, 4.0F)
            /* body27 */ .texOffs(50, 0).addBox(-2.5F, -3.5F, 5.0F, 5.0F, 7.0F, 4.0F)
            /* body28 */ .texOffs(216, 24).addBox(-2.5F, -2.5F, -11.0F, 5.0F, 5.0F, 1.0F)
            /* body29 */ .texOffs(236, 15).addBox(-3.0F, -2.5F, -10.0F, 6.0F, 5.0F, 3.0F)
            /* body30 */ .texOffs(120, 32).addBox(-1.5F, -1.5F, -12.0F, 3.0F, 3.0F, 1.0F)
            /* body31 */ .texOffs(158, 32).addBox(-1.0F, 1.5F, -12.0F, 2.0F, 3.0F, 1.0F)
            /* body32 */ .texOffs(20, 41).addBox(-2.0F, 2.5F, -11.0F, 4.0F, 1.0F, 1.0F)
            /* body33 */ .texOffs(204, 32).addBox(-2.5F, 2.5F, -10.0F, 5.0F, 1.0F, 2.0F)
            /* body34 */ .texOffs(208, 38).addBox(-3.0F, 2.5F, -8.0F, 6.0F, 1.0F, 1.0F)
            /* body35 */ .texOffs(128, 32).addBox(-1.5F, 3.5F, -11.0F, 3.0F, 3.0F, 1.0F)
            /* body36 */ .texOffs(68, 32).addBox(-2.5F, 3.5F, -10.0F, 5.0F, 1.0F, 3.0F)
            /* body37 */ .texOffs(96, 0).addBox(-3.0F, 3.5F, -7.0F, 6.0F, 2.0F, 8.0F)
            /* body38 */ .texOffs(50, 24).addBox(-2.5F, 3.5F, 1.0F, 5.0F, 3.0F, 4.0F)
            /* body39 */ .texOffs(84, 24).addBox(-2.0F, 3.5F, 5.0F, 4.0F, 3.0F, 4.0F)
            /* body40 */ .texOffs(30, 41).addBox(-2.0F, 4.5F, -10.0F, 4.0F, 1.0F, 1.0F)
            /* body41 */ .texOffs(218, 32).addBox(-2.5F, 4.5F, -9.0F, 5.0F, 1.0F, 2.0F)
            /* body42 */ .texOffs(98, 32).addBox(-2.0F, 5.5F, -10.0F, 4.0F, 1.0F, 3.0F)
            /* body43 */ .texOffs(234, 38).addBox(-2.5F, 5.5F, -7.0F, 5.0F, 1.0F, 1.0F)
            /* body44 */ .texOffs(166, 15).addBox(-3.0F, 5.5F, -6.0F, 6.0F, 1.0F, 7.0F)
            /* body45 */ .texOffs(74, 41).addBox(-1.5F, 6.5F, -10.0F, 3.0F, 1.0F, 1.0F)
            /* body46 */ .texOffs(244, 32).addBox(-2.0F, 6.5F, -9.0F, 4.0F, 1.0F, 2.0F)
            /* body47 */ .texOffs(150, 0).addBox(-2.5F, 6.5F, -7.0F, 5.0F, 2.0F, 8.0F)
            /* body48 */ .texOffs(172, 24).addBox(-2.0F, 6.5F, 1.0F, 4.0F, 2.0F, 4.0F)
            /* body49 */ .texOffs(202, 24).addBox(-1.5F, 6.5F, 5.0F, 3.0F, 2.0F, 4.0F)
            /* body50 */ .texOffs(82, 41).addBox(-1.5F, 7.5F, -9.0F, 3.0F, 1.0F, 1.0F)
            /* body51 */ .texOffs(40, 41).addBox(-2.0F, 7.5F, -8.0F, 4.0F, 1.0F, 1.0F)
            /* body52 */ .texOffs(90, 41).addBox(-1.5F, 8.5F, -8.0F, 3.0F, 1.0F, 1.0F)
            /* body53 */ .texOffs(0, 15).addBox(-2.0F, 8.5F, -7.0F, 4.0F, 1.0F, 8.0F)
            /* body54 */ .texOffs(198, 0).addBox(-1.5F, 8.5F, 1.0F, 3.0F, 2.0F, 8.0F)
            /* body55 */ .texOffs(214, 15).addBox(-2.0F, 9.5F, -6.0F, 4.0F, 1.0F, 7.0F)
            /* eye_l */ .texOffs(164, 32).addBox(3.0F, -5.5F, -6.0F, 1.0F, 2.0F, 2.0F)
            /* eye_r */ .texOffs(170, 32).addBox(-4.0F, -5.5F, -6.0F, 1.0F, 2.0F, 2.0F)
            /* mouth */ .texOffs(120, 38).addBox(-1.0F, -2.5F, -13.0F, 2.0F, 2.0F, 1.0F),
            PartPose.offset(0.0F, 4.5F, 0.0F));
        root.addOrReplaceChild("dorsal_fin", CubeListBuilder.create()
            /* dorsal00 */ .texOffs(24, 15).addBox(-1.0F, -1.0F, -3.5F, 2.0F, 1.0F, 8.0F)
            /* dorsal01 */ .texOffs(64, 15).addBox(-1.0F, -2.0F, -3.5F, 2.0F, 1.0F, 8.0F)
            /* dorsal02 */ .texOffs(104, 15).addBox(-0.5F, -3.0F, -3.5F, 1.0F, 1.0F, 8.0F)
            /* dorsal03 */ .texOffs(0, 24).addBox(-0.5F, -4.0F, -2.5F, 1.0F, 1.0F, 7.0F)
            /* dorsal04 */ .texOffs(100, 24).addBox(-0.5F, -5.0F, -1.5F, 1.0F, 1.0F, 6.0F)
            /* dorsal05 */ .texOffs(128, 24).addBox(-0.5F, -6.0F, -1.5F, 1.0F, 1.0F, 6.0F)
            /* dorsal06 */ .texOffs(228, 24).addBox(-0.5F, -7.0F, -0.5F, 1.0F, 1.0F, 5.0F)
            /* dorsal07 */ .texOffs(12, 32).addBox(-0.5F, -8.0F, 0.5F, 1.0F, 1.0F, 4.0F)
            /* dorsal08 */ .texOffs(32, 32).addBox(-0.5F, -9.0F, 0.5F, 1.0F, 1.0F, 4.0F)
            /* dorsal09 */ .texOffs(136, 32).addBox(-0.5F, -10.0F, 1.5F, 1.0F, 1.0F, 3.0F)
            /* dorsal10 */ .texOffs(126, 38).addBox(-0.5F, -11.0F, 2.5F, 1.0F, 1.0F, 2.0F),
            PartPose.offset(0.0F, -3.5F, 5.0F));
        root.addOrReplaceChild("anal_fin", CubeListBuilder.create()
            /* anal00 */ .texOffs(44, 15).addBox(-1.0F, 0.0F, -3.5F, 2.0F, 1.0F, 8.0F)
            /* anal01 */ .texOffs(84, 15).addBox(-1.0F, 1.0F, -3.5F, 2.0F, 1.0F, 8.0F)
            /* anal02 */ .texOffs(122, 15).addBox(-0.5F, 2.0F, -3.5F, 1.0F, 1.0F, 8.0F)
            /* anal03 */ .texOffs(16, 24).addBox(-0.5F, 3.0F, -2.5F, 1.0F, 1.0F, 7.0F)
            /* anal04 */ .texOffs(114, 24).addBox(-0.5F, 4.0F, -1.5F, 1.0F, 1.0F, 6.0F)
            /* anal05 */ .texOffs(142, 24).addBox(-0.5F, 5.0F, -1.5F, 1.0F, 1.0F, 6.0F)
            /* anal06 */ .texOffs(240, 24).addBox(-0.5F, 6.0F, -0.5F, 1.0F, 1.0F, 5.0F)
            /* anal07 */ .texOffs(22, 32).addBox(-0.5F, 7.0F, 0.5F, 1.0F, 1.0F, 4.0F)
            /* anal08 */ .texOffs(42, 32).addBox(-0.5F, 8.0F, 0.5F, 1.0F, 1.0F, 4.0F)
            /* anal09 */ .texOffs(144, 32).addBox(-0.5F, 9.0F, 1.5F, 1.0F, 1.0F, 3.0F)
            /* anal10 */ .texOffs(132, 38).addBox(-0.5F, 10.0F, 2.5F, 1.0F, 1.0F, 2.0F),
            PartPose.offset(0.0F, 12.5F, 5.0F));
        root.addOrReplaceChild("clavus", CubeListBuilder.create()
            /* clavus_in00 */ .texOffs(0, 38).addBox(-1.0F, -7.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_in01 */ .texOffs(8, 38).addBox(-1.0F, -6.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim01 */ .texOffs(98, 41).addBox(-0.5F, -6.5F, 2.0F, 1.0F, 1.0F, 1.0F)
            /* clavus_in02 */ .texOffs(16, 38).addBox(-1.0F, -5.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim02 */ .texOffs(138, 38).addBox(-0.5F, -5.5F, 2.0F, 1.0F, 1.0F, 2.0F)
            /* clavus_in03 */ .texOffs(24, 38).addBox(-1.0F, -4.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim03 */ .texOffs(144, 38).addBox(-0.5F, -4.5F, 2.0F, 1.0F, 1.0F, 2.0F)
            /* clavus_in04 */ .texOffs(32, 38).addBox(-1.0F, -3.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim04 */ .texOffs(102, 41).addBox(-0.5F, -3.5F, 2.0F, 1.0F, 1.0F, 1.0F)
            /* clavus_in05 */ .texOffs(40, 38).addBox(-1.0F, -2.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim05 */ .texOffs(150, 38).addBox(-0.5F, -2.5F, 2.0F, 1.0F, 1.0F, 2.0F)
            /* clavus_in06 */ .texOffs(48, 38).addBox(-1.0F, -1.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim06 */ .texOffs(156, 38).addBox(-0.5F, -1.5F, 2.0F, 1.0F, 1.0F, 2.0F)
            /* clavus_in07 */ .texOffs(56, 38).addBox(-1.0F, -0.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim07 */ .texOffs(106, 41).addBox(-0.5F, -0.5F, 2.0F, 1.0F, 1.0F, 1.0F)
            /* clavus_in08 */ .texOffs(64, 38).addBox(-1.0F, 0.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim08 */ .texOffs(162, 38).addBox(-0.5F, 0.5F, 2.0F, 1.0F, 1.0F, 2.0F)
            /* clavus_in09 */ .texOffs(72, 38).addBox(-1.0F, 1.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim09 */ .texOffs(168, 38).addBox(-0.5F, 1.5F, 2.0F, 1.0F, 1.0F, 2.0F)
            /* clavus_in10 */ .texOffs(80, 38).addBox(-1.0F, 2.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim10 */ .texOffs(110, 41).addBox(-0.5F, 2.5F, 2.0F, 1.0F, 1.0F, 1.0F)
            /* clavus_in11 */ .texOffs(88, 38).addBox(-1.0F, 3.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim11 */ .texOffs(174, 38).addBox(-0.5F, 3.5F, 2.0F, 1.0F, 1.0F, 2.0F)
            /* clavus_in12 */ .texOffs(96, 38).addBox(-1.0F, 4.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim12 */ .texOffs(180, 38).addBox(-0.5F, 4.5F, 2.0F, 1.0F, 1.0F, 2.0F)
            /* clavus_in13 */ .texOffs(104, 38).addBox(-1.0F, 5.5F, 0.0F, 2.0F, 1.0F, 2.0F)
            /* clavus_rim13 */ .texOffs(114, 41).addBox(-0.5F, 5.5F, 2.0F, 1.0F, 1.0F, 1.0F)
            /* clavus_in14 */ .texOffs(112, 38).addBox(-1.0F, 6.5F, 0.0F, 2.0F, 1.0F, 2.0F),
            PartPose.offset(0.0F, 4.5F, 9.0F));
        root.addOrReplaceChild("left_fin", CubeListBuilder.create()
            /* l_pec1 */ .texOffs(0, 32).addBox(0.0F, -2.0F, 0.0F, 1.0F, 4.0F, 2.0F)
            /* l_pec2 */ .texOffs(186, 38).addBox(0.0F, -1.0F, 2.0F, 1.0F, 2.0F, 1.0F),
            PartPose.offsetAndRotation(3.5F, 4.0F, -2.0F, 0.0F, 0.45F, 0.0F));
        root.addOrReplaceChild("right_fin", CubeListBuilder.create()
            /* r_pec1 */ .texOffs(6, 32).addBox(-1.0F, -2.0F, 0.0F, 1.0F, 4.0F, 2.0F)
            /* r_pec2 */ .texOffs(190, 38).addBox(-1.0F, -1.0F, 2.0F, 1.0F, 2.0F, 1.0F),
            PartPose.offsetAndRotation(-3.5F, 4.0F, -2.0F, 0.0F, -0.45F, 0.0F));
        return LayerDefinition.create(mesh, 256, 128);
    }
}
