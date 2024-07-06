from color import Color
import random
from itertools import combinations
from itertools import product
import shutil
from utils import ansi_center

class Die:
    """
    A Qwixx die.
    
    Attributes:
        color (Color): The color of the die.
        sides (int): The number of sides on the die.
        last_roll (int): The result of the last roll of the die.

    Methods:
        roll(): Rolls the die, saving and returning a value between 1 and the number of sides.
    """

    def __init__(self, color=Color.NO_COLOR, sides=6):
        """
        Initializes a Die instance with a specified color and number of sides.

        Parameters:
        color (Color): The color of the die. Default is Color.NO_COLOR.
        sides (int): The number of sides on the die. Default is 6.
        """
        self.color = color
        self.sides = sides
        self.last_roll = 0
        self.roll()
    
    def roll(self):
        """
        Rolls the die, saving and returning a value between 1 and the number of sides.

        Returns:
        int: The result of the die roll.
        """
        self.last_roll = random.randint(1, self.sides)
        return self.last_roll
    
    def __int__(self):
        """
        Returns the last roll result when the Die object is cast to an integer.

        Returns:
        int: The result of the last roll.
        """
        return self.last_roll

    def __add__(self, other):
        """
        Adds the results of two dice rolls.

        Parameters:
        other (Die): Another Die instance to add.

        Returns:
        int: The sum of the last rolls of both dice.
        """
        return int(self) + int(other)
    
    def __str__(self):
        """
        Returns a string representation of the die, showing its color and last roll.

        Returns:
        str: A string representation of the die.
        """
        return str(self.color) + str(self.last_roll)
    
    def term_rep(self):
        """
        Returns a terminal-friendly string representation of the die.

        Returns:
        str: A terminal-friendly string representation of the die.
        """
        return Color.color_text(self.color, ":" + str(self.last_roll) + ":")


class DiceSet:
    """
    Implements a set of six Qwixx dice.

    Attributes:
        dice (list): A list of Die instances representing the dice set.
        white_dice (list): A list of Die instances representing the white dice.
        colored_dice (list): A list of Die instances representing the colored dice.

    Methods:
        roll(): Rolls all the dice in the set.
        white_options(): Returns colorless play options based on the last roll.
        color_options(): Returns colored play options based on the last roll.
        term_rep(): Returns a terminal-friendly string representation of the dice set.
    """

    def __init__(self):
        """
        Initializes a DiceSet instance with six dice: two white and four colored (red, yellow, green, blue).
        """
        colors = [
            Color.NO_COLOR,
            Color.NO_COLOR,
            Color.RED,
            Color.YELLOW, 
            Color.GREEN, 
            Color.BLUE
            ]
        sides = [6 for c in colors]

        # Create the dice, for convenience separate into white and colored groups
        self.dice = []
        self.white_dice = []
        self.colored_dice = []
        for (c, s) in zip(colors, sides):
            d = Die(c, s)
            self.dice.append(d)
            if d.color == Color.NO_COLOR:
                self.white_dice.append(d)
            else:
                self.colored_dice.append(d)
            

    def __str__(self):
        """
        Returns a string representation of the dice set, showing all dice and their last rolls.

        Returns:
        str: A string representation of the dice set.
        """
        output = ""
        for d in self.dice:
            output += str(d) + " "
        return output
    
    def term_rep(self):
        """
        Returns a terminal-friendly string representation of the dice set.

        Returns:
        str: A terminal-friendly string representation of the dice set, centered in the terminal.
        """
        terminal_size = shutil.get_terminal_size().columns
        output = ""
        for d in self.dice:
            output += d.term_rep() + " "
        return ansi_center(output, terminal_size)
        
    def roll(self):
        """
        Rolls all the dice in the set and returns their string representation.

        Returns:
        str: A string representation of the dice set after rolling.
        """
        for die in self.dice:
            die.roll()
        return str(self)
    
    def white_options(self):
        """
        Using the last roll, returns colorless play options as (Color, value) tuples by combining sets of two dice.

        Returns:
        list: A list of tuples representing colorless play options.
        """
        play_options = []

        # Get colorless combinations, usable by all players.
        for (d1, d2) in combinations(self.white_dice, 2):
            play_options.append((Color.NO_COLOR, d1 + d2))

        return play_options
    
    def color_options(self):
        """
        Using the last roll, returns all colored play options as (Color, value) tuples by combining sets of two dice.

        Returns:
        list: A list of tuples representing colored play options.
        """
        play_options = []

        # Get colored combinations
        for (d_colored, d_white) in product(self.colored_dice, self.white_dice):
            play_options.append((d_colored.color, d_colored + d_white))
        
        return play_options
    
    def __iter__(self):
        """
        Returns an iterator over the dice in the set.

        Returns:
        iterator: An iterator over the dice in the set.
        """
        return iter(self.dice)