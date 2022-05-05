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


def generate_exact_cover_board(grid_size):

    exact_cover_board = np.zeros((grid_size**3, 4 * grid_size**2))

    for col in range(grid_size ** 2):
        for row in range(grid_size):
            exact_cover_board[row + col * grid_size][col] = 1

    for col in range(grid_size ** 2, 2 * grid_size**2):
        adjusted_col = col % grid_size**2
        column_block = adjusted_col // grid_size
        for row in range(grid_size):
            x = row + (column_block * grid_size) + grid_size**2
            y = adjusted_col * grid_size + row
            exact_cover_board[y][x] = 1

    for col in range(2 * grid_size**2, 3 * grid_size**2):
        adjusted_col = col % grid_size**2
        for row in range(grid_size):
            x = (row + adjusted_col * grid_size) % grid_size**2 + 2 * grid_size**2
            y = row + adjusted_col * grid_size
            exact_cover_board[y][x] = 1

    for col in range(3 * grid_size**2, 4 * grid_size**2):
        adjusted_col = col % grid_size**2
        box_size = int(np.sqrt(grid_size))
        column_block = (adjusted_col // box_size) % box_size
        for row in range(grid_size):
            x = row + (column_block + (adjusted_col // (grid_size * box_size)) *
                       box_size) * grid_size + 3 * grid_size**2
            y = adjusted_col * grid_size + row
            exact_cover_board[y][x] = 1

    return exact_cover_board


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


def choose_least_column(root):
    node = root.right
    least_column = node
    while node.right != root:
        node = node.right
        if node.node_count < least_column.node_count:
            least_column = node
    return least_column


def cover(node):
    column = node.column
    column.right.left = column.left
    column.left.right = column.right

    row = column.down
    while row != column:
        right_node = row.right
        while right_node != row:
            right_node.up.down = right_node.down
            right_node.down.up = right_node.up
            right_node.column.node_count -= 1
            right_node = right_node.right
        row = row.down


def uncover(node):
    column = node.column

    row = column.up
    while row != column:
        left_node = row.left
        while left_node != row:
            left_node.up.down = left_node
            left_node.down.up = left_node
            left_node.column.node_count += 1
            left_node = left_node.left
        row = row.up

    column.right.left = column
    column.left.right = column


def cover_values(root, values, size):
    for value in values:
        column_id = value[0] * size + value[1]

        column = root.right
        while column != root:
            if column.value == column_id:
                break
            column = column.right

        cover(column)

        row_node = column.down
        while row_node != column:
            if row_node.value == value:
                break
            row_node = row_node.down

        right_node = row_node.right
        while right_node != row_node:
            cover(right_node)
            right_node = right_node.right


def solve(root, solution):
    if root.right == root:
        return solution, True

    column = choose_least_column(root)
    cover(column)

    row_node = column.down
    while row_node != column:
        solution.append(row_node)

        right_node = row_node.right
        while right_node != row_node:
            cover(right_node)
            right_node = right_node.right

        solution, found = solve(root, solution)
        if found:
            return solution, True

        solution.pop()

        column = row_node.column
        left_node = row_node.left
        while left_node != row_node:
            if left_node != root:
                uncover(left_node)
            left_node = left_node.left
        row_node = row_node.down
    uncover(column)

    return solution, False


def solver_pipeline(sudoku_grid):

    sudoku_size = len(sudoku_grid)

    exact_cover = generate_exact_cover_board(sudoku_size)

    root = create_sparse_matrix(exact_cover)

    values = []
    for row in range(len(sudoku_grid)):
        for col in range(len(sudoku_grid[0])):
            if sudoku_grid[row][col]:
                values.append((row, col, sudoku_grid[row][col]))
    try:
        cover_values(root, values, sudoku_size)
    except AttributeError:
        return 'Given Sudoku field violate game rules'

    solution, found = solve(root, [])

    solved_sudoku_grid = sudoku_grid.copy()
    if found:
        for element in solution:
            sol_value = element.value
            solved_sudoku_grid[sol_value[0]][sol_value[1]] = sol_value[2]
        return np.array(solved_sudoku_grid, dtype=float)
    else:
        return 'No solution to given Sudoku field'


if __name__ == '__main__':

    start = time.time()

    grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    sol = solver_pipeline(grid)
    print(sol)

    end = time.time()
    print(end - start)
