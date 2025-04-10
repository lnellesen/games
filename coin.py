import pygame

class Coin:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.is_destroyed = False

    def update(self):
        self.draw()
        if self.rect.colliderect(self.game.player.rect):
            self.is_destroyed = True

    def draw(self):
        pygame.draw.rect(self.game.window, "yellow", self.rect)