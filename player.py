import pygame


class Player:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game
        self.surface = game.window
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.height = 64
        self.width = 64
        self.fall_velocity = 200 # fall velocity
        self.on_ground = False # check if player is on the ground
        self.falling = False


    def update(self):
        self.rect = pygame.Rect(self.x, self.y, 64, 64)
        self.movement(speed=100)
        self.draw()
    
    def draw(self):
        pygame.draw.rect(self.surface, "red", (self.x, self.y, 64, 64))


    def movement(self, speed):
        keys = pygame.key.get_pressed()

        if not self.on_ground and not self.falling: # no horizontal movement while player is falling
            if keys[pygame.K_RIGHT]:
                self.x += speed * self.game.delta_time # movement in pixel per second
                if self.x > self.game.screen_width - self.width: # right border for rectangle
                    self.x = self.game.screen_width - self.width

            elif keys[pygame.K_LEFT]:
                self.x -= speed * self.game.delta_time
                if self.x < 0: # left border for rectangle
                    self.x = 0

        if keys[pygame.K_DOWN] and not self.on_ground and not self.falling:
            self.falling = True
        if not self.on_ground and self.falling:
            self.y += self.fall_velocity * self.game.delta_time

            # Check for collision with other players
            for other in self.game.players:
                if other is self:
                    continue
                if self._is_falling_on_top_of(other):
                    self.y = other.y - self.height
                    self.on_ground = True
                    self.falling = False
                    return

            # Check collision with the ground
            if self.y >= self.game.screen_height - self.height:
                self.y = self.game.screen_height - self.height
                self.on_ground = True
                self.falling = False


    def _is_falling_on_top_of(self, other):
        # Check if this player is falling onto another player
        horizontally_aligned = (
            self.x + self.width > other.x and
            self.x < other.x + other.width
        )
        vertically_touching = (
            self.y + self.height >= other.y and
            self.y + self.height - self.fall_velocity * self.game.delta_time < other.y
        )
        return horizontally_aligned and vertically_touching