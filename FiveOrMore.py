import pygame
import random
from collections import deque

# Constants
GRID_WIDTH = 9
GRID_HEIGHT = 9
CELL_SIZE = 50  # Size of each grid cell
BALL_COLORS = ['R', 'G', 'B', 'Y', 'M', 'T', 'O']  # Ball colors
MIN_BALLS_TO_REMOVE = 4

# Additional scoring based on the number of aligned balls
SCORE_MAP = {
    5: 10,
    6: 12,
    7: 18,
    8: 28,
    9: 42
}

# Initialize Pygame
pygame.init()
screen_width = GRID_WIDTH * CELL_SIZE
screen_height = GRID_HEIGHT * CELL_SIZE + CELL_SIZE  # Increase height to accommodate score bar
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Game board represented as a 2D list
board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
score = 0


def initialize_board():
    # Start with three random balls on the board
    for _ in range(3):
        x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
        board[y][x] = random.choice(BALL_COLORS)


def draw_board():
    screen.fill((255, 255, 255))  # Clear screen with white color

    # Draw gray horizontal bar at the bottom (score bar)
    pygame.draw.rect(screen, (200, 200, 200), (0, screen_height - CELL_SIZE, screen_width, CELL_SIZE))

    # Display current score on the gray bar at the bottom
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height - CELL_SIZE // 2))
    screen.blit(score_text, score_rect)

    # Draw grid lines for the entire playable area (excluding the score bar)
    for x in range(GRID_WIDTH):
        pygame.draw.line(screen, (0, 0, 0), (x * CELL_SIZE, 0), (x * CELL_SIZE, screen_height - CELL_SIZE))
    for y in range(GRID_HEIGHT):
        pygame.draw.line(screen, (0, 0, 0), (0, y * CELL_SIZE), (screen_width, y * CELL_SIZE))

    # Color mapping for ball colors
    color_map = {
        'R': (255, 0, 0),    # Red
        'G': (0, 255, 0),    # Green
        'B': (0, 0, 255),    # Blue
        'Y': (255, 255, 0),  # Yellow
        'M': (255, 0, 255),  # Magenta
        'T': (64, 224, 208), # Turquoise
        'O': (255, 165, 0)   # Orange
    }

    # Draw balls on the game board within the playable area
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if board[y][x] is not None:
                color = color_map[board[y][x]]
                # Draw grey perimeter (outline) around the ball
                pygame.draw.circle(screen, (150, 150, 150),
                                   (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 17)
                # Draw colored ball inside the perimeter
                pygame.draw.circle(screen, color,
                                   (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 15)

    pygame.display.flip()


def is_valid_move(x1, y1, x2, y2):
    # Check if the destination cell is within bounds and empty
    if not (0 <= x2 < GRID_WIDTH and 0 <= y2 < GRID_HEIGHT) or board[y2][x2] is not None:
        return False

    # Directions for movement (right, left, down, up)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # BFS to check for a valid path from (x1, y1) to (x2, y2)
    queue = deque([(x1, y1)])
    visited = set([(x1, y1)])

    while queue:
        x, y = queue.popleft()

        # Check if we've reached the destination (x2, y2)
        if (x, y) == (x2, y2):
            return True

        # Explore neighboring cells
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the neighbor is within bounds, not visited, and the cell is empty
            if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in visited
                    and board[ny][nx] is None):
                visited.add((nx, ny))
                queue.append((nx, ny))

    # If no valid path is found
    return False


def perform_move(start_x, start_y, end_x, end_y):
    # Move the selected ball to the target position
    board[end_y][end_x] = board[start_y][start_x]
    board[start_y][start_x] = None


def check_matches():
    global score
    matched_positions = set()

    def dfs(y, x, color, visited, dy, dx):
        """ Perform DFS to count consecutive balls of the same color in a specific direction """
        if (y, x) in visited or not (0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH):
            return 0
        if board[y][x] != color:
            return 0

        visited.add((y, x))
        return 1 + dfs(y + dy, x + dx, color, visited, dy, dx)

    def is_valid_match(length):
        """ Check if the matched sequence length is 5 or more """
        return length >= MIN_BALLS_TO_REMOVE

    # Define all possible directions: vertical, horizontal, and both diagonals
    directions = [
        (0, 1),   # Right (horizontal)
        (1, 0),   # Down (vertical)
        (1, 1),   # Down-Right (diagonal)
        (1, -1)   # Down-Left (diagonal)
    ]

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if board[y][x] is not None:
                color = board[y][x]
                for dy, dx in directions:
                    visited = set()
                    length = dfs(y, x, color, visited, dy, dx) + dfs(y, x, color, visited, -dy, -dx) - 1
                    if is_valid_match(length):
                        for pos in visited:
                            matched_positions.add(pos)

    # Remove matched balls and update score
    if matched_positions:
        num_matched = len(matched_positions)
        additional_score = SCORE_MAP.get(num_matched, 0)
        score += additional_score  # Add the additional score based on the number of aligned balls
        for y, x in matched_positions:
            board[y][x] = None

    return len(matched_positions) >= MIN_BALLS_TO_REMOVE  # Return True if matches were found


def fill_empty_spots():
    # Fill empty spots on the board with new balls (up to three new balls per empty spot)
    empty_spots = [(y, x) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH) if board[y][x] is None]
    for _ in range(min(3, len(empty_spots))):  # Add up to 3 new balls
        if empty_spots:
            y, x = random.choice(empty_spots)
            board[y][x] = random.choice(BALL_COLORS)


def is_game_over():
    # Check if there are no valid moves left
    for y1 in range(GRID_HEIGHT):
        for x1 in range(GRID_WIDTH):
            if board[y1][x1] is not None:
                for y2 in range(GRID_HEIGHT):
                    for x2 in range(GRID_WIDTH):
                        if is_valid_move(x1, y1, x2, y2):
                            return False
    return True


initialize_board()
running = True
selected_ball = None  # Coordinates of the selected ball
target_position = None  # Coordinates of the target position for the move

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button down
            x, y = event.pos
            grid_x = x // CELL_SIZE
            grid_y = y // CELL_SIZE

            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                if selected_ball is None:
                    # Select the ball at the clicked position
                    if board[grid_y][grid_x] is not None:
                        selected_ball = (grid_x, grid_y)
                        #print(f"Ball selected at ({grid_x}, {grid_y})")
                else:
                    # Set the target position for the move
                    target_position = (grid_x, grid_y)
                    #print(f"Move ball to ({grid_x}, {grid_y})")

                    # Attempt to perform the move
                    start_x, start_y = selected_ball
                    end_x, end_y = target_position

                    # Check if the move is valid
                    if is_valid_move(start_x, start_y, end_x, end_y):
                        # Move the ball to the target position
                        perform_move(start_x, start_y, end_x, end_y)

                        # Check for matches and remove balls
                        if not check_matches():
                            # Fill empty spots with new balls after the move
                            fill_empty_spots()
                    else:
                        print("Path not free. Try another move.")

                    # Reset selected ball and target position
                    selected_ball = None
                    target_position = None

    draw_board()

    # Check if the game is over
    if is_game_over():
        print("Game Over! Score = ", score)
        running = False

    clock.tick(30)  # Limit frame rate to 30 FPS

pygame.quit()
