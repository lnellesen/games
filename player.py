import pygame
import random
import sys

from fruits import LIST_PLAYERS, reshape_player


class Player(pygame.sprite.Sprite):
    """Class to store and define parameters for each player."""
    def __init__(self, game, X=300, Y=32, fruits=random.choice(LIST_PLAYERS), SIZE=64):
        super().__init__()
        self.game = game
        self.fruits = fruits
        self.height = SIZE
        self.width = SIZE
        self.image = reshape_player(self.fruits)
        self.surface = game.window
        # self.X = X if X > self.game.platform_x else self.game.platform_x
        self.rect = self.image.get_rect(topleft=(X, Y))
        self.FALL_VELOCITY = 300
        self.on_ground = False
        self.falling = False


    def update(self):
        """Check the positions of the player to move them."""
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if not self.on_ground and not self.falling:
            if keys[pygame.K_RIGHT]:
                self.rect.x += 150 * self.game.delta_time # 150 detetermines how fast a player moves horizontally. consant should be somewhere else (?)
                if self.rect.right > self.game.screen_width:
                    self.rect.right = self.game.screen_width
            elif keys[pygame.K_LEFT]:
                self.rect.x -= 150 * self.game.delta_time
                if self.rect.left < 0:
                    self.rect.left = 0

        # Start falling
        if keys[pygame.K_DOWN] and not self.on_ground and not self.falling:
            self.falling = True

        # Falling
        if not self.on_ground and self.falling:
            self.rect.y += self.FALL_VELOCITY * self.game.delta_time

            colliding = pygame.sprite.spritecollide(self, self.game.players, False)
            for other in colliding:
                if other is self:
                    continue
                # Only handle if falling on top
                if self.rect.bottom >= other.rect.top:
                    self.handle_collision(other)

            # Collision with the ground
            if self.rect.bottom >= self.game.platform_y:
                if self.game.platform_x <= self.rect.centerx <= (self.game.WINDOW_WIDTH - self.game.platform_width)/2 + self.game.platform_width:
                    self.rect.bottom = self.game.platform_y
                    self.on_ground = True
                    self.falling = False
                else:
                    self.kill()

            self.apply_gravity()



    def handle_collision(self, other):
        """Check if a collision results in a merge or not."""
        form_keys = list(self.game.player_forms.keys())

        if self.fruits == other.fruits and form_keys.index(self.fruits) > 0:
            self.merge_with(other)

        else:
            # stop falling on top of another player
            self.rect.bottom = other.rect.top
            self.on_ground = True
            self.falling = False

    def check_chain_merge(self):
        """Check if multiple merges need to happen consecutively."""
        def touching_or_colliding(sprite, group):
            """Check if the players are touching or colliding."""
            result = []
            for other_ in group:
                if other_ is sprite:
                    continue
                if sprite.rect.colliderect(other_.rect):
                    result.append(other_)
                    continue
                vertical_touch = sprite.rect.bottom == other_.rect.top
                horizontal_overlap = sprite.rect.right > other_.rect.left and sprite.rect.left < other_.rect.right
                horizontal_touch =  sprite.rect.right == other_.rect.left or sprite.rect.left == other_.rect.right
                vertical_overlap = sprite.rect.bottom > other_.rect.top and sprite.rect.top < other_.rect.bottom
                if (vertical_touch and horizontal_overlap) or (horizontal_touch and vertical_overlap):
                    result.append(other_)
            return result

        collided = touching_or_colliding(self, self.game.players)
        for other in collided:
            if other.rect is self.rect:
                continue
            if other.fruits == self.fruits:
                self.merge_with(other)
                # recursively check the new merged block
                for sprite in self.game.players:
                    if sprite.fruits == self.fruits:
                        sprite.check_chain_merge()
                return


    def apply_gravity(self):
        for sprite in self.game.players:
            if sprite.on_ground:
                if sprite.rect.bottom < self.game.platform_y:
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


    def explode_cluster(self, center_player, push=30):

        visited = set()
        to_check = [center_player]

        while to_check:
            sprite = to_check.pop()
            visited.add(sprite)

            for other in list(self.game.players):
                if other is center_player or other in visited:
                    continue

                if sprite.rect.colliderect(other.rect):
                    # determines which direction to move - either vertically or horizontally after push
                    dx = other.rect.centerx - center_player.rect.centerx
                    dy = other.rect.centery - center_player.rect.centery
                    # Default movement vector
                    move_x, move_y = 0, 0

                    if abs(dx) > abs(dy):
                        # horizontal push
                        if dx > 0:
                            # Push right, but only if not too close to right edge after push
                            if other.rect.right + push <= (self.game.WINDOW_WIDTH - self.game.platform_width)/2 + self.game.platform_width:
                                move_x = push
                            else:
                                other.kill()
                        else:
                            # Push left, but only if not too close to left edge
                            if other.rect.left - push >= (self.game.WINDOW_WIDTH - self.game.platform_width)/2:
                                move_x = -push
                            else:
                                other.kill()

                    else:
                        # vertical overlap -> vertical movement - strength on explosion should not be too large. otherwise direct neibouring fruits gets pushed over overlaying fruits
                        if dy < 0:
                            move_y -= push * 5

                    # Apply movement
                    other.rect.x += move_x
                    other.rect.y += move_y

                    # window edges
                    if other.rect.left < 0:
                        other.rect.left = 0
                    if other.rect.right > self.game.screen_width:
                        other.rect.right = self.game.screen_width

                    # check neighbors of neighbors
                    to_check.append(other)
                    visited.add(other)



    def merge_with(self, other):
        form_keys = list(self.game.player_forms.keys())
        self.kill()
        other.kill()
        new_color = form_keys[form_keys.index(self.fruits) - 1]
        new_size = self.game.player_forms[new_color]
        # vertical position of new player on top of player below and horizontally centered around other player
        new_x = other.rect.centerx + (self.rect.width - new_size) / 2
        new_y = other.rect.y + (self.rect.height - new_size) + 2 # trying to slightly lift newly merged player

        merged = Player(self.game, new_x, new_y, fruits=new_color, SIZE=new_size)
        merged.on_ground = True
        self.game.players.add(merged)
        self.explode_cluster(merged)
        merged.check_chain_merge()
        self.explode_cluster(merged)
        self.apply_gravity()
        merged.winning()
        merged.game_over(other)

    def winning(self):
        form_keys = list(self.game.player_forms.keys())
        new_color = form_keys[form_keys.index(self.fruits) - 1]
        if new_color == LIST_PLAYERS[8]:
            pygame.init()
            font = pygame.font.Font(None, 74)
            text = font.render("YOU WON!", True, (255, 255, 255))
            self.surface.blit(text, (300, 250))
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()


    def game_over(self, other):
        form_keys = list(self.game.player_forms.keys())
        new_color = form_keys[form_keys.index(self.fruits) - 1]
        new_size = self.game.player_forms[new_color]
        new_y = other.rect.y + (self.height - new_size)
        if new_y <= 100 or other.rect.y <= 100:
            pygame.init()
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER :(", True, (255, 255, 255))
            self.surface.blit(text, (300, 250))
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()