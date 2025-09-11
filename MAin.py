# tic_tac_toe.py
# Two-player (local) Tic Tac Toe in the terminal

from typing import List, Optional

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6)              # diagonals
]

def print_board(board: List[str]) -> None:
    """Pretty print the 3x3 board."""
    cells = [c if c != " " else str(i+1) for i, c in enumerate(board)]
    row_sep = "───┼───┼───"
    def row(a,b,c): return f" {a} │ {b} │ {c} "
    print()
    print(row(cells[0], cells[1], cells[2]))
    print(row_sep)
    print(row(cells[3], cells[4], cells[5]))
    print(row_sep)
    print(row(cells[6], cells[7], cells[8]))
    print()

def winner(board: List[str]) -> Optional[str]:
    """Return 'X' or 'O' if someone won, else None."""
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None

def board_full(board: List[str]) -> bool:
    return all(c != " " for c in board)

def ask_move(player: str, board: List[str]) -> int:
    """Ask current player for a move (1-9), validate, and return 0-8 index."""
    while True:
        raw = input(f"Player {player}, choose a cell (1-9): ").strip()
        if not raw.isdigit():
            print("Please enter a number between 1 and 9.")
            continue
        pos = int(raw)
        if not (1 <= pos <= 9):
            print("Out of range. Choose 1-9.")
            continue
        idx = pos - 1
        if board[idx] != " ":
            print("That cell is taken. Choose another.")
            continue
        return idx

def play_round(starting_player: str) -> str:
    """Play one round. Returns 'X', 'O', or 'D' (draw)."""
    board = [" "] * 9
    current = starting_player

    while True:
        print_board(board)
        move = ask_move(current, board)
        board[move] = current

        win = winner(board)
        if win:
            print_board(board)
            print(f"🎉 Player {win} wins!")
            return win

        if board_full(board):
            print_board(board)
            print("🤝 It's a draw.")
            return "D"

        current = "O" if current == "X" else "X"

def main():
    print("=== Tic Tac Toe (2 Players) ===")
    print("Players take turns as X and O. Choose cells by number (1–9).")
    print("Board numbers:")
    print_board([str(i) for i in range(1, 10)])

    scores = {"X": 0, "O": 0, "D": 0}
    starting_player = "X"

    while True:
        result = play_round(starting_player)
        scores[result] += 1

        # Alternate who starts next round for fairness
        starting_player = "O" if starting_player == "X" else "X"

        print(f"\nScore →  X: {scores['X']}   O: {scores['O']}   Draws: {scores['D']}")
        again = input("Play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Thanks for playing! 👋")
            break

if __name__ == "__main__":
    main()
