package com.maltaminecraft.mimcontent.test;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.maltaminecraft.mimcontent.MimConfig;
import com.maltaminecraft.mimcontent.entity.LuzzuBoat;
import java.nio.file.Files;
import java.util.Locale;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.client.CameraType;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.vehicle.boat.AbstractBoat;
import net.minecraft.world.inventory.ChestMenu;
import net.minecraft.world.item.Items;
import net.minecraft.world.phys.AABB;

/**
 * Checks the luzzu's buffs in a real game: the config file, 4 seats (vanilla boats still 2), the fish hold (opens,
 * keeps an item through save and reload, drops it when the boat breaks), and the speeds (engine on open sea, normal
 * in a narrow channel, the way home), each measured against a vanilla oak boat driven the same way. Fails the run
 * with an AssertionError if anything is off; the numbers are printed as [smoke] lines.
 */
public class LuzzuBuffsCheck implements FabricClientGameTest {
    @Override
    public void runTest(ClientGameTestContext context) {
        // 1. the config file, written with every switch on
        try {
            var file = MimConfig.path();
            check(Files.exists(file), "config file " + file + " was not written");
            JsonObject json = JsonParser.parseString(Files.readString(file)).getAsJsonObject();
            for (String key : new String[] {"luzzu_more_seats", "luzzu_fish_hold", "luzzu_engine", "luzzu_finds_home"}) {
                check(json.has(key) && json.get(key).getAsBoolean(), "config " + key + " missing or not true by default");
            }
            log("config file written with defaults: " + json);
        } catch (java.io.IOException e) {
            throw new AssertionError("can't read the config file", e);
        }

        TestWorldSave save;
        UUID holdBoat;
        int[] at;
        try (TestSingleplayerContext world = context.worldBuilder().create()) {
            save = world.getWorldSave();
            world.getConnection().waitForChunksRender();
            TestServerContext server = world.getServer();
            server.runCommand("gamemode creative @a");
            server.runCommand("gamerule spawn_mobs false");
            server.runCommand("gamerule advance_time false");
            server.runCommand("time set 6000");
            int[] p = context.computeOnClient(mc -> new int[] {mc.player.getBlockX(), mc.player.getBlockY(), mc.player.getBlockZ()});
            int x = p[0], y = p[1] + 30, z = p[2];
            at = new int[] {x, y, z};
            // open sea: a pool 13 wide and 4 deep, high above the land; and beside it a 3-wide, 1-deep channel
            fill(server, x - 2, y - 6, z - 13, x + 82, y + 4, z + 9, "minecraft:air");
            fill(server, x - 1, y - 5, z - 7, x + 81, y - 1, z + 7, "minecraft:stone");
            fill(server, x, y - 4, z - 6, x + 80, y - 1, z + 6, "minecraft:water");
            fill(server, x - 1, y - 2, z - 12, x + 81, y - 1, z - 8, "minecraft:stone");
            fill(server, x, y - 1, z - 11, x + 80, y - 1, z - 9, "minecraft:water");
            server.runCommand(String.format("tp @a %d %d %d", x + 3, y + 1, z));
            world.getConnection().waitForChunksRender();
            context.waitTicks(20);

            // 2. seats: 4 in a luzzu, still 2 in an oak boat
            int luzzuSeats = seatCount(context, server, "mimcontent:luzzu", x + 40, y, z);
            int oakSeats = seatCount(context, server, "minecraft:oak_boat", x + 40, y, z);
            log("seats: luzzu took " + luzzuSeats + " villagers, oak boat " + oakSeats);
            check(luzzuSeats == 4, "luzzu should seat 4, took " + luzzuSeats);
            check(oakSeats == 2, "oak boat should seat 2, took " + oakSeats);

            // 3. speeds, driven by the player holding forward for 90 ticks; distance over ticks 40 to 90
            double oakSea = drive(context, server, "minecraft:oak_boat", x + 3, y, z, "");
            double luzzuSea = drive(context, server, "mimcontent:luzzu", x + 3, y, z, "");
            double oakChannel = drive(context, server, "minecraft:oak_boat", x + 3, y, z - 10, "");
            double luzzuChannel = drive(context, server, "mimcontent:luzzu", x + 3, y, z - 10, "");
            // a harbour far ahead: the luzzu is heading home
            String home = String.format(",Harbour:[I;%d,%d,%d]", x + 400, y - 1, z);
            double luzzuHome = drive(context, server, "mimcontent:luzzu", x + 3, y, z, home);
            log(String.format(Locale.ROOT, "speed over 50 ticks (blocks): oak sea %.2f, luzzu sea %.2f (x%.3f); oak channel %.2f, luzzu channel %.2f (x%.3f); luzzu heading home %.2f (x%.3f)",
                oakSea, luzzuSea, luzzuSea / oakSea, oakChannel, luzzuChannel, luzzuChannel / oakChannel, luzzuHome, luzzuHome / oakSea));
            // vanilla's top speed on water is 0.4 blocks a tick, so 50 ticks at full speed is about 20 blocks
            check(oakSea > 17.0 && oakSea < 21.0, "oak boat speed changed: " + oakSea);
            check(Math.abs(oakChannel - oakSea) / oakSea < 0.05, "oak boat channel speed differs from open sea: " + oakChannel);
            check(luzzuSea / oakSea > 1.18 && luzzuSea / oakSea < 1.30, "luzzu open sea should be about 25% faster: x" + luzzuSea / oakSea);
            check(Math.abs(luzzuChannel / oakChannel - 1.0) < 0.04, "luzzu near shore should be vanilla speed: x" + luzzuChannel / oakChannel);
            check(luzzuHome / luzzuSea > 1.06 && luzzuHome / luzzuSea < 1.14, "heading home should add about 10%: x" + luzzuHome / luzzuSea);

            // 4. the fish hold: a seat-sized boat with a hold; sneak-use opens it, the inventory opens it while riding
            server.runCommand("kill @e[type=!minecraft:player]");
            server.runCommand(String.format(Locale.ROOT, "summon mimcontent:luzzu %.1f %d %.1f {Rotation:[-90f,0f]}", x + 20.5, y, z + 0.5));
            context.waitTicks(5);
            holdBoat = server.computeOnServer(s -> {
                ServerLevel level = s.overworld();
                LuzzuBoat boat = level.getEntitiesOfClass(LuzzuBoat.class, new AABB(x - 5, y - 10, z - 20, x + 90, y + 10, z + 20)).getFirst();
                ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                player.teleportTo(boat.getX(), boat.getY() + 1, boat.getZ());
                player.setShiftKeyDown(true);
                boolean opened = boat.interact(player, InteractionHand.MAIN_HAND, boat.position()).consumesAction()
                    && player.containerMenu instanceof ChestMenu menu && menu.getContainer() == boat;
                player.setShiftKeyDown(false);
                player.closeContainer();
                check(opened, "sneak-use did not open the hold");
                check(player.startRiding(boat), "player couldn't board");
                boat.openCustomInventoryScreen(player);
                check(player.containerMenu instanceof ChestMenu, "the hold didn't open while riding");
                player.closeContainer();
                return boat.getUUID();
            });
            server.runCommand("item replace entity @e[type=mimcontent:luzzu,limit=1] container.4 with minecraft:cod 7");
            int stored = server.computeOnServer(s -> ((LuzzuBoat) s.overworld().getEntity(holdBoat)).getItem(4).getCount());
            check(stored == 7, "hold didn't take the cod: " + stored);
            log("hold opens by sneak-use and from the seat, and stored 7 cod");

            // the ridden shot: the player at the helm and three villagers, to check the seat height
            seatVillagers(server, holdBoat, 3);
            context.runOnClient(mc -> {
                if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle();
                mc.player.setYRot(-50.0F);
                mc.player.setXRot(25.0F);
                mc.options.setCameraType(CameraType.THIRD_PERSON_BACK);
            });
            context.waitTicks(30);
            context.takeScreenshot("buffs-01-four-aboard");
            // side on: the player looks across the beam, so the third-person camera sits off the boat's side
            context.runOnClient(mc -> {
                mc.player.setYRot(0.0F);
                mc.player.setXRot(12.0F);
            });
            context.waitTicks(20);
            context.takeScreenshot("buffs-02-four-aboard-side");
            context.runOnClient(mc -> mc.options.setCameraType(CameraType.FIRST_PERSON));
            server.runCommand("ride @p dismount");
            server.runCommand("kill @e[type=minecraft:villager]");
            context.waitTicks(5);
        }

        // 5. save and reload: the cod is still in the hold, and breaking the boat drops it
        try (TestSingleplayerContext world = save.open()) {
            world.getConnection().waitForChunksRender();
            TestServerContext server = world.getServer();
            server.runCommand(String.format("tp @a %d %d %d", at[0] + 20, at[1] + 1, at[2] + 2));
            server.waitFor(s -> s.overworld().getEntity(holdBoat) != null, 400);
            context.waitTicks(5);
            int kept = server.computeOnServer(s -> {
                Entity e = s.overworld().getEntity(holdBoat);
                return e instanceof LuzzuBoat boat ? boat.getItem(4).getCount() : -1;
            });
            check(kept == 7, "hold lost its cod over save and reload: " + kept);
            server.runCommand("kill @e[type=mimcontent:luzzu]");
            context.waitTicks(5);
            int dropped = server.computeOnServer(s -> s.overworld().getEntitiesOfClass(ItemEntity.class,
                    new AABB(at[0] - 5, at[1] - 10, at[2] - 20, at[0] + 90, at[1] + 10, at[2] + 20))
                .stream().filter(i -> i.getItem().is(Items.COD)).mapToInt(i -> i.getItem().getCount()).sum());
            check(dropped == 7, "breaking the luzzu should drop the 7 cod, dropped " + dropped);
            log("hold kept 7 cod over save and reload, and dropped them when the boat broke");
        }
        System.out.println("[smoke] luzzu buffs: all checks passed");
    }

    /** Summons the boat on the pool and boards villagers one by one the normal way (no forcing); how many fit. */
    private static int seatCount(ClientGameTestContext context, TestServerContext server, String type, int x, int y, int z) {
        server.runCommand("kill @e[type=!minecraft:player]");
        server.runCommand(String.format(Locale.ROOT, "summon %s %.1f %d %.1f", type, x + 0.5, y, z + 0.5));
        context.waitTicks(5);
        return server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            AbstractBoat boat = level.getEntitiesOfClass(AbstractBoat.class, new AABB(x - 3, y - 6, z - 3, x + 4, y + 4, z + 4)).getFirst();
            int seated = 0;
            for (int i = 0; i < 5; i++) {
                Villager v = net.minecraft.world.entity.EntityTypes.VILLAGER.create(level, net.minecraft.world.entity.EntitySpawnReason.COMMAND);
                v.setNoAi(true);
                v.setPos(boat.getX(), boat.getY() + 1, boat.getZ());
                level.addFreshEntity(v);
                if (v.startRiding(boat)) {
                    seated++;
                }
            }
            return seated;
        });
    }

    /** Boards villagers into a luzzu (by UUID) until it holds n more. */
    private static void seatVillagers(TestServerContext server, UUID boatId, int n) {
        server.runOnServer(s -> {
            ServerLevel level = s.overworld();
            Entity boat = level.getEntity(boatId);
            for (int i = 0; i < n; i++) {
                Villager v = net.minecraft.world.entity.EntityTypes.VILLAGER.create(level, net.minecraft.world.entity.EntitySpawnReason.COMMAND);
                v.setNoAi(true);
                v.setPos(boat.getX(), boat.getY() + 1, boat.getZ());
                level.addFreshEntity(v);
                v.startRiding(boat);
            }
        });
    }

    /** The player boards a fresh boat heading east (+x) and holds forward for 90 ticks; blocks run in ticks 40 to 90. */
    private static double drive(ClientGameTestContext context, TestServerContext server, String type, int x, int y, int z, String nbt) {
        server.runCommand("kill @e[type=!minecraft:player]");
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %d %.1f -90 0", x + 0.5, y + 1, z + 0.5));
        server.runCommand(String.format(Locale.ROOT, "summon %s %.1f %d %.1f {Rotation:[-90f,0f]%s}", type, x + 0.5, y, z + 0.5, nbt));
        context.waitTicks(20);
        server.runCommand(String.format("ride @p mount @e[type=%s,limit=1,sort=nearest]", type));
        context.waitFor(mc -> mc.player.getVehicle() != null);
        context.waitTicks(10);
        context.getInput().holdKey(o -> o.keyUp);
        context.waitTicks(40);
        double start = context.computeOnClient(mc -> mc.player.getVehicle().getX());
        context.waitTicks(50);
        double end = context.computeOnClient(mc -> mc.player.getVehicle().getX());
        context.getInput().releaseKey(o -> o.keyUp);
        server.runCommand("ride @p dismount");
        context.waitTicks(10);
        return end - start;
    }

    private static void fill(TestServerContext server, int x0, int y0, int z0, int x1, int y1, int z1, String block) {
        server.runCommand(String.format("fill %d %d %d %d %d %d %s", x0, y0, z0, x1, y1, z1, block));
    }

    private static void check(boolean ok, String message) {
        if (!ok) {
            throw new AssertionError("[smoke] luzzu buffs: " + message);
        }
    }

    private static void log(String message) {
        System.out.println("[smoke] luzzu buffs: " + message);
    }

}
