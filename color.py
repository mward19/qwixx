from enum import Enum

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