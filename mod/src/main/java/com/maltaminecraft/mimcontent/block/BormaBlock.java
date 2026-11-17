package com.maltaminecraft.mimcontent.block;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/** The borma (terracotta stew pot), standing on its own. Art pilot: looks only. */
public class BormaBlock extends Block {
    private static final VoxelShape SHAPE = Block.box(2, 0, 2, 14, 11, 14);

    public BormaBlock(BlockBehaviour.Properties props) {
        super(props);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext ctx) {
        return SHAPE;
    }
}
