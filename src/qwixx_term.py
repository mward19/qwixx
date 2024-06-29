from player import Player
from dice import DiceSet
from board import Board
from board import BoardState
from color import Color
import random
from qwixx_game import QwixxGame
import shutil
from utils import color_center
from utils import ansi_center
from utils import strikethrough
from utils import bold
from utils import coord_to_A1
from utils import clear_terminal # TODO: rename "utils" as "termutils" or similar
import time

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
            else:
                output += strikethrough(self.show_die(d)) + " "
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

    def white_choice_offturn(self, this_player, turn_player):
        """
        Displays the white die options for `player`.
        Allows them to choose which option they will take.
        Returns:
            (bool) If a square was marked (false if pass or penalty)
        """
        options = this_player.valid_white_options(self.dice)

        # Let the player make a move using A1 notation
        valid_choice = False
        pass_turn = False
        while not valid_choice:
            #self.display_choices(options) # TODO: I think this is distracting
            message = "Choose your move (\"-\" to opt out): "
            user_input = input(message)
            if user_input.strip() == "-":
                valid_choice = True
                pass_turn = True
            else:
                # TODO: Force this to only accept white choice (replace A1_mark)
                valid_choice = this_player.board.A1_mark(user_input.strip())

        return pass_turn
    
    def white_choice_turn(self, player):
        """
        Displays the white die options for `player`.
        Allows them to choose which option they will take.
        Returns:
            (bool) If a square was marked (false if pass or penalty)
        """
        options = player.valid_white_options(self.dice)

        # Let the player make a move using A1 notation
        valid_choice = False
        pass_turn = False
        while not valid_choice:
            #self.display_choices(options) # TODO: I think this is distracting
            message = "Choose your white move (\"-\" to opt out): "
            user_input = input(message)
            if user_input.strip() == "-":
                valid_choice = True
                pass_turn = True
            else:
                # TODO: Force this to only accept white choice (replace A1_mark)
                valid_choice = player.board.A1_mark(user_input.strip())

        return pass_turn
    
    # TODO: fix character length so that white and colored moves have same width
    def color_choice_turn(self, player):
        """
        Displays the color die options for `player`.
        Allows them to choose which option they will take.
        Returns:
            (bool) If a square was marked (false if pass or penalty)
        """
        options = player.valid_color_options(self.dice)

        # Let the player make a move using A1 notation
        valid_choice = False
        pass_turn = False
        while not valid_choice:
            #self.display_choices(options) # TODO: I think this is distracting
            message = "Choose your colored move (\"-\" to opt out): "
            user_input = input(message)
            if user_input.strip() == "-":
                valid_choice = True
                pass_turn = True
            else:
                # TODO: Force this to only accept white choice (replace A1_mark)
                valid_choice = player.board.A1_mark(user_input.strip())

        return pass_turn
    
    def all_choice(self, player):
        """
        Displays all dice options for `player`, white first, then colored.
        Allows them to choose which option(s) they will take.
        If no option is chosen, invokes a penalty on the player.
        Returns:
            (bool) If a penalty was taken
        """
        pass_white = self.white_choice_turn(player) #TODO: display updated board
        pass_color = self.color_choice_turn(player)
        penalize = pass_white and pass_color
        if penalize: self.penalize(player)
        return penalize
    
    def penalize(self, player):
        player.penalize()
        self.display_penalize(player)

    def display_penalize(self, player):
        terminal_size = shutil.get_terminal_size().columns
        print(f"{player.name} took a penalty!".center(terminal_size))

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
        clear_terminal()
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

    def play_game(self, player_order=None):
        terminal_size = shutil.get_terminal_size().columns
        self.display_intro()
        time.sleep(1)

        # If no player_order is provided, use a random order
        if player_order == None:
            player_order = random.sample(self.players, len(self.players))
        
        self.display_player_order(player_order)
        time.sleep(1)
        input("Press enter to continue.".center(terminal_size))

        # TODO: implement mutiplayer locking with boardstates
        # Begin turns
        state = BoardState.CONTINUE
        while True:
            for p_index, p in enumerate(player_order):
                clear_terminal()
                print(ansi_center(f"{bold(p.name)}, it is your turn.", terminal_size))
                time.sleep(0.5)
                self.display_board(p)
                time.sleep(0.5)
                self.roll_dice()
                self.display_dice() # Let this player see the roll they made
                time.sleep(0.5)

                # Let other players use white roll
                other_players = self.get_other_players(player_order, p, p_index)
                print(ansi_center(
                    (f"{bold(p.name)}, wait as other players "
                    "decide if they will use the white roll."), terminal_size)
                )
                input("Press enter to continue.".center(terminal_size))
                for other_p in other_players:
                    clear_terminal()
                    print(ansi_center(
                        (f"{bold(other_p.name)}, choose how/if you will "
                        "use the white roll."), terminal_size)
                    )
                    self.display_board(other_p)
                    self.display_white_dice()
                    self.white_choice_offturn(other_p, p)
                    time.sleep(0.5)

                    # Possible game end point
                    state = other_p.board.get_state()
                    if state != BoardState.CONTINUE:
                        break

                # Possible game end point
                if state != BoardState.CONTINUE:
                    break

                # Let this player use roll
                clear_terminal()
                print(ansi_center(
                    (f"{bold(p.name)}, you may now decide how "
                    "you will use your roll."), terminal_size)
                )
                time.sleep(0.5)
                self.display_board(p)
                self.display_dice()
                pass_white = self.white_choice_turn(p)
                self.display_board(p) # Update board
                self.display_dice()
                pass_color = self.color_choice_turn(p)
                if pass_white and pass_color: self.penalize(p)

                # Display updated board
                self.display_board(p)
                time.sleep(1)

                # Possible game end point
                state = p.board.get_state()
                if state != BoardState.CONTINUE:
                    break

                input("Press enter to continue.".center(terminal_size))
            
            # Possible game end point
            if state != BoardState.CONTINUE:
                break
            
        # Show final boards
        self.display_boards()
        # Show final scores
        self.display_podium()
    


if __name__ == "__main__":
    game = QwixxTerm(["stick", "grass"])
    game.play_game()