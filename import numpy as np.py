import numpy as np

def is_valid(board, piece, row, col):
    for i in range(4):
        for j in range(4):
            if piece[i][j] == 1:
                x, y = row + i, col + j
                if x < 0 or y < 0 or x >= board.shape[0] or y >= board.shape[1] or board[x][y] == 1:
                    return False
    return True

def move_horizontal(board, piece, col_diff):
    rows, cols = board.shape
    result = np.zeros((rows, cols))

    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 1:
                new_col = col + col_diff
                if 0 <= new_col < cols:
                    result[row][new_col] = 1
                else:
                    result[row][col] = 1
            else:
                result[row][col] = board[row][col]

    return result

def print_board(board):
    rows, cols = board.shape
    for row in range(rows):
        for col in range(cols):
            print('1' if board[row][col] == 1 else '0', end=' ')
        print()

board = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

piece = np.array([[0, 0, 0, 0],
                 [1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]])

row, col = 2, 2

if is_valid(board, piece, row, col):
    board = move_horizontal(board, piece, col_diff=2)
    print_board(board)
else:
    print("Invalid move")