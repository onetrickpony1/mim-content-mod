package com.maltaminecraft.mimcontent.client;

import com.maltaminecraft.mimcontent.MimContent;
import com.maltaminecraft.mimcontent.MimFishes;
import com.maltaminecraft.mimcontent.client.fish.AwrataModel;
import com.maltaminecraft.mimcontent.client.fish.BollModel;
import com.maltaminecraft.mimcontent.client.fish.CawlModel;
import com.maltaminecraft.mimcontent.client.fish.CernaModel;
import com.maltaminecraft.mimcontent.client.fish.FishModel;
import com.maltaminecraft.mimcontent.client.fish.FishRenderer;
import com.maltaminecraft.mimcontent.client.fish.HutaKahlaModel;
import com.maltaminecraft.mimcontent.client.fish.IncovaModel;
import com.maltaminecraft.mimcontent.client.fish.LampukaModel;
import com.maltaminecraft.mimcontent.client.fish.MolaMolaModel;
import com.maltaminecraft.mimcontent.client.fish.MurinaModel;
import com.maltaminecraft.mimcontent.client.fish.PixxispadModel;
import com.maltaminecraft.mimcontent.client.fish.SardinaModel;
import com.maltaminecraft.mimcontent.client.fish.SkorfnaModel;
import com.maltaminecraft.mimcontent.client.fish.TonnModel;
import com.maltaminecraft.mimcontent.client.fish.ZiemelModel;
import com.maltaminecraft.mimcontent.entity.fish.SkorfnaFish;
import com.maltaminecraft.mimcontent.MimJellyfish;
import com.maltaminecraft.mimcontent.client.jelly.FriedEggJellyfishModel;
import com.maltaminecraft.mimcontent.client.jelly.JellyfishModel;
import com.maltaminecraft.mimcontent.client.jelly.JellyfishRenderer;
import com.maltaminecraft.mimcontent.client.jelly.ManOWarModel;
import com.maltaminecraft.mimcontent.client.jelly.MauveStingerModel;
import java.util.function.Function;
import net.fabricmc.fabric.api.client.item.v1.ItemTooltipCallback;
import net.minecraft.ChatFormatting;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import net.minecraft.world.item.component.CustomData;
import org.jspecify.annotations.Nullable;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.ModelLayerRegistry;
import net.minecraft.client.renderer.entity.EntityRenderers;

/** Client entrypoint: the luzzu's model and its renderers, one per colour scheme; the fish models and renderers. */
public class MimContentClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        ModelLayerRegistry.registerModelLayer(LuzzuRenderer.LAYER, LuzzuModel::createBodyLayer);
        ModelLayerRegistry.registerModelLayer(LuzzuRenderer.WATER_PATCH, LuzzuModel::createWaterPatch);
        EntityRenderers.register(MimContent.LUZZU, context -> new LuzzuRenderer(context, "luzzu"));
        EntityRenderers.register(MimContent.LUZZU_RED, context -> new LuzzuRenderer(context, "luzzu_red"));
        EntityRenderers.register(MimContent.LUZZU_BROWN, context -> new LuzzuRenderer(context, "luzzu_brown"));
        // the fish: model, shadow size, body wiggle in degrees (vanilla cod 4.3), lift on land in blocks (vanilla cod 0.1;
        // thick bodies need more so they don't sink into the ground: (half thickness in px + 0.5) / 16)
        fish(MimFishes.SARDINA, SardinaModel::createBodyLayer, SardinaModel::new, 0.2F, 4.3F, 0.1F);
        fish(MimFishes.TONN, TonnModel::createBodyLayer, TonnModel::new, 0.6F, 2.5F, 0.1875F);
        fish(MimFishes.LAMPUKA, LampukaModel::createBodyLayer, LampukaModel::new, 0.45F, 3.5F, 0.1F);
        fish(MimFishes.AWRATA, AwrataModel::createBodyLayer, AwrataModel::new, 0.35F, 4.3F, 0.1F);
        fish(MimFishes.CERNA, CernaModel::createBodyLayer, CernaModel::new, 0.45F, 3.0F, 0.21875F);
        fish(MimFishes.MURINA, MurinaModel::createBodyLayer, MurinaModel::new, 0.3F, 0.0F, 0.1875F);
        fish(MimFishes.ZIEMEL, ZiemelModel::createBodyLayer, ZiemelModel::new, 0.15F, 0.0F, 0.1F);
        fish(MimFishes.PIXXISPAD, PixxispadModel::createBodyLayer, PixxispadModel::new, 0.6F, 2.0F, 0.21875F);
        fish(MimFishes.INCOVA, IncovaModel::createBodyLayer, IncovaModel::new, 0.15F, 4.3F, 0.1F);
        fish(MimFishes.CAWL, CawlModel::createBodyLayer, CawlModel::new, 0.2F, 4.3F, 0.1F);
        fish(MimFishes.HUTA_KAHLA, HutaKahlaModel::createBodyLayer, HutaKahlaModel::new, 0.6F, 1.0F, 0.1875F);
        // the boll is flat: no body wiggle (its wings ripple instead, RayModel), and it lies flat on land (no lift needed)
        fish(MimFishes.BOLL, BollModel::createBodyLayer, BollModel::new, 0.6F, 0.0F, 0.0F, true);
        // the skorfna: stocky (5 px thick), a small wiggle as it barely swims
        // two versions on one model, black (skorfna.png) and red (skorfna_red.png), drawn by the fish's variant
        fish(MimFishes.SKORFNA, SkorfnaModel::createBodyLayer, SkorfnaModel::new, 0.35F, 2.0F, 0.1875F, false, MimContentClient::skorfnaTexture);
        // the mola mola: tall and thin, a slight wiggle; lying on its side (on land, or basking at the surface) its middle
        // lies over its position (the side shift); both numbers come from its model (art/src/fish_mola_model.py)
        ModelLayerLocation mola = new ModelLayerLocation(MimContent.id("fish/" + MimFishes.MOLA_MOLA.id()), "main");
        ModelLayerRegistry.registerModelLayer(mola, MolaMolaModel::createBodyLayer);
        EntityRenderers.register(MimFishes.MOLA_MOLA.type(), context -> new FishRenderer(context, new MolaMolaModel(context.bakeLayer(mola)),
            MimFishes.MOLA_MOLA.id(), 0.9F, 0.8F, MolaMolaModel.LAND_LIFT).withSideShift(MolaMolaModel.SIDE_SHIFT));
        // the jellyfish: model, shadow size (drawn translucent, JellyfishRenderer)
        jelly(MimJellyfish.MAUVE_STINGER, MauveStingerModel::createBodyLayer, MauveStingerModel::new, 0.25F);
        jelly(MimJellyfish.FRIED_EGG, FriedEggJellyfishModel::createBodyLayer, FriedEggJellyfishModel::new, 0.45F);
        jelly(MimJellyfish.MAN_O_WAR, ManOWarModel::createBodyLayer, ManOWarModel::new, 0.3F);
        // the skorfna bucket says which version is inside, as vanilla's tropical fish bucket names its pattern
        ItemTooltipCallback.EVENT.register((stack, context, flag, lines) -> {
            if (stack.is(MimFishes.SKORFNA.bucket())) {
                CompoundTag tag = stack.getOrDefault(DataComponents.BUCKET_ENTITY_DATA, CustomData.EMPTY).copyTag();
                SkorfnaFish.Variant variant = SkorfnaFish.Variant.byId(tag.getStringOr(SkorfnaFish.VARIANT_KEY, SkorfnaFish.Variant.BLACK.id()));
                lines.add(Math.min(1, lines.size()), Component.translatable(variant.translationKey()).withStyle(ChatFormatting.ITALIC, ChatFormatting.GRAY));
            }
        });
        // and shows it: items/skorfna_bucket.json picks the black or red picture by this property
        com.maltaminecraft.mimcontent.client.item.BucketVariantProperty.register();
    }

    private static void fish(MimFishes.Fish fish, net.fabricmc.fabric.api.client.rendering.v1.ModelLayerRegistry.TexturedLayerDefinitionProvider layer,
                             Function<ModelPart, FishModel> model, float shadow, float wiggle, float landLift) {
        fish(fish, layer, model, shadow, wiggle, landLift, false);
    }

    private static void fish(MimFishes.Fish fish, net.fabricmc.fabric.api.client.rendering.v1.ModelLayerRegistry.TexturedLayerDefinitionProvider layer,
                             Function<ModelPart, FishModel> model, float shadow, float wiggle, float landLift, boolean liesFlat) {
        fish(fish, layer, model, shadow, wiggle, landLift, liesFlat, null);
    }

    private static void fish(MimFishes.Fish fish, net.fabricmc.fabric.api.client.rendering.v1.ModelLayerRegistry.TexturedLayerDefinitionProvider layer,
                             Function<ModelPart, FishModel> model, float shadow, float wiggle, float landLift, boolean liesFlat,
                             @Nullable Function<AbstractFish, Identifier> textures) {
        ModelLayerLocation location = new ModelLayerLocation(MimContent.id("fish/" + fish.id()), "main");
        ModelLayerRegistry.registerModelLayer(location, layer);
        EntityRenderers.register(fish.type(), context -> {
            FishRenderer renderer = new FishRenderer(context, model.apply(context.bakeLayer(location)), fish.id(), shadow, wiggle, landLift, liesFlat);
            return textures == null ? renderer : renderer.withTextures(textures);
        });
    }

    private static void jelly(MimJellyfish.Jelly jelly, net.fabricmc.fabric.api.client.rendering.v1.ModelLayerRegistry.TexturedLayerDefinitionProvider layer,
                              Function<ModelPart, JellyfishModel> model, float shadow) {
        ModelLayerLocation location = new ModelLayerLocation(MimContent.id("jellyfish/" + jelly.id()), "main");
        ModelLayerRegistry.registerModelLayer(location, layer);
        EntityRenderers.register(jelly.type(), context -> new JellyfishRenderer(context, model.apply(context.bakeLayer(location)), jelly.id(), shadow));
    }

    /** The skorfna's texture by its version: black skorfna.png, red skorfna_red.png. */
    public static Identifier skorfnaTexture(AbstractFish fish) {
        boolean red = fish instanceof SkorfnaFish skorfna && skorfna.getVariant() == SkorfnaFish.Variant.RED;
        return MimContent.id("textures/entity/fish/skorfna" + (red ? "_red" : "") + ".png");
    }
}
