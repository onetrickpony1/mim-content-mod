package com.maltaminecraft.mimcontent.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * A big oven dish (ross il-forn first) set on a table and eaten in slices, like a vanilla cake (food plan, option 1).
 * SLICES counts the slices already eaten (0 = whole dish, 5 = one slice left); the last slice removes the block.
 * Art trial 2026-11-17: the numbers are placeholders until the food values are decided.
 */
public class SliceDishBlock extends HorizontalDirectionalBlock {
    public static final int MAX_EATEN = 5;
    public static final IntegerProperty EATEN = IntegerProperty.create("eaten", 0, MAX_EATEN);
    private static final VoxelShape SHAPE = Block.box(1, 0, 1, 15, 5, 15);

    private final int nutrition;
    private final float saturation;

    public SliceDishBlock(Properties props, int nutrition, float saturation) {
        super(props);
        this.nutrition = nutrition;
        this.saturation = saturation;
        registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH).setValue(EATEN, 0));
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext ctx) {
        return defaultBlockState().setValue(FACING, ctx.getHorizontalDirection().getOpposite());
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext ctx) {
        return SHAPE;
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!player.canEat(false)) {
            return InteractionResult.PASS;
        }
        if (!level.isClientSide()) {
            player.getFoodData().eat(nutrition, saturation);
            int eaten = state.getValue(EATEN);
            if (eaten < MAX_EATEN) {
                level.setBlock(pos, state.setValue(EATEN, eaten + 1), Block.UPDATE_ALL);
            } else {
                level.removeBlock(pos, false);
            }
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING, EATEN);
    }
}
