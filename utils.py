def strikethrough_text(text):
    """ Yields text with strikethrough using ANSI escape sequence. """
    strike_prefix = "\033[9m"
    strike_suffix = "\033[0m"
    return strike_prefix + str(text) + strike_suffix