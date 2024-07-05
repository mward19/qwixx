from player import Player
from dice import DiceSet
from board import Board
from board import BoardState
from color import Color
import random
from abc import ABC, abstractmethod

class QwixxGame(ABC):
    """
    An abstract class that manages a game of Qwixx.
    An implementation would run the game in a terminal, browser, or app.
    """
    @abstractmethod
    def __init__(self, players, dice, lc):
        self.players = players
        self.dice = dice
        self.locked_colors = lc
        self.N_players = len(self.players)

    def lock(self, color):
        self.locked_colors.add(color)
    
    @abstractmethod
    def display_player_order(self, player_order):
        pass

    @abstractmethod
    def roll_dice(self):
        """
        Roll the dice.
        """
        pass
    
    @abstractmethod
    def display_dice(self):
        pass
    
    @abstractmethod
    def display_white_dice(self):
        pass


    @abstractmethod
    def display_all_options(self, player):
        """
        Displays all dice options for `player`, white first, then colored. Used on a player's turn, after a dice roll, but before other players have decided to use the white roll.
        """
        pass

    def get_other_players(self, player_order, player, player_index=None):
        """
        Get a list of the other players that come after player in order.
        
        Returns:
            (list of Players): A list of the players besides `player`.
        """
        N = self.N_players
        idx = player_index # Index of this player
        if idx == None:
            idx = player_order.index(player)
        begin = (idx + 1) % N
        first_set =  player_order[begin:] if begin != 0 else []
        second_set = player_order[:idx]
        return first_set + second_set
    
    def penalize(self, player):
        player.penalize()

    @abstractmethod
    def play_game(self, player_order=None):
        """
        Begins and manages a Qwixx game.

        Args:
            player_order (list of Players): The order of the players, as a list of players.
        """
        pass

    @abstractmethod
    def display_board(self, player):
        """
        Displays a player's board. If desired, other player's boards may be displayed, but they would be displayed secondarily.
        """
        pass

    @abstractmethod
    def display_boards(self):
        """
        Displays all players' boards, with equal priority.
        """
        pass
    
    @abstractmethod
    def display_podium(self):
        """
        Displays a podium with the players ranked by their score. Intended for use at the conclusion of the game.
        """
        pass

    @abstractmethod
    def display_intro(self):
        """
        Displays an introduction to the Qwixx game.
        """
        pass

