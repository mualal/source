import numpy as np
import time


class Node:
    def __init__(self, header_node=None):
        self.value = None
        self.up = self
        self.down = self
        self.left = self
        self.right = self
        self.column = header_node

    def __repr__(self):
        return 'Node: {}:{}'.format(self.column.value, self.value)


class HeaderNode(Node):
    def __init__(self, column_id):
        super().__init__(header_node=self)
        self.value = column_id
        self.node_count = 0

    def __repr__(self):
        return 'HeaderNode: {}'.format(self.value)


class RootNode(Node):
    def __init__(self, value='root'):
        super().__init__()
        self.value = value

    def __repr__(self):
        return 'RootNode'


def create_sparse_matrix(matrix):
    root = RootNode()

    for i in range(len(matrix[0])):
        new_node = HeaderNode(i)
        last = root.left
        new_node.right = root
        root.left = new_node
        new_node.left = last
        last.right = new_node

    for i in range(len(matrix)):
        row_start = None
        for j in range(len(matrix[0])):
            if matrix[i][j]:
                header = root.right
                for _ in range(j):
                    header = header.right
                new_node = Node(header)
                new_node.value = (int(i // len(matrix) ** (2 / 3)),
                                  int(i // len(matrix) ** (1 / 3) % len(matrix) ** (1 / 3)),
                                  int(i % len(matrix) ** (1 / 3)) + 1)
                last = header.up
                new_node.down = header
                header.up = new_node
                new_node.up = last
                last.down = new_node
                header.node_count += 1

                if row_start:
                    last = row_start.left
                    new_node.right = row_start
                    row_start.left = new_node
                    new_node.left = last
                    last.right = new_node
                else:
                    row_start = new_node
    return root


def print_sparse_matrix(root):
    node = root
    while node.right != root:
        node = node.right
        column = node
        print(node, 'node_count:', node.node_count)
        while node.down != column:
            node = node.down
            print('\t {} Right{} Left{}'.format(node, node.right, node.left))
        node = node.down


if __name__ == '__main__':

    start = time.time()

    sudoku_size = 9
    exact_cover_board = np.zeros((sudoku_size**3, 4 * sudoku_size**2))

    for col in range(sudoku_size ** 2):
        for row in range(sudoku_size):
            exact_cover_board[row + col * sudoku_size][col] = 1

    for col in range(sudoku_size ** 2, 2 * sudoku_size**2):
        adjusted_col = col % sudoku_size**2
        column_block = adjusted_col // sudoku_size
        for row in range(sudoku_size):
            x = row + (column_block * sudoku_size) + sudoku_size**2
            y = adjusted_col * sudoku_size + row
            exact_cover_board[y][x] = 1

    for col in range(2 * sudoku_size**2, 3 * sudoku_size**2):
        adjusted_col = col % sudoku_size**2
        for row in range(sudoku_size):
            x = (row + adjusted_col * sudoku_size) % sudoku_size**2 + 2 * sudoku_size**2
            y = row + adjusted_col * sudoku_size
            exact_cover_board[y][x] = 1

    for col in range(3 * sudoku_size**2, 4 * sudoku_size**2):
        adjusted_col = col % sudoku_size**2
        box_size = int(np.sqrt(sudoku_size))
        column_block = (adjusted_col // box_size) % box_size
        for row in range(sudoku_size):
            x = row + (column_block + (adjusted_col // (sudoku_size * box_size)) *
                       box_size) * sudoku_size + 3 * sudoku_size**2
            y = adjusted_col * sudoku_size + row
            exact_cover_board[y][x] = 1

    # print(exact_cover_board)

    root1 = create_sparse_matrix(exact_cover_board)

    # print_sparse_matrix(root1)

    grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    values1 = []

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col]:
                values1.append((row, col, grid[row][col]))

    end = time.time()
    print(end - start)
