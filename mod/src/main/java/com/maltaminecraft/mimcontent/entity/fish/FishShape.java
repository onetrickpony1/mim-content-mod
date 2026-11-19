package com.maltaminecraft.mimcontent.entity.fish;

import java.util.AbstractMap;
import java.util.List;
import java.util.Map;
import net.minecraft.util.Mth;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * Where each fish's chain of hit boxes goes (owner 2026-11-18: "hitboxes for all fish should match their actual
 * size"). The boxes are sized from the accepted model, the same way for every fish:
 * <ol>
 * <li>take the model at rest (all its cubes, fins and tail included) and measure it from snout to tail along z;</li>
 * <li>cut that length into {@code ceil(length / 6 px)} equal slices, at least 2 and at most 8;</li>
 * <li>each slice becomes one box: as tall as the cubes that reach into the slice, and as wide as they are or as
 *     long as the slice, whichever is more (so the boxes touch end to end whichever way the fish faces).</li>
 * </ol>
 * The numbers below are that measurement, in model pixels (16 px = 1 block; y as in the model, the ground at 24).
 * The model classes live on the client only, so the server can't measure them itself; the smoke test
 * ({@code FishHitboxCheck}) measures every baked model again with {@link #slice} and fails if a row here no longer
 * matches, printing the row to paste in. The tonn's boxes grow with its size like the rest of it.
 *
 * <p>Placement follows {@code FishRenderer}: the body's yaw turns the chain, and out of water the fish lies on its
 * side (rotated 90 degrees about its length, lifted by the renderer's land lift), so the boxes lie flat too. The
 * murina's boxes follow the travelling wave of its five-section body ({@code MurinaModel}). A flat fish (the boll,
 * {@code flat}) lies flat on land too, as in water, only lifted by its land lift (the petriċa, deep in the water, is also squashed
 * flat on land: {@code landSquash}). The whole-body wiggle of the other
 * fish (a few degrees) is left out.
 *
 * <p>A fish much taller than it is thick (the mola mola) has a {@code sideShift}: lying on its side (on land, or basking
 * at the surface) it is moved back along its own height by that many blocks, so its middle lies over its position
 * instead of its belly (the renderer does the same; the smoke test checks they agree). 0 for every other fish.
 */
public record FishShape(float sliceLength, float[][] slices, float landLift, Wave wave, boolean flat, float sideShift, float landSquash) {
    /** The most slices a fish gets. */
    public static final int MAX_PARTS = 8;
    /** The slice length the count aims for, in px. */
    public static final float TARGET_SLICE = 6.0F;

    /**
     * A body that bends as a chain of sections (the murina): where each section's pivot sits along z (px), how far it
     * turns (radians), how quickly the wave runs (radians per tick) and how far behind each section is (radians);
     * out of water the wave is wider and quicker.
     */
    public record Wave(float[] pivots, float[] amplitude, float rate, float lag, float landAmplitude, float landSpeed) {
    }

    /**
     * Each row: {slice centre z, half width, top y, bottom y}, model px. Made by {@link #slice} from the models; the
     * land lift is the renderer's (MimContentClient).
     */
    private static final Map<String, FishShape> SHAPES = Map.ofEntries(
        // 23 px long, 5.4 wide, 12 tall
        shape("awrata", 5.75F, 0.1F, new float[][] {{-8.125F, 1.5F, 13F, 23F}, {-2.375F, 2.72F, 13F, 25F}, {3.375F, 1.5F, 13F, 24F}, {9.125F, 1F, 14F, 24F}}),
        // 42 px long (the whip tail included), 20 wide (the disc, 1.25 blocks), 2 thick over the dome; flat: it lies flat on land too
        flatShape("boll", 6.000F, 0.0F, new float[][] {{-7F, 8F, 21F, 24F}, {-1F, 10F, 22F, 24F}, {5F, 8F, 22F, 24F}, {11F, 2F, 23F, 24F}, {17F, 0.5F, 22.95F, 24F}, {23F, 0.5F, 23F, 24F}, {29F, 0.5F, 23F, 24F}}),
        // 14 px long, 4.4 wide, 8 tall
        shape("cawl", 4.667F, 0.1F, new float[][] {{-4.667F, 2.22F, 16F, 24F}, {0F, 2.22F, 16F, 24F}, {4.667F, 0.5F, 16F, 24F}}),
        // 29 px long, 9.1 wide, 13 tall
        shape("cerna", 5.8F, 0.21875F, new float[][] {{-10.1F, 2.5F, 15F, 23F}, {-4.3F, 4.56F, 12F, 24F}, {1.5F, 4.56F, 12F, 25F}, {7.3F, 2.5F, 12F, 25F}, {13.1F, 1.5F, 15F, 24F}}),
        // 43 px long, 12.9 wide (the pectoral fins), 12.4 tall
        shape("huta_kahla", 5.375F, 0.1875F, new float[][] {{-19.31F, 2F, 18F, 22F}, {-13.94F, 6.45F, 17F, 24.39F}, {-8.56F, 6.45F, 13F, 24.39F},
            {-3.19F, 2.5F, 13F, 23F}, {2.19F, 2.5F, 17F, 22F}, {7.56F, 2F, 16F, 23F}, {12.94F, 1F, 12F, 24F}, {18.31F, 0F, 12F, 24F}}),
        // 13 px long, 2.7 wide, 5 tall
        shape("incova", 4.333F, 0.1F, new float[][] {{-2.833F, 1.36F, 21F, 23.93F}, {1.5F, 1.36F, 19F, 24F}, {5.833F, 0.5F, 20F, 24F}}),
        // 35 px long, 6.3 wide, 11 tall
        shape("lampuka", 5.833F, 0.1F, new float[][] {{-14.08F, 3.15F, 13F, 23F}, {-8.25F, 3.15F, 13F, 23F}, {-2.42F, 1.5F, 13F, 24F}, {3.42F, 1F, 15F, 24F},
            {9.25F, 1F, 15F, 24F}, {15.08F, 0F, 16F, 24F}}),
        // 26 px long (mouth to clavus), 11.4 wide (the pectoral fins), 38 tall (dorsal fin tip to anal fin tip); its middle
        // (y 4.5) lies over its position when it lies on its side (on land, or basking): side shift 1.501 - 4.5 / 16
        tallShape("mola_mola", 5.2F, 0.3125F, 1.21975F, new float[][] {{-10.4F, 3F, -5F, 14F}, {-5.2F, 4F, -6F, 15F},
            {0F, 5.705F, -7.5F, 16.5F}, {5.2F, 3F, -14.5F, 23.5F}, {10.4F, 2.5F, -14.5F, 23.5F}}),
        // 32 px long, 4 wide, 6 tall; bends with its wave (MurinaModel: sections body, seg1, seg2, seg3, tail)
        new AbstractMap.SimpleEntry<>("murina", new FishShape(5.333F, new float[][] {{-11.33F, 1.5F, 18F, 23F}, {-6F, 2F, 18F, 23F},
            {-0.667F, 1.5F, 18F, 23F}, {4.667F, 1.5F, 18F, 24F}, {10F, 1F, 18F, 24F}, {15.33F, 1F, 18.5F, 23.5F}}, 0.1875F,
            new Wave(new float[] {0F, 0F, 5F, 10F, 14F}, new float[] {0.05F, 0.15F, 0.26F, 0.36F, 0.46F}, 0.33F, 1.05F, 1.2F, 1.8F), false, 0.0F, 1.0F)),
        // 45 px long (the sword included), 14 wide (the pectoral fins), 18 tall (dorsal fin to tail fin)
        shape("pixxispad", 5.625F, 0.21875F, new float[][] {{-20.19F, 1F, 19F, 20F}, {-14.56F, 1.5F, 18.5F, 21.5F}, {-8.94F, 2.5F, 16.5F, 23.5F},
            {-3.31F, 6.99F, 9F, 26.7F}, {2.31F, 6.99F, 9F, 26.7F}, {7.94F, 3F, 16.5F, 26F}, {13.56F, 2F, 13F, 27F}, {19.19F, 0F, 13F, 27F}}),
        // 14 px long, 3.5 wide, 6 tall
        shape("sardina", 4.667F, 0.1F, new float[][] {{-3.667F, 1.76F, 20F, 23.14F}, {1F, 1.76F, 18F, 24F}, {5.667F, 1F, 18.5F, 23.5F}}),
        // 15 px long, 11.9 wide (the spread pectoral fans), 9 tall (the spiny dorsal fin to the fins under the throat)
        shape("skorfna", 5F, 0.1875F, new float[][] {{-4.5F, 3F, 15F, 24F}, {0.5F, 5.941F, 15F, 23F}, {5.5F, 1F, 15F, 23.5F}}),
        // 39 px long, 9.5 wide, 15 tall (at the model's own size, 2.44 blocks; each tonn scales it)
        shape("tonn", 5.571F, 0.1875F, new float[][] {{-16.21F, 2.5F, 15.5F, 22.5F}, {-10.64F, 4.73F, 11F, 24F}, {-5.07F, 3.5F, 11F, 24F},
            {0.5F, 3.5F, 11F, 26F}, {6.07F, 2.5F, 11F, 26F}, {11.64F, 2F, 15F, 23F}, {17.21F, 2F, 13.5F, 24.5F}}),
        // 9 px long, 3 wide, 13 tall (upright)
        shape("ziemel", 4.5F, 0.1F, new float[][] {{-1.75F, 1.5F, 12F, 24F}, {2.75F, 1.5F, 11F, 24F}}),
        // the night job's fish (2026-11-18), placeholder models (art/src/fish_placeholders.py)
        // 17 px long, 3 wide, 6.5 tall
        shape("kavall", 5.250F, 0.125F, new float[][] {{-7.375F, 2.122F, 17.000F, 23.000F}, {-2.125F, 2.122F, 17.000F, 24.000F}, {3.125F, 1.500F, 17.000F, 24.000F}, {8.375F, 0.500F, 18.000F, 24.000F}}),
        // 24 px long, 2 wide, 6 tall
        shape("lizz", 6.000F, 0.1F, new float[][] {{-9.000F, 1.000F, 20.000F, 22.000F}, {-3.000F, 1.622F, 17.000F, 23.000F}, {3.000F, 1.000F, 17.000F, 23.000F}, {9.000F, 0.500F, 18.000F, 23.000F}}),
        // 15 px long, 5.8 wide (the pectoral fins), 9 tall (the dorsal fin to the anal fin)
        shape("marzpan", 5F, 0.125F, new float[][] {{-4.5F, 2.887F, 14F, 22F}, {0.5F, 2.887F, 14F, 23F}, {5.5F, 1F, 15F, 23F}}),
        // 12 px long, 2 wide, 5 tall (art/src/fish_tird_model.py)
        shape("tird", 6.000F, 0.1F, new float[][] {{-3.000F, 1.622F, 19.000F, 23.000F}, {3.000F, 1.000F, 18.500F, 23.500F}}),
        // 13 px long, 2 wide, 6 tall (the barbels hang under the chin)
        shape("trilja", 5.000F, 0.1F, new float[][] {{-5.500F, 1.000F, 17.000F, 24.933F}, {-0.500F, 1.000F, 17.000F, 23.000F}, {4.500F, 0.500F, 18.000F, 24.000F}}),
        // 14 px long, 6.5 wide (the pectoral fans), 5 tall with the black dorsal; 1 px of it in the sand (art/src/fish_sawt_model.py)
        shape("sawt", 4.667F, 0.1F, new float[][] {{-3.667F, 2.497F, 20.000F, 25.000F}, {1.000F, 1.000F, 20.000F, 25.000F}, {5.667F, 1.000F, 21.500F, 25.500F}}),
        // 22 px long, 2 wide, about 22 tall (the dorsal filaments to the pelvic fins; art/src/fish_pixxi_san_pietru_model.py)
        shape("pixxi_san_pietru", 5.500F, 0.1F, new float[][] {{-8.250F, 1.000F, 13.000F, 24.000F}, {-2.750F, 1.000F, 3.000F, 24.000F}, {2.750F, 1.000F, 2.305F, 24.000F}, {8.250F, 0.500F, 2.305F, 24.000F}}),
        // 30 px long, 25 wide (the pectoral fins), 13 tall with the lure; flat on land, squashed to 0.45 of its height
        flatShape("petrica", 6.000F, 0.0F, 0.45F, new float[][] {{-13.000F, 8.000F, 11.040F, 24.000F}, {-7.000F, 12.512F, 14.067F, 24.000F}, {-1.000F, 12.512F, 17.000F, 24.000F}, {5.000F, 3.500F, 17.000F, 24.000F}, {11.000F, 1.500F, 19.000F, 24.000F}}),
        // 23 px long with the tail, 10 wide, 2 thick (3 at the raised pectoral fin); flat: it lies flat on land too (art/src/fish_lingwata_model.py)
        flatShape("lingwata", 5.750F, 0.0F, new float[][] {{-9.125F, 5.000F, 22.000F, 24.000F}, {-3.375F, 5.000F, 21.164F, 24.000F}, {2.375F, 5.000F, 21.164F, 24.000F}, {8.125F, 3.000F, 22.000F, 24.000F}}),
        // 16 px long, 3 wide, 13 tall
        // 19 px long with the tail, 3 wide, 13 tall from the trigger to the anal fin (art/src/fish_hmar_model.py)
        shape("hmar", 5.333F, 0.125F, new float[][] {{-4.333F, 1.500F, 9.000F, 20.000F}, {1.000F, 1.500F, 9.000F, 22.000F}, {6.333F, 1.000F, 10.000F, 22.000F}}),
        // 18 px long, 14 wide (the pectoral "wings"), 5.5 tall
        shape("gallinella", 6.000F, 0.15625F, new float[][] {{-6.000F, 7.026F, 18.000F, 23.000F}, {0.000F, 7.026F, 18.000F, 24.000F}, {6.000F, 1.000F, 19.000F, 24.000F}}),
        // 15 px long, 11 wide (the fan fins), 10 tall (the dorsal spines)
        shape("lionfish", 5.000F, 0.125F, new float[][] {{-4.500F, 4.463F, 10.490F, 23.000F}, {0.500F, 4.463F, 10.926F, 23.000F}, {5.500F, 4.463F, 15.500F, 22.684F}}));

    private static Map.Entry<String, FishShape> shape(String id, float slice, float landLift, float[][] rows) {
        return new AbstractMap.SimpleEntry<>(id, new FishShape(slice, rows, landLift, null, false, 0.0F, 1.0F));
    }

    /** A tall fish (the mola mola) whose middle, not its belly, lies over its position when it lies on its side. */
    private static Map.Entry<String, FishShape> tallShape(String id, float slice, float landLift, float sideShift, float[][] rows) {
        return new AbstractMap.SimpleEntry<>(id, new FishShape(slice, rows, landLift, null, false, sideShift, 1.0F));
    }

    /** A flat fish (the boll): it lies flat on land as in water (its renderer doesn't turn it on its side). */
    private static Map.Entry<String, FishShape> flatShape(String id, float slice, float landLift, float[][] rows) {
        return flatShape(id, slice, landLift, 1.0F, rows);
    }

    /**
     * A flat fish that is deep in the water but lies flattened on land (the petriċa): on land its height is squashed to
     * landSquash from the ground up, as its renderer does (FishRenderer.withLandSquash).
     */
    private static Map.Entry<String, FishShape> flatShape(String id, float slice, float landLift, float landSquash, float[][] rows) {
        return new AbstractMap.SimpleEntry<>(id, new FishShape(slice, rows, landLift, null, true, 0.0F, landSquash));
    }

    /** The shape for one of our fish (by its id, e.g. "tonn"), or null. */
    public static FishShape of(String id) {
        return SHAPES.get(id);
    }

    public int parts() {
        return slices.length;
    }

    /**
     * The box of one slice in the world: the fish's position, body yaw (degrees), scale, whether it is in water
     * (else it lies on its side) and, for the murina, its age in ticks (for the wave).
     */
    public AABB box(int i, Vec3 at, float bodyYaw, float scale, boolean inWater, float age) {
        return box(i, at, bodyYaw, scale, inWater, !inWater, age);
    }

    /**
     * As above, with whether it lies on its side given apart from being in water: the mola mola lies on its side while
     * it basks at the surface, in the water.
     */
    public AABB box(int i, Vec3 at, float bodyYaw, float scale, boolean inWater, boolean onSide, float age) {
        float[] row = slices[i];
        float z = row[0], halfWidth = row[1], top = row[2], bottom = row[3];
        float x = 0.0F;
        if (wave != null) {
            float[] xz = bend(z, inWater, age);
            x = xz[0];
            z = xz[1];
        }
        float yMid = (top + bottom) / 2.0F;
        float side = Math.max(2.0F * halfWidth, sliceLength) / 16.0F;
        float tall = (bottom - top) / 16.0F;
        // FishRenderer's frame before the body's yaw: scale(-1, -1, 1) then up 1.501
        double a = -x / 16.0, b = 1.501 - yMid / 16.0, c = z / 16.0;
        if (onSide && flat) {
            // a flat fish lies on land as it swims, lifted a little, its height squashed from the ground up (landSquash)
            b = b * landSquash + landLift;
            tall *= landSquash;
        } else if (onSide) {
            // lying on its side: translate(0.1, landLift, -0.1), rotate 90 degrees about z, then back along its height
            // by the side shift (a tall fish's middle over its position)
            b -= sideShift;
            double a2 = 0.1 - b, b2 = landLift + a;
            a = a2;
            b = b2;
            c -= 0.1;
            // on its side the fish's height lies flat and its width stands up (a flat fin still gets 1 px)
            side = Math.max(bottom - top, sliceLength) / 16.0F;
            tall = Math.max(2.0F * halfWidth, 1.0F) / 16.0F;
        }
        double yaw = Math.toRadians(bodyYaw);
        double cos = Math.cos(yaw), sin = Math.sin(yaw);
        double wx = (-a * cos + c * sin) * scale, wy = b * scale, wz = (-a * sin - c * cos) * scale;
        double hs = side * scale / 2.0, ht = tall * scale / 2.0;
        return new AABB(at.x + wx - hs, at.y + wy - ht, at.z + wz - hs, at.x + wx + hs, at.y + wy + ht, at.z + wz + hs);
    }

    /** The murina: where a point that lies at z on the straight body sits once the wave bends it, as {x, z} in px. */
    private float[] bend(float z, boolean inWater, float age) {
        float amp = inWater ? 1.0F : wave.landAmplitude();
        float speed = inWater ? 1.0F : wave.landSpeed();
        float phase = speed * wave.rate() * age;
        float[] pivots = wave.pivots();
        float px = 0.0F, pz = pivots[0];
        for (int s = 0; s < pivots.length; s++) {
            float angle = amp * wave.amplitude()[s] * Mth.sin(phase - s * wave.lag());
            boolean last = s == pivots.length - 1 || z < pivots[s + 1];
            if (s > 0) {
                // this section's pivot: the previous one, carried along the previous section
                float prev = amp * wave.amplitude()[s - 1] * Mth.sin(phase - (s - 1) * wave.lag());
                float len = pivots[s] - pivots[s - 1];
                px += len * Mth.sin(prev);
                pz += len * Mth.cos(prev);
            }
            if (last) {
                float d = z - pivots[s];
                return new float[] {px + d * Mth.sin(angle), pz + d * Mth.cos(angle)};
            }
        }
        return new float[] {0.0F, z};
    }

    /**
     * Measures a model the way the table was made: given every cube of the model at rest as {minX, minY, minZ,
     * maxX, maxY, maxZ} in px (fins and rotations included), returns the slice length followed by the rows.
     */
    public static float[][] slice(List<float[]> cubes) {
        float zMin = Float.MAX_VALUE, zMax = -Float.MAX_VALUE;
        for (float[] c : cubes) {
            zMin = Math.min(zMin, c[2]);
            zMax = Math.max(zMax, c[5]);
        }
        float length = zMax - zMin;
        int n = Mth.clamp((int) Math.ceil(length / TARGET_SLICE - 1.0E-4), 2, MAX_PARTS);
        float slice = length / n;
        float[][] out = new float[n + 1][];
        out[0] = new float[] {slice};
        for (int i = 0; i < n; i++) {
            float s0 = zMin + i * slice, s1 = s0 + slice;
            float half = 0.0F, top = Float.MAX_VALUE, bottom = -Float.MAX_VALUE;
            for (float[] c : cubes) {
                if (c[2] < s1 - 1.0E-4F && c[5] > s0 + 1.0E-4F) {
                    half = Math.max(half, Math.max(Math.abs(c[0]), Math.abs(c[3])));
                    top = Math.min(top, c[1]);
                    bottom = Math.max(bottom, c[4]);
                }
            }
            out[i + 1] = new float[] {(s0 + s1) / 2.0F, half, top, bottom};
        }
        return out;
    }
}
