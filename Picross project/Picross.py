import pygame
import sys
import random

pygame.init()

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
# AWESOME UNIQUE SOLUTION CHECK
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

    while True:
        screen.fill(BG_COLOR)

        # ----- TITLE -----
        title_text = TITLE_FONT.render("Jackson's awesome Picross", True, TEXT_COLOR)
        title_x = (SCREEN_W - title_text.get_width()) // 2
        screen.blit(title_text, (title_x, TITLE_Y))

        # ----- DROPDOWN -----
        dropdown_rect = pygame.Rect(
            (SCREEN_W - DROPDOWN_W) // 2,
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
            (SCREEN_W - BUTTON_W) // 2,
            BUTTON_Y,
            BUTTON_W,
            BUTTON_H
        )

        mx, my = pygame.mouse.get_pos()
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
def play_game(screen, GRID_SIZE):
    font = pygame.font.SysFont("Segoe UI", CLUE_FONT_SIZE)

    while True:
        SOLUTION = generate_random_grid(GRID_SIZE)
        row_clues, col_clues = generate_clues(SOLUTION)
        num_solutions = solve_all(row_clues, col_clues, limit=2)
        if num_solutions == 1:
            break   

    max_row_clue_width = max(font.size(" ".join(map(str, clues)))[0] for clues in row_clues)
    max_col_clue_height = max(len(clues) * CLUE_FONT_SIZE for clues in col_clues)

    LEFT_MARGIN = max_row_clue_width + 30
    TOP_MARGIN = max_col_clue_height + 30

    window_width = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + 40
    window_height = TOP_MARGIN + GRID_SIZE * CELL_SIZE + 40

    screen = pygame.display.set_mode((window_width, window_height))

    player_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def draw():
        screen.fill(BG_COLOR)

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
    #Checks if you won the game
    def check_win():
        normalized = [[1 if cell == 1 else 0 for cell in row] for row in player_grid]
        return normalized == SOLUTION

    # Game loop
    while True:
        draw()

        if check_win():
            print("You solved it!")
            pygame.time.wait(1500)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if mx > LEFT_MARGIN and my > TOP_MARGIN:
                    col = (mx - LEFT_MARGIN) // CELL_SIZE
                    row = (my - TOP_MARGIN) // CELL_SIZE

                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                        if event.button == 1:
                            player_grid[row][col] = 1 if player_grid[row][col] != 1 else 0
                        elif event.button == 3:
                            player_grid[row][col] = 2 if player_grid[row][col] != 2 else 0

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    screen = pygame.display.set_mode((640, 720))
    pygame.display.set_caption("Picross")

    while True:
        size = home_screen(screen)
        play_game(screen, size)

if __name__ == "__main__":
    main()