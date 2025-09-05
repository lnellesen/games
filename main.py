"""Run/starts game."""
import pygame
import player
import random
from fruits import LIST_PLAYERS


class Game:
    def __init__(self):
        """Init of the game class."""
        pygame.init()
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 600
        self.platform_width = self.WINDOW_WIDTH - 300
        self.platform_height = 20
        self.platform_x = (self.WINDOW_WIDTH - self.platform_width) // 2
        self.platform_y = self.WINDOW_HEIGHT - self.platform_height
        self.platform_rect = pygame.Rect(self.platform_x, self.platform_y, self.platform_width, self.platform_height)
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("fruit merge")
        self.clock = pygame.time.Clock()
        self.screen_height = self.window.get_height()
        self.screen_width = self.window.get_width()
        self._running = True
        self.delta_time = 1000 # how should this be initilized?

        self.player_forms = {
            LIST_PLAYERS[0]: 278,
            LIST_PLAYERS[1]: 272,
            LIST_PLAYERS[2]: 241,
            LIST_PLAYERS[3]: 234,
            LIST_PLAYERS[4]: 210,
            LIST_PLAYERS[5]: 173,
            LIST_PLAYERS[6]: 149,
            LIST_PLAYERS[7]: 126,
            LIST_PLAYERS[8]: 109,
            LIST_PLAYERS[9]: 79,
        }

        self.players = pygame.sprite.Group()

        self.add_new_player()

        self.run()

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
            self.delta_time = self.clock.tick(60) / 900
            self.window.fill((25, 25, 25))

            self.players.update()
            self.players.draw(self.window)
            pygame.draw.rect(self.window, (50, 50, 50), self.platform_rect)
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.window.blit(score_text, (10, 10))

            if not self.players or all(p.on_ground for p in self.players):
                self.add_new_player()


            pygame.display.update()

    pygame.quit()

    def add_new_player(self):
        """Add a new player."""
        fruits, size = random.choice(list(self.player_forms.items())[6:])
        new_player = player.Player(self, 300, 32, fruits=fruits, SIZE=size)
        self.players.add(new_player)

if __name__ == "__main__":
    game = Game()
