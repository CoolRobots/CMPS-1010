import pygame
import sys
import random
import pyperclip

pygame.init()
#------------------------------
# LOGIC VARS
#-----------------------------
last_row=0
last_col=0

# -----------------------------
# UI CONFIGURATION
# -----------------------------
BG_COLOR = (245, 245, 245)
PANEL_COLOR = (225, 225, 235)
BUTTON_COLOR = (180, 200, 255)
BUTTON_HOVER = (160, 180, 240)
GRID_LINE = (80, 80, 80)
FILLED_COLOR = (40, 40, 40)
EMPTY_COLOR = (255, 255, 255)
X_COLOR = (200, 60, 60)
TEXT_COLOR = (30, 30, 30)

CELL_SIZE = 40
CLUE_FONT_SIZE = 26

TITLE_FONT = pygame.font.SysFont("Segoe UI", 48, bold=True)
FONT = pygame.font.SysFont("Segoe UI", 28)
SMALL_FONT = pygame.font.SysFont("Segoe UI", 22)

# -----------------------------
# RANDOM PUZZLE GENERATION
# -----------------------------
def generate_random_grid(size):
    return [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]

# -----------------------------
# CLUE GENERATION
# -----------------------------
def generate_clues(grid):
    row_clues = []
    col_clues = []

    for row in grid:
        clues, count = [], 0
        for cell in row:
            if cell == 1:
                count += 1
            else:
                if count:
                    clues.append(count)
                    count = 0
        if count:
            clues.append(count)
        row_clues.append(clues or [0])

    for col in range(len(grid[0])):
        clues, count = [], 0
        for row in range(len(grid)):
            if grid[row][col] == 1:
                count += 1
            else:
                if count:
                    clues.append(count)
                    count = 0
        if count:
            clues.append(count)
        col_clues.append(clues or [0])

    return row_clues, col_clues
#------------------------------
# AWESOME UNIQUE SOLUTION CHECKER
#------------------------------
def generate_line_patterns(length, clues):
    # Special case: checks for empty row/column, making puzzle impossible
    if clues == [0]:
        return [[0] * length]

    results = []

    def backtrack(pos, clue_index, current):
        if clue_index == len(clues):
            # Fill remaining cells with 0
            results.append(current + [0] * (length - len(current)))
            return

        block = clues[clue_index]
        # Earliest and latest start positions for this block
        min_pos = pos
        max_pos = length - sum(clues[clue_index:]) - (len(clues) - clue_index - 1)

        for start in range(min_pos, max_pos + 1):
            new_line = current + [0] * (start - len(current)) + [1] * block
            if len(new_line) < length:
                new_line.append(0)  # required separator unless last block
            backtrack(start + block + 1, clue_index + 1, new_line)

    backtrack(0, 0, [])
    return results


def solve_all(row_clues, col_clues, limit=2):
    size = len(row_clues)

    # Precompute all valid patterns for each row and column
    row_patterns = [generate_line_patterns(size, rc) for rc in row_clues]
    col_patterns = [generate_line_patterns(size, cc) for cc in col_clues]

    # Grid starts empty (None = unknown)
    grid = [[None] * size for _ in range(size)]
    solutions = 0

    # Check if the partial grid is still compatible with column patterns
    def is_valid_partial(r):
        for col in range(size):
            col_vals = [grid[row][col] for row in range(r + 1)]
            # A column is valid if at least one pattern matches the prefix
            if not any(pattern[:r + 1] == col_vals for pattern in col_patterns[col]):
                return False
        return True

    def backtrack_row(r):
        nonlocal solutions
        if solutions >= limit:
            return

        if r == size:
            solutions += 1
            return

        for pattern in row_patterns[r]:
            # Place pattern into row r
            for c in range(size):
                grid[r][c] = pattern[c]

            if is_valid_partial(r):
                backtrack_row(r + 1)

            if solutions >= limit:
                return

    backtrack_row(0)
    return solutions
# -----------------------------
# UI POLISH
# -----------------------------
def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_text_shadow(surface, text, font, x, y, color=TEXT_COLOR):
    shadow = font.render(text, True, (0, 0, 0))
    surface.blit(shadow, (x + 2, y + 2))
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

# -----------------------------
# HOME SCREEN
# -----------------------------
def home_screen(screen):

    dropdown_open = False
    puzzle_sizes = [5, 10, 15]
    selected_size = 5

    clock = pygame.time.Clock()

    SCREEN_W, SCREEN_H = screen.get_size()

    # UI element sizes
    DROPDOWN_W, DROPDOWN_H = 260, 55
    BUTTON_W, BUTTON_H = 240, 60
    OPTION_SPACING = DROPDOWN_H + 10

    # Vertical layout
    TITLE_Y = 80
    DROPDOWN_Y = 200
    OPTIONS_TOP = DROPDOWN_Y + DROPDOWN_H + 15
    BUTTON_Y = OPTIONS_TOP + OPTION_SPACING * len(puzzle_sizes) + 60

    CUSTOM_BUTTON = pygame.Rect((SCREEN_W - BUTTON_W) - 50, DROPDOWN_Y, BUTTON_W, BUTTON_H)
    IMPORT_BUTTON = pygame.Rect((SCREEN_W - BUTTON_W) - 50, BUTTON_Y, BUTTON_W, BUTTON_H)

    while True:
        screen.fill(BG_COLOR)
        mx, my = pygame.mouse.get_pos()
        # --- CUSTOM PUZZLE BUTTON ---
        hovered = CUSTOM_BUTTON.collidepoint(mx, my)
        draw_rounded_rect(screen, BUTTON_HOVER if hovered else BUTTON_COLOR, CUSTOM_BUTTON)
        pygame.draw.rect(screen, GRID_LINE, CUSTOM_BUTTON, 2, border_radius=10)
        txt = FONT.render("Create Puzzle", True, TEXT_COLOR)
        screen.blit(txt, (CUSTOM_BUTTON.centerx - txt.get_width() // 2,
                        CUSTOM_BUTTON.centery - txt.get_height() // 2))

        # --- IMPORT PUZZLE BUTTON ---
        hovered = IMPORT_BUTTON.collidepoint(mx, my)
        draw_rounded_rect(screen, BUTTON_HOVER if hovered else BUTTON_COLOR, IMPORT_BUTTON)
        pygame.draw.rect(screen, GRID_LINE, IMPORT_BUTTON, 2, border_radius=10)
        txt = FONT.render("Import Puzzle", True, TEXT_COLOR)
        screen.blit(txt, (IMPORT_BUTTON.centerx - txt.get_width() // 2,
                        IMPORT_BUTTON.centery - txt.get_height() // 2))

        # ----- TITLE -----
        title_text = TITLE_FONT.render("Jackson's Awesome Picross", True, TEXT_COLOR)
        title_x = (SCREEN_W - title_text.get_width()) // 2
        screen.blit(title_text, (title_x, TITLE_Y))

        # ----- DROPDOWN -----
        dropdown_rect = pygame.Rect(
            50,
            DROPDOWN_Y,
            DROPDOWN_W,
            DROPDOWN_H
        )

        draw_rounded_rect(screen, PANEL_COLOR, dropdown_rect)
        pygame.draw.rect(screen, GRID_LINE, dropdown_rect, 2, border_radius=10)

        selected_text = FONT.render(f"Puzzle Size: {selected_size}×{selected_size}", True, TEXT_COLOR)
        screen.blit(
            selected_text,
            (dropdown_rect.centerx - selected_text.get_width() // 2,
             dropdown_rect.centery - selected_text.get_height() // 2)
        )

        # ----- DROPDOWN OPTIONS -----
        if dropdown_open:
            for i, size in enumerate(puzzle_sizes):
                opt_rect = pygame.Rect(
                    dropdown_rect.x,
                    OPTIONS_TOP + i * OPTION_SPACING,
                    DROPDOWN_W,
                    DROPDOWN_H
                )

                draw_rounded_rect(screen, PANEL_COLOR, opt_rect)
                pygame.draw.rect(screen, GRID_LINE, opt_rect, 2, border_radius=10)

                opt_text = FONT.render(f"{size} × {size}", True, TEXT_COLOR)
                screen.blit(
                    opt_text,
                    (opt_rect.centerx - opt_text.get_width() // 2,
                     opt_rect.centery - opt_text.get_height() // 2)
                )

        # ----- START BUTTON -----
        start_rect = pygame.Rect(
            70,
            BUTTON_Y,
            BUTTON_W,
            BUTTON_H
        )

        hovered = start_rect.collidepoint(mx, my)
        draw_rounded_rect(screen, BUTTON_HOVER if hovered else BUTTON_COLOR, start_rect)
        pygame.draw.rect(screen, GRID_LINE, start_rect, 2, border_radius=10)

        start_text = FONT.render("Start Game", True, TEXT_COLOR)
        screen.blit(
            start_text,
            (start_rect.centerx - start_text.get_width() // 2,
             start_rect.centery - start_text.get_height() // 2)
        )

        pygame.display.update()

        # PUZZLE SIZE EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if CUSTOM_BUTTON.collidepoint(mx, my):
                    return "custom"

                if IMPORT_BUTTON.collidepoint(mx, my):
                    return "import"
    
                # Toggle dropdown
                if dropdown_rect.collidepoint(mx, my):
                    dropdown_open = not dropdown_open

                # Dropdown options
                if dropdown_open:
                    for i, size in enumerate(puzzle_sizes):
                        opt_rect = pygame.Rect(
                            dropdown_rect.x,
                            OPTIONS_TOP + i * OPTION_SPACING,
                            DROPDOWN_W,
                            DROPDOWN_H
                        )
                        if opt_rect.collidepoint(mx, my):
                            selected_size = size
                            dropdown_open = False

                # Start game
                if start_rect.collidepoint(mx, my):
                    return selected_size

        clock.tick(60)

        # Redundant homescreen events?????
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Toggle dropdown
                if dropdown_rect.collidepoint(mx, my):
                    dropdown_open = not dropdown_open

                # Dropdown options
                if dropdown_open:
                    for i, size in enumerate(puzzle_sizes):
                        opt_rect = pygame.Rect(
                            dropdown_rect.x,
                            dropdown_rect.bottom + 5 + i * (DROPDOWN_H + 5),
                            DROPDOWN_W,
                            DROPDOWN_H
                        )
                        if opt_rect.collidepoint(mx, my):
                            selected_size = size
                            dropdown_open = False

                # Start game
                if start_rect.collidepoint(mx, my):
                    return selected_size

        clock.tick(60)

# -----------------------------
# GAME SCREEN
# -----------------------------
def play_game(screen, GRID_SIZE, SOLUTION=None):
    font = pygame.font.SysFont("Segoe UI", CLUE_FONT_SIZE)

    if SOLUTION is None:
        SOLUTION = generate_random_grid(GRID_SIZE)
    row_clues, col_clues = generate_clues(SOLUTION)

    max_row_clue_width = max(font.size(" ".join(map(str, clues)))[0] for clues in row_clues)
    max_col_clue_height = max(len(clues) * CLUE_FONT_SIZE for clues in col_clues)

    LEFT_MARGIN = max_row_clue_width + 30
    TOP_MARGIN = max_col_clue_height + 30

    window_width = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + 250
    window_height = TOP_MARGIN + GRID_SIZE * CELL_SIZE + 30

    screen = pygame.display.set_mode((window_width, window_height))

    player_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    HINT_BUTTON = pygame.Rect(window_width-200, 20, 160, 50)

    hints_used = 0

    drag_mode = None  # None, "fill", or "x"

    def draw():
        screen.fill(BG_COLOR)
        # Draw hint button
        draw_rounded_rect(screen, BUTTON_COLOR, HINT_BUTTON)
        pygame.draw.rect(screen, GRID_LINE, HINT_BUTTON, 2, border_radius=10)

        hint_text = SMALL_FONT.render("Get Hint", True, TEXT_COLOR)
        screen.blit(
            hint_text,
            (HINT_BUTTON.centerx - hint_text.get_width() // 2,
            HINT_BUTTON.centery - hint_text.get_height() // 2)
        )

        # Draw hint counter
        counter_text = SMALL_FONT.render(f"Hints used: {hints_used}", True, TEXT_COLOR)
        screen.blit(counter_text, (window_width-200, 80))

        # Row clues
        for i, clues in enumerate(row_clues):
            text = " ".join(map(str, clues))
            img = font.render(text, True, TEXT_COLOR)
            y = TOP_MARGIN + i * CELL_SIZE + (CELL_SIZE - img.get_height()) // 2
            screen.blit(img, (LEFT_MARGIN - img.get_width() - 15, y))

        # Column clues
        for j, clues in enumerate(col_clues):
            y_offset = TOP_MARGIN - (len(clues) * CLUE_FONT_SIZE) - 10
            for c in clues:
                img = font.render(str(c), True, TEXT_COLOR)
                x = LEFT_MARGIN + j * CELL_SIZE + (CELL_SIZE - img.get_width()) // 2
                screen.blit(img, (x, y_offset))
                y_offset += CLUE_FONT_SIZE

        # Grid
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x = LEFT_MARGIN + j * CELL_SIZE
                y = TOP_MARGIN + i * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                if player_grid[i][j] == 1:
                    pygame.draw.rect(screen, FILLED_COLOR, rect, border_radius=4)
                elif player_grid[i][j] == 2:
                    pygame.draw.rect(screen, EMPTY_COLOR, rect, border_radius=4)
                    pygame.draw.line(screen, X_COLOR, (x+6, y+6), (x+CELL_SIZE-6, y+CELL_SIZE-6), 4)
                    pygame.draw.line(screen, X_COLOR, (x+CELL_SIZE-6, y+6), (x+6, y+CELL_SIZE-6), 4)
                else:
                    pygame.draw.rect(screen, EMPTY_COLOR, rect, border_radius=4)

                pygame.draw.rect(screen, GRID_LINE, rect, 2, border_radius=4)

        pygame.display.update()

    def check_win():
        normalized = [[1 if cell == 1 else 0 for cell in row] for row in player_grid]
        return normalized == SOLUTION


    # Game loop
    while True:
        draw()

        if check_win():
            screen = pygame.display.set_mode((640, 720))
            win_screen(screen)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Start drag
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Hint button clicked
                if HINT_BUTTON.collidepoint(mx, my):
                    # Find a cell that is wrong or empty
                    for r in range(GRID_SIZE):
                        for c in range(GRID_SIZE):
                            correct = SOLUTION[r][c]
                            current = 1 if player_grid[r][c] == 1 else 0
                            if current != correct:
                                # Apply correct value
                                player_grid[r][c] = 1 if correct == 1 else 2
                                hints_used += 1
                                break
                        else:
                            continue
                        break
                    continue  # Skip normal click handling
                if mx > LEFT_MARGIN and my > TOP_MARGIN:
                    col = (mx - LEFT_MARGIN) // CELL_SIZE
                    row = (my - TOP_MARGIN) // CELL_SIZE

                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                        if event.button == 1:  # left click
                            drag_mode = "fill"
                            player_grid[row][col] = 0 if player_grid[row][col] == 1 else 1

                        elif event.button == 3:  # right click
                            drag_mode = "x"
                            player_grid[row][col] = 0 if player_grid[row][col] == 2 else 2

            # Dragging
            if event.type == pygame.MOUSEMOTION and drag_mode:
                mx, my = pygame.mouse.get_pos()
                if mx > LEFT_MARGIN and my > TOP_MARGIN:
                    col = (mx - LEFT_MARGIN) // CELL_SIZE
                    row = (my - TOP_MARGIN) // CELL_SIZE

                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                        if drag_mode == "fill":
                            player_grid[row][col] = 1
                        elif drag_mode == "x":
                            player_grid[row][col] = 2

            # Stop drag
            if event.type == pygame.MOUSEBUTTONUP:
                drag_mode = None


def win_screen(screen):
    clock = pygame.time.Clock()
    SCREEN_W, SCREEN_H = screen.get_size()

    BUTTON_W, BUTTON_H = 260, 70
    button_rect = pygame.Rect(
        (SCREEN_W - BUTTON_W) // 2,
        SCREEN_H // 2 + 40,
        BUTTON_W,
        BUTTON_H
    )

    while True:
        screen.fill(BG_COLOR)

        # Title text
        win_text = TITLE_FONT.render("You solved it!!!!", True, TEXT_COLOR)
        win_x = (SCREEN_W - win_text.get_width()) // 2
        screen.blit(win_text, (win_x, SCREEN_H // 2 - 80))

        # Button
        mx, my = pygame.mouse.get_pos()
        hovered = button_rect.collidepoint(mx, my)

        draw_rounded_rect(screen, BUTTON_HOVER if hovered else BUTTON_COLOR, button_rect)
        pygame.draw.rect(screen, GRID_LINE, button_rect, 2, border_radius=10)

        btn_text = FONT.render("Return to Title", True, TEXT_COLOR)
        screen.blit(
            btn_text,
            (button_rect.centerx - btn_text.get_width() // 2,
             button_rect.centery - btn_text.get_height() // 2)
        )

        pygame.display.update()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(mx, my):
                    return  # go back to main loop

        clock.tick(60)
def custom_puzzle_screen(screen):
    solution_count = None

    # Make the window bigger for drawing
    screen = pygame.display.set_mode((900, 900))
    clock = pygame.time.Clock()

    # Default grid size
    GRID_SIZE = 10
    CELL = 40

    # Text input for grid size
    size_text = str(GRID_SIZE)
    input_active = False
    input_box = pygame.Rect(50, 40, 150, 55)


    EXPORT_BUTTON = pygame.Rect(250, 20, 180, 55)
    BACK_BUTTON = pygame.Rect(450, 20, 180, 55)
    CHECK_BUTTON = pygame.Rect(650, 20, 220, 55)


    # Create initial grid
    grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]

    # Dragging state
    drag_mode = None   # None, "fill", or "erase"

    while True:
        screen.fill(BG_COLOR)
        mx, my = pygame.mouse.get_pos()

        # --- BACKSOLVER BUTTON ---
        draw_rounded_rect(screen, BUTTON_COLOR, CHECK_BUTTON)
        screen.blit(FONT.render("Check Solutions", True, TEXT_COLOR),
            (CHECK_BUTTON.x + 15, CHECK_BUTTON.y + 12))

        # --- INPUT BOX ---
        draw_rounded_rect(screen, PANEL_COLOR, input_box)
        pygame.draw.rect(screen, GRID_LINE, input_box, 2, border_radius=10)

        label = SMALL_FONT.render("Grid Size (max 15):", True, TEXT_COLOR)
        screen.blit(label, (50, 0))

        txt_surface = FONT.render(size_text, True, TEXT_COLOR)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

        # --- BUTTONS ---
        draw_rounded_rect(screen, BUTTON_COLOR, EXPORT_BUTTON)
        screen.blit(FONT.render("Export", True, TEXT_COLOR),
                    (EXPORT_BUTTON.x+45, EXPORT_BUTTON.y+12))

        draw_rounded_rect(screen, BUTTON_COLOR, BACK_BUTTON)
        screen.blit(FONT.render("Back", True, TEXT_COLOR),
                    (BACK_BUTTON.x+60, BACK_BUTTON.y+12))

        # --- DRAW GRID ---
        grid_left = 50
        grid_top = 120

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = grid_left + c*CELL
                y = grid_top + r*CELL
                rect = pygame.Rect(x, y, CELL, CELL)

                pygame.draw.rect(screen, FILLED_COLOR if grid[r][c] else EMPTY_COLOR, rect)
                pygame.draw.rect(screen, GRID_LINE, rect, 2)
        # Show solver result
        if solution_count is not None:
            result_text = FONT.render(f"Solutions: {solution_count}", True, TEXT_COLOR)
            screen.blit(result_text, (grid_left + GRID_SIZE * CELL + 40, grid_top))

        pygame.display.update()

        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse down: start drag or click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Activate input box
                if input_box.collidepoint(mx, my):
                    input_active = True
                else:
                    input_active = False
                if CHECK_BUTTON.collidepoint(mx, my):
                # Convert grid to clues
                    row_clues, col_clues = generate_clues(grid)

                    # Run solver
                    solution_count = solve_all(row_clues, col_clues, limit=1000)


                # Export
                if EXPORT_BUTTON.collidepoint(mx, my):
                        # Convert grid to text
                            puzzle_text = "\n".join("".join(map(str, row)) for row in grid)

                            # Copy to clipboard
                            pyperclip.copy(puzzle_text)

                            # Redirect to confirmation screen
                            copied_screen(screen)
                            return None


                # Back → reset screen size
                if BACK_BUTTON.collidepoint(mx, my):
                    pygame.display.set_mode((640, 720))
                    return None

                # Start drag on grid
                for r in range(GRID_SIZE):
                    for c in range(GRID_SIZE):
                        x = grid_left + c*CELL
                        y = grid_top + r*CELL
                        if pygame.Rect(x, y, CELL, CELL).collidepoint(mx, my):
                            if event.button == 1:   # left click
                                drag_mode = "fill"
                                grid[r][c] = 1
                            elif event.button == 3: # right click
                                drag_mode = "erase"
                                grid[r][c] = 0

            # Mouse motion: continue drag
            if event.type == pygame.MOUSEMOTION and drag_mode:
                mx, my = pygame.mouse.get_pos()
                for r in range(GRID_SIZE):
                    for c in range(GRID_SIZE):
                        x = grid_left + c*CELL
                        y = grid_top + r*CELL
                        if pygame.Rect(x, y, CELL, CELL).collidepoint(mx, my):
                            if drag_mode == "fill":
                                grid[r][c] = 1
                            elif drag_mode == "erase":
                                grid[r][c] = 0

            # Mouse up: stop drag
            if event.type == pygame.MOUSEBUTTONUP:
                drag_mode = None

            # Typing into the size box
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    size_text = size_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # Validate input
                    if size_text.isdigit():
                        new_size = int(size_text)
                        if 1 <= new_size <= 15:
                            GRID_SIZE = new_size
                            grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
                        else:
                            size_text = str(GRID_SIZE)  # revert
                    else:
                        size_text = str(GRID_SIZE)
                else:
                    # Only allow digits
                    if event.unicode.isdigit():
                        size_text += event.unicode

        clock.tick(60)
def import_puzzle_screen(screen):
    text = ""
    error_message = ""
    input_box = pygame.Rect(50, 100, 540, 400)

    while True:
        screen.fill(BG_COLOR)

        # Title
        title = TITLE_FONT.render("Import Puzzle", True, TEXT_COLOR)
        screen.blit(title, (50, 30))

        # Input box
        pygame.draw.rect(screen, PANEL_COLOR, input_box)
        pygame.draw.rect(screen, GRID_LINE, input_box, 2)
        if error_message:
            err = SMALL_FONT.render(error_message, True, (200, 50, 50))
            screen.blit(err, (50, 580)) 
        # Render text
        y = 110
        for line in text.split("\n"):
            img = SMALL_FONT.render(line, True, TEXT_COLOR)
            screen.blit(img, (60, y))
            y += 24

        # Buttons
        IMPORT_BTN = pygame.Rect(50, 520, 200, 60)
        BACK_BTN = pygame.Rect(300, 520, 200, 60)
        
        draw_rounded_rect(screen, BUTTON_COLOR, IMPORT_BTN)
        screen.blit(FONT.render("Load", True, TEXT_COLOR),
                    (IMPORT_BTN.x+60, IMPORT_BTN.y+15))

        draw_rounded_rect(screen, BUTTON_COLOR, BACK_BTN)
        screen.blit(FONT.render("Back", True, TEXT_COLOR),
                    (BACK_BTN.x+60, BACK_BTN.y+15))
        
        pygame.display.update()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Ctrl+V paste support
                if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    pasted = pyperclip.paste()
                    # Filter pasted text to only 0, 1, and newlines
                    filtered = "".join(ch for ch in pasted if ch in "01\n")
                    text += filtered
                    continue

                    # Backspace
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                # Newline
                elif event.key == pygame.K_RETURN:
                    text += "\n"

                # Only allow typing 0 or 1
                elif event.unicode in ("0", "1"):
                    text += event.unicode



            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if IMPORT_BTN.collidepoint(mx, my):
                    # Convert text to grid
                    lines = [list(map(int, row.strip())) for row in text.split("\n") if row.strip()]

                    # Must have at least 1 row
                    if len(lines) == 0:
                        error_message = "Puzzle is empty"
                        continue

                    # All rows must be the same length
                    row_length = len(lines[0])
                    if any(len(row) != row_length for row in lines):
                        error_message = "All rows must have the same length"
                        continue

                    # Must be square
                    if len(lines) != row_length:
                        error_message = "Puzzle must be square (same rows and columns)"
                        continue

                    # Passed all checks
                    return lines


                if BACK_BTN.collidepoint(mx, my):
                    return None
def play_game_with_solution(screen, solution):
    if solution is None:
        return
    size = len(solution)
    play_game(screen, size, SOLUTION=solution)

def copied_screen(screen):
    screen = pygame.display.set_mode((640, 720))
    clock = pygame.time.Clock()

    BUTTON_W, BUTTON_H = 260, 70
    button_rect = pygame.Rect(
        (640 - BUTTON_W) // 2,
        400,
        BUTTON_W,
        BUTTON_H
    )

    while True:
        screen.fill(BG_COLOR)

        # Title text
        msg = TITLE_FONT.render("Puzzle copied to clipboard!", True, TEXT_COLOR)
        msg_x = (640 - msg.get_width()) // 2
        screen.blit(msg, (msg_x, 250))

        # Back button
        mx, my = pygame.mouse.get_pos()
        hovered = button_rect.collidepoint(mx, my)

        draw_rounded_rect(screen, BUTTON_HOVER if hovered else BUTTON_COLOR, button_rect)
        pygame.draw.rect(screen, GRID_LINE, button_rect, 2, border_radius=10)

        btn_text = FONT.render("Back", True, TEXT_COLOR)
        screen.blit(
            btn_text,
            (button_rect.centerx - btn_text.get_width() // 2,
             button_rect.centery - btn_text.get_height() // 2)
        )

        pygame.display.update()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(mx, my):
                    return  # go back to home screen

        clock.tick(60)
def solution_count_screen(screen, count):
    screen = pygame.display.set_mode((640, 720))
    clock = pygame.time.Clock()

    BUTTON_W, BUTTON_H = 260, 70
    button_rect = pygame.Rect(
        (640 - BUTTON_W) // 2,
        400,
        BUTTON_W,
        BUTTON_H
    )

    while True:
        screen.fill(BG_COLOR)

        # Title text
        msg = TITLE_FONT.render(f"Possible solutions: {count}", True, TEXT_COLOR)
        msg_x = (640 - msg.get_width()) // 2
        screen.blit(msg, (msg_x, 250))

        # Back button
        mx, my = pygame.mouse.get_pos()
        hovered = button_rect.collidepoint(mx, my)

        draw_rounded_rect(screen, BUTTON_HOVER if hovered else BUTTON_COLOR, button_rect)
        pygame.draw.rect(screen, GRID_LINE, button_rect, 2, border_radius=10)

        btn_text = FONT.render("Back", True, TEXT_COLOR)
        screen.blit(
            btn_text,
            (button_rect.centerx - btn_text.get_width() // 2,
             button_rect.centery - btn_text.get_height() // 2)
        )

        pygame.display.update()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(mx, my):
                    return  # return to custom puzzle creator

        clock.tick(60)

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    screen = pygame.display.set_mode((640, 720))
    pygame.display.set_caption("Picross")

    while True:
        choice = home_screen(screen)

        if choice == "custom":
            custom_grid = custom_puzzle_screen(screen)
            play_game_with_solution(screen, custom_grid)

        elif choice == "import":
            imported = import_puzzle_screen(screen)
            play_game_with_solution(screen, imported)

        else:
            play_game(screen, choice)


if __name__ == "__main__":
    main()