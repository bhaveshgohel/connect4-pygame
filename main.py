import pygame
import sys
import time
from board import Board
from ui import UI
from ai import AI

class Connect4Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Connect 4")
        
        # Game constants - increased height to accommodate menu button
        self.WIDTH = 700
        self.HEIGHT = 700  # Increased from 600 to 700
        self.BOARD_ROWS = 6
        self.BOARD_COLS = 7
        
        # Game state
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.board = Board(self.BOARD_ROWS, self.BOARD_COLS)
        self.ui = UI(self.screen, self.WIDTH, self.HEIGHT)
        self.ai = AI(self.board)
        
        # Game settings
        self.game_mode = None  # 'pvp' or 'ai'
        self.ai_difficulty = 'easy'  # 'easy', 'medium', 'hard'
        self.current_player = 1  # Player 1 starts (1 or 2)
        self.game_over = False
        self.in_menu = True
        self.in_settings = False
        
        # Animation variables
        self.animation_active = False
        self.animation_col = None
        self.animation_row = None
        self.animation_player = None
        self.animation_y = 0
        self.animation_speed = 15
        
        # Game clock
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
    def run(self):
        """Main game loop"""
        while True:
            self.clock.tick(self.FPS)
            
            if self.in_menu:
                self.show_menu()
            elif self.in_settings:
                self.show_settings()
            else:
                self.play_game()
    
    def show_menu(self):
        """Display the game menu"""
        menu_choice = self.ui.draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Ignore mouse wheel events
            if event.type == pygame.MOUSEWHEEL:
                continue
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button only
                if menu_choice == "pvp":
                    self.game_mode = "pvp"
                    self.in_menu = False
                    self.reset_game()
                elif menu_choice == "ai":
                    self.game_mode = "ai"
                    self.in_menu = False
                    self.reset_game()
                elif menu_choice == "settings":
                    self.in_menu = False
                    self.in_settings = True
                elif menu_choice == "quit":
                    pygame.quit()
                    sys.exit()
    
    def show_settings(self):
        """Display the settings menu"""
        action, value = self.ui.draw_settings()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Ignore mouse wheel events
            if event.type == pygame.MOUSEWHEEL:
                continue
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Only process left mouse button clicks (button 1)
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check for difficulty button clicks
                    if self.ui.is_easy_button_clicked(mouse_pos):
                        self.ai_difficulty = 'easy'
                        self.ui.set_difficulty('easy')
                    elif self.ui.is_medium_button_clicked(mouse_pos):
                        self.ai_difficulty = 'medium'
                        self.ui.set_difficulty('medium')
                    elif self.ui.is_hard_button_clicked(mouse_pos):
                        self.ai_difficulty = 'hard'
                        self.ui.set_difficulty('hard')
                    elif self.ui.is_settings_back_clicked():
                        self.in_settings = False
                        self.in_menu = True
    
    def play_game(self):
        """Main gameplay function"""
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Ignore mouse wheel events
            if event.type == pygame.MOUSEWHEEL:
                continue
            
            if not self.game_over and not self.animation_active:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button only
                    # Check if back button is clicked
                    if self.ui.is_back_button_clicked():
                        self.in_menu = True
                        return
                    
                    # Player's turn
                    if self.game_mode == "pvp" or (self.game_mode == "ai" and self.current_player == 1):
                        col = self.ui.get_column_from_mouse()
                        if col is not None and self.board.is_valid_move(col):
                            row = self.board.get_next_open_row(col)
                            self.start_animation(row, col, self.current_player)
            else:
                # Game over state
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button only
                    if self.ui.is_play_again_clicked():
                        self.reset_game()
                    elif self.ui.is_menu_clicked():
                        self.in_menu = True
        
        # Process animation
        if self.animation_active:
            self.process_animation()
        
        # AI's turn
        if not self.game_over and not self.animation_active and self.game_mode == "ai" and self.current_player == 2:
            col = self.ai.get_best_move(self.ai_difficulty)
            if col is not None:
                row = self.board.get_next_open_row(col)
                self.start_animation(row, col, self.current_player)
        
        # Draw the game
        self.ui.draw_board(self.board.board, self.current_player)
        
        # Draw animation
        if self.animation_active:
            self.draw_animation()
        
        if self.game_over:
            self.ui.draw_game_over(self.board.check_win(1), self.board.check_win(2), self.board.is_full())
        
        pygame.display.update()
    
    def start_animation(self, row, col, player):
        """Start the piece dropping animation
        
        Args:
            row (int): Target row
            col (int): Column
            player (int): Current player
        """
        self.animation_active = True
        self.animation_col = col
        self.animation_row = row
        self.animation_player = player
        self.animation_y = 0
    
    def process_animation(self):
        """Process the animation state"""
        target_y = (self.animation_row + 1) * self.ui.SQUARE_SIZE + self.ui.board_y
        
        if self.animation_y < target_y:
            self.animation_y += self.animation_speed
        else:
            # Animation complete
            self.board.drop_piece(self.animation_row, self.animation_col, self.animation_player)
            self.animation_active = False
            
            # Check game state
            if self.board.check_win(self.animation_player):
                self.game_over = True
            elif self.board.is_full():
                self.game_over = True
            else:
                self.current_player = 3 - self.current_player  # Switch player (1->2, 2->1)
    
    def draw_animation(self):
        """Draw the animation frame"""
        x = self.ui.board_x + self.animation_col * self.ui.SQUARE_SIZE + self.ui.SQUARE_SIZE // 2
        
        if self.animation_player == 1:
            # Red piece with shadow
            pygame.draw.circle(self.screen, self.ui.BLACK, (x+2, self.animation_y+2), self.ui.RADIUS)
            pygame.draw.circle(self.screen, self.ui.RED, (x, self.animation_y), self.ui.RADIUS)
            # Add highlight
            pygame.draw.circle(self.screen, (241, 148, 138), (x-10, self.animation_y-10), self.ui.RADIUS//4)
        else:
            # Yellow piece with shadow
            pygame.draw.circle(self.screen, self.ui.BLACK, (x+2, self.animation_y+2), self.ui.RADIUS)
            pygame.draw.circle(self.screen, self.ui.YELLOW, (x, self.animation_y), self.ui.RADIUS)
            # Add highlight
            pygame.draw.circle(self.screen, (247, 220, 111), (x-10, self.animation_y-10), self.ui.RADIUS//4)
    
    def reset_game(self):
        """Reset the game state"""
        self.board.reset()
        self.current_player = 1
        self.game_over = False
        self.animation_active = False

if __name__ == "__main__":
    game = Connect4Game()
    game.run()
