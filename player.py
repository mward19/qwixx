from dice import DiceSet
from color import Color
import keyboard
import time


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
        # Display the board.
        print(str(self.board))

        # Let the player roll the dice. Simulate dice rolling.
        while not (keyboard.is_pressed('space') or keyboard.is_pressed('enter')):
            print(dice.roll())
            time.sleep(0.01)
            print('\r') # Carriage return to print again
        # Roll once more
        print(dice.roll)

        
    
    def __str__(self):
        return self.name

    
            

