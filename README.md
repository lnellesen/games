Fruit merge 2.0 invented by Merit Carstensen and Leonie Nellesen is a game with its idea based on the original game fruit merge. 
The current version is a fully functioning game with room for improvement in later versions.


**Code structure** \
To run this game you need to clone this repository. You need a Python version of 3.11.9 or 3.12. 
Install the requirements using 'pip install -r requirements.txt'. 
The scripts needed to play the game are in the src folder. Run main.py to start playing.
main.py uses player.py which hosts the game mechanics. 
player.py uses the folder resized_images which includes the fruit images used in the game.
player_configuration.py is not needed to play the game, but it was needed to resize the raw fruit images so that they can be used in the game.
The folder tests includes a simple test for a function in player.py.

**Playing** \
A window will pop up in which you see a platform at the bottom and your score on the top left. 
A fruit appears at the top-middle of the window and can be moved using the arrows keys of your keyboard.
If you want to fruit to move horizontally right or left, press the arrow keys right or left. 
If you want the fruit to fall to the bottom press the arrow key pointing downward. 
Once the fruit is falling you are no longer able to move it horizontally. 
The fruit should land on the platform as it disappears otherwise.
Once the fruit landed a new fruit appears at the top of the window.
There is a total of 10 fruits - blueberry, raspberry, cherry, strawberry, kiwi, lemon, apple, orange, dragonfruit, melon.
A random fruit of the first 4 fruits appears at the top of the window.
Fruits of the same kind merge when falling on top of each other which increases the score. 
The points of a merge increase with the size of the fruit starting with 1 point if two blueberries. 
The highest possible merge (9 points) is when two dragon fruits merge to a melon. This is when you win!
When a merge takes place surrounding fruits get pushed away horizontally and vertically to avoid overlaps.
This also means that existing fruits can be push of the platform and disappear. 
You can lose the game if you stack too many fruits on top of each other so that you cannot put another fruit on top.
If you win/lose the screen changes displaying you final score. 
If you want to play again you can simply press on the green replay button. 
You can always end the game by closing the game window or by pressing esc.
It might seem like that fruits are not touching because all of them are inside a rectangle which made their movements and interactions a lot easier
(this is where the game mechanics could be improved).

**Good luck** winning is very difficult and takes a while! \
Be warned it is addicting! 
