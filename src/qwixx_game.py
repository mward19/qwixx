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
    def __init__(self, players, dice):
        self.players = players
        self.dice = dice
        self.N_players = len(self.players)
    
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
    def white_choice(self, player):
        """
        Displays the white die options for `player`.
        Allows them to choose which option they will take.
        Returns:
            (bool) If the choice was successful
        """
        pass

    @abstractmethod
    def color_choice(self, player):
        """
        Displays the colored die options for `player`.
        Allows them to choose which option they will take.
        If no option is chosen, invokes a penalty on the player.
        Returns:
            (bool) If the choice was successful
        """
        pass

    @abstractmethod
    def all_choice(self, player):
        """
        Displays all dice options for `player`, white first, then colored.
        Allows them to choose which option(s) they will take.
        If no option is chosen, invokes a penalty on the player.
        Returns:
            (bool) If the choice was successful
        """
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
        return player_order[begin:] + player_order[:idx]
        

    def play_game(self, player_order=None):
        """
        Begins and manages a Qwixx game.

        Args:
            player_order (list of Players): The order of the players, as a list of players.
        """
        self.display_intro()

        # If no player_order is provided, use a random order
        if player_order == None:
            player_order = random.sample(self.players, len(self.players))
        
        self.display_player_order(player_order)

        # TODO: implement mutiplayer locking with boardstates
        # Begin turns
        for p_index, p in enumerate(player_order):
            self.display_board(p)
            self.roll_dice()
            self.display_dice()
            # Let this player see the roll they made
            self.display_all_options(p)

            # Let other players use white roll
            other_players = self.get_other_players(player_order, p, p_index)
            for other_p in other_players:
                self.display_board(other_p)
                self.display_white_dice()
                self.white_choice(other_p)
            # Let this player use roll
            self.all_choice(p)
            # Display updated board
            self.display_board(p)
        
        # Show final boards
        self.display_boards()
        # Show final scores
        self.display_podium()
    
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

