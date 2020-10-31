import pygame
from pygame.locals import *
import random
import os
default_used_characters = (65, 123) # Character Choices
# user_characters = []
fade_rate = 20 # Fade Rate - Higher is faster
spawn_rate = 1 # Spawn Rate
number_of_columns = 100 # actual number has 1 added to it
fps = 0 # FPS 0 equals as fast as possible
cell_lock = True


window_size = (1600,900)
char_size = max(2, round(window_size[0] / max(1, number_of_columns)))

colors = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'PURPLE': (0, 0, 255),
    'LIGHT PURPLE': (170, 170, 220),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
}

# Add your own Styles
styles = {
    'Christmas': ((255, 0, 0), (0, 255, 0)),
    'Random': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    'Rainbow': ((255, 0, 255), (125, 0, 255), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 127, 0), (255, 0, 0)),
    'White': (255, 255, 255),
    'Matrix': (0, 255, 0),
}
style = 'Matrix' # Select Style

class Char():
    def __init__(self, x, y, char_size, character=None, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.char_size = char_size
        self.character = character
        if not self.character:
            self.character = chr(random.randint(default_used_characters[0], default_used_characters[1]))
        self.color = color

class Button():
    def __init__(self, style_name, position=(0, 0), color=colors['LIGHT PURPLE'], selected=False):
        self.style_name = style_name
        self.top_left = position
        self.width = window_x // (len(styles)+1)
        self.height = int(window_y * .05)
        self.current_color = color
        self.selected = selected
        self.default_color = color
        
    def mouse_hover(self, mouse_position):
        if self.selected:
            pass
        elif self.in_button_area(mouse_position):
            self.current_color = colors['WHITE']
        else:
            self.current_color = colors['LIGHT PURPLE']
        
    def clicked(self, mouse_position):
        if self.in_button_area(mouse_position):
            self.selected = True
            self.changeColor()
            return True
        else:
            self.selected = False
            self.changeColor()
            return False
            
    def in_button_area(self, mouse_position):
        if self.top_left[0] <= mouse_position[0] <= self.top_left[0]+self.width \
                        and self.top_left[1] <= mouse_position[1] <= self.top_left[1]+self.height:
            return True
        return False
    
    def changeColor(self):
        if self.selected:
            self.current_color = colors['GREEN']
        else:
            self.current_color = colors['LIGHT PURPLE']

def color(char=None):
    if style == 'Random':
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    elif style == 'White':
        return (255, 255, 255)
    elif style == 'Matrix':
        return (0, 255, 0)
    elif style == 'Christmas':
        if char:
            return char.color
        else:
            return random.choice(styles[style])
    elif style == 'Rainbow':
        if char:
            try:
                return styles[style][styles[style].index(char.color)+1]
            except IndexError:
                return (255, 0, 255)
            except ValueError:
                return (255, 0, 255)
        else:
            return (255, 0, 255)
    else:
        return (255, 255, 255, 255)

def calc_x():
    # TODO Figure out why on different numbers, the screen isn't column locked
    if cell_lock:
        choices = [y*(window_x//number_of_columns) for y in range(number_of_columns)]
        x = random.choice(choices)
    else:
        x = random.randint(0, window_size[0])
    return x

def mouse_move(mouse_position):
    for button in style_selection_buttons:
        button.mouse_hover(mouse_position)

def on_click(mouse_click_position):
    new_style = ''
    for button in style_selection_buttons:
        if button.clicked(mouse_click_position):
            new_style = button.style_name
    return new_style

pygame.init()
surface = pygame.display.set_mode(window_size, flags=(pygame.FULLSCREEN))
pygame.display.set_caption('Matrix')

window_x = surface.get_width()
window_y = surface.get_height()
font = pygame.font.SysFont('consolas', char_size)
button_font = pygame.font.SysFont('consolas', int(window_size[0]/number_of_columns*3))

style_selection_buttons = []
for pos, (style_name, colorss) in enumerate(styles.items()):
    style_selection_buttons.append(Button(style_name, position=(pos * (window_x*.95//len(styles)), window_y-(window_y*.05))))

running = True
char_root_list = []
drop_wait = 0
while running:
    if spawn_rate >= 1:
        for _ in range(int(spawn_rate)):
            char_root_list.append(Char(calc_x(), 0-char_size, char_size, color=color()))
    else:
        if 1 / max(.1, spawn_rate) <= drop_wait:
            char_root_list.append(Char(calc_x(), 0-char_size, char_size, color=color()))
            drop_wait = 0
        else:
            drop_wait += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_RIGHT:
                # Decrease number of columns and increase character size
                if number_of_columns <= 1:
                    pass
                else:
                    number_of_columns -= 1
                    char_size = max(2, round(window_size[0] / max(1, number_of_columns)))
            elif event.key == K_LEFT:
                # Increase number of columns and decrease character size
                if number_of_columns >= window_size[0] / 2:
                    pass
                else:
                    number_of_columns += 1
                    char_size = max(2, round(window_size[0] / max(1, number_of_columns)))
            elif event.key == K_UP:
                if spawn_rate <= .1:
                    if spawn_rate <= .01:
                        pass
                    else:
                        spawn_rate -= .01
                else:
                    spawn_rate -= .1
            elif event.key == K_DOWN:
                if spawn_rate >= 20:
                    pass
                else:
                    spawn_rate += .1            
            font = pygame.font.SysFont('consolas', char_size)
            print(color(), number_of_columns, char_size)
        elif event.type == MOUSEBUTTONDOWN:
            """SCROLLING WILL INCREASE AND DECREASE SPEED"""
            if event.button == 5: # Wheel Down / Speed up
                if fps == 0:
                    pass
                elif fps > 240:
                    fps = 0
                else:
                    fps += 5
            elif event.button == 4: # Wheel Up / Slow down
                if fps == 0:
                    fps = 240
                elif fps < 10:
                    fps = 1
                else:
                    fps -= 5
            elif event.button == 1:
                style = on_click(pygame.mouse.get_pos())
        elif event.type == MOUSEMOTION:
            mouse_move(pygame.mouse.get_pos())
                
    prev_char_root_list = char_root_list[:]
    char_root_list = []

    # Create new character below each current character on screen
    for char in prev_char_root_list:
        # If character is offscreen, don't bother making another character
        if char.y < 0-char_size or char.x > window_x:
            continue
        new_char = Char(char.x, char.y+char_size, char_size, color=color(char))
        char_root_list.append(new_char)
        text = font.render(char.character, True, char.color)
        surface.blit(text, (char.x, char.y))

    for button in style_selection_buttons:
        pygame.draw.rect(surface, button.current_color, [button.top_left[0], button.top_left[1], button.width, button.height])
        button_text = button_font.render(button.style_name, True, colors['BLACK'])
        surface.blit(button_text, (button.top_left[0]+10, button.top_left[1]+5))
    
    pygame.display.update()
    fade = pygame.Surface((window_x, window_y))
    fade.set_alpha(fade_rate)
    surface.blit(fade, (0, 0))
    pygame.time.Clock().tick(fps)

pygame.quit()