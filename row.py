from square import Square
from color import Color
from utils import strikethrough_text
from utils import color_center

class Row:
    """ 
    A row of squares for a Qwixx board.
    
    Attributes:
        squares (list of Squares): A list of Qwixx board squares
        locked (bool): If true, the row is locked
        scoring (dict: int -> int): TODO
        TODO
    """
    def __init__(self, squares):
        self.squares = squares
        self.locked = False
        # Default scoring metric
        self.scoring = Row.default_metric(len(self.squares))
        self.lock_min = 5
    
    def default_metric(n_squares):
        scoring = dict()
        curr_val = 0
        for index in range(n_squares + 2): # +2 because of the possibility of locking
            curr_val += index
            scoring[index] = curr_val
        return scoring

    def score(self):
        marks = sum([sq.marked for sq in self.squares])
        # Add locking bonus
        if self.squares[-1].marked: marks += 1

        return self.scoring[marks]
    
    def mark(self, index):
        """ Implements marking rules. If successful, returns True. """
        marks = [sq.marked for sq in self.squares]
        # Do not allow marking on a locked row
        if self.locked:
            return False
        # Do not allow marking on or to the left of other marks
        if True in marks[index:]:
            return False
        # Do not allow locking with less than self.lock_min marks
        if (index == len(self.squares)-1) and (sum(marks) < self.lock_min):
            return False
        
        # Otherwise, proceed with the mark
        self.squares[index].mark()
        return True

    def __len__(self):
        return len(self.squares)
    
    def __iter__(self):
        return iter(self.squares)
    
    def __getitem__(self, index):
        return self.squares[index]
    
    def lock(self):
        self.locked = True

    def term_rep(self, sq_width=6):
        """
        A colored representation using ANSI escape sequences for terminals.
        """
        text = ""
        row_len = len(self)
        # Display each square
        for square in self.squares:
            text += color_center(square.term_rep(), sq_width)
        
        # Display lock icon
        lock_icon = Color.color_text(self.squares[-1].color, "L")
        if self.squares[-1].marked: 
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
