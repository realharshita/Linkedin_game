import tkinter as tk
import time
import random
import os

# Constants
BOARD_SIZE = 8
SQUARE_SIZE = 50
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE
LIGHT_THEME = {
    "bg": "white",
    "text_color": "black",
    "highlight_color": "lightgrey"
}
DARK_THEME = {
    "bg": "#1e1e1e",
    "text_color": "white",
    "highlight_color": "#2e2e2e"
}
CURRENT_THEME = LIGHT_THEME  # Initial theme

# Global variables
board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
remaining_time = 60
timer = None
start_time = None
end_time = None
moves_count = 0
hint_count = 3  # Example: Allow up to 3 hints
total_moves = 0
successful_attempts = 0
total_attempts = 0
total_solve_time = 0
LEADERBOARD_FILE = "leaderboard.txt"

def initialize_board():
    global board
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

def draw_board(canvas, board):
    canvas.delete("all")
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x1, y1 = col * SQUARE_SIZE, row * SQUARE_SIZE
            x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
            color = CURRENT_THEME["bg"]
            if (row + col) % 2 == 0:
                color = CURRENT_THEME["highlight_color"]
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            if board[row][col] == 1:
                canvas.create_text(x1 + SQUARE_SIZE // 2, y1 + SQUARE_SIZE // 2, text="♕", font=("Arial", 24), fill=CURRENT_THEME["text_color"])

def place_queen(row, col):
    global board
    board[row][col] = 1

def remove_queen(row, col):
    global board
    board[row][col] = 0

def is_safe(board, row, col):
    # Check row and column
    for i in range(BOARD_SIZE):
        if board[row][i] == 1 or board[i][col] == 1:
            return False
    # Check diagonals
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if (i + j == row + col) or (i - j == row - col):
                if board[i][j] == 1:
                    return False
    return True

def solve_n_queens(board, col):
    if col >= BOARD_SIZE:
        return True
    for i in range(BOARD_SIZE):
        if is_safe(board, i, col):
            place_queen(i, col)
            if solve_n_queens(board, col + 1):
                return True
            remove_queen(i, col)
    return False

def start_solver():
    global start_time, remaining_time, moves_count
    initialize_board()
    if solve_n_queens(board, 0):
        start_time = time.time()
        remaining_time = 60
        moves_count = 0
        update_timer()
        draw_board(canvas, board)
        show_game_ui()
    else:
        print("No solution found for this board size.")

def on_canvas_click(event):
    global moves_count
    row = event.y // SQUARE_SIZE
    col = event.x // SQUARE_SIZE
    if board[row][col] == 1:
        remove_queen(row, col)
    else:
        place_queen(row, col)
    mark_unsafe_spots()

def mark_unsafe_spots():
    global board
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 1:
                mark_attacking_spots(row, col)

def mark_attacking_spots(row, col):
    global board
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if (i == row or j == col or i + j == row + col or i - j == row - col) and not (i == row and j == col):
                if board[i][j] == 0:
                    board[i][j] = -1

def show_game_ui():
    for widget in root.winfo_children():
        widget.pack_forget()
    canvas.pack()

    check_solution_button.pack(pady=10)
    hint_button.pack(pady=10)
    timer_label.pack(pady=10)

def show_title_page():
    for widget in root.winfo_children():
        widget.pack_forget()
    title_label.pack(pady=50)
    start_button.pack(pady=20)

def show_solution_status(board):
    global successful_attempts, total_attempts
    if check_solution(board):
        successful_attempts += 1
        stop_timer()
        transition_to_ending_screen(True)
    else:
        status_label.config(text="Solution is incorrect!", fg="red")

def check_solution(board):
    queens_count = sum(sum(row) for row in board)
    if queens_count == BOARD_SIZE:
        for col in range(BOARD_SIZE):
            if sum(row[col] for row in board) != 1:
                return False
        return True
    return False

def update_timer():
    global remaining_time
    if remaining_time > 0:
        mins, secs = divmod(remaining_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        timer_label.config(text="Time remaining: " + time_format, font=("Arial", 14), fg=CURRENT_THEME["text_color"], bg=CURRENT_THEME["bg"])
        global timer
        timer = root.after(1000, decrement_timer)
    else:
        stop_timer()
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
    global total_moves, successful_attempts, total_attempts, total_solve_time
    total_moves += moves_count
    total_solve_time += duration
    total_attempts += 1
    if check_solution(board):
        successful_attempts += 1
    with open(LEADERBOARD_FILE, "a") as f:
        player_name = "Anonymous"  # Replace with actual input from user
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{player_name},{duration},{moves_count},{timestamp}\n")

def get_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return "No scores yet!"
    with open(LEADERBOARD_FILE, "r") as f:
        scores = [line.strip().split(",") for line in f.readlines()]
    scores.sort(key=lambda x: float(x[1]))  # Sort by duration
    leaderboard = "\n".join(f"{i+1}. {score[0]} - {score[1]:.2f} seconds, Moves: {score[2]}, ({score[3]})" for i, score in enumerate(scores[:10]))
    return leaderboard

def transition_to_ending_screen(success):
    global successful_attempts, total_attempts
    for widget in root.winfo_children():
        widget.pack_forget()

    if success:
        ending_label = tk.Label(root, text="Congratulations! You solved the N-Queens problem!", font=("Arial", 24))
    else:
        ending_label = tk.Label(root, text="Game Over! Time's up!", font=("Arial", 24))

    ending_label.pack(pady=20)

    stats_label = tk.Label(root, text=f"Statistics:\n"
                                      f"Total Attempts: {total_attempts}\n"
                                      f"Successful Attempts: {successful_attempts}\n"
                                      f"Average Moves: {total_moves / total_attempts:.2f}\n"
                                      f"Average Solve Time: {total_solve_time / total_attempts:.2f} seconds",
                           font=("Arial", 16))
    stats_label.pack(pady=20)

    exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 14))
    exit_button.pack(pady=10)

    restart_button = tk.Button(root, text="Restart", command=restart_application, font=("Arial", 14))
    restart_button.pack(pady=10)

def give_hint(board):
    global hint_count
    if hint_count > 0:
        hint_count -= 1
        safe_spots = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == 0 and is_safe(board, row, col):
                    safe_spots.append((row, col))
        if safe_spots:
            row, col = random.choice(safe_spots)
            highlight_hint(row, col)
    else:
        status_label.config(text="No more hints left!", fg="red")

def highlight_hint(row, col):
    canvas.create_rectangle(col * SQUARE_SIZE, row * SQUARE_SIZE, (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                            outline="yellow", width=3)

def restart_application():
    for widget in root.winfo_children():
        widget.pack_forget()
    initialize_board()
    show_title_page()

root = tk.Tk()
root.title("N-Queens Solver")
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")

# Create canvas for drawing the board
canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE, bg=CURRENT_THEME["bg"])
canvas.bind("<Button-1>", on_canvas_click)

# Title page elements
title_label = tk.Label(root, text="N-Queens Solver", font=("Arial", 24))
start_button = tk.Button(root, text="Start Game", command=start_solver, font=("Arial", 14))

# Game UI elements
check_solution_button = tk.Button(root, text="Check Solution", command=lambda: show_solution_status(board), font=("Arial", 14))
hint_button = tk.Button(root, text="Hint (3 left)", command=lambda: give_hint(board), font=("Arial", 14))
timer_label = tk.Label(root, text="Time remaining: 01:00", font=("Arial", 14), fg=CURRENT_THEME["text_color"], bg=CURRENT_THEME["bg"])

# Leaderboard display
leaderboard_label = tk.Label(root, text="Leaderboard", font=("Arial", 20))
leaderboard_text = tk.Text(root, width=50, height=10, font=("Arial", 12), wrap=tk.WORD)
leaderboard_text.insert(tk.END, get_leaderboard())
leaderboard_text.config(state=tk.DISABLED)

show_title_page()
root.mainloop()
