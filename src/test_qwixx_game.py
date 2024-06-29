import pytest
from qwixx_game import QwixxGame
from quixx_term import QwixxTerm

def test_get_other_players():
    names = ["one", "two", "three"]
    game = QwixxTerm(names)
    player_order = game.players
    this_player = player_order[1]
    others = game.get_other_players(player_order, this_player)
    assert len(others) == len(names) - 1
    assert others[-1] == player_order[0]

    names = ["one", "two", "three"]
    game = QwixxTerm(names)
    player_order = game.players
    this_player = player_order[0]
    others = game.get_other_players(player_order, this_player)
    assert len(others) == len(names) - 1
    assert others[-1] == player_order[-1]

    names = ["one", "two"]
    game = QwixxTerm(names)
    player_order = game.players
    this_player = player_order[1]
    others = game.get_other_players(player_order, this_player)
    assert len(others) == len(names) - 1
    assert others[-1] == player_order[0]