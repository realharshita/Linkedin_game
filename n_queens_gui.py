import tkinter as tk

def create_board_canvas(root, size):
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()
    return canvas

def draw_board(canvas, board):
    canvas.delete("all")
    n = len(board)
    cell_size = 500 // n
    for i in range(n):
        for j in range(n):
            x0 = j * cell_size
            y0 = i * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            color = "white" if (i + j) % 2 == 0 else "gray"
            canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            if board[i][j] == 1:
                canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text="Q", font=("Arial", cell_size // 2), fill="black")

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

def start_solver(canvas, size_entry):
    n = int(size_entry.get())
    solution = solve_nqueens(n)
    if solution:
        draw_board(canvas, solution)
    else:
        print("No solution exists")

root = tk.Tk()
root.title("N-Queens Solver")
size_entry = tk.Entry(root)
size_entry.pack()
canvas = create_board_canvas(root, 500)
start_button = tk.Button(root, text="Solve", command=lambda: start_solver(canvas, size_entry))
start_button.pack()
root.mainloop()
