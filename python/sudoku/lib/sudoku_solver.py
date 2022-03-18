import numpy as np


def possible(matrix: list, x: int, y: int, number: int) -> bool:
    """
    check if number is possible to place in (x,y)-position of sudoku matrix
    :param matrix: sudoku matrix
    :param x: x-position
    :param y: y-position
    :param number: current number to place
    :return: true if possible and false otherwise
    """
    for i in range(9):
        if matrix[x][i] == number:
            return False
    for j in range(9):
        if matrix[j][y] == number:
            return False
    x0 = (x//3)*3
    y0 = (y//3)*3
    for k in range(3):
        for m in range(3):
            if matrix[x0+k][y0+m] == number:
                return False
    return True


def solve(matrix):
    for x in range(9):
        for y in range(9):
            if matrix[x][y] == 0:
                for n in range(1, 10):
                    if possible(matrix, x, y, n):
                        matrix[x][y] = n
                        solve(matrix)
                        matrix[x][y] = 0
                return
    print(np.array(matrix))