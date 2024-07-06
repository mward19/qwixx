import re
import os

def strikethrough(text):
    """ 
    Yields text with strikethrough formatting using ANSI escape sequences.

    Parameters:
    text (str): The input text to be formatted with a strikethrough.

    Returns:
    str: The input text with ANSI escape sequences applied for strikethrough formatting.
    """
    strike_prefix = "\033[9m"
    strike_suffix = "\033[0m"
    return strike_prefix + str(text) + strike_suffix

def bold(text):
    """ 
    Yields bold text using ANSI escape sequences.

    Parameters:
    text (str): The input text to be formatted in bold.

    Returns:
    str: The input text with ANSI escape sequences applied for bold formatting.
    """
    bold_prefix = "\033[1m"
    bold_suffix = "\033[0m"
    return bold_prefix + str(text) + bold_suffix

def valid_A1(text, N_rows, N_cols):
    """ 
    Checks if the provided text is a valid A1 style coordinate.

    Parameters:
    text (str): The input text to be validated as an A1 coordinate.
    N_rows (int): The number of rows in the grid.
    N_cols (int): The number of columns in the grid.

    Returns:
    bool: True if the input text is a valid A1 coordinate within the grid bounds, False otherwise.
    """
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
    Converts row and column indices to A1 style coordinates.

    Parameters:
    row (int): The row index (0-based).
    column (int): The column index (0-based).

    Returns:
    str: The corresponding A1 style coordinate.

    Raises:
    ValueError: If the row index is greater than or equal to 26.
    """
    if row >= 26:
        raise ValueError("Cannot represent rows past 'Z'")
    return chr(65 + row) + str(column + 1)

def A1_to_coord(text):
    """
    Converts A1 style coordinates to row and column indices.

    Parameters:
    text (str): The A1 style coordinate to be converted.

    Returns:
    tuple: A tuple (row, column) representing the 0-based indices.

    Raises:
    ValueError: If the text contains invalid characters or represents rows past 'Z'.
    """
    letter = text[0].upper()
    number = text[1:]
    if not number.isdigit():
        if number.isalpha():
            raise ValueError("Cannot represent rows past 'Z'")
        else:
            raise ValueError(f"{number} is not a valid column index.")

    letter_index = ord(letter) - 65
    number_index = int(number) - 1
    return (letter_index, number_index)

def ansi_str_length(text):
    """ 
    Returns the length of text after removing ANSI escape sequences.

    Parameters:
    text (str): The input text potentially containing ANSI escape sequences.

    Returns:
    int: The length of the text without ANSI escape sequences.
    """
    # Regular expression to match ANSI escape sequences
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    # Remove ANSI escape sequences
    text_without_ansi = ansi_escape.sub('', text)
    # Return the length of the cleaned text
    return len(text_without_ansi)

def ansi_center(text, width, spacer=' '):
    """
    Centers text within a specified width, accounting for ANSI escape sequences.

    Parameters:
    text (str): The input text to be centered.
    width (int): The total width to center the text within.
    spacer (str): The character to use for padding on either side. Default is a space.

    Returns:
    str: The centered text with appropriate padding.

    Raises:
    RuntimeError: If the centering calculation fails.
    """
    # Calculate the padding on each side
    padding = (width - ansi_str_length(text)) // 2
    spacer_string = spacer * padding

    centered = f"{spacer_string}{text}{spacer_string}"
    # If the centering cannot be perfect, length will be one less than it should.
    if ansi_str_length(centered) == width:
        return centered
    elif ansi_str_length(centered) == width - 1:
        return centered + spacer
    else:
        raise(RuntimeError("Centering failed, system error"))

def clear_terminal():
    """
    Clears the terminal screen.

    Works on both Windows and Unix-like systems.
    """
    # Check the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Mac and Linux
        os.system('clear')
