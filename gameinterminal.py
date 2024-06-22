from player import Player
from dice import DiceSet
from board import Board
from color import Color
import random

class GameInTerminal:
    def __init__(self, players):
        self.players = players
        self.dice = DiceSet()
    
    def __init__(self, names):
        self.players = [Player(name, Board()) for name in names]
        self.dice = DiceSet()

    def play(self):
        print("Welcome to " +
              Color.color_text(Color.RED, 'Q') +
              Color.color_text(Color.YELLOW, 'W') +
              Color.color_text(Color.NO_COLOR, 'I') +
              Color.color_text(Color.GREEN, 'X') +
              Color.color_text(Color.BLUE, 'X') +
              "!"
            )
        # First, choose player order by permuting self.players
        self.players = random.shuffle(self.players)
        # Begin game loop
        game_over = False
        while not game_over:
            game_over = self.play_round()
        
        # Display final scores
        
    def 


