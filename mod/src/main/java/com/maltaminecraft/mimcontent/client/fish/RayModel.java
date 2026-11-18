package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.util.Mth;

/**
 * The base of a ray's model (the boll): a flat disc that swims by rippling its wing edges up and down, not by wagging
 * from side to side like a fish. Its renderer's body wiggle is 0 and it lies flat on land (FishRenderer liesFlat).
 * Model contract, on top of FishModel's (docs/Tools and Process/Art pipeline.md, "Fish models"):
 * <ul>
 * <li>{@code body} (root child, required): the middle of the disc, head toward -z; it stays flat;</li>
 * <li>{@code left_wing} (+x) and {@code right_wing} (-x), children of {@code body} (required), pivoted where they join
 *     the body: they flap up and down together;</li>
 * <li>{@code left_wing_tip} and {@code right_wing_tip} (optional), children of the wings, pivoted where they join: the
 *     outer edge, flapping a little later and further, so the wing ripples;</li>
 * <li>{@code left_wing_edge} and {@code right_wing_edge} (optional), children of the tips, pivoted where they join:
 *     a third, outermost ring, later again, so the ripple runs smoothly out to the wing corners;</li>
 * <li>{@code tail} (root child, required), pivoted at the back of the disc and running toward +z: it trails and sways
 *     slowly; the spine on it can be a child part {@code spine} (optional, not animated) or cubes of the tail.</li>
 * </ul>
 * The ripple is gentle when it lies still (upward only, so the wings never dip into the floor) and grows into a full
 * up-and-down beat as it swims faster; out of water the wings only flutter a little, upward.
 */
public abstract class RayModel extends FishModel {
    private final ModelPart leftWing;
    private final ModelPart rightWing;
    private final ModelPart leftTip;
    private final ModelPart rightTip;
    private final ModelPart leftEdge;
    private final ModelPart rightEdge;
    private final ModelPart tail;

    protected RayModel(ModelPart root) {
        super(root);
        ModelPart body = root.getChild("body");
        this.leftWing = body.getChild("left_wing");
        this.rightWing = body.getChild("right_wing");
        this.leftTip = leftWing.hasChild("left_wing_tip") ? leftWing.getChild("left_wing_tip") : null;
        this.rightTip = rightWing.hasChild("right_wing_tip") ? rightWing.getChild("right_wing_tip") : null;
        this.leftEdge = leftTip != null && leftTip.hasChild("left_wing_edge") ? leftTip.getChild("left_wing_edge") : null;
        this.rightEdge = rightTip != null && rightTip.hasChild("right_wing_edge") ? rightTip.getChild("right_wing_edge") : null;
        this.tail = root.getChild("tail");
    }

    @Override
    public void setupAnim(LivingEntityRenderState state) {
        super.setupAnim(state);
        float t = state.ageInTicks;
        float flap;
        float lag;
        float phase;
        // how much of the beat goes below flat: none while it lies still (on the floor, or on land) so the wings never
        // dip into the ground, a full up-and-down beat while it swims
        float swim;
        if (state.isInWater) {
            // 0.06 radians while still, up to 0.32 swimming; one beat about every 1.25 s
            float moving = Mth.clamp(state.walkAnimationSpeed * 2.0F, 0.0F, 1.0F);
            flap = 0.06F + 0.26F * moving;
            phase = 0.25F * t;
            lag = 0.9F;
            swim = moving;
        } else {
            flap = 0.05F;
            phase = 0.5F * t;
            lag = 0.6F;
            swim = 0.0F;
        }
        float wing = flap * beat(phase, swim);
        float tip = 1.3F * flap * beat(phase - lag, swim);
        float edge = 1.3F * flap * beat(phase - 2.0F * lag, swim);
        // +zRot turns the +x side down, so the two wings mirror each other
        leftWing.zRot = wing;
        rightWing.zRot = -wing;
        if (leftTip != null) {
            leftTip.zRot = tip;
        }
        if (rightTip != null) {
            rightTip.zRot = -tip;
        }
        if (leftEdge != null) {
            leftEdge.zRot = edge;
        }
        if (rightEdge != null) {
            rightEdge.zRot = -edge;
        }
        // the tail trails behind and sways slowly (FishModel's quick fish sway is replaced)
        tail.yRot = (state.isInWater ? 0.08F : 0.02F) * Mth.sin(0.1F * t);
        tail.xRot = state.isInWater ? 0.03F * Mth.sin(0.13F * t + 1.0F) : 0.0F;
    }

    /**
     * One ring's beat at this phase, from -1 (up) to 1 (down): a full sine while swimming (swim 1), only upward from
     * flat while still (swim 0), blended in between.
     */
    private static float beat(float phase, float swim) {
        float sin = Mth.sin(phase);
        return swim * sin - (1.0F - swim) * 0.5F * (1.0F + sin);
    }
}
