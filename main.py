"""Run/starts game."""
import pygame
import player
import random
from fruits import LIST_PLAYERS

# Every value which doesn't change and has a "domain purpose" should be a constant.
# If you use a setting on a library function, e.g. `infer_datetime=True` in pandas, True must not be a constant
# I'll mark constants with a comment
# You might want to have a config.py module if you want to separate it from your code,
# or it is also relent for other modules

class Game:
    def __init__(self):
        """Init of the game class."""
        # One line docstring stays in same line.
        pygame.init()
        self.window_width = 800  # constant
        self.window_height = 600  # constant
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("fruit merge")
        self.clock = pygame.time.Clock()
        self.screen_height = self.window.get_height()
        self.screen_width = self.window.get_width()

        # extension should be clear by th code doing it, therefor the comment can be removed
        # list of all players in the game - it gets extended whenever a new player is added
        self.players = [player.Player(self)]  # why is the player dependent on the game?
        # why don't you set up `LIST_PLAYERS` directly as a dictionary? currently both collections not well linked,
        # if LIST_PLAYERS changes in length, this code will not know
        self.player_forms = {
            LIST_PLAYERS[0]: 278,
            LIST_PLAYERS[1]: 272,
            LIST_PLAYERS[2]: 241,
            LIST_PLAYERS[3]: 234,
            LIST_PLAYERS[4]: 210,
            LIST_PLAYERS[5]: 173,
            LIST_PLAYERS[6]: 149,
            LIST_PLAYERS[7]: 126,
            LIST_PLAYERS[8]: 109,
            LIST_PLAYERS[9]: 79,
        }

        self.players = pygame.sprite.Group() # overwrites first `players` definition?

        self.add_new_player(first=True)

        self.run()

    def run(self):
        """Run the game."""
        running = True
        while running:
            # make separate method, as this is a quit specific tasks in a method which is high level
            # like: running = shall_run()
            # or even in loop directly, but this would not run th code after the False case... Keep this in mind:
            # while shall_run():
            #     ...
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            # delta_time was not setup in init.
            # You should not introduce new attributes outside the init
            self.delta_time = self.clock.tick(60) / 1000
            self.window.fill((255, 255, 255))

            self.players.update()
            self.players.draw(self.window)

            last = self.players.sprites()[-1]  # if the thing you cast to a list is unordered, it can have weird results, use the method, provided by the library
            if last.on_ground:  # is a player a fruit? confusing naming
                self.add_new_player()


            pygame.display.update()

    pygame.quit()

    # unnecessary comment, can be described in docstring
    # function to add new player with randomly selected color and size
    def add_new_player(self, first=False):  # ´first´ parameter not used
        """Add a new player."""
        fruits, size = random.choice(list(self.player_forms.items())[6:])  # why 6? -> constant
        new_player = player.Player(self, 300, 32, fruits=fruits, size=size)
        # old code
        # fruit, size = random.choice(list(self.player_forms.items())[6:])
        # new_player = player.Player(self, 300, 32, fruit=fruit, size=size)
        self.players.add(new_player)  # new_player seems to have an unexpected type. Pycharm highlights `new_player`

# "if __name__ == '__main__':" is missing
game = Game()
