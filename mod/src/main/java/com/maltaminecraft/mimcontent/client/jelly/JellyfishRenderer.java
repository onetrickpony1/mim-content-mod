package com.maltaminecraft.mimcontent.client.jelly;

import com.maltaminecraft.mimcontent.MimContent;
import com.maltaminecraft.mimcontent.entity.jelly.Jellyfish;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.Identifier;
import net.minecraft.world.phys.AABB;

/**
 * Draws a jellyfish translucent (the model's render type) from textures/entity/jellyfish/&lt;id&gt;.png. A flashing
 * mauve stinger is drawn full-bright. The man o' war is kept drawn while only its long tentacles are on screen.
 */
public class JellyfishRenderer extends MobRenderer<Jellyfish, JellyfishRenderState, JellyfishModel> {
    private final Identifier texture;

    public JellyfishRenderer(EntityRendererProvider.Context context, JellyfishModel model, String id, float shadow) {
        super(context, model, shadow);
        this.texture = MimContent.id("textures/entity/jellyfish/" + id + ".png");
    }

    @Override
    public Identifier getTextureLocation(JellyfishRenderState state) {
        return texture;
    }

    @Override
    public JellyfishRenderState createRenderState() {
        return new JellyfishRenderState();
    }

    @Override
    public void extractRenderState(Jellyfish jelly, JellyfishRenderState state, float partialTick) {
        super.extractRenderState(jelly, state, partialTick);
        state.floats = jelly.kind().floats();
        state.flashing = jelly.isFlashing();
        state.pulse = jelly.pulseProgress(partialTick);
    }

    @Override
    protected int getBlockLightLevel(Jellyfish jelly, BlockPos pos) {
        return jelly.isFlashing() ? 15 : super.getBlockLightLevel(jelly, pos);
    }

    @Override
    protected AABB getBoundingBoxForCulling(Jellyfish jelly, float partialTicks) {
        AABB box = super.getBoundingBoxForCulling(jelly, partialTicks);
        return jelly.kind().floats() ? box.expandTowards(0.0, -(Jellyfish.MAN_O_WAR_TENTACLE_LENGTH + 0.5), 0.0) : box;
    }
}
