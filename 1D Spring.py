from typing import get_origin
import pygame
import numpy as np

# Visual Params
FILL =      (45, 197, 244)
BACKGROUND_COLOR = (112, 50, 126)
(width, height) = (1280, 720)

def main():
    bob = (300, 300)    # (x, y)
    anchor = (300, 100) # (x, y)
    rest_length = 150
    k = 0.01
    velocity = 0
    force = 0

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((width, height))
    screen_setup(bob, anchor, screen)

    running = True
    while running:
        clock.tick(60)
        spring_length = bob[1] - anchor[1]  # Only subtract y values
        x = spring_length - rest_length     # Spring Displacement
        force = -1 * k * x
        velocity += force
        bob = (bob[0], bob[1] + velocity) 

        velocity = velocity * 0.99

        update_screen(bob, anchor, screen)

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                y = move_bob()
                bob = (bob[0], y)
                velocity = 0
                update_screen(bob, anchor, screen)

            if event.type == pygame.QUIT:
                running = False

def move_bob():
    pos = get_pos()
    y = pos[1]
    return y

def get_pos():
    pos = pygame.mouse.get_pos()
    return (pos)

def screen_setup(bob, anchor, screen):
    """Initialise PyGame screen and draw initial state."""

    pygame.init()
    pygame.display.set_caption("Spring Damper")
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.circle(screen, FILL, bob, 35)
    pygame.draw.line(screen, FILL, bob, anchor, 2)

    pygame.display.update()
    

def update_screen(bob, anchor, screen):
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.circle(screen, FILL, bob, 35)
    pygame.draw.line(screen, FILL, bob, anchor, 2)

    pygame.display.update()

if __name__ == '__main__':
    main()