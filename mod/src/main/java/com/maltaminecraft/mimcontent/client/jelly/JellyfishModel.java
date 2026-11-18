package com.maltaminecraft.mimcontent.client.jelly;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.util.Mth;
import org.jspecify.annotations.Nullable;

/**
 * The base of every jellyfish model, with the animation, so a model only has to name its parts.
 * Model contract (docs/Tools and Process/Art pipeline.md, "Jellyfish models"):
 * <ul>
 * <li>{@code bell} (required), a child of the root: the bell, or the man o' war's float. A bell pulses (a slight squash
 *     and stretch on each pulse, and a faint breathing between); the float doesn't pulse, it bobs and tilts.</li>
 * <li>{@code tentacle_0} ... {@code tentacle_N} (optional), children of the root or of {@code bell}: each sways gently,
 *     out of phase with the others. Out of water they splay out from the middle, as the animal lies flat.</li>
 * <li>{@code oral_arms} (optional), a child of {@code bell}: sways slowly.</li>
 * </ul>
 * Drawn translucent (an entity translucent render type), so the texture's alpha shows. Y 24 is the bottom of the box.
 */
public abstract class JellyfishModel extends EntityModel<JellyfishRenderState> {
    private final ModelPart bell;
    private final @Nullable ModelPart oralArms;
    private final List<ModelPart> tentacles = new ArrayList<>();

    protected JellyfishModel(ModelPart root) {
        super(root, RenderTypes::entityTranslucent);
        this.bell = root.getChild("bell");
        this.oralArms = bell.hasChild("oral_arms") ? bell.getChild("oral_arms") : null;
        for (int i = 0; ; i++) {
            String name = "tentacle_" + i;
            if (root.hasChild(name)) {
                tentacles.add(root.getChild(name));
            } else if (bell.hasChild(name)) {
                tentacles.add(bell.getChild(name));
            } else {
                break;
            }
        }
    }

    @Override
    public void setupAnim(JellyfishRenderState state) {
        super.setupAnim(state);
        float t = state.ageInTicks;
        if (state.floats) {
            // the float rides the ripples: a small bob, a slow roll and pitch
            bell.y += 0.5F * Mth.sin(t * 0.12F);
            bell.zRot += 0.07F * Mth.sin(t * 0.09F);
            bell.xRot += 0.04F * Mth.sin(t * 0.07F + 1.0F);
        } else {
            float squeeze = state.pulse >= 0.0F ? Mth.sin(state.pulse * Mth.PI) : 0.0F;
            float breathe = 0.02F * Mth.sin(t * 0.1F);
            float wide = 1.0F - 0.14F * squeeze + breathe;
            float tall = 1.0F + 0.12F * squeeze - breathe;
            if (!state.isInWater) {
                // slumped on land
                wide *= 1.1F;
                tall *= 0.75F;
            }
            bell.xScale *= wide;
            bell.zScale *= wide;
            bell.yScale *= tall;
        }
        float sway = state.floats ? 0.04F : 0.12F;
        for (int i = 0; i < tentacles.size(); i++) {
            ModelPart tentacle = tentacles.get(i);
            tentacle.xRot += sway * Mth.sin(t * 0.08F + i * 1.7F);
            tentacle.zRot += sway * Mth.cos(t * 0.07F + i * 1.1F);
            if (!state.isInWater && !state.floats) {
                // lying on land: splay out from the middle
                PartPose rest = tentacle.getInitialPose();
                float r = Mth.sqrt(rest.x() * rest.x() + rest.z() * rest.z());
                if (r > 0.01F) {
                    tentacle.xRot += 1.2F * rest.z() / r;
                    tentacle.zRot -= 1.2F * rest.x() / r;
                }
            }
        }
        if (oralArms != null) {
            oralArms.yRot += 0.15F * Mth.sin(t * 0.04F);
            oralArms.zRot += 0.05F * Mth.sin(t * 0.06F);
        }
    }
}
