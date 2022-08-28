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

    weights = np.array([-0.07786255, -0.10458034, -0.33304497,  0.3330691 ,  0.18681488,
       -0.33448513,  0.37388125, -0.01162207, -0.42684953, -0.08373324,
        0.01079516,  0.0150961 , -0.16305547, -0.0890706 ,  0.06958446,
       -0.19676572, -0.41773044, -0.17866076,  0.00671605, -0.15380785,
       -0.26732384, -0.11798017, -0.10275461,  0.00575364,  0.15833623,
        0.45296068, -0.39745243,  0.21381208, -0.48153107, -0.14268276,
       -0.20946224,  0.24590995,  0.11760261, -0.179807  , -0.46621357,
       -0.07669686,  0.18377087, -0.12203799, -0.45129657, -0.25540809,
        0.49178173,  0.04737897, -0.48463273, -0.23553345,  0.36738805,
       -0.21129482, -0.23299562,  0.3462169 , -0.27114004,  0.14366488,
        0.15916519, -0.06729734, -0.44745173, -0.23328316, -0.05011673,
       -0.45391369, -0.26387427,  0.31240904, -0.28882449, -0.4086629 ,
        0.33750432,  0.05087124, -0.48633877,  0.28195838])

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
