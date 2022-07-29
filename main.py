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

from ga_functions import fitness

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
    labels = False # If Statistic labels should be shown
    running = True
    clock = pygame.time.Clock()

    t = 0
    dt = 0.01  # Delta time, amount to increase time by per iteration of sim
    duration = 10

    # entities.append(FCSquare((50, 50), 20, 50))

    weights = np.array([[ 0.32614771, -0.28483914,  0.34747939, -0.12279233, -0.50417765,
        -0.17541021],
       [ 0.41368913, -0.35156443, -0.02450417, -0.15905971, -0.13313408,
        -0.21988195],
       [ 0.3275578 ,  0.12976873, -0.1649671 , -0.08215002, -0.04344411,
         0.27552451],
       [-0.19081223,  0.23174393, -0.0293657 , -0.35042643,  0.50296365,
        -0.10969984],
       [ 0.11254286,  0.41495674, -0.33163494, -0.12005114,  0.02197439,
        -0.05631447],
       [-0.00706742, -0.55829957,  0.06676179,  0.3106291 , -0.46564181,
        -0.38705996]])

    entities.append(Reservoir((100, 100), 2, 50, weights, draw_parts=True))
    """
    weights = np.array([[-0.15965825, -0.04472828, -0.17489066, -0.14029823,  0.12123431, -0.19051437],
                        [-0.044062,    0.02782405,  0.09694456,  0.00077341, -0.02727581,  0.03902043],
                        [-0.18638232, -0.25393301, -0.17324981, -0.33858329, -0.39901128, -0.04866117],
                        [-0.1334979,  -0.35789833, -0.33544484, -0.36050979, -0.07933475, -0.20109482],
                        [-0.3933088,  -0.49376863, -0.28255998, -0.38948525, -0.52340934, -0.52738481],
                        [-0.00930335, -0.27436726, -0.04594403, -0.27503552, -0.16287371, -0.17164353]])

    entities.append(Reservoir((150, 50), 2, 50, weights))

    weights = np.array([[-0.15965825, -0.04472828, -0.17489066, -0.14029823,  0.12123431, -0.19051437],
                        [-0.044062,    0.02782405,  0.09694456,  0.00077341, -0.02727581,  0.03902043],
                        [ 0.01361768, -0.05393301,  0.02675019, -0.13858329, -0.19901128,  0.15133883],
                        [ 0.0665021,  -0.15789833, -0.13544484, -0.16050979,  0.12066525, -0.00109482],
                        [ 0.0066912,  -0.09376863,  0.11744002,  0.01051475, -0.12340934, -0.12738481],
                        [ 0.19069665, -0.07436726,  0.15405597, -0.07503552,  0.03712629,  0.02835647]])

    entities.append(Reservoir((250, 50), 2, 50, weights))

    
    entities.append(Reservoir((50, 150), 2, 50))
    entities.append(Reservoir((50, 250), 2, 50))

    entities.append(Reservoir((150, 150), 2, 50))
    entities.append(Reservoir((150, 250), 2, 50))

    entities.append(Reservoir((250, 150), 2, 50))
    entities.append(Reservoir((250, 250), 2, 50))
    """

    if animate:
        screen = pygame.display.set_mode((width, height))
        screen_setup(entities, screen)
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
    print(fitness(entities[0]))

def get_pos():
    """Get position of mouse cursor."""
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
    Screen to draw assets to.
    """
    global myfont, titlefont
    pygame.init()
    pygame.display.set_caption("Spring Damper")

    titlefont = pygame.font.SysFont("monospace", 20)
    myfont = pygame.font.SysFont("monospace", 15)

    update_screen(entities, screen)


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
            length = math.floor(length)
            label = myfont.render("{}".format(length), 1, SILVER)
            screen.blit(label, (1400, (150 + i * 50)))

        # Draw Spring Forces to Screen
        for i, force in enumerate(entities[0].get_spring_forces()):
            label = myfont.render("{}".format(force), 1, SILVER)
            screen.blit(label, (1500, (150 + i * 50)))

    pygame.display.update()


if __name__ == '__main__':
    main()