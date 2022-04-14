from lib import sudoku_solver
import numpy as np

if __name__ == '__main__':

    sudoku_example = [[0, 0, 0, 0, 0, 9, 4, 7, 0],
                      [0, 0, 2, 0, 3, 0, 0, 9, 8],
                      [0, 6, 0, 0, 0, 2, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 5, 0, 7],
                      [0, 7, 0, 0, 0, 0, 0, 6, 0],
                      [8, 0, 3, 0, 0, 0, 0, 0, 0],
                      [6, 0, 0, 1, 0, 0, 0, 2, 0],
                      [7, 4, 0, 0, 6, 0, 9, 0, 0],
                      [0, 1, 9, 4, 0, 0, 0, 0, 0]]

    a = []
    sudoku_solver.solve(a, sudoku_example)
    if a:
        print(a[0])

    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            print(np.array(sudoku_example)[0 + 3 * i:3 + 3 * i, 0 + 3 * j:3 + 3 * j].reshape(9))
