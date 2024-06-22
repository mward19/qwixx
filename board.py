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
        self.board = Board.get_default_board()
        self.MAX_PENALTIES = 3
    
    def get_default_board():
        # Generate rows of Squares
        red_row =    Row([Square(Color.RED,    dice_val) for dice_val in range(2, 13)])
        yellow_row = Row([Square(Color.YELLOW, dice_val) for dice_val in range(2, 13)])
        green_row =  Row([Square(Color.GREEN,  dice_val) for dice_val in range(12, 1, -1)])
        blue_row =   Row([Square(Color.BLUE,   dice_val) for dice_val in range(12, 1, -1)])

        # Stack rows
        board = [red_row, yellow_row, green_row, blue_row]
        return board
    
    def term_rep(self):
        text = ""
        for row in self.board:
            text += row.term_rep()
            text += "\n"
        return text
        
    def __str__(self):
        return 0 # TODO


if __name__ == "__main__":
    board = Board()
    print(board.term_rep())