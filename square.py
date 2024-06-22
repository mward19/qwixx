from color import Color
from utils import strikethrough_text

class Square:
    def __init__(self, color, value, lock=False):
        self.color = color
        self.value = value
        self.x = False

    def term_rep(self, width=4):
        text = Color.color_text(self.color, self.value)
        if self.x:
            text = strikethrough_text(text)
        # The length cannot be calculated with `text` because of the ANSI escape sequences
        padding = ' ' * (width - len(str(self.value)))
        return text + padding
    
    # TODO: Doesn't implement crossing out
    def __str__(self):
        return (str(self.color) + str(self.value))
