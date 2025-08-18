import pygame
import random

from fruits import LIST_PLAYERS, reshape_player


class Player(pygame.sprite.Sprite):
    """Class to store and define parameters for each player."""
    def __init__(self, game, x=300, y=32, color=random.choice(LIST_PLAYERS), size=64):
        super().__init__()
        self.game = game
        self.file = color
        self.height = size
        self.width = size
        self.image = reshape_player(self.file)
        self.surface = game.window
        self.rect = self.image.get_rect(topleft=(x, y))
        self.fall_velocity = 200 # fall velocity
        self.on_ground = False # check if player is on the ground
        self.falling = False


    def update(self):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if not self.on_ground and not self.falling:
            if keys[pygame.K_RIGHT]:
                self.rect.x += 100 * self.game.delta_time
                if self.rect.right > self.game.screen_width:
                    self.rect.right = self.game.screen_width
            elif keys[pygame.K_LEFT]:
                self.rect.x -= 100 * self.game.delta_time
                if self.rect.left < 0:
                    self.rect.left = 0

        # Start falling
        if keys[pygame.K_DOWN] and not self.on_ground and not self.falling:
            self.falling = True

        # Falling
        if not self.on_ground and self.falling:
            self.rect.y += self.fall_velocity * self.game.delta_time

            colliding = pygame.sprite.spritecollide(self, self.game.players, False)
            for other in colliding:
                if other is self:
                    continue
                # Only handle if falling on top
                if self.rect.bottom <= other.rect.top + 5:
                    self.handle_collision(other)

            # Collision with the ground
            if self.rect.bottom >= self.game.screen_height:
                self.rect.bottom = self.game.screen_height
                self.on_ground = True
                self.falling = False



    def handle_collision(self, other):
        form_keys = list(self.game.player_forms.keys())

        if self.file == other.file and form_keys.index(self.file) > 0:
            self.merge_with(other)
        else:
            # stop falling on top of another player
            self.rect.bottom = other.rect.top
            self.on_ground = True
            self.falling = False

    def check_chain_merge(self):
        collided = pygame.sprite.spritecollide(self, self.game.players, False)
        for other in collided:
            if other is self:
                continue
            # only merge if same color and size
            if other.file == self.file and other.rect.size == self.rect.size:
                self.merge_with(other)
                break  # only merge one at a time and then re-check

    def merge_with(self, other):
        form_keys = list(self.game.player_forms.keys())
        self.kill()
        other.kill()
        new_color = form_keys[form_keys.index(self.file) - 1]
        new_size = self.game.player_forms[new_color]
        # vertical position of new player on top of player below and horizontally centered around other player
        new_x = other.rect.x + (self.height - new_size) / 2
        new_y = other.rect.y + (self.height - new_size)

        merged = Player(self.game, new_x, new_y, color=new_color, size=new_size)
        merged.on_ground = True
        self.game.players.add(merged)

        merged.check_chain_merge()

        if new_color == LIST_PLAYERS[0]:
            pygame.init()
            font = pygame.font.Font(None, 74)
            text = font.render("YOU WON!", True, (255, 255, 255))
            self.surface.blit(text, (300, 250))
            pygame.display.flip()
            pygame.time.delay(100000)
            pygame.quit()
