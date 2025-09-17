import pygame
import random

from player_configuration import remodel_player, LIST_PLAYER_FILES


class Player(pygame.sprite.Sprite):
    """Class to store and define parameters for each player."""
    FALL_VELOCITY = 300
    HORIZONTAL_VELOCITY = 150
    PUSH = 20
    def __init__(self, game, size, x=500, y=32,  fruit=random.choice(LIST_PLAYER_FILES)):
        super().__init__()
        self.game = game
        self.fruit = fruit
        self._height = size
        self.image = remodel_player(self.fruit)
        self._surface = game.window
        self.rect = self.image.get_rect(topleft=(x, y))
        self.on_ground = False
        self._falling = False


    def _stop_falling(self):
        self.on_ground = True
        self.falling = False


    def update(self):
        """Check the positions of the player to move them."""
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if not self.on_ground and not self._falling:
            if keys[pygame.K_RIGHT]:
                self.rect.x += Player.HORIZONTAL_VELOCITY * self.game.delta_time
                if self.rect.right > self.game.screen_width:
                    self.rect.right = self.game.screen_width
            elif keys[pygame.K_LEFT]:
                self.rect.x -= Player.HORIZONTAL_VELOCITY * self.game.delta_time
                if self.rect.left < 0:
                    self.rect.left = 0

        # Start falling
        if keys[pygame.K_DOWN] and not self.on_ground and not self._falling:
            self._falling = True

        # Falling
        if not self.on_ground and self._falling:
            self.rect.y += Player.FALL_VELOCITY * self.game.delta_time

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
                    self._stop_falling()
                else:
                    self.kill()

            self.apply_gravity()



    def handle_collision(self, other):
        """Check if a collision results in a merge or not."""
        form_keys = LIST_PLAYER_FILES
        # form_keys.index(self.fruit) > 0: watermelons are the largest fruit and can not merge
        if self.fruit == other.fruit and form_keys.index(self.fruit) > 0:
            self.merge_with(other)
        else:
            # stop falling on top of another player
            self.rect.bottom = other.rect.top
            self._stop_falling()

    def check_chain_merge(self):
        """Check if multiple merges need to happen consecutively."""
        def touching_or_colliding(sprite, group):
            """Check if the players are touching or colliding."""
            result = []
            for _other in group:
                if _other is sprite:
                    continue
                if sprite.rect.colliderect(_other.rect):
                    result.append(_other)
                    continue
                # check for overlaps and contact
                if (
                        sprite.rect.bottom == _other.rect.top or sprite.rect.top == _other.rect.bottom
                        and sprite.rect.right > _other.rect.left and sprite.rect.left < _other.rect.right
                ) or (
                        sprite.rect.right == _other.rect.left or sprite.rect.left == _other.rect.right
                        and sprite.rect.bottom > _other.rect.top and sprite.rect.top < _other.rect.bottom
                ):
                    result.append(_other)
            return result

        collided = touching_or_colliding(self, self.game.players)
        for other in collided:
            if other.rect is self.rect:
                continue
            if other.fruit == self.fruit:
                self.merge_with(other)
                # recursively check the new merged block
                for other_players in self.game.players:
                    if other_players.fruit == self.fruit:
                        other_players.check_chain_merge()
                return


    def apply_gravity(self):
        """Check that no player hangs in the air."""
        for _player in self.game.players:
            if _player.on_ground:
                if _player.rect.bottom < self.game.platform_y:
                    # check if a player is directly below
                    below =[
                        other for other in self.game.players if other is not _player
                        and _player.rect.bottom == other.rect.top
                        and _player.rect.right > other.rect.left
                        and _player.rect.left < other.rect.right
                    ]
                    if below:
                        _player.on_ground = True
                        _player._falling = False
                    if not below:
                        _player.on_ground = False
                        _player._falling = True


    def explode_cluster(self, center_player):
        """Move players if a new player after a colision needs more space."""
        visited = set()
        to_check = [center_player]
        push = Player.PUSH

        while to_check:
            _player = to_check.pop()
            visited.add(_player)

            for other in list(self.game.players):
                if other is center_player or other in visited:
                    continue

                if _player.rect.colliderect(other.rect):
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
                        # vertical overlap -> vertical movement - strength on explosion should not be too large.
                        # otherwise direct neibouring fruits gets pushed over overlaying fruits
                        if dy < 0:
                            move_y -= push * 5

                    # Apply movement
                    other.rect.x += move_x
                    other.rect.y += move_y

                    # check neighbors of neighbors
                    to_check.append(other)
                    visited.add(other)



    def merge_with(self, other):
        """Merge two players."""
        form_keys = LIST_PLAYER_FILES
        self.kill()
        other.kill()
        new_player = form_keys[form_keys.index(self.fruit) - 1]
        new_size = self.game.PLAYER_FORMS[new_player]
        # vertical position of new player on top of player below and horizontally centered around other player
        new_x = other.rect.centerx + (self.rect.width - new_size) / 2
        new_y = other.rect.y + (self.rect.height - new_size) + 2 # trying to slightly lift newly merged player

        merged = Player(self.game, size=new_size,fruit=new_player, x=new_x, y=new_y)
        level = form_keys.index(self.fruit)
        merged.on_ground = True
        points = len(form_keys) - level
        self.game.score += points
        self.game.players.add(merged)
        self.explode_cluster(merged)
        merged.check_chain_merge()
        self.explode_cluster(merged)
        self.apply_gravity()
        merged.winning()
        merged.game_over(other)

    def winning(self):
        """Notify if the last fruit was created and the game is won."""
        form_keys = LIST_PLAYER_FILES
        new_player = form_keys[form_keys.index(self.fruit)]
        if new_player == LIST_PLAYER_FILES[self.game.WINNING_PLAYER]:
            pygame.init()
            font = pygame.font.Font(None, self.game.TEXT_SIZE_FINISH)
            text = font.render("YOU WON!", True, self.game.WHITE)
            self._surface.blit(text, self.game.POSITION_FINISH)
            font_score = pygame.font.Font(None, self.game.TEXT_SIZE_FINAL_SCORE)
            score_text = font_score.render(f"Final Score: {self.game.score}", True, self.game.WHITE)
            self._surface.blit(score_text, self.game.POSITION_FINAL_SCORE)

            button_rect = pygame.Rect((self.game.WINDOW_WIDTH - self.game.BUTTON_WIDTH) // 2, self.game.POSITION_FINAL_SCORE[1] + 100, self.game.BUTTON_WIDTH, self.game.BUTTON_HEIGHT)
            pygame.draw.rect(self._surface, self.game.BUTTON_COLOR, button_rect)
            button_font = pygame.font.Font(None, self.game.TEXT_SIZE_SCORE)
            button_text = button_font.render("Replay", True, self.game.WHITE)
            text_x = (self.game.WINDOW_WIDTH - self.game.BUTTON_WIDTH) // 2 + (self.game.BUTTON_WIDTH - button_text.get_width()) // 2
            text_y = self.game.POSITION_FINAL_SCORE[1] + 100 + (self.game.BUTTON_HEIGHT - button_text.get_height()) // 2
            self._surface.blit(button_text, (text_x, text_y))
            pygame.display.flip()
            # Freeze game, wait for quit or key press
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect.collidepoint(event.pos):
                            waiting = False

            import main
            pygame.quit()
            main.Game().run()


    def game_over(self, other):
        """Notify if the max height was reached and the game is lost."""
        form_keys = LIST_PLAYER_FILES
        new_player = form_keys[form_keys.index(self.fruit) - 1]
        new_size = self.game.PLAYER_FORMS[new_player]
        new_y = other.rect.y + (self._height - new_size)
        if new_y <= self.game.GAME_OVER_HIGHT or other.rect.y <= self.game.GAME_OVER_HIGHT:
            font = pygame.font.Font(None, self.game.TEXT_SIZE_FINISH)
            text = font.render("GAME OVER :(", True, self.game.WHITE)
            self._surface.blit(text, self.game.POSITION_FINISH)
            font_score = pygame.font.Font(None, self.game.TEXT_SIZE_FINAL_SCORE)
            score_text = font_score.render(f"Final Score: {self.game.score}", True, self.game.WHITE)
            self._surface.blit(score_text, self.game.POSITION_FINAL_SCORE)

            button_rect = pygame.Rect((self.game.WINDOW_WIDTH - self.game.BUTTON_WIDTH) // 2, self.game.POSITION_FINAL_SCORE[1] + 100, self.game.BUTTON_WIDTH, self.game.BUTTON_HEIGHT)
            pygame.draw.rect(self._surface, self.game.BUTTON_COLOR, button_rect)
            button_font = pygame.font.Font(None, self.game.TEXT_SIZE_SCORE)
            button_text = button_font.render("Replay", True, self.game.WHITE)
            text_x = (self.game.WINDOW_WIDTH - self.game.BUTTON_WIDTH) // 2 + (self.game.BUTTON_WIDTH - button_text.get_width()) // 2
            text_y = self.game.POSITION_FINAL_SCORE[1] + 100 + (self.game.BUTTON_HEIGHT - button_text.get_height()) // 2
            self._surface.blit(button_text, (text_x, text_y))


            pygame.display.flip()
            # Freeze game, wait for quit or key press
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect.collidepoint(event.pos):
                            waiting = False

            import main
            pygame.quit()
            main.Game().run()
