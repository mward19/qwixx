from player import Player
from dice import DiceSet
from board import Board
from board import BoardState
from color import Color
import random
from qwixx_game import QwixxGame
import shutil
from utils import color_center
from utils import coord_to_A1
from utils import clear_terminal # TODO: rename "utils" as "termutils" or similar

class QwixxTerm(QwixxGame):
    """
    Runs a game of Qwixx in the terminal.
    """
    def __init__(self, names):
        """
        Initializes the Qwixx game using the players' names, default boards, and default dice.
        """
        players = [Player(name, Board()) for name in names]
        dice = DiceSet()
        super().__init__(players, dice)
    
    def display_player_order(self, player_order):
        text = "The player order will be:"
        for index, player in enumerate(player_order):
            text += f"\n\t{index+1}. {player.name}"
        print(text)

    def roll_dice(self):
        """
        Roll the dice. 
        """        
        self.dice.roll() 

    def display_dice(self):
        # Display dice
        terminal_size = shutil.get_terminal_size().columns
        output = ""
        for d in self.dice:
            output += self.show_die(d) + " "
        print(color_center(output, terminal_size))
    
    def display_white_dice(self):
        terminal_size = shutil.get_terminal_size().columns
        output = ""
        for d in self.dice:
            if d.color == Color.NO_COLOR:
                output += self.show_die(d) + " "
        print(color_center(output, terminal_size))
    
    def show_die(self, die):
        return Color.color_text(die.color, ":" + str(die.last_roll) + ":")
    
    def display_choices(self, choices):
        """
        Displays the choices listed in `choices`. If there are no choices, displays a message about penalties.
        Args:
            choices (list of (row, column) tuples) 
        """
        # TODO: fully implement. A1 list is not enough
        choices_A1 = [coord_to_A1(*c) for c in choices]
        print(", ".join(choices_A1))

    def white_choice(self, player):
        """
        Displays the white die options for `player`.
        Allows them to choose which option they will take.
        Returns:
            (bool) If the choice was successful
        """
        #TODO: make it allow pass if not your turn
        options = player.valid_white_options(self.dice)

        # Let the player make a move using A1 notation
        valid_choice = False
        while not valid_choice:
            self.display_choices(options)
            user_input = input("Choose your white move (submit \"-\" for penalty): ")
            if user_input.strip() == "-":
                valid_choice = True
                player.penalize()
            else:
                # TODO: Force this to only accept white choice (replace A1_mark)
                valid_choice = player.board.A1_mark(user_input.strip())

        return True
    
    def color_choice(self, player):
        """
        Displays the color die options for `player`.
        Allows them to choose which option they will take.
        Returns:
            (bool) If the choice was successful
        """
        options = player.valid_color_options(self.dice)

        # Let the player make a move using A1 notation
        valid_choice = False
        while not valid_choice:
            self.display_choices(options)
            user_input = input("Choose your colored move (submit \"-\" for penalty): ")
            if user_input.strip() == "-":
                valid_choice = True
                player.penalize()
            else:
                # TODO: Force this to only accept color choice (replace A1_mark)
                valid_choice = player.board.A1_mark(user_input.strip())

        return True
    
    def all_choice(self, player):
        """
        Displays all dice options for `player`, white first, then colored.
        Allows them to choose which option(s) they will take.
        If no option is chosen, invokes a penalty on the player.
        Returns:
            (bool) If the choice was successful
        """
        success_white = self.white_choice(player)
        success_color = self.color_choice(player)
        return success_white and success_color

    def display_all_options(self, player):
        """
        Displays all dice options for `player`, white first, then colored. Used on a player's turn, after a dice roll, but before other players have decided to use the white roll.
        """
        white_options = player.valid_white_options(self.dice)
        color_options = player.valid_color_options(self.dice)
        print("White: ", end="")
        self.display_choices(white_options)
        print("Colored: ", end="")
        self.display_choices(color_options)

    def display_board(self, player):
        """
        Displays a player's board. If desired, other player's boards may be displayed, but they would be displayed secondarily.
        """
        """
        Yields a colored representation for terminals using ANSI escape sequences.
        """
        board = player.board

        terminal_size = shutil.get_terminal_size().columns
        sq_width = 6 # TODO: make this arbitrary choice more robust
        max_row_len = max([len(row) for row in board.rows])
        lmargin = 3

        # Show player name
        print(color_center(f"~~~ {str(player.name)} ~~~", terminal_size))

        text= ""
        # A header, with numeric column coordinates.
        text_row = ' ' * lmargin
        text_row += ''.join([str(column).center(sq_width)
                         for column in range(1, max_row_len+1)])
        text_row = color_center(text_row, terminal_size)
        text += text_row + "\n"

        # The rows of the board.
        for row_index, row in enumerate(board.rows):
            text_row = ""
            # Index rows with letters, calculated with ASCII codes
            text_row += chr(65 + row_index).rjust(lmargin) 
            text_row += row.term_rep(sq_width)
            text_row = color_center(text_row, terminal_size)
            text += text_row + "\n"
        
        # Penalties. TODO: give board.penalties a get method
        text += f"Penalties: {board.penalties}".center(terminal_size)
        
        print(text)
    
    def display_boards(self):
        """
        Displays all players' boards, with equal priority.
        """
        for player in self.players:
            self.display_board(player)
            print()
    
    def display_podium(self):
        """
        Displays a podium with the players ranked by their score. Intended for use at the conclusion of the game.
        """
        # Display final scores. Sort scores in reverse order (1st is first)
        scored = [(p, p.board.score()) for p in self.players].sort(
            key=lambda x: x[1],
            reverse=True
        )
        print("~~~ PODIUM ~~~")
        # TODO: make ordinals more robust for support of larger arbitrary numbers
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

    def display_intro(self):
        """
        Displays an introduction to the Qwixx game.
        """
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


if __name__ == "__main__":
    game = QwixxTerm(["stick", "grass", "moss"])
    game.play_game()