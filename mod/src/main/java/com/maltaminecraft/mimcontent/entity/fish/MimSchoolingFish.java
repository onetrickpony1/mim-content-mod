package com.maltaminecraft.mimcontent.entity.fish;

import java.util.function.Supplier;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.fish.AbstractSchoolingFish;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import org.jspecify.annotations.Nullable;

/**
 * A fish that swims in schools, exactly like vanilla's cod (followers keep near a leader), with its own school size.
 * Used for the sardina, tonn and lampuka.
 */
public class MimSchoolingFish extends AbstractSchoolingFish implements FishParts.Holder {
    private final Supplier<Item> bucket;
    private final int schoolSize;
    /** The chain of hit boxes along the body (FishParts), or null. */
    private final @Nullable FishParts parts;

    public MimSchoolingFish(EntityType<? extends MimSchoolingFish> type, Level level, Supplier<Item> bucket, int schoolSize) {
        super(type, level);
        this.parts = FishParts.of(this);
        if (parts != null && !level.isClientSide()) {
            // the ids after the fish's (a client sets them when the fish arrives, setId)
            parts.setIds(getId());
        }
        this.bucket = bucket;
        this.schoolSize = schoolSize;
    }

    @Override
    public ItemStack getBucketItemStack() {
        return new ItemStack(bucket.get());
    }

    @Override
    public int getMaxSchoolSize() {
        return schoolSize;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.COD_AMBIENT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.COD_DEATH;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.COD_HURT;
    }

    @Override
    protected SoundEvent getFlopSound() {
        return SoundEvents.COD_FLOP;
    }

    @Override
    public @Nullable FishParts mimcontent$parts() {
        return parts;
    }

    @Override
    public void setId(int id) {
        super.setId(id);
        if (parts != null) {
            parts.setIds(id);
        }
    }

    @Override
    public void tick() {
        super.tick();
        if (parts != null) {
            parts.update();
        }
    }

    /** Only the chain of hit boxes is aimed at, not the fish's own square box. */
    @Override
    public boolean isPickable() {
        return parts == null && super.isPickable();
    }
}
