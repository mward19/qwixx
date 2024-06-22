from dice import DiceSet
from color import Color


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
    
    def valid_options(self, dice):
        """ Uses dice's (DiceSet) last roll to calculate all possible moves. """
        all_options = dice.options()
        valid_options = []
        for option in all_options:
            valid_options.append(self.board.placements(option))
        return valid_options

    
            

