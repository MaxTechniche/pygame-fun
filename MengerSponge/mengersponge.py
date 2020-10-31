import pygame
from pygame.locals import *

window_size = (3**6, 3**6)


def expand(block):

    top_left = [block[0] - ((2/3) * block[2]), block[1] - ((2/3) * block[3]),
                block[2] - ((2/3) * block[2]), block[3] - ((2/3) * block[3])]

    top = [block[0] + ((1/3) * block[2]), block[1] - ((2/3) * block[3]),
           block[2] - ((2/3) * block[2]), block[3] - ((2/3) * block[3])]

    top_right = [block[0] + ((4/3) * block[2]), block[1] - ((2/3) * block[3]),
                 block[2] - ((2/3) * block[2]), block[3] - ((2/3) * block[3])]

    right = [block[0] + ((4/3) * block[2]), block[1] + ((1/3) * block[3]),
             block[2] - ((2/3) * block[2]), block[3] - ((2/3) * block[3])]

    bottom_right = [block[0] + ((4/3) * block[2]), block[1] + ((4/3) * block[3]),
                    block[2] - ((2/3) * block[2]), block[3] - ((2/3) * block[3])]

    bottom = [block[0] + ((1/3) * block[2]), block[1] + ((4/3) * block[3]),
              block[2] - ((2/3) * block[2]), block[3] - ((2/3) * block[3])]

    bottom_left = [block[0] - ((2/3) * block[2]), block[1] + ((4/3) * block[3]),
                   block[2] - ((2/3) * block[2]), block[3] - ((2/3) * block[3])]

    left = [block[0] - ((2/3) * block[2]), block[1] + ((1/3) * block[3]),
            block[2] - ((2/3) * block[2]), block[3] - ((2/3) * block[3])]

    return_blocks = [top_left, top, top_right, right,
                     bottom_right, bottom, bottom_left, left]

    return return_blocks


pygame.init()
window = pygame.display.set_mode(window_size)

blocks = [[window_size[0]//3, window_size[1] //
           3, window_size[0]//3, window_size[1]//3]]
blocks_buffer = []
window.fill((255, 255, 255))
running = True
while running:

    for block in blocks:
        pygame.draw.rect(window, 0, block)
        # pygame.display.update()
    pygame.display.update()

    for block in blocks:
        blocks_buffer.extend(expand(block))

    choice = False
    while not choice:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    choice = True
                elif event.key == K_ESCAPE:
                    choice = True
                    running = False
            elif event.type == QUIT:
                running = False

    blocks = blocks_buffer[:]
    blocks_buffer.clear()

pygame.quit()
