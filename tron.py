import numpy as np
from Game import Game
import pygame as py
        
class Game_object:
    
    def __init__(self, color: tuple, id:int, x:int, y:int) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.pos = [x, y]
        self.rgb_value = color
        
    def __str__(self) -> str:
        return str(self.id)
    
    def get_pos(self):
        return self.pos

class Cycle(Game_object):
    
    def __init__(self, color: tuple, id: int, x: int, y: int, direction: int, controls):
        super().__init__(color, id, x, y)
        self.direction = direction
        self.controls = controls
        self._direction_map = {
            1: np.array([1, 0]),    # Array - Down,     Draw - Right
            2: np.array([0, 1]),    # Array - Right,    Draw - Down
            3: np.array([-1, 0]),   # Array - Up,       Draw - Left
            4: np.array([0, -1]),   # Array - Left,     Draw - Up
        }
        
    def change_direction(self, new_direction):
        dir_change = False
        if new_direction == self.direction or new_direction % 2 == self.direction % 2:
            pass
        else:
            self.direction = new_direction
            dir_change = True
        return dir_change
    
    def move(self):
        wall = Game_object(self.rgb_value, self.id + 5, self.x, self.y)

        current_direction = self._direction_map[self.direction]
        self.x += current_direction[0]
        self.y += current_direction[1]

        return wall, self

class Board:
    
    def __init__(self, size:int, cycles, scale):
        self.size = size
        self.board = np.zeros((self.size,self.size), dtype=np.float32)
        self.cycles = cycles
        self.scale = scale
        self.game = Game(self.size, self.size, self.scale)
        self.reward = 0
        self.steps = 0
        # set rewards
        self.death_penalty = -50
        self.alive_one = 1/self.size
        self.alive_ten = 1/(self.size/2)
        self.alive_hundred = 1/(self.size/4)
        self.win = 100
    
    def __str__(self):
        output = ''
        output += '\n'.join(''.join('{:3}'.format(item) for item in row) for row in self.board)
        return output

    def check_status(self, cycle: Cycle):
        if (cycle.x < 0 or cycle.y < 0 or cycle.x >= self.size or cycle.y >= self.size or self.board[cycle.x, cycle.y] != 0):
            self.cycles.remove(cycle)
            return False
        return True
    
    def game_status(self):
        if(len(self.cycles) >= 1):
            return False
        else:
            return True

    def set_pos(self, obj):
        self.board[obj.x][obj.y] = obj.id

    def turn(self, action):
        for cycle in self.cycles:
            dir_change = cycle.change_direction(action)
            # if(dir_change and self.steps % 50 == 0):
            #     self.reward += self.alive_one
            self.update()

    def view(self):
        for cycle in self.cycles:
            self.game.draw(cycle)
        
    def update(self, display_array = False):
        for cycle in self.cycles:
            if display_array:
                print("Input move for player ",cycle.id,":",sep='',end='')
                direction = int(input())
                cycle.change_direction(direction)
            wall, cycle = cycle.move()
            if self.check_status(cycle):
                self.set_pos(wall)
                self.set_pos(cycle)
                if not display_array:
                    self.game.draw(cycle)
            else:
                # print("Player",cycle.id, "Died!")
                self.reward += self.death_penalty
                return False
        return True

    def evaluate(self):
        self.steps += 1

        if self.steps % 100 == 0:
            self.reward += 1 * (self.steps / 100)
        # elif self.steps % 10 == 0:
        #     self.reward += self.alive_one
        # if len(self.cycles) == 1:
        #     self.reward += self.win
        return self.reward

    def get_board(self):
        return self.board

    def observe(self):
        return self.board.flatten().astype(np.float32)
    
    def reset(self):
        del self.game 
        self.game = Game(self.size, self.size, self.scale)
        obs = self.observe()
        return obs
