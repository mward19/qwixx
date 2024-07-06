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
from utils import A1_to_coord
from utils import valid_A1
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
        lc = set()
        players = [Player(name, Board(lc)) for name in names]
        dice = DiceSet()
        super().__init__(players, dice, lc)
    
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
            if d.color not in self.locked_colors:
                output += self.show_die(d) + " "
        print(color_center(output, terminal_size))
    
    def display_white_dice(self):
        terminal_size = shutil.get_terminal_size().columns
        output = ""
        for d in self.dice:
            if d.color == Color.NO_COLOR:
                output += self.show_die(d) + " "
            elif d.color not in self.locked_colors:
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

    def choice_offturn(self, this_player, turn_player):
        """
        Displays the white die options for `player`.
        Allows them to choose which option they will take.
        Returns:
            (bool) If a square was marked (false if pass or penalty)
        """
        white_turn = True # Offturn is always white only.
        options = this_player.valid_options(self.dice, white_turn)

        # Let the player make a move using A1 notation
        valid_choice = False
        pass_turn = False
        while not valid_choice:
            message = "Choose your move (\"-\" to opt out): "
            user_input = input(message)
            if user_input.strip() == "-":
                valid_choice = True
                pass_turn = True
            elif this_player.valid_A1(user_input):
                r, c = A1_to_coord(user_input)
                if (r, c) in options:
                    pass_turn = False
                    valid_choice = True
                    mark_success = this_player.board.mark(r, c)
                    if not mark_success: raise RuntimeError("Turn validation failed!")
                else:
                    valid_choice = False
        return pass_turn
    
    def choice_onturn(self, this_player, white_turn=True):
        """
        Displays the white die options for `player`.
        Allows them to choose which option they will take.
        Returns:
            (bool) If a square was marked (false if pass or penalty)
        """
        options = this_player.valid_options(self.dice, white_turn)

        # Let the player make a move using A1 notation
        valid_choice = False
        pass_turn = False
        while not valid_choice:
            message = None
            if white_turn:
                message = "Choose your white move (\"-\" to opt out): "
            else:
                message = "Choose your color move (\"-\" to opt out): "
            user_input = input(message)
            if user_input.strip() == "-":
                valid_choice = True
                pass_turn = True
            elif this_player.valid_A1(user_input):
                r, c = A1_to_coord(user_input)
                if (r, c) in options:
                    pass_turn = False
                    valid_choice = True
                    mark_success = this_player.board.mark(r, c)
                    if not mark_success: raise RuntimeError("Turn validation failed!")
                else:

                    valid_choice = False
        return pass_turn

    def penalize(self, player):
        player.penalize()
        self.display_penalize(player)

    def update_lock(self):
        for p in self.players:
            p.board.update_lock()
        return None

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
        
        # Penalties.
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
        terminal_size = shutil.get_terminal_size().columns
        # Display final scores. Sort scores in reverse order (1st is first)
        scored = [(p, p.board.score()) for p in self.players]
        scored.sort(key=lambda x: x[1], reverse=True)
        print(ansi_center("~~~ PODIUM ~~~", terminal_size))
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
        # TODO: allow ties
        place = 1
        print(ansi_center(f"Congratulations, {bold(scored[0][0].name)}!", terminal_size))
        for (player, score) in scored:
            score_statement = (f"{ordinals[place]} place: "
                               f"{bold(player.name)} with a score of {bold(score)}.")
            print(score_statement)
            place += 1

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
        # Update locking
        self.update_lock()

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
                terminal_size = shutil.get_terminal_size().columns
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
                    self.choice_offturn(other_p, p)
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
                self.display_white_dice()
                pass_white = self.choice_onturn(p, True)
                
                self.display_board(p) # Update board
                self.display_dice()
                pass_color = self.choice_onturn(p, False)
                if pass_white and pass_color: self.penalize(p)

                # Update locking
                self.update_lock()

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

    ## Almost finished game
    #game.players[0].board.mark(0, 0)
    #game.players[0].board.mark(0, 1)
    #game.players[0].board.mark(0, 2)
    #game.players[0].board.mark(0, 3)
    #game.players[0].board.mark(0, 4)
    #game.players[0].board.mark(0, 5)
    #game.players[0].board.mark(0, 10)
    #
    #game.players[0].board.mark(2, 0)
    #game.players[0].board.mark(2, 1)
    #game.players[0].board.mark(2, 2)
    #game.players[0].board.mark(2, 3)
    #game.players[0].board.mark(2, 4)
    #
    #game.players[0].board.mark(3, 0)
    #game.players[0].board.mark(3, 1)
    #game.players[0].board.mark(3, 2)
    #game.players[0].board.mark(3, 3)
    #game.players[0].board.mark(3, 4)
    #
    #game.players[0].board.mark(1, 0)
    #game.players[0].board.mark(1, 1)
    #game.players[0].board.mark(1, 2)
    #game.players[0].board.mark(1, 3)
    #game.players[0].board.mark(1, 4)

    game.play_game()