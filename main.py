"""Run/starts game."""

import pygame
import player
import random


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
            "watermelone_upgrade.jpeg": 64,
            "dragonfruit_upgrade.jpeg": 60,
            "orange_upgrade.jpeg": 52,
            "apple_upgrade.jpeg": 56,
            "lemon_upgrade.jpeg": 48,
            "kiwi_upgrade.jpeg": 44,
            "strawberry_upgrade.jpeg": 40,
            "raspberry_upgrade.jpeg": 36,
            "cherry_upgrade.jpeg": 32,
            "blueberry_upgrade.jpeg": 28,
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
