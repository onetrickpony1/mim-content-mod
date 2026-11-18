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
 * Checks the luzzu's buffs in a real game: the config file, 3 seats (vanilla boats still 2), the fish hold (opens,
 * keeps an item through save and reload, drops it when the boat breaks), and the speeds (engine on open sea, normal
 * in a narrow channel, the way home), each measured against a vanilla oak boat driven the same way. Fails the run
 * with an AssertionError if anything is off; the numbers are printed as [smoke] lines.
 */
public class LuzzuBuffsCheck implements FabricClientGameTest {
    @Override
    public void runTest(ClientGameTestContext context) {
        if (!Smoke.runs("luzzu")) {
            return;
        }
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

            // 2. seats: 3 in a luzzu (a 4th is refused), still 2 in an oak boat
            int luzzuSeats = seatCount(context, server, "mimcontent:luzzu", x + 40, y, z);
            int oakSeats = seatCount(context, server, "minecraft:oak_boat", x + 40, y, z);
            log("seats: luzzu took " + luzzuSeats + " villagers, oak boat " + oakSeats);
            check(luzzuSeats == 3, "luzzu should seat 3, took " + luzzuSeats);
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

            // how they sit: three mannequins (drawn like players), then three villagers, seen from outside the boat;
            // then the real player at the helm with three mannequins, seen from behind
            double[] b = server.computeOnServer(s -> {
                Entity e = s.overworld().getEntity(holdBoat);
                return new double[] {e.getX(), e.getY(), e.getZ()};
            });
            context.runOnClient(mc -> {
                if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle();
            });
            String[] riders = {"mannequin", "villager"};
            for (int r = 0; r < riders.length; r++) {
                fillSeats(server, holdBoat, -1, riders[r]);
                context.waitTicks(10);
                String n = "sit-" + (r + 1) + riders[r];
                look(context, server, b[0], y, b[2] + 3.5, b[0], b[1] + 0.3, b[2], n + "-a-side");
                look(context, server, b[0] + 3.0, y, b[2] + 0.5, b[0], b[1] + 0.3, b[2], n + "-b-bow");
                look(context, server, b[0] - 2.4, y + 0.5, b[2] + 2.4, b[0], b[1] + 0.3, b[2], n + "-c-quarter");
                look(context, server, b[0], y + 4, b[2] + 0.01, b[0], b[1], b[2], n + "-d-above");
            }
            // the real player: a lone player always takes the helm (vanilla puts players first), with mannequins in
            // the other seats; third person from behind, then side on
            fillSeats(server, holdBoat, 0, "mannequin");
            context.waitTicks(10);
            context.runOnClient(mc -> {
                mc.options.setCameraType(CameraType.THIRD_PERSON_BACK);
                mc.player.setYRot(-50.0F);
                mc.player.setXRot(25.0F);
            });
            context.waitTicks(20);
            context.takeScreenshot("sit-3player-helm-a-behind");
            context.runOnClient(mc -> {
                mc.player.setYRot(0.0F);
                mc.player.setXRot(15.0F);
            });
            context.waitTicks(20);
            context.takeScreenshot("sit-3player-helm-b-side");
            fillSeats(server, holdBoat, -1, null);
            context.runOnClient(mc -> mc.options.setCameraType(CameraType.FIRST_PERSON));
            context.waitTicks(5);

            // the oars: hidden while the boat lies still, out while rowing
            server.runCommand(String.format(Locale.ROOT, "summon mimcontent:luzzu %.1f %d %.1f {Rotation:[-90f,0f]}", x + 5.5, y, z + 0.5));
            context.waitTicks(10);
            server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %d %.1f", x + 5.5, y + 1, z + 0.5));
            server.runCommand(String.format(Locale.ROOT, "ride @p mount @e[type=mimcontent:luzzu,limit=1,sort=nearest,x=%.1f,y=%d,z=%.1f]", x + 5.5, y, z + 0.5));
            context.waitFor(mc -> mc.player.getVehicle() != null);
            context.runOnClient(mc -> {
                mc.options.setCameraType(CameraType.THIRD_PERSON_BACK);
                mc.player.setYRot(0.0F);
                mc.player.setXRot(12.0F);
            });
            context.waitTicks(20);
            boolean idleOars = context.computeOnClient(mc -> ((LuzzuBoat) mc.player.getVehicle()).getPaddleState(0));
            context.takeScreenshot("sit-4-idle-oars-hidden");
            context.getInput().holdKey(o -> o.keyUp);
            context.waitTicks(25);
            boolean rowingOars = context.computeOnClient(mc -> ((LuzzuBoat) mc.player.getVehicle()).getPaddleState(0));
            context.takeScreenshot("sit-5-rowing-oars-out");
            context.getInput().releaseKey(o -> o.keyUp);
            check(!idleOars && rowingOars, "paddle state should be off when idle and on while rowing");
            context.runOnClient(mc -> mc.options.setCameraType(CameraType.FIRST_PERSON));
            server.runCommand("ride @p dismount");
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
            // the player steps well away first, so they can't pick the cod up before it is counted (on a busy
            // machine the few ticks' wait can outlast the drops' pickup delay)
            server.runCommand(String.format("tp @a %d %d %d", at[0] + 60, at[1] + 1, at[2]));
            server.runCommand("clear @a minecraft:cod");
            context.waitTicks(2);
            server.runCommand("kill @e[type=mimcontent:luzzu]");
            context.waitTicks(5);
            int dropped = server.computeOnServer(s -> s.overworld().getEntitiesOfClass(ItemEntity.class,
                    new AABB(at[0] - 5, at[1] - 10, at[2] - 20, at[0] + 50, at[1] + 10, at[2] + 20))
                .stream().filter(i -> i.getItem().is(Items.COD)).mapToInt(i -> i.getItem().getCount()).sum());
            int pickedUp = server.computeOnServer(s -> s.getPlayerList().getPlayers().getFirst().getInventory()
                .countItem(Items.COD));
            check(dropped == 7, "breaking the luzzu should drop the 7 cod, dropped " + dropped + " (player holds " + pickedUp + ")");
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

    /** Empties the luzzu and, unless riderType is null, boards it full: riderType in every seat but the player's
     *  (playerSeat -1: no player aboard). */
    private static void fillSeats(TestServerContext server, UUID boatId, int playerSeat, String riderType) {
        server.runOnServer(s -> {
            ServerLevel level = s.overworld();
            Entity boat = level.getEntity(boatId);
            ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
            for (Entity rider : java.util.List.copyOf(boat.getPassengers())) {
                rider.stopRiding();
                if (rider != player) {
                    rider.discard();
                }
            }
            if (riderType == null) {
                return;
            }
            for (int seat = 0; seat < 3; seat++) {
                if (seat == playerSeat) {
                    check(player.startRiding(boat, true, false), "player couldn't take seat " + (seat + 1));
                    continue;
                }
                net.minecraft.world.entity.LivingEntity rider = riderType.equals("villager")
                    ? net.minecraft.world.entity.EntityTypes.VILLAGER.create(level, net.minecraft.world.entity.EntitySpawnReason.COMMAND)
                    : net.minecraft.world.entity.EntityTypes.MANNEQUIN.create(level, net.minecraft.world.entity.EntitySpawnReason.COMMAND);
                if (rider instanceof net.minecraft.world.entity.Mob mob) {
                    mob.setNoAi(true);
                }
                rider.setPos(boat.getX(), boat.getY() + 1, boat.getZ());
                // facing the bow, as every seat does (a mannequin otherwise keeps looking where it was made)
                float facing = boat.getYRot();
                rider.setYRot(facing);
                rider.setYHeadRot(facing);
                rider.setYBodyRot(facing);
                level.addFreshEntity(rider);
                check(rider.startRiding(boat, true, false), riderType + " couldn't take seat " + (seat + 1));
            }
        });
    }

    /** A first-person shot from feet position (fx, fy, fz) looking at (tx, ty, tz), standing on an invisible barrier. */
    private static void look(ClientGameTestContext context, TestServerContext server,
                             double fx, double fy, double fz, double tx, double ty, double tz, String name) {
        double dx = tx - fx, dy = ty - (fy + 1.62), dz = tz - fz;
        float yaw = (float) Math.toDegrees(Math.atan2(-dx, dz));
        float pitch = (float) -Math.toDegrees(Math.atan2(dy, Math.sqrt(dx * dx + dz * dz)));
        server.runCommand(String.format("setblock %d %d %d minecraft:barrier", (int) Math.floor(fx), (int) Math.floor(fy) - 1, (int) Math.floor(fz)));
        server.runCommand(String.format(Locale.ROOT, "tp @a %.2f %.2f %.2f %.1f %.1f", fx, fy, fz, yaw, pitch));
        context.waitTicks(15);
        context.takeScreenshot(name);
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
