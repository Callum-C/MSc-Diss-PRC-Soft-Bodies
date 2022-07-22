import pygame
import numpy as np
import math

from colours import FILL, SILVER, BACKGROUND_COLOUR, RED

from Classes.Particle import Particle
from Classes.Spring import Spring
from Classes.Square import Square
from Classes.C_Elegen import CElegen
from Classes.TestEnt import Test
from Classes.FC_Square import FCSquare

(width, height) = (1800, 900)
entities = []
titlefont = None
myfont = None


def main():
    animate = True
    running = True
    clock = pygame.time.Clock()

    t = 0
    dt = 0.01  # Delta time, amount to increase time by per iteration of sim
    duration = 150

    entities.append(FCSquare((50, 50), 6, 75, SILVER))

    if animate:
        screen = pygame.display.set_mode((width, height))
        screen_setup(entities, screen)
        pygame.display.update()

    while t < duration and running:
        if animate:
            clock.tick(144)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

        for e in entities:
            e.update(dt)

        if animate:
            update_screen(entities, screen)

        # Increment Time
        t += dt

    running = False

def get_pos():
    """Get position of mouse cursor."""
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
    Screen to draw assets to.
    """
    global myfont, titlefont
    pygame.init()
    pygame.display.set_caption("Spring Damper")

    titlefont = pygame.font.SysFont("monospace", 20)
    myfont = pygame.font.SysFont("monospace", 15)

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

    """
    title = titlefont.render("Spring Lengths and Forces", 5, SILVER)
    screen.blit(title, (1400, 100))
    
    # Draw Spring Lengths to Screen
    for i, length in enumerate(entities[0].get_spring_lengths()):
        length = math.floor(length)
        label = myfont.render("{}".format(length), 1, SILVER)
        screen.blit(label, (1400, (150 + i * 50)))

    # Draw Spring Forces to Screen
    for i, force in enumerate(entities[0].get_spring_forces()):
        label = myfont.render("{}".format(force), 1, SILVER)
        screen.blit(label, (1500, (150 + i * 50)))
    """

    pygame.display.update()




if __name__ == '__main__':
    main()