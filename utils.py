import re
import os

def strikethrough_text(text):
    """ Yields text with strikethrough using ANSI escape sequence. """
    strike_prefix = "\033[9m"
    strike_suffix = "\033[0m"
    return strike_prefix + str(text) + strike_suffix

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
    letter = text[0]
    number = text[1:]
    if not number.isdigit(): 
        if number.isalpha(): raise ValueError("Cannot represent rows past 'Z'")
        else: raise ValueError(f"{number} is not a valid column index.")

    letter_index = ord(letter) - 65
    number_index = int(number) - 1
    return (letter_index, number_index)

def color_str_length(text):
    """ Returns the length of text after removing ANSI escape sequences. """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text_without_ansi = ansi_escape.sub('', text)
    return len(text_without_ansi)

def color_center(text, width, spacer=' '):
    """
    Centers text with a specified spacer at a given width, 
    using color_str_length to find string length.
    """
    # Calculate the padding on each side
    padding = (width - color_str_length(text)) // 2
    spacer_string = spacer * padding

    centered = f"{spacer_string}{text}{spacer_string}"
    # If the centering cannot be perfect, length will be one less than it should.
    if color_str_length(centered) == width:     return centered
    elif color_str_length(centered) == width-1: return centered + spacer
    else: raise(RuntimeError("Centering failed, system error"))

def clear_terminal():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Mac and Linux
        os.system('clear')