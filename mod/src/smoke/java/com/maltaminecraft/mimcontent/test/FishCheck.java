package com.maltaminecraft.mimcontent.test;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.maltaminecraft.mimcontent.MimConfig;
import com.maltaminecraft.mimcontent.MimFishes;
import com.maltaminecraft.mimcontent.entity.fish.TonnFish;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.MobBucketItem;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;

/**
 * Checks the tier A fish in a real game: the config switch; each fish lives and swims in water; killing it drops its
 * item (the lampuka fried if it dies burning; the żiemel drops nothing); a water bucket catches it into its own bucket,
 * emptying the bucket lets it out again, and the spawn egg spawns it. Then screenshots for the art review (fish-*):
 * all seven in a glass tank beside vanilla cod and salmon, some flopping on land, and the items, buckets and eggs in
 * the hotbar. Fails the run with an AssertionError if anything is off.
 */
public class FishCheck implements FabricClientGameTest {
    @Override
    public void runTest(ClientGameTestContext context) {
        if (!Smoke.runs("fish")) {
            return;
        }
        // 1. the config switch, on by default
        try {
            JsonObject json = JsonParser.parseString(Files.readString(MimConfig.path())).getAsJsonObject();
            check(json.has("fish_in_vanilla_oceans") && json.get("fish_in_vanilla_oceans").getAsBoolean(),
                "config fish_in_vanilla_oceans missing or not true by default");
            log("config has fish_in_vanilla_oceans = true");
        } catch (java.io.IOException e) {
            throw new AssertionError("can't read the config file", e);
        }

        try (TestSingleplayerContext world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            TestServerContext server = world.getServer();
            server.runCommand("gamemode creative @a");
            server.runCommand("gamerule spawn_mobs false");
            server.runCommand("gamerule advance_time false");
            server.runCommand("time set 6000");
            int[] p = context.computeOnClient(mc -> new int[] {mc.player.getBlockX(), mc.player.getBlockY(), mc.player.getBlockZ()});
            int x = p[0], y = p[1] + 30, z = p[2];
            // a pool 15 x 15, 5 deep, high above the land, with a stone rim to stand on
            fill(server, x - 10, y - 8, z - 10, x + 10, y + 4, z + 10, "minecraft:air");
            fill(server, x - 8, y - 6, z - 8, x + 8, y, z + 8, "minecraft:stone");
            fill(server, x - 7, y - 5, z - 7, x + 7, y - 1, z + 7, "minecraft:water");
            server.runCommand(String.format("tp @a %d %d %d", x - 8, y + 1, z - 8));
            world.getConnection().waitForChunksRender();
            context.waitTicks(10);
            AABB pool = new AABB(x - 9, y - 7, z - 9, x + 10, y + 5, z + 10);

            // 2. each fish lives and swims: all seven at once, positions sampled for 200 ticks
            List<MimFishes.Fish> all = MimFishes.ALL;
            check(all.size() == 7, "expected 7 fish, found " + all.size());
            for (int i = 0; i < all.size(); i++) {
                server.runCommand(String.format(Locale.ROOT, "summon mimcontent:%s %.1f %d %.1f", all.get(i).id(), x - 5.5 + 2 * i, y - 3, z + 0.5));
            }
            context.waitTicks(2);
            Map<String, Vec3> start = positions(server, pool);
            Map<String, Double> moved = new HashMap<>();
            for (int t = 0; t < 20; t++) {
                context.waitTicks(10);
                positions(server, pool).forEach((id, pos) -> moved.merge(id, pos.distanceTo(start.getOrDefault(id, pos)), Math::max));
            }
            for (MimFishes.Fish f : all) {
                String state = server.computeOnServer(s -> {
                    List<? extends AbstractFish> found = s.overworld().getEntities(f.type(), pool, e -> true);
                    if (found.size() != 1) {
                        return "found " + found.size();
                    }
                    AbstractFish fish = found.getFirst();
                    return String.format(Locale.ROOT, "%s alive=%s inWater=%s health=%.0f size=%.2fx%.2f",
                        fish.isAlive() ? "ok" : "dead", fish.isAlive(), fish.isInWater(), fish.getHealth(), fish.getBbWidth(), fish.getBbHeight());
                });
                log(String.format(Locale.ROOT, "%s: %s, swam up to %.2f blocks", f.id(), state, moved.getOrDefault(f.id(), 0.0)));
                check(state.startsWith("ok") && state.contains("inWater=true"), f.id() + " not alive in water: " + state);
                check(moved.getOrDefault(f.id(), 0.0) > 0.5, f.id() + " did not swim");
            }

            // 3. drops: kill each one in turn, count what lands
            for (MimFishes.Fish f : all) {
                server.runCommand("kill @e[type=item]");
                server.runCommand("kill @e[type=mimcontent:" + f.id() + "]");
                context.waitTicks(5);
                String drops = drops(server, pool);
                String expected = f.item() == null ? "" : BuiltInRegistries.ITEM.getKey(f.item()) + " x1";
                log(f.id() + " dropped [" + drops + "]");
                check(drops.equals(expected), f.id() + " should drop [" + expected + "], dropped [" + drops + "]");
            }
            check(MimFishes.LAMPUKA.item() == com.maltaminecraft.mimcontent.MimContent.LAMPUKA, "the lampuka should drop the existing lampuka item");
            // a lampuka that dies burning (on the rim, out of the water) drops the fried one
            server.runCommand("kill @e[type=item]");
            server.runOnServer(s -> {
                ServerLevel level = s.overworld();
                AbstractFish fish = (AbstractFish) MimFishes.LAMPUKA.type().create(level, EntitySpawnReason.COMMAND);
                fish.setPos(x + 7.5, y + 1, z - 7.5);
                level.addFreshEntity(fish);
                fish.igniteForSeconds(5.0F);
                fish.kill(level);
            });
            context.waitTicks(5);
            String fried = drops(server, pool);
            log("burning lampuka dropped [" + fried + "]");
            check(fried.equals("mimcontent:lampuka_moqlija x1"), "a burning lampuka should drop lampuka_moqlija, dropped [" + fried + "]");
            server.runCommand("kill @e[type=item]");

            // 4. buckets, in survival (creative keeps the water bucket): catch, let out; then the spawn egg
            server.runCommand("gamemode survival @a");
            server.runCommand("effect give @a minecraft:resistance 60 4 true");
            for (MimFishes.Fish f : all) {
                server.runCommand(String.format(Locale.ROOT, "summon mimcontent:%s %.1f %d %.1f {NoAI:1b}", f.id(), x + 0.5, y - 3, z + 0.5));
                context.waitTicks(2);
                String result = server.computeOnServer(s -> {
                    ServerLevel level = s.overworld();
                    ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                    AbstractFish fish = level.getEntities(f.type(), pool, e -> true).getFirst();
                    player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.WATER_BUCKET));
                    fish.interact(player, InteractionHand.MAIN_HAND, fish.position());
                    ItemStack held = player.getItemInHand(InteractionHand.MAIN_HAND);
                    if (!held.is(f.bucket())) {
                        return "bucketing gave " + BuiltInRegistries.ITEM.getKey(held.getItem());
                    }
                    if (fish.isAlive() && !fish.isRemoved()) {
                        return "the fish stayed in the water after bucketing";
                    }
                    // let it out again
                    BlockPos out = BlockPos.containing(x + 3.5, y - 3, z + 3.5);
                    ((MobBucketItem) held.getItem()).checkExtraContent(player, level, held, out);
                    List<? extends AbstractFish> back = level.getEntities(f.type(), new AABB(out).inflate(1.5), e -> true);
                    if (back.size() != 1 || !back.getFirst().fromBucket()) {
                        return "emptying the bucket gave " + back.size() + " fish";
                    }
                    back.getFirst().discard();
                    // the spawn egg, used on the pool floor
                    player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(f.spawnEgg()));
                    BlockPos floor = BlockPos.containing(x - 3.5, y - 6, z - 3.5);
                    player.getItemInHand(InteractionHand.MAIN_HAND).useOn(new UseOnContext(player, InteractionHand.MAIN_HAND,
                        new BlockHitResult(Vec3.atCenterOf(floor).add(0, 0.5, 0), Direction.UP, floor, false)));
                    List<? extends AbstractFish> hatched = level.getEntities(f.type(), new AABB(floor.above()).inflate(1.5), e -> true);
                    if (hatched.size() != 1) {
                        return "the spawn egg made " + hatched.size() + " fish";
                    }
                    hatched.getFirst().discard();
                    return "ok";
                });
                log(f.id() + ": bucket and egg " + result);
                check(result.equals("ok"), f.id() + ": " + result);
            }
            server.runCommand("gamemode creative @a");
            server.runCommand("kill @e[type=!minecraft:player]");
            log("all checks passed");

            shots(context, server, world, p[0], p[1], p[2]);
        }
        tonnSizes(context);
        System.out.println("[smoke] fish: all checks passed, screenshots written");
    }

    /** The art review scene, on the ground near spawn: a long glass tank seen side on, fish on land, the hotbar. */
    private static void shots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int gx, int gy, int gz) {
        int x = gx, y = gy, z = gz + 20;
        // a sandstone floor, a glass tank 19 long (x), 5 deep (z), 5 high, filled with water
        fill(server, x - 12, y, z - 4, x + 12, y + 8, z + 10, "minecraft:air");
        fill(server, x - 12, y - 1, z - 4, x + 12, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 10, y, z + 4, x + 10, y + 5, z + 9, "minecraft:glass");
        fill(server, x - 9, y, z + 5, x + 9, y + 4, z + 8, "minecraft:water");
        // left to right as seen from the camera (looking south, +x is on the left): cod, salmon, then the seven
        String[] row = {"minecraft:cod", "minecraft:salmon", "mimcontent:sardina", "mimcontent:awrata", "mimcontent:lampuka",
            "mimcontent:cerna", "mimcontent:tonn", "mimcontent:murina", "mimcontent:ziemel"};
        for (int i = 0; i < row.length; i++) {
            server.runCommand(String.format(Locale.ROOT, "summon %s %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
                row[i], x + 8.0 - 2.0 * i, y + 1.6, z + 6.5));
        }
        // three out of the water, flopping on the floor in front of the tank
        String[] land = {"mimcontent:sardina", "mimcontent:cerna", "mimcontent:tonn", "mimcontent:ziemel"};
        for (int i = 0; i < land.length; i++) {
            server.runCommand(String.format(Locale.ROOT, "summon %s %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
                land[i], x + 3.0 - 2.0 * i, y, z + 1.5));
        }
        context.runOnClient(mc -> {
            if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle();
        });
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        look(context, server, x, y + 0.5, z - 3.5, x, y + 1.6, z + 6.5, "fish-01-tank-all");
        look(context, server, x + 6.0, y, z + 1.5, x + 6.0, y + 1.6, z + 6.5, "fish-02-tank-cod-salmon-sardina");
        look(context, server, x + 1.0, y, z + 1.5, x + 1.0, y + 1.6, z + 6.5, "fish-03-tank-awrata-lampuka-cerna");
        look(context, server, x - 5.0, y, z + 1.5, x - 5.0, y + 1.6, z + 6.5, "fish-04-tank-tonn-murina-ziemel");
        look(context, server, x + 2.0, y + 2.5, z + 3.5, x, y + 1.6, z + 6.5, "fish-05-tank-above");
        look(context, server, x, y + 0.5, z - 2.5, x, y, z + 1.5, "fish-06-on-land");
        lampukaShots(context, server, world, x + 30, y, z);
        tonnShots(context, server, world, x - 30, y, z);
        sardinaShots(context, server, world, x + 30, y, z + 25);
        cernaShots(context, server, world, x - 30, y, z + 50);
        ziemelShots(context, server, world, x + 30, y, z + 75);

        // the hotbar: the caught fish beside vanilla's, then the buckets, then the spawn eggs
        String[][] bars = {
            {"minecraft:cod", "minecraft:salmon", "mimcontent:lampuka", "mimcontent:tonn", "mimcontent:sardina", "mimcontent:cerna",
                "mimcontent:awrata", "mimcontent:murina", "minecraft:tropical_fish"},
            {"minecraft:cod_bucket", "mimcontent:lampuka_bucket", "mimcontent:tonn_bucket", "mimcontent:sardina_bucket", "mimcontent:cerna_bucket",
                "mimcontent:awrata_bucket", "mimcontent:murina_bucket", "mimcontent:ziemel_bucket", "minecraft:salmon_bucket"},
            {"minecraft:cod_spawn_egg", "mimcontent:lampuka_spawn_egg", "mimcontent:tonn_spawn_egg", "mimcontent:sardina_spawn_egg",
                "mimcontent:cerna_spawn_egg", "mimcontent:awrata_spawn_egg", "mimcontent:murina_spawn_egg", "mimcontent:ziemel_spawn_egg",
                "minecraft:salmon_spawn_egg"},
        };
        String[] names = {"fish-07-hotbar-items", "fish-08-hotbar-buckets", "fish-09-hotbar-eggs"};
        context.runOnClient(mc -> {
            if (mc.gui.hud.isHidden()) mc.gui.hud.toggle();
            mc.options.guiScale().set(4);
        });
        server.runCommand(String.format("tp @a %d %d %d 0 -60", x, y, z - 3));
        for (int b = 0; b < bars.length; b++) {
            for (int i = 0; i < bars[b].length; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + bars[b][i]);
            }
            context.waitTicks(15);
            context.takeScreenshot(names[b]);
        }
    }

    /** The lampuka model's own review: one fish alone in a small tank, close up from several sides, and one on land. */
    private static void lampukaShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 7, y, z - 6, x + 7, y + 12, z + 10, "minecraft:air");
        fill(server, x - 7, y - 1, z - 6, x + 7, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 4, y, z + 4, x + 4, y + 4, z + 9, "minecraft:glass");
        fill(server, x - 3, y, z + 5, x + 3, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:lampuka %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1.5, z + 5.6));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:lampuka %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        look(context, server, x + 0.5, y, z + 3.3, x + 0.5, y + 1.5, z + 5.6, "fish-lampuka-side");
        look(context, server, x - 1.8, y + 0.6, z + 2.2, x + 0.5, y + 1.5, z + 5.6, "fish-lampuka-three-quarter");
        look(context, server, x + 0.5, y + 5.0, z + 3.6, x + 0.5, y + 1.5, z + 5.6, "fish-lampuka-top");
        look(context, server, x + 0.5, y, z - 2.0, x + 0.5, y + 0.2, z + 0.5, "fish-lampuka-on-land");
    }

    /** The tonn model's own review: one tonn alone in a tank, close up from several sides, and one on land. */
    private static void tonnShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 8, y, z - 8, x + 8, y + 12, z + 11, "minecraft:air");
        fill(server, x - 8, y - 1, z - 8, x + 8, y - 1, z + 11, "minecraft:smooth_sandstone");
        fill(server, x - 5, y, z + 4, x + 5, y + 4, z + 10, "minecraft:glass");
        fill(server, x - 4, y + 1, z + 5, x + 4, y + 4, z + 9, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:tonn %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 2.0, z + 6.0));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:tonn %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z - 2.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        look(context, server, x + 0.5, y + 0.6, z + 3.4, x + 0.5, y + 2.3, z + 6.0, "fish-tonn-side");
        look(context, server, x - 2.0, y + 1.4, z + 3.2, x + 0.5, y + 2.3, z + 6.0, "fish-tonn-three-quarter");
        look(context, server, x + 0.5, y + 6.2, z + 5.6, x + 0.5, y + 2.3, z + 6.0, "fish-tonn-top");
        look(context, server, x + 0.5, y, z - 6.4, x + 0.5, y + 0.3, z - 2.5, "fish-tonn-on-land");
        look(context, server, x - 2.5, y + 0.8, z - 5.6, x + 0.5, y + 0.3, z - 2.5, "fish-tonn-on-land-three-quarter");
    }

    /**
     * The tonn's mixed sizes (owner 2026-11-18): in a world of its own, three schools spawned the natural way, three
     * from the spawn egg and three by /summon. Each must be 2 to 4 blocks long, the sizes must vary, a school must stay
     * near its leader's size, hitbox, health and the client's scale must match the length, and the length must survive a
     * bucket and a save and reload. Then the review shot fish-tonn-sizes: a small, a medium and a large tonn in a tank,
     * with the player standing beside it for scale.
     */
    private static void tonnSizes(ClientGameTestContext context) {
        TestWorldSave save;
        Map<UUID, Float> lengths = new HashMap<>();
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
            at = p;
            fill(server, x - 12, y - 9, z - 12, x + 12, y + 4, z + 12, "minecraft:air");
            fill(server, x - 11, y - 8, z - 11, x + 11, y, z + 11, "minecraft:stone");
            fill(server, x - 10, y - 7, z - 10, x + 10, y - 1, z + 10, "minecraft:water");
            server.runCommand(String.format("tp @a %d %d %d", x - 11, y + 1, z - 11));
            world.getConnection().waitForChunksRender();
            context.waitTicks(10);
            AABB pool = new AABB(x - 12, y - 9, z - 12, x + 12, y + 5, z + 12);

            // three schools of five, spawned as the natural spawner does (one spawn group per school)
            List<List<UUID>> schools = server.computeOnServer(s -> {
                ServerLevel level = s.overworld();
                List<List<UUID>> out = new ArrayList<>();
                for (int school = 0; school < 3; school++) {
                    List<UUID> ids = new ArrayList<>();
                    SpawnGroupData group = null;
                    for (int i = 0; i < 5; i++) {
                        BlockPos pos = BlockPos.containing(x - 6 + 6 * school, y - 4, z - 6 + 3 * i);
                        TonnFish fish = (TonnFish) MimFishes.TONN.type().create(level, EntitySpawnReason.NATURAL);
                        fish.snapTo(pos.getX() + 0.5, pos.getY(), pos.getZ() + 0.5, 0.0F, 0.0F);
                        group = fish.finalizeSpawn(level, level.getCurrentDifficultyAt(pos), EntitySpawnReason.NATURAL, group);
                        fish.setPersistenceRequired();
                        level.addFreshEntity(fish);
                        ids.add(fish.getUUID());
                    }
                    out.add(ids);
                }
                return out;
            });
            // three from the spawn egg and three by /summon
            for (int i = 0; i < 3; i++) {
                int fx = x + 6, fz = z - 6 + 6 * i;
                server.runOnServer(s -> {
                    ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                    player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(MimFishes.TONN.spawnEgg()));
                    BlockPos floor = BlockPos.containing(fx, y - 8, fz);
                    player.getItemInHand(InteractionHand.MAIN_HAND).useOn(new UseOnContext(player, InteractionHand.MAIN_HAND,
                        new BlockHitResult(Vec3.atCenterOf(floor).add(0, 0.5, 0), Direction.UP, floor, false)));
                });
                server.runCommand(String.format(Locale.ROOT, "summon mimcontent:tonn %.1f %d %.1f", x - 8.5, y - 3, z - 6.0 + 6 * i));
            }
            context.waitTicks(2);
            server.runOnServer(s -> s.overworld().getEntities(MimFishes.TONN.type(), pool, e -> true).forEach(e -> e.setPersistenceRequired()));

            Map<UUID, Float> found = tonnLengths(server, pool);
            check(found.size() == 21, "expected 21 tonn, found " + found.size());
            float min = Float.MAX_VALUE, max = 0;
            for (float l : found.values()) {
                check(l >= TonnFish.MIN_LENGTH && l <= TonnFish.MAX_LENGTH, "a tonn is " + l + " blocks long, outside 2 to 4");
                min = Math.min(min, l);
                max = Math.max(max, l);
            }
            log(String.format(Locale.ROOT, "tonn lengths: 21 fish from %.2f to %.2f blocks", min, max));
            check(max - min >= 0.5F, String.format(Locale.ROOT, "tonn sizes hardly vary (%.2f to %.2f)", min, max));
            for (List<UUID> school : schools) {
                float leader = found.get(school.getFirst());
                StringBuilder line = new StringBuilder(String.format(Locale.ROOT, "school: leader %.2f, others", leader));
                for (UUID id : school.subList(1, school.size())) {
                    float l = found.get(id);
                    line.append(String.format(Locale.ROOT, " %.2f", l));
                    boolean clamped = l == TonnFish.MIN_LENGTH || l == TonnFish.MAX_LENGTH;
                    check(clamped || Math.abs(l / leader - 1.0F) <= 0.101F, "a school member is " + l + " beside a leader of " + leader);
                }
                log(line.toString());
            }
            // hitbox and health on the server, scale and hitbox on the client, all from the length
            String onServer = server.computeOnServer(s -> {
                for (TonnFish fish : tonns(s.overworld(), pool)) {
                    String bad = sizeProblem(fish, fish.getLength());
                    if (bad != null) {
                        return bad;
                    }
                    if (fish.getMaxHealth() != Math.round(fish.getLength() * TonnFish.HEALTH_PER_BLOCK) || fish.getHealth() != fish.getMaxHealth()) {
                        return String.format(Locale.ROOT, "length %.2f has health %.1f of %.1f", fish.getLength(), fish.getHealth(), fish.getMaxHealth());
                    }
                }
                return "ok";
            });
            check(onServer.equals("ok"), "server: " + onServer);
            context.waitTicks(10);
            String client = context.computeOnClient(mc -> {
                int seen = 0;
                for (Entity e : mc.level.entitiesForRendering()) {
                    if (e.getType() == MimFishes.TONN.type() && found.containsKey(e.getUUID())) {
                        String bad = sizeProblem((AbstractFish) e, found.get(e.getUUID()));
                        if (bad != null) {
                            return bad;
                        }
                        seen++;
                    }
                }
                return seen == found.size() ? "ok" : "the client sees " + seen + " of " + found.size() + " tonn";
            });
            log("hitbox, health and client scale follow the length: " + client);
            check(client.equals("ok"), "client: " + client);

            // the bucket keeps the size: catch the largest, let it out, same length
            UUID biggest = found.entrySet().stream().max(Map.Entry.comparingByValue()).orElseThrow().getKey();
            server.runCommand("gamemode survival @a");
            String bucket = server.computeOnServer(s -> {
                ServerLevel level = s.overworld();
                ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                TonnFish fish = (TonnFish) level.getEntity(biggest);
                float before = fish.getLength();
                player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.WATER_BUCKET));
                fish.interact(player, InteractionHand.MAIN_HAND, fish.position());
                ItemStack held = player.getItemInHand(InteractionHand.MAIN_HAND);
                if (!held.is(MimFishes.TONN.bucket())) {
                    return "bucketing gave " + BuiltInRegistries.ITEM.getKey(held.getItem());
                }
                float stored = held.getOrDefault(DataComponents.BUCKET_ENTITY_DATA, CustomData.EMPTY).copyTag().getFloatOr("Length", -1.0F);
                BlockPos out = BlockPos.containing(x - 8.5, y - 4, z + 8.5);
                ((MobBucketItem) held.getItem()).checkExtraContent(player, level, held, out);
                List<TonnFish> back = tonns(level, new AABB(out).inflate(3.0)).stream().filter(TonnFish::fromBucket).toList();
                if (back.size() != 1) {
                    return "emptying the bucket gave " + back.size() + " tonn";
                }
                TonnFish released = back.getFirst();
                String bad = sizeProblem(released, before);
                return String.format(Locale.ROOT, "caught %.2f, bucket says %.2f, let out %.2f (health %.1f of %.1f)%s",
                    before, stored, released.getLength(), released.getHealth(), released.getMaxHealth(), bad == null ? "" : ": " + bad)
                    + (stored == before && released.getLength() == before && bad == null ? " ok" : " WRONG") + "|" + released.getUUID() + "|" + biggest;
            });
            String[] parts = bucket.split("\\|");
            log("bucket: " + parts[0]);
            check(parts[0].endsWith(" ok"), "the bucket lost the size: " + parts[0]);
            server.runCommand("gamemode creative @a");
            lengths.putAll(tonnLengths(server, pool));
            check(lengths.size() == 21, "after the bucket, expected 21 tonn, found " + lengths.size());
        }

        // save and reload: every tonn comes back the same length
        try (TestSingleplayerContext world = save.open()) {
            world.getConnection().waitForChunksRender();
            context.waitTicks(40);
            TestServerContext server = world.getServer();
            int x = at[0], y = at[1] + 30, z = at[2];
            AABB pool = new AABB(x - 12, y - 9, z - 12, x + 12, y + 5, z + 12);
            Map<UUID, Float> reloaded = tonnLengths(server, pool);
            int same = 0;
            for (Map.Entry<UUID, Float> e : lengths.entrySet()) {
                Float now = reloaded.get(e.getKey());
                check(now != null, "a tonn went missing after reload");
                check(now.floatValue() == e.getValue().floatValue(), "a tonn was " + e.getValue() + " long, after reload " + now);
                same++;
            }
            String sizes = server.computeOnServer(s -> {
                for (TonnFish fish : tonns(s.overworld(), pool)) {
                    String bad = sizeProblem(fish, fish.getLength());
                    if (bad != null) {
                        return bad;
                    }
                }
                return "ok";
            });
            check(sizes.equals("ok"), "after reload: " + sizes);
            log("save and reload: all " + same + " tonn kept their length and hitbox");
            server.runCommand("kill @e[type=mimcontent:tonn]");
            tonnSizeShot(context, server, world, at[0], at[1], at[2]);
        }
    }

    /**
     * The review shot: a small (2), medium (3) and large (4 blocks) tonn side by side in a tank, and a player standing
     * beside it for scale. The tank's front wall is barrier (invisible), so no glass frames cross the fish. The figure
     * is a client-side player (the game never draws the player you look through).
     */
    private static void tonnSizeShot(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        int fz = z + 6;
        fill(server, x - 14, y, z - 10, x + 12, y + 10, z + 10, "minecraft:air");
        fill(server, x - 14, y - 1, z - 10, x + 12, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 10, y, fz - 2, x + 4, y + 3, fz + 2, "minecraft:glass");
        fill(server, x - 10, y, fz - 2, x + 4, y + 3, fz - 2, "minecraft:barrier");
        fill(server, x - 9, y, fz - 1, x + 3, y + 3, fz + 1, "minecraft:water");
        // left to right as the camera (looking south) sees them: small, medium, large (+x is on the camera's left)
        float[] sizes = {2.0F, 3.0F, 4.0F};
        double[] centres = {x + 1.5, x - 2.5, x - 7.0};
        server.runOnServer(s -> {
            ServerLevel level = s.overworld();
            for (int i = 0; i < sizes.length; i++) {
                TonnFish fish = (TonnFish) MimFishes.TONN.type().create(level, EntitySpawnReason.COMMAND);
                fish.snapTo(centres[i], y + 1.2, fz + 0.5, 90.0F, 0.0F);
                fish.setYHeadRot(90.0F);
                fish.setYBodyRot(90.0F);
                fish.setNoAi(true);
                fish.setPersistenceRequired();
                fish.setLength(sizes[i]);
                fish.setHealth(fish.getMaxHealth());
                level.addFreshEntity(fish);
            }
        });
        context.runOnClient(mc -> {
            if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle();
            net.minecraft.client.player.RemotePlayer figure = new net.minecraft.client.player.RemotePlayer(mc.level,
                new com.mojang.authlib.GameProfile(UUID.randomUUID(), "Steve"));
            figure.setId(-4242);
            figure.snapTo(x + 6.5, y, fz - 0.5, 160.0F, 0.0F);
            figure.setYHeadRot(160.0F);
            figure.setYBodyRot(160.0F);
            mc.level.addEntity(figure);
        });
        world.getConnection().waitForChunksRender();
        context.waitTicks(30);
        look(context, server, x - 1.0, y, fz - 10.5, x - 1.0, y + 1.3, fz + 0.5, "fish-tonn-sizes");
        context.runOnClient(mc -> mc.level.removeEntity(-4242, Entity.RemovalReason.DISCARDED));
    }

    /** Every tonn in the area, by UUID, with its length. */
    private static Map<UUID, Float> tonnLengths(TestServerContext server, AABB area) {
        return server.computeOnServer(s -> {
            Map<UUID, Float> out = new HashMap<>();
            tonns(s.overworld(), area).forEach(f -> out.put(f.getUUID(), f.getLength()));
            return out;
        });
    }

    private static List<TonnFish> tonns(ServerLevel level, AABB area) {
        List<TonnFish> out = new ArrayList<>();
        level.getEntities(MimFishes.TONN.type(), area, e -> true).forEach(e -> out.add((TonnFish) e));
        return out;
    }

    /** Null if the fish's scale and hitbox fit a tonn of this length, else what is wrong. */
    private static String sizeProblem(AbstractFish fish, float length) {
        float scale = length / TonnFish.MODEL_LENGTH;
        if (Math.abs(fish.getScale() - scale) > 0.001F || Math.abs(fish.getBbWidth() - 1.3F * scale) > 0.01F
            || Math.abs(fish.getBbHeight() - 0.7F * scale) > 0.01F) {
            return String.format(Locale.ROOT, "length %.2f has scale %.3f (want %.3f) and hitbox %.2fx%.2f (want %.2fx%.2f)",
                length, fish.getScale(), scale, fish.getBbWidth(), fish.getBbHeight(), 1.3F * scale, 0.7F * scale);
        }
        return null;
    }

    /** The sardina model's own review: one sardina alone in a small tank, close up from several sides, one beside a vanilla cod, and one on land. */
    private static void sardinaShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 7, y, z - 6, x + 7, y + 12, z + 10, "minecraft:air");
        fill(server, x - 7, y - 1, z - 6, x + 7, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 4, y, z + 4, x + 4, y + 4, z + 9, "minecraft:glass");
        fill(server, x - 3, y, z + 5, x + 3, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:sardina %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1.5, z + 5.6));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.4, y + 1.5, z + 5.6));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:sardina %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall, so no glass frames cross the fish; in spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.5, y, z + 4.3, x + 0.5, y + 1.5, z + 5.6, "fish-sardina-side");
        look(context, server, x - 0.4, y + 0.6, z + 4.4, x + 0.5, y + 1.5, z + 5.6, "fish-sardina-three-quarter");
        look(context, server, x + 0.5, y + 1.1, z + 4.85, x + 0.5, y + 1.5, z + 5.6, "fish-sardina-top");
        look(context, server, x - 0.45, y, z + 4.3, x - 0.45, y + 1.5, z + 5.6, "fish-sardina-beside-cod");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y, z - 1.0, x + 0.5, y + 0.15, z + 0.5, "fish-sardina-on-land");
    }

    /** The cerna model's own review: one cerna alone in a small tank, close up from several sides, one beside a vanilla cod, and one on land. */
    private static void cernaShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 7, y, z - 6, x + 7, y + 12, z + 10, "minecraft:air");
        fill(server, x - 7, y - 1, z - 6, x + 7, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 5, y, z + 4, x + 5, y + 5, z + 9, "minecraft:glass");
        fill(server, x - 4, y, z + 5, x + 4, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:cerna %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1.5, z + 6.2));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.9, y + 1.6, z + 6.2));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:cerna %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall, so no glass frames cross the fish; in spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.5, y + 0.2, z + 4.3, x + 0.5, y + 1.85, z + 6.2, "fish-cerna-side");
        look(context, server, x - 1.0, y + 0.6, z + 4.6, x + 0.3, y + 1.85, z + 6.2, "fish-cerna-three-quarter");
        look(context, server, x + 0.5, y + 1.6, z + 4.7, x + 0.5, y + 1.85, z + 6.2, "fish-cerna-top");
        look(context, server, x - 0.6, y + 0.2, z + 4.3, x - 0.6, y + 1.85, z + 6.2, "fish-cerna-beside-cod");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y, z - 1.3, x + 0.5, y + 0.2, z + 0.5, "fish-cerna-on-land");
    }

    /** The ziemel model's own review: one seahorse alone in a small tank (side, three-quarter, and face on from inside
     *  the water), one beside a vanilla cod for its size, and one on land. */
    private static void ziemelShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 7, y, z - 6, x + 7, y + 12, z + 10, "minecraft:air");
        fill(server, x - 7, y - 1, z - 6, x + 7, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 4, y, z + 4, x + 4, y + 4, z + 9, "minecraft:glass");
        fill(server, x - 3, y, z + 5, x + 3, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:ziemel %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1.3, z + 5.6));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:ziemel %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall (or in the water, face on), so no glass frames cross the fish; in
        // spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.5, y + 0.1, z + 4.3, x + 0.5, y + 1.7, z + 5.6, "fish-ziemel-side");
        look(context, server, x - 0.5, y + 0.5, z + 4.4, x + 0.5, y + 1.7, z + 5.6, "fish-ziemel-three-quarter");
        look(context, server, x - 1.2, y + 0.1, z + 5.6, x + 0.5, y + 1.7, z + 5.6, "fish-ziemel-front");
        // the cod comes in only now, so it doesn't stand between the camera and the seahorse's face
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.4, y + 1.5, z + 5.6));
        context.waitTicks(20);
        look(context, server, x - 0.45, y + 0.1, z + 4.3, x - 0.45, y + 1.6, z + 5.6, "fish-ziemel-beside-cod");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y, z - 1.0, x + 0.5, y + 0.15, z + 0.5, "fish-ziemel-on-land");
    }

    private static Map<String, Vec3> positions(TestServerContext server, AABB area) {
        return server.computeOnServer(s -> {
            Map<String, Vec3> out = new HashMap<>();
            for (Entity e : s.overworld().getEntitiesOfClass(AbstractFish.class, area)) {
                out.put(BuiltInRegistries.ENTITY_TYPE.getKey(e.getType()).getPath(), e.position());
            }
            return out;
        });
    }

    /** What items lie in the area, as "namespace:id xN" joined by commas (sorted). */
    private static String drops(TestServerContext server, AABB area) {
        return server.computeOnServer(s -> {
            Map<String, Integer> counts = new java.util.TreeMap<>();
            for (ItemEntity item : s.overworld().getEntitiesOfClass(ItemEntity.class, area)) {
                counts.merge(BuiltInRegistries.ITEM.getKey(item.getItem().getItem()).toString(), item.getItem().getCount(), Integer::sum);
            }
            List<String> out = new ArrayList<>();
            counts.forEach((k, v) -> out.add(k + " x" + v));
            return String.join(", ", out);
        });
    }

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

    private static void fill(TestServerContext server, int x0, int y0, int z0, int x1, int y1, int z1, String block) {
        server.runCommand(String.format("fill %d %d %d %d %d %d %s", x0, y0, z0, x1, y1, z1, block));
    }

    private static void check(boolean ok, String message) {
        if (!ok) {
            throw new AssertionError("[smoke] fish: " + message);
        }
    }

    private static void log(String message) {
        System.out.println("[smoke] fish: " + message);
    }
}
