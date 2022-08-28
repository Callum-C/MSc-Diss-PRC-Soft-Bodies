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
    labels = True  # If Statistic labels should be shown
    running = True
    clock = pygame.time.Clock()

    t = 0
    dt = 0.05  # Delta time, amount to increase time by per iteration of sim
    duration = 500

    weights = np.array([-0.19751962, -0.11810784, -0.39437976,  0.01924451, -0.29481724,
       -0.42188617, -0.17610861, -0.32882354, -0.41836879,  0.31076775,
       -0.39214451, -0.00417202, -0.13055731, -0.24964642,  0.03609906,
       -0.06448757, -0.44423081, -0.17440527, -0.39037926, -0.07695319,
        0.38543742,  0.34886577, -0.08897331,  0.16183839, -0.37567446,
       -0.37468406, -0.4955103 , -0.24285253, -0.09782435,  0.37390702,
       -0.20184409,  0.44638911, -0.20909938, -0.49177521,  0.33452371,
       -0.18993387, -0.02471582, -0.12661276, -0.11943181, -0.39840228,
        0.47404478, -0.45731435,  0.00877242, -0.19620082, -0.42285934,
       -0.24357615, -0.36875013,  0.23987109, -0.29030067, -0.1149457 ,
       -0.42760117, -0.036378  ,  0.25198915, -0.19018495, -0.06795525,
        0.07764397, -0.09845772, -0.21547351, -0.44903891, -0.12641612,
        0.39140017,  0.4349442 ,  0.12813137, -0.47550478])

    #entities.append(HydrostatSquare((500, 500), 50,  0.01, draw_parts=True))  # 5000 Pressure breaks the springs
    entities.append(HydrostatReservoir((600, 600), 50, 0.03, weights=weights, draw_parts=True))
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
