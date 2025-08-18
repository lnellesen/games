"""Run/starts game."""
import pygame
import player
import random



class Game:
    def __init__(self):
        pygame.init()
        self.window_width = 400
        self.window_height = 300
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("fruit merge")
        self.clock = pygame.time.Clock()
        self.screen_height = self.window.get_height()
        self.screen_width = self.window.get_width()

        self.player_forms = {'red': 64, 'yellow': 60, 'green': 56, 'orange': 52, 'blue': 48,
                             'pink': 44, 'gray': 40, 'salmon': 36, 'purple': 32, 'darkblue': 28}

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
        color, size = random.choice(list(self.player_forms.items())[5:])
        p = player.Player(self, 300, 32, file=color, size=size)
        self.players.add(p)

game = Game()
