from row import Row
from square import Square
from color import Color

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
    
if __name__ == "__main__":
    board = Board()
    print(board.term_rep())