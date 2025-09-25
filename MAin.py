#Connect four main
# Step 1: Create and print an empty Connect Four board

ROWS = 6
COLS = 7

def create_board():
    """
    Create an empty board as a list of lists.
    Each cell starts as a single space ' '.
    """
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    """
    Print the board in a simple text format.
    Top row = row 0, bottom row = row 5.
    """
    print()
    for r in range(ROWS):
        line = "|"
        for c in range(COLS):
            line += board[r][c] + "|"
        print(line)
    print("+" + "-+" * COLS)   # separator line

    # column numbers at the bottom
    nums = " "
    for c in range(COLS):
        nums += str(c) + " "
    print(nums)
    print()

# Test Step 1
def main():
    board = create_board()
    print_board(board)

    # quick test: put an 'X' in bottom row, col 3
    board[5][3] = 'X'
    print_board(board)

if __name__ == "__main__":
    main()
