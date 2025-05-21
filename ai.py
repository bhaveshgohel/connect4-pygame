import numpy as np
import random
import math

class AI:
    def __init__(self, board):
        """Initialize the AI
        
        Args:
            board: Board object representing the game state
        """
        self.board = board
        self.PLAYER = 2  # AI is player 2
        self.OPPONENT = 1  # Human is player 1
    
    def get_best_move(self, difficulty):
        """Get the best move for the AI based on difficulty
        
        Args:
            difficulty (str): Difficulty level ('easy', 'medium', 'hard')
            
        Returns:
            int: Column index for the best move
        """
        valid_locations = self.board.get_valid_locations()
        
        if not valid_locations:
            return None
        
        if difficulty == 'easy':
            return self._get_easy_move(valid_locations)
        elif difficulty == 'medium':
            return self._get_medium_move(valid_locations)
        else:  # hard
            return self._get_hard_move(valid_locations)
    
    def _get_easy_move(self, valid_locations):
        """Get a random move
        
        Args:
            valid_locations (list): List of valid column indices
            
        Returns:
            int: Column index for the move
        """
        return random.choice(valid_locations)
    
    def _get_medium_move(self, valid_locations):
        """Get a move that blocks opponent's win or makes a win if possible,
        otherwise random
        
        Args:
            valid_locations (list): List of valid column indices
            
        Returns:
            int: Column index for the move
        """
        # Check if AI can win in the next move
        for col in valid_locations:
            row = self.board.get_next_open_row(col)
            temp_board = self.board.board.copy()
            temp_board[row][col] = self.PLAYER
            
            if self._check_win_state(temp_board, self.PLAYER):
                return col
        
        # Check if opponent can win in the next move and block
        for col in valid_locations:
            row = self.board.get_next_open_row(col)
            temp_board = self.board.board.copy()
            temp_board[row][col] = self.OPPONENT
            
            if self._check_win_state(temp_board, self.OPPONENT):
                return col
        
        # Otherwise, choose randomly
        return random.choice(valid_locations)
    
    def _get_hard_move(self, valid_locations):
        """Get the best move using minimax algorithm with alpha-beta pruning
        
        Args:
            valid_locations (list): List of valid column indices
            
        Returns:
            int: Column index for the best move
        """
        best_score = -math.inf
        best_col = random.choice(valid_locations)
        
        for col in valid_locations:
            row = self.board.get_next_open_row(col)
            temp_board = self.board.board.copy()
            temp_board[row][col] = self.PLAYER
            
            score = self._minimax(temp_board, 4, False, -math.inf, math.inf)
            
            if score > best_score:
                best_score = score
                best_col = col
        
        return best_col
    
    def _minimax(self, board, depth, is_maximizing, alpha, beta):
        """Minimax algorithm with alpha-beta pruning
        
        Args:
            board: Current board state
            depth (int): Current depth in the search tree
            is_maximizing (bool): True if maximizing player's turn
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            
        Returns:
            float: Score for the current board state
        """
        # Check terminal states
        if self._check_win_state(board, self.PLAYER):
            return 100000
        elif self._check_win_state(board, self.OPPONENT):
            return -100000
        elif self._is_board_full(board) or depth == 0:
            return self._evaluate_board(board)
        
        valid_locations = self._get_valid_locations(board)
        
        if is_maximizing:
            value = -math.inf
            for col in valid_locations:
                row = self._get_next_open_row(board, col)
                temp_board = board.copy()
                temp_board[row][col] = self.PLAYER
                
                new_score = self._minimax(temp_board, depth-1, False, alpha, beta)
                value = max(value, new_score)
                alpha = max(alpha, value)
                
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for col in valid_locations:
                row = self._get_next_open_row(board, col)
                temp_board = board.copy()
                temp_board[row][col] = self.OPPONENT
                
                new_score = self._minimax(temp_board, depth-1, True, alpha, beta)
                value = min(value, new_score)
                beta = min(beta, value)
                
                if alpha >= beta:
                    break
            return value
    
    def _evaluate_board(self, board):
        """Evaluate the board state
        
        Args:
            board: Current board state
            
        Returns:
            float: Score for the current board state
        """
        score = 0
        
        # Score center column
        center_array = board[:, 3]
        center_count = np.count_nonzero(center_array == self.PLAYER)
        score += center_count * 3
        
        # Score horizontal
        for r in range(self.board.rows):
            for c in range(self.board.cols - 3):
                window = board[r, c:c+4]
                score += self._evaluate_window(window)
        
        # Score vertical
        for c in range(self.board.cols):
            for r in range(self.board.rows - 3):
                window = board[r:r+4, c]
                score += self._evaluate_window(window)
        
        # Score positive diagonal
        for r in range(self.board.rows - 3):
            for c in range(self.board.cols - 3):
                window = [board[r+i][c+i] for i in range(4)]
                score += self._evaluate_window(window)
        
        # Score negative diagonal
        for r in range(3, self.board.rows):
            for c in range(self.board.cols - 3):
                window = [board[r-i][c+i] for i in range(4)]
                score += self._evaluate_window(window)
        
        return score
    
    def _evaluate_window(self, window):
        """Evaluate a window of 4 positions
        
        Args:
            window: Array of 4 positions
            
        Returns:
            int: Score for the window
        """
        score = 0
        
        player_count = np.count_nonzero(window == self.PLAYER)
        opponent_count = np.count_nonzero(window == self.OPPONENT)
        empty_count = np.count_nonzero(window == 0)
        
        if player_count == 4:
            score += 100
        elif player_count == 3 and empty_count == 1:
            score += 5
        elif player_count == 2 and empty_count == 2:
            score += 2
        
        if opponent_count == 3 and empty_count == 1:
            score -= 4
        
        return score
    
    def _check_win_state(self, board, player):
        """Check if the given player has won
        
        Args:
            board: Current board state
            player (int): Player number to check for win
            
        Returns:
            bool: True if player has won, False otherwise
        """
        # Check horizontal
        for r in range(self.board.rows):
            for c in range(self.board.cols - 3):
                if (board[r][c] == player and
                    board[r][c+1] == player and
                    board[r][c+2] == player and
                    board[r][c+3] == player):
                    return True
        
        # Check vertical
        for r in range(self.board.rows - 3):
            for c in range(self.board.cols):
                if (board[r][c] == player and
                    board[r+1][c] == player and
                    board[r+2][c] == player and
                    board[r+3][c] == player):
                    return True
        
        # Check diagonal (positive slope)
        for r in range(self.board.rows - 3):
            for c in range(self.board.cols - 3):
                if (board[r][c] == player and
                    board[r+1][c+1] == player and
                    board[r+2][c+2] == player and
                    board[r+3][c+3] == player):
                    return True
        
        # Check diagonal (negative slope)
        for r in range(3, self.board.rows):
            for c in range(self.board.cols - 3):
                if (board[r][c] == player and
                    board[r-1][c+1] == player and
                    board[r-2][c+2] == player and
                    board[r-3][c+3] == player):
                    return True
        
        return False
    
    def _is_board_full(self, board):
        """Check if the board is full
        
        Args:
            board: Current board state
            
        Returns:
            bool: True if the board is full, False otherwise
        """
        return not any(board[0] == 0)
    
    def _get_valid_locations(self, board):
        """Get all valid column locations for the next move
        
        Args:
            board: Current board state
            
        Returns:
            list: List of valid column indices
        """
        valid_locations = []
        for col in range(self.board.cols):
            if board[0][col] == 0:
                valid_locations.append(col)
        return valid_locations
    
    def _get_next_open_row(self, board, col):
        """Find the next open row in the given column
        
        Args:
            board: Current board state
            col (int): Column to check
            
        Returns:
            int: Row index of the next open position
        """
        for r in range(self.board.rows-1, -1, -1):
            if board[r][col] == 0:
                return r
        return -1
