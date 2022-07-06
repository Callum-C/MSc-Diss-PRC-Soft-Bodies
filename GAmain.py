import pygame
import numpy as np

from colours import FILL, SILVER, BACKGROUND_COLOUR

from Classes.Particle import Particle
from Classes.Spring import Spring
from Classes.Square import Square
from Classes.C_Elegen import C_Elegen
from Classes.Genotype import Genotype
from Classes.LocomotionGA import GeneticAlgorithm

# Visual Params

(width, height) = (1280, 720)
entities = []


def main():
    clock = pygame.time.Clock()

    GA = GeneticAlgorithm((200, 100), 100, 2, 300)
    _, a_lock, b_lock = GA.run_ga()
    print("A Lock: {} B Lock: {}".format(a_lock, b_lock))

    geno = Genotype((200, 100), 100, a_lock, b_lock)
    entities.append(geno)

    screen = pygame.display.set_mode((width, height))
    screen_setup(entities, screen)

    pygame.display.update()

    running = True
    count = 0
    while running:
        clock.tick(30)

        for e in entities:
            e.update(count)

        update_screen(entities, screen)

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                NotImplemented

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = get_pos()

            if event.type == pygame.QUIT:
                running = False

        if count == 50:
            count = 0
        else:
            count += 1


def get_pos():
    pos = pygame.mouse.get_pos()
    pos = (float(pos[0]), float(pos[1]))
    return pos


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
