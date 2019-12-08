import random
import pygame
from pygame.locals import *

universal_color = (255, 255, 255)


class Star():
    def __init__(self, x=None, y=None, color=None):
        random.randint(0, window_width), random.randint(0, window_height)
        self.x = x
        if not self.x:
            self.x = random.randint(0, window_width)

        self.y = y
        if not self.y:
            self.y = random.randint(0, window_height)

        self.color = color
        if not self.color:
            self.color = universal_color

        self.size = random.randint(1, 2)
        self.x_s = self.x_speed()
        self.y_s = self.y_speed()

    def x_speed(self):
        return (self.x - window_width/2) / (window_width/2) * speed

    def y_speed(self):
        return (self.y - window_height/2) / (window_height/2) * speed

    def updatePosition(self):
        self.x += self.x_s
        self.y += self.y_s


window_width = 600
window_height = 600
window_size = (window_width, window_height)

speed = 5
spawn_rate = 10
max_stars = 0

window = pygame.display.set_mode(window_size)

stars = []
stars_buffer = []
running = True
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    for _ in range(spawn_rate):
        stars.append(Star())

    for star in stars:
        star.updatePosition()
        if 0 < star.x < window_width and 0 < star.y < window_height:
            stars_buffer.append(star)

    for star in stars:
        pygame.draw.circle(window, star.color,
                           (int(star.x), int(star.y)), star.size)
    max_stars = max(max_stars, len(stars))
    print(len(stars), max_stars)
    stars = stars_buffer[:]
    stars_buffer.clear()

    pygame.time.Clock().tick()
    pygame.display.update()
    window.fill(0)
pygame.quit()
