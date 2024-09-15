def get_grid_size(count):
    grid_size = 64 + (count * 2)

    if grid_size > 128:
        grid_size = 128

    return grid_size