"""
testing stop falling as an example test (jon hat gesagt das reicht :))
"""

from src.main import Game
from src.player import Player


def test_stop_falling():

    test_game = Game()
    player = Player(test_game, 1)

    assert not player.on_ground
    assert not player._falling

    player._stop_falling()

    assert player.on_ground
    assert not player._falling, "after calling stop falling _falling should be False"
