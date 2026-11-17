package com.maltaminecraft.mimcontent;

import com.maltaminecraft.mimcontent.block.BormaBlock;
import com.maltaminecraft.mimcontent.block.KenurBlock;
import com.maltaminecraft.mimcontent.block.SliceDishBlock;
import com.maltaminecraft.mimcontent.entity.LuzzuBoat;
import java.util.function.Function;
import java.util.function.Supplier;
import net.fabricmc.api.ModInitializer;
import net.minecraft.core.Registry;
import net.minecraft.core.dispenser.BoatDispenseItemBehavior;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.BoatItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.DispenserBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.material.MapColor;

/** Art pilot (2026-11-17): the kenur, the borma and the foods, registered only so they can be seen in-game; and the luzzu, a rideable boat. */
public class MimContent implements ModInitializer {
    public static final String MOD_ID = "mimcontent";

    public static final Block KENUR = block("kenur", KenurBlock::new, BlockBehaviour.Properties.of()
        .mapColor(MapColor.SAND).strength(1.5F, 6.0F).sound(SoundType.STONE).noOcclusion()
        .lightLevel(s -> s.getValue(BlockStateProperties.LIT) ? 15 : 0));
    public static final Block BORMA = block("borma", BormaBlock::new, BlockBehaviour.Properties.of()
        .mapColor(MapColor.TERRACOTTA_ORANGE).strength(0.6F).sound(SoundType.DECORATED_POT).noOcclusion());
    public static final Block BORMA_STUFFAT = block("borma_stuffat", BormaBlock::new, BlockBehaviour.Properties.of()
        .mapColor(MapColor.TERRACOTTA_ORANGE).strength(0.6F).sound(SoundType.DECORATED_POT).noOcclusion());

    public static final Block ROSS_IL_FORN = block("ross_il_forn", p -> new SliceDishBlock(p, 4, 0.6F), BlockBehaviour.Properties.of()
        .mapColor(MapColor.COLOR_ORANGE).strength(0.5F).sound(SoundType.WOOL).noOcclusion());

    public static final Block IMQARRUN_IL_FORN = block("imqarrun_il_forn", p -> new SliceDishBlock(p, 4, 0.6F), BlockBehaviour.Properties.of()
        .mapColor(MapColor.COLOR_ORANGE).strength(0.5F).sound(SoundType.WOOL).noOcclusion());

    public static final Block TIMPANA = block("timpana", p -> new SliceDishBlock(p, 5, 0.7F), BlockBehaviour.Properties.of()
        .mapColor(MapColor.SAND).strength(0.5F).sound(SoundType.WOOL).noOcclusion());

    public static final Block TORTA_LAMPUKI = block("torta_lampuki", p -> new SliceDishBlock(p, 5, 0.8F), BlockBehaviour.Properties.of()
        .mapColor(MapColor.SAND).strength(0.5F).sound(SoundType.WOOL).noOcclusion());

    public static final Item HOBZ_MALTI = item("hobz_malti", Item::new, new Item.Properties());
    public static final Item PASTIZZ_IRKOTTA = item("pastizz_irkotta", Item::new, new Item.Properties());
    public static final Item PASTIZZ_PIZELLI = item("pastizz_pizelli", Item::new, new Item.Properties());
    public static final Item PASTIZZ_XEMA_IRKOTTA = item("pastizz_xema_irkotta", Item::new, new Item.Properties());
    public static final Item PASTIZZ_XEMA_PIZELLI = item("pastizz_xema_pizelli", Item::new, new Item.Properties());
    public static final Item FTIRA = item("ftira", Item::new, new Item.Properties());
    public static final Item HOBZ_BIZZEJT = item("hobz_bizzejt", Item::new, new Item.Properties());
    public static final Item FTIRA_GHAWDXIJA = item("ftira_ghawdxija", Item::new, new Item.Properties());
    public static final Item IMQARET = item("imqaret", Item::new, new Item.Properties());
    public static final Item KANNOLI = item("kannoli", Item::new, new Item.Properties());
    public static final Item QAGHAQ_GHASEL = item("qaghaq_ghasel", Item::new, new Item.Properties());
    public static final Item STUFFAT_FENEK = item("stuffat_fenek", Item::new, new Item.Properties());
    public static final Item ALJOTTA = item("aljotta", Item::new, new Item.Properties());
    public static final Item STUFFAT_QARNIT = item("stuffat_qarnit", Item::new, new Item.Properties());
    public static final Item BIGILLA = item("bigilla", Item::new, new Item.Properties());
    public static final Item GALLETTI = item("galletti", Item::new, new Item.Properties());
    public static final Item LAMPUKA = item("lampuka", Item::new, new Item.Properties());
    public static final Item LAMPUKA_MOQLIJA = item("lampuka_moqlija", Item::new, new Item.Properties());
    public static final Item SOPPA_TAL_ARMLA = item("soppa_tal_armla", Item::new, new Item.Properties());
    public static final Item MINESTRA = item("minestra", Item::new, new Item.Properties());
    public static final Item KAWLATA = item("kawlata", Item::new, new Item.Properties());
    public static final Item KUSKSU = item("kusksu", Item::new, new Item.Properties());
    public static final Item BRODU_TAT_TIGIEG = item("brodu_tat_tigieg", Item::new, new Item.Properties());
    public static final Item BRODU_TAL_LAHAM = item("brodu_tal_laham", Item::new, new Item.Properties());
    public static final Item QASSATA_IRKOTTA = item("qassata_irkotta", Item::new, new Item.Properties());
    public static final Item QASSATA_PIZELLI = item("qassata_pizelli", Item::new, new Item.Properties());
    public static final Item QAGHAQ_HMIRA = item("qaghaq_hmira", Item::new, new Item.Properties());
    public static final Item QAGHQA_APPOSTLI = item("qaghqa_appostli", Item::new, new Item.Properties());
    public static final Item DIP_GBEJNA = item("dip_gbejna", Item::new, new Item.Properties());
    public static final Item DIP_TONN = item("dip_tonn", Item::new, new Item.Properties());
    public static final Item DIP_TEWM = item("dip_tewm", Item::new, new Item.Properties());
    public static final Item GELAT_MALTI = item("gelat_malti", Item::new, new Item.Properties());
    public static final Item STUFFAT_BEBBUX = item("stuffat_bebbux", Item::new, new Item.Properties());
    public static final Item FENEK_MOQLI = item("fenek_moqli", Item::new, new Item.Properties());
    public static final Item KINNIE = item("kinnie", Item::new, new Item.Properties());
    public static final Item KINNIE_CAN = item("kinnie_can", Item::new, new Item.Properties());
    public static final Item KINNIE_GLASS = item("kinnie_glass", Item::new, new Item.Properties());
    public static final Item GBEJNA = item("gbejna", Item::new, new Item.Properties());
    public static final Item GBEJNA_NIEXFA = item("gbejna_niexfa", Item::new, new Item.Properties());
    public static final Item GBEJNA_TAL_BZAR = item("gbejna_tal_bzar", Item::new, new Item.Properties());

    /**
     * The luzzu: placed, ridden and broken like a vanilla boat, with its own model and the owner's buffs (more seats,
     * a fish hold, an engine, finding home; each switchable in config/mimcontent.json, see LuzzuBoat).
     * One type per colour scheme, like vanilla's wood types: green (the default), red and brown.
     */
    public static final EntityType<LuzzuBoat> LUZZU = luzzu("luzzu", () -> MimContent.LUZZU_ITEM);
    public static final Item LUZZU_ITEM = boatItem("luzzu", LUZZU);
    public static final EntityType<LuzzuBoat> LUZZU_RED = luzzu("luzzu_red", () -> MimContent.LUZZU_RED_ITEM);
    public static final Item LUZZU_RED_ITEM = boatItem("luzzu_red", LUZZU_RED);
    public static final EntityType<LuzzuBoat> LUZZU_BROWN = luzzu("luzzu_brown", () -> MimContent.LUZZU_BROWN_ITEM);
    public static final Item LUZZU_BROWN_ITEM = boatItem("luzzu_brown", LUZZU_BROWN);

    @Override
    public void onInitialize() {
        MimConfig.load();
        DispenserBlock.registerBehavior(LUZZU_ITEM, new BoatDispenseItemBehavior(LUZZU));
        DispenserBlock.registerBehavior(LUZZU_RED_ITEM, new BoatDispenseItemBehavior(LUZZU_RED));
        DispenserBlock.registerBehavior(LUZZU_BROWN_ITEM, new BoatDispenseItemBehavior(LUZZU_BROWN));
    }

    public static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(MOD_ID, path);
    }

    private static Block block(String name, Function<BlockBehaviour.Properties, Block> factory, BlockBehaviour.Properties props) {
        ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, id(name));
        Block block = Registry.register(BuiltInRegistries.BLOCK, key, factory.apply(props.setId(key)));
        item(name, p -> new BlockItem(block, p), new Item.Properties().useBlockDescriptionPrefix());
        return block;
    }

    private static EntityType<LuzzuBoat> luzzu(String name, Supplier<Item> drop) {
        return entity(name, EntityType.Builder.<LuzzuBoat>of((type, level) -> new LuzzuBoat(type, level, drop), MobCategory.MISC)
            .noLootTable().sized(1.375F, 0.5625F).eyeHeight(0.5625F).clientTrackingRange(10));
    }

    private static Item boatItem(String name, EntityType<LuzzuBoat> type) {
        return item(name, p -> new BoatItem(type, p), new Item.Properties().stacksTo(1));
    }

    private static <T extends Entity> EntityType<T> entity(String name, EntityType.Builder<T> builder) {
        ResourceKey<EntityType<?>> key = ResourceKey.create(Registries.ENTITY_TYPE, id(name));
        return Registry.register(BuiltInRegistries.ENTITY_TYPE, key, builder.build(key));
    }

    private static Item item(String name, Function<Item.Properties, Item> factory, Item.Properties props) {
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id(name));
        return Registry.register(BuiltInRegistries.ITEM, key, factory.apply(props.setId(key)));
    }
}
