from square import Square
from color import Color
from utils import strikethrough_text

class Row:
    """ 
    A row of squares for a Qwixx board.
    
    Attributes:
        squares (list of Squares): A list of Qwixx board squares
        locked (bool): If true, the row is locked
    """
    def __init__(self, squares):
        self.squares = squares
        self.locked = False
    
    def __len__(self):
        return len(self.squares)
    
    def __iter__(self):
        return self.squares
    
    def __getitem__(self, index):
        return self.squares[index]
    
    def lock(self):
        self.locked = True
    
    def locked(self):
        return self.locked

    def term_rep(self, sq_width=6):
        """
        A colored representation using ANSI escape sequences for terminals.
        """
        text = ""
        row_len = len(self)
        # Display each square
        for square in self.squares:
            text += square.term_rep(sq_width)
        
        # Display lock icon
        lock_icon = Color.color_text(self.squares[-1].color, "L")
        if self.squares[-1].x: 
            text += strikethrough_text(lock_icon)
        else:
            text += lock_icon
        
        return text

    # TODO: Doesn't implement crossing out
    def __str__(self): 
        sq_size = 4
        row_len = len(self)
        # Display each square
        for square in self.squares:
            text += str(square).ljust(sq_size)
        
        # Display lock icon
        text += str(self.squares[-1].color) + "L"
        
        return text  
