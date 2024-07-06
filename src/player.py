from dice import DiceSet
from color import Color
from board import Board
from board import BoardState
import time
import shutil
from utils import A1_to_coord
from utils import valid_A1
from utils import ansi_center
from utils import clear_terminal


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

    def valid_placements(self, dice, white_turn=True):
        """ Uses dice's (DiceSet) last roll to calculate all possible moves. """
        options = dice.white_options() if white_turn else dice.color_options()
        valid_placements = []
        for option in options:
            valid_placements += self.board.placements(option, white_turn)
        return list(set(valid_placements))
    
    def valid_A1(self, A1_coord):
        n_rows = self.board.n_rows()
        n_cols = self.board.n_cols()
        return valid_A1(A1_coord, n_rows, n_cols)
    
    def score(self):
        return self.board.score()
    
    def get_state(self):
        return self.board.get_state()
    
    def __str__(self):
        return self.name

    
            

