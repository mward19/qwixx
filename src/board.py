from row import Row
from square import Square
from color import Color
from utils import A1_to_coord
from utils import coord_to_A1
from utils import valid_A1
from enum import Enum
import shutil
from utils import ansi_center

class BoardState(Enum):
    """
    Enum representing the possible states of a Qwixx board.
    
    Attributes:
        CONTINUE (int): Board state indicating the game can continue.
        LOCKED (int): Board state indicating that too many rows are locked.
        PENALTIES (int): Board state indicating that penalties have exceeded the maximum allowed.
    """
    CONTINUE = 0
    LOCKED = 1
    PENALTIES = 2

class Board:
    """
    Represents a Qwixx board for one player. Contains many Squares.
    
    Attributes:
        rows (list of Row): A list of rows, each containing squares of different colors.
        penalty_val (int): Value deducted per penalty.
        penalties (int): Number of penalties incurred.
        MAX_PENALTIES (int): Maximum number of penalties allowed.
        MAX_LOCK (int): Maximum number of locked rows allowed.
        locked_colors (set of Color): Colors that are locked for marking on the board.
    """
    def __init__(self, locked_colors):
        """
        Initializes a Qwixx board with default rows and settings.

        Parameters:
        locked_colors (set of Color): Colors that are initially locked on the board.
        """
        lc = locked_colors
        # Generate rows of Squares
        red_row =    Row([Square(Color.RED,    dice_val) 
                          for dice_val in range(2, 13)], lc)
        yellow_row = Row([Square(Color.YELLOW, dice_val) 
                          for dice_val in range(2, 13)], lc)
        green_row =  Row([Square(Color.GREEN,  dice_val) 
                          for dice_val in range(12, 1, -1)], lc)
        blue_row =   Row([Square(Color.BLUE,   dice_val) 
                          for dice_val in range(12, 1, -1)], lc)

        # Stack rows, save as self.rows
        self.rows = [red_row, yellow_row, green_row, blue_row]
        self.penalty_val = 5
        self.penalties = 0

        self.MAX_PENALTIES = 3
        self.MAX_LOCK = 1

        self.locked_colors = locked_colors
    
    
    def term_rep(self, sq_width=6):
        """
        Generates a colored representation of the board for terminals using ANSI escape sequences.

        Parameters:
        sq_width (int): Width of each square representation. Default is 6.

        Returns:
        str: A string representing the board's layout and current state.
        """
        terminal_size = shutil.get_terminal_size().columns
        max_row_len = max([len(row) for row in self.rows])
        lmargin = 3

        text= ""
        # A header, with numeric column coordinates.
        text_row = ' ' * lmargin
        text_row += ''.join([str(column).center(sq_width)
                         for column in range(1, max_row_len+1)])
        text_row = ansi_center(text_row, terminal_size)
        text += text_row + "\n"

        # The rows of the board.
        for row_index, row in enumerate(self.rows):
            text_row = ""
            # Index rows with letters, calculated with ASCII codes
            text_row += chr(65 + row_index).rjust(lmargin) 
            text_row += row.term_rep(sq_width)
            text_row = ansi_center(text_row, terminal_size)
            text += text_row + "\n"
        
        # Penalties.
        text += f"Penalties: {self.penalties}".center(terminal_size)
        
        return text
    
    def add_penalty(self):
        """
        Adds a penalty to the counter.

        Returns:
            bool: True if the maximum number of penalties has been surpassed, False otherwise.
        """
        self.penalties += 1
        return self.penalties > self.MAX_PENALTIES
    
    # TODO
    def __str__(self):
        return 0 
    
    def __iter__(self):
        """
        Returns an iterator over the rows of the board.

        Returns:
        iterator: An iterator over the rows of the board.
        """
        return iter(self.rows)
    
    def n_rows(self):
        """
        Returns the number of rows in the board.

        Returns:
        int: The number of rows in the board.
        """
        return len(self.rows)

    def n_cols(self):
        """
        Returns the maximum number of squares in any row of the board.

        Returns:
        int: The maximum number of squares in any row of the board.
        """
        return max([len(row) for row in self.rows])
    
    def mark(self, row_index, col_index):
        """
        Marks a square at a specific row and column index on the board.

        Parameters:
        row_index (int): Index of the row containing the square to mark.
        col_index (int): Index of the square to mark within the row.

        Returns:
        bool: True if marking was successful, False otherwise.
        """
        return self.rows[row_index].mark(col_index)
    
    def valid(self, option, row_index, sq_index, white_turn=True):
        """
        Checks if a given option (Color, value) can be played on a specific square on the board.

        Parameters:
        option (tuple): A tuple containing Color and value to check.
        row_index (int): Index of the row containing the square to check.
        sq_index (int): Index of the square within the row to check.
        white_turn (bool): True if it's a white dice turn, False otherwise. Default is True.

        Returns:
        bool: True if the option can be played on the square, False otherwise.
        """
        row = self.rows[row_index]
        square = row[sq_index]
        color, value = option

        # If white turn, must be white dice
        if white_turn and color != Color.NO_COLOR: return False
        # If color turn, must be color dice
        if (not white_turn) and (color == Color.NO_COLOR): return False
        # Must be of a compatible color 
        color_cond     = (Color.compatible(color, square.color))
        # Must not be of a locked color
        not_locked     = (square.color not in self.locked_colors)
        # Must share square value
        value_cond     = (value == square.value)
        # No squares marked here or to the right
        placement_cond = (True not in [sq.marked for sq in row[sq_index:]])
        
        return color_cond and not_locked and value_cond and placement_cond
    
    def placements(self, option, white_turn=True):
        """
        Finds all valid placements for a given option (Color, value) on the board.

        Parameters:
        option (tuple): A tuple containing Color and value to check.
        white_turn (bool): True if it's a white dice turn, False otherwise. Default is True.

        Returns:
        list of tuples: A list of coordinate tuples (row_index, col_index) where the option can be placed.
        """
        color, value = option
        placements = []
        for row_index, row in enumerate(self.rows):
            for col_index, square in enumerate(row):
                if self.valid(option, row_index, col_index, white_turn):
                    placements.append((row_index, col_index))
        return placements

    def score(self):
        """
        Calculates the current score of the board.

        Returns:
        int: The current score of the board.
        """
        score = 0
        # Score rows
        for row in self.rows:
            score += row.score()
        # Score penalties
        score -= self.penalties * self.penalty_val

        return score

    def get_state(self):
        """
        Determines the current state of the board based on locked rows and penalties.

        Returns:
        BoardState: The current state of the board (CONTINUE, LOCKED, or PENALTIES).
        """
        # Count locked rows
        colors = [row[-1].color for row in self.rows]
        N_locked = sum([(color in self.locked_colors) for color in colors])

        if N_locked > self.MAX_LOCK:             return BoardState.LOCKED
        elif self.penalties > self.MAX_PENALTIES:   return BoardState.PENALTIES
        else:                                       return BoardState.CONTINUE
    
    def __getitem__(self, index):
        """
        Returns the row at the specified index.

        Parameters:
        index (int): Index of the row to retrieve.

        Returns:
        Row: The row at the specified index.
        """
        return self.rows[index]
    
    def update_lock(self):
        """
        Updates the set of locked colors based on the current state of each row.

        Returns:
        set of Color: The updated set of locked colors.
        """
        for row in self.rows:
            locked_color = row.what_is_locked()
            if locked_color: self.color_lock(locked_color)
        return self.locked_colors

    def color_lock(self, color):
        """
        Locks a color for marking on the board.

        Parameters:
        color (Color): The color to lock.
        """
        self.locked_colors.add(color)
    