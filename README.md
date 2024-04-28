# Ball Matching Game

This project is a simple ball matching game implemented using Python and Pygame. The game board consists of a grid where colored balls can be moved to create matches and earn points.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame library (`pip install pygame`)

### Running the Game

1. Clone this repository or download the `ball_matching_game.py` file.
2. Install the required dependencies using `pip`.
3. Run the game script by executing `python ball_matching_game.py` in your terminal.

### Game Rules

- Balls of the same color can be moved horizontally or vertically to align them.
- Aligning at least four balls of the same color in a row or column will remove them from the board and earn points.
- The game ends when no valid moves are left.

## Gameplay Controls

- Use the mouse to select and move balls:
  - Click on a ball to select it.
  - Click on another empty cell to move the selected ball to that position.
  - Valid moves are restricted to empty cells and require a clear path between the start and end positions.

## Game Components

- **Grid**: Represents the playable area where balls can be moved.
- **Balls**: Colored spheres that can be aligned to score points.
- **Score Bar**: Displays the current score at the bottom of the screen.

## Customization

You can customize the game by adjusting the following parameters in the script:

- `GRID_WIDTH` and `GRID_HEIGHT`: Adjust the size of the game board.
- `CELL_SIZE`: Modify the size of each grid cell.
- `BALL_COLORS`: Change the available colors for the balls.

## Acknowledgments

This project is inspired by classic tile-matching puzzle games and serves as a fun exercise in game development with Pygame.



