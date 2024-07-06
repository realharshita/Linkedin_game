import tkinter as tk
import time
import os

LEADERBOARD_FILE = "leaderboard.txt"


LIGHT_THEME = {
    "bg": "white",
    "board_color1": "white",
    "board_color2": "gray",
    "queen_color": "black",
    "safe_spot_color": "yellow",
    "text_color": "black"
}

DARK_THEME = {
    "bg": "#2b2b2b",
    "board_color1": "#383838",
    "board_color2": "#505050",
    "queen_color": "white",
    "safe_spot_color": "#ffff00",
    "text_color": "white"
}

CURRENT_THEME = LIGHT_THEME  # Default theme

def create_board_canvas(root, size):
    canvas = tk.Canvas(root, width=size, height=size, bg=CURRENT_THEME["bg"], highlightthickness=0)
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
            color = CURRENT_THEME["board_color1"] if (i + j) % 2 == 0 else CURRENT_THEME["board_color2"]
            canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            if board[i][j] == 1:
                canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text="Q", font=("Arial", cell_size // 2, "bold"), fill=CURRENT_THEME["queen_color"])

def mark_unsafe_spots(board, row, col):
    n = len(board)
    # Mark horizontally
    for i in range(n):
        if board[row][i] == 0:
            board[row][i] = -1
    # Mark vertically
    for i in range(n):
        if board[i][col] == 0:
            board[i][col] = -1
    # Mark diagonally (top-left to bottom-right)
    r, c = row, col
    while r >= 0 and c >= 0:
        if board[r][c] == 0:
            board[r][c] = -1
        r -= 1
        c -= 1
    r, c = row, col
    while r < n and c < n:
        if board[r][c] == 0:
            board[r][c] = -1
        r += 1
        c += 1
    # Mark diagonally (top-right to bottom-left)
    r, c = row, col
    while r >= 0 and c < n:
        if board[r][c] == 0:
            board[r][c] = -1
        r -= 1
        c += 1
    r, c = row, col
    while r < n and c >= 0:
        if board[r][c] == 0:
            board[r][c] = -1
        r += 1
        c -= 1

def on_canvas_click(event, canvas, board):
    n = len(board)
    cell_size = canvas.winfo_width() // n
    row = event.y // cell_size
    col = event.x // cell_size
    if board[row][col] == 1:
        board[row][col] = 0
        mark_unsafe_spots(board, row, col)
    else:
        if board[row][col] == 0:
            board[row][col] = 1
            mark_unsafe_spots(board, row, col)
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
    if check_solution(board):
        stop_timer()
        transition_to_ending_screen(True)
    else:
        status_label.config(text="Solution is incorrect!", fg="red")

def transition_to_ending_screen(success):
    for widget in root.winfo_children():
        widget.pack_forget()

    if success:
        ending_label = tk.Label(root, text="Congratulations! You solved the N-Queens problem!", font=("Arial", 24))
        save_score()
    else:
        ending_label = tk.Label(root, text="Game Over! Time's up!", font=("Arial", 24))

    ending_label.pack(pady=20)

    exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 14))
    exit_button.pack(pady=10)

    restart_button = tk.Button(root, text="Restart", command=restart_application, font=("Arial", 14))
    restart_button.pack(pady=10)

    if success:
        leaderboard_label = tk.Label(root, text="Leaderboard", font=("Arial", 18))
        leaderboard_label.pack(pady=10)

        leaderboard_text = tk.Text(root, height=10, width=50, font=("Arial", 12))
        leaderboard_text.pack()
        leaderboard_text.insert(tk.END, get_leaderboard())
        leaderboard_text.config(state=tk.DISABLED)

def restart_application():
    for widget in root.winfo_children():
        widget.pack_forget()
    show_title_page()

def start_solver():
    try:
        n = int(size_entry.get())
        if n < 4:
            raise ValueError("Board size must be at least 4.")
    except ValueError as e:
        error_label.config(text=str(e))
        return

    for widget in root.winfo_children():
        widget.pack_forget()

    canvas = create_board_canvas(root, 500)
    canvas.pack(pady=20)
    board = [[0 for _ in range(n)] for _ in range(n)]

    canvas.bind("<Button-1>", lambda event: on_canvas_click(event, canvas, board))

    check_button = tk.Button(root, text="Check Solution", command=lambda: show_solution_status(board), font=("Arial", 14))
    check_button.pack(pady=10)

    hint_button = tk.Button(root, text="Hint", command=lambda: give_hint(board), font=("Arial", 14))
    hint_button.pack(pady=10)

    global status_label
    status_label = tk.Label(root, text="", font=("Arial", 14))
    status_label.pack(pady=10)

    global moves_label
    moves_label = tk.Label(root, text="Moves: 0", font=("Arial", 14))
    moves_label.pack(pady=10)

    global total_moves
    total_moves = 0

    draw_board(canvas, board)

    start_timer(60)  # Set the timer for 60 seconds

def give_hint(board):
    n = len(board)
    for col in range(n):
        for row in range(n):
            if board[row][col] == 0 and is_safe(board, row, col, n):

                canvas.itemconfig(board[row][col], fill=CURRENT_THEME["safe_spot_color"])
                return

def show_title_page():
    title_label = tk.Label(root, text="Welcome to the N-Queens Solver", font=("Arial", 24, "bold"), fg=CURRENT_THEME["text_color"], bg=CURRENT_THEME["bg"])
    title_label.pack(pady=20)

    instruction_label = tk.Label(root, text="Enter the board size and click Start:", font=("Arial", 14), fg=CURRENT_THEME["text_color"], bg=CURRENT_THEME["bg"])
    instruction_label.pack(pady=10)

    global size_entry
    size_entry = tk.Entry(root, font=("Arial", 14))
    size_entry.pack(pady=5)

    start_button = tk.Button(root, text="Start", command=start_solver, font=("Arial", 14))
    start_button.pack(pady=10)

    global error_label
    error_label = tk.Label(root, text="", fg="red", font=("Arial", 12), bg=CURRENT_THEME["bg"])
    error_label.pack(pady=5)

def start_timer(duration):
    global start_time
    start_time = time.time()
    global remaining_time
    remaining_time = duration
    update_timer()

def update_timer():
    if remaining_time > 0:
        mins, secs = divmod(remaining_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        timer_label.config(text="Time remaining: " + time_format, font=("Arial", 14), fg=CURRENT_THEME["text_color"], bg=CURRENT_THEME["bg"])
        global timer
        timer = root.after(1000, decrement_timer)
    else:
        transition_to_ending_screen(False)

def decrement_timer():
    global remaining_time
    remaining_time -= 1
    update_timer()

def stop_timer():
    root.after_cancel(timer)
    global end_time
    end_time = time.time()

def save_score():
    duration = end_time - start_time
    global total_moves
    with open(LEADERBOARD_FILE, "a") as f:

        player_name = "Anonymous"  # Replace with actual input from user
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{player_name},{duration},{total_moves},{timestamp}\n")

def get_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return "No scores yet!"
    with open(LEADERBOARD_FILE, "r") as f:
        scores = [line.strip().split(",") for line in f.readlines()]
    scores.sort(key=lambda x: float(x[1]))  
    leaderboard = "\n".join(f"{i+1}. {score[0]} - {score[1]:.2f} seconds, Moves: {score[2]}, ({score[3]})" for i, score in enumerate(scores[:10]))
    return leaderboard


def toggle_theme():
    global CURRENT_THEME
    if CURRENT_THEME == LIGHT_THEME:
        CURRENT_THEME = DARK_THEME
    else:
        CURRENT_THEME = LIGHT_THEME
    root.config(bg=CURRENT_THEME["bg"])
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text)):
            widget.config(bg=CURRENT_THEME["bg"], fg=CURRENT_THEME["text_color"])
    draw_board(canvas, board)

root = tk.Tk()
root.title("Interactive N-Queens Solver")
root.config(bg=CURRENT_THEME["bg"])

timer_label = tk.Label(root, text="", font=("Arial", 14), fg=CURRENT_THEME["text_color"], bg=CURRENT_THEME["bg"])
timer_label.pack(pady=10)

show_title_page()

theme_button = tk.Button(root, text="Toggle Theme", command=toggle_theme, font=("Arial", 14))
theme_button.pack(pady=10)

root.mainloop()
