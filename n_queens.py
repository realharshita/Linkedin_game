import sys

def is_safe(board, row, col, n):
    for i in range(col):
        if board[row][i] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    return True

def solve_nqueens_util(board, col, n):
    if col >= n:
        return True
    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            if solve_nqueens_util(board, col + 1, n):
                return True
            board[i][col] = 0
    return False

def solve_nqueens(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    if not solve_nqueens_util(board, 0, n):
        return None
    return board

def print_board(board):
    for row in board:
        print(" ".join("Q" if x else "." for x in row))
    print("\nBoard Size: {}x{}".format(len(board), len(board)))
    print("Solution:\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python n_queens.py <board_size>")
        sys.exit(1)
    
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Board size must be an integer")
        sys.exit(1)

    if n < 1:
        print("Board size must be greater than 0")
        sys.exit(1)

    solution = solve_nqueens(n)
    if solution:
        print_board(solution)
    else:
        print("No solution exists")
