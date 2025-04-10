
import pygame
import player
import coin



class Game:
    def __init__(self):
        pygame.init()
        self.window_width = 800
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("coins")
        self.clock = pygame.time.Clock()

        self.player = player.Player(self, 32, 32)
        self.coins = [coin.Coin(self, 150, 150),
                      coin.Coin(self, 250, 150),
                      coin.Coin(self, 350, 350)]
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

            for coin in self.coins:
                coin.update()
                if coin.is_destroyed:
                    self.coins.remove(coin)





            pygame.display.update()

    pygame.quit()


game = Game()
