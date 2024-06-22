from square import Square
from color import Color
from utils import strikethrough_text

class Row:
    def __init__(self, squares):
        self.squares = squares
        self.locked = False
    
    def __len__(self):
        return len(self.squares)
    
    def lock(self):
        self.locked = True
    
    def locked(self):
        return self.locked

    def term_rep(self):
        text = ""
        row_len = len(self)
        # Display each square
        for square in self.squares:
            text += square.term_rep()
        
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
