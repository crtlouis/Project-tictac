# CONNECT FOUR — Modern Tkinter UI (functions only, no classes)
# Scope: Think Python Ch. 1–13 (+18), standard library only.

import tkinter as tk

# -------------------- CONFIG --------------------

ROWS = 6
COLS = 7
CELL = 92           # pixel size per cell (board = COLS*CELL × ROWS*CELL)
PADDING = 10        # inner padding for discs
ANIM_DY = 18        # animation speed (pixels per frame)
TITLE = "Connect Four — 2025 Edition"

THEME_DARK = {
    "bg":        "#0b0f1a",
    "panel":     "#111827",
    "board":     "#1e293b",
    "hole":      "#0f172a",
    "grid":      "#0ea5e9",
    "text":      "#e5e7eb",
    "muted":     "#94a3b8",
    "accent":    "#38bdf8",
    "p1":        "#ef4444",   # red
    "p2":        "#f59e0b",   # amber
    "shadow":    "#000000",
}
THEME_LIGHT = {
    "bg":        "#f5f7fb",
    "panel":     "#e7ecf5",
    "board":     "#cbd5e1",
    "hole":      "#ffffff",
    "grid":      "#2563eb",
    "text":      "#0f172a",
    "muted":     "#334155",
    "accent":    "#2563eb",
    "p1":        "#ef4444",
    "p2":        "#f59e0b",
    "shadow":    "#111111",
}

# -------------------- STATE --------------------

board = []                 # list of lists: ' ' (empty), 'R', 'Y'
current_symbol = 'R'       # whose turn ('R' or 'Y')
game_over = False
animating = False
last_move = None           # (r, c)
hover_col = None           # column under the mouse
scores = {"R": 0, "Y": 0, "D": 0}
THEME = THEME_DARK

# -------------------- MECHANICS --------------------

def create_board():
    b = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(' ')
        b.append(row)
    return b

def is_valid_column(b, col):
    if col is None or col < 0 or col >= COLS:
        return False
    return b[0][col] == ' '

def drop_target_row(b, col):
    """Return the row index where a disc would land in this column, or None if full."""
    if not (0 <= col < COLS): 
        return None
    r = ROWS - 1
    while r >= 0:
        if b[r][col] == ' ':
            return r
        r -= 1
    return None

def place_piece(b, r, c, sym):
    b[r][c] = sym

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(b, r0, c0, dr, dc, sym):
    cnt = 0
    r, c = r0 + dr, c0 + dc
    while in_bounds(r, c) and b[r][c] == sym:
        cnt += 1
        r += dr
        c += dc
    return cnt

def is_winning_move(b, r, c, sym):
    dirs = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in dirs:
        total = 1
        total += count_in_direction(b, r, c, dr, dc, sym)
        total += count_in_direction(b, r, c, -dr, -dc, sym)
        if total >= 4:
            return True
    return False

def is_board_full(b):
    for c in range(COLS):
        if b[0][c] == ' ':
            return False
    return True

# -------------------- UI DRAWING --------------------

def symbol_to_color(sym):
    if sym == 'R':
        return THEME["p1"]
    if sym == 'Y':
        return THEME["p2"]
    return THEME["hole"]

def set_status(text):
    status_var.set(text)

def player_name(sym):
    return "Player 1 (Red)" if sym == 'R' else "Player 2 (Yellow)"

def draw_rounded_rect(canvas, x1, y1, x2, y2, r, fill, outline="", width=1):
    """Rounded rectangle using 4 arcs + 4 rectangles (simple, no alpha)."""
    # Corners
    canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, style="pieslice",
                      outline=outline, width=width, fill=fill)
    canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, style="pieslice",
                      outline=outline, width=width, fill=fill)
    canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style="pieslice",
                      outline=outline, width=width, fill=fill)
    canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style="pieslice",
                      outline=outline, width=width, fill=fill)
    # Edges
    canvas.create_rectangle(x1+r, y1, x2-r, y2, outline=outline, width=0, fill=fill)
    canvas.create_rectangle(x1, y1+r, x2, y2-r, outline=outline, width=0, fill=fill)
    if outline and width > 0:
        # simple outline on the box edges
        canvas.create_rectangle(x1+r, y1, x2-r, y1, outline=outline, width=width)
        canvas.create_rectangle(x1+r, y2, x2-r, y2, outline=outline, width=width)
        canvas.create_rectangle(x1, y1+r, x1, y2-r, outline=outline, width=width)
        canvas.create_rectangle(x2, y1+r, x2, y2-r, outline=outline, width=width)

def draw_disc(canvas, r, c, color, ring=False, glow=False):
    """Draw a disc with a subtle inner ring and optional glow/last-move ring."""
    x1 = c*CELL + PADDING
    y1 = r*CELL + PADDING
    x2 = (c+1)*CELL - PADDING
    y2 = (r+1)*CELL - PADDING

    # Shadow under disc
    canvas.create_oval(x1+2, y1+3, x2+2, y2+3, fill=THEME["shadow"], width=0)

    # Base disc
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline="#111111", width=2)

    # Inner ring for depth
    inset = 10
    canvas.create_oval(x1+inset, y1+inset, x2-inset, y2-inset,
                       outline="#000000", width=1)

    # Specular highlight (tiny top-left glossy spot)
    hl = 16
    canvas.create_oval(x1+inset-6, y1+inset-6, x1+inset-6+hl, y1+inset-6+hl,
                       fill="#ffffff", outline="")

    # Last-move glow ring
    if glow:
        canvas.create_oval(x1-4, y1-4, x2+4, y2+4,
                           outline=THEME["accent"], width=4)

def draw_board(canvas):
    canvas.delete("all")
    # Background
    canvas.configure(bg=THEME["bg"])

    # Board with rounded corners
    br = 22
    draw_rounded_rect(canvas, 0, 0, COLS*CELL, ROWS*CELL, br,
                      fill=THEME["board"], outline="", width=0)

    # Optional column hover highlight
    if hover_col is not None and 0 <= hover_col < COLS:
        x1 = hover_col*CELL
        x2 = (hover_col+1)*CELL
        canvas.create_rectangle(x1, 0, x2, ROWS*CELL, fill=THEME["panel"], width=0)

    # Holes / discs
    for r in range(ROWS):
        for c in range(COLS):
            x1 = c*CELL + PADDING
            y1 = r*CELL + PADDING
            x2 = (c+1)*CELL - PADDING
            y2 = (r+1)*CELL - PADDING
            if board[r][c] == ' ':
                # Empty hole with subtle border
                canvas.create_oval(x1, y1, x2, y2, fill=THEME["hole"], outline="#0b1222", width=2)
            else:
                color = symbol_to_color(board[r][c])
                glow = (last_move == (r, c))
                draw_disc(canvas, r, c, color, ring=True, glow=glow)

    # Ghost preview disc (top)
    if hover_col is not None and is_valid_column(board, hover_col):
        ghost_row = drop_target_row(board, hover_col)
        if ghost_row is not None:
            # draw a thin outline disc at the target cell to preview
            x1 = hover_col*CELL + PADDING
            y1 = ghost_row*CELL + PADDING
            x2 = (hover_col+1)*CELL - PADDING
            y2 = (ghost_row+1)*CELL - PADDING
            color = symbol_to_color(current_symbol)
            canvas.create_oval(x1, y1, x2, y2, outline=color, width=3)

def refresh_theme():
    # Window + panels
    root.configure(bg=THEME["bg"])
    top_bar.configure(bg=THEME["panel"])
    title_label.configure(bg=THEME["panel"], fg=THEME["text"])
    btn_new.configure(bg=THEME["panel"], fg=THEME["text"], activebackground=THEME["board"])
    btn_reset_scores.configure(bg=THEME["panel"], fg=THEME["text"], activebackground=THEME["board"])
    btn_theme.configure(bg=THEME["panel"], fg=THEME["text"], activebackground=THEME["board"])
    status_label.configure(bg=THEME["bg"], fg=THEME["muted"])
    score_frame.configure(bg=THEME["bg"])
    p1_score_label.configure(bg=THEME["bg"], fg=THEME["text"])
    p2_score_label.configure(bg=THEME["bg"], fg=THEME["text"])
    d_score_label.configure(bg=THEME["bg"], fg=THEME["muted"])
    draw_board(canvas)

# -------------------- INTERACTION --------------------

def end_game(message, winner=None):
    global game_over, scores
    game_over = True
    set_status(message + "  Click NEW MATCH to play again.")
    if winner == 'R':
        scores["R"] += 1
    elif winner == 'Y':
        scores["Y"] += 1
    elif winner == 'D':
        scores["D"] += 1
    update_scores()

def update_scores():
    p1_score_label.config(text=f"Red: {scores['R']}")
    p2_score_label.config(text=f"Yellow: {scores['Y']}")
    d_score_label.config(text=f"Draws: {scores['D']}")

def toggle_theme():
    global THEME
    THEME = THEME_LIGHT if THEME is THEME_DARK else THEME_DARK
    refresh_theme()

def on_motion(event):
    global hover_col
    if animating or game_over:
        return
    col = event.x // CELL
    if 0 <= col < COLS:
        hover_col = col
    else:
        hover_col = None
    draw_board(canvas)

def on_leave(event):
    global hover_col
    hover_col = None
    draw_board(canvas)

def handle_click(event):
    global animating
    if animating or game_over:
        return
    col = event.x // CELL
    if not is_valid_column(board, col):
        set_status("Column not valid. Pick another.")
        return
    target_row = drop_target_row(board, col)
    if target_row is None:
        set_status("Column is full. Try a different one.")
        return
    start_drop_animation(col, target_row)

def start_drop_animation(col, target_row):
    """Animate a disc falling, then commit the move."""
    global animating
    animating = True

    # Disc visuals for animation
    color = symbol_to_color(current_symbol)
    x1 = col*CELL + PADDING
    x2 = (col+1)*CELL - PADDING
    # start just above the top cell
    y_top = -CELL + PADDING
    y_dest = target_row*CELL + PADDING
    disc = canvas.create_oval(x1, y_top, x2, y_top+(CELL-2*PADDING), fill=color, outline="#111111", width=2)

    def step(y):
        nonlocal disc
        if y < y_dest:
            ny = min(y + ANIM_DY, y_dest)
            dy = ny - y
            canvas.move(disc, 0, dy)
            canvas.after(12, step, ny)
        else:
            canvas.delete(disc)
            finalize_move(target_row, col)

    step(y_top)

def finalize_move(r, c):
    global current_symbol, last_move, animating
    place_piece(board, r, c, current_symbol)
    last_move = (r, c)
    draw_board(canvas)

    # Check outcomes
    if is_winning_move(board, r, c, current_symbol):
        end_game(f"🎉 {player_name(current_symbol)} wins!", winner=current_symbol)
    elif is_board_full(board):
        end_game("It's a draw!", winner='D')
    else:
        # switch player
        current_symbol = 'Y' if current_symbol == 'R' else 'R'
        set_status(f"{player_name(current_symbol)} — click a column to drop your piece.")
    animating = False

def new_match():
    global board, current_symbol, game_over, animating, last_move, hover_col
    board = create_board()
    current_symbol = 'R'
    game_over = False
    animating = False
    last_move = None
    hover_col = None
    draw_board(canvas)
    set_status(f"{player_name(current_symbol)} starts. Click a column to drop your piece.")

def reset_scores():
    global scores
    scores = {"R": 0, "Y": 0, "D": 0}
    update_scores()
    set_status("Scores reset. Start a new match!")

# -------------------- BOOTSTRAP --------------------

root = tk.Tk()
root.title(TITLE)
root.resizable(False, False)
root.configure(bg=THEME["bg"])

# Top bar
top_bar = tk.Frame(root, bg=THEME["panel"])
top_bar.pack(fill="x", padx=12, pady=(12, 8))

title_label = tk.Label(top_bar, text="Connect Four", font=("Segoe UI", 16, "bold"),
                       bg=THEME["panel"], fg=THEME["text"])
title_label.pack(side="left")

btn_new = tk.Button(top_bar, text="NEW MATCH", command=new_match,
                    relief="flat", padx=12, pady=6, bg=THEME["panel"], fg=THEME["text"])
btn_new.pack(side="right", padx=6)

btn_reset_scores = tk.Button(top_bar, text="RESET SCORES", command=reset_scores,
                             relief="flat", padx=12, pady=6, bg=THEME["panel"], fg=THEME["text"])
btn_reset_scores.pack(side="right", padx=6)

btn_theme = tk.Button(top_bar, text="THEME", command=toggle_theme,
                      relief="flat", padx=12, pady=6, bg=THEME["panel"], fg=THEME["text"])
btn_theme.pack(side="right", padx=6)

# Canvas (board)
canvas = tk.Canvas(root, width=COLS*CELL, height=ROWS*CELL, bg=THEME["bg"], highlightthickness=0)
canvas.pack(padx=12, pady=(0, 6))

canvas.bind("<Button-1>", handle_click)
canvas.bind("<Motion>", on_motion)
canvas.bind("<Leave>", on_leave)

# Status + scores
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, font=("Segoe UI", 11),
                        bg=THEME["bg"], fg=THEME["muted"])
status_label.pack(pady=(2, 4))

score_frame = tk.Frame(root, bg=THEME["bg"])
score_frame.pack(pady=(0, 12))

p1_score_label = tk.Label(score_frame, text="Red: 0", font=("Segoe UI", 11, "bold"),
                          bg=THEME["bg"], fg=THEME["text"])
p1_score_label.grid(row=0, column=0, padx=10)

p2_score_label = tk.Label(score_frame, text="Yellow: 0", font=("Segoe UI", 11, "bold"),
                          bg=THEME["bg"], fg=THEME["text"])
p2_score_label.grid(row=0, column=1, padx=10)

d_score_label = tk.Label(score_frame, text="Draws: 0", font=("Segoe UI", 10),
                         bg=THEME["bg"], fg=THEME["muted"])
d_score_label.grid(row=0, column=2, padx=10)

# Init
def start():
    new_match()
    update_scores()
    refresh_theme()
    set_status(f"{player_name('R')} starts. Click a column to drop your piece.")

start()
root.mainloop()
print ("test louis")