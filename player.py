import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x=300, y=32, color='red', size=64):
        super().__init__()
        self.game = game
        self.color = color
        self.surface = game.window
        self.height = size
        self.width = size
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
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
                # check if merge is necessary
                self.check_merge_collisions(other)

                # check if new player sits on top of other players
                if self.rect.bottom >= other.rect.top and self.rect.centery < other.rect.centery:
                    self.rect.bottom = other.rect.top
                    self.on_ground = True
                    self.falling = False
                    return

            # Collision with the ground
            if self.rect.bottom >= self.game.screen_height:
                self.rect.bottom = self.game.screen_height
                self.on_ground = True
                self.falling = False



    def check_merge_collisions(self, other):
        merged = True
        while merged:
            merged = False
            colliding = pygame.sprite.spritecollide(self, self.game.players, False)
            for other in colliding:
                if other is self:
                    continue
                if self.color == other.color:
                    self.merge_with(other)
                    merged = True
                    break

    def check_chain_merge(self):
        # Keep merging while colliding with same color player
        merged = True
        while merged:
            merged = False
            colliding = pygame.sprite.spritecollide(self, self.game.players, False)
            for other in colliding:
                if other is self:
                    continue
                if self.color == other.color:
                    self.merge_with(other)
                    merged = True
                    break

    def merge_with(self, other):
        form_keys = list(self.game.player_forms.keys())
        self.kill()
        other.kill()
        new_color = form_keys[form_keys.index(self.color) - 1]
        new_size = self.game.player_forms[new_color]
        new_x = other.rect.x + (self.rect.width - new_size) / 2
        new_y = other.rect.y + (self.rect.height - new_size)
        merged = Player(self.game, new_x, new_y, color=new_color, size=new_size)
        merged.on_ground = True
        self.game.players.add(merged)
        # merged.check_merge_collisions(other)
        merged.check_chain_merge()