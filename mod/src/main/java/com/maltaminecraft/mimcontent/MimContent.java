package com.maltaminecraft.mimcontent;

import com.maltaminecraft.mimcontent.block.BormaBlock;
import com.maltaminecraft.mimcontent.block.KenurBlock;
import com.maltaminecraft.mimcontent.block.SliceDishBlock;
import java.util.function.Function;
import net.fabricmc.api.ModInitializer;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.material.MapColor;

/** Art pilot (2026-11-17): the kenur, the borma and three foods, registered only so they can be seen in-game. */
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
    public static final Item KINNIE = item("kinnie", Item::new, new Item.Properties());
    public static final Item KINNIE_CAN = item("kinnie_can", Item::new, new Item.Properties());
    public static final Item KINNIE_GLASS = item("kinnie_glass", Item::new, new Item.Properties());
    public static final Item GBEJNA = item("gbejna", Item::new, new Item.Properties());
    public static final Item GBEJNA_NIEXFA = item("gbejna_niexfa", Item::new, new Item.Properties());
    public static final Item GBEJNA_TAL_BZAR = item("gbejna_tal_bzar", Item::new, new Item.Properties());

    @Override
    public void onInitialize() {
    }

    static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(MOD_ID, path);
    }

    private static Block block(String name, Function<BlockBehaviour.Properties, Block> factory, BlockBehaviour.Properties props) {
        ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, id(name));
        Block block = Registry.register(BuiltInRegistries.BLOCK, key, factory.apply(props.setId(key)));
        item(name, p -> new BlockItem(block, p), new Item.Properties().useBlockDescriptionPrefix());
        return block;
    }

    private static Item item(String name, Function<Item.Properties, Item> factory, Item.Properties props) {
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id(name));
        return Registry.register(BuiltInRegistries.ITEM, key, factory.apply(props.setId(key)));
    }
}
