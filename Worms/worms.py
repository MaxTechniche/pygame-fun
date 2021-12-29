import pygame
import random
import time

window_width = 200
window_height = 200

current_grid_position = (window_width//2, window_height//2)


class Cell:

    def __init__(self, grid_position):
        self.occupied_by_worm = False
        self.occupying_worm = None
        self.occupied_by_worm_path = False
        self.grid_position = grid_position
        self.grid_x = self.grid_position[0]
        self.grid_y = self.grid_position[1]
        self.neighboring_cells = []

        self.neighbor_left = None
        self.neighbor_up = None
        self.neighbor_right = None
        self.neighbor_down = None

    def __hash__(self):
        return 0

    def __eq__(self, other):
        return True

    def set_neighbors(self):
        if self.grid_x <= 0:
            self.neighbor_left = None
        else:
            self.neighbor_left = grid[self.grid_x - 1][self.grid_y]
            self.neighboring_cells.append(self.neighbor_left)

        if self.grid_y <= 0:
            self.neighbor_up = None
        else:
            self.neighbor_up = grid[self.grid_x][self.grid_y - 1]
            self.neighboring_cells.append(self.neighbor_up)

        if self.grid_x >= window_width - 1:
            self.neighbor_right = None
        else:
            self.neighbor_right = grid[self.grid_x + 1][self.grid_y]
            self.neighboring_cells.append(self.neighbor_right)

        if self.grid_y >= window_height - 1:
            self.neighbor_down = None
        else:
            self.neighbor_down = grid[self.grid_x][self.grid_y + 1]
            self.neighboring_cells.append(self.neighbor_down)

    def get_occupying_worm(self):
        return self.occupying_worm


class Worm:
    Number_of_Worms = 0

    def __init__(self, grid_position=(window_width//2, window_height//2)):
        self.grid_position = grid_position
        self.grid_x = self.grid_position[0]
        self.grid_y = self.grid_position[1]
        self.cell = grid[self.grid_x][self.grid_y]
        self.cell.occupied_by_worm_path = True
        self.alive = True
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        Worm.Number_of_Worms += 1

    def in_grid(self):
        if self.grid_x < 0 or self.grid_x > window_width:
            return False
        if self.grid_y < 0 or self.grid_y > window_height:
            return False
        return True

    def set_position(self, grid_position):
        self.grid_position = grid_position
        self.grid_x = grid_position[0]
        self.grid_y = grid_position[1]

    def perform_action(self):
        self.move()

    def neighbors(self):
        available_neighbors = []
        for neighbor in self.cell.neighboring_cells:
            if not neighbor.occupied_by_worm_path:
                available_neighbors.append(neighbor)
        if len(available_neighbors) == 0:
            return
        return random.choice(available_neighbors)

    def move(self):
        self.cell.occupied_by_worm_path = True
        self.cell.occupying_worm = None
        self.cell = self.neighbors()
        if self.cell is None:
            self.alive = False
            return
        self.cell.occupying_worm = self
        self.grid_position = self.cell.grid_position
        pygame.draw.line(surface, self.color, self.grid_position, self.grid_position)

    def __del__(self):
        Worm.Number_of_Worms -= 1


def get_number_of_worms():
    return Worm.Number_of_Worms

pygame.init()
surface = pygame.display.set_mode((window_width, window_height))

grid = []

for x in range(window_width):
    cell_row = []
    for y in range(window_height):
        cell_row.append(Cell((x, y)))
    grid.append(cell_row)
for x in range(len(grid)):
    for y in range(len(grid[x])):
        grid[x][y].set_neighbors()

worm_list = [Worm(current_grid_position)]
max_worms = 1
while get_number_of_worms() > 0:
    pygame.event.get()
    worm_list.append(Worm((random.randint(0, window_width-1), random.randint(0, window_height-1))))
    for worm in worm_list:
        if worm.alive:
            worm.perform_action()
            pygame.display.update()
        else:
            worm_list.remove(worm)
            worm.__del__()
    time.sleep(.02)
    max_worms = max(max_worms, get_number_of_worms())

print(max_worms)
