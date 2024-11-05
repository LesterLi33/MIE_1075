import numpy as np
from skimage.draw import line

import pygame
from pygame.locals import *

class Nodes:
    def __init__(self, point, parent_id):
        self.point = point
        self.parent = parent_id
        

class Pygame_Window:
    def __init__(self):
        
        self.size = self.width, self.height = 900, 766

        pygame.init()
        pygame.display.set_caption('RRT* Visualization')
        
        layout_img = pygame.image.load('layout.png')
        layout_img = pygame.transform.scale(layout_img, self.size)
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.blit(layout_img, (0,0))
        pygame.display.flip()

    #draw a point on the map
    def add_node(self, point, color=(102, 178, 255), radius=2, width=2):
        pixel_color = self.screen.get_at(point)
        if pixel_color == (255, 255, 255, 255):
            pygame.draw.circle(self.screen, color, point, radius, width)
            pygame.display.update()

    #Draw line between two points
    def add_line(self, start, end, color=(0, 0, 0, 255), width=1):
        pygame.draw.line(self.screen, color, start, end, width)
        pygame.display.update()
    
    def on_cleanup(self):
        pygame.quit()

class RRT:
    def __init__(self):
        self.window = Pygame_Window()
        
        self.num_samples = 10000
        self.goal_threshold = 30
        self.nodes = []
        
        start = (110, 600)
        self.nodes.append(Nodes(start, None))
        self.window.add_node(start, (255, 0, 0), radius=3, width=3)
        
        self.goal = (670, 200)
        self.window.add_node(self.goal, (0, 255, 0), radius=3, width=3)

    #Randomly sample a point in free space on the map
    def new_sample(self):
        while True:
            point_x = np.random.randint(110, 840, size=(1))
            point_y = np.random.randint(80, 700, size=(1))
            point = (point_x[0], point_y[0])

            pixel_color = self.window.screen.get_at(point)
            if pixel_color == (255, 255, 255, 255):
                return point

    #Find nearest node to newly samples point
    def get_nearest_node(self, point):
        node_points = np.array([node.point for node in self.nodes])
        distances = np.linalg.norm(node_points - point, axis=1)
        nearest_node_idx = np.argmin(distances)

        return nearest_node_idx

    #Get all pixel coordinates of the line between the start point and end point
    def get_line_pixels(self, start, end):
        rr, cc = line(start[0], start[1], end[0], end[1])
        line_pixels = np.zeros((len(rr), 2), dtype=int)
        line_pixels[:, 0] += rr
        line_pixels[:, 1] += cc
        line_pixels = line_pixels[1:]
        
        return line_pixels
    
    #Check if the line passes through an obstacle
    def check_collision(self, start, end):
        line_pixels = self.get_line_pixels(start, end)
        for pixel in line_pixels:
            pixel_color = self.window.screen.get_at(pixel)
            if pixel_color == (255, 0, 0, 255):
                continue
            elif pixel_color == (102, 178, 255):
                continue
            elif pixel_color != (255, 255, 255, 255):
                return True
        return False

    def goal_reached(self):
        last_node = self.nodes[-1]
        dist_to_goal = np.linalg.norm(np.array(last_node.point) - np.array(self.goal))
        if dist_to_goal <= self.goal_threshold:
            return True
        
        return False
    
    def draw_path(self):
        #Draw line from goal to last node in list
        color = (0, 255, 0)
        width = 5
        
        last_node = self.nodes[-1]
        self.window.add_line(self.goal, last_node.point, color, width)

        while last_node.parent is not None:
            parent = last_node.parent
            self.window.add_line(last_node.point, parent.point, color, width)
            last_node = parent


    #Execute RRT Path Planning Algorithm
    def planning(self):
        i = 1
        goal_reached = False
        while not goal_reached and i < self.num_samples:
            point = self.new_sample()
            nearest_node_idx = self.get_nearest_node(point)
            nearest_node = self.nodes[nearest_node_idx]
            if np.linalg.norm(np.array(nearest_node.point) - np.array(point)) > 30:
                continue

            collision = self.check_collision(nearest_node.point, point)
            if not collision:
                self.window.add_node(point)
                self.window.add_line(nearest_node.point, point)
                self.nodes.append(Nodes(point, nearest_node))
                
                goal_reached = self.goal_reached()
                if goal_reached:
                    self.draw_path()
                    break
            i += 1
            

rrt = RRT()
rrt.planning()

running = True
while running:
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rrt.window.on_cleanup()
                    running = False
