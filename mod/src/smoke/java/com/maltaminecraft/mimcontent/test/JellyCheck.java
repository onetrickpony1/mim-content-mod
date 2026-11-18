package com.maltaminecraft.mimcontent.test;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.maltaminecraft.mimcontent.MimConfig;
import com.maltaminecraft.mimcontent.MimJellyfish;
import com.maltaminecraft.mimcontent.client.jelly.JellyfishModel;
import com.maltaminecraft.mimcontent.client.jelly.JellyfishRenderer;
import com.maltaminecraft.mimcontent.entity.jelly.Jellyfish;
import com.mojang.blaze3d.vertex.PoseStack;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TreeMap;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.alchemy.Potion;
import net.minecraft.world.item.alchemy.PotionContents;
import net.minecraft.world.item.alchemy.Potions;
import net.minecraft.world.item.crafting.AbstractCookingRecipe;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.block.entity.BrewingStandBlockEntity;
import net.minecraft.world.phys.AABB;
import org.joml.Vector3f;

/**
 * Checks the three jellyfish in a real game (SMOKE_ONLY=jelly): the config switches; each spawns, lives in water and
 * has a box the size of its model; the man o' war stays on the surface; the mauve stinger rises at night and sinks by
 * day; the stings (mauve stinger, man o' war and its tentacle column; never below 1 heart; none in creative, none from
 * the fried-egg, none with Jellyfish Ward); the mauve stinger's flash; the drops; both venom brews in a real brewing
 * stand; the meat can't be cooked and is bait; the spawns in vanilla's oceans. Then screenshots (jelly-*).
 */
public class JellyCheck implements FabricClientGameTest {
    @Override
    public void runTest(ClientGameTestContext context) {
        if (!Smoke.runs("jelly")) {
            return;
        }
        try {
            JsonObject json = JsonParser.parseString(Files.readString(MimConfig.path())).getAsJsonObject();
            check(json.has("jellyfish_venom_recipes") && json.get("jellyfish_venom_recipes").getAsBoolean(),
                "config jellyfish_venom_recipes missing or not true by default");
            log("config has jellyfish_venom_recipes = true");
        } catch (java.io.IOException e) {
            throw new AssertionError("can't read the config file", e);
        }
        try (TestSingleplayerContext world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            modelSizes(context);
            TestServerContext server = world.getServer();
            server.runCommand("gamemode creative @a");
            server.runCommand("gamerule spawn_mobs false");
            server.runCommand("gamerule advance_time false");
            server.runCommand("gamerule advance_weather false");
            server.runCommand("weather clear");
            server.runCommand("time set 6000");
            int[] p = context.computeOnClient(mc -> new int[] {mc.player.getBlockX(), mc.player.getBlockY(), mc.player.getBlockZ()});
            int x = p[0], y = p[1] + 40, z = p[2];
            // a deep pool 15 x 15, 16 deep, high above the land: water y-16 to y-1, the surface at about y-0.11
            fill(server, x - 10, y - 19, z - 10, x + 10, y + 4, z + 10, "minecraft:air");
            fill(server, x - 8, y - 17, z - 8, x + 8, y - 1, z + 8, "minecraft:stone");
            fill(server, x - 7, y - 16, z - 7, x + 7, y - 1, z + 7, "minecraft:water");
            server.runCommand(String.format("tp @a %d %d %d", x - 8, y + 1, z - 8));
            world.getConnection().waitForChunksRender();
            context.waitTicks(10);
            AABB pool = new AABB(x - 9, y - 18, z - 9, x + 10, y + 5, z + 10);
            double surface = server.computeOnServer(s -> {
                BlockPos top = new BlockPos(x, y - 1, z);
                return top.getY() + (double) s.overworld().getFluidState(top).getHeight(s.overworld(), top);
            });

            // 1. each lives in water, with its box size and health
            check(MimJellyfish.ALL.size() == 3, "expected 3 jellyfish, found " + MimJellyfish.ALL.size());
            for (int i = 0; i < 3; i++) {
                server.runCommand(String.format(Locale.ROOT, "summon mimcontent:%s %.1f %d %.1f", MimJellyfish.ALL.get(i).id(), x - 4.0 + 4 * i, y - 8, z + 0.5));
            }
            context.waitTicks(100);
            for (MimJellyfish.Jelly j : MimJellyfish.ALL) {
                String state = server.computeOnServer(s -> {
                    List<Jellyfish> found = s.overworld().getEntities(j.type(), pool, e -> true);
                    if (found.size() != 1) {
                        return "found " + found.size();
                    }
                    Jellyfish e = found.getFirst();
                    return String.format(Locale.ROOT, "%s inWater=%s health=%.0f box=%.4fx%.4f", e.isAlive() ? "ok" : "dead", e.isInWater(),
                        e.getHealth(), e.getBbWidth(), e.getBbHeight());
                });
                log(j.id() + ": " + state);
                check(state.startsWith("ok") && state.contains("inWater=true"), j.id() + " not alive in water: " + state);
            }
            check(server.computeOnServer(s -> MimJellyfish.MAUVE_STINGER.type().create(s.overworld(), EntitySpawnReason.COMMAND).getMaxHealth() == 4.0F
                && MimJellyfish.FRIED_EGG.type().create(s.overworld(), EntitySpawnReason.COMMAND).getMaxHealth() == 6.0F
                && MimJellyfish.MAN_O_WAR.type().create(s.overworld(), EntitySpawnReason.COMMAND).getMaxHealth() == 6.0F), "health should be 4, 6, 6");
            check(MimJellyfish.MAUVE_STINGER.type().getCategory() == MobCategory.WATER_AMBIENT, "jellyfish should be water ambient mobs");

            // 2. the man o' war rose from 8 blocks down to the surface, and stays there
            context.waitTicks(60);
            double lowest = 99, highest = -99;
            for (int t = 0; t < 20; t++) {
                context.waitTicks(5);
                double h = server.computeOnServer(s -> s.overworld().getEntities(MimJellyfish.MAN_O_WAR.type(), pool, e -> true).getFirst().getY());
                lowest = Math.min(lowest, h - surface);
                highest = Math.max(highest, h - surface);
            }
            log(String.format(Locale.ROOT, "man o' war: its bottom from %.2f to %.2f blocks against the surface over 5 s (wanted -%.2f)",
                lowest, highest, Jellyfish.FLOAT_DRAFT));
            check(lowest > -0.4 && highest < 0.1, "the man o' war should float on the surface");
            server.runCommand("kill @e[type=!minecraft:player]");

            // 3. the mauve stinger rises at night (from 10 down) and sinks by day (from just under the surface)
            server.runCommand("time set 18000");
            server.runCommand(String.format(Locale.ROOT, "summon mimcontent:mauve_stinger %.1f %d %.1f {PersistenceRequired:1b}", x + 0.5, y - 12, z + 0.5));
            double night = waitDepth(context, server, pool, surface, 40 * 20, d -> d <= 2.5);
            log(String.format(Locale.ROOT, "mauve stinger at night, from 10.4 deep: its bell top rose to %.2f below the surface", night));
            check(night <= 2.5, "a mauve stinger should rise near the surface at night, it stayed " + night + " deep");
            server.runCommand("time set 6000");
            double day = waitDepth(context, server, pool, surface, 40 * 20, d -> d >= 3.5);
            log(String.format(Locale.ROOT, "mauve stinger by day: its bell top sank to %.2f below the surface", day));
            check(day >= 3.5, "a mauve stinger should sink lower by day, it stayed " + day + " deep");
            server.runCommand("kill @e[type=!minecraft:player]");

            stings(context, server, x, y, z, pool, surface);
            drops(context, server, x, y, z, pool);
            brewing(context, server, x, y, z);
            meat(server);
            vanillaOceanSpawns(server);
            log("all checks passed");
            shots(context, server, world, p[0], p[1], p[2]);
        }
        System.out.println("[smoke] jelly: all checks passed, screenshots written");
    }

    /** Each box matches its baked model: width the bell's (or float's) widest, height from the bottom (y 24) to the top. */
    private static void modelSizes(ClientGameTestContext context) {
        String result = context.computeOnClient(mc -> {
            StringBuilder out = new StringBuilder();
            for (MimJellyfish.Jelly j : MimJellyfish.ALL) {
                JellyfishRenderer renderer = (JellyfishRenderer) (Object) mc.getEntityRenderDispatcher().getRenderer(j.type().create(mc.level, EntitySpawnReason.LOAD));
                JellyfishModel model = renderer.getModel();
                model.resetPose();
                float[] b = {Float.MAX_VALUE, Float.MAX_VALUE, Float.MAX_VALUE, -Float.MAX_VALUE, -Float.MAX_VALUE, -Float.MAX_VALUE};
                boolean floats = j.kind().floats();
                float[] tentacleBottom = {0.0F};
                model.root().visit(new PoseStack(), (pose, path, index, cube) -> {
                    for (int c = 0; c < 8; c++) {
                        Vector3f v = pose.pose().transformPosition(((c & 1) == 0 ? cube.minX : cube.maxX) / 16.0F,
                            ((c & 2) == 0 ? cube.minY : cube.maxY) / 16.0F, ((c & 4) == 0 ? cube.minZ : cube.maxZ) / 16.0F, new Vector3f());
                        if (floats && path.contains("tentacle")) {
                            tentacleBottom[0] = Math.max(tentacleBottom[0], v.y - 1.5F);
                            continue;
                        }
                        float[] px = {v.x, v.y, v.z};
                        for (int k = 0; k < 3; k++) {
                            b[k] = Math.min(b[k], px[k]);
                            b[k + 3] = Math.max(b[k + 3], px[k]);
                        }
                    }
                });
                float width = Math.max(b[3] - b[0], b[5] - b[2]);
                float height = 1.5F - b[1];
                float boxW = j.type().getWidth(), boxH = j.type().getHeight();
                log(String.format(Locale.ROOT, "%s model: %.4f wide, %.4f tall above its bottom%s; box %.4f x %.4f", j.id(), width, height,
                    floats ? " (the float; tentacles to " + String.format(Locale.ROOT, "%.2f", tentacleBottom[0]) + " below)" : "", boxW, boxH));
                if (Math.abs(width - boxW) > 0.07F || Math.abs(height - boxH) > 0.07F) {
                    out.append(j.id()).append(String.format(Locale.ROOT, " box %.3fx%.3f, model %.3fx%.3f; ", boxW, boxH, width, height));
                }
                if (floats && Math.abs(tentacleBottom[0] - Jellyfish.MAN_O_WAR_TENTACLE_LENGTH) > 0.25F) {
                    out.append(String.format(Locale.ROOT, "tentacles hang %.2f, the sting column is %.2f; ", tentacleBottom[0], Jellyfish.MAN_O_WAR_TENTACLE_LENGTH));
                }
            }
            return out.isEmpty() ? "ok" : out.toString();
        });
        check(result.equals("ok"), "hitboxes don't match the models: " + result);
    }

    private static double waitDepth(ClientGameTestContext context, TestServerContext server, AABB pool, double surface, int ticks,
                                    java.util.function.DoublePredicate done) {
        double depth = 0;
        for (int t = 0; t < ticks; t += 20) {
            context.waitTicks(20);
            depth = surface - server.computeOnServer(s -> s.overworld().getEntities(MimJellyfish.MAUVE_STINGER.type(), pool, e -> true).getFirst().getBoundingBox().maxY);
            if (done.test(depth)) {
                break;
            }
        }
        log(server.computeOnServer(s -> {
            Jellyfish j = s.overworld().getEntities(MimJellyfish.MAUVE_STINGER.type(), pool, e -> true).getFirst();
            return String.format(Locale.ROOT, "  (dark outside %s, sky darken %d, speed %s, preferred %s)", s.overworld().isDarkOutside(),
                s.overworld().getSkyDarken(), j.getDeltaMovement(), java.util.Arrays.toString(j.preferredDepth()));
        }));
        return depth;
    }

    private static void stings(ClientGameTestContext context, TestServerContext server, int x, int y, int z, AABB pool, double surface) {
        server.runCommand("gamemode survival @a");
        server.runCommand("effect give @a minecraft:water_breathing 600 0 true");
        // the mauve stinger: touched by a survival player
        summonStill(server, "mauve_stinger", x + 0.5, y - 6, z + 0.5);
        String mauve = touch(context, server, pool, MimJellyfish.MAUVE_STINGER, 0.0, 20.0F);
        log("a survival player touching a mauve stinger: " + mauve);
        check(mauve.contains("poison=" + Jellyfish.MAUVE_POISON_SECONDS + "s"), "mauve: poison 5 s: " + mauve);
        check(mauve.startsWith("health 18.0") && mauve.contains("by mauve_stinger"), "mauve: 2 damage: " + mauve);
        boolean flashing = server.computeOnServer(s -> ((Jellyfish) s.overworld().getEntities(MimJellyfish.MAUVE_STINGER.type(), pool, e -> true).getFirst()).isFlashing());
        log("the touched mauve stinger flashes: " + flashing);
        check(flashing, "a touched mauve stinger should flash");
        context.waitTicks(Jellyfish.FLASH_TICKS + 5);
        // a melee hit: the attacker is stung, and it flashes again
        server.runCommand("effect clear @a minecraft:poison");
        server.runCommand(String.format(Locale.ROOT, "tp @a %.1f %d %.1f", x + 2.0, y - 6, z + 0.5));
        context.waitTicks(Jellyfish.STING_COOLDOWN);
        String hit = server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
            player.setHealth(20.0F);
            player.setLastHurtByMob(null);
            Jellyfish jelly = level.getEntities(MimJellyfish.MAUVE_STINGER.type(), pool, e -> true).getFirst();
            jelly.hurtServer(level, level.damageSources().playerAttack(player), 0.5F);
            return state(player) + ", flashing " + jelly.isFlashing();
        });
        log("hitting a mauve stinger in melee: " + hit);
        check(hit.contains("by mauve_stinger") && !hit.contains("poison=none") && hit.endsWith("flashing true"), "a melee hit should sting and flash: " + hit);

        // creative: never stung
        server.runCommand("kill @e[type=!minecraft:player]");
        server.runCommand("effect clear @a minecraft:poison");
        server.runCommand("gamemode creative @a");
        summonStill(server, "mauve_stinger", x + 0.5, y - 6, z + 0.5);
        String creative = touch(context, server, pool, MimJellyfish.MAUVE_STINGER, 0.0, 20.0F);
        log("a creative player touching a mauve stinger: " + creative);
        check(creative.contains("poison=none") && creative.contains("by nothing"), "creative should not be stung: " + creative);
        server.runCommand("gamemode survival @a");

        // Jellyfish Ward: no sting from the mauve stinger
        server.runCommand("kill @e[type=!minecraft:player]");
        server.runCommand("effect give @a mimcontent:jellyfish_ward 120 0 true");
        context.waitTicks(25);
        summonStill(server, "mauve_stinger", x + 0.5, y - 6, z + 0.5);
        String ward = touch(context, server, pool, MimJellyfish.MAUVE_STINGER, 0.0, 20.0F);
        log("a survival player with Jellyfish Ward touching a mauve stinger: " + ward);
        check(ward.contains("poison=none") && ward.contains("by nothing"), "the ward should block the mauve stinger: " + ward);

        // the fried-egg: harmless
        server.runCommand("kill @e[type=!minecraft:player]");
        server.runCommand("effect clear @a");
        server.runCommand("effect give @a minecraft:water_breathing 600 0 true");
        summonStill(server, "fried_egg_jellyfish", x + 0.5, y - 6, z + 0.5);
        String egg = touch(context, server, pool, MimJellyfish.FRIED_EGG, 0.0, 20.0F);
        log("a survival player touching a fried-egg jellyfish: " + egg);
        check(egg.contains("poison=none") && egg.startsWith("health 20.0"), "the fried-egg should not sting: " + egg);

        // the man o' war: its tentacles 2.5 blocks under the float sting, never below 1 heart, with nausea
        server.runCommand("kill @e[type=!minecraft:player]");
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:man_o_war %.1f %.2f %.1f {PersistenceRequired:1b}", x + 0.5, surface - Jellyfish.FLOAT_DRAFT, z + 0.5));
        context.waitTicks(25);
        String war = touch(context, server, pool, MimJellyfish.MAN_O_WAR, -2.5 - 1.8, 20.0F);
        log("a survival player 2.5 blocks under a man o' war: " + war);
        check(war.startsWith("health 17.0") && war.contains("by man_o_war") && war.contains("nausea=" + Jellyfish.MAN_O_WAR_NAUSEA_SECONDS + "s"),
            "the man o' war's tentacles: 3 damage, poison and nausea: " + war);
        check(war.contains("poison=" + Jellyfish.MAN_O_WAR_POISON_SECONDS + "s"), "man o' war poison 8 s: " + war);
        server.runCommand("effect clear @a");
        server.runCommand("effect give @a minecraft:water_breathing 600 0 true");
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x - 6, y - 10, z - 6));
        context.waitTicks(Jellyfish.STING_COOLDOWN + 5);
        String low = touch(context, server, pool, MimJellyfish.MAN_O_WAR, -1.0 - 1.8, 3.0F);
        log("a survival player at 1.5 hearts stung by a man o' war: " + low);
        check(low.startsWith("health 2.0") || low.startsWith("health 1.0"), "a sting should never take a player below 1 heart: " + low);
        check(low.contains("by man_o_war"), "the low-health player should be stung: " + low);
        // and with the ward, the man o' war doesn't sting either
        server.runCommand("effect clear @a");
        server.runCommand("effect give @a minecraft:water_breathing 600 0 true");
        server.runCommand("effect give @a mimcontent:jellyfish_ward 120 0 true");
        server.runCommand(String.format(Locale.ROOT, "tp @a %d %d %d", x - 6, y - 10, z - 6));
        context.waitTicks(Jellyfish.STING_COOLDOWN + 5);
        String warWard = touch(context, server, pool, MimJellyfish.MAN_O_WAR, -2.5 - 1.8, 20.0F);
        log("a survival player with Jellyfish Ward under a man o' war: " + warWard);
        check(warWard.contains("poison=none") && warWard.contains("nausea=none") && warWard.startsWith("health 20.0"), "the ward should block the man o' war: " + warWard);
        server.runCommand("kill @e[type=!minecraft:player]");
        server.runCommand("effect clear @a");
        server.runCommand("gamemode creative @a");
    }

    private static void summonStill(TestServerContext server, String id, double x, double y, double z) {
        server.runCommand(String.format(Locale.ROOT, "summon mimcontent:%s %.2f %.2f %.2f {NoAI:1b,PersistenceRequired:1b}", id, x, y, z));
    }

    /** Puts the player at the jellyfish (dy blocks above its feet), at the given health; waits up to 1 s for a sting. */
    private static String touch(ClientGameTestContext context, TestServerContext server, AABB pool, MimJellyfish.Jelly jelly, double dy, float health) {
        String at = server.computeOnServer(s -> {
            Jellyfish e = s.overworld().getEntities(jelly.type(), pool, j -> true).getFirst();
            ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
            player.setHealth(health);
            player.setLastHurtByMob(null);
            player.teleportTo(e.getX(), e.getY() + dy, e.getZ());
            player.setDeltaMovement(0, 0, 0);
            return "";
        });
        String state = at;
        for (int t = 0; t < 40; t += 2) {
            context.waitTicks(2);
            // the player is pushed off the jellyfish (and drifts in the water), so it is held there while it waits
            state = server.computeOnServer(s -> {
                Jellyfish e = s.overworld().getEntities(jelly.type(), pool, j -> true).getFirst();
                ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                String now = state(player);
                if (now.contains("poison=none")) {
                    player.teleportTo(e.getX(), e.getY() + dy, e.getZ());
                    player.setDeltaMovement(0, 0, 0);
                }
                return now;
            });
            if (!state.contains("poison=none")) {
                break;
            }
        }
        if (state.contains("poison=none")) {
            log(server.computeOnServer(s -> {
                Jellyfish e = s.overworld().getEntities(jelly.type(), pool, j -> true).getFirst();
                ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                return "  (no sting: " + jelly.id() + " box " + e.touchBox() + ", player box " + player.getBoundingBox() + ", " + player.gameMode() + ")";
            }));
        }
        return state;
    }

    /** Health, poison and nausea in whole seconds left (rounded up), and who hurt it last. */
    private static String state(LivingEntity e) {
        var poison = e.getEffect(MobEffects.POISON);
        var nausea = e.getEffect(MobEffects.NAUSEA);
        var by = e.getLastHurtByMob();
        return String.format(Locale.ROOT, "health %.1f, poison=%s, nausea=%s, hurt %s", e.getHealth(),
            poison == null ? "none" : (poison.getDuration() + 19) / 20 + "s", nausea == null ? "none" : (nausea.getDuration() + 19) / 20 + "s",
            by == null ? "by nothing" : "by " + BuiltInRegistries.ENTITY_TYPE.getKey(by.getType()).getPath());
    }

    /** Kills many of each and counts the drops: venom and meat in their ranges (no looting). */
    private static void drops(ClientGameTestContext context, TestServerContext server, int x, int y, int z, AABB pool) {
        int n = 20;
        String[][] want = {
            {"mauve_stinger", "mimcontent:jellyfish_venom", "0", "1", "mimcontent:jellyfish_meat", "1", "2"},
            {"man_o_war", "mimcontent:jellyfish_venom", "1", "2", "mimcontent:jellyfish_meat", "1", "2"},
            {"fried_egg_jellyfish", "mimcontent:jellyfish_venom", "0", "0", "mimcontent:jellyfish_meat", "2", "3"}};
        for (String[] w : want) {
            server.runCommand("kill @e[type=item]");
            for (int i = 0; i < n; i++) {
                summonStill(server, w[0], x - 5 + (i % 5) * 2.5, y - 4 - (i / 5) * 2, z + 0.5);
            }
            context.waitTicks(2);
            server.runCommand("kill @e[type=mimcontent:" + w[0] + "]");
            context.waitTicks(5);
            Map<String, Integer> counts = server.computeOnServer(s -> {
                Map<String, Integer> out = new TreeMap<>();
                for (ItemEntity item : s.overworld().getEntitiesOfClass(ItemEntity.class, pool)) {
                    out.merge(BuiltInRegistries.ITEM.getKey(item.getItem().getItem()).toString(), item.getItem().getCount(), Integer::sum);
                }
                return out;
            });
            log(w[0] + " x" + n + " dropped " + counts);
            for (int k = 1; k < 7; k += 3) {
                int got = counts.getOrDefault(w[k], 0);
                int lo = Integer.parseInt(w[k + 1]) * n, hi = Integer.parseInt(w[k + 2]) * n;
                check(got >= lo && got <= hi, w[0] + " should drop " + lo + " to " + hi + " " + w[k] + " from " + n + ", dropped " + got);
                if (hi > lo) {
                    check(got > lo && got < hi, w[0] + ": " + w[k] + " count " + got + " is at the edge of " + lo + " to " + hi + " (not random?)");
                }
            }
            check(counts.keySet().stream().allMatch(k -> k.equals(w[1]) || k.equals(w[4])), w[0] + " dropped something else: " + counts);
        }
        server.runCommand("kill @e[type=item]");
    }

    /** A real brewing stand: venom on awkward and thick potions, then redstone on the ward. */
    private static void brewing(ClientGameTestContext context, TestServerContext server, int x, int y, int z) {
        BlockPos stand = new BlockPos(x - 8, y + 1, z + 9);
        server.runCommand(String.format("setblock %d %d %d minecraft:stone", stand.getX(), stand.getY() - 1, stand.getZ()));
        server.runCommand(String.format("setblock %d %d %d minecraft:brewing_stand", stand.getX(), stand.getY(), stand.getZ()));
        context.waitTicks(2);
        String first = brew(context, server, stand, new ItemStack(MimJellyfish.VENOM),
            PotionContents.createItemStack(Items.POTION, Potions.AWKWARD),
            PotionContents.createItemStack(Items.POTION, Potions.THICK),
            PotionContents.createItemStack(Items.SPLASH_POTION, Potions.THICK));
        log("brewing jellyfish venom into awkward potion, thick potion, thick splash potion gives: " + first);
        check(first.equals("minecraft:potion minecraft:poison, minecraft:potion mimcontent:jellyfish_ward, minecraft:splash_potion mimcontent:jellyfish_ward"),
            "venom brews: " + first);
        String second = brew(context, server, stand, new ItemStack(Items.REDSTONE),
            PotionContents.createItemStack(Items.POTION, MimJellyfish.WARD_POTION),
            PotionContents.createItemStack(Items.POTION, Potions.POISON),
            PotionContents.createItemStack(Items.POTION, MimJellyfish.WARD_POTION));
        log("then redstone on ward, poison, ward gives: " + second);
        check(second.equals("minecraft:potion mimcontent:long_jellyfish_ward, minecraft:potion minecraft:long_poison, minecraft:potion mimcontent:long_jellyfish_ward"),
            "redstone on the ward: " + second);
        int[] durations = server.computeOnServer(s -> new int[] {MimJellyfish.WARD_POTION.value().getEffects().getFirst().getDuration(),
            MimJellyfish.LONG_WARD_POTION.value().getEffects().getFirst().getDuration()});
        log("Jellyfish Ward lasts " + durations[0] / 20 + " s, long " + durations[1] / 20 + " s");
        server.runCommand(String.format("setblock %d %d %d minecraft:air", stand.getX(), stand.getY(), stand.getZ()));
    }

    private static String brew(ClientGameTestContext context, TestServerContext server, BlockPos pos, ItemStack reagent, ItemStack... bottles) {
        server.runOnServer(s -> {
            BrewingStandBlockEntity be = (BrewingStandBlockEntity) s.overworld().getBlockEntity(pos);
            for (int i = 0; i < 3; i++) {
                be.setItem(i, bottles[i].copy());
            }
            be.setItem(3, reagent.copy());
            be.setItem(4, new ItemStack(Items.BLAZE_POWDER));
            be.setChanged();
        });
        String out = "";
        for (int t = 0; t < 900; t += 20) {
            context.waitTicks(20);
            boolean done = server.computeOnServer(s -> ((BrewingStandBlockEntity) s.overworld().getBlockEntity(pos)).getItem(3).isEmpty());
            if (done) {
                break;
            }
        }
        out = server.computeOnServer(s -> {
            BrewingStandBlockEntity be = (BrewingStandBlockEntity) s.overworld().getBlockEntity(pos);
            List<String> names = new ArrayList<>();
            for (int i = 0; i < 3; i++) {
                ItemStack st = be.getItem(i);
                String potion = st.getOrDefault(DataComponents.POTION_CONTENTS, PotionContents.EMPTY).potion()
                    .flatMap(Holder::unwrapKey).map(k -> k.identifier().toString()).orElse("none");
                names.add(BuiltInRegistries.ITEM.getKey(st.getItem()) + " " + potion);
            }
            return String.join(", ", names);
        });
        return out;
    }

    /** The meat: food with its numbers, no cooking recipe, in the bait tag. */
    private static void meat(TestServerContext server) {
        String result = server.computeOnServer(s -> {
            ItemStack meat = new ItemStack(MimJellyfish.MEAT);
            List<String> cooking = new ArrayList<>();
            int cookingRecipes = 0;
            for (var holder : s.getRecipeManager().getRecipes()) {
                if (holder.value() instanceof AbstractCookingRecipe recipe) {
                    cookingRecipes++;
                    if (recipe.input().test(meat)) {
                        cooking.add(holder.id().identifier().toString());
                    }
                }
            }
            var food = meat.get(DataComponents.FOOD);
            boolean bait = meat.is(net.minecraft.tags.TagKey.create(net.minecraft.core.registries.Registries.ITEM, com.maltaminecraft.mimcontent.MimContent.id("bait")));
            return String.format(Locale.ROOT, "food %s hunger %d saturation %.2f; of %d cooking recipes, %s take it; bait tag %s",
                food != null, food == null ? 0 : food.nutrition(), food == null ? 0 : food.saturation(), cookingRecipes,
                cooking.isEmpty() ? "none" : cooking, bait);
        });
        log("jellyfish meat: " + result);
        check(result.startsWith("food true hunger 2 ") && result.contains("none take it") && result.endsWith("bait tag true"), "jellyfish meat: " + result);
    }

    private static void vanillaOceanSpawns(TestServerContext server) {
        String result = server.computeOnServer(s -> {
            var biomes = s.registryAccess().lookupOrThrow(net.minecraft.core.registries.Registries.BIOME);
            StringBuilder out = new StringBuilder();
            Map<MimJellyfish.Jelly, List<net.minecraft.resources.ResourceKey<net.minecraft.world.level.biome.Biome>>> want = Map.of(
                MimJellyfish.MAUVE_STINGER, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN, Biomes.DEEP_LUKEWARM_OCEAN),
                MimJellyfish.FRIED_EGG, List.of(Biomes.WARM_OCEAN, Biomes.LUKEWARM_OCEAN),
                MimJellyfish.MAN_O_WAR, List.of(Biomes.DEEP_LUKEWARM_OCEAN));
            var attribute = net.minecraft.world.attribute.EnvironmentAttributes.NATURAL_MOB_SPAWNS;
            for (var e : want.entrySet()) {
                for (var key : e.getValue()) {
                    var spawns = biomes.getValue(key).getAttributes().applyModifier(attribute, attribute.defaultValue());
                    if (spawns.getMobsToSpawn(MobCategory.WATER_AMBIENT).unwrap().stream().noneMatch(w -> w.value().type() == e.getKey().type())) {
                        out.append(e.getKey().id()).append(" missing from ").append(key.identifier()).append("; ");
                    }
                }
                var cold = biomes.getValue(Biomes.COLD_OCEAN).getAttributes().applyModifier(attribute, attribute.defaultValue());
                if (cold.getMobsToSpawn(MobCategory.WATER_AMBIENT).unwrap().stream().anyMatch(w -> w.value().type() == e.getKey().type())) {
                    out.append(e.getKey().id()).append(" in cold ocean; ");
                }
            }
            return out.isEmpty() ? "ok" : out.toString();
        });
        log("jellyfish spawns in vanilla oceans: " + result);
        check(result.equals("ok"), "spawns: " + result);
    }

    /**
     * The art review: a glass tank of water; each jellyfish alone beside a vanilla cod and squid, from the side, three
     * quarters and below; then all three together; then a mauve stinger flashing at night.
     */
    private static void shots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int x, int y, int z) {
        server.runCommand("time set 6000");
        server.runCommand("gamerule send_command_feedback false");
        // the tank: glass x-6..x+6, z+4..z+10, y..y+8; water inside y+1..y+7 (surface about y+7.9), open at the top
        fill(server, x - 8, y - 1, z - 6, x + 8, y + 14, z + 12, "minecraft:air");
        fill(server, x - 8, y - 1, z - 6, x + 8, y - 1, z + 12, "minecraft:smooth_sandstone");
        fill(server, x - 6, y, z + 4, x + 6, y + 8, z + 10, "minecraft:glass");
        fill(server, x - 5, y + 1, z + 5, x + 5, y + 8, z + 9, "minecraft:air");
        fill(server, x - 5, y + 1, z + 5, x + 5, y + 7, z + 9, "minecraft:water");
        world.getConnection().waitForChunksRender();
        double top = y + 7 + 0.8889;
        for (MimJellyfish.Jelly j : MimJellyfish.ALL) {
            server.runCommand("kill @e[type=!minecraft:player]");
            double jy = j.kind().floats() ? top - Jellyfish.FLOAT_DRAFT : y + 3.5;
            summonStill(server, j.id(), x + 0.5, jy, z + 7.0);
            server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}", x - 1.3, y + 3.0, z + 7.5));
            server.runCommand(String.format(Locale.ROOT, "summon minecraft:squid %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b}", x + 3.2, y + 3.0, z + 8.5));
            context.waitTicks(30);
            server.runCommand("gamemode spectator @a");
            double ty = j.kind().floats() ? top - 1.9 : y + 4.0;
            double camY = j.kind().floats() ? y + 5.6 : y + 2.6;
            look(context, server, x + 0.5, camY - 1.62 + 1.0, z + 4.4, x + 0.5, ty, z + 7.0, "jelly-" + j.id() + "-side");
            look(context, server, x - 1.6, camY - 1.62 + 1.6, z + 4.4, x + 0.5, ty, z + 7.0, "jelly-" + j.id() + "-three-quarter");
            look(context, server, x + 0.9, y - 1.62 + 0.4, z + 6.2, x + 0.5, j.kind().floats() ? top : y + 4.0, z + 7.0, "jelly-" + j.id() + "-below");
            server.runCommand("gamemode creative @a");
        }
        // all three together, with the cod and squid, at the back of the tank; the camera sits inside the front glass
        // wall, so it looks through no glass
        server.runCommand("kill @e[type=!minecraft:player]");
        summonStill(server, "mauve_stinger", x - 1.8, y + 3.6, z + 8.3);
        summonStill(server, "fried_egg_jellyfish", x + 0.5, y + 2.0, z + 8.3);
        summonStill(server, "man_o_war", x + 2.0, top - Jellyfish.FLOAT_DRAFT, z + 8.3);
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:cod %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b,Rotation:[90f,0f]}", x - 3.4, y + 2.0, z + 8.0));
        server.runCommand(String.format(Locale.ROOT, "summon minecraft:squid %.1f %.1f %.1f {NoAI:1b,PersistenceRequired:1b}", x - 0.6, y + 5.6, z + 8.7));
        context.waitTicks(30);
        server.runCommand("gamemode spectator @a");
        look(context, server, x + 0.0, y + 4.0 - 1.62, z + 4.45, x + 0.0, y + 4.9, z + 8.3, "jelly-group");
        // the mauve stinger's flash at night
        server.runCommand("time set 18000");
        context.waitTicks(10);
        server.runOnServer(s -> {
            ServerLevel level = s.overworld();
            level.getEntities(MimJellyfish.MAUVE_STINGER.type(), new AABB(x - 6, y, z + 4, x + 6, y + 9, z + 10), e -> true).forEach(j -> j.flash(level));
        });
        context.waitTicks(4);
        look(context, server, x - 1.8, y + 3.4 - 1.62, z + 4.45, x - 1.8, y + 4.4, z + 8.3, "jelly-mauve_stinger-flash-night");
        server.runCommand("gamemode creative @a");
        server.runCommand("time set 6000");
    }

    private static void look(ClientGameTestContext context, TestServerContext server,
                             double fx, double fy, double fz, double tx, double ty, double tz, String name) {
        double dx = tx - fx, dy = ty - (fy + 1.62), dz = tz - fz;
        float yaw = (float) Math.toDegrees(Math.atan2(-dx, dz));
        float pitch = (float) -Math.toDegrees(Math.atan2(dy, Math.sqrt(dx * dx + dz * dz)));
        server.runCommand(String.format(Locale.ROOT, "tp @a %.2f %.2f %.2f %.1f %.1f", fx, fy, fz, yaw, pitch));
        context.waitTicks(15);
        context.takeScreenshot(name);
    }

    private static void fill(TestServerContext server, int x0, int y0, int z0, int x1, int y1, int z1, String block) {
        server.runCommand(String.format("fill %d %d %d %d %d %d %s", x0, y0, z0, x1, y1, z1, block));
    }

    private static void check(boolean ok, String message) {
        if (!ok) {
            throw new AssertionError("[smoke] jelly: " + message);
        }
    }

    private static void log(String message) {
        System.out.println("[smoke] jelly: " + message);
    }
}
