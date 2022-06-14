import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve


def gosper_glider_gun(size):
    glider_gun_grid = np.zeros(shape=(size, size))
    for (i, j) in [(5, 1), (5, 2), (6, 1), (6, 2), (5, 11), (6, 11), (7, 11), (4, 12), (8, 12), (3, 13), (9, 13),
                   (3, 14), (9, 14), (6, 15), (4, 16), (8, 16), (5, 17), (6, 17), (7, 17), (6, 18), (3, 21), (4, 21),
                   (5, 21), (3, 22), (4, 22), (5, 22), (2, 23), (6, 23), (1, 25), (2, 25), (6, 25), (7, 25), (3, 35),
                   (4, 35), (3, 36), (4, 36)]:
        glider_gun_grid[i, j] = 1

    return glider_gun_grid


def pulsar(size):
    pulsar_grid = np.zeros(shape=(size, size))
    for (i, j) in [(2, 4), (2, 5), (2, 6), (2, 10), (2, 11), (2, 12), (4, 2), (4, 7), (4, 9), (4, 14), (5, 2),
                   (5, 7), (5, 9), (5, 14), (6, 2), (6, 7), (6, 9), (6, 14), (7, 4), (7, 5), (7, 6),
                   (7, 10), (7, 11), (7, 12), (9, 4), (9, 5), (9, 6), (9, 10), (9, 11), (9, 12),
                   (10, 2), (10, 7), (10, 9), (10, 14), (11, 2), (11, 7), (11, 9), (11, 14), (12, 2), (12, 7), (12, 9),
                   (12, 14), (14, 4), (14, 5), (14, 6), (14, 10), (14, 11), (14, 12)]:
        pulsar_grid[i, j] = 1

    return pulsar_grid


def simkin_glider_gun(size):
    glider_gun_grid = np.zeros(shape=(size, size))
    for (i, j) in [(1, 1), (1, 2), (2, 1), (2, 2), (1, 8), (1, 9), (2, 8), (2, 9), (4, 5), (4, 6), (5, 5), (5, 6),
                   (10, 23), (10, 24), (10, 26), (10, 27), (11, 22), (11, 28), (12, 22), (12, 29), (13, 22),
                   (13, 23), (13, 24), (13, 28), (14, 27), (18, 21), (18, 22), (19, 21), (20, 22), (20, 23), (20, 24),
                   (21, 24), (12, 32), (12, 33), (13, 32), (13, 33)]:
        (i, j) = (i + 15, j + 15)
        glider_gun_grid[i, j] = 1

    return glider_gun_grid


def spaceships(size):
    spaceships_grid = np.zeros(shape=(size, size))
    for (i, j) in [(2, 3), (2, 4), (2, 5), (2, 6), (3, 2), (3, 6), (4, 6), (5, 2), (5, 5)]:
        (i, j) = (i + 5, j)
        spaceships_grid[i, j] = 1

    for (i, j) in [(1, 4), (2, 2), (2, 6), (3, 7), (4, 2), (4, 7), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7)]:
        (i, j) = (i + 20, j)
        spaceships_grid[i, j] = 1

    for (i, j) in [(1, 4), (1, 5), (2, 2), (2, 7), (3, 8), (4, 2), (4, 8), (5, 3), (5, 4), (5, 5), (5, 6),
                   (5, 7), (5, 8)]:
        (i, j) = (i + 35, j)
        spaceships_grid[i, j] = 1

    return spaceships_grid


def field_process(cells_grid, kernel=None):
    if kernel is None:
        kernel = [[1, 1, 1],
                  [1, 0, 1],
                  [1, 1, 1]]
    neighbours_sum = convolve(cells_grid, kernel, mode='constant')
    new_cells_grid = cells_grid.copy()
    new_cells_grid[neighbours_sum != 2] = 0
    new_cells_grid[neighbours_sum == 3] = 1
    return new_cells_grid


def main():
    grid_size = 50
    cell_geometry_scale = 0.1
    update_time = 0.01

    # grid = gosper_glider_gun(grid_size)

    # grid = pulsar(grid_size)

    # grid = simkin_glider_gun(grid_size)

    grid = spaceships(grid_size)

    fig = plt.figure(figsize=(cell_geometry_scale * grid_size, cell_geometry_scale * grid_size))

    selected_cells_coords = []

    plt.ion()
    while True:
        for n, _ in enumerate(grid[0, :]):
            plt.axvline(x=-0.5+n, linewidth=cell_geometry_scale, color='blue')
            plt.axhline(y=-0.5+n, linewidth=cell_geometry_scale, color='blue')

        plt.imshow(X=grid, cmap='binary')
        grid = field_process(grid)

        pt = plt.ginput(n=1, timeout=update_time)

        if pt:
            p_x = int(round(number=pt[0][0], ndigits=0))
            p_y = int(round(number=pt[0][1], ndigits=0))
            cell_coords = (p_x, len(grid) - p_y - 1)
            if cell_coords in selected_cells_coords:
                grid[p_y][p_x] = 0
                selected_cells_coords.remove(cell_coords)
            else:
                grid[p_y][p_x] = 1
                selected_cells_coords.append(cell_coords)
        # grid[-1, -1] = 1 - grid[-1, -1]

        plt.clf()


if __name__ == '__main__':
    main()
