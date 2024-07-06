import tkinter as tk

def create_board_canvas(root, size):
    canvas = tk.Canvas(root, width=size, height=size)
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
    if check_solution(board):
        transition_to_ending_screen(True)
    else:
        status_label.config(text="Solution is incorrect!", fg="red")

def transition_to_ending_screen(success):
    for widget in root.winfo_children():
        widget.pack_forget()

    if success:
        ending_label = tk.Label(root, text="Congratulations! You solved the N-Queens problem!", font=("Arial", 24))
    else:
        ending_label = tk.Label(root, text="Time's up! Better luck next time!", font=("Arial", 24))

    ending_label.pack(pady=20)

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

    restart_button = tk.Button(root, text="Restart", command=restart_application)
    restart_button.pack(pady=10)

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
    canvas.pack()
    board = [[0 for _ in range(n)] for _ in range(n)]

    canvas.bind("<Button-1>", lambda event: on_canvas_click(event, canvas, board))

    check_button = tk.Button(root, text="Check Solution", command=lambda: show_solution_status(board))
    check_button.pack()

    global status_label
    status_label = tk.Label(root, text="")
    status_label.pack()

    draw_board(canvas, board)

    start_timer(60)  # Set the timer for 60 seconds

def show_title_page():
    title_label = tk.Label(root, text="Welcome to the N-Queens Solver", font=("Arial", 24))
    title_label.pack(pady=20)

    instruction_label = tk.Label(root, text="Enter the board size and click Start:")
    instruction_label.pack(pady=10)

    global size_entry
    size_entry = tk.Entry(root)
    size_entry.pack(pady=5)

    start_button = tk.Button(root, text="Start", command=start_solver)
    start_button.pack(pady=10)

    global error_label
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack(pady=5)

def start_timer(duration):
    global remaining_time
    remaining_time = duration
    update_timer()

def update_timer():
    if remaining_time > 0:
        mins, secs = divmod(remaining_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        timer_label.config(text="Time remaining: " + time_format)
        global timer
        timer = root.after(1000, decrement_timer)
    else:
        transition_to_ending_screen(False)

def decrement_timer():
    global remaining_time
    remaining_time -= 1
    update_timer()

root = tk.Tk()
root.title("Interactive N-Queens Solver")

timer_label = tk.Label(root, text="", font=("Arial", 14))
timer_label.pack()

show_title_page()
root.mainloop()
