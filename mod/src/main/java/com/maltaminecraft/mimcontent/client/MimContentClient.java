package com.maltaminecraft.mimcontent.client;

import com.maltaminecraft.mimcontent.MimContent;
import com.maltaminecraft.mimcontent.MimFishes;
import com.maltaminecraft.mimcontent.client.fish.AwrataModel;
import com.maltaminecraft.mimcontent.client.fish.CawlModel;
import com.maltaminecraft.mimcontent.client.fish.CernaModel;
import com.maltaminecraft.mimcontent.client.fish.FishModel;
import com.maltaminecraft.mimcontent.client.fish.FishRenderer;
import com.maltaminecraft.mimcontent.client.fish.HutaKahlaModel;
import com.maltaminecraft.mimcontent.client.fish.IncovaModel;
import com.maltaminecraft.mimcontent.client.fish.LampukaModel;
import com.maltaminecraft.mimcontent.client.fish.MurinaModel;
import com.maltaminecraft.mimcontent.client.fish.PixxispadModel;
import com.maltaminecraft.mimcontent.client.fish.SardinaModel;
import com.maltaminecraft.mimcontent.client.fish.TonnModel;
import com.maltaminecraft.mimcontent.client.fish.ZiemelModel;
import java.util.function.Function;
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
    }

    private static void fish(MimFishes.Fish fish, net.fabricmc.fabric.api.client.rendering.v1.ModelLayerRegistry.TexturedLayerDefinitionProvider layer,
                             Function<ModelPart, FishModel> model, float shadow, float wiggle, float landLift) {
        ModelLayerLocation location = new ModelLayerLocation(MimContent.id("fish/" + fish.id()), "main");
        ModelLayerRegistry.registerModelLayer(location, layer);
        EntityRenderers.register(fish.type(), context -> new FishRenderer(context, model.apply(context.bakeLayer(location)), fish.id(), shadow, wiggle, landLift));
    }
}
