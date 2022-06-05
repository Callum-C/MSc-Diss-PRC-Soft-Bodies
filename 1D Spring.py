from turtle import position
from typing import get_origin
import pygame
import numpy as np

# Visual Params
FILL =      (45, 197, 244)
BACKGROUND_COLOR = (112, 50, 126)
(width, height) = (1280, 720)
def main():
    bob = np.array((640.0, 400.0))    # (x, y)
    anchor = np.array((640.0, 360.0)) # (x, y)
    gravity = np.array((0.0, 0.4))

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

        spring_vector = bob - anchor
        spring_length = np.linalg.norm(spring_vector)
        x = spring_length - rest_length     # Spring Displacement

        v_hat = 0
        if spring_length != 0:
            v_hat = spring_vector / spring_length   # Unit vector 

        force = -1 * ((k * x) * v_hat)

        velocity += force
        velocity += gravity
        bob += velocity

        velocity = velocity * 0.99

        update_screen(bob, anchor, screen)

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                pos = get_pos()
                bob = np.array(pos)
                velocity = 0
                update_screen(bob, anchor, screen)

            if event.type == pygame.QUIT:
                running = False

def get_pos():
    pos = pygame.mouse.get_pos()
    pos = (float(pos[0]), float(pos[1]))
    return (pos)

def screen_setup(bob, anchor, screen):
    """Initialise PyGame screen and draw initial state."""

    pygame.init()
    pygame.display.set_caption("Spring Damper")
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.circle(screen, FILL, bob, 32)
    pygame.draw.circle(screen, FILL, anchor, 16)
    pygame.draw.line(screen, FILL, bob, anchor, 2)

    pygame.display.update()
    

def update_screen(bob, anchor, screen):
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.circle(screen, FILL, bob, 32)
    pygame.draw.circle(screen, FILL, anchor, 16)
    pygame.draw.line(screen, FILL, bob, anchor, 2)

    pygame.display.update()

if __name__ == '__main__':
    main()