package com.maltaminecraft.mimcontent.test;

import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;

/**
 * Close-ups of the Eye of Osiris on the luzzu's bow, for each colour scheme: from the side and the three-quarter
 * front ashore (on a plinth, so the camera is level with the eye), head-on close and from play distance, then afloat from a pier and from normal play
 * distance. Runs only when asked for by name: SMOKE_ONLY=luzzu_eye tools/run-art.sh. Called from ArtShots.
 */
final class LuzzuEyeShots {
    private LuzzuEyeShots() {
    }

    static void run(ClientGameTestContext context) {
        try (TestSingleplayerContext world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            TestServerContext server = world.getServer();
            server.runCommand("gamemode creative @a");
            server.runCommand("gamerule advance_time false");
            server.runCommand("gamerule spawn_mobs false");
            server.runCommand("time set 6000");
            int[] p = context.computeOnClient(mc -> new int[] {mc.player.getBlockX(), mc.player.getBlockY(), mc.player.getBlockZ()});
            int x = p[0], y = p[1], z = p[2] + 5;
            server.runCommand(String.format("fill %d %d %d %d %d %d minecraft:air", x - 12, y, z, x + 12, y + 8, z + 30));
            server.runCommand(String.format("fill %d %d %d %d %d %d minecraft:smooth_sandstone", x - 12, y - 3, z, x + 12, y - 1, z + 30));
            server.runCommand(String.format("fill %d %d %d %d %d %d minecraft:water", x - 11, y - 2, z + 16, x + 11, y - 1, z + 26));
            String[] schemes = {"luzzu", "luzzu_red", "luzzu_brown"};
            String[] names = {"green", "red", "brown"};
            int bz = z + 8, wz = z + 21, fz = z + 29;
            for (int i = 0; i < schemes.length; i++) {
                int bx = x + 5 - 5 * i;
                // an invisible plinth one block high, so the boat's eye is at the camera's height
                server.runCommand(String.format("fill %d %d %d %d %d %d minecraft:barrier", bx - 1, y, bz, bx + 1, y, bz));   // (3 wide: room in front for the head-on shot)
                server.runCommand(String.format(java.util.Locale.ROOT, "summon mimcontent:%s %.1f %d %.1f {Rotation:[90f,0f]}", schemes[i], bx + 0.5, y + 1, bz + 0.5));
                server.runCommand(String.format(java.util.Locale.ROOT, "summon mimcontent:%s %.1f %d %.1f {Rotation:[90f,0f]}", schemes[i], bx + 0.5, y, wz + 0.5));
                // ashore beyond the water, bow towards the camera: the head-on view from play distance
                server.runCommand(String.format(java.util.Locale.ROOT, "summon mimcontent:%s %.1f %d %.1f {Rotation:[180f,0f]}", schemes[i], x + 6.5 - 6 * i, y, fz + 0.5));
            }
            context.runOnClient(mc -> {
                if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle();
            });
            world.getConnection().waitForChunksRender();
            context.waitTicks(60);
            for (int i = 0; i < schemes.length; i++) {
                double bx = x + 5 - 5 * i + 0.5, cz = bz + 0.5, ex = bx - 1.0, ey = y + 1 + 0.65;
                look(context, server, ex, y, cz - 1.5, ex, ey, cz, "e1-" + names[i] + "-side");
                look(context, server, ex - 1.3, y, cz - 1.1, ex, ey, cz - 0.3, "e2-" + names[i] + "-34front");
                look(context, server, ex, y, cz + 1.5, ex, ey, cz, "e3-" + names[i] + "-side-far");
                look(context, server, bx - 3.0, y, cz, ex, ey, cz, "e0-" + names[i] + "-front");
                look(context, server, bx - 3.0, y, cz - 0.7, ex, ey, cz - 0.2, "e8-" + names[i] + "-front-slight");
                look(context, server, x + 6.5 - 6 * i, y, fz + 0.5 - 6.0, x + 6.5 - 6 * i, y + 0.6, fz + 0.5 - 1.0, "e7-" + names[i] + "-front-play-distance");
                look(context, server, ex - 2.0, y, wz + 0.5 - 2.0, ex, y + 0.35, wz + 0.5 - 0.3, "e4-" + names[i] + "-afloat-pier");
            }
            look(context, server, x + 0.5, y + 1, wz + 0.5 - 6.0, x + 0.5, y + 0.3, wz + 0.5, "e5-all-play-distance");
            look(context, server, x + 0.5 - 6.0, y + 1, wz + 0.5 - 4.5, x + 0.5, y + 0.3, wz + 0.5, "e6-all-play-distance-34");
            System.out.println("[smoke] luzzu eye screenshots written");
        }
    }

    /** A shot from feet position (fx, fy, fz) looking at (tx, ty, tz), standing on an invisible barrier. */
    private static void look(ClientGameTestContext context, TestServerContext server,
                             double fx, double fy, double fz, double tx, double ty, double tz, String name) {
        double dx = tx - fx, dy = ty - (fy + 1.62), dz = tz - fz;
        float yaw = (float) Math.toDegrees(Math.atan2(-dx, dz));
        float pitch = (float) -Math.toDegrees(Math.atan2(dy, Math.sqrt(dx * dx + dz * dz)));
        server.runCommand(String.format("setblock %d %d %d minecraft:barrier", (int) Math.floor(fx), (int) Math.floor(fy) - 1, (int) Math.floor(fz)));
        server.runCommand(String.format(java.util.Locale.ROOT, "tp @a %.2f %.2f %.2f %.1f %.1f", fx, fy, fz, yaw, pitch));
        context.waitTicks(15);
        context.takeScreenshot(name);
    }
}
