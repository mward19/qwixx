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
    CONTINUE = 0
    LOCKED = 1
    PENALTIES = 2

class Board:
    """
    Represents a Qwixx board for one player. Contains many Squares.
    """
    def __init__(self, locked_colors):
        """ Default Qwixx layout. """
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
        Yields a colored representation for terminals using ANSI escape sequences.
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
            bool: if MAX_PENALTIES has been surpassed
        """
        self.penalties += 1
        return self.penalties > self.MAX_PENALTIES
    
    # TODO
    def __str__(self):
        return 0 
    
    def __iter__(self):
        return self.rows
    
    def n_rows(self):
        return len(self.rows)

    def n_cols(self):
        return max([len(row) for row in self.rows])
    
    def mark(self, row_index, col_index):
        return self.rows[row_index].mark(col_index)
    
    def valid(self, option, row_index, sq_index, white_turn=True):
        """
        Checks if `option` (tuple: (Color, value)) can be played on a given square
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
        Checks where `option` (tuple: (Color, value)) can be played on the board.
        Returns a list of coordinate tuples (row, column).
        """
        color, value = option
        placements = []
        for row_index, row in enumerate(self.rows):
            for col_index, square in enumerate(row):
                if self.valid(option, row_index, col_index, white_turn):
                    placements.append((row_index, col_index))
        return placements
    

    def score(self):
        score = 0
        # Score rows
        for row in self.rows:
            score += row.score()
        # Score penalties
        score -= self.penalties * self.penalty_val

        return score

    def get_state(self):
        # Count locked rows
        colors = [row[-1].color for row in self.rows]
        N_locked = sum([(color in self.locked_colors) for color in colors])

        if N_locked > self.MAX_LOCK:             return BoardState.LOCKED
        elif self.penalties > self.MAX_PENALTIES:   return BoardState.PENALTIES
        else:                                       return BoardState.CONTINUE
    
    def __getitem__(self, index):
        return self.rows[index]
    
    def update_lock(self):
        for row in self.rows:
            locked_color = row.what_is_locked()
            if locked_color: self.color_lock(locked_color)
        return self.locked_colors

    def color_lock(self, color):
        self.locked_colors.add(color)
    
if __name__ == "__main__":
    lc = {Color.GREEN} # locked colors
    board = Board(lc)
    board.mark(0, 7)
    print(board.valid_place((Color.BLUE, 5), 3, 7))