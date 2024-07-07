import tkinter as tk

root = tk.Tk()
root.title("Queens Game")

BOARD_SIZE = 8
CELL_SIZE = 50
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE

canvas = tk.Canvas(root, width=BOARD_WIDTH, height=BOARD_HEIGHT)
canvas.pack()

# Define regions with their colors
REGIONS = [
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)],  # Top-left region
    [(0, 4), (0, 5), (0, 6), (0, 7), (1, 4), (1, 5), (1, 6), (1, 7), (2, 4), (2, 5), (2, 6), (2, 7), (3, 4), (3, 5), (3, 6), (3, 7)],  # Top-right region
    [(4, 0), (4, 1), (4, 2), (4, 3), (5, 0), (5, 1), (5, 2), (5, 3), (6, 0), (6, 1), (6, 2), (6, 3), (7, 0), (7, 1), (7, 2), (7, 3)],  # Bottom-left region
    [(4, 4), (4, 5), (4, 6), (4, 7), (5, 4), (5, 5), (5, 6), (5, 7), (6, 4), (6, 5), (6, 6), (6, 7), (7, 4), (7, 5), (7, 6), (7, 7)],  # Bottom-right region
]
COLORS = ["red", "blue", "green", "purple"]

board = [[""] * BOARD_SIZE for _ in range(BOARD_SIZE)]
queens_count = 0
dragging_queen = None

def handle_click(event):
    global queens_count, dragging_queen
    x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
    if board[y][x] == "Q":
        dragging_queen = (x, y)
    elif board[y][x] == "":
        mark_cannot_place(x, y)
    elif board[y][x] == "X":
        remove_mark(x, y)
    else:
        place_queen(x, y)

def handle_drag(event):
    global dragging_queen
    if dragging_queen:
        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            canvas.delete("drag")
            canvas.create_text(event.x, event.y, text="Q", font=("Arial", 20), tags="drag")

def handle_drop(event):
    global dragging_queen
    if dragging_queen:
        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
        old_x, old_y = dragging_queen
        if can_place_queen(y, x):
            remove_queen(old_x, old_y)
            place_queen(x, y)
        dragging_queen = None
        canvas.delete("drag")

def mark_cannot_place(col, row):
    global queens_count
    board[row][col] = "X"
    canvas.create_text(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2, text="X", font=("Arial", 20))
    update_region_count()

def remove_mark(col, row):
    global queens_count
    board[row][col] = ""
    canvas.delete(tk.ALL)
    redraw_board()
    update_queens_count()

def place_queen(col, row):
    global queens_count
    if can_place_queen(row, col):
        board[row][col] = "Q"
        queens_count += 1
        canvas.create_text(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2, text="Q", font=("Arial", 20))
        update_queens_count()
        update_region_count()

def remove_queen(col, row):
    global queens_count
    board[row][col] = ""
    queens_count -= 1
    canvas.delete(tk.ALL)
    redraw_board()
    update_queens_count()
    update_region_count()

def can_place_queen(row, col):
    # Check if the position is in the same region as any other queen
    for region in REGIONS:
        if (row, col) in region:
            for (r, c) in region:
                if board[r][c] == "Q":
                    return False
            break
    
    # Check if any queens are in the same row, column, or diagonal
    for i in range(BOARD_SIZE):
        if board[i][col] == "Q" or board[row][i] == "Q":
            return False
    for i in range(BOARD_SIZE):
        if (row + i < BOARD_SIZE and col + i < BOARD_SIZE and board[row + i][col + i] == "Q") or \
           (row - i >= 0 and col + i < BOARD_SIZE and board[row - i][col + i] == "Q") or \
           (row + i < BOARD_SIZE and col - i >= 0 and board[row + i][col - i] == "Q") or \
           (row - i >= 0 and col - i >= 0 and board[row - i][col - i] == "Q"):
            return False
    return True

def redraw_board():
    for region_index, region in enumerate(REGIONS):
        color = COLORS[region_index]
        for (row, col) in region:
            canvas.create_rectangle(col * CELL_SIZE, row * CELL_SIZE, (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE, fill=color, outline="black")
            if board[row][col] == "X":
                canvas.create_text(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2, text="X", font=("Arial", 20))
            elif board[row][col] == "Q":
                canvas.create_text(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2, text="Q", font=("Arial", 20))

def update_queens_count():
    queens_left = BOARD_SIZE - queens_count
    if queens_left > 0:
        result_label.config(text=f"Queens left to place: {queens_left}")
    else:
        result_label.config(text="All queens placed!")

def update_region_count():
    region_counts = [sum(board[row][col] == "Q" for row, col in region) for region in REGIONS]
    region_labels[0].config(text=f"Region 1 Queens: {region_counts[0]}")
    region_labels[1].config(text=f"Region 2 Queens: {region_counts[1]}")
    region_labels[2].config(text=f"Region 3 Queens: {region_counts[2]}")
    region_labels[3].config(text=f"Region 4 Queens: {region_counts[3]}")

def check_solution():
    if is_valid_solution():
        result_label.config(text="Valid solution!")
    else:
        result_label.config(text="Invalid solution!")

def is_valid_solution():
    queens_positions = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if board[row][col] == "Q"]
    for i in range(len(queens_positions)):
        for j in range(i + 1, len(queens_positions)):
            if attacks(queens_positions[i], queens_positions[j]):
                return False
    return True

def attacks(pos1, pos2):
    row1, col1 = pos1
    row2, col2 = pos2
    return row1 == row2 or col1 == col2 or abs(row1 - row2) == abs(col1 - col2)

def reset_board():
    global queens_count
    queens_count = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            board[row][col] = ""
    canvas.delete(tk.ALL)
    redraw_board()
    result_label.config(text="")
    update_region_count()

canvas.bind("<Button-1>", handle_click)
canvas.bind("<B1-Motion>", handle_drag)
canvas.bind("<ButtonRelease-1>", handle_drop)

check_button = tk.Button(root, text="Check Solution", command=check_solution)
check_button.pack()

reset_button = tk.Button(root, text="Reset Board", command=reset_board)
reset_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

region_labels = [tk.Label(root, text=f"Region {i + 1} Queens: 0") for i in range(4)]
for label in region_labels:
    label.pack()

redraw_board()
root.mainloop()
