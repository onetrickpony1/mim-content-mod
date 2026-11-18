package com.maltaminecraft.mimcontent.entity.fish;

import com.maltaminecraft.mimcontent.MimContent;
import java.util.function.Supplier;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.util.Mth;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import org.jspecify.annotations.Nullable;

/**
 * The tonn, which comes in mixed sizes (owner 2026-11-18, "Mixed sizes"): each one is between 2 and 4 blocks long,
 * like a real school with young and old fish. The accepted model is drawn {@link #MODEL_LENGTH} blocks long; the whole
 * fish (model, hitbox, eyes and shadow) grows with vanilla's scale attribute, so what you see and what you hit match.
 * <ul>
 * <li>A new tonn (natural spawn, spawn egg, /summon) gets a random length, most often near 3 blocks. Fish spawned
 *     together as one school stay within about 10% of their leader's length.</li>
 * <li>The length is saved with the fish ({@code Length}, in blocks) and travels in the bucket, so a caught tonn comes
 *     out the same size. Clients learn it through the scale attribute, which vanilla syncs.</li>
 * <li>Health grows with length: 5 health per block (2 blocks: 10, 4 blocks: 20; the old fixed tonn had 12).</li>
 * </ul>
 */
public class TonnFish extends MimSchoolingFish {
    /** The accepted model's length in blocks, tail included (39 pixels). */
    public static final float MODEL_LENGTH = 39.0F / 16.0F;
    public static final float MIN_LENGTH = 2.0F;
    public static final float MAX_LENGTH = 4.0F;
    /** Health per block of length. */
    public static final float HEALTH_PER_BLOCK = 5.0F;
    private static final AttributeModifier.Operation ADD = AttributeModifier.Operation.ADD_VALUE;
    private static final net.minecraft.resources.Identifier SIZE_ID = MimContent.id("tonn_size");
    private static final String KEY = "Length";

    private float length = MODEL_LENGTH;

    public TonnFish(EntityType<? extends MimSchoolingFish> type, Level level, Supplier<Item> bucket, int schoolSize) {
        super(type, level, bucket, schoolSize);
    }

    /** The fish's length in blocks, tail included. */
    public float getLength() {
        return length;
    }

    /** Sets the length (kept within 2 to 4 blocks), scaling the fish and its maximum health to match. */
    public void setLength(float blocks) {
        length = Mth.clamp(blocks, MIN_LENGTH, MAX_LENGTH);
        AttributeInstance scale = getAttribute(Attributes.SCALE);
        if (scale != null) {
            scale.addOrUpdateTransientModifier(new AttributeModifier(SIZE_ID, length / MODEL_LENGTH - 1.0, ADD));
        }
        AttributeInstance health = getAttribute(Attributes.MAX_HEALTH);
        if (health != null) {
            health.setBaseValue(Math.round(length * HEALTH_PER_BLOCK));
        }
        refreshDimensions();
    }

    @Override
    public @Nullable SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, EntitySpawnReason reason,
                                                  @Nullable SpawnGroupData groupData) {
        SpawnGroupData out = super.finalizeSpawn(level, difficulty, reason, groupData);
        if (groupData instanceof SchoolSpawnGroupData school && school.leader instanceof TonnFish leader && leader != this) {
            setLength(leader.getLength() * (1.0F + getRandom().triangle(0.0F, 0.1F)));
        } else {
            setLength(getRandom().triangle(3.0F, 1.0F));
        }
        setHealth(getMaxHealth());
        return out;
    }

    @Override
    protected void addAdditionalSaveData(ValueOutput output) {
        super.addAdditionalSaveData(output);
        output.putFloat(KEY, length);
    }

    @Override
    protected void readAdditionalSaveData(ValueInput input) {
        super.readAdditionalSaveData(input);
        // a tonn saved before sizes existed keeps the old size
        setLength(input.getFloatOr(KEY, MODEL_LENGTH));
    }

    @Override
    public void saveToBucketTag(ItemStack bucket) {
        super.saveToBucketTag(bucket);
        CustomData.update(DataComponents.BUCKET_ENTITY_DATA, bucket, tag -> tag.putFloat(KEY, length));
    }

    @Override
    public void loadFromBucketTag(CompoundTag tag) {
        // the length first, so the saved health fits under the right maximum
        tag.getFloat(KEY).ifPresent(this::setLength);
        super.loadFromBucketTag(tag);
    }
}
