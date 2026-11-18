package com.maltaminecraft.mimcontent.client.fish;

import com.maltaminecraft.mimcontent.MimContent;
import com.maltaminecraft.mimcontent.entity.fish.MolaFish;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import java.util.function.Function;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.resources.Identifier;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import org.jspecify.annotations.Nullable;

/**
 * Draws a tier A fish like vanilla draws cod: the whole body wiggles a little as it swims, and out of water it lies on
 * its side and flops. A flat fish (the boll, {@code liesFlat}) stays flat on land, only lifted by its land lift.
 * Texture: textures/entity/fish/&lt;id&gt;.png, or one picked per fish ({@link #withTextures}, the skorfna's two versions).
 */
public class FishRenderer extends MobRenderer<AbstractFish, LivingEntityRenderState, FishModel> {
    /** How far off flat the mola mola lies while it basks, in degrees. */
    public static final float BASK_TILT = 12.0F;
    private final Identifier texture;
    private final float wiggle;
    private final float landLift;
    private final boolean liesFlat;
    /** A tall fish's shift back along its height when it lies on its side, in blocks (FishShape's sideShift). */
    private float sideShift;
    /** Picks the texture for each fish (a fish with versions), or null for the one texture. */
    private @Nullable Function<AbstractFish, Identifier> textures;

    /** The render state, with the texture picked for this fish. */
    public static class FishRenderState extends LivingEntityRenderState {
        public @Nullable Identifier texture;
        /** The mola mola lying on its side at the surface (MolaFish): drawn on its side, though in the water. */
        public boolean basking;
    }

    /**
     * wiggle: how far the body turns from side to side as it swims, in degrees (vanilla cod 4.3).
     * landLift: how far a fish lying on its side on land is lifted, in blocks, so a thick body doesn't sink into the
     * ground. Vanilla cod uses 0.1 for its thin body; a thicker fish needs about (half its thickness in px + 0.5) / 16.
     * It is applied before the entity's own scale, so a bigger tonn is lifted in proportion.
     */
    public FishRenderer(EntityRendererProvider.Context context, FishModel model, String id, float shadow, float wiggle, float landLift) {
        this(context, model, id, shadow, wiggle, landLift, false);
    }

    /** liesFlat: true for a flat fish (the boll) that lies flat on land instead of on its side. */
    public FishRenderer(EntityRendererProvider.Context context, FishModel model, String id, float shadow, float wiggle, float landLift, boolean liesFlat) {
        super(context, model, shadow);
        this.texture = MimContent.id("textures/entity/fish/" + id + ".png");
        this.wiggle = wiggle;
        this.landLift = landLift;
        this.liesFlat = liesFlat;
    }

    /** Picks each fish's texture from the fish (e.g. by its variant), instead of the one texture. */
    public FishRenderer withTextures(Function<AbstractFish, Identifier> textures) {
        this.textures = textures;
        return this;
    }

    /**
     * A tall fish (the mola mola): lying on its side, it is moved back along its height by this many blocks, so its
     * middle lies over its position instead of its belly. FishShape's sideShift copies it (the smoke test checks).
     */
    public FishRenderer withSideShift(float blocks) {
        this.sideShift = blocks;
        return this;
    }

    public float sideShift() {
        return sideShift;
    }

    /** The texture this renderer draws the fish with. */
    public Identifier textureFor(AbstractFish fish) {
        return textures == null ? texture : textures.apply(fish);
    }

    /** Whether it lies flat on land (FishShape's flat; the smoke test checks they agree). */
    public boolean liesFlat() {
        return liesFlat;
    }

    /** The land lift, which the fish's hit boxes copy (FishShape; the smoke test checks they agree). */
    public float landLift() {
        return landLift;
    }

    @Override
    public Identifier getTextureLocation(LivingEntityRenderState state) {
        return state instanceof FishRenderState fish && fish.texture != null ? fish.texture : texture;
    }

    @Override
    public LivingEntityRenderState createRenderState() {
        return new FishRenderState();
    }

    @Override
    public void extractRenderState(AbstractFish fish, LivingEntityRenderState state, float partialTick) {
        super.extractRenderState(fish, state, partialTick);
        if (state instanceof FishRenderState fishState) {
            fishState.texture = textureFor(fish);
            fishState.basking = fish instanceof MolaFish mola && mola.isBasking();
        }
    }

    @Override
    protected void setupRotations(LivingEntityRenderState state, PoseStack poseStack, float bodyRot, float entityScale) {
        super.setupRotations(state, poseStack, bodyRot, entityScale);
        boolean basking = state instanceof FishRenderState fish && fish.basking;
        if (!basking) {
            poseStack.rotateDegrees(Axis.YP, wiggle * Mth.sin(0.6F * state.ageInTicks));
        }
        if (!state.isInWater && liesFlat) {
            poseStack.translate(0.0F, landLift, 0.0F);
        } else if (!state.isInWater || basking) {
            poseStack.translate(0.1F, landLift, -0.1F);
            // basking (the mola mola) it lies a little off flat, BASK_TILT degrees, so its upper fin breaks the
            // surface at an angle; its hit boxes stay flat (the difference is at most about a quarter block at a fin tip)
            poseStack.rotateDegrees(Axis.ZP, basking && state.isInWater ? 90.0F - BASK_TILT : 90.0F);
            poseStack.translate(0.0F, -sideShift, 0.0F);
        }
    }
}
