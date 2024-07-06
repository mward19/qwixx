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
    """ 
    Abstraction of a player in Qwixx.
    
    Attributes:
    name (str): The name of the player.
    board (Board): The board associated with the player.
    points (int): The current points of the player.
    """
    def __init__(self, name, board):
        """
        Initializes a Player instance.

        Parameters:
        name (str): The name of the player.
        board (Board): The board associated with the player.
        """
        self.name = name
        self.board = board
        self.points = 0
    
    def add(self, points):
        """
        Adds points to the player's score.

        Parameters:
        points (int): The number of points to add.

        Returns:
        int: The updated points of the player.
        """
        self.points += points
        return self.points
    
    def penalize(self):
        """
        Penalizes the player by adding a penalty to the board.

        Returns:
        int: The updated penalty count on the board.
        """
        return self.board.add_penalty()

    def valid_placements(self, dice, white_turn=True):
        """
        Calculates all possible valid placements based on the last roll of the dice.

        Parameters:
        dice (DiceSet): The dice set used in the game.
        white_turn (bool): Indicates if it's the white dice turn. Default is True.

        Returns:
        list: A list of valid placements.
        """
        options = dice.white_options() if white_turn else dice.color_options()
        valid_placements = []
        for option in options:
            valid_placements += self.board.placements(option, white_turn)
        return list(set(valid_placements))
    
    def valid_A1(self, A1_coord):
        """
        Checks if the provided A1 coordinate is valid and within the board bounds.

        Parameters:
        A1_coord (str): The A1 coordinate to validate.

        Returns:
        bool: True if the coordinate is valid, False otherwise.
        """
        n_rows = self.board.n_rows()
        n_cols = self.board.n_cols()
        return valid_A1(A1_coord, n_rows, n_cols)
    
    def score(self):
        """
        Calculates the current score of the player based on the board state.

        Returns:
        int: The current score of the player.
        """
        return self.board.score()
    
    def get_state(self):
        """
        Retrieves the current state of the board.

        Returns:
        BoardState: The current state of the board.
        """
        return self.board.get_state()
    
    def __str__(self):
        """
        Returns a string representation of the player.

        Returns:
        str: The name of the player.
        """
        return self.name
