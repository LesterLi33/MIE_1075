import numpy as np
from skimage.draw import line
import heapq

import pygame
from game import Pygame_Window

class Nodes:
    def __init__(self, point=None, parent_id=None, g=float("inf"), h=None, f=float("inf")):
        self.point = point
        self.parent = parent_id
        self.g = g
        self.h = h
        self.f = f

    def update(self, parent, g, h, f):
        self.parent = parent
        self.g = g
        self.h = h
        self.f = f

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

class Astar:
    def __init__(self):
        self.window = Pygame_Window()
        
        start = (110, 600)
        self.window.add_node(start, (255, 0, 0), radius=3, width=3)  
        self.goal = (670, 200)
        self.window.add_node(self.goal, (0, 255, 0), radius=3, width=3)

        self.grid = self.create_grid()
        self.open_list = []
        self.closed_list = np.zeros_like(self.grid)

        heapq.heappush(self.open_list, (0.0, (0, 52)))
        self.grid[0, 52].update(parent=None, g=0, h=float("inf"), f=0)

        # for x in range(self.grid.shape[0]):
        #     for y in range(self.grid.shape[1]):
        #         print(self.grid[x, y].point)

        # self.execute()

    def execute(self):
        while self.open_list:
            pygame.time.delay(10)
            curr_node = heapq.heappop(self.open_list)
            self.closed_list[curr_node[1]] = 1
            self.window.add_node(self.grid[curr_node[1]].point, color=(0, 0, 0, 255))

            if self.grid[curr_node[1]].h < 11:
                color = (0, 255, 0)
                width = 5
                current = self.grid[curr_node[1]]
                self.window.add_line(self.goal, current.point, color=color, width=5)
                while current.parent is not None:
                    parent = self.grid[current.parent]
                    self.window.add_line(current.point, parent.point, color=color, width=5)
                    current = parent
                break

            neighbors = self.get_neighbors(curr_node[1])
            for neighbor in neighbors:
                if not self.closed_list[neighbor] and self.is_free(self.grid[neighbor].point):
                    self.window.add_node(self.grid[neighbor].point)
                    if neighbor[0] != curr_node[1][0] and neighbor[1] != curr_node[1][1]:
                        g = self.grid[curr_node[1]].g + (2 * 10 ** 2) ** (1/2)
                    else:
                        g = self.grid[curr_node[1]].g + 10
                    h = np.linalg.norm(np.array(self.grid[neighbor].point) - np.array(self.goal))
                    f = g + h

                    if self.grid[neighbor].f == float("inf") or self.grid[neighbor].f > f:
                        heapq.heappush(self.open_list, (f, neighbor))
                        self.grid[neighbor].update(curr_node[1], g, h, f)
                        

    def create_grid(self):
        x_coords = np.arange(110, 840, 10)
        y_coords = np.arange(80, 700, 10)

        grid = np.zeros((x_coords.shape[0], y_coords.shape[0]), dtype=tuple)

        for i, x in enumerate(x_coords):
            for j, y in enumerate(y_coords):
                grid[i][j] = Nodes(point=(x, y))

        return grid
    
    def is_free(self, point):
        pixel_color = self.window.screen.get_at(point)
        if pixel_color == (255, 255, 255, 255):
            return True

        
    def get_neighbors(self, node_idx):
        """Get the valid neighbors of a node"""
        row_idx, col_idx = node_idx
        neighbors_idxs = [
            (row_idx+1, col_idx),
            (row_idx-1, col_idx),
            (row_idx, col_idx+1),
            (row_idx, col_idx-1),
            (row_idx+1, col_idx+1),
            (row_idx+1, col_idx-1),
            (row_idx-1, col_idx+1),
            (row_idx-1, col_idx-1),
        ]

        neighbors_idxs = [idx for idx in neighbors_idxs
                          if idx[0] >= 0 and idx[0] <= self.grid.shape[0] - 1
                          and idx[1] >= 0 and idx[1] <= self.grid.shape[1] - 1]
                
        return neighbors_idxs        

    
a_star = Astar()
rrt = RRT()

planner = input("Choose Global Planner: RRT or A*: ")
planner = planner.upper()
assert planner in ['RRT', 'A*']


usr_input = input("Press s to begin: ")

if usr_input == "s":
    print(f"Starting {planner}")
    if planner == 'RRT':
        rrt.planning()
    else:
        a_star.execute()

while True:
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
