import numpy as np


def check_sudoku_field(matrix):
    matrix_num = np.array(matrix)
    for i in range(9):
        vertical = list(filter(lambda a: a != 0, matrix_num[:, i]))
        horizontal = list(filter(lambda a: a != 0, matrix_num[i, :]))

        if len(set(vertical)) != len(vertical):
            return False

        if len(set(horizontal)) != len(horizontal):
            return False

    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            current_square = np.array(matrix_num)[0 + 3 * i:3 + 3 * i, 0 + 3 * j:3 + 3 * j].reshape(9)
            current_square = list(filter(lambda a: a != 0, current_square))

        if len(set(current_square)) != len(current_square):
            return False

    return True


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


def solve(a, matrix, flag=1):
    flag = flag + 1
    if flag > 1000:
        return
    for x in range(9):
        for y in range(9):
            if matrix[x][y] == 0:
                for n in range(1, 10):
                    if possible(matrix, x, y, n):
                        matrix[x][y] = n
                        solve(a, matrix, flag)
                        matrix[x][y] = 0
                return
    a.append(np.array(matrix))
    if len(a) > 1:
        a = []
        return
