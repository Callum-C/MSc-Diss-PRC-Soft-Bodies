import pygame
import numpy as np

from colours import FILL, SILVER, BACKGROUND_COLOUR

from Classes.Particle import Particle
from Classes.Spring import Spring
from Classes.Square import Square

# Visual Params

(width, height) = (1280, 720)


def main():
    clock = pygame.time.Clock()

    bob = Square((200, 100), 5, 100, SILVER)

    screen = pygame.display.set_mode((width, height))
    screen_setup(bob, screen)

    pygame.display.update()

    running = True
    count = 0
    while running:
        clock.tick(30)

        if count > 120:
            bob.update()

        update_screen(bob, screen)

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                NotImplemented

            if event.type == pygame.QUIT:
                max_force = bob.get_max_force()
                min_force = bob.get_min_force()
                print("Min Force: {} Max Force: {}".format(min_force, max_force))
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

    screen.fill(BACKGROUND_COLOUR)

    bob.draw(screen)

    # pygame.draw.rect(screen, SILVER, pygame.Rect(200, 100, 400, 400), 2)

    pygame.display.update()


if __name__ == '__main__':
    main()
