import re
import os

def strikethrough(text):
    """ Yields text with strikethrough using ANSI escape sequence. """
    strike_prefix = "\033[9m"
    strike_suffix = "\033[0m"
    return strike_prefix + str(text) + strike_suffix

def bold(text):
    """ Yields bold text using ANSI escape sequence. """
    bold_prefix = "\033[1m"
    bold_suffix = "\033[0m"
    return bold_prefix + str(text) + bold_suffix

def valid_A1(text, N_rows, N_cols):
    """ Checks if `text` is a valid A1 style coordinate."""
    pattern = r"^[A-Za-z]\d+$"
    text = text.strip()
    if not re.match(pattern, text):
        return False
    
    coords = A1_to_coord(text)
    if coords[0] >= N_rows or coords[1] >= N_cols:
        return False

    return True

def coord_to_A1(row, column):
    """
    Returns (row, column) as 'A1' coordinates.
    `A` is row 0, `1` is column 0. Thus row 4, column 3 would be 'E4'.
    """
    if row >= 26: raise ValueError("Cannot represent rows past 'Z'")
    return chr(65 + row) + str(column+1)

def A1_to_coord(text):
    """
    Returns A1' coordinates as (row, column).
    `A` is row 0, `1` is column 0. Thus 'E4' would be row 4, column 3.
    """
    letter = text[0].upper()
    number = text[1:]
    if not number.isdigit(): 
        if number.isalpha(): raise ValueError("Cannot represent rows past 'Z'")
        else: raise ValueError(f"{number} is not a valid column index.")

    letter_index = ord(letter) - 65
    number_index = int(number) - 1
    return (letter_index, number_index)

def ansi_str_length(text):
    """ Returns the length of text after removing ANSI escape sequences. """
    # Regular expression to match ANSI escape sequences
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    # Remove ANSI escape sequences
    text_without_ansi = ansi_escape.sub('', text)
    # Return the length of the cleaned text
    return len(text_without_ansi)

def ansi_center(text, width, spacer=' '):
    """
    Centers text with a specified spacer at a given width, 
    using ansi_str_length to find string length.
    """
    # Calculate the padding on each side
    padding = (width - ansi_str_length(text)) // 2
    spacer_string = spacer * padding

    centered = f"{spacer_string}{text}{spacer_string}"
    # If the centering cannot be perfect, length will be one less than it should.
    if ansi_str_length(centered) == width:     return centered
    elif ansi_str_length(centered) == width-1: return centered + spacer
    else: raise(RuntimeError("Centering failed, system error"))

def clear_terminal():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Mac and Linux
        os.system('clear')