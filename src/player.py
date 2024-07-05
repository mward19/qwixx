from dice import DiceSet
from color import Color
from board import Board
from board import BoardState
import time
import shutil
from utils import A1_to_coord
from utils import valid_A1
from utils import color_center
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

    # TODO: misleading function name. Or maybe the other one is misleading?
    def valid_options(self, dice, white_turn=True):
        """ Uses dice's (DiceSet) last roll to calculate all possible moves. """
        options = dice.white_options() if white_turn else dice.color_options()
        valid_options = []
        for option in options:
            valid_options += self.board.placements(option, white_turn)
        return list(set(valid_options))
    
    def valid_A1(self, A1_coord):
        n_rows = self.board.n_rows()
        n_cols = self.board.n_cols()
        return valid_A1(A1_coord, n_rows, n_cols)
    
    def terminal_turn(self, dice):
        """ Take a turn. """
        terminal_size = shutil.get_terminal_size().columns
        print(color_center(f"~~~ {str(self)} ~~~", terminal_size))
        # Display the board.
        print(self.board.term_rep())
        dice.roll()
        print()
        print(dice.term_rep())

        # Get possible moves
        options = self.valid_options(dice)

        # Let the player make a move
        valid_choice = False
        while not valid_choice:
            # TODO: clean up the display of options
            print("Options: " + str(options))
            user_input = input("Choose your move (submit \"-\" for penalty): ")
            if user_input.strip() == "-":
                valid_choice = True
                self.penalize()
            else:
                valid_choice = self.board.A1_mark(user_input.strip())
        
        # Display new score and modified board
        clear_terminal()
        print(self.board.term_rep())
        print(f"Your current score is {self.score()}.".center(terminal_size))
        time.sleep(3)
        print()
        input("Press enter to continue.".center(terminal_size))
        clear_terminal()

        return self.get_state()
        
    def score(self):
        return self.board.score()
    
    def get_state(self):
        return self.board.get_state()
    
    def __str__(self):
        return self.name

    
            

