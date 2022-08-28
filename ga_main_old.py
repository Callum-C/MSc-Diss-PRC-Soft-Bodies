import pygame
import numpy as np
import math
from random import randrange
import copy

from colours import FILL, SILVER, BACKGROUND_COLOUR, RED

from ga_functions import mutate, fitness_function

from classes.particle import Particle
from classes.spring import Spring
from classes.square import Square
from classes.test_ent import Test
from classes.fc_square import FCSquare
from classes.reservoir import Reservoir

(width, height) = (1800, 1200)
entities = []
titlefont = None
myfont = None


def main():
    """Run Locomotion Genetic Algorithm."""
    start_point = (50, 50)
    dt = 0.01  # Delta time, amount to increase time by per iteration of sim
    duration = 10

    num_mutations = 1
    pop_size = 6  # Needs to be even numbers due to j+1 notation
    generations = 3000
    fits = np.zeros((generations, pop_size))

    "Make Initial pop - population[0]"
    population = []
    init_pop = []
    for i in range(pop_size):
        init_pop.append(Reservoir(start_point, 2, 50))
    population.append(init_pop)
    print(population[-1][1].get_weights())

    for i in range(generations):
        next_gen = []  # Next generation
        print("Performing Generation: {}".format(i))

        "Perform Simulation"
        t = 0
        while t < duration:
            for e in population[i]:
                e.step(dt)
                e.update(dt)
            # Increment Time
            t += dt

        "Evaluate Generation"
        for j in range(0, pop_size, 2):
            curr_pop = copy.deepcopy(population[i])

            Ai = randrange(0, len(curr_pop))
            A = curr_pop[Ai]
            curr_pop.remove(A)

            Bi = randrange(0, len(curr_pop))
            B = curr_pop[Bi]
            curr_pop.remove(B)

            # Assess Fitness
            Afit = fitness_function(A)
            Bfit = fitness_function(B)

            # Store Fitness
            fits[i][j] = Afit
            fits[i][j+1] = Bfit

            mutations = {'orig': [], 'orig_fit': [], 'mutant': []}

            if i < (generations-1):
                # Perform Selection

                if Afit > Bfit:
                    if j == 0:
                        f = open("GA-Training.txt", "a")
                        f.write("Fitness: {} Weights: {} \n\n".format(Afit, A.get_weights()))
                        f.close()

                    next_gen.append(Reservoir(start_point, 2, 50, A.get_weights()))
                    weights = mutate(A.get_weights(), num_mutations)
                    Bm = Reservoir(start_point, 2, 50, weights)
                    mutations['orig'].append(B)
                    mutations['orig_fit'].append(Bfit)
                    mutations['mutant'].append(Bm)

                else:
                    if j == 0:
                        f = open("GA-Training.txt", "a")
                        f.write("Fitness: {} Weights: {} \n\n".format(Afit, A.get_weights()))
                        f.close()

                    next_gen.append(Reservoir(start_point, 2, 50, B.get_weights()))
                    weights = mutate(B.get_weights(), num_mutations)
                    Am = Reservoir(start_point, 2, 50, weights)
                    mutations['orig'].append(A)
                    mutations['orig_fit'].append(Afit)
                    mutations['mutant'].append(Am)

        t = 0
        while t < duration:
            for e in mutations['mutant']:
                e.step(dt)
                e.update(dt)
            # Increment Time
            t += dt

        for k, mutant in enumerate(mutations['mutant']):
            orig = mutations['orig'][k]
            orig_fit = mutations['orig_fit'][k]

            if fitness_function(mutant) > orig_fit:
                next_gen.append(Reservoir(start_point, 2, 50, mutant.get_weights()))
            else:
                next_gen.append(Reservoir(start_point, 2, 50, orig.get_weights()))

        population.append(next_gen)
        total = sum(fits[i])
        max_fit = max(fits[i])
        avg = total / pop_size
        print(" - Avg Fitness: {} Max Fitness: {}\n".format(avg, max_fit))

    running = False
    print(fits[-1])
    print(population[-2][1].get_weights())
    # print(entities[0].get_distance())


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