package com.maltaminecraft.mimcontent.entity;

import com.maltaminecraft.mimcontent.MimConfig;
import java.util.Optional;
import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.NonNullList;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.Mth;
import net.minecraft.world.Containers;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.ContainerUser;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.HasCustomInventoryScreen;
import net.minecraft.world.entity.MoverType;
import net.minecraft.world.entity.SlotAccess;
import net.minecraft.world.entity.monster.piglin.PiglinAi;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.vehicle.ContainerEntity;
import net.minecraft.world.entity.vehicle.boat.Boat;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ChestMenu;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.phys.Vec3;
import org.jspecify.annotations.Nullable;

/**
 * The luzzu, the Maltese fishing boat. Placed, ridden and broken like a vanilla boat, with the owner's buffs, each
 * behind its own switch in config/mimcontent.json (off = vanilla boat behaviour for that part):
 * <ul>
 * <li>more seats: 4 instead of 2, along the longer hull; the first to board steers;</li>
 * <li>a fish hold: 27 slots like a chest boat, without losing a seat;</li>
 * <li>an engine: about 25% faster than a vanilla boat on open sea, normal speed near the shore;</li>
 * <li>it finds home: about 10% faster when steering toward its harbour.</li>
 * </ul>
 * The server's switches reach the clients through the entity's synced data, so a server decides for everyone.
 * Speed works by stretching each tick's own move, not the stored velocity, so it can't build up, and it runs wherever
 * vanilla runs the boat (the driver's client, with the server checking as usual).
 */
public class LuzzuBoat extends Boat implements HasCustomInventoryScreen, ContainerEntity {
    private static final byte SEATS = 1, HOLD = 2, ENGINE = 4, HOME = 8;
    /** The server's switches. The default is a constant (not the local config), so a client never keeps its own. */
    private static final EntityDataAccessor<Byte> DATA_BUFFS = SynchedEntityData.defineId(LuzzuBoat.class, EntityDataSerializers.BYTE);
    private static final EntityDataAccessor<Optional<BlockPos>> DATA_HARBOUR =
        SynchedEntityData.defineId(LuzzuBoat.class, EntityDataSerializers.OPTIONAL_BLOCK_POS);

    /** The floorboards sit 2 px above a vanilla boat's (the luzzu rides high in the water). */
    private static final double SEAT_RAISE = 2.0 / 16.0;
    /** Seat positions, in blocks forward of the middle (the bow is forward), in boarding order: the helmsman at the
     *  oars amidships, then one aft, one in the bow and one at the stern. Kept inside the open part of the hull. */
    private static final float[] SEAT_OFFSETS = {0.15F, -0.35F, 0.6F, -0.8F};
    private static final int MAX_SEATS = 4;

    public static final int HOLD_SIZE = 27;
    /** On open sea the luzzu goes this much further each tick than a vanilla boat would. */
    public static final float ENGINE_FACTOR = 1.25F;
    /** Steering toward the harbour adds this on top. */
    public static final float HOME_FACTOR = 1.10F;
    /** Within this angle of the harbour's bearing counts as steering toward it. */
    private static final double HOME_COS = Math.cos(Math.toRadians(30.0));
    /** No home boost this close to the harbour (it is already there). */
    private static final double HOME_MIN_DISTANCE = 16.0;
    /** Open sea: water all round for this many blocks, and at least SEA_DEPTH blocks deep under the boat. */
    private static final int SHORE_RADIUS = 4;
    private static final int SEA_DEPTH = 3;
    /** How fast the speed eases toward its target each tick, so changes never jerk. */
    private static final float EASE = 0.08F;

    private NonNullList<ItemStack> itemStacks = NonNullList.withSize(HOLD_SIZE, ItemStack.EMPTY);
    private @Nullable ResourceKey<LootTable> lootTable;
    private long lootTableSeed;
    private float speedFactor = 1.0F;
    private boolean openSea;

    public LuzzuBoat(EntityType<? extends Boat> type, Level level, Supplier<Item> dropItem) {
        super(type, level, dropItem);
        if (!level.isClientSide()) {
            this.entityData.set(DATA_BUFFS, configBuffs());
        }
    }

    private static byte configBuffs() {
        return (byte) ((MimConfig.luzzuMoreSeats ? SEATS : 0) | (MimConfig.luzzuFishHold ? HOLD : 0)
            | (MimConfig.luzzuEngine ? ENGINE : 0) | (MimConfig.luzzuFindsHome ? HOME : 0));
    }

    private boolean buff(byte flag) {
        return (this.entityData.get(DATA_BUFFS) & flag) != 0;
    }

    public boolean hasMoreSeats() {
        return buff(SEATS);
    }

    public boolean hasFishHold() {
        return buff(HOLD);
    }

    public boolean hasEngine() {
        return buff(ENGINE);
    }

    public boolean findsHome() {
        return buff(HOME);
    }

    public Optional<BlockPos> getHarbour() {
        return this.entityData.get(DATA_HARBOUR);
    }

    public void setHarbour(@Nullable BlockPos pos) {
        this.entityData.set(DATA_HARBOUR, Optional.ofNullable(pos));
    }

    /** The current speed multiplier (1 = vanilla). */
    public float getSpeedFactor() {
        return speedFactor;
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder entityData) {
        super.defineSynchedData(entityData);
        entityData.define(DATA_BUFFS, (byte) 0);
        entityData.define(DATA_HARBOUR, Optional.empty());
    }

    // ---- seats ----

    @Override
    protected double rideHeight(EntityDimensions dimensions) {
        return super.rideHeight(dimensions) + SEAT_RAISE;
    }

    @Override
    protected int getMaxPassengers() {
        return hasMoreSeats() ? MAX_SEATS : super.getMaxPassengers();
    }

    @Override
    protected Vec3 getPassengerAttachmentPoint(Entity passenger, EntityDimensions dimensions, float scale) {
        if (!hasMoreSeats()) {
            return super.getPassengerAttachmentPoint(passenger, dimensions, scale);
        }
        int index = Math.max(0, this.getPassengers().indexOf(passenger));
        float offset = SEAT_OFFSETS[Math.min(index, SEAT_OFFSETS.length - 1)];
        return new Vec3(0.0, this.rideHeight(dimensions), offset).yRot(-this.getYRot() * Mth.DEG_TO_RAD);
    }

    // ---- speed: the engine and the way home ----

    @Override
    public void tick() {
        if (!this.level().isClientSide()) {
            byte buffs = configBuffs();
            if (this.entityData.get(DATA_BUFFS) != buffs) {
                this.entityData.set(DATA_BUFFS, buffs);
            }
            // first tick after being placed (or summoned): it sets out from here
            if (getHarbour().isEmpty()) {
                setHarbour(this.blockPosition());
            }
        }
        updateSpeedFactor();
        super.tick();
        // TODO fishing bonus (owner's buff 3): better catches when fishing from a luzzu, and the lampuka under the
        //  kannizzati in season. Waits for the fish and season systems; it will go here, behind luzzu_fishing.
    }

    private void updateSpeedFactor() {
        float target = 1.0F;
        if (this.isLocalInstanceAuthoritative() && this.getControllingPassenger() instanceof Player) {
            if (this.tickCount % 5 == 0 || this.tickCount < 2) {
                openSea = checkOpenSea();
            }
            boolean onWater = onWater();
            if (hasEngine() && onWater && openSea) {
                target *= ENGINE_FACTOR;
            }
            if (findsHome() && onWater && headingHome()) {
                target *= HOME_FACTOR;
            }
        }
        speedFactor += (target - speedFactor) * EASE;
        if (Math.abs(target - speedFactor) < 0.001F) {
            speedFactor = target;
        }
    }

    /** Floating on water (not on land, ice or in the air). */
    private boolean onWater() {
        return this.level().getFluidState(BlockPos.containing(this.getX(), this.getY() + 0.05, this.getZ())).is(FluidTags.WATER);
    }

    /** Water all round at the surface for a few blocks, and deep enough under the boat: away from any shore. */
    private boolean checkOpenSea() {
        Level level = this.level();
        BlockPos centre = BlockPos.containing(this.getX(), this.getY() + 0.05, this.getZ());
        BlockPos.MutableBlockPos pos = new BlockPos.MutableBlockPos();
        for (int dx = -SHORE_RADIUS; dx <= SHORE_RADIUS; dx++) {
            for (int dz = -SHORE_RADIUS; dz <= SHORE_RADIUS; dz++) {
                pos.set(centre.getX() + dx, centre.getY(), centre.getZ() + dz);
                if (!level.getFluidState(pos).is(FluidTags.WATER)) {
                    return false;
                }
            }
        }
        for (int dy = 0; dy < SEA_DEPTH; dy++) {
            pos.set(centre.getX(), centre.getY() - dy, centre.getZ());
            if (!level.getFluidState(pos).is(FluidTags.WATER)) {
                return false;
            }
        }
        return true;
    }

    /** The bow points within 30 degrees of the harbour, and the harbour isn't right here. */
    private boolean headingHome() {
        Optional<BlockPos> harbour = getHarbour();
        if (harbour.isEmpty()) {
            return false;
        }
        double dx = harbour.get().getX() + 0.5 - this.getX();
        double dz = harbour.get().getZ() + 0.5 - this.getZ();
        double distance = Math.sqrt(dx * dx + dz * dz);
        if (distance < HOME_MIN_DISTANCE) {
            return false;
        }
        double yaw = this.getYRot() * Mth.DEG_TO_RAD;
        double forwardX = -Math.sin(yaw), forwardZ = Math.cos(yaw);
        return (forwardX * dx + forwardZ * dz) / distance >= HOME_COS;
    }

    @Override
    public void move(MoverType type, Vec3 delta) {
        if (type == MoverType.SELF && speedFactor != 1.0F) {
            delta = new Vec3(delta.x * speedFactor, delta.y, delta.z * speedFactor);
        }
        super.move(type, delta);
    }

    @Override
    protected void removePassenger(Entity passenger) {
        boolean driver = passenger == this.getControllingPassenger();
        super.removePassenger(passenger);
        // the driver stepping off at a shore makes this its harbour (left at open sea, the harbour stays)
        if (driver && !this.level().isClientSide() && !this.isRemoved() && (!onWater() || !checkOpenSea())) {
            setHarbour(this.blockPosition());
        }
    }

    // ---- the fish hold ----

    @Override
    public InteractionResult interact(Player player, InteractionHand hand, Vec3 location) {
        InteractionResult result = super.interact(player, hand, location);
        if (result != InteractionResult.PASS || !hasFishHold()) {
            return result;
        }
        // like a chest boat: use to board, sneak and use (or use a full boat) to open the hold
        if (this.canAddPassenger(player) && !player.isSecondaryUseActive()) {
            return InteractionResult.PASS;
        }
        InteractionResult opened = this.interactWithContainerVehicle(player);
        if (opened.consumesAction() && player.level() instanceof ServerLevel serverLevel) {
            this.gameEvent(GameEvent.CONTAINER_OPEN, player);
            PiglinAi.angerNearbyPiglins(serverLevel, player, true);
        }
        return opened;
    }

    /** Riding, the inventory key opens the hold (as in a chest boat); with the hold off the client opens the player's
     *  own inventory instead (see MultiPlayerGameModeMixin), so this only ever runs with the hold on. */
    @Override
    public void openCustomInventoryScreen(Player player) {
        if (!hasFishHold()) {
            return;
        }
        player.openMenu(this);
        if (player.level() instanceof ServerLevel level) {
            this.gameEvent(GameEvent.CONTAINER_OPEN, player);
            PiglinAi.angerNearbyPiglins(level, player, true);
        }
    }

    @Override
    public void remove(RemovalReason reason) {
        // whatever is in the hold drops when the boat breaks, even with the hold switched off, so nothing is lost
        if (!this.level().isClientSide() && reason.shouldDestroy()) {
            this.unpackChestVehicleLootTable(null);
            for (int i = 0; i < itemStacks.size(); i++) {
                ItemStack stack = itemStacks.get(i);
                if (!stack.isEmpty()) {
                    Containers.dropItemStack(this.level(), this.getX(), this.getY(), this.getZ(), stack);
                    itemStacks.set(i, ItemStack.EMPTY);
                }
            }
        }
        super.remove(reason);
    }

    @Override
    protected void addAdditionalSaveData(ValueOutput output) {
        super.addAdditionalSaveData(output);
        this.addChestVehicleSaveData(output);
        getHarbour().ifPresent(pos -> output.store("Harbour", BlockPos.CODEC, pos));
    }

    @Override
    protected void readAdditionalSaveData(ValueInput input) {
        super.readAdditionalSaveData(input);
        this.readChestVehicleSaveData(input);
        setHarbour(input.read("Harbour", BlockPos.CODEC).orElse(null));
    }

    /** With the hold off it shows no slots (hoppers and commands leave it alone); the items stay saved. */
    @Override
    public int getContainerSize() {
        return hasFishHold() ? HOLD_SIZE : 0;
    }

    @Override
    public void clearContent() {
        this.clearChestVehicleContent();
    }

    @Override
    public ItemStack getItem(int slot) {
        return this.getChestVehicleItem(slot);
    }

    @Override
    public ItemStack removeItem(int slot, int count) {
        return this.removeChestVehicleItem(slot, count);
    }

    @Override
    public ItemStack removeItemNoUpdate(int slot) {
        return this.removeChestVehicleItemNoUpdate(slot);
    }

    @Override
    public void setItem(int slot, ItemStack itemStack) {
        this.setChestVehicleItem(slot, itemStack);
    }

    @Override
    public @Nullable SlotAccess getSlot(int slot) {
        return hasFishHold() ? this.getChestVehicleSlot(slot) : super.getSlot(slot);
    }

    @Override
    public void setChanged() {
    }

    @Override
    public boolean stillValid(Player player) {
        return hasFishHold() && this.isChestVehicleStillValid(player);
    }

    @Override
    public @Nullable AbstractContainerMenu createMenu(int containerId, Inventory inventory, Player player) {
        if (!hasFishHold() || this.lootTable != null && player.isSpectator()) {
            return null;
        }
        this.unpackChestVehicleLootTable(inventory.player);
        return ChestMenu.threeRows(containerId, inventory, this);
    }

    @Override
    public void stopOpen(ContainerUser containerUser) {
        this.level().gameEvent(GameEvent.CONTAINER_CLOSE, this.position(), GameEvent.Context.of(containerUser.getLivingEntity()));
    }

    @Override
    public @Nullable ResourceKey<LootTable> getContainerLootTable() {
        return this.lootTable;
    }

    @Override
    public void setContainerLootTable(@Nullable ResourceKey<LootTable> lootTable) {
        this.lootTable = lootTable;
    }

    @Override
    public long getContainerLootTableSeed() {
        return this.lootTableSeed;
    }

    @Override
    public void setContainerLootTableSeed(long lootTableSeed) {
        this.lootTableSeed = lootTableSeed;
    }

    @Override
    public NonNullList<ItemStack> getItemStacks() {
        return this.itemStacks;
    }

    /** Always the full hold, whatever the switch says, so loading a save never drops items. */
    @Override
    public void clearItemStacks() {
        this.itemStacks = NonNullList.withSize(HOLD_SIZE, ItemStack.EMPTY);
    }
}
