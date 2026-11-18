package com.maltaminecraft.mimcontent.test;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;

/** Which in-game checks to run: all, unless tools/run-art.sh was given SMOKE_ONLY (it writes the file smoke-only). */
final class Smoke {
    private Smoke() {
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
