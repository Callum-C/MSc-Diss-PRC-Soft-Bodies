import pygame
import numpy as np
import math
import time

from colours import FILL, SILVER, BACKGROUND_COLOUR, RED

from classes.particle import Particle
from classes.spring import Spring
from classes.square import Square
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
    labels = False  # If Statistic labels should be shown
    running = True
    clock = pygame.time.Clock()

    t = 0
    dt = 0.05  # Delta time, amount to increase time by per iteration of sim
    duration = 500

    weights = np.array([-2.47027064e-01, -2.31041286e-01, -8.35632625e-04, -3.10527290e-01,
        3.03539674e-01, -3.92647070e-01,  1.62469162e-01, -2.70795159e-02,
       -1.63053023e-01,  7.61070736e-02,  1.10917383e-02, -1.48215552e-01,
        1.36703866e-01,  4.00459564e-02,  1.04855317e-01, -1.06095560e-01,
       -1.68312607e-01,  9.22871293e-02,  1.76435431e-01,  1.68265312e-01,
        3.26200747e-03,  1.00085597e-01,  4.33514662e-01,  5.68545924e-02,
       -4.01225031e-01, -3.64055776e-01,  5.46908291e-03,  1.82082415e-01,
       -3.70119624e-01,  3.65413810e-02,  7.87216431e-02,  1.21222283e-01,
        1.54661952e-01,  1.78266980e-01, -5.53578469e-02,  4.96124108e-01,
       -5.25804533e-02, -1.88703479e-02,  3.74126127e-01,  2.74042676e-02,
       -2.22844296e-01,  5.86348954e-02,  4.81526790e-01, -1.47459900e-01,
       -2.66958777e-01,  2.61106839e-02,  5.09496073e-01,  4.12463675e-02,
       -2.95111295e-01,  2.21134645e-01,  1.90525648e-03,  7.49078311e-02,
       -2.17365571e-01, -1.32705305e-01,  4.84282159e-01, -7.69995358e-02,
       -3.88406917e-01, -7.15802466e-02,  1.91432733e-04, -1.09843124e-01,
       -2.28291041e-01,  1.23660946e-01,  3.78289661e-01, -3.34272218e-02])

    #entities.append(HydrostatSquare((500, 500), 50,  0.01, draw_parts=True))  # 5000 Pressure breaks the springs
    entities.append(HydrostatReservoir((500, 50), 50, 40, weights=weights, draw_parts=True))
    """
    Init = HydrostatSquare((500, 500), 50, 40, draw_parts=True)
    entities.append(Init)
    for i in range(1, 10):
        tl = entities[i - 1].get_tr_particle()
        bl = entities[i - 1].get_br_particle()
        tlbl = entities[i - 1].get_right_spring()

        entities.append(HydrostatSquare((500 + i * 50, 500), 50, 40, draw_parts=True,
                                        tl=tl, bl=bl, spring_tlbl=tlbl))

"""
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
