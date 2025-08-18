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
        # self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.fall_velocity = 200 # fall velocity
        self.on_ground = False # check if player is on the ground
        self.falling = False


    def update(self):
        # self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.movement(speed=100)
        # self.draw() # draws object during every update
    
    def draw(self): # shape of object
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))


    def movement(self, speed):
        keys = pygame.key.get_pressed()

        if not self.on_ground and not self.falling:
            if keys[pygame.K_RIGHT]:
                self.rect.x += speed * self.game.delta_time
                # right border for rectangle
                if self.rect.right > self.game.screen_width:
                    self.rect.right = self.game.screen_width

            elif keys[pygame.K_LEFT]:
                self.rect.x -= speed * self.game.delta_time
                # left border for rectangle
                if self.rect.left < 0:
                    self.rect.left = 0

        if keys[pygame.K_DOWN] and not self.on_ground and not self.falling:
            self.falling = True
        if not self.on_ground and self.falling:
            self.rect.y += self.fall_velocity * self.game.delta_time

            # Check for collision with other players
            for other in self.game.players:
                if other is self:
                    continue
                if self.is_falling_on_top_of(other) and self.color == other.color:
                    form_keys = list(self.game.player_forms.keys())
                    # merge with other player it not largest possible player
                    if form_keys.index(self.color) > 0:
                        self.merge_with(other)
                    else:
                        self.rect.y = other.rect.y - self.height
                        self.on_ground = True
                        self.falling = False
                    return
                elif self.is_falling_on_top_of(other):
                    self.rect.y = other.rect.y - self.height
                    self.on_ground = True
                    self.falling = False
                    return

            # Check collision with the ground
            if self.rect.y >= self.game.screen_height - self.height:
                self.rect.y = self.game.screen_height - self.height
                self.on_ground = True
                self.falling = False


    def is_falling_on_top_of(self, other):
        # Check if this player is falling onto another player
        horizontally_aligned = (
            self.rect.right > other.rect.left and
            self.rect.left < other.rect.right
        )
        vertically_touching = (
            self.rect.bottom >= other.rect.top and
            self.rect.bottom - self.fall_velocity * self.game.delta_time < other.rect.top
        )
        return horizontally_aligned and vertically_touching
    
    def merge_with(self, other):
        
        form_keys = list(self.game.player_forms.keys())
        self.kill()
        other.kill()
        new_color = form_keys[form_keys.index(self.color) - 1]
        new_size = self.game.player_forms[new_color]
        # vertical position of new player on top of player below and horizontally centered around other player
        new_x = other.rect.x + (self.height - new_size) / 2
        new_y = other.rect.y + (self.height - new_size)

        merged = Player(self.game, new_x, new_y, color=new_color, size=new_size)
        merged.on_ground = True
        self.game.players.add(merged)