import pygame
import numpy as np

from Classes.Particle import Particle
from Classes.Spring import Spring
from Classes.Square import Square

# Visual Params
FILL =      (45, 197, 244)
PURP =      (230,230,250)
BACKGROUND_COLOR = (112, 50, 126)
(width, height) = (1280, 720)

def main():
    clock = pygame.time.Clock()

    bob = Square((200, 100), 5, 50, FILL)

    screen = pygame.display.set_mode((width, height))
    screen_setup(bob, screen)

    pygame.display.update()

    running = True
    count = 0
    while running:
        clock.tick(60)

        if count > 120:
            bob.update()

        update_screen(bob, screen)

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                NotImplemented

            if event.type == pygame.QUIT:
                running = False
        count += 1

def get_pos():
    pos = pygame.mouse.get_pos()
    pos = (float(pos[0]), float(pos[1]))
    return (pos)

def screen_setup(bob, screen):
    """Initialise pygame screen and draw initial state."""

    pygame.init()
    pygame.display.set_caption("Spring Damper")

    update_screen(bob, screen) 

def update_screen(bob, screen):
    """Update screen, called every frame."""

    screen.fill(BACKGROUND_COLOR)

    bob.draw(screen)

    pygame.draw.rect(screen, PURP, pygame.Rect(200, 100, 400, 400), 2)

    pygame.display.update()

if __name__ == '__main__':
    main()