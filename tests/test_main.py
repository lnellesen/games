import pygame
import pytest
from src.main import Game

@pytest.fixture
def game():
    g = Game()
    yield g

def test_game_initialization(game):
    """Game initializes with window, font, and one player."""
    assert game.window is not None
    assert isinstance(game.players, pygame.sprite.Group)
    assert len(game.players) == 1

def test_add_new_player(game):
    """Adding new player increases sprite count."""
    initial_count = len(game.players)
    game.add_new_player()
    assert len(game.players) == initial_count + 1

def test_platform_size(game):
    """Platform dimensions match settings."""
    assert game.platform_rect.width == game.WINDOW_WIDTH - game.PLATFORM_DELTA
    assert game.platform_rect.height == game.PLATFORM_HEIGHT

def test_score_starts_at_zero(game):
    """Score should begin at SCORE_BEGIN."""
    assert game.score == game.SCORE_BEGIN
