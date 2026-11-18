package com.maltaminecraft.mimcontent.client.jelly;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * The fried-egg jellyfish (Cotylorhiza tuberculata): a wide, flat, cream-yellow bell 15 px across with a raised
 * orange-yellow dome in the middle (the "yolk"), and under it a short, wide drum of oral arms studded
 * with white knobs above and purple-blue ones below, with a few short knobbed filaments hanging under it. Round layers are
 * built of 1 px strips, so nothing overlaps; faces against another box are clear in the texture.
 * Made by art/src/jelly_fried_egg_model.py (do not edit by hand); texture
 * textures/entity/jellyfish/fried_egg_jellyfish.png. Parts: "bell" (pulsed by JellyfishModel), "oral_arms"
 * in it, and "tentacle_0".. "tentacle_5" in it (swayed by JellyfishModel).
 */
public class FriedEggJellyfishModel extends JellyfishModel {
    public FriedEggJellyfishModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        PartDefinition bell = root.addOrReplaceChild("bell", CubeListBuilder.create()
            .texOffs(76, 114).addBox(-7.5F, -2.0F, -2.5F, 1.0F, 2.0F, 5.0F)
            .texOffs(0, 93).addBox(-6.5F, -2.0F, -4.5F, 1.0F, 2.0F, 9.0F)
            .texOffs(24, 66).addBox(-5.5F, -2.0F, -5.5F, 1.0F, 2.0F, 11.0F)
            .texOffs(56, 34).addBox(-4.5F, -2.0F, -6.5F, 1.0F, 2.0F, 13.0F)
            .texOffs(84, 34).addBox(-3.5F, -2.0F, -6.5F, 1.0F, 2.0F, 13.0F)
            .texOffs(0, 0).addBox(-2.5F, -2.0F, -7.5F, 1.0F, 2.0F, 15.0F)
            .texOffs(32, 0).addBox(-1.5F, -2.0F, -7.5F, 1.0F, 2.0F, 15.0F)
            .texOffs(64, 0).addBox(-0.5F, -2.0F, -7.5F, 1.0F, 2.0F, 15.0F)
            .texOffs(96, 0).addBox(0.5F, -2.0F, -7.5F, 1.0F, 2.0F, 15.0F)
            .texOffs(0, 17).addBox(1.5F, -2.0F, -7.5F, 1.0F, 2.0F, 15.0F)
            .texOffs(0, 51).addBox(2.5F, -2.0F, -6.5F, 1.0F, 2.0F, 13.0F)
            .texOffs(28, 51).addBox(3.5F, -2.0F, -6.5F, 1.0F, 2.0F, 13.0F)
            .texOffs(48, 66).addBox(4.5F, -2.0F, -5.5F, 1.0F, 2.0F, 11.0F)
            .texOffs(20, 93).addBox(5.5F, -2.0F, -4.5F, 1.0F, 2.0F, 9.0F)
            .texOffs(88, 114).addBox(6.5F, -2.0F, -2.5F, 1.0F, 2.0F, 5.0F)
            .texOffs(0, 123).addBox(-7.5F, 0.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(68, 129).addBox(-6.5F, 0.0F, -4.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(74, 129).addBox(-6.5F, 0.0F, 2.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(20, 135).addBox(-5.5F, 0.0F, -5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(24, 135).addBox(-5.5F, 0.0F, 4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(28, 135).addBox(-4.5F, 0.0F, -6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(32, 135).addBox(-4.5F, 0.0F, 5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(36, 135).addBox(-3.5F, 0.0F, -6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(40, 135).addBox(-3.5F, 0.0F, 5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(44, 135).addBox(-2.5F, 0.0F, -7.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(48, 135).addBox(-2.5F, 0.0F, 6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(52, 135).addBox(-1.5F, 0.0F, -7.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(56, 135).addBox(-1.5F, 0.0F, 6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(60, 135).addBox(-0.5F, 0.0F, -7.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(64, 135).addBox(-0.5F, 0.0F, 6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(68, 135).addBox(0.5F, 0.0F, -7.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(72, 135).addBox(0.5F, 0.0F, 6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(76, 135).addBox(1.5F, 0.0F, -7.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(80, 135).addBox(1.5F, 0.0F, 6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(84, 135).addBox(2.5F, 0.0F, -6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(88, 135).addBox(2.5F, 0.0F, 5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(92, 135).addBox(3.5F, 0.0F, -6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(96, 135).addBox(3.5F, 0.0F, 5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(100, 135).addBox(4.5F, 0.0F, -5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(104, 135).addBox(4.5F, 0.0F, 4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(80, 129).addBox(5.5F, 0.0F, -4.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(86, 129).addBox(5.5F, 0.0F, 2.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(12, 123).addBox(6.5F, 0.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(24, 123).addBox(-5.5F, -3.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(108, 135).addBox(-4.5F, -3.0F, -3.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(112, 135).addBox(-4.5F, -3.0F, 2.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(116, 135).addBox(-3.5F, -3.0F, -4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(120, 135).addBox(-3.5F, -3.0F, 3.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(124, 135).addBox(-2.5F, -3.0F, -5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(0, 138).addBox(-2.5F, -3.0F, 4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(4, 138).addBox(-1.5F, -3.0F, -5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(8, 138).addBox(-1.5F, -3.0F, 4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(12, 138).addBox(-0.5F, -3.0F, -5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(16, 138).addBox(-0.5F, -3.0F, 4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(20, 138).addBox(0.5F, -3.0F, -5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(24, 138).addBox(0.5F, -3.0F, 4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(28, 138).addBox(1.5F, -3.0F, -5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(32, 138).addBox(1.5F, -3.0F, 4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(36, 138).addBox(2.5F, -3.0F, -4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(40, 138).addBox(2.5F, -3.0F, 3.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(44, 138).addBox(3.5F, -3.0F, -3.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(48, 138).addBox(3.5F, -3.0F, 2.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(36, 123).addBox(4.5F, -3.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(48, 123).addBox(-4.5F, -3.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(92, 129).addBox(-3.5F, -3.0F, -3.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(98, 129).addBox(-3.5F, -3.0F, 1.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(104, 129).addBox(-2.5F, -3.0F, -4.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(110, 129).addBox(-2.5F, -3.0F, 2.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(52, 138).addBox(-1.5F, -3.0F, -4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(56, 138).addBox(-1.5F, -3.0F, 3.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(60, 138).addBox(-0.5F, -3.0F, -4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(64, 138).addBox(-0.5F, -3.0F, 3.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(68, 138).addBox(0.5F, -3.0F, -4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(72, 138).addBox(0.5F, -3.0F, 3.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(116, 129).addBox(1.5F, -3.0F, -4.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(122, 129).addBox(1.5F, -3.0F, 2.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(0, 135).addBox(2.5F, -3.0F, -3.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(6, 135).addBox(2.5F, -3.0F, 1.5F, 1.0F, 1.0F, 2.0F)
            .texOffs(60, 123).addBox(3.5F, -3.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(36, 129).addBox(-3.5F, -4.0F, -1.5F, 1.0F, 2.0F, 3.0F)
            .texOffs(100, 114).addBox(-2.5F, -4.0F, -2.5F, 1.0F, 2.0F, 5.0F)
            .texOffs(60, 104).addBox(-1.5F, -4.0F, -3.5F, 1.0F, 2.0F, 7.0F)
            .texOffs(76, 104).addBox(-0.5F, -4.0F, -3.5F, 1.0F, 2.0F, 7.0F)
            .texOffs(92, 104).addBox(0.5F, -4.0F, -3.5F, 1.0F, 2.0F, 7.0F)
            .texOffs(112, 114).addBox(1.5F, -4.0F, -2.5F, 1.0F, 2.0F, 5.0F)
            .texOffs(44, 129).addBox(2.5F, -4.0F, -1.5F, 1.0F, 2.0F, 3.0F)
            .texOffs(52, 129).addBox(-2.5F, -5.0F, -1.5F, 1.0F, 1.0F, 3.0F)
            .texOffs(72, 123).addBox(-1.5F, -5.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(84, 123).addBox(-0.5F, -5.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(96, 123).addBox(0.5F, -5.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(60, 129).addBox(1.5F, -5.0F, -1.5F, 1.0F, 1.0F, 3.0F),
            PartPose.offset(0.0F, 16.0F, 0.0F));
        bell.addOrReplaceChild("oral_arms", CubeListBuilder.create()
            .texOffs(108, 123).addBox(-4.5F, 0.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(12, 114).addBox(-3.5F, 0.0F, -3.5F, 1.0F, 1.0F, 7.0F)
            .texOffs(40, 93).addBox(-2.5F, 0.0F, -4.5F, 1.0F, 1.0F, 9.0F)
            .texOffs(60, 93).addBox(-1.5F, 0.0F, -4.5F, 1.0F, 1.0F, 9.0F)
            .texOffs(80, 93).addBox(-0.5F, 0.0F, -4.5F, 1.0F, 1.0F, 9.0F)
            .texOffs(100, 93).addBox(0.5F, 0.0F, -4.5F, 1.0F, 1.0F, 9.0F)
            .texOffs(0, 104).addBox(1.5F, 0.0F, -4.5F, 1.0F, 1.0F, 9.0F)
            .texOffs(28, 114).addBox(2.5F, 0.0F, -3.5F, 1.0F, 1.0F, 7.0F)
            .texOffs(0, 129).addBox(3.5F, 0.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(108, 104).addBox(-6.5F, 1.0F, -2.5F, 1.0F, 4.0F, 5.0F)
            .texOffs(72, 66).addBox(-5.5F, 1.0F, -4.5F, 1.0F, 4.0F, 9.0F)
            .texOffs(56, 51).addBox(-4.5F, 1.0F, -5.5F, 1.0F, 4.0F, 11.0F)
            .texOffs(80, 51).addBox(-3.5F, 1.0F, -5.5F, 1.0F, 4.0F, 11.0F)
            .texOffs(32, 17).addBox(-2.5F, 1.0F, -6.5F, 1.0F, 4.0F, 13.0F)
            .texOffs(60, 17).addBox(-1.5F, 1.0F, -6.5F, 1.0F, 4.0F, 13.0F)
            .texOffs(88, 17).addBox(-0.5F, 1.0F, -6.5F, 1.0F, 4.0F, 13.0F)
            .texOffs(0, 34).addBox(0.5F, 1.0F, -6.5F, 1.0F, 4.0F, 13.0F)
            .texOffs(28, 34).addBox(1.5F, 1.0F, -6.5F, 1.0F, 4.0F, 13.0F)
            .texOffs(104, 51).addBox(2.5F, 1.0F, -5.5F, 1.0F, 4.0F, 11.0F)
            .texOffs(0, 66).addBox(3.5F, 1.0F, -5.5F, 1.0F, 4.0F, 11.0F)
            .texOffs(92, 66).addBox(4.5F, 1.0F, -4.5F, 1.0F, 4.0F, 9.0F)
            .texOffs(0, 114).addBox(5.5F, 1.0F, -2.5F, 1.0F, 4.0F, 5.0F)
            .texOffs(12, 129).addBox(-5.5F, 5.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(44, 114).addBox(-4.5F, 5.0F, -3.5F, 1.0F, 1.0F, 7.0F)
            .texOffs(20, 104).addBox(-3.5F, 5.0F, -4.5F, 1.0F, 1.0F, 9.0F)
            .texOffs(0, 81).addBox(-2.5F, 5.0F, -5.5F, 1.0F, 1.0F, 11.0F)
            .texOffs(24, 81).addBox(-1.5F, 5.0F, -5.5F, 1.0F, 1.0F, 11.0F)
            .texOffs(48, 81).addBox(-0.5F, 5.0F, -5.5F, 1.0F, 1.0F, 11.0F)
            .texOffs(72, 81).addBox(0.5F, 5.0F, -5.5F, 1.0F, 1.0F, 11.0F)
            .texOffs(96, 81).addBox(1.5F, 5.0F, -5.5F, 1.0F, 1.0F, 11.0F)
            .texOffs(40, 104).addBox(2.5F, 5.0F, -4.5F, 1.0F, 1.0F, 9.0F)
            .texOffs(60, 114).addBox(3.5F, 5.0F, -3.5F, 1.0F, 1.0F, 7.0F)
            .texOffs(24, 129).addBox(4.5F, 5.0F, -2.5F, 1.0F, 1.0F, 5.0F)
            .texOffs(92, 138).addBox(-6.5F, 1.0F, 2.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(96, 138).addBox(-4.5F, 4.0F, 5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(100, 138).addBox(-2.5F, 5.0F, -6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(104, 138).addBox(-1.5F, 2.0F, -7.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(108, 138).addBox(-1.5F, 5.0F, 5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(112, 138).addBox(-0.5F, 3.0F, -7.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(116, 138).addBox(0.5F, 1.0F, 6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(120, 138).addBox(1.5F, 3.0F, -7.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(124, 138).addBox(1.5F, 4.0F, 6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(0, 140).addBox(3.5F, 3.0F, 5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(4, 140).addBox(3.5F, 4.0F, -6.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(8, 140).addBox(4.5F, 1.0F, -5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(12, 140).addBox(4.5F, 5.0F, -3.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(16, 140).addBox(5.5F, 1.0F, -3.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(20, 140).addBox(-7.5F, 2.0F, -2.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(24, 140).addBox(-7.5F, 2.0F, -1.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(28, 140).addBox(-7.5F, 2.0F, 1.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(32, 140).addBox(-7.5F, 3.0F, -0.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(36, 140).addBox(6.5F, 2.0F, -2.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(40, 140).addBox(6.5F, 2.0F, -0.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(44, 140).addBox(-5.5F, 6.0F, -1.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(48, 140).addBox(-5.5F, 5.0F, 2.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(52, 140).addBox(-4.5F, 6.0F, -3.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(56, 140).addBox(-4.5F, 6.0F, 2.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(60, 140).addBox(-3.5F, 5.0F, 4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(64, 140).addBox(-1.5F, 6.0F, -5.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(68, 140).addBox(4.5F, 5.0F, -4.5F, 1.0F, 1.0F, 1.0F)
            .texOffs(72, 140).addBox(4.5F, 6.0F, 0.5F, 1.0F, 1.0F, 1.0F),
            PartPose.offset(0.0F, 0.0F, 0.0F));
        bell.addOrReplaceChild("tentacle_0", CubeListBuilder.create()
            .texOffs(12, 135).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 2.0F, 1.0F),
            PartPose.offset(-2.0F, 6.0F, -1.0F));
        bell.addOrReplaceChild("tentacle_1", CubeListBuilder.create()
            .texOffs(16, 135).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 2.0F, 1.0F),
            PartPose.offset(2.0F, 6.0F, 1.0F));
        bell.addOrReplaceChild("tentacle_2", CubeListBuilder.create()
            .texOffs(76, 138).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 1.0F, 1.0F),
            PartPose.offset(-1.0F, 6.0F, 3.0F));
        bell.addOrReplaceChild("tentacle_3", CubeListBuilder.create()
            .texOffs(80, 138).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 1.0F, 1.0F),
            PartPose.offset(1.0F, 6.0F, -3.0F));
        bell.addOrReplaceChild("tentacle_4", CubeListBuilder.create()
            .texOffs(84, 138).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 1.0F, 1.0F),
            PartPose.offset(-4.0F, 6.0F, 1.0F));
        bell.addOrReplaceChild("tentacle_5", CubeListBuilder.create()
            .texOffs(88, 138).addBox(-0.5F, 0.0F, -0.5F, 1.0F, 1.0F, 1.0F),
            PartPose.offset(4.0F, 6.0F, -1.0F));
        return LayerDefinition.create(mesh, 128, 256);
    }
}
