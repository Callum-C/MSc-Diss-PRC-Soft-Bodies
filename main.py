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
from classes.hydrostat_triangle import HydrostatTriangle
from classes.hydrostat_square import HydrostatSquare

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
    labels = True  # If Statistic labels should be shown
    running = True
    clock = pygame.time.Clock()

    t = 0
    dt = 0.05  # Delta time, amount to increase time by per iteration of sim
    duration = 500

    weights = np.array([ 0.1113417 , -0.01567203, -0.33429351, -0.02081124, -0.0743839 ,
        0.02462345, -0.4359338 , -0.41623522, -0.38436757,  0.29092453,
       -0.02022829, -0.23686904,  0.39088547, -0.40872139, -0.2109282 ,
        0.06772556, -0.55308473, -0.1240209 , -0.15141219, -0.10461958,
       -0.03416356,  0.37798783, -0.11059116, -0.34009464,  0.4033937 ,
       -0.218228  , -0.09044993,  0.37342249,  0.43275193,  0.20557787,
        0.41581972, -0.46492424,  0.36992228, -0.30410626,  0.24705637,
        0.41379982])

    #  entities.append(Reservoir((100, 100), 2, 50, weights, draw_parts=True))

    # entities.append(HydrostatTriangle((250, 250), 100))
    entities.append(HydrostatSquare((250, 250), 100, True))

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

    # print(entities[0].get_distance())
    # print(fitness_function(entities[0]))


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

        if entities[0].has_area:
            area = entities[0].calc_area()
            label = myfont.render("Area: {}".format(area), 1, SILVER)
            screen.blit(label, (1400, 150))

        # Draw Spring Lengths to Screen
        for i, length in enumerate(entities[0].get_spring_lengths()):
            try:
                length = math.floor(length)
            except:
                None
            label = myfont.render("{}".format(length), 1, SILVER)
            screen.blit(label, (1400, (250 + i * 50)))

        # Draw Spring Forces to Screen
        for i, force in enumerate(entities[0].get_spring_forces()):
            label = myfont.render("{}".format(force), 1, SILVER)
            screen.blit(label, (1500, (250 + i * 50)))

    pygame.display.update()


if __name__ == '__main__':
    main()