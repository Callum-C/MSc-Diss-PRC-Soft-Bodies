import pygame
import numpy as np

from colours import FILL, SILVER, BACKGROUND_COLOUR

from Classes.Particle import Particle
from Classes.Spring import Spring
from Classes.Square import Square
from Classes.C_Elegen import C_Elegen

# Visual Params

(width, height) = (1280, 720)
entities = []

def main():
    clock = pygame.time.Clock()

    elegen = C_Elegen((200, 100), 7, 100)
    entities.append(elegen)


    screen = pygame.display.set_mode((width, height))
    screen_setup(entities, screen)

    pygame.display.update()

    running = True
    count = 0
    while running:
        clock.tick(30)

        if count > 120:
            for e in entities:
                e.update()

        update_screen(entities, screen)

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                elegen.unlock_head()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = get_pos()
                elegen.move_to_cursor(pos)
                elegen.lock_head()

            if event.type == pygame.QUIT:
                running = False
        count += 1


def get_pos():
    pos = pygame.mouse.get_pos()
    pos = (float(pos[0]), float(pos[1]))
    return (pos)


def screen_setup(entities, screen):
    """
    Initialise pygame screen and draw initial state.
    
    Params
    ------

    entities: list
    List of entity objects.

    screen: Pygame Screen
    Screent to draw assets to.
    """

    pygame.init()
    pygame.display.set_caption("Spring Damper")

    update_screen(entities, screen)


def update_screen(entities, screen):
    """
    Update screen, called every frame.
    
    Params
    ------

    entities: list
    List of entity objects.

    screen: Pygame Screen
    Screen to draw assets to.
    """

    screen.fill(BACKGROUND_COLOUR)

    for e in entities:
        e.draw(screen)

    # pygame.draw.rect(screen, SILVER, pygame.Rect(200, 100, 400, 400), 2)

    pygame.display.update()


if __name__ == '__main__':
    main()
