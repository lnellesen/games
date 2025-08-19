import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x=300, y=32, file='darkblue', size=64):
        super().__init__()
        self.game = game
        self.file = file
        self.surface = game.window
        self.height = size
        self.width = size
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.file)
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

            self.apply_gravity()



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
        def vertically_touching_or_colliding(sprite, group):
            result = []
            for other in group:
                if other is sprite:
                    continue
                if sprite.rect.colliderect(other.rect):
                    result.append(other)
                    continue
                vertical_touch = sprite.rect.bottom == other.rect.top or sprite.rect.top == other.rect.bottom
                horizontal_overlap = sprite.rect.right > other.rect.left and sprite.rect.left < other.rect.right
                if vertical_touch and horizontal_overlap:
                    result.append(other)
            return result
        collided = vertically_touching_or_colliding(self, self.game.players)
        # collided = pygame.sprite.spritecollide(self, self.game.players, False) # this for some reason only works on windows
        for other in collided:
            if other.rect is self.rect:
                continue
            if other.file == self.file:
                self.merge_with(other)
                # recursively check the new merged block
                for sprite in self.game.players:
                    if sprite.file == self.file:
                        sprite.check_chain_merge()
                return


    def apply_gravity(self):
        for sprite in self.game.players:
            if sprite.on_ground:
                if sprite. rect.bottom < self.game.screen_height:
                    # check if a player is directly below
                    below =[
                        other for other in self.game.players if other is not sprite
                        and sprite.rect.bottom == other.rect.top
                        and sprite.rect.right > other.rect.left
                        and sprite.rect.left < other.rect.right
                    ]
                    if below:
                        sprite.on_ground = True
                        sprite.falling = False
                    if not below:
                        sprite.on_ground = False
                        sprite.falling = True


    def explode_cluster(self, center_sprite, push=10):
        visited = set()
        to_check = [center_sprite]

        while to_check:
            sprite = to_check.pop()
            visited.add(sprite)

            for other in list(self.game.players):
                if other is center_sprite:
                    continue
                if other in visited:
                    continue

                if sprite.rect.colliderect(other.rect):
                    # determins which direction to move
                    dx = other.rect.centerx - center_sprite.rect.centerx
                    dy = other.rect.centery - center_sprite.rect.centery

                    if abs(dx) > abs(dy):
                        # horizontal overlap -> horizontal movement
                        if dx > 0:
                            other.rect.x += push
                        else:
                            other.rect.x -= push
                    else:
                        # vertical overlap -> vertical movement
                        if dy < 0:  # nur nach oben
                            other.rect.y -= push

                    # window edges
                    if other.rect.left < 0:
                        other.rect.left = 0
                    if other.rect.right > self.game.screen_width:
                        other.rect.right = self.game.screen_width
                    if other.rect.top < 0:
                        other.rect.top = 0

                    # acheck neighbors or neighbors
                    to_check.append(other)
                    visited.add(other)



    def merge_with(self, other):
        form_keys = list(self.game.player_forms.keys())
        self.kill()
        other.kill()
        new_color = form_keys[form_keys.index(self.file) - 1]
        new_size = self.game.player_forms[new_color]
        # vertical position of new player on top of player below and horizontally centered around other player
        new_x = other.rect.x + (self.height - new_size) / 2
        new_y = other.rect.y + (self.height - new_size)

        merged = Player(self.game, new_x, new_y, file=new_color, size=new_size)
        merged.on_ground = True
        self.game.players.add(merged)
        self.explode_cluster(merged)
        merged.check_chain_merge()
        self.apply_gravity()