package com.maltaminecraft.mimcontent.test;

import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;

/**
 * Art pilot screenshots: the mod's blocks beside vanilla stoves and pots, by day and by night, and the food items in
 * the hotbar beside vanilla foods. Written to build/smoke-run/screenshots; nothing is asserted, they are for review.
 */
public class ArtShots implements FabricClientGameTest {
    @Override
    public void runTest(ClientGameTestContext context) {
        try (TestSingleplayerContext world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            var server = world.getServer();
            server.runCommand("gamemode creative @a");
            server.runCommand("gamerule advance_time false");
            server.runCommand("gamerule spawn_mobs false");
            server.runCommand("time set 6000");
            int[] p = context.computeOnClient(mc -> new int[] {mc.player.getBlockX(), mc.player.getBlockY(), mc.player.getBlockZ()});
            int x = p[0], y = p[1], z = p[2] + 5;
            // a limestone floor to stand the row on, so the colours read against stone, not grass
            server.runCommand(String.format("fill %d %d %d %d %d %d minecraft:smooth_sandstone", x - 8, y - 1, z - 6, x + 8, y - 1, z + 3));
            // the row, left to right as seen from the camera (camera looks south, so +x is on the left)
            String[] row = {
                "minecraft:furnace[facing=north,lit=true]",
                "minecraft:smoker[facing=north]",
                "mimcontent:kenur[facing=north,lit=true,pot=stuffat]",
                "mimcontent:kenur[facing=north,lit=false,pot=empty]",
                "mimcontent:kenur[facing=north,lit=false,pot=none]",
                "minecraft:cauldron",
                "minecraft:decorated_pot",
            };
            for (int i = 0; i < row.length; i++) {
                server.runCommand(String.format("setblock %d %d %d %s", x + 6 - 2 * i, y, z, row[i]));
            }
            // a plank table with the two pots on it, and a vanilla flower pot for scale
            for (int i = 0; i < 3; i++) {
                server.runCommand(String.format("setblock %d %d %d minecraft:spruce_planks", x + 2 - 2 * i, y, z + 2));
            }
            server.runCommand(String.format("setblock %d %d %d mimcontent:borma", x + 2, y + 1, z + 2));
            server.runCommand(String.format("setblock %d %d %d mimcontent:borma_stuffat", x, y + 1, z + 2));
            server.runCommand(String.format("setblock %d %d %d minecraft:flower_pot", x - 2, y + 1, z + 2));
            context.runOnClient(mc -> { if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle(); });
            world.getConnection().waitForChunksRender();
            context.waitTicks(40);

            shot(context, server, x, y + 2.2, z - 7, 0, 15, "01-row-day");
            shot(context, server, x + 2, y + 1.6, z - 2.6, 0, 22, "02-kenur-close-day");
            shot(context, server, x + 3.5, y + 2.6, z - 1.5, 35, 40, "03-kenur-above-day");
            shot(context, server, x + 1, y + 2.4, z + 0.2, 0, 50, "04-pots-on-table-day");
            server.runCommand("time set 18000");
            context.waitTicks(20);
            shot(context, server, x + 2, y + 1.6, z - 2.6, 0, 22, "05-kenur-close-night");

            // the hotbar: vanilla food beside the Maltese food, and the blocks as items
            server.runCommand("time set 6000");
            String[] bar = {"minecraft:bread", "mimcontent:hobz_malti", "minecraft:cookie", "mimcontent:pastizz_irkotta",
                "minecraft:egg", "mimcontent:gbejna", "minecraft:pumpkin_pie", "mimcontent:kenur", "mimcontent:borma_stuffat"};
            for (int i = 0; i < bar.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + bar[i]);
            }
            context.runOnClient(mc -> {
                if (mc.gui.hud.isHidden()) mc.gui.hud.toggle();
                mc.options.guiScale().set(4);
            });
            server.runCommand(String.format("tp @a %d %d %d 0 -60", x, y, z - 7));
            context.waitTicks(20);
            context.takeScreenshot("06-hotbar");
            // food only: the Maltese foods between the vanilla foods they sit beside
            String[] food = {"minecraft:bread", "mimcontent:hobz_malti", "minecraft:cookie", "mimcontent:pastizz_irkotta",
                "mimcontent:pastizz_pizelli", "minecraft:pumpkin_pie", "minecraft:baked_potato", "mimcontent:gbejna", "minecraft:egg"};
            for (int i = 0; i < food.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + food[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("07-hotbar-food");
            // the pastizz family, between vanilla foods
            String[] pastizzi = {"minecraft:cookie", "mimcontent:pastizz_irkotta", "mimcontent:pastizz_pizelli",
                "mimcontent:pastizz_xema_irkotta", "mimcontent:pastizz_xema_pizelli", "minecraft:pumpkin_pie",
                "minecraft:bread", "mimcontent:hobz_malti", "minecraft:baked_potato"};
            for (int i = 0; i < pastizzi.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + pastizzi[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("08-hotbar-pastizzi");
            // the bread family
            String[] bread = {"minecraft:bread", "mimcontent:hobz_malti", "mimcontent:hobz_bizzejt", "mimcontent:ftira",
                "mimcontent:ftira_ghawdxija", "minecraft:pumpkin_pie", "minecraft:cookie", "minecraft:baked_potato", "mimcontent:gbejna"};
            for (int i = 0; i < bread.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + bread[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("09-hotbar-bread");
            // the sweets
            String[] sweets = {"minecraft:cookie", "mimcontent:imqaret", "mimcontent:kannoli", "mimcontent:qaghaq_ghasel",
                "minecraft:pumpkin_pie", "mimcontent:pastizz_irkotta", "mimcontent:ftira", "minecraft:bread", "minecraft:cake"};
            for (int i = 0; i < sweets.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + sweets[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("10-hotbar-sweets");
            System.out.println("[smoke] art screenshots written");
        }
    }

    private static void shot(ClientGameTestContext context, net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext server,
                             double x, double y, double z, float yaw, float pitch, String name) {
        server.runCommand(String.format(java.util.Locale.ROOT, "tp @a %.2f %.2f %.2f %.1f %.1f", x, y, z, yaw, pitch));
        context.waitTicks(15);
        context.takeScreenshot(name);
    }
}
