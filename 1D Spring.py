from typing import get_origin
import pygame
import numpy as np

# Visual Params
FILL =      (45, 197, 244)
BACKGROUND_COLOR = (112, 50, 126)
(width, height) = (1280, 720)

def main():
    y = 200
    rest_length = 150
    k = 0.01
    velocity = 0
    force = 0

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((width, height))
    screen_setup(y, screen)

    running = True
    while running:
        clock.tick(60)
        x = y - rest_length
        force = -1 * k * x
        velocity += force
        y += velocity 

        velocity = velocity * 0.99

        update_screen(y, screen)

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                y = move_bob(screen)
                velocity = 0
                update_screen(y, screen)

            if event.type == pygame.QUIT:
                running = False

def move_bob(screen):
    pos = get_pos()
    y = pos[1]
    return y


def get_pos():
    pos = pygame.mouse.get_pos()
    return (pos)

def screen_setup(y, screen):
    """Initialise PyGame screen and draw initial state."""

    pygame.init()
    pygame.display.set_caption("Spring Damper")
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.circle(screen, FILL, (300, y), 35)
    pygame.draw.line(screen, FILL, (300, y), (300, 0), 2)

    pygame.display.update()
    

def update_screen(y, screen):
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.circle(screen, FILL, (300, y), 35)
    pygame.draw.line(screen, FILL, (300, y), (300, 0), 2)

    pygame.display.update()

if __name__ == '__main__':
    main()