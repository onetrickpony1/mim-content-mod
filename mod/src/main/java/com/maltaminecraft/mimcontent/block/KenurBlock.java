package com.maltaminecraft.mimcontent.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.StringRepresentable;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/** The kenur: a portable limestone stove for one pot, mouth at the front. Art pilot: looks only. */
public class KenurBlock extends HorizontalDirectionalBlock {
    public static final BooleanProperty LIT = BlockStateProperties.LIT;
    public static final EnumProperty<Pot> POT = EnumProperty.create("pot", Pot.class);
    private static final VoxelShape SHAPE = Block.box(1, 0, 1, 15, 14, 15);
    private static final VoxelShape SHAPE_WITH_POT = Block.box(1, 0, 1, 15, 21, 15); // the pot sits above the block

    public enum Pot implements StringRepresentable {
        NONE("none"), EMPTY("empty"), STUFFAT("stuffat");
        private final String name;
        Pot(String name) { this.name = name; }
        @Override public String getSerializedName() { return name; }
    }

    public KenurBlock(BlockBehaviour.Properties props) {
        super(props);
        registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH).setValue(LIT, false).setValue(POT, Pot.NONE));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING, LIT, POT);
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext ctx) {
        return defaultBlockState().setValue(FACING, ctx.getHorizontalDirection().getOpposite());
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext ctx) {
        return state.getValue(POT) == Pot.NONE ? SHAPE : SHAPE_WITH_POT;
    }
}
