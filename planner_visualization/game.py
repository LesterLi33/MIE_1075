import pygame
from pygame.locals import *

class Pygame_Window:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption('RRT* Visualization')
        self.display_info = pygame.display.Info()
        self.size = self.width, self.height = 900, 766
        # self.size = self.width, self.height = self.display_info.current_w, self.display_info.current_h

        layout_img = pygame.image.load('layout.png')
        layout_img = pygame.transform.scale(layout_img, self.size)
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.blit(layout_img, (0,0))
        pygame.display.flip()

    #draw a point on the map
    def add_node(self, point, color=(102, 178, 255), radius=2, width=2):
        pixel_color = self.screen.get_at(point)
        # if pixel_color == (255, 255, 255, 255):
        pygame.draw.circle(self.screen, color, point, radius, width)
        pygame.display.update()

    #Draw line between two points
    def add_line(self, start, end, color=(0, 0, 0, 255), width=1):
        pygame.draw.line(self.screen, color, start, end, width)
        pygame.display.update()
    
    def on_cleanup(self):
        pygame.quit()