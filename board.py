import numpy as np

class Board:
    def __init__(self, rows, cols):
        """Initialize the game board
        
        Args:
            rows (int): Number of rows in the board
            cols (int): Number of columns in the board
        """
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
    
    def reset(self):
        """Reset the board to empty state"""
        self.board = np.zeros((self.rows, self.cols), dtype=int)
    
    def drop_piece(self, row, col, player):
        """Place a piece on the board
        
        Args:
            row (int): Row position
            col (int): Column position
            player (int): Player number (1 or 2)
        """
        self.board[row][col] = player
    
    def is_valid_move(self, col):
        """Check if a move is valid
        
        Args:
            col (int): Column to check
            
        Returns:
            bool: True if the column has an empty space, False otherwise
        """
        # Check if column is in range
        if col < 0 or col >= self.cols:
            return False
        
        # Check if the top row of the column is empty
        return self.board[0][col] == 0
    
    def get_next_open_row(self, col):
        """Find the next open row in the given column
        
        Args:
            col (int): Column to check
            
        Returns:
            int: Row index of the next open position
        """
        for r in range(self.rows-1, -1, -1):
            if self.board[r][col] == 0:
                return r
        return -1
    
    def is_full(self):
        """Check if the board is full
        
        Returns:
            bool: True if the board is full, False otherwise
        """
        return not any(self.board[0] == 0)
    
    def check_win(self, player):
        """Check if the given player has won
        
        Args:
            player (int): Player number to check for win
            
        Returns:
            bool: True if player has won, False otherwise
        """
        # Check horizontal
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if (self.board[r][c] == player and
                    self.board[r][c+1] == player and
                    self.board[r][c+2] == player and
                    self.board[r][c+3] == player):
                    return True
        
        # Check vertical
        for r in range(self.rows - 3):
            for c in range(self.cols):
                if (self.board[r][c] == player and
                    self.board[r+1][c] == player and
                    self.board[r+2][c] == player and
                    self.board[r+3][c] == player):
                    return True
        
        # Check diagonal (positive slope)
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if (self.board[r][c] == player and
                    self.board[r+1][c+1] == player and
                    self.board[r+2][c+2] == player and
                    self.board[r+3][c+3] == player):
                    return True
        
        # Check diagonal (negative slope)
        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                if (self.board[r][c] == player and
                    self.board[r-1][c+1] == player and
                    self.board[r-2][c+2] == player and
                    self.board[r-3][c+3] == player):
                    return True
        
        return False
    
    def get_valid_locations(self):
        """Get all valid column locations for the next move
        
        Returns:
            list: List of valid column indices
        """
        valid_locations = []
        for col in range(self.cols):
            if self.is_valid_move(col):
                valid_locations.append(col)
        return valid_locations
