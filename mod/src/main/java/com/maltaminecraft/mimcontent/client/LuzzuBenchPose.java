package com.maltaminecraft.mimcontent.client;

/**
 * A player's render state knows whether its player rides a luzzu (set by AvatarRendererMixin), so the player model
 * can sit them on a thwart instead of with vanilla's legs-straight-out boat pose (HumanoidModelMixin), and knows
 * whether they are at the helm (rowing) or resting.
 */
public interface LuzzuBenchPose {
    boolean mimcontent$onLuzzu();

    void mimcontent$setOnLuzzu(boolean onLuzzu);

    /** At the helm (rowing): arms forward as vanilla's; anyone else rests their hands on their thighs. */
    boolean mimcontent$atHelm();

    void mimcontent$setAtHelm(boolean atHelm);

    /** Legs down and forward, 60 degrees from straight down (vanilla's boat pose is about 81), feet on the floorboards. */
    float LEG_X_ROT = (float) Math.toRadians(-60.0);
    /** Knees apart a little less than vanilla's, so the feet stay inside the narrow hull. */
    float LEG_Y_ROT = 0.12F;
    float LEG_Z_ROT = 0.05F;
    /** Vanilla adds this to both arms of any rider (reaching for the paddles). */
    float VANILLA_RIDING_ARM = (float) (-Math.PI / 5);
    /** A resting crew member's arms: nearly straight down, hands on the thighs, clear of the rider ahead. */
    float RESTING_ARM = -0.25F;
}
