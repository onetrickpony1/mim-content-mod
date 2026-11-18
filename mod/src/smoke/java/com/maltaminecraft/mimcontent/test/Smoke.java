package com.maltaminecraft.mimcontent.test;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;

/** Which in-game checks to run: all, unless tools/run-art.sh was given SMOKE_ONLY (it writes the file smoke-only). */
final class Smoke {
    private Smoke() {
    }

    /** True only if SMOKE_ONLY was given and names this check. */
    static boolean listed(String name) {
        try {
            Path file = Path.of("smoke-only");
            return Files.exists(file) && Arrays.stream(Files.readString(file).trim().split(",")).anyMatch(s -> s.trim().equals(name));
        } catch (java.io.IOException e) {
            return false;
        }
    }

    /** The fish id given as FISH_ONLY (tools/run-art.sh writes the file fish-only), for SMOKE_ONLY=fish-one; null if none. */
    static String fishOnly() {
        try {
            Path file = Path.of("fish-only");
            return Files.exists(file) && !Files.readString(file).isBlank() ? Files.readString(file).trim() : null;
        } catch (java.io.IOException e) {
            return null;
        }
    }

    static boolean runs(String name) {
        try {
            Path file = Path.of("smoke-only");
            if (!Files.exists(file)) {
                return true;
            }
            boolean on = Arrays.stream(Files.readString(file).trim().split(",")).anyMatch(s -> s.trim().equals(name));
            if (!on) {
                System.out.println("[smoke] skipping " + name + " (SMOKE_ONLY)");
            }
            return on;
        } catch (java.io.IOException e) {
            return true;
        }
    }
}
