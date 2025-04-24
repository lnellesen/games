
import pygame
import player
import random



class Game:
    def __init__(self):
        pygame.init()
        self.window_width = 800
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("coins")
        self.clock = pygame.time.Clock()
        self.screen_height = self.window.get_height()
        self.screen_width = self.window.get_width()

        self.players = [player.Player(self, 300, 32)]
        self.player_forms = {
                            'red': 64, 'yellow': 60, 'green': 56, 'orange': 52, 'blue': 48,
                            'pink': 44, 'gray': 40, 'salmon': 36, 'purple': 32, 'darkblue': 28
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

            if self.players[-1].on_ground: # if last player on the ground add a new player
                self.add_new_player()


            pygame.display.update()

    pygame.quit()

    # function to add new player with randomly selected color and size
    def add_new_player(self): 
        color, size = random.choice(list(self.player_forms.items()))
        self.players.append(player.Player(self, 300, 32, color=color, size=size))

game = Game()
