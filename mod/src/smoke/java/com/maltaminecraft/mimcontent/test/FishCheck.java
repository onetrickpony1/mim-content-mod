package com.maltaminecraft.mimcontent.test;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.maltaminecraft.mimcontent.MimConfig;
import com.maltaminecraft.mimcontent.MimFishes;
import com.maltaminecraft.mimcontent.entity.fish.BollFish;
import com.maltaminecraft.mimcontent.entity.fish.BottomFish;
import com.maltaminecraft.mimcontent.entity.fish.FishPart;
import com.maltaminecraft.mimcontent.entity.fish.FishParts;
import com.maltaminecraft.mimcontent.entity.fish.HutaKahlaFish;
import com.maltaminecraft.mimcontent.entity.fish.MolaFish;
import com.maltaminecraft.mimcontent.entity.fish.SkorfnaFish;
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
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.MobBucketItem;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.biome.Biomes;
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
        if (Smoke.listed("fish-hitboxes")) {
            // SMOKE_ONLY=fish-hitboxes: only the hit box check (it is also part of the whole fish check, below)
            FishHitboxCheck.run(context);
            System.out.println("[smoke] fish: hit boxes passed, screenshots written");
            return;
        }
        if (Smoke.listed("fish-one")) {
            // SMOKE_ONLY=fish-one FISH_ONLY=<id>: one fish's review shots, its hit box row and its swim check, for the art makers
            oneFish(context, Smoke.fishOnly());
            return;
        }
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

            // 2. each fish lives and swims: all twenty-six at once (the tier A seven, the pixxispad, the inċova, ċawl, ħuta
            // kaħla, boll, skorfna and mola mola, and the night job's twelve), positions sampled for 200 ticks (the
            // skorfna, sawt and petriċa sink to the floor, which counts)
            List<MimFishes.Fish> all = MimFishes.ALL;
            check(all.size() == 26, "expected 26 fish, found " + all.size());
            swims(context, server, x, y, z, pool, all);
            // the pixxispad is a fast swimmer: twice vanilla's fish speed
            double[] speeds = server.computeOnServer(s -> new double[] {
                MimFishes.PIXXISPAD.type().create(s.overworld(), EntitySpawnReason.COMMAND).getAttributeValue(Attributes.MOVEMENT_SPEED),
                MimFishes.CERNA.type().create(s.overworld(), EntitySpawnReason.COMMAND).getAttributeValue(Attributes.MOVEMENT_SPEED)});
            log(String.format(Locale.ROOT, "swim speed: pixxispad %.2f, cerna %.2f", speeds[0], speeds[1]));
            check(speeds[0] == 1.4 && speeds[1] == 0.7, "the pixxispad should swim at 1.4 and the others at 0.7");

            // 3. drops: kill each one in turn, count what lands
            for (MimFishes.Fish f : all) {
                server.runCommand("kill @e[type=item]");
                // the skorfna was summoned with a random version, and each version drops its own item
                boolean red = f == MimFishes.SKORFNA && server.computeOnServer(s -> s.overworld().getEntities(f.type(), pool, e -> true).stream()
                    .anyMatch(e -> e instanceof SkorfnaFish k && k.getVariant() == SkorfnaFish.Variant.RED));
                server.runCommand("kill @e[type=mimcontent:" + f.id() + "]");
                context.waitTicks(5);
                String drops = drops(server, pool);
                String expected = f.item() == null ? "" : BuiltInRegistries.ITEM.getKey(red ? MimFishes.SKORFNA_RED : f.item()) + " x1";
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
            skorfnaDrops(context, server, x, y, z, pool);

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
            server.runCommand("kill @e[type=!minecraft:player]");
            vanillaOceanSpawns(server);
            shark(context, server, x, y, z, pool);
            server.runCommand("kill @e[type=!minecraft:player]");
            boll(context, server, x, y, z, pool);
            server.runCommand("kill @e[type=!minecraft:player]");
            skorfna(context, server, x, y, z, pool);
            server.runCommand("kill @e[type=!minecraft:player]");
            mola(context, server, x, y, z);
            server.runCommand("kill @e[type=!minecraft:player]");
            nightFish(context, server, x, y, z, pool);
            server.runCommand("gamemode creative @a");
            server.runCommand("kill @e[type=!minecraft:player]");
            log("all checks passed");

            shots(context, server, world, p[0], p[1], p[2]);
        }
        tonnSizes(context);
        skorfnaVariants(context);
        FishHitboxCheck.run(context);
        System.out.println("[smoke] fish: all checks passed, screenshots written");
    }

    /**
     * Each fish lives and swims: summoned in the pool at once, spread across its water, positions sampled for 200 ticks;
     * each must be alive, in the water, and have swum more than half a block. Logs each one's health and body box.
     */
    private static void swims(ClientGameTestContext context, TestServerContext server, int x, int y, int z, AABB pool, List<MimFishes.Fish> all) {
        for (int i = 0; i < all.size(); i++) {
            // spread across the pool's water (x - 7 to x + 7), however many fish there are
            server.runCommand(String.format(Locale.ROOT, "summon mimcontent:%s %.1f %d %.1f", all.get(i).id(), x - 6.0 + 12.0 * i / Math.max(1, all.size() - 1), y - 3, z + 0.5));
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
    }

    /**
     * SMOKE_ONLY=fish-one FISH_ONLY=&lt;id&gt; (the art makers' quick run): only that fish. It swims in the pool (the swim
     * check above, alone), then takes the review shots the whole fish check takes for it (ownShots) and its own hotbar
     * (fish-&lt;id&gt;-hotbar: its item, bucket and egg beside vanilla's cod), and checks its row of FishShape's table against
     * its model (FishHitboxCheck.runOne, which logs the measured row). Everything else is the whole check's
     * (SMOKE_ONLY=fish), which still has to pass before a fish is done.
     */
    private static void oneFish(ClientGameTestContext context, String id) {
        MimFishes.Fish f = MimFishes.ALL.stream().filter(g -> g.id().equals(id)).findFirst().orElse(null);
        check(f != null, "FISH_ONLY: no fish called '" + id + "'; the ids are "
            + MimFishes.ALL.stream().map(MimFishes.Fish::id).toList());
        try (TestSingleplayerContext world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            TestServerContext server = world.getServer();
            server.runCommand("gamemode creative @a");
            server.runCommand("gamerule spawn_mobs false");
            server.runCommand("gamerule advance_time false");
            server.runCommand("time set 6000");
            int[] p = context.computeOnClient(mc -> new int[] {mc.player.getBlockX(), mc.player.getBlockY(), mc.player.getBlockZ()});
            int x = p[0], y = p[1] + 30, z = p[2];
            // the same pool as the whole check's
            fill(server, x - 10, y - 8, z - 10, x + 10, y + 4, z + 10, "minecraft:air");
            fill(server, x - 8, y - 6, z - 8, x + 8, y, z + 8, "minecraft:stone");
            fill(server, x - 7, y - 5, z - 7, x + 7, y - 1, z + 7, "minecraft:water");
            server.runCommand(String.format("tp @a %d %d %d", x - 8, y + 1, z - 8));
            world.getConnection().waitForChunksRender();
            context.waitTicks(10);
            AABB pool = new AABB(x - 9, y - 7, z - 9, x + 10, y + 5, z + 10);
            swims(context, server, x, y, z, pool, List.of(f));
            server.runCommand("kill @e[type=!minecraft:player]");
            FishHitboxCheck.runOne(context, f);

            // the shots, on the ground near spawn as in shots()
            server.runCommand(String.format("tp @a %d %d %d", p[0], p[1] + 3, p[2] + 16));
            world.getConnection().waitForChunksRender();
            context.runOnClient(mc -> {
                if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle();
            });
            ownShots(context, server, world, p[0], p[1], p[2] + 20, f);
            context.runOnClient(mc -> {
                if (mc.gui.hud.isHidden()) mc.gui.hud.toggle();
                mc.options.guiScale().set(4);
            });
            server.runCommand("gamemode creative @a");
            server.runCommand(String.format("tp @a %d %d %d 0 -60", p[0], p[1], p[2] + 17));
            List<String> bar = new ArrayList<>(List.of("minecraft:cod"));
            if (f.item() != null) {
                bar.add(BuiltInRegistries.ITEM.getKey(f.item()).toString());
            }
            if (f == MimFishes.SKORFNA) {
                bar.add(BuiltInRegistries.ITEM.getKey(MimFishes.SKORFNA_RED).toString());
            }
            bar.addAll(List.of("minecraft:cod_bucket", BuiltInRegistries.ITEM.getKey(f.bucket()).toString(),
                "minecraft:cod_spawn_egg", BuiltInRegistries.ITEM.getKey(f.spawnEgg()).toString()));
            for (int i = 0; i < 9; i++) {
                server.runCommand("item replace entity @a hotbar." + i + " with " + (i < bar.size() ? bar.get(i) : "minecraft:air"));
            }
            // until the game mode messages in the chat have faded (10 s)
            context.waitTicks(210);
            context.takeScreenshot("fish-" + id + "-hotbar");
        }
        if (f == MimFishes.TONN) {
            tonnSizes(context);
        }
        if (f == MimFishes.SKORFNA) {
            skorfnaVariants(context);
        }
        System.out.println("[smoke] fish: " + id + ": fish-one checks passed, screenshots written");
    }

    /**
     * One fish's own review shots, the same ones shots() takes for it (the tank shots of all the fish together and the
     * shared hotbars aren't here). When you add a shot for a fish in shots(), add it here too.
     */
    private static void ownShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z, MimFishes.Fish f) {
        switch (f.id()) {
            case "lampuka" -> lampukaShots(context, server, world, x, y, z);
            case "tonn" -> tonnShots(context, server, world, x, y, z);
            case "sardina" -> sardinaShots(context, server, world, x, y, z);
            case "cerna" -> cernaShots(context, server, world, x, y, z);
            case "ziemel" -> ziemelShots(context, server, world, x, y, z);
            case "pixxispad" -> pixxispadShots(context, server, world, x, y, z);
            case "awrata" -> awrataShots(context, server, world, x, y, z);
            case "murina" -> murinaShots(context, server, world, x, y, z);
            case "incova" -> incovaShots(context, server, world, x, y, z);
            case "cawl" -> cawlShots(context, server, world, x, y, z);
            case "huta_kahla" -> hutaKahlaShots(context, server, world, x, y, z);
            case "boll" -> bollShots(context, server, world, x, y, z);
            case "skorfna" -> skorfnaShots(context, server, world, x, y, z);
            case "mola_mola" -> molaShots(context, server, world, x, y, z);
            default -> {
                // the night job's fish: the placeholder shots, then any of their own
                check(java.util.Arrays.asList(NIGHT).contains(f), f.id() + " has no review shots in ownShots");
                placeholderShots(context, server, world, x, y, z, f.id());
                switch (f.id()) {
                    case "lizz" -> lizzSizeShot(context, server, world, x + 30, y, z);
                    case "marzpan" -> marzpanSizeShot(context, server, world, x + 30, y, z);
                    case "kavall" -> kavallSizeShot(context, server, world, x + 30, y, z);
                    case "tird" -> tirdSizeShot(context, server, world, x + 30, y, z);
                    default -> {
                    }
                }
            }
        }
    }

    /**
     * The inċova, ċawl and ħuta kaħla are in vanilla's oceans (the switch is on): each in the oceans picked for it.
     * (The Malta world's biomes aren't in a test world.)
     */
    private static void vanillaOceanSpawns(TestServerContext server) {
        Map<MimFishes.Fish, List<net.minecraft.resources.ResourceKey<net.minecraft.world.level.biome.Biome>>> want = Map.of(
            MimFishes.INCOVA, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN, Biomes.DEEP_LUKEWARM_OCEAN, Biomes.OCEAN, Biomes.DEEP_OCEAN),
            MimFishes.CAWL, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN),
            MimFishes.HUTA_KAHLA, List.of(Biomes.LUKEWARM_OCEAN, Biomes.DEEP_LUKEWARM_OCEAN, Biomes.DEEP_OCEAN),
            MimFishes.BOLL, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN),
            MimFishes.SKORFNA, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN),
            MimFishes.MOLA_MOLA, List.of(Biomes.WARM_OCEAN, Biomes.DEEP_LUKEWARM_OCEAN));
        // the night job's fish (2026-11-18)
        Map<MimFishes.Fish, List<net.minecraft.resources.ResourceKey<net.minecraft.world.level.biome.Biome>>> night = Map.ofEntries(
            Map.entry(MimFishes.KAVALL, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN, Biomes.DEEP_LUKEWARM_OCEAN)),
            Map.entry(MimFishes.LIZZ, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN)),
            Map.entry(MimFishes.MARZPAN, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN)),
            Map.entry(MimFishes.TIRD, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN)),
            Map.entry(MimFishes.TRILJA, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN)),
            Map.entry(MimFishes.SAWT, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN)),
            Map.entry(MimFishes.PIXXI_SAN_PIETRU, List.of(Biomes.LUKEWARM_OCEAN, Biomes.DEEP_LUKEWARM_OCEAN)),
            Map.entry(MimFishes.PETRICA, List.of(Biomes.DEEP_LUKEWARM_OCEAN)),
            Map.entry(MimFishes.LINGWATA, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN)),
            Map.entry(MimFishes.HMAR, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN)),
            Map.entry(MimFishes.GALLINELLA, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN, Biomes.DEEP_LUKEWARM_OCEAN)),
            Map.entry(MimFishes.LIONFISH, List.of(Biomes.WARM_OCEAN)));
        Map<MimFishes.Fish, List<net.minecraft.resources.ResourceKey<net.minecraft.world.level.biome.Biome>>> both = new HashMap<>(want);
        both.putAll(night);
        String result = server.computeOnServer(s -> {
            var biomes = s.registryAccess().lookupOrThrow(Registries.BIOME);
            StringBuilder out = new StringBuilder();
            for (var e : both.entrySet()) {
                for (var key : e.getValue()) {
                    boolean found = spawnsIn(biomes.getValue(key)).getMobsToSpawn(MobCategory.WATER_AMBIENT).unwrap().stream()
                        .anyMatch(w -> w.value().type() == e.getKey().type());
                    if (!found) {
                        out.append(e.getKey().id()).append(" missing from ").append(key.identifier()).append("; ");
                    }
                    // the mola mola is extremely rare (owner 2026-11-18): the lowest weight, 1
                    if (e.getKey() == MimFishes.MOLA_MOLA && spawnsIn(biomes.getValue(key)).getMobsToSpawn(MobCategory.WATER_AMBIENT).unwrap().stream()
                        .anyMatch(w -> w.value().type() == e.getKey().type() && w.weight() != 1)) {
                        out.append("mola_mola weight is not 1 in ").append(key.identifier()).append("; ");
                    }
                }
                // and never in a cold ocean
                if (spawnsIn(biomes.getValue(Biomes.COLD_OCEAN)).getMobsToSpawn(MobCategory.WATER_AMBIENT).unwrap().stream()
                    .anyMatch(w -> w.value().type() == e.getKey().type())) {
                    out.append(e.getKey().id()).append(" in cold ocean; ");
                }
            }
            return out.isEmpty() ? "ok" : out.toString();
        });
        log("inċova, ċawl, ħuta kaħla, boll, skorfna, mola mola and the night job's twelve: spawns in vanilla oceans: " + result);
        check(result.equals("ok"), "spawns: " + result);
    }

    /** A biome's natural spawns (in 26.3 an environment attribute of the biome). */
    private static net.minecraft.world.level.biome.MobSpawnSettings spawnsIn(net.minecraft.world.level.biome.Biome biome) {
        var attribute = net.minecraft.world.attribute.EnvironmentAttributes.NATURAL_MOB_SPAWNS;
        return biome.getAttributes().applyModifier(attribute, attribute.defaultValue());
    }

    /**
     * The ħuta kaħla's behaviour (owner 2026-11-18: "blue shark should ignore you unless you hurt it OR you have fish
     * in your inventory"), with the player in survival in the water beside it: an idle player without fish is left
     * alone; a cod in the hotbar, or a lampuka deep in the inventory, draws it; it gives up once the fish are gone;
     * hurting it makes it bite back.
     */
    private static void shark(ClientGameTestContext context, TestServerContext server, int x, int y, int z, AABB pool) {
        server.runCommand("clear @a");
        server.runCommand("effect give @a minecraft:water_breathing 120 0 true");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:huta_kahla %.1f %d %.1f {PersistenceRequired:1b}", x + 0.5, y - 3, z + 0.5));
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %d %.1f", x - 3.5, y - 5, z + 0.5));
        context.waitTicks(5);
        // idle, no fish: 5 seconds, never a target
        boolean everTargeted = false;
        for (int t = 0; t < 10; t++) {
            context.waitTicks(10);
            everTargeted |= sharkState(server, pool).startsWith("target=player");
        }
        String idle = sharkState(server, pool);
        log("shark beside an idle player without fish: " + idle + (everTargeted ? " (but targeted the player at some point)" : ""));
        check(!everTargeted && idle.startsWith("target=none") && idle.contains("angry=false"), "the shark should ignore a player without fish: " + idle);

        String[][] baits = {{"hotbar.0", "minecraft:cod"}, {"inventory.10", "mimcontent:lampuka"}};
        for (String[] bait : baits) {
            server.runCommand("item replace entity @a " + bait[0] + " with " + bait[1]);
            String state = waitForShark(context, server, pool, "target=player", 100);
            log("player carrying " + bait[1] + " (" + bait[0] + "): " + state);
            check(state.startsWith("target=player") && state.contains("bait=true") && state.contains("angry=false"),
                "the shark should hunt a player carrying " + bait[1] + ": " + state);
            server.runCommand("clear @a");
            String gaveUp = waitForShark(context, server, pool, "target=none", 140);
            log("fish gone: " + gaveUp);
            check(gaveUp.startsWith("target=none"), "the shark should give up once the fish are gone: " + gaveUp);
        }

        // hurt it: it turns on the player and bites (resistance keeps the player safe; the hit still counts)
        server.runOnServer(s -> {
            ServerLevel level = s.overworld();
            ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
            player.setLastHurtByMob(null);
            HutaKahlaFish shark = (HutaKahlaFish) level.getEntities(MimFishes.HUTA_KAHLA.type(), pool, e -> true).getFirst();
            shark.hurtServer(level, level.damageSources().playerAttack(player), 1.0F);
        });
        String angry = waitForShark(context, server, pool, "target=player", 40);
        log("after being hurt: " + angry);
        check(angry.startsWith("target=player") && angry.contains("angry=true") && angry.contains("bait=false"),
            "a hurt shark should turn on the player: " + angry);
        boolean bitten = false;
        for (int t = 0; t < 30 && !bitten; t++) {
            context.waitTicks(10);
            bitten = server.computeOnServer(s -> {
                ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                return player.getLastHurtByMob() != null && player.getLastHurtByMob().getType() == MimFishes.HUTA_KAHLA.type();
            });
        }
        log("the hurt shark bit the player: " + bitten);
        check(bitten, "a hurt shark should bite the player");
        server.runCommand("effect clear @a minecraft:water_breathing");
        server.runCommand("clear @a");
    }

    /**
     * The boll (common stingray): it lives on the bottom (summoned near the surface, it goes down and stays within
     * about two blocks of the floor); it only spawns over a soft floor; hurt it and it stings the attacker (damage and
     * poison); a survival player standing on it is stung; a creative player is not.
     */
    private static void boll(ClientGameTestContext context, TestServerContext server, int x, int y, int z, AABB pool) {
        server.runCommand("clear @a");
        server.runCommand("effect clear @a");
        // the pool: water y-5 to y-1, its stone floor's top at y-5. A spectator far off, so it doesn't shy away.
        server.runCommand("gamemode spectator @a");
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x - 8, y + 6, z - 8));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:boll %.1f %.1f %.1f {PersistenceRequired:1b}", x + 0.5, y - 1.5, z + 0.5));
        double floor = y - 5;
        context.waitTicks(140);
        double highest = 0.0, sum = 0.0;
        boolean rested = false;
        int samples = 30;
        for (int t = 0; t < samples; t++) {
            context.waitTicks(10);
            double[] h = server.computeOnServer(s -> {
                BollFish boll = (BollFish) s.overworld().getEntities(MimFishes.BOLL.type(), pool, e -> true).getFirst();
                return new double[] {boll.getY() - floor, boll.isResting() ? 1 : 0};
            });
            highest = Math.max(highest, h[0]);
            sum += h[0];
            rested |= h[1] > 0;
        }
        log(String.format(Locale.ROOT, "boll summoned 3.5 blocks above the floor: after 7 s, over 15 s it swam at most %.2f blocks above the floor"
            + " (on average %.2f); rested on the bottom: %s", highest, sum / samples, rested));
        // the water's surface is 4 blocks above the floor here
        check(highest <= BollFish.SWIM_HIGH + 1.0 && sum / samples <= 1.5,
            String.format(Locale.ROOT, "the boll should stay near the bottom, it rose %.2f above it (average %.2f)", highest, sum / samples));

        // the spawn floor: sand under one spot of the pool, stone under the rest
        server.runCommand(String.format(Locale.ROOT, "setblock %d %d %d minecraft:sand", x + 5, y - 6, z + 5));
        String floors = server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            boolean sand = BollFish.softFloorBelow(level, new BlockPos(x + 5, y - 3, z + 5)) != null;
            boolean stone = BollFish.softFloorBelow(level, new BlockPos(x - 5, y - 3, z - 5)) != null;
            @SuppressWarnings("unchecked")
            var type = (net.minecraft.world.entity.EntityType<BollFish>) (Object) MimFishes.BOLL.type();
            boolean rule = BollFish.checkBollSpawnRules(type, level, EntitySpawnReason.NATURAL, new BlockPos(x + 5, y - 3, z + 5), level.getRandom());
            return "over sand " + sand + ", over stone " + stone + "; the full rule over sand here (sea level " + level.getSeaLevel()
                + ", pool at y " + (y - 3) + "): " + rule;
        });
        log("boll spawn floor: " + floors);
        check(floors.startsWith("over sand true, over stone false"), "the boll should spawn over sand only: " + floors);

        // hurt it, with the player beside it: it stings back
        server.runCommand("gamemode survival @a");
        server.runCommand("effect give @a minecraft:water_breathing 120 0 true");
        Vec3 at = server.computeOnServer(s -> s.overworld().getEntities(MimFishes.BOLL.type(), pool, e -> true).getFirst().position());
        server.runCommand(String.format(Locale.ROOT, "tp @a %.2f %.2f %.2f", at.x + 1.2, at.y, at.z));
        context.waitTicks(5);
        String hurt = server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
            player.setHealth(player.getMaxHealth());
            player.setLastHurtByMob(null);
            BollFish boll = (BollFish) level.getEntities(MimFishes.BOLL.type(), pool, e -> true).getFirst();
            boll.hurtServer(level, level.damageSources().playerAttack(player), 1.0F);
            return stingState(player);
        });
        log("hurt the boll from beside it: " + hurt);
        check(hurt.contains("poison=" + BollFish.POISON_SECONDS * 20) && hurt.contains("by boll") && !hurt.startsWith("health 20.0"),
            "a hurt boll should sting the attacker (2 damage and poison): " + hurt);

        // a survival player standing on a boll lying on the floor is stung; then a creative one is not
        server.runCommand("kill @e[type=mimcontent:boll]");
        server.runCommand("effect clear @a minecraft:poison");
        // past the player's hurt cooldown from the sting above (else the next sting's damage doesn't count)
        context.waitTicks(25);
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:boll %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b}", x + 3.5, floor, z - 3.5));
        server.runOnServer(s -> {
            ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
            player.setHealth(player.getMaxHealth());
            player.setLastHurtByMob(null);
        });
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %.2f %.1f", x + 3.5, floor + 0.1, z - 3.5));
        String stepped = waitForSting(context, server, 20);
        log("a survival player standing on a boll: " + stepped);
        check(stepped.contains("poison=") && !stepped.contains("poison=none") && stepped.contains("by boll"),
            "a survival player standing on a boll should be stung: " + stepped);
        server.runCommand("effect clear @a minecraft:poison");
        server.runCommand("gamemode creative @a");
        server.runOnServer(s -> s.getPlayerList().getPlayers().getFirst().setLastHurtByMob(null));
        context.waitTicks(BollFish.STING_COOLDOWN + 5);
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %.2f %.1f", x + 3.5, floor + 0.1, z - 3.5));
        String creative = waitForSting(context, server, 30);
        log("a creative player standing on a boll: " + creative);
        check(creative.contains("poison=none") && !creative.contains("by boll"), "a creative player should not be stung: " + creative);

        // a survival player under Jellyfish Ward isn't stung either (Venom.canSting: the Ward blocks every sting)
        server.runCommand("effect give @a mimcontent:jellyfish_ward 60 0 true");
        server.runCommand("gamemode survival @a");
        server.runOnServer(s -> s.getPlayerList().getPlayers().getFirst().setLastHurtByMob(null));
        context.waitTicks(BollFish.STING_COOLDOWN + 5);
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %.2f %.1f", x + 3.5, floor + 0.1, z - 3.5));
        String warded = waitForSting(context, server, 30);
        log("a survival player under Jellyfish Ward standing on a boll: " + warded);
        check(warded.contains("poison=none") && !warded.contains("by boll"), "a player under Jellyfish Ward should not be stung by a boll: " + warded);
        server.runCommand("effect clear @a mimcontent:jellyfish_ward");
        server.runCommand("gamemode creative @a");
        server.runCommand("effect clear @a");
        server.runCommand("clear @a");
    }

    /**
     * The skorfna (black scorpionfish): it lives on the bottom (summoned near the surface, it sinks and stays on the
     * floor, resting most of the time); it only spawns over a rock floor; hit it in melee and its spines sting the
     * attacker (damage and poison); a survival player or a mob touching it is stung; a creative player is not.
     */
    private static void skorfna(ClientGameTestContext context, TestServerContext server, int x, int y, int z, AABB pool) {
        server.runCommand("clear @a");
        server.runCommand("effect clear @a");
        // the pool: water y-5 to y-1, its stone floor's top at y-5. A spectator far off.
        server.runCommand("gamemode spectator @a");
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x - 8, y + 6, z - 8));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:skorfna %.1f %.1f %.1f {PersistenceRequired:1b}", x + 0.5, y - 1.5, z + 0.5));
        double floor = y - 5;
        context.waitTicks(100);
        double highest = 0.0, sum = 0.0;
        int rests = 0, samples = 40;
        for (int t = 0; t < samples; t++) {
            context.waitTicks(10);
            double[] h = server.computeOnServer(s -> {
                SkorfnaFish fish = (SkorfnaFish) s.overworld().getEntities(MimFishes.SKORFNA.type(), pool, e -> true).getFirst();
                return new double[] {fish.getY() - floor, fish.isResting() ? 1 : 0};
            });
            highest = Math.max(highest, h[0]);
            sum += h[0];
            rests += (int) h[1];
        }
        log(String.format(Locale.ROOT, "skorfna summoned 3.5 blocks above the floor: after 5 s, over 20 s it was at most %.2f blocks above the floor"
            + " (on average %.2f); resting in %d of %d samples", highest, sum / samples, rests, samples));
        check(highest <= 0.6 && sum / samples <= 0.3, String.format(Locale.ROOT,
            "the skorfna should stay on the bottom, it rose %.2f above it (average %.2f)", highest, sum / samples));
        check(rests >= samples / 2, "the skorfna should rest most of the time, it rested in " + rests + " of " + samples + " samples");

        // the spawn floor: sand under one spot of the pool, stone under the rest
        server.runCommand(String.format(Locale.ROOT, "setblock %d %d %d minecraft:sand", x + 5, y - 6, z + 5));
        String floors = server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            boolean stone = SkorfnaFish.rockFloorBelow(level, new BlockPos(x - 5, y - 3, z - 5)) != null;
            boolean sand = SkorfnaFish.rockFloorBelow(level, new BlockPos(x + 5, y - 3, z + 5)) != null;
            @SuppressWarnings("unchecked")
            var type = (net.minecraft.world.entity.EntityType<SkorfnaFish>) (Object) MimFishes.SKORFNA.type();
            boolean rule = SkorfnaFish.checkSkorfnaSpawnRules(type, level, EntitySpawnReason.NATURAL, new BlockPos(x - 5, y - 3, z - 5), level.getRandom());
            return "over stone " + stone + ", over sand " + sand + "; the full rule over stone here (sea level " + level.getSeaLevel()
                + ", pool at y " + (y - 3) + "): " + rule;
        });
        log("skorfna spawn floor: " + floors);
        check(floors.startsWith("over stone true, over sand false"), "the skorfna should spawn over rock only: " + floors);
        server.runCommand(String.format(Locale.ROOT, "setblock %d %d %d minecraft:stone", x + 5, y - 6, z + 5));

        // hit it in melee, with the player beside it: the spines sting
        server.runCommand("gamemode survival @a");
        server.runCommand("effect give @a minecraft:water_breathing 120 0 true");
        Vec3 at = server.computeOnServer(s -> s.overworld().getEntities(MimFishes.SKORFNA.type(), pool, e -> true).getFirst().position());
        server.runCommand(String.format(Locale.ROOT, "tp @a %.2f %.2f %.2f", at.x + 1.5, at.y, at.z));
        context.waitTicks(5);
        String hit = server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
            player.setHealth(player.getMaxHealth());
            player.setLastHurtByMob(null);
            player.removeEffect(net.minecraft.world.effect.MobEffects.POISON);
            SkorfnaFish fish = (SkorfnaFish) level.getEntities(MimFishes.SKORFNA.type(), pool, e -> true).getFirst();
            fish.hurtServer(level, level.damageSources().playerAttack(player), 1.0F);
            return stingState(player);
        });
        log("hit the skorfna in melee: " + hit);
        check(hit.contains("poison=" + SkorfnaFish.POISON_SECONDS * 20) && hit.contains("by skorfna") && !hit.startsWith("health 20.0"),
            "a skorfna hit in melee should sting the attacker (2 damage and poison): " + hit);

        // a survival player touching (standing on) a skorfna lying on the floor is stung
        server.runCommand("kill @e[type=mimcontent:skorfna]");
        server.runCommand("effect clear @a minecraft:poison");
        // past the player's hurt cooldown from the sting above (else the next sting's damage doesn't count)
        context.waitTicks(25);
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:skorfna %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b}", x + 3.5, floor, z - 3.5));
        server.runOnServer(s -> {
            ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
            player.setHealth(player.getMaxHealth());
            player.setLastHurtByMob(null);
        });
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %.2f %.1f", x + 3.5, floor + 0.1, z - 3.5));
        String touched = waitForSting(context, server, 20);
        log("a survival player touching a skorfna: " + touched);
        check(touched.contains("poison=") && !touched.contains("poison=none") && touched.contains("by skorfna"),
            "a survival player touching a skorfna should be stung: " + touched);

        // then a creative one is not
        server.runCommand("effect clear @a minecraft:poison");
        server.runCommand("gamemode creative @a");
        server.runOnServer(s -> s.getPlayerList().getPlayers().getFirst().setLastHurtByMob(null));
        context.waitTicks(SkorfnaFish.STING_COOLDOWN + 5);
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %.2f %.1f", x + 3.5, floor + 0.1, z - 3.5));
        String creative = waitForSting(context, server, 30);
        log("a creative player touching a skorfna: " + creative);
        check(creative.contains("poison=none") && !creative.contains("by skorfna"), "a creative player should not be stung: " + creative);

        // a survival player under Jellyfish Ward isn't stung either (Venom.canSting: the Ward blocks every sting)
        server.runCommand("effect give @a mimcontent:jellyfish_ward 60 0 true");
        server.runCommand("gamemode survival @a");
        server.runOnServer(s -> s.getPlayerList().getPlayers().getFirst().setLastHurtByMob(null));
        context.waitTicks(SkorfnaFish.STING_COOLDOWN + 5);
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %.2f %.1f", x + 3.5, floor + 0.1, z - 3.5));
        String warded = waitForSting(context, server, 30);
        log("a survival player under Jellyfish Ward touching a skorfna: " + warded);
        check(warded.contains("poison=none") && !warded.contains("by skorfna"), "a player under Jellyfish Ward should not be stung by a skorfna: " + warded);
        server.runCommand("effect clear @a mimcontent:jellyfish_ward");
        server.runCommand("gamemode creative @a");

        // a mob touching it is stung too (a pig pushed against it), but other fish are not
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x - 8, y + 6, z - 8));
        context.waitTicks(SkorfnaFish.STING_COOLDOWN + 5);
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.2f %.1f {NoAI:1b,PersistenceRequired:1b}", x + 3.5, floor + 0.1, z - 3.5));
        context.waitTicks(10);
        String cod = server.computeOnServer(s -> {
            var found = s.overworld().getEntitiesOfClass(net.minecraft.world.entity.LivingEntity.class, pool,
                e -> BuiltInRegistries.ENTITY_TYPE.getKey(e.getType()).getPath().equals("cod"));
            return found.isEmpty() ? "no cod" : stingState(found.getFirst());
        });
        log("a cod touching a skorfna: " + cod);
        check(cod.contains("poison=none"), "another fish should not be stung: " + cod);
        server.runCommand("kill @e[type=minecraft:cod]");
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:pig %.1f %.2f %.1f {NoAI:1b,PersistenceRequired:1b}", x + 3.5, floor + 0.1, z - 3.5));
        String pig = "";
        for (int t = 0; t < 20 && !pig.contains("by skorfna"); t += 2) {
            context.waitTicks(2);
            pig = server.computeOnServer(s -> {
                var found = s.overworld().getEntitiesOfClass(net.minecraft.world.entity.LivingEntity.class, pool,
                e -> BuiltInRegistries.ENTITY_TYPE.getKey(e.getType()).getPath().equals("pig"));
                return found.isEmpty() ? "no pig" : stingState(found.getFirst());
            });
        }
        log("a pig touching a skorfna: " + pig);
        check(pig.contains("by skorfna") && !pig.contains("poison=none"), "a mob touching a skorfna should be stung: " + pig);
        server.runCommand("kill @e[type=minecraft:pig]");
        server.runCommand("effect clear @a");
        server.runCommand("clear @a");
    }

    /** The night job's twelve fish (2026-11-18, "Night job - the rest of the fish, Claude decides"), in survival order. */
    private static final MimFishes.Fish[] NIGHT = {MimFishes.KAVALL, MimFishes.LIZZ, MimFishes.MARZPAN, MimFishes.TIRD, MimFishes.TRILJA,
        MimFishes.SAWT, MimFishes.PIXXI_SAN_PIETRU, MimFishes.PETRICA, MimFishes.LINGWATA, MimFishes.HMAR, MimFishes.GALLINELLA, MimFishes.LIONFISH};

    /**
     * The night job's twelve fish: each has the health and body box it was given (logged for the owner in
     * docs/Creatures and Plants/Night log/); each bottom fish only spawns over its own kind of floor; the sawt and the
     * petriċa sink to the floor and lie there, and the gallinella keeps close to it; the sawt's and the lionfish's
     * stings (see stingCheck). Their hit box rows are checked against their models in FishHitboxCheck.
     */
    private static void nightFish(ClientGameTestContext context, TestServerContext server, int x, int y, int z, AABB pool) {
        // health, body box width and height
        Map<MimFishes.Fish, double[]> want = Map.ofEntries(
            Map.entry(MimFishes.KAVALL, new double[] {4, 0.5, 0.35}), Map.entry(MimFishes.LIZZ, new double[] {8, 0.7, 0.3}),
            Map.entry(MimFishes.MARZPAN, new double[] {4, 0.5, 0.4}), Map.entry(MimFishes.TIRD, new double[] {3, 0.35, 0.3}),
            Map.entry(MimFishes.TRILJA, new double[] {3, 0.45, 0.3}), Map.entry(MimFishes.SAWT, new double[] {3, 0.35, 0.2}),
            Map.entry(MimFishes.PIXXI_SAN_PIETRU, new double[] {6, 0.6, 0.8}), Map.entry(MimFishes.PETRICA, new double[] {10, 0.9, 0.35}),
            Map.entry(MimFishes.LINGWATA, new double[] {4, 0.6, 0.2}), Map.entry(MimFishes.HMAR, new double[] {6, 0.55, 0.7}),
            Map.entry(MimFishes.GALLINELLA, new double[] {5, 0.6, 0.35}), Map.entry(MimFishes.LIONFISH, new double[] {4, 0.5, 0.55}));
        for (MimFishes.Fish f : NIGHT) {
            double[] w = want.get(f);
            String got = server.computeOnServer(s -> {
                AbstractFish fish = (AbstractFish) f.type().create(s.overworld(), EntitySpawnReason.COMMAND);
                return String.format(Locale.ROOT, "health %.1f, box %.2f x %.2f, speed %.2f%s", fish.getMaxHealth(), fish.getBbWidth(), fish.getBbHeight(),
                    fish.getAttributeValue(Attributes.MOVEMENT_SPEED), fish instanceof BottomFish b ? ", floor " + b.habit().floor() : "");
            });
            String expected = String.format(Locale.ROOT, "health %.1f, box %.2f x %.2f", w[0], w[1], w[2]);
            log(f.id() + ": " + got);
            check(got.startsWith(expected), f.id() + " should have " + expected + ", has " + got);
        }

        // the spawn floor: sand under one spot of the pool, stone under the rest
        server.runCommand(String.format(Locale.ROOT, "setblock %d %d %d minecraft:sand", x + 5, y - 6, z + 5));
        String floors = server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            BlockPos sand = new BlockPos(x + 5, y - 3, z + 5), stone = new BlockPos(x - 5, y - 3, z - 5);
            StringBuilder out = new StringBuilder();
            for (BottomFish.Floor floor : BottomFish.Floor.values()) {
                out.append(floor).append(": sand ").append(BottomFish.floorBelow(floor, level, sand) != null)
                    .append(", stone ").append(BottomFish.floorBelow(floor, level, stone) != null).append("; ");
            }
            // the full rule: the pool is above sea level here, so a natural spawn is refused; a spawner is not
            out.append("rule above sea level: natural ").append(BottomFish.checkSpawnRules(BottomFish.Floor.SOFT, level, EntitySpawnReason.NATURAL, sand))
                .append(", spawner ").append(BottomFish.checkSpawnRules(BottomFish.Floor.SOFT, level, EntitySpawnReason.SPAWNER, sand));
            return out.toString();
        });
        log("night fish spawn floors: " + floors);
        check(floors.equals("SOFT: sand true, stone false; ROCK: sand false, stone true; ANY: sand true, stone true; "
            + "rule above sea level: natural false, spawner true"), "the bottom fish's spawn floors are off: " + floors);
        String habits = server.computeOnServer(s -> {
            StringBuilder out = new StringBuilder();
            for (MimFishes.Fish f : NIGHT) {
                if (f.type().create(s.overworld(), EntitySpawnReason.COMMAND) instanceof BottomFish b) {
                    out.append(f.id()).append('=').append(b.habit().floor()).append(' ');
                }
            }
            return out.toString().trim();
        });
        log("night fish floors: " + habits);
        check(habits.equals("marzpan=ROCK tird=ANY trilja=SOFT sawt=SOFT petrica=SOFT lingwata=SOFT hmar=ROCK gallinella=SOFT lionfish=ROCK"),
            "the night fish's floors: " + habits);
        server.runCommand(String.format(Locale.ROOT, "setblock %d %d %d minecraft:stone", x + 5, y - 6, z + 5));

        // near the floor: summoned 3.5 blocks above it, with a spectator far off so the shy ones don't flee
        server.runCommand("gamemode spectator @a");
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x - 8, y + 6, z - 8));
        MimFishes.Fish[] low = {MimFishes.SAWT, MimFishes.PETRICA, MimFishes.GALLINELLA};
        for (int i = 0; i < low.length; i++) {
            server.runCommand(String.format(Locale.ROOT, "summon mimcontent:%s %.1f %.1f %.1f {PersistenceRequired:1b}", low[i].id(), x - 3.5 + 4 * i, y - 1.5, z + 0.5));
        }
        double floor = y - 5;
        context.waitTicks(160);
        int samples = 20;
        double[] highest = new double[low.length], sum = new double[low.length];
        int[] rests = new int[low.length];
        for (int t = 0; t < samples; t++) {
            context.waitTicks(10);
            double[][] h = server.computeOnServer(s -> {
                double[][] out = new double[low.length][];
                for (int i = 0; i < low.length; i++) {
                    BottomFish fish = (BottomFish) s.overworld().getEntities(low[i].type(), pool, e -> true).getFirst();
                    out[i] = new double[] {fish.getY() - floor, fish.isResting() ? 1 : 0};
                }
                return out;
            });
            for (int i = 0; i < low.length; i++) {
                highest[i] = Math.max(highest[i], h[i][0]);
                sum[i] += h[i][0];
                rests[i] += (int) h[i][1];
            }
        }
        for (int i = 0; i < low.length; i++) {
            log(String.format(Locale.ROOT, "%s summoned 3.5 blocks above the floor: after 8 s, over 10 s at most %.2f above it (on average %.2f); resting in %d of %d",
                low[i].id(), highest[i], sum[i] / samples, rests[i], samples));
        }
        for (int i = 0; i < 2; i++) {
            check(highest[i] <= 0.6 && sum[i] / samples <= 0.3 && rests[i] >= samples / 2, String.format(Locale.ROOT,
                "the %s should lie on the bottom: at most %.2f above it, average %.2f, resting %d of %d", low[i].id(), highest[i], sum[i] / samples, rests[i], samples));
        }
        check(highest[2] <= 1.5 && sum[2] / samples <= 1.0, String.format(Locale.ROOT,
            "the gallinella should keep near the bottom: at most %.2f above it, average %.2f", highest[2], sum[2] / samples));
        server.runCommand("kill @e[type=!minecraft:player]");
        server.runCommand("gamemode creative @a");

        stingCheck(context, server, x, y, z, pool, MimFishes.SAWT);
        server.runCommand("kill @e[type=!minecraft:player]");
        stingCheck(context, server, x, y, z, pool, MimFishes.LIONFISH);
        server.runCommand("kill @e[type=!minecraft:player]");
    }

    /**
     * A venomous night fish (the sawt, the lionfish): hit it in melee and it stings the attacker (1 heart and Poison
     * for 6 seconds); a survival player standing on it is stung; a creative player, or one under Jellyfish Ward, is
     * not; a mob touching it (a pig) is stung; another fish (a cod) is not.
     */
    private static void stingCheck(ClientGameTestContext context, TestServerContext server, int x, int y, int z, AABB pool, MimFishes.Fish f) {
        String id = f.id();
        BottomFish.Sting sting = server.computeOnServer(s -> ((BottomFish) f.type().create(s.overworld(), EntitySpawnReason.COMMAND)).habit().sting());
        check(sting != null && sting.damage() == 2.0F && sting.poisonSeconds() == 6, id + " should sting for 1 heart and 6 s of poison: " + sting);
        double floor = y - 5;
        server.runCommand("clear @a");
        server.runCommand("effect clear @a");
        server.runCommand("gamemode survival @a");
        server.runCommand("effect give @a minecraft:water_breathing 120 0 true");
        // hit it in melee, from beside it
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:%s %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b}", id, x + 0.5, floor, z + 0.5));
        server.runCommand(String.format(Locale.ROOT, "tp @a %.2f %.2f %.2f", x + 2.0, floor, z + 0.5));
        context.waitTicks(5);
        String hit = server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
            player.setHealth(player.getMaxHealth());
            player.setLastHurtByMob(null);
            player.removeEffect(net.minecraft.world.effect.MobEffects.POISON);
            // a living one: the last one killed may still lie there in its death animation
            AbstractFish fish = level.getEntities(f.type(), pool, e -> e.isAlive()).getFirst();
            float before = fish.getHealth();
            boolean hurt = fish.hurtServer(level, level.damageSources().playerAttack(player), 1.0F);
            return stingState(player) + String.format(Locale.ROOT, " (the hit %s: %s health %.1f -> %.1f, can be stung %s)",
                hurt ? "counted" : "did not count", id, before, fish.getHealth(),
                com.maltaminecraft.mimcontent.entity.fish.Venom.canSting(player));
        });
        log("hit the " + id + " in melee: " + hit);
        check(hit.contains("poison=" + sting.poisonSeconds() * 20) && hit.contains("by " + id) && !hit.startsWith("health 20.0"),
            "a " + id + " hit in melee should sting the attacker (2 damage and poison): " + hit);

        // a survival player standing on one lying on the floor is stung
        server.runCommand("kill @e[type=mimcontent:" + id + "]");
        server.runCommand("effect clear @a minecraft:poison");
        // past the player's hurt cooldown from the sting above (else the next sting's damage doesn't count)
        context.waitTicks(25);
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:%s %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b}", id, x + 3.5, floor, z - 3.5));
        server.runOnServer(s -> {
            ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
            player.setHealth(player.getMaxHealth());
            player.setLastHurtByMob(null);
        });
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %.2f %.1f", x + 3.5, floor + 0.1, z - 3.5));
        String touched = waitForSting(context, server, 20);
        log("a survival player standing on a " + id + ": " + touched);
        check(touched.contains("poison=") && !touched.contains("poison=none") && touched.contains("by " + id),
            "a survival player standing on a " + id + " should be stung: " + touched);

        // then a creative one is not
        server.runCommand("effect clear @a minecraft:poison");
        server.runCommand("gamemode creative @a");
        server.runOnServer(s -> s.getPlayerList().getPlayers().getFirst().setLastHurtByMob(null));
        context.waitTicks(sting.cooldown() + 5);
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %.2f %.1f", x + 3.5, floor + 0.1, z - 3.5));
        String creative = waitForSting(context, server, 30);
        log("a creative player standing on a " + id + ": " + creative);
        check(creative.contains("poison=none") && !creative.contains("by " + id), "a creative player should not be stung by a " + id + ": " + creative);

        // nor a survival player under Jellyfish Ward (Venom.canSting: the Ward blocks every sting)
        server.runCommand("effect give @a mimcontent:jellyfish_ward 60 0 true");
        server.runCommand("gamemode survival @a");
        server.runOnServer(s -> s.getPlayerList().getPlayers().getFirst().setLastHurtByMob(null));
        context.waitTicks(sting.cooldown() + 5);
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %.2f %.1f", x + 3.5, floor + 0.1, z - 3.5));
        String warded = waitForSting(context, server, 30);
        log("a survival player under Jellyfish Ward standing on a " + id + ": " + warded);
        check(warded.contains("poison=none") && !warded.contains("by " + id), "a player under Jellyfish Ward should not be stung by a " + id + ": " + warded);
        server.runCommand("effect clear @a mimcontent:jellyfish_ward");
        server.runCommand("gamemode creative @a");

        // a mob touching it is stung (a pig pushed against it), another fish is not
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x - 8, y + 6, z - 8));
        context.waitTicks(sting.cooldown() + 5);
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.2f %.1f {NoAI:1b,PersistenceRequired:1b}", x + 3.5, floor + 0.1, z - 3.5));
        context.waitTicks(10);
        String cod = server.computeOnServer(s -> {
            var found = s.overworld().getEntitiesOfClass(net.minecraft.world.entity.LivingEntity.class, pool,
                e -> BuiltInRegistries.ENTITY_TYPE.getKey(e.getType()).getPath().equals("cod"));
            return found.isEmpty() ? "no cod" : stingState(found.getFirst());
        });
        log("a cod touching a " + id + ": " + cod);
        check(cod.contains("poison=none"), "another fish should not be stung by a " + id + ": " + cod);
        server.runCommand("kill @e[type=minecraft:cod]");
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:pig %.1f %.2f %.1f {NoAI:1b,PersistenceRequired:1b}", x + 3.5, floor + 0.1, z - 3.5));
        String pig = "";
        for (int t = 0; t < 20 && !pig.contains("by " + id); t += 2) {
            context.waitTicks(2);
            pig = server.computeOnServer(s -> {
                var found = s.overworld().getEntitiesOfClass(net.minecraft.world.entity.LivingEntity.class, pool,
                    e -> BuiltInRegistries.ENTITY_TYPE.getKey(e.getType()).getPath().equals("pig"));
                return found.isEmpty() ? "no pig" : stingState(found.getFirst());
            });
        }
        log("a pig touching a " + id + ": " + pig);
        check(pig.contains("by " + id) && !pig.contains("poison=none"), "a mob touching a " + id + " should be stung: " + pig);
        server.runCommand("kill @e[type=minecraft:pig]");
        server.runCommand("effect clear @a");
        server.runCommand("clear @a");
    }

    /**
     * A placeholder fish's review shots, for the art makers to extend (like the cerna's): one alone in a small tank seen
     * side on, three-quarter and from above, one beside a vanilla cod, and one on land. Names: fish-&lt;id&gt;-side,
     * -three-quarter, -top, -beside-cod, -on-land.
     */
    private static void placeholderShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z, String id) {
        // go there first, so the chunks are loaded before the tank is built
        server.runCommand("gamemode creative @a");
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x, y + 3, z - 4));
        world.getConnection().waitForChunksRender();
        fill(server, x - 7, y, z - 6, x + 7, y + 12, z + 10, "minecraft:air");
        fill(server, x - 7, y - 1, z - 6, x + 7, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 5, y, z + 4, x + 5, y + 5, z + 9, "minecraft:glass");
        fill(server, x - 4, y, z + 5, x + 4, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:%s %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            id, x + 0.5, y + 1.5, z + 6.2));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.9, y + 1.6, z + 6.2));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:%s %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            id, x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall, so no glass frames cross the fish; in spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.5, y + 0.2, z + 4.3, x + 0.5, y + 1.85, z + 6.2, "fish-" + id + "-side");
        look(context, server, x - 1.0, y + 0.6, z + 4.6, x + 0.3, y + 1.85, z + 6.2, "fish-" + id + "-three-quarter");
        look(context, server, x + 0.5, y + 1.6, z + 4.7, x + 0.5, y + 1.85, z + 6.2, "fish-" + id + "-top");
        look(context, server, x - 0.6, y + 0.2, z + 4.3, x - 0.6, y + 1.85, z + 6.2, "fish-" + id + "-beside-cod");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y, z - 1.3, x + 0.5, y + 0.2, z + 0.5, "fish-" + id + "-on-land");
    }

    /** The lizz's size review: in one tank, left to right as the camera sees them, a lizz, the cerna, a small (2 block) tonn and a vanilla cod. */
    private static void lizzSizeShot(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        server.runCommand("gamemode creative @a");
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x, y + 3, z - 4));
        world.getConnection().waitForChunksRender();
        int fz = z + 6;
        fill(server, x - 14, y, z - 10, x + 12, y + 10, z + 10, "minecraft:air");
        fill(server, x - 14, y - 1, z - 10, x + 12, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 10, y, fz - 2, x + 6, y + 3, fz + 2, "minecraft:glass");
        fill(server, x - 10, y, fz - 2, x + 6, y + 3, fz - 2, "minecraft:barrier");
        fill(server, x - 9, y, fz - 1, x + 5, y + 3, fz + 1, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:lizz %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 2.5, y + 1.5, fz + 0.5));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:cerna %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 0.2, y + 1.2, fz + 0.5));
        server.runOnServer(s -> {
            TonnFish fish = (TonnFish) MimFishes.TONN.type().create(s.overworld(), EntitySpawnReason.COMMAND);
            fish.snapTo(x - 3.3, y + 1.2, fz + 0.5, 90.0F, 0.0F);
            fish.setYHeadRot(90.0F);
            fish.setYBodyRot(90.0F);
            fish.setNoAi(true);
            fish.setPersistenceRequired();
            fish.setLength(2.0F);
            s.overworld().addFreshEntity(fish);
        });
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 5.8, y + 1.5, fz + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        server.runCommand("gamemode spectator @a");
        look(context, server, x - 1.5, y + 0.0, fz - 5.0, x - 1.5, y + 1.6, fz + 0.5, "fish-lizz-beside-cerna-tonn");
        server.runCommand("gamemode creative @a");
    }

    /** The marzpan's size review: in one tank, left to right as the camera sees them, a marzpan, a vanilla cod, the cerna and a small (2 block) tonn. */
    private static void marzpanSizeShot(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        server.runCommand("gamemode creative @a");
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x, y + 3, z - 4));
        world.getConnection().waitForChunksRender();
        int fz = z + 6;
        fill(server, x - 14, y, z - 10, x + 12, y + 10, z + 10, "minecraft:air");
        fill(server, x - 14, y - 1, z - 10, x + 12, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 10, y, fz - 2, x + 6, y + 3, fz + 2, "minecraft:glass");
        fill(server, x - 10, y, fz - 2, x + 6, y + 3, fz - 2, "minecraft:barrier");
        fill(server, x - 9, y, fz - 1, x + 5, y + 3, fz + 1, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:marzpan %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 1.5, y + 1.5, fz + 0.5));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.3, y + 1.5, fz + 0.5));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:cerna %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.6, y + 1.2, fz + 0.5));
        server.runOnServer(s -> {
            TonnFish fish = (TonnFish) MimFishes.TONN.type().create(s.overworld(), EntitySpawnReason.COMMAND);
            fish.snapTo(x - 4.2, y + 1.2, fz + 0.5, 90.0F, 0.0F);
            fish.setYHeadRot(90.0F);
            fish.setYBodyRot(90.0F);
            fish.setNoAi(true);
            fish.setPersistenceRequired();
            fish.setLength(2.0F);
            s.overworld().addFreshEntity(fish);
        });
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        server.runCommand("gamemode spectator @a");
        look(context, server, x - 1.2, y + 0.3, z + 1.0, x - 1.2, y + 1.6, fz + 0.5, "fish-marzpan-lineup");
        server.runCommand("gamemode creative @a");
    }

    /** The kavall's size review: in one tank, left to right as the camera sees them, a kavall, a vanilla cod, the cerna and a small (2 block) tonn. */
    /** The tird's size review: in one tank, left to right as the camera sees them, a tird, a vanilla cod, the cerna and a small (2 block) tonn. */
    private static void tirdSizeShot(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        server.runCommand("gamemode creative @a");
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x, y + 3, z - 4));
        world.getConnection().waitForChunksRender();
        int fz = z + 6;
        fill(server, x - 14, y, z - 10, x + 12, y + 10, z + 10, "minecraft:air");
        fill(server, x - 14, y - 1, z - 10, x + 12, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 10, y, fz - 2, x + 6, y + 3, fz + 2, "minecraft:glass");
        fill(server, x - 10, y, fz - 2, x + 6, y + 3, fz - 2, "minecraft:barrier");
        fill(server, x - 9, y, fz - 1, x + 5, y + 3, fz + 1, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:tird %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 1.5, y + 1.5, fz + 0.5));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.3, y + 1.5, fz + 0.5));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:cerna %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.6, y + 1.2, fz + 0.5));
        server.runOnServer(s -> {
            TonnFish fish = (TonnFish) MimFishes.TONN.type().create(s.overworld(), EntitySpawnReason.COMMAND);
            fish.snapTo(x - 4.2, y + 1.2, fz + 0.5, 90.0F, 0.0F);
            fish.setYHeadRot(90.0F);
            fish.setYBodyRot(90.0F);
            fish.setNoAi(true);
            fish.setPersistenceRequired();
            fish.setLength(2.0F);
            s.overworld().addFreshEntity(fish);
        });
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        server.runCommand("gamemode spectator @a");
        look(context, server, x - 1.2, y + 0.3, z + 1.0, x - 1.2, y + 1.6, fz + 0.5, "fish-tird-lineup");
        server.runCommand("gamemode creative @a");
    }

    private static void kavallSizeShot(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        server.runCommand("gamemode creative @a");
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x, y + 3, z - 4));
        world.getConnection().waitForChunksRender();
        int fz = z + 6;
        fill(server, x - 14, y, z - 10, x + 12, y + 10, z + 10, "minecraft:air");
        fill(server, x - 14, y - 1, z - 10, x + 12, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 10, y, fz - 2, x + 6, y + 3, fz + 2, "minecraft:glass");
        fill(server, x - 10, y, fz - 2, x + 6, y + 3, fz - 2, "minecraft:barrier");
        fill(server, x - 9, y, fz - 1, x + 5, y + 3, fz + 1, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:kavall %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 1.5, y + 1.5, fz + 0.5));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.3, y + 1.5, fz + 0.5));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:cerna %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.6, y + 1.2, fz + 0.5));
        server.runOnServer(s -> {
            TonnFish fish = (TonnFish) MimFishes.TONN.type().create(s.overworld(), EntitySpawnReason.COMMAND);
            fish.snapTo(x - 4.2, y + 1.2, fz + 0.5, 90.0F, 0.0F);
            fish.setYHeadRot(90.0F);
            fish.setYBodyRot(90.0F);
            fish.setNoAi(true);
            fish.setPersistenceRequired();
            fish.setLength(2.0F);
            s.overworld().addFreshEntity(fish);
        });
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        server.runCommand("gamemode spectator @a");
        look(context, server, x - 1.2, y + 0.3, z + 1.0, x - 1.2, y + 1.6, fz + 0.5, "fish-kavall-lineup");
        server.runCommand("gamemode creative @a");
    }

    private static String waitForSting(ClientGameTestContext context, TestServerContext server, int ticks) {
        String state = "";
        for (int t = 0; t < ticks; t += 2) {
            context.waitTicks(2);
            state = server.computeOnServer(s -> stingState(s.getPlayerList().getPlayers().getFirst()));
            if (!state.contains("poison=none")) {
                break;
            }
        }
        return state;
    }

    private static String stingState(net.minecraft.world.entity.LivingEntity player) {
        var poison = player.getEffect(net.minecraft.world.effect.MobEffects.POISON);
        var by = player.getLastHurtByMob();
        return String.format(Locale.ROOT, "health %.1f, poison=%s, hurt %s", player.getHealth(), poison == null ? "none" : poison.getDuration() + "",
            by == null ? "by nothing" : "by " + BuiltInRegistries.ENTITY_TYPE.getKey(by.getType()).getPath());
    }

    /** Waits up to the given ticks until the shark's state starts with the prefix; returns the last state. */
    private static String waitForShark(ClientGameTestContext context, TestServerContext server, AABB pool, String prefix, int ticks) {
        String state = sharkState(server, pool);
        for (int t = 0; t < ticks && !state.startsWith(prefix); t += 5) {
            context.waitTicks(5);
            state = sharkState(server, pool);
        }
        return state;
    }

    private static String sharkState(TestServerContext server, AABB pool) {
        return server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            List<? extends AbstractFish> sharks = level.getEntities(MimFishes.HUTA_KAHLA.type(), pool, e -> true);
            if (sharks.size() != 1) {
                return "found " + sharks.size() + " sharks";
            }
            HutaKahlaFish shark = (HutaKahlaFish) sharks.getFirst();
            String target = shark.getTarget() == null ? "none" : shark.getTarget() instanceof ServerPlayer ? "player" : shark.getTarget().getType().toString();
            return String.format(Locale.ROOT, "target=%s angry=%s bait=%s", target, shark.isAngry(), shark.isChasingBait());
        });
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
        // each fish's own shots; a shot added here also goes in ownShots, so SMOKE_ONLY=fish-one takes it too
        lampukaShots(context, server, world, x + 30, y, z);
        tonnShots(context, server, world, x - 30, y, z);
        sardinaShots(context, server, world, x + 30, y, z + 25);
        cernaShots(context, server, world, x - 30, y, z + 50);
        ziemelShots(context, server, world, x + 30, y, z + 75);
        pixxispadShots(context, server, world, x - 30, y, z + 75);
        awrataShots(context, server, world, x + 30, y, z + 50);
        murinaShots(context, server, world, x, y, z + 100);
        incovaShots(context, server, world, x + 30, y, z + 125);
        cawlShots(context, server, world, x - 30, y, z + 125);
        hutaKahlaShots(context, server, world, x - 30, y, z + 150);
        bollShots(context, server, world, x + 30, y, z + 150);
        skorfnaShots(context, server, world, x, y, z + 150);
        molaShots(context, server, world, x, y, z + 185);
        // the night job's twelve (placeholder art): three tanks to a row, from z + 225
        for (int i = 0; i < NIGHT.length; i++) {
            placeholderShots(context, server, world, x - 30 + 30 * (i % 3), y, z + 225 + 25 * (i / 3), NIGHT[i].id());
        }
        lizzSizeShot(context, server, world, x + 90, y, z + 250);
        marzpanSizeShot(context, server, world, x + 90, y, z + 285);
        kavallSizeShot(context, server, world, x + 90, y, z + 320);
        tirdSizeShot(context, server, world, x + 130, y, z + 250);

        // the hotbar: the caught fish beside vanilla's, then the buckets, then the spawn eggs
        String[][] bars = {
            {"minecraft:cod", "minecraft:salmon", "mimcontent:lampuka", "mimcontent:tonn", "mimcontent:sardina", "mimcontent:cerna",
                "mimcontent:awrata", "mimcontent:murina", "minecraft:tropical_fish"},
            {"minecraft:cod_bucket", "mimcontent:lampuka_bucket", "mimcontent:tonn_bucket", "mimcontent:sardina_bucket", "mimcontent:cerna_bucket",
                "mimcontent:awrata_bucket", "mimcontent:murina_bucket", "mimcontent:ziemel_bucket", "minecraft:salmon_bucket"},
            {"minecraft:cod_spawn_egg", "mimcontent:lampuka_spawn_egg", "mimcontent:tonn_spawn_egg", "mimcontent:sardina_spawn_egg",
                "mimcontent:cerna_spawn_egg", "mimcontent:awrata_spawn_egg", "mimcontent:murina_spawn_egg", "mimcontent:ziemel_spawn_egg",
                "minecraft:salmon_spawn_egg"},
            {"minecraft:cod", "mimcontent:pixxispad", "minecraft:cod_bucket", "mimcontent:pixxispad_bucket", "minecraft:cod_spawn_egg",
                "mimcontent:pixxispad_spawn_egg", "mimcontent:tonn", "mimcontent:tonn_bucket", "mimcontent:tonn_spawn_egg"},
            {"minecraft:cod", "mimcontent:boll", "minecraft:cod_bucket", "mimcontent:boll_bucket", "minecraft:cod_spawn_egg",
                "mimcontent:boll_spawn_egg", "mimcontent:huta_kahla", "mimcontent:huta_kahla_bucket", "mimcontent:huta_kahla_spawn_egg"},
            {"minecraft:cod", "mimcontent:skorfna", "minecraft:cod_bucket", "mimcontent:skorfna_bucket", "minecraft:cod_spawn_egg",
                "mimcontent:skorfna_spawn_egg", "minecraft:pufferfish", "minecraft:pufferfish_bucket", "minecraft:pufferfish_spawn_egg"},
            // the mola mola's placeholder item, bucket and egg (its icons wait for the owner's OK on the model)
            {"minecraft:cod", "mimcontent:mola_mola", "minecraft:cod_bucket", "mimcontent:mola_mola_bucket", "minecraft:cod_spawn_egg",
                "mimcontent:mola_mola_spawn_egg", "mimcontent:tonn", "mimcontent:tonn_bucket", "mimcontent:tonn_spawn_egg"},
            // the two skorfna items, black and red, beside vanilla's fish and the accepted ones
            {"minecraft:cod", "mimcontent:skorfna", "mimcontent:skorfna_red", "minecraft:salmon", "mimcontent:cerna",
                "mimcontent:awrata", "minecraft:pufferfish", "mimcontent:lampuka", "minecraft:tropical_fish"},
            // the night job's twelve (placeholder icons, buckets and eggs), each row beside vanilla's cod
            {"minecraft:cod", "mimcontent:kavall", "mimcontent:lizz", "mimcontent:marzpan", "mimcontent:tird", "mimcontent:trilja",
                "mimcontent:sawt", "mimcontent:pixxi_san_pietru", "mimcontent:petrica"},
            {"minecraft:cod", "mimcontent:lingwata", "mimcontent:hmar", "mimcontent:gallinella", "mimcontent:lionfish", "minecraft:salmon",
                "minecraft:pufferfish", "minecraft:tropical_fish", "mimcontent:skorfna"},
            {"minecraft:cod_bucket", "mimcontent:kavall_bucket", "mimcontent:lizz_bucket", "mimcontent:marzpan_bucket", "mimcontent:tird_bucket",
                "mimcontent:trilja_bucket", "mimcontent:sawt_bucket", "mimcontent:pixxi_san_pietru_bucket", "mimcontent:petrica_bucket"},
            {"minecraft:cod_bucket", "mimcontent:lingwata_bucket", "mimcontent:hmar_bucket", "mimcontent:gallinella_bucket", "mimcontent:lionfish_bucket",
                "minecraft:salmon_bucket", "minecraft:pufferfish_bucket", "minecraft:tropical_fish_bucket", "mimcontent:skorfna_bucket"},
            {"minecraft:cod_spawn_egg", "mimcontent:kavall_spawn_egg", "mimcontent:lizz_spawn_egg", "mimcontent:marzpan_spawn_egg",
                "mimcontent:tird_spawn_egg", "mimcontent:trilja_spawn_egg", "mimcontent:sawt_spawn_egg", "mimcontent:pixxi_san_pietru_spawn_egg",
                "mimcontent:petrica_spawn_egg"},
            {"minecraft:cod_spawn_egg", "mimcontent:lingwata_spawn_egg", "mimcontent:hmar_spawn_egg", "mimcontent:gallinella_spawn_egg",
                "mimcontent:lionfish_spawn_egg", "minecraft:salmon_spawn_egg", "minecraft:pufferfish_spawn_egg", "minecraft:tropical_fish_spawn_egg",
                "mimcontent:skorfna_spawn_egg"},
        };
        String[] names = {"fish-07-hotbar-items", "fish-08-hotbar-buckets", "fish-09-hotbar-eggs", "fish-10-hotbar-pixxispad", "fish-11-hotbar-boll",
            "fish-12-hotbar-skorfna", "fish-14-hotbar-mola", "fish-13-hotbar-skorfna-items", "fish-15-hotbar-night-items-1", "fish-15-hotbar-night-items-2",
            "fish-16-hotbar-night-buckets-1", "fish-16-hotbar-night-buckets-2", "fish-17-hotbar-night-eggs-1", "fish-17-hotbar-night-eggs-2"};
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

    /**
     * The skorfna's two versions (owner 2026-11-18, "Skorfna - two versions, red and black, as reskins"), in a world of
     * its own: the spawn split; /summon and the spawn egg give a random version, /summon with Variant gives that one,
     * one with no saved version is black; the client sees each fish's version and draws it with its own texture (both
     * textures exist); the bucket keeps the version and its tooltip names it; and every version survives a save and
     * reload. Then the review shot fish-skorfna-variants: a black and a red one side by side.
     */
    private static void skorfnaVariants(ClientGameTestContext context) {
        // the spawn split, drawn 4000 times each way
        net.minecraft.util.RandomSource random = net.minecraft.util.RandomSource.create(1234L);
        int deepRed = 0, elsewhereRed = 0, draws = 4000;
        for (int i = 0; i < draws; i++) {
            deepRed += SkorfnaFish.pickVariant(random, true) == SkorfnaFish.Variant.RED ? 1 : 0;
            elsewhereRed += SkorfnaFish.pickVariant(random, false) == SkorfnaFish.Variant.RED ? 1 : 0;
        }
        float deepShare = deepRed / (float) draws, elsewhereShare = elsewhereRed / (float) draws;
        log(String.format(Locale.ROOT, "skorfna variants: red %.1f%% in the deep-sea biomes (want %.0f%%), %.1f%% elsewhere (want %.0f%%)",
            deepShare * 100, SkorfnaFish.RED_CHANCE_DEEP * 100, elsewhereShare * 100, SkorfnaFish.RED_CHANCE_ELSEWHERE * 100));
        check(Math.abs(deepShare - SkorfnaFish.RED_CHANCE_DEEP) < 0.03F && Math.abs(elsewhereShare - SkorfnaFish.RED_CHANCE_ELSEWHERE) < 0.03F,
            "the skorfna spawn split is off");

        TestWorldSave save;
        Map<UUID, SkorfnaFish.Variant> variants = new HashMap<>();
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

            // 20 by /summon and 10 from the spawn egg, all random
            for (int i = 0; i < 20; i++) {
                server.runCommand(String.format(Locale.ROOT, "summon mimcontent:skorfna %.1f %d %.1f", x - 9.5 + i, y - 4, z - 6.5));
            }
            for (int i = 0; i < 10; i++) {
                int fx = x - 9 + 2 * i;
                server.runOnServer(s -> {
                    ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                    player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(MimFishes.SKORFNA.spawnEgg()));
                    BlockPos floor = BlockPos.containing(fx, y - 8, z - 2);
                    player.getItemInHand(InteractionHand.MAIN_HAND).useOn(new UseOnContext(player, InteractionHand.MAIN_HAND,
                        new BlockHitResult(Vec3.atCenterOf(floor).add(0, 0.5, 0), Direction.UP, floor, false)));
                });
            }
            context.waitTicks(2);
            Map<UUID, SkorfnaFish.Variant> random30 = skorfnaVariantsIn(server, pool);
            long reds = random30.values().stream().filter(v -> v == SkorfnaFish.Variant.RED).count();
            log("summon and spawn egg: " + random30.size() + " skorfna, " + reds + " red, " + (random30.size() - reds) + " black");
            check(random30.size() == 30, "expected 30 skorfna, found " + random30.size());
            check(reds > 0 && reds < 30, "summon and the spawn egg should give both versions, got " + reds + " red of 30");

            // /summon with the version in its data; one with no saved version (as saved before versions existed) is black
            server.runCommand(String.format(Locale.ROOT, "summon mimcontent:skorfna %.1f %d %.1f {PersistenceRequired:1b,Variant:\"red\"}", x + 0.5, y - 4, z + 3.5));
            server.runCommand(String.format(Locale.ROOT, "summon mimcontent:skorfna %.1f %d %.1f {PersistenceRequired:1b,Variant:\"black\"}", x + 0.5, y - 4, z + 5.5));
            server.runCommand(String.format(Locale.ROOT, "summon mimcontent:skorfna %.1f %d %.1f {PersistenceRequired:1b}", x + 0.5, y - 4, z + 7.5));
            context.waitTicks(2);
            String summoned = server.computeOnServer(s -> {
                StringBuilder out = new StringBuilder();
                for (double sz : new double[] {3.5, 5.5, 7.5}) {
                    List<SkorfnaFish> here = skorfnas(s.overworld(), new AABB(x, y - 9, z + sz - 0.9, x + 1, y, z + sz + 0.9));
                    out.append(here.size() == 1 ? here.getFirst().getVariant().id() : "found " + here.size()).append(' ');
                }
                return out.toString().trim();
            });
            log("summon with Variant red, Variant black, no Variant: " + summoned);
            check(summoned.equals("red black black"), "summoned with data: " + summoned);
            server.runOnServer(s -> s.overworld().getEntities(MimFishes.SKORFNA.type(), pool, e -> true).forEach(e -> e.setPersistenceRequired()));
            Map<UUID, SkorfnaFish.Variant> found = skorfnaVariantsIn(server, pool);

            // the client: same version for each fish, drawn with its own texture, and both textures exist
            context.waitTicks(10);
            String client = context.computeOnClient(mc -> {
                for (String tex : new String[] {"skorfna", "skorfna_red"}) {
                    if (mc.getResourceManager().getResource(com.maltaminecraft.mimcontent.MimContent.id("textures/entity/fish/" + tex + ".png")).isEmpty()) {
                        return "missing texture " + tex + ".png";
                    }
                }
                int seen = 0;
                for (Entity e : mc.level.entitiesForRendering()) {
                    if (e instanceof SkorfnaFish fish && found.containsKey(e.getUUID())) {
                        if (fish.getVariant() != found.get(e.getUUID())) {
                            return "the client sees a " + fish.getVariant().id() + " skorfna that is " + found.get(e.getUUID()).id();
                        }
                        String tex = ((com.maltaminecraft.mimcontent.client.fish.FishRenderer) (Object) mc.getEntityRenderDispatcher().getRenderer(e))
                            .textureFor(fish).getPath();
                        String want = fish.getVariant() == SkorfnaFish.Variant.RED ? "textures/entity/fish/skorfna_red.png" : "textures/entity/fish/skorfna.png";
                        if (!tex.equals(want)) {
                            return "a " + fish.getVariant().id() + " skorfna is drawn with " + tex;
                        }
                        seen++;
                    }
                }
                return seen == found.size() ? "ok, " + seen + " fish, both textures found" : "the client sees " + seen + " of " + found.size() + " skorfna";
            });
            log("client sync and textures: " + client);
            check(client.startsWith("ok"), "client: " + client);

            // the bucket keeps the version: catch a red and a black one, read the bucket and its tooltip, let them out
            server.runCommand("gamemode survival @a");
            for (SkorfnaFish.Variant variant : SkorfnaFish.Variant.values()) {
                UUID id = found.entrySet().stream().filter(e -> e.getValue() == variant).findFirst().orElseThrow().getKey();
                String bucket = server.computeOnServer(s -> {
                    ServerLevel level = s.overworld();
                    ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                    SkorfnaFish fish = (SkorfnaFish) level.getEntity(id);
                    player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.WATER_BUCKET));
                    fish.interact(player, InteractionHand.MAIN_HAND, fish.position());
                    ItemStack held = player.getItemInHand(InteractionHand.MAIN_HAND);
                    if (!held.is(MimFishes.SKORFNA.bucket())) {
                        return "bucketing gave " + BuiltInRegistries.ITEM.getKey(held.getItem());
                    }
                    String stored = held.getOrDefault(DataComponents.BUCKET_ENTITY_DATA, CustomData.EMPTY).copyTag().getStringOr("Variant", "none");
                    player.getInventory().setItem(8, held.copy());
                    BlockPos out = BlockPos.containing(x + 6.5, y - 4, z + 6.5);
                    ((MobBucketItem) held.getItem()).checkExtraContent(player, level, held, out);
                    List<SkorfnaFish> back = skorfnas(level, new AABB(out).inflate(2.0)).stream().filter(SkorfnaFish::fromBucket).toList();
                    if (back.size() != 1) {
                        return "emptying the bucket gave " + back.size() + " skorfna";
                    }
                    SkorfnaFish released = back.getFirst();
                    released.discard();
                    return "caught " + variant.id() + ", bucket says " + stored + ", let out " + released.getVariant().id()
                        + (stored.equals(variant.id()) && released.getVariant() == variant ? " ok" : " WRONG");
                });
                context.waitTicks(5);
                String tooltip = context.computeOnClient(mc -> {
                    ItemStack stack = mc.player.getInventory().getItem(8);
                    List<net.minecraft.network.chat.Component> lines = stack.getTooltipLines(net.minecraft.world.item.Item.TooltipContext.of(mc.level),
                        mc.player, net.minecraft.world.item.TooltipFlag.NORMAL);
                    return String.join(" / ", lines.stream().map(net.minecraft.network.chat.Component::getString).toList());
                });
                String word = variant == SkorfnaFish.Variant.RED ? "Red" : "Black";
                log("bucket: " + bucket + "; tooltip: " + tooltip);
                check(bucket.endsWith(" ok"), "the bucket lost the version: " + bucket);
                check(tooltip.contains(" / " + word), "the bucket tooltip should say " + word + ": " + tooltip);
                server.runCommand("clear @a");
            }
            // an old bucket (filled before versions existed) holds a black one
            String old = server.computeOnServer(s -> {
                ServerLevel level = s.overworld();
                ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                ItemStack held = new ItemStack(MimFishes.SKORFNA.bucket());
                BlockPos out = BlockPos.containing(x - 6.5, y - 4, z + 6.5);
                ((MobBucketItem) held.getItem()).checkExtraContent(player, level, held, out);
                List<SkorfnaFish> back = skorfnas(level, new AABB(out).inflate(2.0));
                String v = back.size() == 1 ? back.getFirst().getVariant().id() : "found " + back.size();
                back.forEach(Entity::discard);
                return v;
            });
            log("an old bucket with no version lets out: " + old);
            check(old.equals("black"), "an old bucket should hold a black skorfna, gave " + old);
            server.runCommand("gamemode creative @a");
            context.waitTicks(2);
            variants.putAll(skorfnaVariantsIn(server, pool));
            check(variants.size() == 31, "before saving (two caught and let out, then removed), expected 31 skorfna, found " + variants.size());
        }

        // save and reload: every skorfna comes back the same version
        try (TestSingleplayerContext world = save.open()) {
            world.getConnection().waitForChunksRender();
            context.waitTicks(40);
            TestServerContext server = world.getServer();
            int x = at[0], y = at[1] + 30, z = at[2];
            AABB pool = new AABB(x - 12, y - 9, z - 12, x + 12, y + 5, z + 12);
            Map<UUID, SkorfnaFish.Variant> reloaded = skorfnaVariantsIn(server, pool);
            int same = 0;
            for (Map.Entry<UUID, SkorfnaFish.Variant> e : variants.entrySet()) {
                check(reloaded.get(e.getKey()) == e.getValue(), "a " + e.getValue().id() + " skorfna came back as " + reloaded.get(e.getKey()));
                same++;
            }
            long reds = variants.values().stream().filter(v -> v == SkorfnaFish.Variant.RED).count();
            log("save and reload: all " + same + " skorfna kept their version (" + reds + " red, " + (same - reds) + " black)");
            server.runCommand("kill @e[type=mimcontent:skorfna]");
            skorfnaVariantShot(context, server, world, at[0], at[1], at[2]);
        }
    }

    /** The review shot fish-skorfna-variants: a black (left) and a red skorfna (right) side by side on a stone floor, in a
     *  shallow open tank at midday, seen from the air above the water. */
    private static void skorfnaVariantShot(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 9, y, z - 6, x + 9, y + 12, z + 10, "minecraft:air");
        fill(server, x - 9, y - 1, z - 6, x + 9, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 6, y, z + 4, x + 6, y + 5, z + 9, "minecraft:glass");
        fill(server, x - 5, y, z + 5, x + 5, y, z + 8, "minecraft:stone");
        // a shallow, open tank in full daylight, so the two colours can be judged: one block of water, air above it,
        // and the cameras in the air (inside the water its fog greys and darkens everything)
        fill(server, x - 5, y + 1, z + 5, x + 5, y + 1, z + 8, "minecraft:water");
        fill(server, x - 5, y + 2, z + 5, x + 5, y + 5, z + 8, "minecraft:air");
        server.runCommand("time set 6000");
        server.runCommand("weather clear");
        // +x is on the left of a camera looking south
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:skorfna %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f],Variant:\"black\"}",
            x + 1.3, y + 1, z + 6.5));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:skorfna %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f],Variant:\"red\"}",
            x - 0.7, y + 1, z + 6.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        server.runCommand("gamemode spectator @a");
        context.runOnClient(mc -> {
            if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle();
        });
        // look() places the player's feet (and a barrier under them); the eyes are 1.62 higher, here just above the water
        look(context, server, x + 0.3, y + 0.6, z + 5.2, x + 0.3, y + 1.2, z + 6.5, "fish-skorfna-variants");
        look(context, server, x + 0.3, y + 3.0, z + 6.3, x + 0.3, y + 1.2, z + 6.5, "fish-skorfna-variants-top");
        server.runCommand("gamemode creative @a");
    }

    /** Every skorfna in the area, by UUID, with its version. */
    private static Map<UUID, SkorfnaFish.Variant> skorfnaVariantsIn(TestServerContext server, AABB area) {
        return server.computeOnServer(s -> {
            Map<UUID, SkorfnaFish.Variant> out = new HashMap<>();
            skorfnas(s.overworld(), area).forEach(f -> out.put(f.getUUID(), f.getVariant()));
            return out;
        });
    }

    private static List<SkorfnaFish> skorfnas(ServerLevel level, AABB area) {
        List<SkorfnaFish> out = new ArrayList<>();
        level.getEntities(MimFishes.SKORFNA.type(), area, e -> true).forEach(e -> out.add((SkorfnaFish) e));
        return out;
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

    /** The cawl model's own review: one cawl alone in a small tank, close up from several sides, one beside a vanilla cod, and one on land. */
    private static void cawlShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 7, y, z - 6, x + 7, y + 12, z + 10, "minecraft:air");
        fill(server, x - 7, y - 1, z - 6, x + 7, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 4, y, z + 4, x + 4, y + 4, z + 9, "minecraft:glass");
        fill(server, x - 3, y, z + 5, x + 3, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:cawl %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1.5, z + 5.6));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.4, y + 1.5, z + 5.6));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:cawl %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall, so no glass frames cross the fish; in spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.5, y, z + 4.3, x + 0.5, y + 1.5, z + 5.6, "fish-cawl-side");
        look(context, server, x - 0.4, y + 0.6, z + 4.4, x + 0.5, y + 1.5, z + 5.6, "fish-cawl-three-quarter");
        look(context, server, x + 0.5, y + 1.1, z + 4.85, x + 0.5, y + 1.5, z + 5.6, "fish-cawl-top");
        look(context, server, x - 0.45, y, z + 4.3, x - 0.45, y + 1.5, z + 5.6, "fish-cawl-beside-cod");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y, z - 1.0, x + 0.5, y + 0.15, z + 0.5, "fish-cawl-on-land");
    }

    /** The awrata model's own review: one awrata alone in a small tank, close up from several sides, one beside a vanilla cod, and one on land. */
    private static void awrataShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 7, y, z - 6, x + 7, y + 12, z + 10, "minecraft:air");
        fill(server, x - 7, y - 1, z - 6, x + 7, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 5, y, z + 4, x + 5, y + 5, z + 9, "minecraft:glass");
        fill(server, x - 4, y, z + 5, x + 4, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:awrata %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1.5, z + 6.0));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.6, y + 1.6, z + 6.0));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:awrata %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall, so no glass frames cross the fish; in spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.5, y + 0.2, z + 4.3, x + 0.5, y + 1.8, z + 6.0, "fish-awrata-side");
        look(context, server, x - 0.8, y + 0.6, z + 4.5, x + 0.4, y + 1.8, z + 6.0, "fish-awrata-three-quarter");
        look(context, server, x + 0.5, y + 1.5, z + 4.75, x + 0.5, y + 1.8, z + 6.0, "fish-awrata-top");
        look(context, server, x - 0.5, y + 0.2, z + 4.3, x - 0.5, y + 1.8, z + 6.0, "fish-awrata-beside-cod");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y, z - 1.1, x + 0.5, y + 0.15, z + 0.5, "fish-awrata-on-land");
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
        // side on, looking down through the water so the tank's sand floor is behind it: does it still show on sand?
        look(context, server, x + 0.5, y + 1.4, z + 4.4, x + 0.5, y + 1.6, z + 5.6, "fish-ziemel-side-on-sand");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y, z - 1.0, x + 0.5, y + 0.15, z + 0.5, "fish-ziemel-on-land");
    }

    /** The pixxispad model's own review: one alone in a long tank (side, three-quarter, top), with a vanilla cod in
     *  front of its sword for size, and one on land. */
    private static void pixxispadShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 9, y, z - 6, x + 9, y + 12, z + 10, "minecraft:air");
        fill(server, x - 9, y - 1, z - 6, x + 9, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 6, y, z + 4, x + 6, y + 5, z + 9, "minecraft:glass");
        fill(server, x - 5, y, z + 5, x + 5, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:pixxispad %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1.5, z + 6.5));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 2.6, y + 1.6, z + 6.5));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:pixxispad %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall, so no glass frames cross the fish; in spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x - 0.3, y + 0.2, z + 4.3, x - 0.3, y + 1.8, z + 6.5, "fish-pixxispad-side");
        // front three-quarter from the sword's side; the cod (x - 2.6) stays behind the camera's left shoulder
        look(context, server, x - 1.4, y + 0.7, z + 4.5, x + 0.4, y + 1.8, z + 6.5, "fish-pixxispad-three-quarter");
        look(context, server, x - 0.65, y + 0.2, z + 4.3, x - 0.65, y + 1.8, z + 6.5, "fish-pixxispad-beside-cod");
        // from above, still inside the glass wall: look() puts a barrier under the camera, which must not land in the
        // water next to the fish (it would cut a hole in the water and hurt the fish, flashing it red)
        look(context, server, x + 0.3, y + 2.6, z + 4.6, x + 0.3, y + 1.8, z + 6.5, "fish-pixxispad-top");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y, z - 2.6, x + 0.5, y + 0.2, z + 0.5, "fish-pixxispad-on-land");
    }

    /** The murina model's own review: one moray alone in a tank (it is 2 blocks long), close up from several sides,
     *  one beside a vanilla cod, and one on land. */
    private static void murinaShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 7, y, z - 6, x + 7, y + 12, z + 10, "minecraft:air");
        fill(server, x - 7, y - 1, z - 6, x + 7, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 5, y, z + 4, x + 5, y + 5, z + 9, "minecraft:glass");
        fill(server, x - 4, y, z + 5, x + 4, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:murina %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1.5, z + 6.2));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.9, y + 1.5, z + 6.2));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:murina %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall, so no glass frames cross the fish; in spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.6, y + 0.1, z + 4.3, x + 0.6, y + 1.7, z + 6.2, "fish-murina-side");
        look(context, server, x - 1.0, y + 0.5, z + 4.5, x + 0.3, y + 1.7, z + 6.2, "fish-murina-three-quarter");
        look(context, server, x + 0.6, y + 1.6, z + 4.7, x + 0.6, y + 1.7, z + 6.2, "fish-murina-top");
        look(context, server, x - 0.3, y + 0.1, z + 4.3, x - 0.3, y + 1.7, z + 6.2, "fish-murina-beside-cod");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.6, y, z - 1.3, x + 0.6, y + 0.2, z + 0.5, "fish-murina-on-land");
    }

    /** The incova model's own review: one incova alone in a small tank, close up from several sides, one beside a vanilla cod, and one on land. */
    private static void incovaShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 7, y, z - 6, x + 7, y + 12, z + 10, "minecraft:air");
        fill(server, x - 7, y - 1, z - 6, x + 7, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 4, y, z + 4, x + 4, y + 4, z + 9, "minecraft:glass");
        fill(server, x - 3, y, z + 5, x + 3, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:incova %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1.5, z + 5.6));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.4, y + 1.5, z + 5.6));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:incova %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall, so no glass frames cross the fish; in spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.5, y, z + 4.3, x + 0.5, y + 1.5, z + 5.6, "fish-incova-side");
        look(context, server, x - 0.4, y + 0.6, z + 4.4, x + 0.5, y + 1.5, z + 5.6, "fish-incova-three-quarter");
        look(context, server, x + 0.5, y + 1.1, z + 4.85, x + 0.5, y + 1.5, z + 5.6, "fish-incova-top");
        look(context, server, x - 0.45, y, z + 4.3, x - 0.45, y + 1.5, z + 5.6, "fish-incova-beside-cod");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y, z - 1.0, x + 0.5, y + 0.15, z + 0.5, "fish-incova-on-land");
    }

    /** The huta kahla model's own review: one blue shark alone in a long tank (it is 2.6 blocks long), close up from
     *  several sides, one with a vanilla cod in front of its snout, and one on land. */
    private static void hutaKahlaShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 9, y, z - 6, x + 9, y + 12, z + 10, "minecraft:air");
        fill(server, x - 9, y - 1, z - 6, x + 9, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 6, y, z + 4, x + 6, y + 5, z + 9, "minecraft:glass");
        fill(server, x - 5, y, z + 5, x + 5, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:huta_kahla %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1.5, z + 6.5));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.9, y + 1.7, z + 6.5));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:huta_kahla %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall, so no glass frames cross the fish; in spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.7, y + 0.2, z + 4.3, x + 0.7, y + 1.85, z + 6.5, "fish-huta-kahla-side");
        look(context, server, x - 2.0, y + 0.7, z + 4.5, x + 0.5, y + 1.85, z + 6.5, "fish-huta-kahla-three-quarter");
        // from high in the front glass wall, looking steeply down: look() puts a barrier under the camera, and one
        // inside the water would cut into the shark's hitbox and hurt it (it turns red)
        look(context, server, x + 0.4, y + 2.6, z + 4.3, x + 0.4, y + 1.85, z + 6.5, "fish-huta-kahla-top");
        look(context, server, x - 0.3, y + 0.2, z + 4.3, x - 0.3, y + 1.85, z + 6.5, "fish-huta-kahla-beside-cod");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y, z - 2.6, x + 0.5, y + 0.2, z + 0.5, "fish-huta-kahla-on-land");
    }

    /** The boll's own review: one lying on a sand floor in a tank, a vanilla cod above it for scale, and one on land. */
    private static void bollShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 9, y, z - 6, x + 9, y + 12, z + 10, "minecraft:air");
        fill(server, x - 9, y - 1, z - 6, x + 9, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 6, y, z + 4, x + 6, y + 5, z + 9, "minecraft:glass");
        fill(server, x - 5, y, z + 5, x + 5, y, z + 8, "minecraft:sand");
        fill(server, x - 5, y + 1, z + 5, x + 5, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:boll %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1, z + 5.6));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.9, y + 1.9, z + 5.8));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:boll %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall, so no glass frames cross the fish; in spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.3, y - 0.3, z + 4.3, x + 0.3, y + 1.1, z + 5.6, "fish-boll-side");
        look(context, server, x - 0.5, y + 0.1, z + 4.3, x + 0.6, y + 1.05, z + 5.6, "fish-boll-three-quarter");
        look(context, server, x + 0.3, y + 1.4, z + 4.3, x + 0.3, y + 1.1, z + 5.6, "fish-boll-top");
        look(context, server, x - 0.4, y - 0.2, z + 4.2, x - 0.4, y + 1.4, z + 5.7, "fish-boll-beside-cod");
        // from below: a third boll held up near the surface (no gravity), seen from low in the glass wall
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:boll %.1f %.1f %.1f {NoAI:1b,NoGravity:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 3.8, y + 3.6, z + 5.6));
        context.waitTicks(10);
        look(context, server, x + 3.8, y - 0.1, z + 4.3, x + 3.8, y + 3.65, z + 5.6, "fish-boll-below");
        look(context, server, x + 3.8, y + 0.4, z + 5.6, x + 3.8, y + 3.65, z + 5.65, "fish-boll-below-close");
        // the wing ripple at rest (RayModel: 0.1 radians, a beat about every 25 ticks), from in front of its head
        look(context, server, x - 1.0, y - 0.3, z + 5.6, x + 0.5, y + 1.1, z + 5.6, "fish-boll-ripple-0");
        for (int frame = 1; frame < 5; frame++) {
            context.waitTicks(5);
            context.takeScreenshot("fish-boll-ripple-" + frame);
        }
        server.runCommand("gamemode creative @a");
        look(context, server, x - 0.3, y + 0.1, z - 1.0, x + 0.5, y, z + 0.5, "fish-boll-on-land");
        // the size choice (owner 2026-11-18, "seemingly small"): the installed boll (disc 1.25 blocks) between one scaled
        // to a 1.0 block disc and one to 1.5, beside a vanilla cod and a 3-block tonn, all on dry sand so nothing greys them
        fill(server, x - 9, y, z + 14, x + 9, y + 12, z + 30, "minecraft:air");
        fill(server, x - 9, y - 1, z + 14, x + 9, y - 1, z + 30, "minecraft:smooth_sandstone");
        String[] sizes = {"0.8", "1.0", "1.2"};
        for (int i = 0; i < sizes.length; i++) {
            server.runCommand(String.format(Locale.ROOT,
                "summon mimcontent:boll %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f],attributes:[{id:\"minecraft:scale\",base:%s}]}",
                x - 4.5 + 4.5 * i, y, z + 21.5, sizes[i]));
        }
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 4.5, y, z + 24.5));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:tonn %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f],Length:3.0f}",
            x + 1.5, y, z + 24.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(30);
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.0, y + 6.0, z + 22.9, x + 0.0, y, z + 23.0, "fish-boll-sizes");
        look(context, server, x + 0.0, y + 1.6, z + 17.0, x + 0.0, y, z + 22.5, "fish-boll-sizes-low");
        server.runCommand("gamemode creative @a");
    }

    /** The skorfna's own review: one resting on a stone floor in a tank, a vanilla cod beside it for scale, and one on land. */
    private static void skorfnaShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 9, y, z - 6, x + 9, y + 12, z + 10, "minecraft:air");
        fill(server, x - 9, y - 1, z - 6, x + 9, y - 1, z + 10, "minecraft:smooth_sandstone");
        fill(server, x - 6, y, z + 4, x + 6, y + 5, z + 9, "minecraft:glass");
        fill(server, x - 5, y, z + 5, x + 5, y, z + 8, "minecraft:stone");
        fill(server, x - 5, y + 1, z + 5, x + 5, y + 4, z + 8, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:skorfna %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f],Variant:\"black\"}",
            x + 0.5, y + 1, z + 6.5));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 1.3, y + 1.6, z + 6.5));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:skorfna %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f],Variant:\"black\"}",
            x + 0.5, y, z + 0.5));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        // the cameras sit inside the glass wall, so no glass frames cross the fish; in spectator mode nothing pushes them out
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.3, y + 0.2, z + 4.4, x + 0.3, y + 1.3, z + 6.5, "fish-skorfna-side");
        look(context, server, x - 1.5, y + 0.8, z + 4.4, x + 0.5, y + 1.3, z + 6.5, "fish-skorfna-three-quarter");
        look(context, server, x + 0.4, y + 2.4, z + 4.6, x + 0.4, y + 1.2, z + 6.5, "fish-skorfna-top");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y + 0.2, z - 1.8, x + 0.5, y + 0.2, z + 0.5, "fish-skorfna-on-land");
    }

    /**
     * The mola mola (owner 2026-11-18: "begin on the mola mola"; "the mola mola must be EXTREMELY rare"): its numbers
     * (health, speed, body box, no bite); the rarity roll on natural spawns (one in MolaFish.SPAWN_CHANCE) while eggs,
     * spawners and /summon always work; it doesn't shy away from a player; and in an open pool it rises to the
     * surface and basks on its side (flat box, at the surface, its hit boxes lying flat and centred), until it is hurt.
     */
    private static void mola(ClientGameTestContext context, TestServerContext server, int x, int y, int z) {
        String numbers = server.computeOnServer(s -> {
            AbstractFish fish = MimFishes.MOLA_MOLA.type().create(s.overworld(), EntitySpawnReason.COMMAND);
            return String.format(Locale.ROOT, "health %.0f, speed %.2f, box %.2fx%.2f, bite %s", fish.getMaxHealth(),
                fish.getAttributeValue(Attributes.MOVEMENT_SPEED), fish.getBbWidth(), fish.getBbHeight(),
                fish.getAttribute(Attributes.ATTACK_DAMAGE) == null ? "none" : "yes");
        });
        log("mola mola: " + numbers);
        check(numbers.equals("health 20, speed 0.35, box 1.30x1.80, bite none"), "the mola mola's numbers: " + numbers);

        // the rarity roll: natural spawns pass about one time in SPAWN_CHANCE, spawners and eggs always
        int[] passed = server.computeOnServer(s -> {
            net.minecraft.util.RandomSource random = net.minecraft.util.RandomSource.create(1234L);
            int natural = 0, chunk = 0, other = 0;
            for (int i = 0; i < 400_000; i++) {
                natural += MolaFish.rareRoll(EntitySpawnReason.NATURAL, random) ? 1 : 0;
            }
            for (int i = 0; i < 40_000; i++) {
                chunk += MolaFish.rareRoll(EntitySpawnReason.CHUNK_GENERATION, random) ? 1 : 0;
                other += MolaFish.rareRoll(i % 3 == 0 ? EntitySpawnReason.SPAWNER : i % 3 == 1 ? EntitySpawnReason.SPAWN_ITEM_USE
                    : EntitySpawnReason.COMMAND, random) ? 1 : 0;
            }
            return new int[] {natural, chunk, other};
        });
        log(String.format(Locale.ROOT, "mola mola rarity roll: %d of 400000 natural tries passed (one in %d expected), %d of 40000 at chunk"
            + " generation, %d of 40000 spawner/egg/command", passed[0], MolaFish.SPAWN_CHANCE, passed[1], passed[2]));
        double expect = 400_000.0 / MolaFish.SPAWN_CHANCE;
        check(MolaFish.SPAWN_CHANCE >= 400 && Math.abs(passed[0] - expect) < expect * 0.2 && passed[1] < 40_000 / MolaFish.SPAWN_CHANCE * 2
            && passed[2] == 40_000, "the mola mola's rarity roll is off: " + java.util.Arrays.toString(passed));

        // an open pool (the main pool has a stone lid): 13 x 13, 6 deep, open to the sky
        int px = x + 30;
        fill(server, px - 9, y - 10, z - 9, px + 9, y + 4, z + 9, "minecraft:air");
        fill(server, px - 7, y - 8, z - 7, px + 7, y - 1, z + 7, "minecraft:stone");
        fill(server, px - 6, y - 7, z - 6, px + 6, y - 1, z + 6, "minecraft:water");
        server.runCommand("gamemode survival @a");
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %d %.1f", px - 6.5, y, z - 7.5));
        context.waitTicks(10);
        AABB area = new AABB(px - 8, y - 9, z - 8, px + 9, y + 3, z + 9);
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:mola_mola %.1f %d %.1f {PersistenceRequired:1b}", px + 0.5, y - 6, z + 0.5));
        // a player beside it: it doesn't swim away (no shying), and it basks when it likes
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %d %.1f", px - 2.5, y - 5, z + 0.5));
        server.runCommand("effect give @a minecraft:water_breathing 200 0 true");
        server.runCommand("effect give @a minecraft:resistance 200 4 true");
        String basked = "never";
        double surface = y - 1 + 8.0 / 9.0;
        double[] highest = {-1000.0};
        for (int t = 0; t < 2400 && !basked.startsWith("now"); t += 10) {
            context.waitTicks(10);
            basked = server.computeOnServer(s -> {
                List<? extends AbstractFish> found = s.overworld().getEntities(MimFishes.MOLA_MOLA.type(), area, e -> true);
                if (found.size() != 1) {
                    return "found " + found.size();
                }
                MolaFish mola = (MolaFish) found.getFirst();
                highest[0] = Math.max(highest[0], mola.getY() - surface);
                return String.format(Locale.ROOT, "%s: trips %d, at %.2f below the surface, inWater=%s", mola.isBasking() ? "now" : "not yet",
                    mola.baskTrips, surface - mola.getY(), mola.isInWater());
            });
        }
        log(String.format(Locale.ROOT, "mola mola in an open pool: %s (highest %.2f from the surface)", basked, highest[0]));
        check(basked.startsWith("now"), "the mola mola never came up to bask in 2 minutes: " + basked);
        context.waitTicks(20);
        String state = server.computeOnServer(s -> {
            MolaFish mola = (MolaFish) s.overworld().getEntities(MimFishes.MOLA_MOLA.type(), area, e -> true).getFirst();
            double low = Double.MAX_VALUE, high = -Double.MAX_VALUE, cx = 0, cz = 0;
            int n = 0;
            for (FishPart part : ((FishParts.Holder) mola).mimcontent$parts().parts()) {
                AABB b = part.getBoundingBox();
                low = Math.min(low, b.minY);
                high = Math.max(high, b.maxY);
                cx += b.getCenter().x;
                cz += b.getCenter().z;
                n++;
            }
            double off = Math.hypot(cx / n - mola.getX(), cz / n - mola.getZ());
            return String.format(Locale.ROOT, "basking=%s inWater=%s y=%.2f box=%.2fx%.2f boxes %.2f..%.2f off-centre %.2f",
                mola.isBasking(), mola.isInWater(), mola.getY() - surface, mola.getBbWidth(), mola.getBbHeight(), low - surface, high - surface, off);
        });
        log("mola mola basking (heights from the water's surface): " + state);
        String[] v = state.replaceAll(".*y=([-0-9.]+) box=([0-9.]+)x([0-9.]+) boxes ([-0-9.]+)\\.\\.([-0-9.]+) off-centre ([0-9.]+)", "$1 $2 $3 $4 $5 $6").split(" ");
        double yy = Double.parseDouble(v[0]), bw = Double.parseDouble(v[1]), bh = Double.parseDouble(v[2]);
        double lo = Double.parseDouble(v[3]), hi = Double.parseDouble(v[4]), off = Double.parseDouble(v[5]);
        check(state.startsWith("basking=true inWater=true") && Math.abs(yy + MolaFish.BASK_DEPTH) < 0.2
                && Math.abs(bw - MolaFish.BASK_WIDTH) < 0.01 && Math.abs(bh - MolaFish.BASK_HEIGHT) < 0.01
                && lo > -0.9 && lo < 0.0 && hi > 0.0 && hi < 0.6 && off < 0.6,
            "the basking mola mola should lie flat at the surface, its boxes flat and centred: " + state);
        // hurt it: it stops basking and swims off
        server.runOnServer(s -> {
            ServerLevel level = s.overworld();
            MolaFish mola = (MolaFish) level.getEntities(MimFishes.MOLA_MOLA.type(), area, e -> true).getFirst();
            mola.hurtServer(level, level.damageSources().playerAttack(s.getPlayerList().getPlayers().getFirst()), 1.0F);
        });
        context.waitTicks(10);
        String hurt = server.computeOnServer(s -> {
            MolaFish mola = (MolaFish) s.overworld().getEntities(MimFishes.MOLA_MOLA.type(), area, e -> true).getFirst();
            return String.format(Locale.ROOT, "basking=%s box=%.2fx%.2f", mola.isBasking(), mola.getBbWidth(), mola.getBbHeight());
        });
        log("mola mola after being hurt: " + hurt);
        check(hurt.equals("basking=false box=1.30x1.80"), "a hurt mola mola should stop basking: " + hurt);
        // harmless: the player beside it took no damage from it
        String player = server.computeOnServer(s -> stingState(s.getPlayerList().getPlayers().getFirst()));
        log("the player beside the mola mola: " + player);
        check(!player.contains("by mola_mola"), "the mola mola should be harmless: " + player);
        server.runCommand("effect clear @a");
        server.runCommand("kill @e[type=mimcontent:mola_mola]");
    }

    /**
     * The mola mola model's own review: one in a tall tank (side, three-quarter, front, top), sculling frames from in
     * front, beside a vanilla cod, a 3-block tonn and the blue shark in a long tank, one basking at the surface of an
     * open pool (from above the water and from below), and one on land.
     */
    private static void molaShots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        fill(server, x - 14, y, z - 8, x + 14, y + 12, z + 30, "minecraft:air");
        fill(server, x - 14, y - 1, z - 8, x + 14, y - 1, z + 30, "minecraft:smooth_sandstone");
        // the tall tank: water 11 x 5 x 5 (x - 5 .. x + 5, z + 5 .. z + 9), glass round it
        fill(server, x - 6, y, z + 4, x + 6, y + 6, z + 10, "minecraft:glass");
        fill(server, x - 5, y, z + 5, x + 5, y + 5, z + 9, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:mola_mola %.1f %.1f %.1f {NoAI:1b,NoGravity:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 2.5, y + 1.0, z + 7.5));
        // a vanilla cod in the same tank, for scale and for the water's tint
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,NoGravity:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 1.5, y + 1.8, z + 7.5));
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:mola_mola %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y, z - 3.0));
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        server.runCommand("gamemode spectator @a");
        // centre of the disc: 1.22 blocks above its position
        double cy = y + 1.0 + 1.22;
        // the cameras sit inside the glass walls (look() puts a barrier under the camera: never in the water)
        look(context, server, x - 1.5, y + 0.4, z + 4.3, x - 1.5, cy, z + 7.5, "fish-mola-side");
        look(context, server, x - 5.0, y + 1.0, z + 4.4, x - 2.5, cy, z + 7.5, "fish-mola-three-quarter");
        look(context, server, x - 5.7, y + 0.6, z + 7.5, x - 2.5, cy, z + 7.5, "fish-mola-front");
        // sculling: the dorsal and anal fins swing to the same side together, seen from in front
        look(context, server, x - 5.7, y + 0.6, z + 7.5, x - 2.5, cy, z + 7.5, "fish-mola-scull-0");
        for (int frame = 1; frame < 5; frame++) {
            context.waitTicks(6);
            context.takeScreenshot("fish-mola-scull-" + frame);
        }
        // from high in the front glass wall, looking steeply down (the barrier under the camera goes into the wall)
        look(context, server, x - 2.4, y + 4.4, z + 4.4, x - 2.5, cy, z + 7.5, "fish-mola-top");
        server.runCommand("gamemode creative @a");
        look(context, server, x + 0.5, y + 0.4, z - 6.8, x + 0.5, y + 0.3, z - 3.0, "fish-mola-on-land");

        // the sizes: a long tank, cod, mola mola, a 3-block tonn and the blue shark side by side
        fill(server, x - 14, y, z + 13, x + 14, y + 5, z + 19, "minecraft:glass");
        fill(server, x - 13, y, z + 14, x + 13, y + 4, z + 18, "minecraft:water");
        String[][] row = {{"minecraft:cod", "-7.5", "1.5", ""}, {"mimcontent:mola_mola", "-4.5", "0.6", ""},
            {"mimcontent:tonn", "0.5", "1.3", ",Length:3.0f"}, {"mimcontent:huta_kahla", "6.0", "1.3", ""}};
        for (String[] r : row) {
            server.runCommand(String.format(Locale.ROOT, "summon %s %.1f %.1f %.1f {NoAI:1b,NoGravity:1b,PersistenceRequired:1b,Rotation:[90f,0f]%s}",
                r[0], x + Double.parseDouble(r[1]), y + Double.parseDouble(r[2]), z + 16.5, r[3]));
        }
        world.getConnection().waitForChunksRender();
        context.waitTicks(30);
        server.runCommand("gamemode spectator @a");
        // between the two tanks (inside the first tank's back wall), then close up inside the long tank's front wall
        look(context, server, x - 1.0, y + 0.3, z + 10.5, x - 1.0, y + 1.8, z + 16.5, "fish-mola-sizes");
        look(context, server, x - 4.5, y + 0.3, z + 13.3, x - 4.5, y + 1.8, z + 16.5, "fish-mola-sizes-low");
        server.runCommand("gamemode creative @a");

        // basking: an open pool, the mola lying on its side at the surface, a cod beside it
        fill(server, x - 6, y, z + 22, x + 6, y + 3, z + 30, "minecraft:glass");
        fill(server, x - 5, y, z + 23, x + 5, y + 3, z + 29, "minecraft:water");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:mola_mola %.1f %.1f %.1f {NoAI:1b,NoGravity:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x + 0.5, y + 1.5, z + 26.5));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}",
            x - 2.5, y + 3.2, z + 24.5));
        context.waitTicks(5);
        server.runOnServer(s -> s.overworld().getEntities(MimFishes.MOLA_MOLA.type(), new AABB(x - 6, y, z + 22, x + 6, y + 5, z + 30), e -> true)
            .forEach(e -> ((MolaFish) e).baskNow()));
        world.getConnection().waitForChunksRender();
        context.waitTicks(30);
        look(context, server, x + 0.5, y + 3.6, z + 22.3, x + 0.5, y + 3.6, z + 26.5, "fish-mola-basking");
        look(context, server, x + 0.7, y + 6.5, z + 25.0, x + 0.5, y + 3.6, z + 26.5, "fish-mola-basking-above");
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.5, y - 0.6, z + 22.3, x + 0.5, y + 3.7, z + 26.5, "fish-mola-basking-below");
        server.runCommand("gamemode creative @a");
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
    /**
     * Each skorfna version drops its own item (owner 2026-11-18): black the skorfna item, red skorfna_red, one each, the
     * same way the other fish drop: killed outright, killed by a player with a Looting III sword, and killed burning.
     */
    private static void skorfnaDrops(ClientGameTestContext context, TestServerContext server, int x, int y, int z, AABB pool) {
        check(MimFishes.SKORFNA_RED != null && MimFishes.SKORFNA_RED != MimFishes.SKORFNA.item()
            && BuiltInRegistries.ITEM.getKey(MimFishes.SKORFNA_RED).toString().equals("mimcontent:skorfna_red"), "the skorfna_red item is missing");
        server.runCommand("item replace entity @a weapon.mainhand with minecraft:diamond_sword[enchantments={\"minecraft:looting\":3}]");
        List<String> results = new ArrayList<>();
        for (SkorfnaFish.Variant variant : SkorfnaFish.Variant.values()) {
            String expected = (variant == SkorfnaFish.Variant.RED ? "mimcontent:skorfna_red" : "mimcontent:skorfna") + " x1";
            for (String how : new String[] {"killed", "player, looting 3", "burning"}) {
                server.runCommand("kill @e[type=item]");
                server.runOnServer(s -> {
                    ServerLevel level = s.overworld();
                    SkorfnaFish fish = (SkorfnaFish) MimFishes.SKORFNA.type().create(level, EntitySpawnReason.COMMAND);
                    fish.setVariant(variant);
                    fish.setPos(x + 7.5, y + 1, z - 7.5);
                    level.addFreshEntity(fish);
                    switch (how) {
                        case "player, looting 3" -> {
                            ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                            fish.hurtServer(level, level.damageSources().playerAttack(player), 1000.0F);
                        }
                        case "burning" -> {
                            fish.igniteForSeconds(5.0F);
                            fish.kill(level);
                        }
                        default -> fish.kill(level);
                    }
                });
                context.waitTicks(5);
                String got = drops(server, pool);
                results.add(variant.id() + " " + how + ": [" + got + "]");
                check(got.equals(expected), "a " + variant.id() + " skorfna (" + how + ") should drop [" + expected + "], dropped [" + got + "]");
            }
        }
        server.runCommand("kill @e[type=item]");
        server.runCommand("item replace entity @a weapon.mainhand with minecraft:air");
        log("skorfna drops by version: " + String.join("; ", results));
    }

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
