"""
creates a fake window and fake images and should run before very test
"""

import os
import pygame
import pytest
from unittest.mock import patch
import numpy as np

@pytest.fixture(scope="session", autouse=True)
def pygame_headless():
    """Run pygame in headless mode for all tests."""
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.display.init()
    yield
    pygame.display.quit()

@pytest.fixture(autouse=True)
def mock_imread():
    """Mock image loading so tests don't require actual image files."""
    with patch("matplotlib.pyplot.imread") as fake_imread:
        # return a dummy numpy array when imread is called
        fake_imread.return_value = np.zeros((10, 10, 3), dtype=np.uint8)
        yield