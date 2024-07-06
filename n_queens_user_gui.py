import tkinter as tk

def create_board_canvas(root, size):
    canvas = tk.Canvas(root, width=size, height=size)
    canvas.pack()
    return canvas

def draw_board(canvas, board):
    canvas.delete("all")
    n = len(board)
    cell_size = canvas.winfo_width() // n
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

def on_canvas_click(event, canvas, board):
    n = len(board)
    cell_size = canvas.winfo_width() // n
    row = event.y // cell_size
    col = event.x // cell_size
    if board[row][col] == 1:
        board[row][col] = 0
    else:
        board[row][col] = 1
    draw_board(canvas, board)

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

def check_solution(board):
    n = len(board)
    for col in range(n):
        queen_found = False
        for row in range(n):
            if board[row][col] == 1:
                if not is_safe(board, row, col, n):
                    return False
                queen_found = True
        if not queen_found:
            return False
    return True

def show_solution_status(board):
    status = "Solution is correct!" if check_solution(board) else "Solution is incorrect!"
    status_label.config(text=status)

root = tk.Tk()
root.title("Interactive N-Queens Solver")
size_entry = tk.Entry(root)
size_entry.pack()
canvas_size = 500
canvas = create_board_canvas(root, canvas_size)
board = [[0 for _ in range(8)] for _ in range(8)]

canvas.bind("<Button-1>", lambda event: on_canvas_click(event, canvas, board))

check_button = tk.Button(root, text="Check Solution", command=lambda: show_solution_status(board))
check_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
