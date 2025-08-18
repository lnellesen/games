"""Run/starts game."""

import pygame
import player
import random
from fruits import reshape_player, LIST_PLAYERS


class Game:
    def __init__(self):
        pygame.init()
        self.window_width = 1000
        self.window_height = 800
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("fruit merge")
        self.clock = pygame.time.Clock()
        self.screen_height = self.window.get_height()
        self.screen_width = self.window.get_width()

        # list of all players in the game - it gets extended whenever a new player is added
        self.players = [player.Player(self)]
        self.player_forms = {
            LIST_PLAYERS[9]: 64,
            LIST_PLAYERS[8]: 60,
            LIST_PLAYERS[7]: 52,
            LIST_PLAYERS[6]: 56,
            LIST_PLAYERS[5]: 48,
            LIST_PLAYERS[4]: 44,
            LIST_PLAYERS[3]: 40,
            LIST_PLAYERS[2]: 36,
            LIST_PLAYERS[1]: 32,
            LIST_PLAYERS[0]: 28,
        }

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

            for p in self.players:
                p.update()

            if self.players[-1].on_ground:
                self.add_new_player()

            pygame.display.update()

    pygame.quit()

    # function to add new player with randomly selected color and size
    def add_new_player(self):
        file, size = random.choice(list(self.player_forms.items()))
        self.players.append(player.Player(self, 300, 32, file=file, size=size))


game = Game()
