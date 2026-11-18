package com.maltaminecraft.mimcontent.test;

import com.maltaminecraft.mimcontent.MimContent;
import com.maltaminecraft.mimcontent.MimFishes;
import com.maltaminecraft.mimcontent.client.item.BucketVariantProperty;
import com.maltaminecraft.mimcontent.entity.fish.SkorfnaFish;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Path;
import java.util.Locale;
import javax.imageio.ImageIO;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.client.Minecraft;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.phys.AABB;

/**
 * The skorfna bucket shows the version inside (SMOKE_ONLY=skorfna-bucket): a red and a black skorfna are caught in
 * survival the normal way, and their buckets go in the hotbar beside a bucket with no saved version (one filled before
 * versions existed) and vanilla's cod bucket. Checked:
 * <ul>
 * <li>the client property {@code mimcontent:bucket_variant} reads "red", "black" and nothing from the three buckets;</li>
 * <li>in the drawn hotbar (a screenshot), the red one's fish pixels are skorfna_red_bucket.png's colours and the black
 *     and the old ones' are skorfna_bucket.png's: the item model's select picked the right picture.</li>
 * </ul>
 * Screenshot: skorfna-bucket-hotbar (red, black, old, cod bucket, at GUI scale 4 when the window allows it).
 */
public class SkorfnaBucketCheck implements FabricClientGameTest {
    @Override
    public void runTest(ClientGameTestContext context) {
        if (!Smoke.runs("skorfna-bucket")) {
            return;
        }
        try (TestSingleplayerContext world = context.worldBuilder().create()) {
            world.getConnection().waitForChunksRender();
            TestServerContext server = world.getServer();
            server.runCommand("gamerule spawn_mobs false");
            server.runCommand("gamerule advance_time false");
            server.runCommand("time set 6000");
            int[] p = context.computeOnClient(mc -> new int[] {mc.player.getBlockX(), mc.player.getBlockY(), mc.player.getBlockZ()});
            int x = p[0], y = p[1] + 30, z = p[2];
            fill(server, x - 4, y - 4, z - 4, x + 4, y + 3, z + 4, "minecraft:air");
            fill(server, x - 3, y - 4, z - 3, x + 3, y - 1, z + 3, "minecraft:stone");
            fill(server, x - 2, y - 3, z - 2, x + 2, y - 1, z + 2, "minecraft:water");
            server.runCommand(String.format("tp @a %d %d %d 0 30", x, y, z - 3));
            server.runCommand("gamemode survival @a");
            server.runCommand("clear @a");
            context.waitTicks(5);

            // catch one of each version with a water bucket, as a player does; the buckets go to hotbar slots 0 and 1
            String[] versions = {"red", "black"};
            for (int i = 0; i < versions.length; i++) {
                String version = versions[i];
                int slot = i;
                server.runCommand(String.format(Locale.ROOT, "summon mimcontent:skorfna %.1f %d %.1f {NoAI:1b,PersistenceRequired:1b,Variant:\"%s\"}",
                    x + 0.5, y - 2, z + 0.5, version));
                context.waitTicks(2);
                String caught = server.computeOnServer(s -> {
                    ServerPlayer player = s.getPlayerList().getPlayers().getFirst();
                    AABB pool = new AABB(x - 3, y - 4, z - 3, x + 4, y + 1, z + 4);
                    var fish = s.overworld().getEntities(MimFishes.SKORFNA.type(), pool, e -> true);
                    if (fish.size() != 1) {
                        return "found " + fish.size() + " skorfna";
                    }
                    SkorfnaFish skorfna = (SkorfnaFish) fish.getFirst();
                    // catch with the last slot in hand, so emptying the hand afterwards leaves slots 0-7 alone
                    player.getInventory().setSelectedSlot(8);
                    player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.WATER_BUCKET));
                    skorfna.interact(player, InteractionHand.MAIN_HAND, skorfna.position());
                    ItemStack held = player.getItemInHand(InteractionHand.MAIN_HAND);
                    if (!held.is(MimFishes.SKORFNA.bucket())) {
                        return "bucketing gave " + held.getItem();
                    }
                    player.getInventory().setItem(slot, held.copy());
                    player.setItemInHand(InteractionHand.MAIN_HAND, ItemStack.EMPTY);
                    fish.forEach(Entity::discard);
                    return "ok";
                });
                check(caught.equals("ok"), "catching a " + version + " skorfna: " + caught);
            }
            // a bucket with no version saved (filled before versions existed) in slot 2, vanilla's cod bucket in slot 3
            server.runCommand("item replace entity @a hotbar.2 with mimcontent:skorfna_bucket");
            server.runCommand("item replace entity @a hotbar.3 with minecraft:cod_bucket");
            server.runCommand("item replace entity @a hotbar.4 with minecraft:cod_bucket");
            server.runCommand("item replace entity @a hotbar.5 with minecraft:pufferfish_bucket");
            context.waitTicks(5);

            // the property, as the item model reads it
            String read = context.computeOnClient(mc -> {
                StringBuilder out = new StringBuilder();
                for (int slot = 0; slot < 3; slot++) {
                    ItemStack stack = mc.player.getInventory().getItem(slot);
                    String v = new BucketVariantProperty().get(stack, mc.level, mc.player, 0, ItemDisplayContext.GUI);
                    out.append(v == null ? "none" : v).append(' ');
                }
                return out.toString().trim();
            });
            log("bucket_variant of the red, black and old buckets: " + read);
            check(read.equals("red black none"), "bucket_variant should read red black none: " + read);

            // the drawn hotbar: each bucket's fish pixels against both pictures
            context.runOnClient(mc -> {
                if (mc.gui.hud.isHidden()) mc.gui.hud.toggle();
                mc.options.guiScale().set(4);
                mc.player.getInventory().setSelectedSlot(8);
            });
            context.waitTicks(15);
            Path shot = context.takeScreenshot("skorfna-bucket-hotbar");
            String drawn = context.computeOnClient(mc -> {
                try {
                    BufferedImage screen = ImageIO.read(shot.toFile());
                    BufferedImage black = texture(mc, "skorfna_bucket"), red = texture(mc, "skorfna_red_bucket");
                    StringBuilder out = new StringBuilder();
                    for (int slot = 0; slot < 3; slot++) {
                        out.append(matches(mc, screen, slot, red, black)).append(' ');
                    }
                    return out.toString().trim();
                } catch (IOException e) {
                    return "can't read: " + e;
                }
            });
            log("drawn in the hotbar (slots 0-2, the picture each matches): " + drawn);
            check(drawn.equals("red black black"), "the hotbar should show red, black, black: " + drawn);
        }
    }

    /** One of our textures as the game loaded it from the resources. */
    private static BufferedImage texture(Minecraft mc, String name) throws IOException {
        try (InputStream in = mc.getResourceManager().getResourceOrThrow(MimContent.id("textures/item/" + name + ".png")).open()) {
            return ImageIO.read(in);
        }
    }

    /**
     * Which picture a hotbar slot shows: counts the fish pixels (opaque in our layer) whose screen colour is within 12
     * per channel of the red picture's and of the black one's: "red" or "black" when at least 90% match that one and at
     * most 10% the other (a few tones of the two palettes lie close together), else "unclear(r/b/n)".
     */
    private static String matches(Minecraft mc, BufferedImage screen, int slot, BufferedImage red, BufferedImage black) {
        var window = mc.getWindow();
        int scale = window.getGuiScale();
        double fx = screen.getWidth() / (double) window.getWidth(), fy = screen.getHeight() / (double) window.getHeight();
        // vanilla's hotbar: slot i's item is drawn at (guiWidth / 2 - 90 + 20 i + 2, guiHeight - 19)
        int gx = window.getGuiScaledWidth() / 2 - 88 + 20 * slot, gy = window.getGuiScaledHeight() - 19;
        int r = 0, b = 0, n = 0;
        for (int py = 0; py < 6; py++) {
            for (int px = 0; px < 16; px++) {
                int want = black.getRGB(px, py);
                if ((want >>> 24) == 0 || black.getRGB(px, py) == red.getRGB(px, py)) {
                    continue;
                }
                int sx = (int) (((gx + px) * scale + scale / 2) * fx), sy = (int) (((gy + py) * scale + scale / 2) * fy);
                int got = screen.getRGB(sx, sy);
                n++;
                r += near(got, red.getRGB(px, py)) ? 1 : 0;
                b += near(got, black.getRGB(px, py)) ? 1 : 0;
            }
        }
        if (r * 10 >= n * 9 && b * 10 <= n) {
            return "red";
        }
        if (b * 10 >= n * 9 && r * 10 <= n) {
            return "black";
        }
        return "unclear(" + r + "/" + b + "/" + n + ")";
    }

    private static boolean near(int a, int b) {
        for (int shift = 0; shift <= 16; shift += 8) {
            if (Math.abs(((a >> shift) & 0xff) - ((b >> shift) & 0xff)) > 12) {
                return false;
            }
        }
        return true;
    }

    private static void fill(TestServerContext server, int x0, int y0, int z0, int x1, int y1, int z1, String block) {
        server.runCommand(String.format("fill %d %d %d %d %d %d %s", x0, y0, z0, x1, y1, z1, block));
    }

    private static void check(boolean ok, String message) {
        if (!ok) {
            throw new AssertionError("[smoke] skorfna-bucket: " + message);
        }
    }

    private static void log(String message) {
        System.out.println("[smoke] skorfna-bucket: " + message);
    }
}
