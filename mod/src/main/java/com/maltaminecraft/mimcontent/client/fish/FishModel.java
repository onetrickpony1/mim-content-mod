package com.maltaminecraft.mimcontent.client.fish;

import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.util.Mth;

/**
 * The base of every fish model, with the swimming animation, so a generated model only has to name its parts.
 * Model contract (docs/Tools and Process/Art pipeline.md, "Fish models"):
 * <ul>
 * <li>a root child named {@code body} (required);</li>
 * <li>{@code tail_fin} (optional), a child of the root or of {@code tail}: it sways like vanilla cod's tail fin;</li>
 * <li>{@code tail} (optional), a child of the root: the back half of a long fish (the murina), swaying more gently
 *     like vanilla salmon's back half; put {@code tail_fin} inside it so the fin follows.</li>
 * </ul>
 * Out of water every swing is wider and quicker, as vanilla fish flop.
 */
public abstract class FishModel extends EntityModel<LivingEntityRenderState> {
    private final ModelPart tail;
    private final ModelPart tailFin;

    protected FishModel(ModelPart root) {
        super(root);
        root.getChild("body");
        this.tail = root.hasChild("tail") ? root.getChild("tail") : null;
        if (root.hasChild("tail_fin")) {
            this.tailFin = root.getChild("tail_fin");
        } else if (tail != null && tail.hasChild("tail_fin")) {
            this.tailFin = tail.getChild("tail_fin");
        } else {
            this.tailFin = null;
        }
    }

    @Override
    public void setupAnim(LivingEntityRenderState state) {
        super.setupAnim(state);
        float amplitude = state.isInWater ? 1.0F : 1.5F;
        float speed = state.isInWater ? 1.0F : 1.7F;
        float swing = Mth.sin(speed * 0.6F * state.ageInTicks);
        if (tail != null) {
            tail.yRot = -amplitude * 0.25F * swing;
        }
        if (tailFin != null) {
            tailFin.yRot = -amplitude * 0.45F * swing;
        }
    }
}
