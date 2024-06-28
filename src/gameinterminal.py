### DEPRECATED ###

from player import Player
from dice import DiceSet
from board import Board
from board import BoardState
from color import Color
import random
import time
import shutil
from utils import color_center
from utils import clear_terminal

class GameInTerminal:
    def __init__(self, names):
        if len(names) > 8:
            raise(ValueError("More than 8 players is not supported"))
        self.players = [Player(name, Board()) for name in names]
        self.dice = DiceSet()

    def play(self):
        terminal_size = shutil.get_terminal_size().columns
        clear_terminal()
        print(color_center("Welcome to " +
              Color.color_text(Color.RED, 'Q') +
              Color.color_text(Color.YELLOW, 'W') +
              Color.color_text(Color.NO_COLOR, 'I') +
              Color.color_text(Color.GREEN, 'X') +
              Color.color_text(Color.BLUE, 'X') +
              "!",
            terminal_size)
        )
        time.sleep(1)

        # First, shuffle player order
        random.shuffle(self.players)
        # Begin game loop
        while True:
            state = BoardState.CONTINUE
            for player in self.players:
                state = player.terminal_turn(self.dice)
                if state != BoardState.CONTINUE: break
            #TODO: IMPLEMENT MULTIPLAYER LOCKING WITH BOARDSTATE
            if state != BoardState.CONTINUE: break
        
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
            score_statement = (f"{ordinals[place+1]} place:"
                               f"{player.name} with {score} point(s).")
            print(score_statement)
            
if __name__ == "__main__":
    #names = [f"Player {i}" for i in range(1, 4)]
    names = ["sticc", "grass"]
    game = GameInTerminal(names)
    game.play()
        


