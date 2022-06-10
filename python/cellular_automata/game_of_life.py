import numpy as np
import matplotlib.pyplot as plt


def main():
    grid_size = 50
    cell_geometry_scale = 0.1
    update_time = 0.5

    grid = np.zeros(shape=(grid_size, grid_size))

    fig = plt.figure(figsize=(cell_geometry_scale * grid_size, cell_geometry_scale * grid_size))

    selected_cells_coords = []

    plt.ion()
    while True:
        for n, _ in enumerate(grid[0, :]):
            plt.axvline(x=-0.5 + n, linewidth=cell_geometry_scale, color='blue')
            plt.axhline(y=-0.5 + n, linewidth=cell_geometry_scale, color='blue')
        plt.imshow(X=grid, cmap='binary')

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
        grid[-1, -1] = 1 - grid[-1, -1]

        plt.clf()


if __name__ == '__main__':
    main()
