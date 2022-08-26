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
from classes.triangle import Triangle
from classes.hydrostat_square import HydrostatSquare
from classes.hydrostat_reservoir import HydrostatReservoir

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

    weights = np.array([ 0.01148868,  0.36345918, -0.37036079, -0.12249748, -0.19381718,
       -0.10039645, -0.32867016,  0.30267763,  0.1067658 , -0.20407097,
        0.49636033,  0.16172169,  0.10021826, -0.0529937 ,  0.21998345,
        0.13670042,  0.38955941, -0.24837196,  0.22976312, -0.33715404,
        0.11442199,  0.32122475,  0.25079812, -0.48430318,  0.42448847,
        0.41699952,  0.00604483, -0.01746959,  0.05798429, -0.16880338,
        0.30944573, -0.06820881,  0.04961575, -0.01480511, -0.29537161,
       -0.04652879, -0.02201981,  0.11896809,  0.14194448,  0.07438135,
       -0.27003187, -0.46667697,  0.21622401, -0.03840825,  0.48656198,
        0.28137467,  0.35874385, -0.40486041, -0.36902631,  0.30167248,
       -0.50438389,  0.19454068,  0.42287862,  0.14741932,  0.46223342,
        0.38626055, -0.3045814 , -0.35176172, -0.3769118 , -0.394805  ,
       -0.32026751, -0.05143512,  0.18437142,  0.47550242])

    entities.append(HydrostatSquare((250, 250), 100,  300, draw_parts=True))
    # entities.append(HydrostatReservoir((600, 600), 50, 20, weights=weights, draw_parts=True))

    # entities.append(Reservoir((100, 100), 2, 50, draw_parts=True))
    """
    entities.append(HydrostatReservoir((100, 200), 50, draw_parts=False))

    entities.append(HydrostatReservoir((200, 100), 50, draw_parts=False))

    entities.append(HydrostatReservoir((200, 200), 50, draw_parts=False))

    entities.append(HydrostatReservoir((200, 300), 50, draw_parts=False))

    entities.append(HydrostatReservoir((100, 300), 50, draw_parts=False))

    entities.append(HydrostatReservoir((300, 100), 50, draw_parts=False))

    entities.append(HydrostatReservoir((300, 200), 50, draw_parts=False))

    entities.append(HydrostatReservoir((300, 300), 50, draw_parts=False))
    """

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
            label = myfont.render("Area: {}".format(entities[0].get_area()), 1, SILVER)
            screen.blit(label, (1400, 150))

            label = myfont.render("Pressure: {}".format(entities[0].get_fluid_pressure()), 1, SILVER)
            screen.blit(label, (1400, 200))

            label = myfont.render("Center Position: {}".format(entities[0].get_center()), 1, SILVER)
            screen.blit(label, (1400, 250))

        # Draw Spring Lengths to Screen
        for i, length in enumerate(entities[0].get_spring_lengths()):
            try:
                length = math.floor(length)
            except:
                None
            label = myfont.render("{}".format(length), 1, SILVER)
            screen.blit(label, (1400, (300 + i * 50)))

        # Draw Spring Forces to Screen
        for i, force in enumerate(entities[0].get_spring_forces()):
            label = myfont.render("{}".format(force), 1, SILVER)
            screen.blit(label, (1500, (300 + i * 50)))

    pygame.display.update()


if __name__ == '__main__':
    main()