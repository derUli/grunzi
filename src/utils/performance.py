def get_grid_size(count):
    grid_size = 64

    if count >= 5:
        grid_size += 16

    if count >= 10:
        grid_size += 16

    return grid_size