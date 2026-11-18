package com.maltaminecraft.mimcontent.mixin.client;

import net.minecraft.client.renderer.item.properties.select.SelectItemModelProperties;
import net.minecraft.client.renderer.item.properties.select.SelectItemModelProperty;
import net.minecraft.resources.Identifier;
import net.minecraft.util.ExtraCodecs;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;

/**
 * Vanilla's table of select item model properties (private), so the mod can add its own the way vanilla adds
 * {@code minecraft:custom_model_data} and the rest: {@link com.maltaminecraft.mimcontent.client.item.BucketVariantProperty}.
 */
@Mixin(SelectItemModelProperties.class)
public interface SelectItemModelPropertiesAccessor {
    @Accessor("ID_MAPPER")
    static ExtraCodecs.LateBoundIdMapper<Identifier, SelectItemModelProperty.Type<?, ?>> mimcontent$idMapper() {
        throw new AssertionError();
    }
}
