package com.maltaminecraft.mimcontent.client.item;

import com.maltaminecraft.mimcontent.MimContent;
import com.maltaminecraft.mimcontent.entity.fish.SkorfnaFish;
import com.maltaminecraft.mimcontent.mixin.client.SelectItemModelPropertiesAccessor;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.item.properties.select.SelectItemModelProperty;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;
import org.jspecify.annotations.Nullable;

/**
 * Item model property {@code mimcontent:bucket_variant}, for a {@code minecraft:select} item model: the version of the
 * fish inside a bucket, as the fish saved it ({@code Variant} in the bucket's entity data, e.g. "black" or "red" for the
 * skorfna, {@link SkorfnaFish#VARIANT_KEY}). A bucket with no saved version (empty, or filled before versions existed)
 * gives nothing, so the select's fallback model is drawn.
 * <p>
 * Vanilla's own select properties can't read inside the bucket's entity data (its {@code component} property only
 * matches a whole component value), so this one does, client side only: the bucket items stay plain
 * {@code MobBucketItem}s and the picture follows the data the fish already saves. Used by
 * {@code items/skorfna_bucket.json}: red shows {@code skorfna_red_bucket}, anything else the black one.
 */
public record BucketVariantProperty() implements SelectItemModelProperty<String> {
    public static final SelectItemModelProperty.Type<BucketVariantProperty, String> TYPE =
        SelectItemModelProperty.Type.create(MapCodec.unit(new BucketVariantProperty()), Codec.STRING);

    /** Registers the property under {@code mimcontent:bucket_variant}, beside vanilla's (call once, from the client entrypoint). */
    public static void register() {
        SelectItemModelPropertiesAccessor.mimcontent$idMapper().put(MimContent.id("bucket_variant"), TYPE);
    }

    @Override
    public @Nullable String get(ItemStack stack, @Nullable ClientLevel level, @Nullable LivingEntity owner, int seed, ItemDisplayContext context) {
        CustomData data = stack.get(DataComponents.BUCKET_ENTITY_DATA);
        return data == null ? null : data.copyTag().getString(SkorfnaFish.VARIANT_KEY).orElse(null);
    }

    @Override
    public Codec<String> valueCodec() {
        return Codec.STRING;
    }

    @Override
    public SelectItemModelProperty.Type<BucketVariantProperty, String> type() {
        return TYPE;
    }
}
