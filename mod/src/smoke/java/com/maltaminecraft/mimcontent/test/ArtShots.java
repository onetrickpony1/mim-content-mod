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
        if (Smoke.listed("luzzu_eye")) {   // the luzzu eye close-ups, only when asked for by name
            LuzzuEyeShots.run(context);
        }
        if (!Smoke.runs("art")) {
            return;
        }
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
            server.runCommand(String.format("fill %d %d %d %d %d %d minecraft:smooth_sandstone", x - 8, y - 1, z - 6, x + 8, y - 1, z + 16));
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
            // a second table: ross il-forn whole, part-eaten and nearly gone, beside a vanilla cake
            String[] dishes = {"mimcontent:ross_il_forn[eaten=0]", "mimcontent:ross_il_forn[eaten=2]",
                "mimcontent:ross_il_forn[eaten=4]", "minecraft:cake"};
            for (int i = 0; i < dishes.length; i++) {
                server.runCommand(String.format("setblock %d %d %d minecraft:spruce_planks", x + 3 - 2 * i, y, z + 5));
                server.runCommand(String.format("setblock %d %d %d %s", x + 3 - 2 * i, y + 1, z + 5, dishes[i]));
            }
            // a third table: imqarrun il-forn whole, part-eaten, nearly gone, beside a whole ross il-forn
            String[] dishes2 = {"mimcontent:imqarrun_il_forn[eaten=0]", "mimcontent:imqarrun_il_forn[eaten=2]",
                "mimcontent:imqarrun_il_forn[eaten=4]", "mimcontent:ross_il_forn[eaten=0]"};
            for (int i = 0; i < dishes2.length; i++) {
                server.runCommand(String.format("setblock %d %d %d minecraft:spruce_planks", x + 3 - 2 * i, y, z + 8));
                server.runCommand(String.format("setblock %d %d %d %s", x + 3 - 2 * i, y + 1, z + 8, dishes2[i]));
            }
            // a fourth table: timpana whole, part-eaten, nearly gone, beside a whole imqarrun il-forn
            String[] dishes3 = {"mimcontent:timpana[eaten=0]", "mimcontent:timpana[eaten=2]",
                "mimcontent:timpana[eaten=4]", "mimcontent:imqarrun_il_forn[eaten=0]"};
            for (int i = 0; i < dishes3.length; i++) {
                server.runCommand(String.format("setblock %d %d %d minecraft:spruce_planks", x + 3 - 2 * i, y, z + 11));
                server.runCommand(String.format("setblock %d %d %d %s", x + 3 - 2 * i, y + 1, z + 11, dishes3[i]));
            }
            // a fifth table: torta tal-lampuki whole, part-eaten, nearly gone, beside a whole timpana
            String[] dishes4 = {"mimcontent:torta_lampuki[eaten=0]", "mimcontent:torta_lampuki[eaten=2]",
                "mimcontent:torta_lampuki[eaten=4]", "mimcontent:timpana[eaten=0]"};
            for (int i = 0; i < dishes4.length; i++) {
                server.runCommand(String.format("setblock %d %d %d minecraft:spruce_planks", x + 3 - 2 * i, y, z + 14));
                server.runCommand(String.format("setblock %d %d %d %s", x + 3 - 2 * i, y + 1, z + 14, dishes4[i]));
            }
            context.runOnClient(mc -> { if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle(); });
            world.getConnection().waitForChunksRender();
            context.waitTicks(40);

            shot(context, server, x, y + 2.2, z - 7, 0, 15, "01-row-day");
            shot(context, server, x + 2, y + 1.6, z - 2.6, 0, 22, "02-kenur-close-day");
            shot(context, server, x + 3.5, y + 2.6, z - 1.5, 35, 40, "03-kenur-above-day");
            shot(context, server, x + 1, y + 2.4, z + 0.2, 0, 50, "04-pots-on-table-day");
            shot(context, server, x, y + 2.0, z + 2.4, 0, 30, "12-ross-il-forn-table");
            shot(context, server, x + 0.5, y + 2.6, z + 3.0, 0, 55, "12b-ross-il-forn-above");
            shot(context, server, x, y + 2.0, z + 5.4, 0, 30, "14-imqarrun-table");
            // the camera player falls between shots, so it stands on an invisible barrier for the view from above
            server.runCommand(String.format("setblock %d %d %d minecraft:barrier", x, y + 1, z + 5));
            shot(context, server, x + 0.5, y + 2.0, z + 5.5, 0, 50, "14b-imqarrun-above");
            // close and low over the whole and the part-eaten imqarrun, to see the penne on top and the cut edge
            shot(context, server, x + 2.5, y, z + 6.5, 0, 14, "14c-imqarrun-low");
            shot(context, server, x, y + 2.0, z + 8.4, 0, 30, "15-timpana-table");
            server.runCommand(String.format("setblock %d %d %d minecraft:barrier", x, y + 1, z + 8));
            shot(context, server, x + 0.5, y + 2.0, z + 8.5, 0, 50, "15b-timpana-above");
            shot(context, server, x, y + 2.0, z + 11.4, 0, 30, "16-torta-table");
            server.runCommand(String.format("setblock %d %d %d minecraft:barrier", x, y + 1, z + 11));
            shot(context, server, x + 0.5, y + 2.0, z + 11.5, 0, 50, "16b-torta-above");
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
            // the bowls
            String[] bowls = {"minecraft:bowl", "mimcontent:stuffat_fenek", "mimcontent:aljotta", "mimcontent:stuffat_qarnit",
                "minecraft:mushroom_stew", "minecraft:rabbit_stew", "minecraft:beetroot_soup", "mimcontent:bigilla", "mimcontent:soppa_tal_armla"};
            for (int i = 0; i < bowls.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + bowls[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("11-hotbar-bowls");
            // the soups side by side, so each Maltese soup reads differently from the others and from vanilla's
            String[] soups = {"mimcontent:aljotta", "mimcontent:soppa_tal_armla", "mimcontent:minestra", "mimcontent:kawlata",
                "mimcontent:stuffat_fenek", "minecraft:beetroot_soup", "minecraft:mushroom_stew", "minecraft:rabbit_stew", "minecraft:bowl"};
            for (int i = 0; i < soups.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + soups[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("11b-hotbar-soups");
            // all eight Maltese soups in one row, so each can be told from the others
            String[] soups2 = {"mimcontent:aljotta", "mimcontent:soppa_tal_armla", "mimcontent:minestra", "mimcontent:kawlata",
                "mimcontent:kusksu", "mimcontent:brodu_tat_tigieg", "mimcontent:brodu_tal_laham", "mimcontent:stuffat_fenek", "minecraft:beetroot_soup"};
            for (int i = 0; i < soups2.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + soups2[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("11c-hotbar-all-soups");
            String[] oven = {"minecraft:cake", "mimcontent:ross_il_forn", "mimcontent:imqarrun_il_forn", "mimcontent:timpana", "mimcontent:torta_lampuki", "minecraft:pumpkin_pie", "mimcontent:stuffat_fenek",
                "mimcontent:ftira_ghawdxija", "mimcontent:hobz_malti"};
            for (int i = 0; i < oven.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + oven[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("13-hotbar-oven");
            // the fish: the caught lampuka beside vanilla fish, then fried lampuka beside the cooked ones
            String[] fish = {"minecraft:cod", "minecraft:salmon", "minecraft:tropical_fish", "minecraft:pufferfish", "mimcontent:lampuka",
                "minecraft:cooked_cod", "minecraft:cooked_salmon", "mimcontent:lampuka_moqlija", "mimcontent:aljotta"};
            for (int i = 0; i < fish.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + fish[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("17-hotbar-fish");
            // the cheeses: fresh, dried and peppered ġbejniet beside vanilla foods of similar size
            String[] cheese = {"minecraft:egg", "mimcontent:gbejna", "mimcontent:gbejna_niexfa", "mimcontent:gbejna_tal_bzar",
                "minecraft:cookie", "minecraft:bread", "mimcontent:hobz_malti", "mimcontent:pastizz_irkotta", "minecraft:milk_bucket"};
            for (int i = 0; i < cheese.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + cheese[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("18-hotbar-cheese");
            // the drinks: Kinnie beside vanilla bottles and drinks
            String[] drinks = {"minecraft:glass_bottle", "minecraft:potion", "mimcontent:kinnie", "mimcontent:kinnie_can", "mimcontent:kinnie_glass",
                "minecraft:honey_bottle", "minecraft:milk_bucket", "minecraft:experience_bottle", "mimcontent:pastizz_irkotta"};
            for (int i = 0; i < drinks.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + drinks[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("19-hotbar-drinks");
            // the new bakes: qassatat and the two bread rings beside vanilla bread and the accepted pastries
            String[] bakes = {"minecraft:bread", "mimcontent:pastizz_irkotta", "mimcontent:pastizz_pizelli",
                "mimcontent:qassata_irkotta", "mimcontent:qassata_pizelli", "mimcontent:qaghaq_hmira", "mimcontent:qaghqa_appostli", "mimcontent:qaghaq_ghasel", "mimcontent:hobz_malti"};
            for (int i = 0; i < bakes.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + bakes[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("20-hotbar-bakes");
            // the dips: bigilla and the three new dips side by side with galletti, beside vanilla bowls
            String[] dips = {"mimcontent:bigilla", "mimcontent:dip_gbejna", "mimcontent:dip_tonn", "mimcontent:dip_tewm", "mimcontent:galletti",
                "mimcontent:aljotta", "minecraft:beetroot_soup", "minecraft:mushroom_stew", "minecraft:bowl"};
            for (int i = 0; i < dips.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + dips[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("21-hotbar-dips");
            // ġelat Malti beside the sweets, the dips and the soups, so its dish reads as neither
            String[] gelat = {"minecraft:snowball", "minecraft:cookie", "minecraft:pumpkin_pie", "mimcontent:gelat_malti", "mimcontent:kannoli",
                "mimcontent:imqaret", "mimcontent:bigilla", "mimcontent:aljotta", "minecraft:mushroom_stew"};
            for (int i = 0; i < gelat.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + gelat[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("22-hotbar-gelat");
            // stuffat tal-bebbux beside the other stews and soups in the same bowl, and a dip
            String[] bebbux = {"mimcontent:stuffat_bebbux", "mimcontent:stuffat_fenek", "mimcontent:stuffat_qarnit", "mimcontent:aljotta",
                "mimcontent:minestra", "mimcontent:kawlata", "mimcontent:brodu_tal_laham", "mimcontent:bigilla", "minecraft:rabbit_stew"};
            for (int i = 0; i < bebbux.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + bebbux[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("23-hotbar-bebbux");
            // fenek moqli beside vanilla rabbit and cooked meats, the fried lampuka plate and the rabbit stew
            String[] fenek = {"minecraft:rabbit", "minecraft:cooked_rabbit", "mimcontent:fenek_moqli", "minecraft:cooked_chicken", "minecraft:cooked_porkchop",
                "mimcontent:lampuka_moqlija", "mimcontent:stuffat_fenek", "minecraft:rabbit_stew", "minecraft:baked_potato"};
            for (int i = 0; i < fenek.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + fenek[i]);
            }
            context.waitTicks(10);
            context.takeScreenshot("24-hotbar-fenek");

            // the luzzu: a pool of still water past the tables, the luzzu beside a vanilla oak boat for scale
            int pz = z + 25;
            server.runCommand(String.format("fill %d %d %d %d %d %d minecraft:air", x - 9, y, z + 17, x + 9, y + 8, z + 34));
            server.runCommand(String.format("fill %d %d %d %d %d %d minecraft:smooth_sandstone", x - 9, y - 3, z + 17, x + 9, y - 1, z + 34));
            server.runCommand(String.format("fill %d %d %d %d %d %d minecraft:water", x - 7, y - 2, z + 21, x + 7, y - 1, z + 30));
            server.runCommand(String.format(java.util.Locale.ROOT, "summon mimcontent:luzzu %.1f %d %.1f {Rotation:[90f,0f]}", x - 2.0, y, pz + 0.5));
            server.runCommand(String.format(java.util.Locale.ROOT, "summon minecraft:oak_boat %.1f %d %.1f {Rotation:[90f,0f]}", x + 4.0, y, pz + 0.5));
            context.runOnClient(mc -> {
                if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle();
            });
            world.getConnection().waitForChunksRender();
            context.waitTicks(60);
            double bx = x - 2.0, bz = pz + 0.5;
            look(context, server, x + 1.0, y + 1.0, bz - 5.5, x + 1.0, y + 0.3, bz, "25-luzzu-side");
            look(context, server, bx - 3.5, y + 1.0, bz - 2.5, bx, y + 0.3, bz, "25b-luzzu-front");
            look(context, server, bx + 3.5, y + 1.0, bz - 2.5, bx, y + 0.3, bz, "25c-luzzu-back");
            look(context, server, bx - 1.0, y + 3.0, bz - 1.0, bx, y, bz, "25d-luzzu-above");
            // seated: the camera player in the luzzu, seen from behind
            server.runCommand(String.format(java.util.Locale.ROOT, "tp @a %.2f %d %.2f", bx, y + 1, bz));
            server.runCommand("ride @p mount @e[type=mimcontent:luzzu,limit=1]");
            context.waitTicks(10);
            context.runOnClient(mc -> {
                mc.player.setYRot(35.0F);
                mc.player.setXRot(20.0F);
                mc.options.setCameraType(net.minecraft.client.CameraType.THIRD_PERSON_BACK);
            });
            context.waitTicks(15);
            context.takeScreenshot("25e-luzzu-ridden");
            // from the rider's eyes, looking down into the hull toward the bow, then the stern: the corners beside
            // the floorboards, where the end sections begin, must be closed
            context.runOnClient(mc -> mc.options.setCameraType(net.minecraft.client.CameraType.FIRST_PERSON));
            for (float[] view : new float[][] {{90.0F, 55.0F}, {-90.0F, 55.0F}, {60.0F, 65.0F}, {-120.0F, 65.0F}}) {
                context.runOnClient(mc -> {
                    mc.player.setYRot(view[0]);
                    mc.player.setXRot(view[1]);
                });
                context.waitTicks(10);
                context.takeScreenshot(String.format(java.util.Locale.ROOT, "25%s-luzzu-inside-%s", view[1] < 60 ? (view[0] > 0 ? "j" : "k") : (view[0] > 0 ? "l" : "m"),
                    view[0] > 0 ? "bow" : "stern"));
            }
            server.runCommand("ride @p dismount");
            context.runOnClient(mc -> mc.options.setCameraType(net.minecraft.client.CameraType.FIRST_PERSON));
            // ashore, as luzzus are seen on the slipways: the whole hull, keel and bottom paint, beside the oak boat
            server.runCommand("kill @e[type=mimcontent:luzzu]");
            server.runCommand("kill @e[type=minecraft:oak_boat]");
            server.runCommand(String.format(java.util.Locale.ROOT, "summon mimcontent:luzzu %.1f %d %.1f {Rotation:[90f,0f]}", x - 2.0, y, z + 18.5));
            server.runCommand(String.format(java.util.Locale.ROOT, "summon minecraft:oak_boat %.1f %d %.1f {Rotation:[90f,0f]}", x + 4.0, y, z + 18.5));
            context.waitTicks(20);
            look(context, server, x + 1.0, y + 1.0, z + 23.5, x + 1.0, y + 0.4, z + 18.5, "25f-luzzu-ashore-side");
            look(context, server, bx - 3.0, y + 1.0, z + 22.5, bx, y + 0.4, z + 18.5, "25g-luzzu-ashore-bow");
            // from below at an angle, the luzzu standing on invisible barriers: any hole into the hull shows the sky
            server.runCommand("kill @e[type=mimcontent:luzzu]");
            server.runCommand(String.format("fill %d %d %d %d %d %d minecraft:barrier", x - 4, y + 3, z + 18, x, y + 3, z + 19));
            server.runCommand(String.format(java.util.Locale.ROOT, "summon mimcontent:luzzu %.1f %d %.1f {Rotation:[90f,0f]}", x - 2.0, y + 4, z + 18.5));
            context.waitTicks(20);
            look(context, server, x + 1.5, y, z + 22.0, x - 2.0, y + 4.2, z + 18.5, "25n-luzzu-below");
            look(context, server, x - 5.5, y, z + 21.5, x - 2.0, y + 4.2, z + 18.5, "25o-luzzu-below-bow");
            server.runCommand(String.format("fill %d %d %d %d %d %d minecraft:air", x - 4, y + 3, z + 18, x, y + 3, z + 19));
            // the colour schemes side by side on the water: green, red, brown
            server.runCommand("kill @e[type=mimcontent:luzzu]");
            String[] schemes = {"mimcontent:luzzu", "mimcontent:luzzu_red", "mimcontent:luzzu_brown"};
            for (int i = 0; i < schemes.length; i++) {
                server.runCommand(String.format(java.util.Locale.ROOT, "summon %s %.1f %d %.1f {Rotation:[90f,0f]}", schemes[i], x - 1.0, y, z + 22.5 + 3 * i));
            }
            context.waitTicks(30);
            look(context, server, x + 5.0, y + 1.5, z + 20.5, x - 1.0, y + 0.3, z + 25.5, "25h-luzzu-schemes");
            look(context, server, x - 6.5, y + 1.0, z + 25.5, x - 1.0, y + 0.5, z + 25.5, "25i-luzzu-schemes-bow");

            // the luzzu items beside the vanilla boats
            String[] boats = {"minecraft:oak_boat", "minecraft:spruce_boat", "mimcontent:luzzu", "mimcontent:luzzu_red", "mimcontent:luzzu_brown",
                "minecraft:cherry_boat", "minecraft:mangrove_boat", "minecraft:bamboo_raft", "minecraft:dark_oak_boat"};
            for (int i = 0; i < boats.length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + boats[i]);
            }
            context.runOnClient(mc -> {
                if (mc.gui.hud.isHidden()) mc.gui.hud.toggle();
            });
            server.runCommand(String.format("tp @a %d %d %d 0 -60", x, y, z - 7));
            context.waitTicks(20);
            context.takeScreenshot("26-hotbar-luzzu");
            System.out.println("[smoke] art screenshots written");
        }
    }

    /** A shot from feet position (fx, fy, fz) looking at (tx, ty, tz), standing on an invisible barrier (kept out of
     *  the water, so the water shows no hole round it). */
    private static void look(ClientGameTestContext context, net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext server,
                             double fx, double fy, double fz, double tx, double ty, double tz, String name) {
        double dx = tx - fx, dy = ty - (fy + 1.62), dz = tz - fz;
        float yaw = (float) Math.toDegrees(Math.atan2(-dx, dz));
        float pitch = (float) -Math.toDegrees(Math.atan2(dy, Math.sqrt(dx * dx + dz * dz)));
        server.runCommand(String.format("setblock %d %d %d minecraft:barrier", (int) Math.floor(fx), (int) Math.floor(fy) - 1, (int) Math.floor(fz)));
        shot(context, server, fx, fy, fz, yaw, pitch, name);
    }

    private static void shot(ClientGameTestContext context, net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext server,
                             double x, double y, double z, float yaw, float pitch, String name) {
        server.runCommand(String.format(java.util.Locale.ROOT, "tp @a %.2f %.2f %.2f %.1f %.1f", x, y, z, yaw, pitch));
        context.waitTicks(15);
        context.takeScreenshot(name);
    }
}
