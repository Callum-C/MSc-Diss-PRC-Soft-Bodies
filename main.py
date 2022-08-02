import pygame
import numpy as np
import math
import time

from colours import FILL, SILVER, BACKGROUND_COLOUR, RED

from classes.particle import Particle
from classes.spring import Spring
from classes.square import Square
from classes.c_elegen import CElegen
from classes.test_ent import Test
from classes.fc_square import FCSquare
from classes.reservoir import Reservoir

from ga_functions import fitness_function

(width, height) = (1800, 1200)
entities = []
titlefont = None
myfont = None


def main():
    """
    Code Inspirations:
    Situsim - Chris Johnson
        - Simulation to PyGame interaction
    """

    animate = True
    labels = True # If Statistic labels should be shown
    running = True
    clock = pygame.time.Clock()

    t = 0
    dt = 0.01  # Delta time, amount to increase time by per iteration of sim
    duration = 100

    weights = np.array([ 0.26464369, -0.13888123, -0.4966466 ,  0.14680064,  0.10995252,
       -0.4791615 ,  0.22543148,  0.29673954,  0.27456666,  0.0019056 ,
       -0.02352004, -0.16383139,  0.44572589,  0.15125114,  0.12270445,
        0.23608383, -0.14464199,  0.01276045,  0.21775858, -0.41729467,
       -0.16233837,  0.17911   ,  0.35181613,  0.47890564,  0.2238786 ,
        0.13087408,  0.08967999,  0.27383116,  0.02615911, -0.38770578,
       -0.04380034, -0.40060928, -0.26762863,  0.16472093, -0.35041787,
       -0.4397554 ])

    entities.append(Reservoir((100, 100), 2, 50, weights, draw_parts=True))

    if animate:
        screen = pygame.display.set_mode((width, height))
        screen_setup(entities, screen, labels)
        pygame.display.update()
        time.sleep(2)

    while t < duration and running:
        if animate:
            clock.tick(144)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if entities[0].has_head():
                            pos = get_pos()
                            entities[0].move_to_cursor(pos)

                    if event.button == 3:
                        print(entities[0].get_distance())

        for e in entities:
            e.step(dt)
            e.update(dt)

        if animate:
            update_screen(entities, screen, labels)

        # Increment Time
        t += dt

    running = False

    print(entities[0].get_distance())
    print(fitness_function(entities[0]))


def get_pos():
    """Get position of mouse cursor."""
    pos = pygame.mouse.get_pos()
    pos = (float(pos[0]), float(pos[1]))
    return pos


def screen_setup(entities, screen, labels=False):
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

    update_screen(entities, screen, labels)


def update_screen(entities, screen, labels=False):
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

    if labels:
        title = titlefont.render("Spring Lengths and Forces", 5, SILVER)
        screen.blit(title, (1400, 100))

        # Draw Spring Lengths to Screen
        for i, length in enumerate(entities[0].get_spring_lengths()):
            try:
                length = math.floor(length)
            except:
                None
            label = myfont.render("{}".format(length), 1, SILVER)
            screen.blit(label, (1400, (150 + i * 50)))

        # Draw Spring Forces to Screen
        for i, force in enumerate(entities[0].get_spring_forces()):
            label = myfont.render("{}".format(force), 1, SILVER)
            screen.blit(label, (1500, (150 + i * 50)))

    pygame.display.update()


if __name__ == '__main__':
    main()