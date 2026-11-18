package com.maltaminecraft.mimcontent.entity.fish;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import net.minecraft.world.phys.AABB;
import org.jspecify.annotations.Nullable;

/**
 * A fish's chain of hit boxes ({@link FishPart}), sized by {@link FishShape}. The fish keeps its own box for moving
 * and bumping into things; for hitting, only the chain counts (the fish itself is not pickable), so a hit lands
 * where the fish is drawn, from snout to tail, and not in the empty corners of its square box.
 *
 * <p>Ids work like the ender dragon's: the parts take the entity ids straight after the fish's (fish id + 1, + 2,
 * ...), on the server as they are made and on the client when the fish arrives ({@link #setIds}), so a client that
 * hits a part names the same part the server knows.
 */
public final class FishParts {
    /** How far any part reaches beyond its fish's own box, in blocks (grows if a bigger fish turns up). */
    private static volatile double reach = 2.0;

    private final AbstractFish fish;
    private final FishShape shape;
    private final FishPart[] parts;

    private FishParts(AbstractFish fish, FishShape shape) {
        this.fish = fish;
        this.shape = shape;
        this.parts = new FishPart[shape.parts()];
        for (int i = 0; i < parts.length; i++) {
            parts[i] = new FishPart(fish, i);
        }
    }

    /** The chain for a fish just made (called from its constructor), or null for a fish without a shape. */
    public static @Nullable FishParts of(AbstractFish fish) {
        FishShape shape = FishShape.of(BuiltInRegistries.ENTITY_TYPE.getKey(fish.getType()).getPath());
        return shape == null ? null : new FishParts(fish, shape);
    }

    public FishPart[] parts() {
        return parts;
    }

    /** Gives the parts the ids after the fish's. */
    public void setIds(int fishId) {
        for (int i = 0; i < parts.length; i++) {
            parts[i].setId(fishId + i + 1);
        }
    }

    /** Puts every box where the fish is drawn now (called at the end of the fish's tick, on both sides). */
    public void update() {
        float scale = fish.getScale();
        boolean inWater = fish.isInWater();
        AABB own = fish.getBoundingBox();
        double far = 0.0;
        for (FishPart part : parts) {
            AABB box = shape.box(part.index, fish.position(), fish.yBodyRot, scale, inWater, fish.tickCount);
            part.setOldPosAndRot();
            part.place(box);
            far = Math.max(far, Math.max(Math.max(own.minX - box.minX, box.maxX - own.maxX),
                Math.max(Math.max(own.minZ - box.minZ, box.maxZ - own.maxZ), Math.max(own.minY - box.minY, box.maxY - own.maxY))));
        }
        if (far > reach) {
            reach = far + 0.5;
        }
    }

    /** How far to widen an entity search so it finds every fish whose parts reach into it. */
    public static double reach() {
        return reach;
    }

    /** The fish a part belongs to, or the entity itself. */
    public static Entity owner(Entity entity) {
        return entity instanceof FishPart part ? part.fish : entity;
    }

    /** Our fish that have a chain of parts. */
    public interface Holder {
        @Nullable FishParts mimcontent$parts();
    }
}
