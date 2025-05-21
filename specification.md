# Connect 4 Game with Pygame - Specification

## Overview
This project creates a modern Connect 4 game using Python and Pygame. The game features a sleek user interface, multiple game modes, and AI opponents with varying difficulty levels. This project was developed with assistance from Amazon Q CLI.

## Features
- A graphical user interface with a modern Connect 4 board design
- Options to play against another person or an AI opponent
- Three AI difficulty levels (easy, medium, hard)
- Visual and animation effects for game events
- Current player indicator
- Settings menu for game customization
- Score tracking and game state management

## Components and Implementation

### 1. Project Setup
- Project directory structure with organized files
- Required dependencies (Pygame, NumPy)
- Main game file with initialization and game loop

### 2. Game Board Implementation
- Board class representing the game state
- Game logic for placing pieces
- Win condition checking (horizontal, vertical, diagonal)
- Draw condition checking

### 3. Modern User Interface
- Sleek design with modern color palette
- Smooth animations for dropping pieces
- Visual feedback for current player and game events
- Rounded corners and shadow effects for visual appeal
- Click detection for column selection
- Current player indicator at the top of the screen

### 4. Navigation System
- Main menu with multiple options
- Settings menu for game configuration
- In-game menu button for returning to main menu
- Game over screen with play again option

### 5. Player vs Player Mode
- Turn-based gameplay
- Visual indicators for current player
- Win/draw detection and game reset

### 6. AI Opponent Implementation
- Easy mode: Random move selection
- Medium mode: Basic strategy (blocks opponent wins, takes winning moves)
- Hard mode: Minimax algorithm with alpha-beta pruning
- Difficulty selection in settings menu

### 7. Animation System
- Smooth piece dropping animations
- Visual effects for game events
- Consistent frame rate control

### 8. Input Handling
- Mouse click detection for user interaction
- Filtering of mouse wheel events
- Button hover effects for better user experience

## File Structure
```
connect4-pygame/
├── main.py           # Main game entry point and game loop
├── board.py          # Game board logic and win detection
├── ui.py             # User interface components and rendering
├── ai.py             # AI opponent implementation with difficulty levels
├── assets/           # Directory for images and sounds
│   ├── images/       # Game graphics
│   └── sounds/       # Sound effects
├── requirements.txt  # Required Python packages
├── specification.md  # This specification file
└── README.md         # Project documentation
```

## Technologies
- Python 3.x
- Pygame library for graphics and game loop
- NumPy for board representation and calculations
- Amazon Q CLI for development assistance

## Game Window Specifications
- Width: 700 pixels
- Height: 700 pixels
- Board: 7 columns × 6 rows
- Responsive layout with proper spacing

## Color Scheme
- Dark blue background
- Navy blue board
- Red pieces for Player 1
- Yellow pieces for Player 2
- Light blue for button highlights
- White text and borders
- Green for selected options

## Future Enhancements
- Sound effects for game events
- Online multiplayer functionality
- Customizable board sizes and themes
- Player statistics and high scores
- Replay functionality
- Additional AI algorithms
