from color import Color
from utils import strikethrough_text

class Square:
    """ 
    A square for a Qwixx board. 
    
    Attributes:
        color (Color): The color of the square
        value (int): The dice sum required to mark this square
        marked (bool): If true, the square is marked.
    """
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.marked = False

    def mark(self):
        if self.marked: raise(RuntimeError("Square already marked"))
        self.marked = True
    
    def term_rep(self, border="·", width=6):
        """
        A colored representation using ANSI escape sequences for terminals.
        """
        text = Color.color_text(
            self.color,
            (border + str(self.value) + border).center(width)
        )
        if self.marked:
            text = strikethrough_text(text)
        return text
    
    # TODO: Doesn't implement crossing out
    def __str__(self):
        return (str(self.color) + str(self.value))
