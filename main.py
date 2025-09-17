"""Setup and start of the game."""

import pygame
import player
import random
from player_configuration import LIST_PLAYER_FILES


class Game:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    PLATFORM_DELTA = 300
    PLATFORM_HEIGHT = 20
    SCORE_BEGIN = 0
    POSITION_SCORE = (10, 10)
    POSITION_FINAL_SCORE = (300, 350)
    POSITION_FINISH = (300, 250)
    TEXT_SIZE_SCORE = 36
    TEXT_SIZE_FINAL_SCORE = 48
    TEXT_SIZE_FINISH = 74
    FRAME_RATE = 900
    GREY = (25, 25, 25)
    DARK_GREY = (50, 50, 50)
    WHITE = (255, 255, 255)
    START_X = 500
    START_Y = 32
    APPEARING_PLAYERS = 6
    GAME_OVER_HIGHT = 100
    WINNING_PLAYER = 7
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 60
    BUTTON_COLOR = (0, 128, 0)
    # The list of player is very constant, if you wish to change the list of files/players, you need to file a complaint
    # with the CEOs of Fruit Merge 2.0. Therefore, this is hardcoded.
    PLAYER_FORMS = {
        LIST_PLAYER_FILES[0]: 278,
        LIST_PLAYER_FILES[1]: 272,
        LIST_PLAYER_FILES[2]: 241,
        LIST_PLAYER_FILES[3]: 234,
        LIST_PLAYER_FILES[4]: 210,
        LIST_PLAYER_FILES[5]: 173,
        LIST_PLAYER_FILES[6]: 149,
        LIST_PLAYER_FILES[7]: 126,
        LIST_PLAYER_FILES[8]: 109,
        LIST_PLAYER_FILES[9]: 79,
    }
    def __init__(self):
        """
        Init of the game class.
        """
        pygame.init()
        self.platform_width = Game.WINDOW_WIDTH - Game.PLATFORM_DELTA
        self.platform_x = (Game.WINDOW_WIDTH - self.platform_width) // 2
        self.platform_y = Game.WINDOW_HEIGHT - Game.PLATFORM_HEIGHT
        self.platform_rect = pygame.Rect(self.platform_x, self.platform_y, self.platform_width, self.PLATFORM_HEIGHT)
        self.score = Game.SCORE_BEGIN
        self.font = pygame.font.Font(None, Game.TEXT_SIZE_SCORE)
        self.window = pygame.display.set_mode((Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))
        pygame.display.set_caption("fruit merge")
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(60) / Game.FRAME_RATE
        self.screen_height = self.window.get_height()
        self.screen_width = self.window.get_width()
        self._running = True
        self.players = pygame.sprite.Group()
        self.add_new_player()
        # self.run()

    def shall_run(self):
        """Return whether the game should continue running."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running  = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running  = False
        return self._running



    def run(self):
        """Run the game."""
        while self.shall_run():
            # need to be initialized again while running
            self.delta_time = self.clock.tick(60) / Game.FRAME_RATE
            self.window.fill(Game.GREY)
            self.players.update()
            self.players.draw(self.window)
            pygame.draw.rect(self.window, Game.DARK_GREY, self.platform_rect)
            score_text = self.font.render(f"Score: {self.score}", True, Game.WHITE)
            # position of score box
            self.window.blit(score_text, Game.POSITION_SCORE)

            if not self.players or all(p.on_ground for p in self.players):
                self.add_new_player()

            pygame.display.update()

    pygame.quit()

    def add_new_player(self):
        """Add a new player as a fruit."""
        fruit, size = random.choice(list(Game.PLAYER_FORMS.items())[Game.APPEARING_PLAYERS:])
        new_player = player.Player(self, size=size,x=Game.START_X, y=Game.START_Y, fruit=fruit)
        self.players.add(new_player) #Todo: should be a sprites


if __name__ == "__main__":
    game = Game()
    game.run()
