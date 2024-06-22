from color import Color
from utils import strikethrough_text

class Square:
    """ 
    A square for a Qwixx board. 
    
    Attributes:
        color (Color): The color of the square
        value (int): The dice sum required to mark this square
        x (bool): If true, the square is marked (x'ed).
    """
    def __init__(self, color, value, lock=False):
        self.color = color
        self.value = value
        self.x = False

    def mark(self):
        if self.x: raise(RuntimeError("Square already marked"))
        self.x = True
    
    def term_rep(self, width=6):
        """
        A colored representation using ANSI escape sequences for terminals.
        """
        text = Color.color_text(self.color, ("·" + str(self.value) + "·").center(width))
        if self.x:
            text = strikethrough_text(text)
        return text
    
    # TODO: Doesn't implement crossing out
    def __str__(self):
        return (str(self.color) + str(self.value))
