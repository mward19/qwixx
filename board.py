from enum import Enum

def strikethrough_text(text):
    strike_prefix = "\033[9m"
    strike_suffix = "\033[0m"
    return strike_prefix + str(text) + strike_suffix

class Color(Enum):
    RED = 'R'
    YELLOW = 'Y'
    GREEN = 'G'
    BLUE = 'B'

    def __str__(self):
        return self.value
    
    def color_text(color, text):
        """ Color text for ANSI escape sequence supporting terminals. """
        color_term_prefix = {
            Color.RED:    "\033[91m",
            Color.YELLOW: "\033[93m",
            Color.GREEN:  "\033[92m",
            Color.BLUE:   "\033[94m"
        }

        color_term_suffix = "\033[0m"

        return color_term_prefix[color] + str(text) + color_term_suffix

class Square:
    def __init__(self, color, value, lock=False):
        self.color = color
        self.value = value
        self.x = False

    def term_rep(self, width=3):
        text = Color.color_text(self.color, self.value)
        if self.x:
            text = strikethrough_text(text)
        # The length cannot be calculated with `text` because of the ANSI escape sequences
        padding = ' ' * (width - len(str(self.value)))
        return text + padding
    
    def __str__(self):
        return (str(self.color) + str(self.value))


class Board:
    """
    Represents a Qwixx board for one player. Contains many Squares.

    Attributes:
    
    """
    def __init__(self):
        """ Default Qwixx layout. """
        self.board = Board.get_default_board()
        self.MAX_PENALTIES = 3
    
    def get_default_board():
        # Generate rows of Squares
        red_row =    [Square(Color.RED,    dice_val) for dice_val in range(2, 13)]
        yellow_row = [Square(Color.YELLOW, dice_val) for dice_val in range(2, 13)]
        green_row =  [Square(Color.GREEN,  dice_val) for dice_val in range(12, 1, -1)]
        blue_row =   [Square(Color.BLUE,   dice_val) for dice_val in range(12, 1, -1)]

        # Stack rows
        board = [red_row, yellow_row, green_row, blue_row]
        return board
    
    def term_rep(self):
        text = ""
        for row in self.board:
            row_len = len(row)
            for col, square in enumerate(row):
                text += square.term_rep()
            text += "\n"
        return text
        

    def __str__(self):
        return 0 # TODO


if __name__ == "__main__":
    board = Board()
    print(board.term_rep())