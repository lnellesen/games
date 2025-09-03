import pygame
import random
import sys

from fruits import LIST_PLAYERS, remodel_player

# you're missing types on function/method definitions. I marked that with "type(s)"

class Player(pygame.sprite.Sprite):
    """Class to store and define parameters for each player."""
    def __init__(self, game, x=300, y=32, fruits=random.choice(LIST_PLAYERS), size=64):  # constants and types
        super().__init__()
        # type hint here so that mypy can better show issues
        self.game = game
        self.fruits = fruits
        self.height = size
        self.width = size
        self.image = remodel_player(self.fruits)  # reshape_player and remodel_player only take a string?
        self.surface = game.window
        self.rect = self.image.get_rect(topleft=(x, y))
        self.fall_velocity = 300 # fall velocity
        self.on_ground = False # check if player is on the ground
        self.falling = False
        # can some of the attributes be protected? (name starts wit an underscore?)


    def update(self):
        """Check the positions of the player to move them."""
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if not self.on_ground and not self.falling:
            if keys[pygame.K_RIGHT]:
                self.rect.x += 150 * self.game.delta_time  # what is 150? -> consent
                if self.rect.right > self.game.screen_width:
                    self.rect.right = self.game.screen_width
            elif keys[pygame.K_LEFT]:
                self.rect.x -= 150 * self.game.delta_time  # what is 150? -> consent
                if self.rect.left < 0:
                    self.rect.left = 0

        # Start falling
        self.falling = (
            keys[pygame.K_DOWN]
            and not self.on_ground
            and not self.falling
        )

        # you reduce indentations here
        if not (not self.on_ground and self.falling):
            return

        # While falling
        self.rect.y += self.fall_velocity * self.game.delta_time

        colliding = pygame.sprite.spritecollide(self, self.game.players, False)
        for other in colliding:
            if other is self:
                continue
            # Only handle if falling on top
            if self.rect.bottom <= other.rect.top + 5:  # what's 5? -> constant
                self.handle_collision(other)

        # Collision with the ground
        if self.rect.bottom >= self.game.screen_height:
            self.rect.bottom = self.game.screen_height
            self.on_ground = True
            self.falling = False

        self.apply_gravity()

    def handle_collision(self, other):  # types
        """Check if a collision results in a merge or not."""
        form_keys = list(self.game.player_forms.keys()) # this is LIST_PLAYERS, right? Why not use it?

        if self.fruits == other.fruits and form_keys.index(self.fruits) > 0:  # index takes a value not a list...
            self.merge_with(other)
            # in case same fruits are merged again
            self.check_chain_merge()
        else:
            # stop falling on top of another player
            self.rect.bottom = other.rect.top
            # This you do quite often. Maybe introduce a dedicated method `self.stop_falling()`
            self.on_ground = True
            self.falling = False

    def check_chain_merge(self):
        """Check if multiple merges need to happen consecutively."""

        def touching_or_colliding(sprite, group):  # types
            """Check if the players are touching or colliding."""
            result = []
            for other in group:  # you use the name "other"  also in `check_chain_merge` directly, this can have side effects, please rename
                if other is sprite:
                    continue
                if sprite.rect.colliderect(other.rect):
                    result.append(other)
                    continue

                # no extra variables needed, add a comment to describe
                # vertical_touch = sprite.rect.bottom == other.rect.top or sprite.rect.top == other.rect.bottom
                # horizontal_overlap = sprite.rect.right > other.rect.left and sprite.rect.left < other.rect.right
                # horizontal_touch =  sprite.rect.right == other.rect.left or sprite.rect.left == other.rect.right
                # vertical_overlap = sprite.rect.bottom > other.rect.top and sprite.rect.top < other.rect.bottom
                if (
                    sprite.rect.bottom == other.rect.top or sprite.rect.top == other.rect.bottom
                    and sprite.rect.right > other.rect.left and sprite.rect.left < other.rect.right
                ) or (
                    sprite.rect.right == other.rect.left or sprite.rect.left == other.rect.right
                    and sprite.rect.bottom > other.rect.top and sprite.rect.top < other.rect.bottom
                ):
                    result.append(other)
            return result

        collided = touching_or_colliding(self, self.game.players)
        # collided = pygame.sprite.spritecollide(self, self.game.players, False) # this for some reason only works on windows  # remove?
        for other in collided:
            if other.rect is self.rect:
                continue
            if other.fruits == self.fruits:
                self.merge_with(other)
                # recursively check the new merged block
                for sprite in self.game.players:
                    if sprite.fruits == self.fruits:
                        sprite.check_chain_merge()  # why is the variable called `sprite`? `check_chain_merge` is a player method
                return


    def apply_gravity(self):
        """Check that no player hangs in the air."""
        for sprite in self.game.players:
            if sprite.on_ground:
                if sprite.rect.bottom < self.game.screen_height:
                    # very nested, try to avoid with methods we have shown to you
                    # check if a player is directly below
                    below =[
                        other
                        for other in self.game.players
                        if (
                            other is not sprite
                            and sprite.rect.bottom == other.rect.top
                            and sprite.rect.right > other.rect.left
                            and sprite.rect.left < other.rect.right
                        )
                    ]
                    if below:
                        sprite.on_ground = True
                        sprite.falling = False
                    else:
                        sprite.on_ground = False
                        sprite.falling = True


    def explode_cluster(self, center_sprite, push=30): # type on `center_sprite`, 30 -> constant
        """Move players if a new player after a collision needs more space."""
        visited = set()
        to_check = [center_sprite]  # is there a better domain related name than `sprite`? based on your docstring it seems to be a player...

        while to_check:
            sprite = to_check.pop()
            visited.add(sprite)

            for other in list(self.game.players):
                if other is center_sprite or other in visited:
                    continue

                if sprite.rect.colliderect(other.rect):
                    # determines which direction to move
                    dx = other.rect.centerx - center_sprite.rect.centerx
                    dy = other.rect.centery - center_sprite.rect.centery

                    # Default movement vector
                    move_x, move_y = 0, 0

                    if abs(dx) > abs(dy):
                        # horizontal push
                        if dx > 0:
                            # Push right, but only if not too close to right edge
                            if other.rect.right <= self.game.screen_width:
                                move_x = push
                            else:
                                move_x = -push
                        else:
                            # Push left, but only if not too close to left edge
                            if other.rect.left >= 0:
                                move_x = -push
                            else:
                                move_x = push  # push right instead

                    else:
                        # vertical overlap -> vertical movement
                        if dy < 0:
                            move_y -= push * 10

                    # Apply movement
                    other.rect.x += move_x
                    other.rect.y += move_y

                    # stop on window edges?
                    if other.rect.left < 0:
                        other.rect.left = 0
                    if other.rect.right > self.game.screen_width:
                        other.rect.right = self.game.screen_width

                    # # Collision resolution: if overlapping after push, separate
                    # for more in self.game.players:
                    #     if more is other or more is center_sprite:
                    #         continue
                    #     if other.rect.colliderect(more.rect):
                    #         # push away slightly
                    #         if move_x > 0:  # pushed right
                    #             other.rect.right = more.rect.left
                    #         elif move_x < 0:  # pushed left
                    #             other.rect.bottom = more.rect.top
                    #         elif move_y < 0:  # pushed up
                    #             other.rect.top = more.rect.bottom

                    # check neighbors of neighbors
                    to_check.append(other)
                    visited.add(other)



    def merge_with(self, other):  # type
        """Merge two players."""
        form_keys = list(self.game.player_forms.keys())
        self.kill()
        other.kill()
        new_color = form_keys[form_keys.index(self.fruits) - 1]  # index doesn't take list?  If you have Fruit as a class, this could improve your usage here `fruit.upgrade()` (but not necessary)
        new_size = self.game.player_forms[new_color]
        # vertical position of new player on top of player below and horizontally centered around other player
        new_x = other.rect.x + (self.rect.width - new_size) / 2
        new_y = other.rect.y + (self.rect.height - new_size)

        merged = Player(self.game, new_x, new_y, fruits=new_color, size=new_size)
        merged.on_ground = True
        self.game.players.add(merged)
        self.explode_cluster(merged)
        merged.check_chain_merge()
        self.apply_gravity()
        merged.winning()  #  merged.check_if_won()
        merged.game_over(other)  #  merged.check_if_game_over()

    def winning(self):
        """Notify if the last fruit was created and the game is won."""
        form_keys = list(self.game.player_forms.keys())  # check comments before on same code
        new_color = form_keys[form_keys.index(self.fruits) - 1]
        if new_color == LIST_PLAYERS[8]:
            pygame.init()
            font = pygame.font.Font(None, 74)
            text = font.render("YOU WON!", True, (255, 255, 255))
            self.surface.blit(text, (300, 250))
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()  # game stops directly, no other try?


    def game_over(self, other):
        """Notify if the max height was reached and the game is lost."""
        form_keys = list(self.game.player_forms.keys())  # check comments before on same code
        new_color = form_keys[form_keys.index(self.fruits) - 1]
        new_size = self.game.player_forms[new_color]
        # above could be also improved with Fruit class
        new_y = other.rect.y + (self.height - new_size)
        if new_y <= 100 or other.rect.y <= 100:
            pygame.init()
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER :(", True, (255, 255, 255))
            self.surface.blit(text, (300, 250))
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()  # game stops directly, no other try?