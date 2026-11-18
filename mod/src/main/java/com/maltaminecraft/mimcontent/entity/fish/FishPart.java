package com.maltaminecraft.mimcontent.entity.fish;

import net.minecraft.network.protocol.Packet;
import net.minecraft.network.protocol.game.ClientGamePacketListener;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerEntity;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Explosion;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.phys.AABB;
import org.jspecify.annotations.Nullable;

/**
 * One box of a fish's chain of hit boxes, like one of the ender dragon's parts: something to aim at and hit, never a
 * mob of its own. It is never added to the level (so it is never saved, ticked, sent to clients or counted for mob
 * caps); the fish moves it every tick ({@link FishParts}), and the level's entity searches find it through the fish
 * (LevelMixin). A hit, a bucket, a lead or an arrow on a part goes to the fish (PlayerMixin, ProjectileMixin); damage
 * that still reaches a part is passed on to the fish.
 */
public class FishPart extends Entity {
    public final AbstractFish fish;
    public final int index;
    private EntityDimensions size = EntityDimensions.fixed(0.1F, 0.1F);

    public FishPart(AbstractFish fish, int index) {
        super(fish.getType(), fish.level());
        this.fish = fish;
        this.index = index;
        this.noPhysics = true;
    }

    /** Moves the box to cover this bounds (the fish calls it every tick). */
    void place(AABB box) {
        float w = (float) box.getXsize(), h = (float) box.getYsize();
        if (Math.abs(w - size.width()) > 1.0E-4F || Math.abs(h - size.height()) > 1.0E-4F) {
            size = EntityDimensions.fixed(w, h);
            refreshDimensions();
        }
        setPos((box.minX + box.maxX) / 2.0, box.minY, (box.minZ + box.maxZ) / 2.0);
    }

    @Override
    public EntityDimensions getDimensions(Pose pose) {
        return size;
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder entityData) {
    }

    @Override
    protected void readAdditionalSaveData(ValueInput input) {
    }

    @Override
    protected void addAdditionalSaveData(ValueOutput output) {
    }

    @Override
    public boolean shouldBeSaved() {
        return false;
    }

    @Override
    public boolean isPickable() {
        return !fish.isRemoved();
    }

    @Override
    public @Nullable ItemStack getPickResult() {
        return fish.getPickResult();
    }

    @Override
    public boolean hurtServer(ServerLevel level, DamageSource source, float damage) {
        // an explosion already reaches the fish itself; every box would hit it again
        if (isInvulnerableToBase(source) || source.is(net.minecraft.tags.DamageTypeTags.IS_EXPLOSION)) {
            return false;
        }
        return fish.hurtServer(level, source, damage);
    }

    @Override
    public boolean ignoreExplosion(Explosion explosion) {
        return true;
    }

    @Override
    public void thunderHit(ServerLevel level, LightningBolt lightningBolt) {
    }

    @Override
    public boolean isIgnoringBlockTriggers() {
        return true;
    }

    @Override
    public boolean is(Entity other) {
        return this == other || fish == other;
    }

    @Override
    public Packet<ClientGamePacketListener> getAddEntityPacket(ServerEntity serverEntity) {
        throw new UnsupportedOperationException("a fish part is never sent on its own");
    }
}
