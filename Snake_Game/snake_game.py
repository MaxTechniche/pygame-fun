"""
BUG:When rapidly pressing a direction and then going to a reverse direction,
    the snake runs into itself
"""

import pygame
import random
from pygame.locals import *

rows = 31
columns = 31
window_width = 500
absolute_window_width = window_width + columns - 5
window_height = 500
absolute_window_height = window_height + rows + 40
window_size = (absolute_window_width, absolute_window_height)


def scale_width(width):
    width *= window_width//(columns) + 1
    return width


def scale_height(height):
    height *= window_height//(rows) + 1
    return height


cells = [(x, y) for x in range(rows) for y in range(columns)]
cell_grid = []
for x in range(rows):
    row = []
    for y in range(columns):
        row.append((x, y))
    cell_grid.append(row)

snake_start = (rows//2, columns//2)

### PYGAME START ###
pygame.init()
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('SNAKE')
font = pygame.font.SysFont('Consolas', 30)

running = True
while running:
    # TODO Start Screen

    empty_cells = cells[:]
    empty_cells.remove(snake_start)
    snake = [snake_start]
    score = 0
    snack = None
    direction = 'left'
    alive = True
    while alive:
        if not snack:
            snack = random.choice(empty_cells)
        pygame.draw.rect(window, (255, 0, 0), [scale_width(snack[0]),
                                               scale_height(snack[1]), window_width//columns, window_height//rows])

        for segment in snake:
            pygame.draw.rect(window, (0, 255, 0), [scale_width(segment[0]),
                                                   scale_height(segment[1]), window_width//columns, window_height//rows])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    alive = False
                    running = False
                elif event.key == K_UP:
                    if direction == 'down':
                        pass
                    else:
                        direction = 'up'
                elif event.key == K_RIGHT:
                    if direction == 'left':
                        pass
                    else:
                        direction = 'right'
                elif event.key == K_DOWN:
                    if direction == 'up':
                        pass
                    else:
                        direction = 'down'
                elif event.key == K_LEFT:
                    if direction == 'right':
                        pass
                    else:
                        direction = 'left'

        if direction == 'up':
            if snake[0][1]-1 < 0:
                alive = False
            else:
                try:
                    snake.insert(0, cell_grid[snake[0][0]][snake[0][1]-1])
                except IndexError:
                    alive = False
        elif direction == 'right':
            try:
                snake.insert(0, cell_grid[snake[0][0]+1][snake[0][1]])
            except IndexError:
                alive = False
        elif direction == 'down':
            try:
                snake.insert(0, cell_grid[snake[0][0]][snake[0][1]+1])
            except IndexError:
                alive = False
        elif direction == 'left':
            if snake[0][0]-1 < 0:
                alive = False
            else:
                try:
                    snake.insert(0, cell_grid[snake[0][0]-1][snake[0][1]])
                except IndexError:
                    alive = False
        if snake[0] == snack:
            snake_last = snake.pop()
            snack = None
            score += 1
            snake.append(snake_last)
        else:
            snake_last = snake.pop()
        if len(snake) > 1 and snake[0] in snake[1:]:
            alive = False

        pygame.display.update()
        window.fill((255, 255, 255))
        pygame.draw.rect(
            window, (0), [0, 0, absolute_window_width, window_height + rows])
        text = font.render(f'Score: {score}', True, (0, 0, 0))
        window.blit(text, (0, window_height+rows))
        pygame.time.Clock().tick(15)
pygame.quit()

# TODO
