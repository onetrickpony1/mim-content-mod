package com.maltaminecraft.mimcontent;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import net.fabricmc.loader.api.FabricLoader;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * The mod's switches, kept in config/mimcontent.json. Written with the defaults on first run; switches missing from
 * an older file are added with their defaults. Every gameplay change has a switch here, and turning one off brings
 * back vanilla behaviour for that part. Read once at start-up: restart the game (or server) after editing the file.
 * On a server, the server's file decides; players' own files don't matter there.
 */
public final class MimConfig {
    private static final Logger LOG = LoggerFactory.getLogger("mimcontent");
    public static final String FILE_NAME = "mimcontent.json";

    /** Luzzu: room for 3 (vanilla boats carry 2). */
    public static boolean luzzuMoreSeats = true;
    /** Luzzu: a fish hold with 27 slots, like a chest boat, without losing a seat. */
    public static boolean luzzuFishHold = true;
    /** Luzzu: about 25% faster than a vanilla boat on open sea, normal speed near the shore. */
    public static boolean luzzuEngine = true;
    /** Luzzu: a little faster (about 10%) when steering toward its harbour. */
    public static boolean luzzuFindsHome = true;
    /** Fish: the tier A fish also live in vanilla's warm and lukewarm oceans, so they turn up in normal worlds.
     *  false: only in the Malta world's sea biomes. */
    public static boolean fishInVanillaOceans = true;
    /** Jellyfish venom brews: a second way to brew Poison (awkward potion + venom) and the Jellyfish Ward potion
     *  (thick potion + venom). false: no venom recipes; Poison brews only from vanilla's spider eye. */
    public static boolean jellyfishVenomRecipes = true;

    private MimConfig() {
    }

    public static Path path() {
        return FabricLoader.getInstance().getConfigDir().resolve(FILE_NAME);
    }

    /** Reads the file (if any), then writes it back so it always lists every switch. */
    public static void load() {
        Path file = path();
        JsonObject json = new JsonObject();
        if (Files.exists(file)) {
            try {
                JsonElement parsed = JsonParser.parseString(Files.readString(file, StandardCharsets.UTF_8));
                if (parsed.isJsonObject()) {
                    json = parsed.getAsJsonObject();
                }
            } catch (IOException | RuntimeException e) {
                LOG.warn("Couldn't read {}, using the defaults: {}", file, e.toString());
            }
        }
        luzzuMoreSeats = read(json, "luzzu_more_seats", true);
        luzzuFishHold = read(json, "luzzu_fish_hold", true);
        luzzuEngine = read(json, "luzzu_engine", true);
        luzzuFindsHome = read(json, "luzzu_finds_home", true);
        fishInVanillaOceans = read(json, "fish_in_vanilla_oceans", true);
        jellyfishVenomRecipes = read(json, "jellyfish_venom_recipes", true);

        JsonObject out = new JsonObject();
        out.addProperty("_about", "Malta in Minecraft content mod. true = on, false = vanilla behaviour. Restart after editing.");
        out.addProperty("luzzu_more_seats", luzzuMoreSeats);
        out.addProperty("luzzu_fish_hold", luzzuFishHold);
        out.addProperty("luzzu_engine", luzzuEngine);
        out.addProperty("luzzu_finds_home", luzzuFindsHome);
        out.addProperty("fish_in_vanilla_oceans", fishInVanillaOceans);
        out.addProperty("jellyfish_venom_recipes", jellyfishVenomRecipes);
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        try {
            Files.createDirectories(file.getParent());
            Files.writeString(file, gson.toJson(out) + "\n", StandardCharsets.UTF_8);
        } catch (IOException e) {
            LOG.warn("Couldn't write {}: {}", file, e.toString());
        }
    }

    private static boolean read(JsonObject json, String key, boolean fallback) {
        JsonElement value = json.get(key);
        return value != null && value.isJsonPrimitive() && value.getAsJsonPrimitive().isBoolean() ? value.getAsBoolean() : fallback;
    }
}
