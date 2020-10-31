import random
import copy
import pygame
import pygame.locals

window_width = 500
window_height = 500
num_rows = 100
num_columns = 100


og_cells = []
for x in range(num_rows):
    row = []
    for y in range(num_columns):
        row.append(random.choice((True, False)))
    og_cells.append(row)
cells = copy.deepcopy(og_cells)
cell_buffer = copy.deepcopy(og_cells)

pygame.init()
window = pygame.display.set_mode((window_width, window_height))


def scale(x=1):
    return x * (window_width/num_columns)


def neighbors(row, column):
    neighbors = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            try:
                if cells[row+x][column+y]:
                    neighbors += 1
            except:
                pass
    return neighbors


running = True
while running:
    if pygame.key.get_pressed()[pygame.locals.K_SPACE]:
        og_cells = []
        for x in range(num_rows):
            row = []
            for y in range(num_columns):
                row.append(random.choice((True, False)))
            og_cells.append(row)
        cells = copy.deepcopy(og_cells)
        cell_buffer = copy.deepcopy(og_cells)

    for event in pygame.event.get():
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_ESCAPE:
                running = False

    for row in range(len(cell_buffer)):
        for column in range(len(cell_buffer[row])):
            if cell_buffer[row][column]:
                pygame.draw.rect(
                    window, 255, [scale(row), scale(column), scale(), scale()])
            else:
                pygame.draw.rect(
                    window, 0, [scale(row), scale(column), scale(), scale()])
    pygame.display.update()
    window.fill(0)

    for row in range(len(cells)):
        for column in range(len(cells[row])):
            neighbors_alive = neighbors(row, column)
            if cells[row][column]:
                if neighbors_alive < 2 or neighbors_alive > 3:
                    cell_buffer[row][column] = False
                else:
                    cell_buffer[row][column] = True
            else:
                if neighbors_alive == 3:
                    cell_buffer[row][column] = True
    cells = copy.deepcopy(cell_buffer)
pygame.quit()
