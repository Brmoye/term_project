from tron import *
from Game import Game
import pygame as py

player1 = Cycle((150,50,200), 1, 50, 50, 2, [[py.K_a],[py.K_w],[py.K_s],[py.K_d]])
#player2 = Cycle((100,64,0), 2, 100, 100, 4,  [[py.K_LEFT],[py.K_UP],[py.K_DOWN],[py.K_RIGHT]])
cycles = [player1]

board_size = 200

b = Board(board_size, cycles, 2)


display_array = False
game_status = True
while game_status:
    if not display_array:
        b.game.check_inputs(cycles)
        game_status = b.update()
        b.view()
        b.game.clock.tick(45)
    else:
        game_status = b.step(display_array)
        print(b)

py.display.quit()
py.quit()