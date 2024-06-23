from dice import DiceSet
from color import Color
from board import Board
from board import BoardState
import keyboard
import time
from utils import A1_to_coord


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
    
    def terminal_turn(self, dice):
        """ Take a turn. """
        print(f"~~~ {str(self)} ~~~")
        # Display the board.
        print(str(self.board))

        # Let the player roll the dice. Simulate dice rolling.
        while not (keyboard.is_pressed('space') or keyboard.is_pressed('enter')):
            print(dice.roll())
            time.sleep(0.01)
            print('\r') # Carriage return to print again
        # Roll once more
        print(dice.roll)

        # Get possible moves
        options = self.valid_options(dice)

        # Let the player make a move
        valid_choice = False
        while not valid_choice:
            # TODO: clean up the display of options
            print("Options: " + options)
            user_input = input("Choose your move (submit \"-\" for penalty): ")
            if user_input.strip() == "-":
                valid_choice = True
                self.penalize()
            else:
                valid_choice = self.board.A1_mark(user_input.strip())
        
        # Display new score
        print(f"Your current score is {self.score()}.")

        return self.get_state()
        
    def score(self):
        return self.board.score()
    
    def get_state(self):
        return self.board.get_state()
    
    def __str__(self):
        return self.name

    
            

