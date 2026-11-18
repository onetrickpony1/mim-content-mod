package com.maltaminecraft.mimcontent.client;

import net.minecraft.util.Mth;
import org.joml.Matrix4f;
import org.joml.Quaternionf;
import org.joml.Vector3f;

/**
 * The luzzu's oars and the rower's hands as one motion (owner, 2026-11-18: "move the oars to match the players
 * location and arm movements").
 * <p>
 * The oars turn on thole pins on the gunwale just ahead of the helm seat, and swing with the same paddle phase
 * vanilla uses ({@code AbstractBoat#getRowingTime}, each side on its own). The rower faces the bow and pushes, as on
 * Maltese boats: hands forward with the blade deep, then back and pressed down to lift the blade clear. Each hand
 * holds a fixed point on its oar's handle ({@link #GRIP}); the player model's arms can't bend, so the shoulder
 * reaches forward and back a little along the side of the body to keep the straight arm on the handle (see
 * {@link #armPose}).
 * <p>
 * The oar pose depends only on the boat (the helm seat and the phase), so the boat model can draw it alone; the
 * rider's arms are then aimed at the grip, worked out from the real positions of the boat and the rider.
 */
public final class LuzzuOars {
    private LuzzuOars() {
    }

    /** Where the thole pins are with the helm in its usual seat (0.28 blocks forward), in the boat model's pixels:
     *  6.5 px ahead of the rower's shoulders, on the gunwale's outer edge, the shaft riding just above it. */
    public static final float THOLE_X = 11.0F;
    public static final float THOLE_Y = -8.5F;
    public static final float THOLE_Z = 8.0F;
    /** The helm seat the thole pins are placed for; another helm seat (more seats switched off) moves them with it. */
    public static final float HELM_PLACE = 0.28F;
    /** The oars' fixed slant, as the model was made. */
    public static final float TILT = (float) (Math.PI / 16);
    /** The hand's grip on the oar, in the oar's own pixels: 4.5 px inboard of the pin along the shaft's centre line.
     *  The handle ends 2.5 px further in, just out through the far side of the fist (at 2 px its end lay flush with
     *  the fist's face and flickered). */
    public static final float GRIP = -4.5F;
    private static final float SHAFT_MID = 0.5F;
    /** The stroke. Pitch: from blade deep in the water (-50 degrees) to blade well clear of it (-10). Sweep: from 20
     *  degrees forward of abeam (the blade goes in ahead of the pin, hands near the chest) to 25 aft (hands at arm's
     *  length). Vanilla's paddles run -60 to -15 and -45 to 45; these are a little smaller so the hands stay on the
     *  handles within a straight arm's reach. */
    private static final float PITCH_DEEP = (float) Math.toRadians(-50.0);
    private static final float PITCH_HIGH = (float) Math.toRadians(-10.0);
    private static final float SWEEP_AFT = (float) Math.toRadians(-25.0);
    private static final float SWEEP_FORE = (float) Math.toRadians(20.0);

    /** The fist's middle in the arm's own pixels: 9 px down the arm (it ends at 10), across the arm's centre. */
    public static final float HAND_DOWN = 9.0F;
    /** How far a shoulder may reach forward or back along the body, in px; past that the arm just aims at the grip. */
    private static final float MAX_REACH = 2.5F;

    /** An oar's pose in the boat model: rotations as {@code ModelPart} takes them and the pin's position (px). */
    public record Pose(float xRot, float yRot, float zRot, float x, float y, float z) {
    }

    /** The pose of one oar (side 0 left, 1 right) at a vanilla rowing time, with the helm at {@code helmPlace}. */
    public static Pose pose(float rowingTime, int side, float helmPlace) {
        // the same phase and curve shapes as vanilla's AbstractBoatModel.animatePaddle, with the luzzu's ranges
        float pitch = Mth.clampedLerp((Mth.sin(-rowingTime) + 1.0F) / 2.0F, PITCH_DEEP, PITCH_HIGH);
        float sweep = Mth.clampedLerp((Mth.sin(-rowingTime + 1.0F) + 1.0F) / 2.0F, SWEEP_AFT, SWEEP_FORE);
        float x = THOLE_X + 16.0F * (helmPlace - HELM_PLACE);
        return side == 0
            ? new Pose(pitch, sweep, TILT, x, THOLE_Y, THOLE_Z)
            : new Pose(pitch, (float) Math.PI - sweep, TILT, x, THOLE_Y, -THOLE_Z);
    }

    /** The grip on an oar, in the boat model's pixels. */
    public static Vector3f gripInModel(Pose pose) {
        Vector3f p = new Vector3f(0.0F, SHAFT_MID, GRIP);
        new Quaternionf().rotationZYX(pose.zRot, pose.yRot, pose.xRot).transform(p);
        return p.add(pose.x, pose.y, pose.z);
    }

    /** From the boat model's pixels to the world, relative to the boat's (drawn) position, as AbstractBoatRenderer
     *  draws it (without the shake when it is hit). */
    public static Matrix4f boatModelToWorld(float boatYRot) {
        return new Matrix4f()
            .translate(0.0F, 0.375F, 0.0F)
            .rotateY((float) Math.toRadians(180.0F - boatYRot))
            .scale(-1.0F, -1.0F, 1.0F)
            .rotateY((float) Math.toRadians(90.0F))
            .scale(1.0F / 16.0F);
    }

    /** From a player model's pixels to the world, relative to the player's (drawn) position, as
     *  LivingEntityRenderer and AvatarRenderer draw it (upright, not sleeping or gliding). */
    public static Matrix4f playerModelToWorld(float bodyRot, float scale) {
        return new Matrix4f()
            .scale(scale)
            .rotateY((float) Math.toRadians(180.0F - bodyRot))
            .scale(-1.0F, -1.0F, 1.0F)
            .scale(0.9375F)
            .translate(0.0F, -1.501F, 0.0F)
            .scale(1.0F / 16.0F);
    }

    /**
     * Aims an arm at a grip (both in the player model's pixels). The arm stays straight, so the shoulder slides
     * forward or back along the body (at most {@link #MAX_REACH}) until the grip is one arm's length away, then the
     * arm points at it. Returns {xRot, yRot, shoulder z}; zRot stays 0.
     *
     * @param handAcross the fist's middle across the arm: + for the left arm, - for the right
     */
    public static float[] armPose(Vector3f grip, float shoulderX, float shoulderY, float shoulderZ, float handAcross) {
        float reach = (float) Math.sqrt(handAcross * handAcross + HAND_DOWN * HAND_DOWN);
        float dx = grip.x - shoulderX, dy = grip.y - shoulderY, dz = grip.z - shoulderZ;
        // slide the shoulder along z by s so that |grip - shoulder| = reach, with the hand in front (-z) of it
        float q = Math.max(0.0F, reach * reach - dx * dx - dy * dy);
        float s = Mth.clamp(-dz - (float) Math.sqrt(q), -MAX_REACH, MAX_REACH);
        float z = shoulderZ - s;
        Vector3f d = new Vector3f(dx, dy, grip.z - z);
        if (d.length() > 1.0E-4F) {
            d.mul(reach / d.length());
        }
        // R = Ry(yRot) Rx(xRot) takes the fist (handAcross, HAND_DOWN, 0) onto d
        float xRot = -(float) Math.acos(Mth.clamp(d.y / HAND_DOWN, -1.0F, 1.0F));
        float srcAngle = (float) Math.atan2(handAcross, HAND_DOWN * Mth.sin(xRot));
        float dstAngle = (float) Math.atan2(d.x, d.z);
        return new float[] {xRot, Mth.wrapDegrees((dstAngle - srcAngle) * Mth.RAD_TO_DEG) * Mth.DEG_TO_RAD, z};
    }
}
