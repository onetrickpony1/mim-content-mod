package com.maltaminecraft.mimcontent.test;

import com.maltaminecraft.mimcontent.client.LuzzuRenderer;
import com.maltaminecraft.mimcontent.entity.LuzzuBoat;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import java.util.Locale;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.client.CameraType;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.player.PlayerModel;
import net.minecraft.client.renderer.entity.player.AvatarRenderer;
import net.minecraft.client.renderer.entity.state.AvatarRenderState;
import net.minecraft.client.renderer.entity.state.BoatRenderState;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.PlayerModelType;
import org.joml.Vector3f;

/**
 * The luzzu's oars and the rower's hands (owner, 2026-11-18: the arms must line up with the oars). The player rows a
 * luzzu held in a pen of barriers; the oars are held at points of the stroke (LuzzuRowingPhaseMixin), and at each
 * point the hands are measured against the oar handles exactly as the game draws them: the real renderers' states,
 * the real models posed by setupAnim, and the renderers' own transforms. Fails if a hand is more than 1 px off its
 * handle. Then screenshots of the stroke from the side and the 3/4 front, in two colour schemes, one oar rowing
 * alone, a full boat, and a vanilla boat for comparison (build/smoke-run/screenshots/oars-*).
 */
public class LuzzuOarsCheck implements FabricClientGameTest {
    /** The rowing time the oars are held at (read by LuzzuRowingPhaseMixin), or NaN to row normally. */
    public static volatile float heldPhase = Float.NaN;

    /** Points of the push stroke, as vanilla rowing times: hands back with the blade entering; mid push, blade
     *  deep; end of the push, hands forward; the recovery, blade lifted clear. */
    private static final float[] STROKE = {5.71F, 1.0F, 2.57F, 4.14F};
    private static final String[] STROKE_NAMES = {"a-push-start", "b-mid-push", "c-push-end", "d-recovery"};
    private static final float MAX_OFF_PX = 1.0F;

    @Override
    public void runTest(ClientGameTestContext context) {
        if (!Smoke.runs("luzzu-oars")) {
            return;
        }
        try (TestSingleplayerContext world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            TestServerContext server = world.getServer();
            server.runCommand("gamemode creative @a");
            server.runCommand("gamerule spawn_mobs false");
            server.runCommand("gamerule advance_time false");
            server.runCommand("time set 6000");
            int[] p = context.computeOnClient(mc -> new int[] {mc.player.getBlockX(), mc.player.getBlockY(), mc.player.getBlockZ()});
            int x = p[0], y = p[1] + 20, z = p[2];
            // a pool high above the land, with a pen of barriers in the middle that keeps a rowed boat in place
            fill(server, x - 12, y - 4, z - 12, x + 12, y + 8, z + 12, "minecraft:air");
            fill(server, x - 12, y - 4, z - 12, x + 12, y - 4, z + 12, "minecraft:smooth_sandstone");
            fill(server, x - 11, y - 3, z - 11, x + 11, y - 1, z + 11, "minecraft:water");
            // (one block high, so it doesn't stop the third-person camera)
            // a ring of barriers lying on the water: the sea stays whole under it
            fill(server, x - 2, y, z - 2, x + 2, y, z + 2, "minecraft:barrier");
            fill(server, x - 1, y, z - 1, x + 1, y, z + 1, "minecraft:air");
            server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %d %.1f", x + 0.5, y + 1, z + 0.5));
            world.getConnection().waitForChunksRender();
            context.runOnClient(mc -> {
                if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle();
            });
            context.waitTicks(20);

            // 1. the numbers: both oars rowing, 16 points of the stroke, three boat headings
            float worst = 0.0F;
            for (float heading : new float[] {-90.0F, 30.0F, 172.0F}) {
                board(context, server, "mimcontent:luzzu", x, y, z, heading);
                context.getInput().holdKey(o -> o.keyUp);
                context.waitTicks(10);
                for (int k = 0; k < 16; k++) {
                    heldPhase = (float) (k * Math.PI / 8);
                    context.waitTicks(1);
                    boolean both = context.computeOnClient(mc -> ((LuzzuBoat) mc.player.getVehicle()).getPaddleState(0)
                        && ((LuzzuBoat) mc.player.getVehicle()).getPaddleState(1));
                    check(both, "both oars should be rowing while forward is held");
                    float[] off = context.computeOnClient(LuzzuOarsCheck::handsOffOars);
                    log(String.format(Locale.ROOT, "heading %.0f, rowing time %.2f: left hand %.2f px off its oar's handle, right %.2f px (shoulder reach %.2f px)",
                        heading, heldPhase, off[0], off[1], off[2]));
                    worst = Math.max(worst, Math.max(off[0], off[1]));
                }
                context.getInput().releaseKey(o -> o.keyUp);
                heldPhase = Float.NaN;
                unboard(context, server);
            }
            log(String.format(Locale.ROOT, "worst hand off its oar handle over the stroke: %.2f px (limit %.1f)", worst, MAX_OFF_PX));
            check(worst <= MAX_OFF_PX, String.format(Locale.ROOT, "a hand is %.2f px off its oar handle", worst));

            // 2. the stroke in pictures: green, then red with two crew aboard (their hands on their thighs)
            String[][] schemes = {{"mimcontent:luzzu", "green"}, {"mimcontent:luzzu_red", "red"}};
            for (int s = 0; s < schemes.length; s++) {
                UUID boat = board(context, server, schemes[s][0], x, y, z, -90.0F);
                if (s == 1) {
                    crew(server, boat);
                }
                context.getInput().holdKey(o -> o.keyUp);
                context.waitTicks(10);
                for (int k = 0; k < STROKE.length; k++) {
                    heldPhase = STROKE[k];
                    String name = "oars-" + schemes[s][1] + "-" + STROKE_NAMES[k];
                    // side on: the player looks to port, so the camera behind them sees the starboard side
                    view(context, CameraType.THIRD_PERSON_BACK, -90.0F + 90.0F, 12.0F);
                    context.takeScreenshot(name + "-1-side");
                    // 3/4 front, a little above, like the owner's view: the camera in front of the rower
                    view(context, CameraType.THIRD_PERSON_FRONT, -90.0F + 35.0F, -22.0F);
                    context.takeScreenshot(name + "-2-front");
                    // low, from just off the bow, near eye height: the owner's own view
                    view(context, CameraType.THIRD_PERSON_FRONT, -90.0F + 15.0F, -4.0F);
                    context.takeScreenshot(name + "-4-bow-low");
                    // from above and behind, both oars in view
                    view(context, CameraType.THIRD_PERSON_BACK, -90.0F, 70.0F);
                    context.takeScreenshot(name + "-3-above");
                }
                context.getInput().releaseKey(o -> o.keyUp);
                heldPhase = Float.NaN;
                unboard(context, server);
            }

            // 3. one oar: turning left rows the starboard oar only; the port hand rests on the thigh, and that oar is in
            UUID turning = board(context, server, "mimcontent:luzzu_brown", x, y, z, -90.0F);
            context.getInput().holdKey(o -> o.keyLeft);
            context.waitTicks(10);
            heldPhase = STROKE[1];
            boolean[] rowing = context.computeOnClient(mc -> {
                LuzzuBoat b = (LuzzuBoat) mc.player.getVehicle();
                return new boolean[] {b.getPaddleState(0), b.getPaddleState(1)};
            });
            check(!rowing[0] && rowing[1], "turning left should row the starboard oar only: " + rowing[0] + ", " + rowing[1]);
            float[] off = context.computeOnClient(LuzzuOarsCheck::handsOffOars);
            log(String.format(Locale.ROOT, "one oar (turning): right hand %.2f px off its handle; left oar in, left hand resting", off[1]));
            check(off[1] <= MAX_OFF_PX, "turning: the rowing hand is off its oar by " + off[1]);
            float boatYaw = context.computeOnClient(mc -> mc.player.getVehicle().getYRot());
            view(context, CameraType.THIRD_PERSON_FRONT, boatYaw - 35.0F, -22.0F);
            context.takeScreenshot("oars-brown-one-oar-1-front");
            boatYaw = context.computeOnClient(mc -> mc.player.getVehicle().getYRot());
            view(context, CameraType.THIRD_PERSON_BACK, boatYaw - 90.0F, 12.0F);
            context.takeScreenshot("oars-brown-one-oar-2-side");
            view(context, CameraType.THIRD_PERSON_BACK, context.computeOnClient(mc -> mc.player.getVehicle().getYRot()), 70.0F);
            context.takeScreenshot("oars-brown-one-oar-3-above");
            context.getInput().releaseKey(o -> o.keyLeft);
            heldPhase = Float.NaN;
            unboard(context, server);

            // 4. a still boat: no oars out, both hands resting
            board(context, server, "mimcontent:luzzu", x, y, z, -90.0F);
            view(context, CameraType.THIRD_PERSON_FRONT, -90.0F + 35.0F, -22.0F);
            context.takeScreenshot("oars-green-still");
            unboard(context, server);

            // 5. vanilla for comparison: an oak boat rowed normally (its paddles and arms are vanilla's)
            board(context, server, "minecraft:oak_boat", x, y, z, -90.0F);
            context.getInput().holdKey(o -> o.keyUp);
            context.waitTicks(10);
            view(context, CameraType.THIRD_PERSON_BACK, -90.0F + 90.0F, 12.0F);
            context.takeScreenshot("oars-vanilla-oak-rowing-1-side");
            view(context, CameraType.THIRD_PERSON_BACK, -90.0F, 70.0F);
            context.takeScreenshot("oars-vanilla-oak-rowing-2-above");
            context.getInput().releaseKey(o -> o.keyUp);
            unboard(context, server);
            context.runOnClient(mc -> mc.options.setCameraType(CameraType.FIRST_PERSON));
        }
        System.out.println("[smoke] luzzu oars: all checks passed");
    }

    /**
     * How far (px) each of the rowing player's hands is from its oar's handle, as drawn: the boat and the player
     * posed by their own renderers and models, placed with the renderers' transforms. The hand is the fist's middle
     * (9 px down the arm, across its middle); the handle is the inboard part of the shaft's centre line. A hand whose
     * oar isn't rowing counts 0.
     */
    private static float[] handsOffOars(Minecraft mc) {
        Entity vehicle = mc.player.getVehicle();
        LuzzuBoat boat = (LuzzuBoat) vehicle;
        var dispatcher = mc.getEntityRenderDispatcher();
        LuzzuRenderer boatRenderer = (LuzzuRenderer) dispatcher.getRenderer(boat);
        BoatRenderState bs = boatRenderer.createRenderState(boat, 1.0F);
        var boatModel = boatRenderer.luzzuModel();
        boatModel.setupAnim(bs);
        @SuppressWarnings("unchecked")
        AvatarRenderer<net.minecraft.client.player.AbstractClientPlayer> playerRenderer =
            (AvatarRenderer<net.minecraft.client.player.AbstractClientPlayer>) dispatcher.getRenderer(mc.player);
        AvatarRenderState ps = playerRenderer.createRenderState(mc.player, 1.0F);
        PlayerModel playerModel = playerRenderer.getModel();
        playerModel.setupAnim(ps);
        float across = ps.skin.model() == PlayerModelType.SLIM ? 0.5F : 1.0F;
        float[] out = new float[3];
        out[2] = Math.max(Math.abs(playerModel.leftArm.z), Math.abs(playerModel.rightArm.z));
        for (int side = 0; side < 2; side++) {
            if (!boat.getPaddleState(side)) {
                continue;
            }
            check(bs instanceof LuzzuRenderer.LuzzuRenderState l && (side == 0 ? l.rowingLeft : l.rowingRight),
                "the boat's render state doesn't show oar " + side + " rowing");
            // the oar, as AbstractBoatRenderer.submit places the model
            PoseStack stack = new PoseStack();
            stack.translate(bs.x, bs.y, bs.z);
            stack.translate(0.0F, 0.375F, 0.0F);
            stack.rotateDegrees(Axis.YP, 180.0F - bs.yRot);
            stack.scale(-1.0F, -1.0F, 1.0F);
            stack.rotateDegrees(Axis.YP, 90.0F);
            boatModel.root().translateAndRotate(stack);
            boatModel.root().getChild(side == 0 ? "left_paddle" : "right_paddle").translateAndRotate(stack);
            Vector3f inner = stack.last().pose().transformPosition(new Vector3f(0.0F, 0.5F, -7.0F).div(16.0F));
            Vector3f pin = stack.last().pose().transformPosition(new Vector3f(0.0F, 0.5F, 0.0F).div(16.0F));
            // the arm, as LivingEntityRenderer.submit and AvatarRenderer.scale place the model
            PoseStack arm = new PoseStack();
            arm.translate(ps.x, ps.y, ps.z);
            arm.scale(ps.scale, ps.scale, ps.scale);
            arm.rotateDegrees(Axis.YP, 180.0F - ps.bodyRot);
            arm.scale(-1.0F, -1.0F, 1.0F);
            arm.scale(0.9375F, 0.9375F, 0.9375F);
            arm.translate(0.0F, -1.501F, 0.0F);
            playerModel.root().translateAndRotate(arm);
            ModelPart armPart = side == 0 ? playerModel.leftArm : playerModel.rightArm;
            armPart.translateAndRotate(arm);
            Vector3f hand = arm.last().pose().transformPosition(new Vector3f(side == 0 ? across : -across, 9.0F, 0.0F).div(16.0F));
            out[side] = distanceToSegment(hand, inner, pin) * 16.0F;
        }
        return out;
    }

    private static float distanceToSegment(Vector3f p, Vector3f a, Vector3f b) {
        Vector3f ab = new Vector3f(b).sub(a);
        float t = Math.clamp(new Vector3f(p).sub(a).dot(ab) / ab.lengthSquared(), 0.0F, 1.0F);
        return new Vector3f(a).add(ab.mul(t)).distance(p);
    }

    /** Summons the boat in the pen facing {@code heading} and seats the player at its helm; returns the boat's id. */
    private static UUID board(ClientGameTestContext context, TestServerContext server, String type, int x, int y, int z, float heading) {
        server.runCommand("kill @e[type=!minecraft:player]");
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %d %.1f %.1f 0", x + 0.5, y + 1, z + 0.5, heading));
        server.runCommand(String.format(Locale.ROOT, "summon %s %.1f %.1f %.1f {Rotation:[%.1ff,0f]}", type, x + 0.5, y - 0.4, z + 0.5, heading));
        context.waitTicks(10);
        server.runCommand(String.format("ride @p mount @e[type=%s,limit=1,sort=nearest]", type));
        context.waitFor(mc -> mc.player.getVehicle() != null);
        context.waitTicks(10);
        return server.computeOnServer(s -> s.getPlayerList().getPlayers().getFirst().getVehicle().getUUID());
    }

    private static void unboard(ClientGameTestContext context, TestServerContext server) {
        server.runCommand("ride @p dismount");
        server.runCommand("kill @e[type=!minecraft:player]");
        context.waitTicks(5);
    }

    /** Fills the two seats behind the player with mannequins facing the bow. */
    private static void crew(TestServerContext server, UUID boatId) {
        server.runOnServer(s -> {
            ServerLevel level = s.overworld();
            Entity boat = level.getEntity(boatId);
            for (int i = 0; i < 2; i++) {
                var rider = net.minecraft.world.entity.EntityTypes.MANNEQUIN.create(level, net.minecraft.world.entity.EntitySpawnReason.COMMAND);
                rider.setPos(boat.getX(), boat.getY() + 1, boat.getZ());
                rider.setYRot(boat.getYRot());
                rider.setYHeadRot(boat.getYRot());
                rider.setYBodyRot(boat.getYRot());
                level.addFreshEntity(rider);
                check(rider.startRiding(boat, true, false), "a mannequin couldn't board");
            }
        });
    }

    private static void view(ClientGameTestContext context, CameraType camera, float yaw, float pitch) {
        context.runOnClient(mc -> {
            mc.options.setCameraType(camera);
            mc.player.setYRot(yaw);
            mc.player.setYHeadRot(yaw);
            mc.player.setXRot(pitch);
        });
        context.waitTicks(4);
    }

    private static void fill(TestServerContext server, int x0, int y0, int z0, int x1, int y1, int z1, String block) {
        server.runCommand(String.format("fill %d %d %d %d %d %d %s", x0, y0, z0, x1, y1, z1, block));
    }

    private static void check(boolean ok, String message) {
        if (!ok) {
            throw new AssertionError("[smoke] luzzu oars: " + message);
        }
    }

    private static void log(String message) {
        System.out.println("[smoke] luzzu oars: " + message);
    }
}
