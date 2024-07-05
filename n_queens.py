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

if __name__ == "__main__":
    n = 8 
    solution = solve_nqueens(n)
    if solution:
        print_board(solution)
    else:
        print("No solution exists")
