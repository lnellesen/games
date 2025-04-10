
import pygame
import player
# import coin



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

        self.player = player.Player(self, 32, 32)

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
            self.player.update()







            pygame.display.update()

    pygame.quit()


game = Game()
