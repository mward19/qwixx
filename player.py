from dice import DiceSet
from color import Color
from utils import A1_to_coord
from utils import coord_to_A1

class Player:
    """ Abstraction of a player in Qwixx. """
    def __init__(self, name, board):
        self.name = name
        self.board = board
        self.points = 0
    
    def add(self, points):
        self.points += points
        return self.points
    
    def penalize(self):
        return self.board.add_penalty()
    
    def placements(self, option):
        """
        Checks where `option` (tuple: (Color, value)) can be played on the board.
        Returns a list of (row, column) coordinate tuples (potentially empty).
        """
        color, value = option
        placements = []

