package com.maltaminecraft.mimcontent.test;

import com.maltaminecraft.mimcontent.MimFishes;
import com.maltaminecraft.mimcontent.client.fish.FishModel;
import com.maltaminecraft.mimcontent.client.fish.FishRenderer;
import com.maltaminecraft.mimcontent.entity.fish.FishPart;
import com.maltaminecraft.mimcontent.entity.fish.FishParts;
import com.maltaminecraft.mimcontent.entity.fish.FishShape;
import com.maltaminecraft.mimcontent.entity.fish.TonnFish;
import com.mojang.blaze3d.vertex.PoseStack;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.components.debug.DebugScreenEntries;
import net.minecraft.client.gui.components.debug.DebugScreenEntryStatus;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySelector;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.animal.fish.AbstractFish;
import net.minecraft.world.entity.projectile.ProjectileUtil;
import net.minecraft.world.entity.projectile.arrow.Arrow;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.Vec3;
import org.joml.Matrix4f;
import org.joml.Vector3f;

/**
 * The fish's chains of hit boxes (owner 2026-11-18: "hitboxes for all fish should match their actual size"), part of
 * the fish check (SMOKE_ONLY=fish):
 * <ol>
 * <li>the table in FishShape still matches every fish's model (measured again from the baked model), and the land
 *     lift matches the renderer's; the murina's boxes follow its model's wave;</li>
 * <li>for the shark, the swordfish, a 3.6-block tonn and the murina, turned at an angle: the client's own crosshair
 *     pick (ProjectileUtil, as the game uses it) finds the snout box from in front and the tail box from behind, a
 *     hit there through the game's attack (packet, server reach check) hurts the fish, and a line 0.8 blocks beside
 *     the body hits nothing (the fish's own square box, which it would have crossed, is not aimed at any more);</li>
 * <li>client and server agree on every part's id;</li>
 * <li>a water bucket used on a part (the murina's tail, the swordfish's sword) catches the fish;</li>
 * <li>an arrow dropped on the tail of a shark lying on land hurts it;</li>
 * <li>the boll, lingwata and petriċa (flat) lie flat on land: their boxes stay on the ground, as thin as the fish;</li>
 * <li>the mola mola lying on its side on land: its boxes lie flat on the ground and centred over it (the side shift);</li>
 * <li>screenshots with hit boxes shown (F3+B): fish-hitbox-*.</li>
 * </ol>
 */
final class FishHitboxCheck {
    private static final String[] HIT_FISH = {"huta_kahla", "pixxispad", "tonn", "murina"};
    private static final float YAW = 30.0F;
    private static final float TONN_LENGTH = 3.6F;

    private FishHitboxCheck() {
    }

    static void run(ClientGameTestContext context) {
        try (TestSingleplayerContext world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            tableMatchesModels(context, MimFishes.ALL);
            murinaWave(context);
            TestServerContext server = world.getServer();
            server.runCommand("gamemode creative @a");
            server.runCommand("gamerule spawn_mobs false");
            server.runCommand("gamerule advance_time false");
            server.runCommand("time set 6000");
            server.runCommand("effect give @a minecraft:water_breathing 600 0 true");
            server.runCommand("effect give @a minecraft:resistance 600 4 true");
            // the player hangs where it is put, so each line of sight starts where it was aimed from
            server.runCommand("attribute @a minecraft:gravity base set 0");
            int[] p = context.computeOnClient(mc -> new int[] {mc.player.getBlockX(), mc.player.getBlockY(), mc.player.getBlockZ()});
            int x = p[0], y = p[1] + 30, z = p[2];
            fill(server, x - 22, y - 9, z - 8, x + 22, y + 4, z + 8, "minecraft:air");
            fill(server, x - 21, y - 8, z - 7, x + 21, y, z + 7, "minecraft:stone");
            fill(server, x - 20, y - 7, z - 6, x + 20, y - 1, z + 6, "minecraft:water");
            server.runCommand(String.format("tp @a %d %d %d", x, y + 1, z - 7));
            world.getConnection().waitForChunksRender();

            List<UUID> fish = new ArrayList<>();
            for (int i = 0; i < HIT_FISH.length; i++) {
                fish.add(spawn(server, HIT_FISH[i], x - 15 + 10 * i + 0.5, y - 4.5, z + 0.5, YAW, true));
            }
            context.waitTicks(20);
            for (int i = 0; i < HIT_FISH.length; i++) {
                ids(context, server, HIT_FISH[i], fish.get(i));
                hits(context, server, HIT_FISH[i], fish.get(i));
            }
            buckets(context, server, x, y, z);
            server.runCommand("kill @e[type=!minecraft:player]");
            arrow(context, server, x, y, z);
            server.runCommand("kill @e[type=!minecraft:player]");
            // the boll's thickest point is 3 px (the raised eyes on the dome; art/src/fish_boll_model.py);
            // the night job's flat fish: the lingwata 3 px with its raised pectoral fin; the petriċa lies flattened on land
            // (squashed to 0.45 of its height in the water), no more than 7 px with its lure
            flatOnLand(context, server, x, y, z, "boll", 3.0);
            server.runCommand("kill @e[type=!minecraft:player]");
            flatOnLand(context, server, x, y, z, "lingwata", 3.0);  // 3 px at the raised pectoral fin (art/src/fish_lingwata_model.py)
            server.runCommand("kill @e[type=!minecraft:player]");
            flatOnLand(context, server, x, y, z, "petrica", 7.0);
            server.runCommand("kill @e[type=!minecraft:player]");
            molaOnLand(context, server, x, y, z);
            server.runCommand("attribute @a minecraft:gravity base reset");
            server.runCommand("gamemode creative @a");
            server.runCommand("kill @e[type=!minecraft:player]");
            shots(context, server, world, p[0], p[1], p[2]);
        }
        log("all hitbox checks passed");
    }

    /**
     * SMOKE_ONLY=fish-one: only one fish's row of the table, checked against its model as above. Its measured row is
     * always logged, ready to copy into FishShape.
     */
    static void runOne(ClientGameTestContext context, MimFishes.Fish fish) {
        tableMatchesModels(context, List.of(fish));
        log(fish.id() + ": table row checked");
    }

    /** Measures every fish's baked model the way FishShape's table was made, and compares. */
    private static void tableMatchesModels(ClientGameTestContext context, List<MimFishes.Fish> fishes) {
        String result = context.computeOnClient(mc -> {
            StringBuilder bad = new StringBuilder();
            for (MimFishes.Fish f : fishes) {
                FishRenderer renderer = renderer(mc, f);
                FishModel model = renderer.getModel();
                model.resetPose();
                List<float[]> cubes = new ArrayList<>();
                model.root().visit(new PoseStack(), (pose, path, index, cube) -> cubes.add(bounds(pose.pose(), cube)));
                float[][] measured = FishShape.slice(cubes);
                FishShape shape = FishShape.of(f.id());
                String problem = shape == null ? "no shape" : compare(shape, measured, renderer.landLift(), renderer.liesFlat(), renderer.sideShift(), renderer.landSquash());
                float length = measured[0][0] * (measured.length - 1);
                log(String.format(Locale.ROOT, "%s model: %.1f px long; %d hit boxes of %.2f px; table %s", f.id(), length,
                    measured.length - 1, measured[0][0], problem == null ? "matches" : "WRONG: " + problem));
                if (fishes.size() == 1) {
                    log(String.format(Locale.ROOT, "%s measured row: %s; land lift %sF, flat %s, side shift %sF, land squash %sF", f.id(), row(measured),
                        renderer.landLift(), renderer.liesFlat(), renderer.sideShift(), renderer.landSquash()));
                }
                if (problem != null) {
                    bad.append(f.id()).append(": ").append(problem).append("; the row should be ").append(row(measured)).append(". ");
                }
            }
            return bad.isEmpty() ? "ok" : bad.toString();
        });
        check(result.equals("ok"), "FishShape's table is out of date: " + result);
    }

    private static String compare(FishShape shape, float[][] measured, float landLift, boolean liesFlat, float sideShift, float landSquash) {
        if (Math.abs(shape.landLift() - landLift) > 1.0E-5F) {
            return "land lift " + shape.landLift() + ", the renderer's is " + landLift;
        }
        if (Math.abs(shape.sideShift() - sideShift) > 1.0E-5F) {
            return "side shift " + shape.sideShift() + ", the renderer's is " + sideShift;
        }
        if (shape.flat() != liesFlat) {
            return "flat " + shape.flat() + ", the renderer's liesFlat is " + liesFlat;
        }
        if (Math.abs(shape.landSquash() - landSquash) > 1.0E-5F) {
            return "land squash " + shape.landSquash() + ", the renderer's is " + landSquash;
        }
        if (shape.parts() != measured.length - 1 || Math.abs(shape.sliceLength() - measured[0][0]) > 0.02F) {
            return shape.parts() + " slices of " + shape.sliceLength() + " px, the model gives " + (measured.length - 1) + " of " + measured[0][0];
        }
        for (int i = 0; i < shape.parts(); i++) {
            for (int k = 0; k < 4; k++) {
                if (Math.abs(shape.slices()[i][k] - measured[i + 1][k]) > 0.02F) {
                    return "slice " + i + " is " + java.util.Arrays.toString(shape.slices()[i]) + ", the model gives " + java.util.Arrays.toString(measured[i + 1]);
                }
            }
        }
        return null;
    }

    private static String row(float[][] measured) {
        StringBuilder out = new StringBuilder(String.format(Locale.ROOT, "%.3fF, {", measured[0][0]));
        for (int i = 1; i < measured.length; i++) {
            out.append(String.format(Locale.ROOT, "%s{%.3fF, %.3fF, %.3fF, %.3fF}", i > 1 ? ", " : "", measured[i][0], measured[i][1], measured[i][2], measured[i][3]));
        }
        return out.append("}").toString();
    }

    /** A cube's bounds in model px, after its part's pose (rotations included). */
    private static float[] bounds(Matrix4f pose, ModelPart.Cube cube) {
        float[] out = {Float.MAX_VALUE, Float.MAX_VALUE, Float.MAX_VALUE, -Float.MAX_VALUE, -Float.MAX_VALUE, -Float.MAX_VALUE};
        for (int c = 0; c < 8; c++) {
            Vector3f v = pose.transformPosition(((c & 1) == 0 ? cube.minX : cube.maxX) / 16.0F,
                ((c & 2) == 0 ? cube.minY : cube.maxY) / 16.0F, ((c & 4) == 0 ? cube.minZ : cube.maxZ) / 16.0F, new Vector3f());
            float[] px = {v.x * 16.0F, v.y * 16.0F, v.z * 16.0F};
            for (int k = 0; k < 3; k++) {
                out[k] = Math.min(out[k], px[k]);
                out[k + 3] = Math.max(out[k + 3], px[k]);
            }
        }
        return out;
    }

    /**
     * The murina's boxes against its model's own wave: at several moments, in water and on land, each box's centre
     * must sit where the bent model puts that point of the body.
     */
    private static void murinaWave(ClientGameTestContext context) {
        String result = context.computeOnClient(mc -> {
            FishModel model = renderer(mc, MimFishes.MURINA).getModel();
            FishShape shape = FishShape.of("murina");
            String[] names = {"body", "seg1", "seg2", "seg3", "tail"};
            model.resetPose();
            Matrix4f[] rest = sections(model.root(), names);
            float worst = 0.0F;
            for (boolean inWater : new boolean[] {true, false}) {
                for (float age : new float[] {0.0F, 3.0F, 7.3F, 13.0F, 21.6F, 40.0F}) {
                    model.resetPose();
                    LivingEntityRenderState state = new LivingEntityRenderState();
                    state.isInWater = inWater;
                    state.ageInTicks = age;
                    model.setupAnim(state);
                    Matrix4f[] bent = sections(model.root(), names);
                    for (int i = 0; i < shape.parts(); i++) {
                        float z = shape.slices()[i][0];
                        int s = 0;
                        for (int k = 1; k < names.length; k++) {
                            if (z >= rest[k].m32() * 16.0F) {
                                s = k;
                            }
                        }
                        Vector3f want = bent[s].transformPosition(0.0F, 0.0F, (z - rest[s].m32() * 16.0F) / 16.0F, new Vector3f()).mul(16.0F);
                        AABB box = shape.box(i, Vec3.ZERO, 0.0F, 1.0F, inWater, age);
                        Vec3 c = box.getCenter();
                        // undo FishShape's placement at yaw 0 (see FishShape.box) to get back model px
                        float gotX = inWater ? (float) c.x * 16.0F : (shape.landLift() - (float) c.y) * 16.0F;
                        float gotZ = inWater ? (float) -c.z * 16.0F : (0.1F - (float) c.z) * 16.0F;
                        worst = Math.max(worst, Math.max(Math.abs(gotX - want.x), Math.abs(gotZ - want.z)));
                    }
                }
            }
            model.resetPose();
            return String.format(Locale.ROOT, "%.3f", worst);
        });
        log("murina boxes follow its wave: largest gap " + result + " px");
        check(Float.parseFloat(result) < 0.25F, "the murina's boxes don't follow its wave (gap " + result + " px)");
    }

    private static Matrix4f[] sections(ModelPart root, String[] names) {
        PoseStack stack = new PoseStack();
        root.translateAndRotate(stack);
        Matrix4f[] out = new Matrix4f[names.length];
        ModelPart part = root;
        for (int i = 0; i < names.length; i++) {
            part = part.getChild(names[i]);
            part.translateAndRotate(stack);
            out[i] = new Matrix4f(stack.last().pose());
        }
        return out;
    }

    private static FishRenderer renderer(Minecraft mc, MimFishes.Fish f) {
        Entity e = f.type().create(mc.level, EntitySpawnReason.LOAD);
        return (FishRenderer) (Object) mc.getEntityRenderDispatcher().getRenderer(e);
    }

    /** Spawns one of our fish without AI, turned to the given yaw; the tonn at TONN_LENGTH. */
    private static UUID spawn(TestServerContext server, String id, double x, double y, double z, float yaw, boolean persist) {
        return server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            AbstractFish fish = (AbstractFish) fish(id).type().create(level, EntitySpawnReason.COMMAND);
            fish.snapTo(x, y, z, yaw, 0.0F);
            fish.setYHeadRot(yaw);
            fish.setYBodyRot(yaw);
            fish.setNoAi(true);
            fish.setPersistenceRequired();
            if (fish instanceof TonnFish tonn) {
                tonn.setLength(TONN_LENGTH);
                tonn.setHealth(tonn.getMaxHealth());
            }
            level.addFreshEntity(fish);
            return fish.getUUID();
        });
    }

    private static MimFishes.Fish fish(String id) {
        return MimFishes.ALL.stream().filter(f -> f.id().equals(id)).findFirst().orElseThrow();
    }

    /** The client's parts carry the same ids as the server's, and the server finds each part by its id. */
    private static void ids(ClientGameTestContext context, TestServerContext server, String id, UUID uuid) {
        String client = context.computeOnClient(mc -> partIds(clientFish(mc, uuid)));
        String onServer = server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            AbstractFish fish = (AbstractFish) level.getEntity(uuid);
            for (FishPart part : ((FishParts.Holder) fish).mimcontent$parts().parts()) {
                if (level.getEntityOrPart(part.getId()) != part) {
                    return "the server can't find part " + part.index + " by its id";
                }
            }
            return partIds(fish);
        });
        log(id + " part ids: client " + client + ", server " + onServer);
        check(client.equals(onServer), id + ": client and server part ids differ");
    }

    private static String partIds(AbstractFish fish) {
        StringBuilder out = new StringBuilder("fish " + fish.getId() + ", parts");
        for (FishPart part : ((FishParts.Holder) fish).mimcontent$parts().parts()) {
            out.append(' ').append(part.getId());
        }
        return out.toString();
    }

    private static AbstractFish clientFish(Minecraft mc, UUID uuid) {
        for (Entity e : mc.level.entitiesForRendering()) {
            if (e.getUUID().equals(uuid)) {
                return (AbstractFish) e;
            }
        }
        throw new AssertionError("[smoke] fish: the client has no fish " + uuid);
    }

    /** A point on the fish's centre line at model z (px) and model height y (px), for the fish as the client draws it in water. */
    private static Vec3 onBody(AbstractFish fish, float zPx, float yPx) {
        double yaw = Math.toRadians(fish.yBodyRot);
        Vec3 forward = new Vec3(-Math.sin(yaw), 0.0, Math.cos(yaw));
        float scale = fish.getScale();
        return fish.position().add(forward.scale(-zPx / 16.0 * scale)).add(0.0, (1.501 - yPx / 16.0) * scale, 0.0);
    }

    private static Vec3 forward(AbstractFish fish) {
        double yaw = Math.toRadians(fish.yBodyRot);
        return new Vec3(-Math.sin(yaw), 0.0, Math.cos(yaw));
    }

    /** Snout and tail hits (the client's pick, then the game's attack) hurt the fish; a line beside the body hits nothing. */
    private static void hits(ClientGameTestContext context, TestServerContext server, String id, UUID uuid) {
        FishShape shape = FishShape.of(id);
        float[][] rows = shape.slices();
        int last = rows.length - 1;
        float half = shape.sliceLength() / 2.0F;
        // aim 1.5 px inside each end, at the height of the end slice's middle
        float[] snout = {rows[0][0] - half + 1.5F, (rows[0][2] + rows[0][3]) / 2.0F};
        float[] tail = {rows[last][0] + half - 1.5F, (rows[last][2] + rows[last][3]) / 2.0F};
        String[] ends = {"snout", "tail"};
        float[][] aims = {snout, tail};
        int[] expect = {0, last};
        for (int e = 0; e < 2; e++) {
            int end = e;
            // stand 2 blocks off that end, in line with the body, looking at it
            Vec3[] ray = context.computeOnClient(mc -> {
                AbstractFish fish = clientFish(mc, uuid);
                Vec3 out = forward(fish).scale(end == 0 ? 1.0 : -1.0);
                Vec3 aim = onBody(fish, aims[end][0], aims[end][1]);
                if (shape.wave() != null) {
                    // the murina's body bends with its wave (checked above): aim along the end box's own line
                    Vec3 centre = ((FishParts.Holder) fish).mimcontent$parts().parts()[expect[end]].getBoundingBox().getCenter();
                    aim = centre.add(out.scale((half - 1.5) / 16.0 * fish.getScale()));
                }
                return new Vec3[] {aim.add(out.scale(2.0)), aim};
            });
            Vec3 eye = ray[0];
            server.runCommand(String.format(Locale.ROOT, "tp @a %.3f %.3f %.3f", eye.x, eye.y - 1.62, eye.z));
            server.runCommand("attribute @a minecraft:gravity base set 0");
            context.waitTicks(5);
            float before = health(server, uuid);
            String picked = context.computeOnClient(mc -> {
                Vec3 from = mc.player.getEyePosition();
                Vec3 to = from.add(ray[1].subtract(from).scale(1.3));
                EntityHitResult hit = ProjectileUtil.getEntityHitResult(mc.player, from, to, new AABB(from, to).inflate(1.0),
                    EntitySelector.CAN_BE_PICKED, from.distanceToSqr(to));
                if (hit == null) {
                    return "nothing";
                }
                if (!(hit.getEntity() instanceof FishPart part) || !part.fish.getUUID().equals(uuid)) {
                    return "something else: " + hit.getEntity();
                }
                mc.gameMode.attack(mc.player, part);
                return String.format(Locale.ROOT, "part %d at %.2f blocks", part.index, from.distanceTo(hit.getLocation()));
            });
            context.waitTicks(3);
            float after = health(server, uuid);
            log(String.format(Locale.ROOT, "%s, %s from in line: picked %s; health %.1f -> %.1f", id, ends[end], picked, before, after));
            check(picked.startsWith("part " + expect[end] + " "), id + ": the " + ends[end] + " should pick part " + expect[end] + ", got " + picked);
            check(after < before, id + ": a hit on the " + ends[end] + " did no damage");
            server.runOnServer(s -> {
                AbstractFish fish = (AbstractFish) s.overworld().getEntity(uuid);
                fish.setHealth(fish.getMaxHealth());
            });
            context.waitTicks(25);
        }
        // a line along the body, 0.8 blocks to its side at mid height: nothing to hit
        String beside = context.computeOnClient(mc -> {
            AbstractFish fish = clientFish(mc, uuid);
            Vec3 f = forward(fish);
            Vec3 side = new Vec3(f.z, 0.0, -f.x).scale(0.8);
            Vec3 mid = fish.getBoundingBox().getCenter().add(side);
            double reach = 3.0 * fish.getScale();
            Vec3 from = mid.add(f.scale(reach)), to = mid.subtract(f.scale(reach));
            EntityHitResult hit = ProjectileUtil.getEntityHitResult(mc.player, from, to, new AABB(from, to).inflate(1.0),
                EntitySelector.CAN_BE_PICKED, from.distanceToSqr(to));
            boolean oldBox = fish.getBoundingBox().clip(from, to).isPresent();
            String what = hit == null ? "nothing" : hit.getEntity() instanceof FishPart part && part.fish == fish ? "part " + part.index
                : hit.getEntity() == fish ? "the fish's own box" : "something else";
            return what + " (the fish's own box " + (oldBox ? "lies across that line" : "doesn't reach it") + ")";
        });
        log(id + ", a line 0.8 blocks beside the body: hit " + beside);
        check(beside.startsWith("nothing"), id + ": a line beside the body should hit nothing, hit " + beside);
    }

    private static float health(TestServerContext server, UUID uuid) {
        return server.computeOnServer(s -> ((AbstractFish) s.overworld().getEntity(uuid)).getHealth());
    }

    /** A water bucket used (the game's own use, through the packet) on a part far from the fish's own box catches it. */
    private static void buckets(ClientGameTestContext context, TestServerContext server, int x, int y, int z) {
        server.runCommand("gamemode survival @a");
        String[][] tries = {{"murina", "tail"}, {"pixxispad", "snout"}};
        for (String[] t : tries) {
            MimFishes.Fish f = fish(t[0]);
            UUID uuid = spawn(server, t[0], x + 0.5, y - 4.5, z + 0.5, 90.0F, true);
            context.waitTicks(10);
            FishShape shape = FishShape.of(t[0]);
            int index = t[1].equals("tail") ? shape.parts() - 1 : 0;
            Vec3[] ray = context.computeOnClient(mc -> {
                AbstractFish fish = clientFish(mc, uuid);
                AABB box = ((FishParts.Holder) fish).mimcontent$parts().parts()[index].getBoundingBox();
                Vec3 aim = box.getCenter();
                // from above-ish and to the side, so the line meets that part first
                Vec3 out = forward(fish).scale(index == 0 ? 1.5 : -1.5).add(0.0, 1.0, 0.0);
                return new Vec3[] {aim.add(out), aim, fish.getBoundingBox().contains(aim) ? new Vec3(1, 0, 0) : Vec3.ZERO};
            });
            server.runCommand(String.format(Locale.ROOT, "tp @a %.3f %.3f %.3f", ray[0].x, ray[0].y - 1.62, ray[0].z));
            server.runCommand("attribute @a minecraft:gravity base set 0");
            server.runCommand("item replace entity @a weapon.mainhand with minecraft:water_bucket");
            context.waitTicks(5);
            String used = context.computeOnClient(mc -> {
                Vec3 from = mc.player.getEyePosition();
                Vec3 to = from.add(ray[1].subtract(from).scale(1.3));
                EntityHitResult hit = ProjectileUtil.getEntityHitResult(mc.player, from, to, new AABB(from, to).inflate(1.0),
                    EntitySelector.CAN_BE_PICKED, from.distanceToSqr(to));
                if (hit == null || !(hit.getEntity() instanceof FishPart part) || !part.fish.getUUID().equals(uuid)) {
                    return "the line missed: " + (hit == null ? "nothing" : hit.getEntity());
                }
                mc.gameMode.interact(mc.player, part, hit, InteractionHand.MAIN_HAND);
                return "used on part " + part.index;
            });
            context.waitTicks(5);
            String result = server.computeOnServer(s -> {
                ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                ItemStack held = player.getItemInHand(InteractionHand.MAIN_HAND);
                Entity fish = s.overworld().getEntity(uuid);
                return "holding " + BuiltInRegistries.ITEM.getKey(held.getItem()) + ", fish " + (fish == null || fish.isRemoved() ? "caught" : "still in the water");
            });
            log(String.format("water bucket on the %s's %s (outside its own box: %s): %s; %s", t[0], t[1], ray[2].x == 0, used, result));
            check(used.equals("used on part " + index) && result.equals("holding " + BuiltInRegistries.ITEM.getKey(f.bucket()) + ", fish caught"),
                "bucketing at the " + t[1] + " of the " + t[0] + ": " + used + "; " + result);
            server.runCommand("clear @a");
        }
        server.runCommand("gamemode creative @a");
    }

    /** An arrow dropped onto the tail of a shark lying on land (outside its own box) hurts it. */
    private static void arrow(ClientGameTestContext context, TestServerContext server, int x, int y, int z) {
        fill(server, x - 4, y + 1, z - 4, x + 4, y + 6, z + 4, "minecraft:air");
        fill(server, x - 4, y, z - 4, x + 4, y, z + 4, "minecraft:smooth_sandstone");
        UUID uuid = spawn(server, "huta_kahla", x + 0.5, y + 1, z + 0.5, 0.0F, true);
        server.runCommand(String.format("tp @a %d %d %d", x + 3, y + 1, z - 3));
        context.waitTicks(20);
        String shot = server.computeOnServer(s -> {
            ServerLevel level = s.overworld();
            AbstractFish fish = (AbstractFish) level.getEntity(uuid);
            FishPart[] parts = ((FishParts.Holder) fish).mimcontent$parts().parts();
            AABB tail = parts[parts.length - 1].getBoundingBox();
            Vec3 aim = tail.getCenter();
            Arrow arrow = new Arrow(level, aim.x, aim.y + 2.5, aim.z, new ItemStack(Items.ARROW), null);
            arrow.setDeltaMovement(0.0, -1.5, 0.0);
            level.addFreshEntity(arrow);
            return String.format(Locale.ROOT, "on land=%s, tail box %.2f..%.2f high, outside its own box=%s",
                !fish.isInWater(), tail.minY - fish.getY(), tail.maxY - fish.getY(), !fish.getBoundingBox().intersects(tail));
        });
        float before = server.computeOnServer(s -> ((AbstractFish) s.overworld().getEntity(uuid)).getMaxHealth());
        float after = before;
        for (int t = 0; t < 20 && after >= before; t++) {
            context.waitTicks(1);
            after = health(server, uuid);
        }
        log(String.format(Locale.ROOT, "an arrow on the tail of a shark on land (%s): health %.1f -> %.1f", shot, before, after));
        check(shot.contains("on land=true") && shot.contains("outside its own box=true"), "the arrow test's set-up is off: " + shot);
        check(after < before, "an arrow on the shark's tail did no damage");
    }

    /** A flat fish (the boll) on land lies flat, as it swims: every box sits on the ground and is no taller than the fish. */
    private static void flatOnLand(ClientGameTestContext context, TestServerContext server, int x, int y, int z, String id, double thickPx) {
        UUID uuid = spawn(server, id, x + 0.5, y + 1, z + 0.5, 30.0F, true);
        context.waitTicks(20);
        String result = server.computeOnServer(s -> {
            AbstractFish fish = (AbstractFish) s.overworld().getEntity(uuid);
            double low = Double.MAX_VALUE, high = -Double.MAX_VALUE;
            for (FishPart part : ((FishParts.Holder) fish).mimcontent$parts().parts()) {
                AABB b = part.getBoundingBox();
                low = Math.min(low, b.minY - fish.getY());
                high = Math.max(high, b.maxY - fish.getY());
            }
            return String.format(Locale.ROOT, "on land=%s, boxes from %.3f to %.3f above its feet", !fish.isInWater(), low, high);
        });
        log("the " + id + " on land: " + result);
        check(result.contains("on land=true"), "the " + id + " should be on land: " + result);
        String[] nums = result.replaceAll(".*from ([-0-9.]+) to ([-0-9.]+).*", "$1 $2").split(" ");
        double low = Double.parseDouble(nums[0]), high = Double.parseDouble(nums[1]);
        // flat on the ground: its boxes start at its feet and reach no higher than the model's thickest point
        check(Math.abs(low) < 0.01 && high <= thickPx / 16.0 + 0.01, "the " + id + "'s boxes on land should lie flat on the ground: " + result);
    }

    /** Side views of the big fish with hit boxes shown (F3+B): the white box moves the fish, the green-yellow chain is hit. */
    /**
     * The mola mola on land lies on its side like the other fish, but its middle (not its belly) over its position (the
     * side shift): its boxes lie on the ground, no thicker than the fish with its pectoral fins, and their middle is
     * within half a block of its position.
     */
    private static void molaOnLand(ClientGameTestContext context, TestServerContext server, int x, int y, int z) {
        UUID uuid = spawn(server, "mola_mola", x + 0.5, y + 1, z + 0.5, 30.0F, true);
        context.waitTicks(20);
        String result = server.computeOnServer(s -> {
            AbstractFish fish = (AbstractFish) s.overworld().getEntity(uuid);
            double low = Double.MAX_VALUE, high = -Double.MAX_VALUE, minX = Double.MAX_VALUE, maxX = -Double.MAX_VALUE;
            double minZ = Double.MAX_VALUE, maxZ = -Double.MAX_VALUE;
            for (FishPart part : ((FishParts.Holder) fish).mimcontent$parts().parts()) {
                AABB b = part.getBoundingBox();
                low = Math.min(low, b.minY - fish.getY());
                high = Math.max(high, b.maxY - fish.getY());
                minX = Math.min(minX, b.minX);
                maxX = Math.max(maxX, b.maxX);
                minZ = Math.min(minZ, b.minZ);
                maxZ = Math.max(maxZ, b.maxZ);
            }
            double off = Math.hypot((minX + maxX) / 2 - fish.getX(), (minZ + maxZ) / 2 - fish.getZ());
            return String.format(Locale.ROOT, "on land=%s, boxes from %.3f to %.3f above its feet, middle %.3f off its position",
                !fish.isInWater(), low, high, off);
        });
        log("the mola mola on land: " + result);
        check(result.contains("on land=true"), "the mola mola should be on land: " + result);
        String[] nums = result.replaceAll(".*from ([-0-9.]+) to ([-0-9.]+) above.*middle ([0-9.]+) off.*", "$1 $2 $3").split(" ");
        double low = Double.parseDouble(nums[0]), high = Double.parseDouble(nums[1]), off = Double.parseDouble(nums[2]);
        // its thickest slice is 11.4 px (the pectoral fins), lying on its side round its land lift (5 px)
        check(low > -0.1 && low < 0.1 && high < 0.75 && off < 0.5, "the mola mola's boxes on land should lie flat and centred: " + result);
    }

    private static void shots(ClientGameTestContext context, TestServerContext server, TestSingleplayerContext world, int gx, int gy, int gz) {
        int x = gx, y = gy, z = gz - 30;
        fill(server, x - 24, y, z - 8, x + 24, y + 10, z + 10, "minecraft:air");
        fill(server, x - 24, y - 1, z - 8, x + 24, y - 1, z + 10, "minecraft:smooth_sandstone");
        // a tank with an invisible (barrier) front wall, so no glass frames cross the boxes
        fill(server, x - 22, y, z + 3, x + 22, y + 4, z + 8, "minecraft:glass");
        fill(server, x - 22, y, z + 3, x + 22, y + 4, z + 3, "minecraft:barrier");
        fill(server, x - 22, y + 4, z + 3, x + 22, y + 4, z + 8, "minecraft:barrier");
        fill(server, x - 21, y, z + 4, x + 21, y + 3, z + 7, "minecraft:water");
        double[] at = {x + 15.5, x + 5.5, x - 5.0, x - 15.5};
        for (int i = 0; i < HIT_FISH.length; i++) {
            spawn(server, HIT_FISH[i], at[i], y + 1.2, z + 5.5, 90.0F, true);
        }
        // and a shark on land in front of the tank; a boll on the tank floor and one on land
        spawn(server, "huta_kahla", x + 15.5, y, z - 3.0, 90.0F, true);
        spawn(server, "boll", x + 10.5, y, z + 5.5, 90.0F, true);
        spawn(server, "boll", x + 5.5, y, z - 3.0, 90.0F, true);
        // a mola mola in the tank and one on land, on its side
        spawn(server, "mola_mola", x - 10.5, y + 0.4, z + 5.5, 90.0F, true);
        spawn(server, "mola_mola", x - 10.5, y, z - 3.5, 90.0F, true);
        context.runOnClient(mc -> {
            if (!mc.gui.hud.isHidden()) mc.gui.hud.toggle();
            mc.debugEntries.setStatus(DebugScreenEntries.ENTITY_HITBOXES, DebugScreenEntryStatus.ALWAYS_ON);
            mc.levelExtractor.debugRenderer.refreshRendererList();
        });
        world.getConnection().waitForChunksRender();
        context.waitTicks(40);
        server.runCommand("gamemode spectator @a");
        String[] names = {"huta-kahla", "pixxispad", "tonn", "murina"};
        double[] back = {2.9, 2.9, 3.6, 2.2};
        for (int i = 0; i < HIT_FISH.length; i++) {
            look(context, server, at[i], y + 0.1, z + 5.5 - back[i], at[i], y + 1.6, z + 5.5, "fish-hitbox-" + names[i]);
        }
        look(context, server, at[3] + 0.2, y + 3.4, z + 5.0, at[3], y + 1.3, z + 5.5, "fish-hitbox-murina-top");
        look(context, server, at[0] + 1.5, y + 0.3, z - 6.0, at[0], y + 0.2, z - 3.0, "fish-hitbox-huta-kahla-on-land");
        look(context, server, x + 10.5, y + 0.2, z + 3.4, x + 10.5, y + 0.1, z + 5.5, "fish-hitbox-boll");
        look(context, server, x + 6.5, y + 0.6, z - 5.5, x + 5.5, y, z - 3.0, "fish-hitbox-boll-on-land");
        look(context, server, x - 10.5, y - 0.3, z + 3.4, x - 10.5, y + 1.6, z + 5.5, "fish-hitbox-mola");
        look(context, server, x - 9.5, y + 1.0, z - 7.0, x - 10.5, y, z - 3.5, "fish-hitbox-mola-on-land");
        server.runCommand("gamemode creative @a");
        context.runOnClient(mc -> {
            mc.debugEntries.setStatus(DebugScreenEntries.ENTITY_HITBOXES, DebugScreenEntryStatus.NEVER);
            mc.levelExtractor.debugRenderer.refreshRendererList();
            if (mc.gui.hud.isHidden()) mc.gui.hud.toggle();
        });
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
            throw new AssertionError("[smoke] fish: " + message);
        }
    }

    private static void log(String message) {
        System.out.println("[smoke] fish: hitbox: " + message);
    }
}
