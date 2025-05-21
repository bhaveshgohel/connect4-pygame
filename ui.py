import pygame
import numpy as np

class UI:
    def __init__(self, screen, width, height):
        """Initialize the UI
        
        Args:
            screen: Pygame display surface
            width (int): Screen width
            height (int): Screen height
        """
        self.screen = screen
        self.width = width
        self.height = height
        
        # Modern color palette
        self.DARK_BLUE = (41, 50, 65)       # Dark blue background
        self.LIGHT_BLUE = (84, 160, 255)    # Light blue for highlights
        self.NAVY_BLUE = (59, 89, 152)      # Navy blue for board
        self.BLACK = (0, 0, 0)
        self.RED = (231, 76, 60)            # Modern red
        self.YELLOW = (241, 196, 15)        # Modern yellow
        self.WHITE = (255, 255, 255)
        self.GRAY = (189, 195, 199)         # Light gray
        self.DARK_GRAY = (52, 73, 94)       # Dark gray for buttons
        self.GREEN = (46, 204, 113)         # Green for selected options
        
        # Board dimensions
        self.BOARD_ROWS = 6
        self.BOARD_COLS = 7
        self.SQUARE_SIZE = 80
        self.RADIUS = int(self.SQUARE_SIZE/2 - 5)
        
        # Board position
        self.board_width = self.BOARD_COLS * self.SQUARE_SIZE
        self.board_height = (self.BOARD_ROWS + 1) * self.SQUARE_SIZE
        self.board_x = (self.width - self.board_width) // 2
        self.board_y = (self.height - self.board_height) // 2
        
        # Fonts
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 30)
        self.large_font = pygame.font.SysFont('Arial', 50)
        self.small_font = pygame.font.SysFont('Arial', 20)
        
        # UI state
        self.selected_difficulty = 'medium'  # Default difficulty
    
    def draw_menu(self):
        """Draw the main menu
        
        Returns:
            str: The menu option that the mouse is hovering over
        """
        self.screen.fill(self.DARK_BLUE)
        
        # Title with shadow effect
        title_shadow = self.large_font.render('CONNECT 4', True, self.BLACK)
        title = self.large_font.render('CONNECT 4', True, self.LIGHT_BLUE)
        title_rect = title.get_rect(center=(self.width//2, 100))
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)
        
        # Menu options
        mouse_pos = pygame.mouse.get_pos()
        
        # PvP button
        pvp_rect = pygame.Rect(self.width//2 - 150, 200, 300, 60)
        pvp_color = self.LIGHT_BLUE if pvp_rect.collidepoint(mouse_pos) else self.DARK_GRAY
        pygame.draw.rect(self.screen, pvp_color, pvp_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.WHITE, pvp_rect, 2, border_radius=10)
        pvp_text = self.font.render('Player vs Player', True, self.WHITE)
        pvp_text_rect = pvp_text.get_rect(center=pvp_rect.center)
        self.screen.blit(pvp_text, pvp_text_rect)
        
        # AI button
        ai_rect = pygame.Rect(self.width//2 - 150, 280, 300, 60)
        ai_color = self.LIGHT_BLUE if ai_rect.collidepoint(mouse_pos) else self.DARK_GRAY
        pygame.draw.rect(self.screen, ai_color, ai_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.WHITE, ai_rect, 2, border_radius=10)
        ai_text = self.font.render('Player vs AI', True, self.WHITE)
        ai_text_rect = ai_text.get_rect(center=ai_rect.center)
        self.screen.blit(ai_text, ai_text_rect)
        
        # Settings button
        settings_rect = pygame.Rect(self.width//2 - 150, 360, 300, 60)
        settings_color = self.LIGHT_BLUE if settings_rect.collidepoint(mouse_pos) else self.DARK_GRAY
        pygame.draw.rect(self.screen, settings_color, settings_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.WHITE, settings_rect, 2, border_radius=10)
        settings_text = self.font.render('Settings', True, self.WHITE)
        settings_text_rect = settings_text.get_rect(center=settings_rect.center)
        self.screen.blit(settings_text, settings_text_rect)
        
        # Quit button
        quit_rect = pygame.Rect(self.width//2 - 150, 440, 300, 60)
        quit_color = self.LIGHT_BLUE if quit_rect.collidepoint(mouse_pos) else self.DARK_GRAY
        pygame.draw.rect(self.screen, quit_color, quit_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.WHITE, quit_rect, 2, border_radius=10)
        quit_text = self.font.render('Quit', True, self.WHITE)
        quit_text_rect = quit_text.get_rect(center=quit_rect.center)
        self.screen.blit(quit_text, quit_text_rect)
        
        # Version info
        version_text = self.small_font.render('v1.1.0', True, self.GRAY)
        self.screen.blit(version_text, (10, self.height - 30))
        
        pygame.display.update()
        
        # Return which button is being hovered
        if pvp_rect.collidepoint(mouse_pos):
            return "pvp"
        elif ai_rect.collidepoint(mouse_pos):
            return "ai"
        elif settings_rect.collidepoint(mouse_pos):
            return "settings"
        elif quit_rect.collidepoint(mouse_pos):
            return "quit"
        return None
    
    def draw_board(self, board, current_player):
        """Draw the game board
        
        Args:
            board: 2D numpy array representing the board state
            current_player: Current player (1 or 2)
        """
        self.screen.fill(self.DARK_BLUE)
        
        # Draw the board background with rounded corners
        board_surface = pygame.Surface((self.board_width, self.board_height - self.SQUARE_SIZE))
        board_surface.fill(self.NAVY_BLUE)
        self.screen.blit(board_surface, (self.board_x, self.board_y + self.SQUARE_SIZE))
        
        # Draw the pieces
        for r in range(self.BOARD_ROWS):
            for c in range(self.BOARD_COLS):
                # Calculate position
                x = self.board_x + c * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                y = self.board_y + (r + 1) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                
                # Draw the circle with shadow effect
                if board[r][c] == 0:
                    # Empty slot with shadow
                    pygame.draw.circle(self.screen, self.BLACK, (x+2, y+2), self.RADIUS)
                    pygame.draw.circle(self.screen, self.DARK_BLUE, (x, y), self.RADIUS)
                elif board[r][c] == 1:
                    # Red piece with shadow
                    pygame.draw.circle(self.screen, self.BLACK, (x+2, y+2), self.RADIUS)
                    pygame.draw.circle(self.screen, self.RED, (x, y), self.RADIUS)
                    # Add highlight
                    pygame.draw.circle(self.screen, (241, 148, 138), (x-10, y-10), self.RADIUS//4)
                else:
                    # Yellow piece with shadow
                    pygame.draw.circle(self.screen, self.BLACK, (x+2, y+2), self.RADIUS)
                    pygame.draw.circle(self.screen, self.YELLOW, (x, y), self.RADIUS)
                    # Add highlight
                    pygame.draw.circle(self.screen, (247, 220, 111), (x-10, y-10), self.RADIUS//4)
        
        # Draw the piece preview
        if pygame.mouse.get_pos()[1] < self.board_y + self.SQUARE_SIZE:
            col = self.get_column_from_mouse()
            if col is not None:
                x = self.board_x + col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                # Use the current player's color for the preview
                if current_player == 1:
                    preview_color = self.RED
                else:
                    preview_color = self.YELLOW
                pygame.draw.circle(self.screen, preview_color, (x, self.board_y + self.SQUARE_SIZE // 2), self.RADIUS)
        
        # Draw current player indicator
        player_text = "Player 1 (Red)" if current_player == 1 else "Player 2 (Yellow)"
        player_color = self.RED if current_player == 1 else self.YELLOW
        player_indicator = self.font.render(player_text, True, player_color)
        player_rect = player_indicator.get_rect(center=(self.width//2, 30))
        self.screen.blit(player_indicator, player_rect)
        
        # Draw back button at the bottom with fixed position
        back_rect = pygame.Rect(self.width//2 - 50, self.height - 60, 100, 40)
        mouse_pos = pygame.mouse.get_pos()
        back_color = self.LIGHT_BLUE if back_rect.collidepoint(mouse_pos) else self.DARK_GRAY
        pygame.draw.rect(self.screen, back_color, back_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.WHITE, back_rect, 2, border_radius=8)
        back_text = self.small_font.render('Menu', True, self.WHITE)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        self.back_rect = back_rect
    
    def get_column_from_mouse(self):
        """Get the column index from mouse position
        
        Returns:
            int: Column index or None if mouse is outside the board
        """
        mouse_x = pygame.mouse.get_pos()[0]
        
        # Check if mouse is within board boundaries
        if mouse_x < self.board_x or mouse_x > self.board_x + self.board_width:
            return None
        
        # Calculate column
        col = (mouse_x - self.board_x) // self.SQUARE_SIZE
        
        # Ensure column is valid
        if col >= 0 and col < self.BOARD_COLS:
            return col
        return None
    
    def draw_game_over(self, player1_win, player2_win, draw):
        """Draw the game over screen
        
        Args:
            player1_win (bool): True if player 1 won
            player2_win (bool): True if player 2 won
            draw (bool): True if the game ended in a draw
        """
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Game over panel
        panel_width, panel_height = 400, 300
        panel_x = (self.width - panel_width) // 2
        panel_y = (self.height - panel_height) // 2
        
        # Draw panel background with rounded corners
        pygame.draw.rect(overlay, self.DARK_GRAY, 
                         (panel_x, panel_y, panel_width, panel_height), 
                         border_radius=15)
        pygame.draw.rect(overlay, self.WHITE, 
                         (panel_x, panel_y, panel_width, panel_height), 
                         2, border_radius=15)
        
        # Game over message
        if player1_win:
            message = "Red Player Wins!"
            color = self.RED
        elif player2_win:
            message = "Yellow Player Wins!"
            color = self.YELLOW
        else:
            message = "It's a Draw!"
            color = self.WHITE
        
        text = self.large_font.render(message, True, color)
        text_rect = text.get_rect(center=(self.width//2, panel_y + 60))
        self.screen.blit(text, text_rect)
        
        # Play again button
        play_again_rect = pygame.Rect(self.width//2 - 120, panel_y + 120, 240, 50)
        mouse_pos = pygame.mouse.get_pos()
        play_again_color = self.LIGHT_BLUE if play_again_rect.collidepoint(mouse_pos) else self.DARK_GRAY
        pygame.draw.rect(self.screen, play_again_color, play_again_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.WHITE, play_again_rect, 2, border_radius=10)
        play_again_text = self.font.render('Play Again', True, self.WHITE)
        play_again_text_rect = play_again_text.get_rect(center=play_again_rect.center)
        self.screen.blit(play_again_text, play_again_text_rect)
        
        # Main menu button
        menu_rect = pygame.Rect(self.width//2 - 120, panel_y + 190, 240, 50)
        menu_color = self.LIGHT_BLUE if menu_rect.collidepoint(mouse_pos) else self.DARK_GRAY
        pygame.draw.rect(self.screen, menu_color, menu_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.WHITE, menu_rect, 2, border_radius=10)
        menu_text = self.font.render('Main Menu', True, self.WHITE)
        menu_text_rect = menu_text.get_rect(center=menu_rect.center)
        self.screen.blit(menu_text, menu_text_rect)
        
        self.play_again_rect = play_again_rect
        self.menu_rect = menu_rect
    
    def is_play_again_clicked(self):
        """Check if the play again button is clicked
        
        Returns:
            bool: True if the play again button is clicked
        """
        if hasattr(self, 'play_again_rect'):
            return self.play_again_rect.collidepoint(pygame.mouse.get_pos())
        return False
    
    def is_menu_clicked(self):
        """Check if the menu button is clicked
        
        Returns:
            bool: True if the menu button is clicked
        """
        if hasattr(self, 'menu_rect'):
            return self.menu_rect.collidepoint(pygame.mouse.get_pos())
        return False
    def draw_settings(self):
        """Draw the settings menu
        
        Returns:
            tuple: (action, value) where action is the selected action and value is the selected option
        """
        self.screen.fill(self.DARK_BLUE)
        
        # Title
        title = self.large_font.render('SETTINGS', True, self.LIGHT_BLUE)
        title_rect = title.get_rect(center=(self.width//2, 100))
        self.screen.blit(title, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Difficulty selection
        difficulty_label = self.font.render('AI Difficulty:', True, self.WHITE)
        self.screen.blit(difficulty_label, (self.width//2 - 250, 200))
        
        # Easy button
        easy_rect = pygame.Rect(self.width//2 - 250, 250, 150, 50)
        easy_color = self.GREEN if self.selected_difficulty == 'easy' else self.DARK_GRAY
        if easy_rect.collidepoint(mouse_pos):
            easy_color = self.LIGHT_BLUE
        pygame.draw.rect(self.screen, easy_color, easy_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.WHITE, easy_rect, 2, border_radius=8)
        easy_text = self.font.render('Easy', True, self.WHITE)
        easy_text_rect = easy_text.get_rect(center=easy_rect.center)
        self.screen.blit(easy_text, easy_text_rect)
        
        # Medium button
        medium_rect = pygame.Rect(self.width//2 - 75, 250, 150, 50)
        medium_color = self.GREEN if self.selected_difficulty == 'medium' else self.DARK_GRAY
        if medium_rect.collidepoint(mouse_pos):
            medium_color = self.LIGHT_BLUE
        pygame.draw.rect(self.screen, medium_color, medium_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.WHITE, medium_rect, 2, border_radius=8)
        medium_text = self.font.render('Medium', True, self.WHITE)
        medium_text_rect = medium_text.get_rect(center=medium_rect.center)
        self.screen.blit(medium_text, medium_text_rect)
        
        # Hard button
        hard_rect = pygame.Rect(self.width//2 + 100, 250, 150, 50)
        hard_color = self.GREEN if self.selected_difficulty == 'hard' else self.DARK_GRAY
        if hard_rect.collidepoint(mouse_pos):
            hard_color = self.LIGHT_BLUE
        pygame.draw.rect(self.screen, hard_color, hard_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.WHITE, hard_rect, 2, border_radius=8)
        hard_text = self.font.render('Hard', True, self.WHITE)
        hard_text_rect = hard_text.get_rect(center=hard_rect.center)
        self.screen.blit(hard_text, hard_text_rect)
        
        # Back button
        back_rect = pygame.Rect(self.width//2 - 150, 400, 300, 60)
        back_color = self.LIGHT_BLUE if back_rect.collidepoint(mouse_pos) else self.DARK_GRAY
        pygame.draw.rect(self.screen, back_color, back_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.WHITE, back_rect, 2, border_radius=10)
        back_text = self.font.render('Back to Menu', True, self.WHITE)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        pygame.display.update()
        
        # Store the button rectangles for click detection
        self.settings_back_rect = back_rect
        self.easy_rect = easy_rect
        self.medium_rect = medium_rect
        self.hard_rect = hard_rect
        
        # This return is no longer used for button detection
        # but kept for compatibility
        return (None, None)
    def is_back_button_clicked(self):
        """Check if the back button is clicked
        
        Returns:
            bool: True if the back button is clicked
        """
        if hasattr(self, 'back_rect'):
            return self.back_rect.collidepoint(pygame.mouse.get_pos())
        return False
        
    def set_difficulty(self, difficulty):
        """Set the AI difficulty
        
        Args:
            difficulty (str): Difficulty level ('easy', 'medium', 'hard')
        """
        self.selected_difficulty = difficulty
        
    def get_difficulty(self):
        """Get the current AI difficulty
        
        Returns:
            str: Current difficulty level
        """
        return self.selected_difficulty
    def is_settings_back_clicked(self):
        """Check if the back button in settings is clicked
        
        Returns:
            bool: True if the settings back button is clicked
        """
        if hasattr(self, 'settings_back_rect'):
            return self.settings_back_rect.collidepoint(pygame.mouse.get_pos())
        return False
    def is_easy_button_clicked(self, mouse_pos):
        """Check if the easy button is clicked
        
        Args:
            mouse_pos: Current mouse position
            
        Returns:
            bool: True if the easy button is clicked
        """
        if hasattr(self, 'easy_rect'):
            return self.easy_rect.collidepoint(mouse_pos)
        return False
    
    def is_medium_button_clicked(self, mouse_pos):
        """Check if the medium button is clicked
        
        Args:
            mouse_pos: Current mouse position
            
        Returns:
            bool: True if the medium button is clicked
        """
        if hasattr(self, 'medium_rect'):
            return self.medium_rect.collidepoint(mouse_pos)
        return False
    
    def is_hard_button_clicked(self, mouse_pos):
        """Check if the hard button is clicked
        
        Args:
            mouse_pos: Current mouse position
            
        Returns:
            bool: True if the hard button is clicked
        """
        if hasattr(self, 'hard_rect'):
            return self.hard_rect.collidepoint(mouse_pos)
        return False
