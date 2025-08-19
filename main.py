"""Run/starts game."""
import pygame
import player
import random
from fruits import LIST_PLAYERS


class Game:
    def __init__(self):
        pygame.init()
        self.window_width = 1000
        self.window_height = 700
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("fruit merge")
        self.clock = pygame.time.Clock()
        self.screen_height = self.window.get_height()
        self.screen_width = self.window.get_width()

        # list of all players in the game - it gets extended whenever a new player is added
        self.players = [player.Player(self)]
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

        self.add_new_player(first=True)

        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            
            self.delta_time = self.clock.tick(60) / 1000
            self.window.fill((25, 25, 25))

            self.players.update()
            self.players.draw(self.window)

            last = list(self.players)[-1]
            if last.on_ground:
                self.add_new_player()


            pygame.display.update()

    pygame.quit()

    # function to add new player with randomly selected color and size
    def add_new_player(self, first=False):
        fruits, size = random.choice(list(self.player_forms.items())[7:])
        p = player.Player(self, 300, 32, fruits=fruits, size=size)
        self.players.add(p)

game = Game()
