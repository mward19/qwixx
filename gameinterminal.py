from player import Player
from dice import DiceSet
from board import Board
from color import Color
import random

class GameInTerminal:
    def __init__(self, players):
        if len(players) > 8:
            raise(ValueError("More than 8 players is not supported"))
        self.players = players
        self.dice = DiceSet()
    
    def __init__(self, names):
        if len(names) > 8:
            raise(ValueError("More than 8 players is not supported"))
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
        while True:
            game_over = False
            for player in self.players:
                game_over = player.terminal_turn()
                if game_over: break
            if game_over: break
        
        # Display final scores. Sort scores in reverse order (1st is first)
        scored = [(p, p.board.score()) for p in self.players].sort(
            key=lambda x: x[1],
            reverse=True
        )
        print("~~~ PODIUM ~~~")
        ordinals = {
            1: "1st", 
            2: "2nd", 
            3: "3rd", 
            4: "4th", 
            5: "5th", 
            6: "6th", 
            7: "7th", 
            8: "8th"
        }
        place = 1
        print(f"Congratulations, {scored[0][0].name}!")
        for (player, score) in enumerate(scored):
            print(f"{ordinals[place+1]} place:
                  {player.name} with {score} point(s).")
        


