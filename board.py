from row import Row
from square import Square
from color import Color
from utils import A1_to_coord
from utils import coord_to_A1

class Board:
    """
    Represents a Qwixx board for one player. Contains many Squares.

    Attributes:
    
    """
    def __init__(self):
        """ Default Qwixx layout. """
        # Generate rows of Squares
        red_row =    Row([Square(Color.RED,    dice_val) for dice_val in range(2, 13)])
        yellow_row = Row([Square(Color.YELLOW, dice_val) for dice_val in range(2, 13)])
        green_row =  Row([Square(Color.GREEN,  dice_val) for dice_val in range(12, 1, -1)])
        blue_row =   Row([Square(Color.BLUE,   dice_val) for dice_val in range(12, 1, -1)])

        # Stack rows, save as self.rows
        self.rows = [red_row, yellow_row, green_row, blue_row]
        self.penalty_val = 5
        self.penalties = 0

        self.MAX_PENALTIES = 3
    
    
    def term_rep(self, sq_width=6):
        """
        Yields a colored representation for terminals using ANSI escape sequences.
        """
        max_row_len = max([len(row) for row in self.rows])
        lmargin = 3

        # A header, with numeric column coordinates.
        text = ' ' * lmargin
        text += ''.join([str(column).center(sq_width)
                         for column in range(1, max_row_len+1)])
        text += "\n"

        for row_index, row in enumerate(self.rows):
            # Index rows with letters, calculated with ASCII codes
            text += chr(65 + row_index).rjust(lmargin) 
            text += row.term_rep(sq_width)
            text += "\n"
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
    
    def mark(self, row_index, col_index):
        return self.rows[row_index].mark(col_index)
    
    def valid_place(self, option, row_index, sq_index):
        """
        Checks if `option` (tuple: (Color, value)) can be played on a given square
        """
        row = self.rows[row_index]
        square = row[sq_index]
        color, value = option

        # Must be of a compatible color 
        color_cond     = (Color.compatible(color, square.color))
        # Must share square value
        value_cond     = (value == square.value)
        # No squares marked to the here or to the right
        placement_cond = (True not in [sq.marked for sq in row[sq_index:]])
        
        return color_cond and value_cond and placement_cond
    
    def placements(self, option):
        """
        Checks where `option` (tuple: (Color, value)) can be played on the board.
        Returns a list of 'A1' coordinate strings (potentially empty).
        """
        color, value = option
        placements = []
        for row_index, row in enumerate(self.board):
            for col_index, square in enumerate(row):
                if self.valid_place(option, row_index, col_index):
                    placements.append(coord_to_A1(row_index, col_index))
        return placements
    
    def score(self):
        score = 0
        # Score rows
        for row in self.rows:
            score += row.score()
        # Score penalties
        score -= self.penalties * self.penalty_val

        return score
    
    def __getitem__(self, index):
        return self.rows[index]

if __name__ == "__main__":
    board = Board()
    print(board.term_rep())