# Connect 4 Game with Pygame

A modern implementation of the classic Connect 4 game built with Python and Pygame. This project was developed using Amazon Q CLI and features a sleek interface, multiple game modes, and AI opponents with varying difficulty levels.

## Features

- Modern, visually appealing user interface with animations
- Two game modes:
  - Player vs Player: Challenge a friend on the same computer
  - Player vs AI: Test your skills against the computer
- Three AI difficulty levels:
  - Easy: Makes random moves for beginners
  - Medium: Uses basic strategy (blocks wins and takes winning moves)
  - Hard: Employs minimax algorithm with alpha-beta pruning for challenging gameplay
- Smooth animations for piece dropping
- Visual feedback for current player and game events
- Win detection for horizontal, vertical, and diagonal connections
- Settings menu for game customization
- Responsive navigation system

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

1. Make sure you have Python installed on your system
2. Install the required packages:

```bash
pip install pygame numpy
```

3. Clone or download this repository

## How to Play

1. Run the game:

```bash
python main.py
```

2. From the main menu, select:
   - "Player vs Player" to play against another person
   - "Player vs AI" to play against the computer
   - "Settings" to adjust game options
   - "Quit" to exit the game

3. In the Settings menu:
   - Select AI difficulty (Easy, Medium, or Hard)
   - Return to the main menu with the "Back to Menu" button

4. During gameplay:
   - Click on a column to drop your piece
   - The current player is displayed at the top of the screen
   - The game will automatically switch turns
   - Use the Menu button at the bottom to return to the main menu
   - When the game ends, you can choose to play again or return to the main menu

## Game Rules

- Players take turns dropping colored discs into the board
- Player 1 uses red pieces, Player 2 (or AI) uses yellow pieces
- The pieces fall to the lowest available position in the selected column
- The first player to connect four of their discs horizontally, vertically, or diagonally wins
- If the board fills up without a winner, the game ends in a draw

## Project Structure

- `main.py`: Main game entry point and game loop
- `board.py`: Game board logic and win detection
- `ui.py`: User interface components and rendering
- `ai.py`: AI opponent implementation with multiple difficulty levels
- `specification.md`: Detailed project specification
- `requirements.txt`: Required Python packages

## Development

This project was built using Amazon Q CLI, which provided assistance with:
- Code generation and implementation
- UI design and improvements
- Bug fixing and troubleshooting
- Feature implementation

## License

This project is open source and available under the MIT License.
