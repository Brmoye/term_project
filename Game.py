import pygame
import numpy
pygame.init()

class Game():
        
    def __init__(self, x, y, scale) -> None:
        self.scale = scale
        self.screen = pygame.display.set_mode([x * scale, y * scale])
        self.clock = pygame.time.Clock()
        
    def draw(self, c):
        pygame.draw.rect(self.screen,c.rgb_value,pygame.Rect(c.x * self.scale , c.y * self.scale  , 1 * self.scale , 1 * self.scale))
        pygame.display.update()

    def check_inputs(self, cycles):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                for c in cycles:
                    
                    if event.key in c.controls[0]:
                        # print("Left")
                        c.change_direction(3)
                    elif event.key in c.controls[1]:
                        # print("Up")
                        c.change_direction(4)
                    elif event.key in c.controls[2]:
                        # print("Down")
                        c.change_direction(2)
                    elif event.key in c.controls[3]:
                        # print("Right")
                        c.change_direction(1)
                    

