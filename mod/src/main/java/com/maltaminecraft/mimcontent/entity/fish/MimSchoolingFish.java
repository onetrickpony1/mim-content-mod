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

/**
 * A fish that swims in schools, exactly like vanilla's cod (followers keep near a leader), with its own school size.
 * Used for the sardina, tonn and lampuka.
 */
public class MimSchoolingFish extends AbstractSchoolingFish {
    private final Supplier<Item> bucket;
    private final int schoolSize;

    public MimSchoolingFish(EntityType<? extends MimSchoolingFish> type, Level level, Supplier<Item> bucket, int schoolSize) {
        super(type, level);
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
}
