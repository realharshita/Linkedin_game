# N-Queens Solver

This folder contains Python scripts for solving the N-Queens problem using different approaches and interfaces.

## Scripts

1. **n_queens_gui.py**
   - Python script using tkinter for GUI.
   - Includes functions to create and draw a chessboard, place queens, and solve the N-Queens problem.
   - Provides a visual representation of the backtracking algorithm's execution.

2. **n_queens.py**
   - Command-line Python script.
   - Implements a recursive backtracking solution to find all possible configurations of placing N queens on an N×N chessboard without attacking each other.
   - Outputs solutions to the console.

3. **n_queens_user_gui.py**
   - Enhanced version of n_queens_gul.py with added features.
   - Includes timer, hints, and leaderboard functionalities.
   - Allows users to interactively place queens on the board and check solutions.
   
4. **Queens.py**
   - tkinter-based GUI game for placing queens on an 8x8 chessboard.
   - Divides the board into four regions, each requiring one queen per region.
   - Allows dragging queens across the board and marks invalid placements.

## Usage

- **n_queens_gui.py** and **n_queens_user_gui.py**: Run the scripts to interactively solve and visualize the N-Queens problem using tkinter.
- **n_queens.py**: Execute with a board size argument to find solutions from the command line.
- **Queens.py**: Run to play the interactive GUI game for placing queens on a specialized chessboard.

Each script provides a unique way to experience and solve the N-Queens problem. 
