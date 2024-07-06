from square import Square
from color import Color
from utils import strikethrough
from utils import ansi_center

class Row:
    """ 
    A row of squares for a Qwixx board.
    
    Attributes:
        squares (list of Squares): A list of Qwixx board squares.
        scoring (dict: int -> int): A dictionary mapping marks to scores based on default metrics.
        locked_colors (set of Color): A set of colors that are locked for marking in this row.
    """
    def __init__(self, squares, locked_colors):
        """
        Initializes a Row instance with a list of squares and locked colors.

        Parameters:
        squares (list of Square): The squares in the row.
        locked_colors (set of Color): The colors that are locked for marking in this row.
        """
        self.squares = squares
        # Default scoring metric
        self.scoring = Row.default_metric(len(self.squares))
        self.lock_min = 5
        self.locked_colors = locked_colors
    
    @staticmethod
    def default_metric(n_squares):
        """
        Generates a default scoring metric based on the number of squares.

        Parameters:
        n_squares (int): The number of squares in the row.

        Returns:
        dict: A dictionary mapping marks to scores based on default metrics.
        """
        scoring = dict()
        curr_val = 0
        for index in range(n_squares + 2):  # +2 because of the possibility of locking
            curr_val += index
            scoring[index] = curr_val
        return scoring

    def score(self):
        """
        Calculates the current score of the row based on marked squares and locking bonus.

        Returns:
        int: The current score of the row.
        """
        marks = sum([sq.marked for sq in self.squares])
        # Add locking bonus
        if self.squares[-1].marked:
            marks += 1

        return self.scoring[marks]
    
    def color_lock(self, color):
        """
        Locks a color for marking in this row.

        Parameters:
        color (Color): The color to be locked.
        """
        self.locked_colors.add(color)

    def what_is_locked(self):
        """
        Returns the color that is locked by this row, if any.

        Returns:
        Color or None: The color that is locked or None if no color is locked.
        """
        if self.squares[-1].marked:
            return self.squares[-1].color
        else:
            return None
    
    def mark(self, index):
        """
        Implements marking rules for a square in the row.

        Parameters:
        index (int): The index of the square to mark.

        Returns:
        bool: True if marking is successful, False otherwise.
        """
        marks = [sq.marked for sq in self.squares]
        # Do not allow marking a locked color
        if self.squares[index].color in self.locked_colors:
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
        """
        Returns the number of squares in the row.

        Returns:
        int: The number of squares in the row.
        """
        return len(self.squares)
    
    def __iter__(self):
        """
        Returns an iterator over the squares in the row.

        Returns:
        iterator: An iterator over the squares in the row.
        """
        return iter(self.squares)
    
    def __getitem__(self, index):
        """
        Returns the square at the specified index in the row.

        Parameters:
        index (int): The index of the square to retrieve.

        Returns:
        Square: The square at the specified index.
        """
        return self.squares[index]
    

    def term_rep(self, sq_width=6):
        """
        Returns a colored representation using ANSI escape sequences for terminals.

        Parameters:
        sq_width (int): The width of each square representation. Default is 6.

        Returns:
        str: A terminal-friendly string representation of the row.
        """
        text = ""
        row_len = len(self)
        # Display each square
        for square in self.squares:
            text += ansi_center(square.term_rep(), sq_width)
        
        # Display lock icon
        lock_icon = Color.color_text(self.squares[-1].color, "L")
        if self.squares[-1].marked: 
            text += strikethrough(lock_icon)
        else:
            text += lock_icon
        
        return text

    def __str__(self): 
        """
        Returns a string representation of the row.

        TODO: Implement crossing out for marked squares.

        Returns:
        str: A string representation of the row.
        """
        text = ""
        sq_size = 4
        row_len = len(self)
        # Display each square
        for square in self.squares:
            text += str(square).ljust(sq_size)
        
        # Display lock icon
        text += str(self.squares[-1].color) + "L"
        
        return text  
