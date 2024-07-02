from enum import Enum

class Color(Enum):
    RED = 'R'
    YELLOW = 'Y'
    GREEN = 'G'
    BLUE = 'B'
    NO_COLOR = 'W'
    locked = False

    def __str__(self):
        return self.value
    
    def color_text(color, text):
        """ Color text for ANSI escape sequence supporting terminals. """
        if color == Color.NO_COLOR: return str(text)
        
        color_term_prefix = {
            Color.RED:      "\033[91m",
            Color.YELLOW:   "\033[93m",
            Color.GREEN:    "\033[92m",
            Color.BLUE:     "\033[94m",
        }

        color_term_suffix = "\033[0m"

        return color_term_prefix[color] + str(text) + color_term_suffix
    
    def compatible(die_color, square_color):
        """
        Checks if the die color is compatible with the square color.
        """
        return die_color == square_color or die_color == Color.NO_COLOR