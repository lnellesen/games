import pygame


class Player:
    def __init__(self, game, x=300, y=32, color='red', size=64):
        self.x = x # vertical starting position
        self.y = y # horizontal starting position
        self.game = game
        self.color = color
        self.surface = game.window
        self.height = size
        self.width = size
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.fall_velocity = 200 # fall velocity
        self.on_ground = False # check if player is on the ground
        self.falling = False


    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.movement(speed=100)
        self.draw() # draws object during every update
    
    def draw(self): # shape of object
        pygame.draw.rect(self.surface, "black", (self.x - 1, self.y - 1, self.width + 2, self.height + 2))
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))


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
                if self._is_falling_on_top_of(other) and self.color == other.color:
                    self.merge_with(other)
                    return
                elif self._is_falling_on_top_of(other):
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
    
    def merge_with(self, other):

        self.game.players.remove(self)
        self.game.players.remove(other)

        form_keys = list(self.game.player_forms.keys())
        current_index = form_keys.index(self.color)

        if current_index > 0:
            new_color = form_keys[current_index - 1]
            new_size = self.game.player_forms[new_color]
        else:
            new_color = self.color
            new_size = self.height
        
        new_x = (self.x + other.x) // 2
        new_y = other.y 

        merged = Player(self.game, new_x, new_y, color=new_color, size=new_size)
        merged.on_ground = True
        self.game.players.append(merged)