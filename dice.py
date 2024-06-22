from color import Color
import random
from itertools import combinations
from itertools import product

class Die:
    """
    A Qwixx die. 
    
    Attributes:
        color (Color): the color of the die
        sides (int): the number of sides
        last_roll (int): the last roll of the die

    Methods:
        roll(): rolls the die, saving and yielding an element of {1, ..., sides}
    """

    def __init__(self, color=Color.NO_COLOR, sides=6):
        self.color = color
        self.sides = sides
        self.last_roll = 0
        self.roll()
    
    def roll(self):
        """ Rolls the die, saving and yielding an element of {1, ..., sides} """
        self.last_roll = random.randint(1, self.sides)
        return self.last_roll
    
    def __int__(self):
        return self.last_roll

    def __add__(self, other):
        return int(self) + int(other)
    
    def __str__(self):
        return str(self.color) + str(self.last_roll)
    
    def term_rep(self):
        return Color.color_text(self.color, ":" + str(self.last_roll) + ":")


class DiceSet:
    """ Implements a set of six Qwixx dice. """

    def __init__(self):
        """ Default set of dice: red, yellow, green, blue, white, white. """
        colors = [
            Color.RED,
            Color.YELLOW, 
            Color.GREEN, 
            Color.BLUE, 
            Color.NO_COLOR, 
            Color.NO_COLOR
            ]
        sides = [6 for c in colors]

        # Create the dice, for convenience separate into white and colored groups
        self.dice = set()
        self.white_dice = set()
        self.colored_dice = set()
        for (c, s) in zip(colors, sides):
            d = Die(c, s)
            self.dice.add(d)
            if d.color == Color.NO_COLOR: self.white_dice.add(d)
            else: self.colored_dice.add(d)
            

    def __str__(self):
        output = ""
        for d in self.dice:
            output += str(d) + " "
        return output
    
    def term_rep(self):
        output = ""
        for d in self.dice:
            output += d.term_rep() + " "
        return output
        
    def roll(self):
        for die in self.dice: die.roll()
        return str(self)
    
    def options(self):
        """ 
        Using last roll, returns all play options as (Color, value)
        tuples by combining sets of two dice.
        """
        play_options = []

        # Get colorless combinations, usable by all players.
        for (d1, d2) in combinations(self.white_dice):
            play_options.append((Color.NO_COLOR, d1+d2))

        # Get colored combinations
        for (d_colored, d_white) in product(self.colored_dice, self.white_dice):
            play_options.append((d_colored.color, d_colored + d_white))
        
        return play_options
    
if __name__ == "__main__":
    ds = DiceSet()
    print(ds.roll())
    print(ds.term_rep())