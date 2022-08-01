import time
import pygad
import numpy as np
import math
import random
from random import randrange

from classes.reservoir import Reservoir


def main():
    start_pos = (50, 50)

    pop_size = 100
    num_of_gens = 10

    max_weight = 1
    size = 2
    spacing = 50

    # pygad init variables:
    parent_selection_type = "sss"
    keep_parents = 1
    crossover_type = "single_point"
    mutation_type = "random"
    mutation_probability = 0.5

    init_pop = pygad_init_pop(pop_size, 6, max_weight)

    ga_instance = pygad.GA(num_generations=num_of_gens,
                           num_parents_mating=pop_size,
                           fitness_func=pygad_fitness,
                           initial_population=init_pop,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_probability=mutation_probability,
                           callback_generation=callback_gen,
                           parallel_processing=['process', 8])

    ga_instance.run()

    print(ga_instance.best_solution())


def pygad_init_pop(pop_size, spring_count=6, max_weight=0.5):
    """
    Create random initial population for pygad.

    Params
    ------
    pop_size: int
    Population size

    spring_count: int
    number of springs entity will have - 4 particles - 6 springs

    max_weight: float
    The max weight size to initially randomize - 0.5 here yields weights -0.5 to 0.5

    Returns
    -------
    init_pop: np.array(pop_size, weight_matrix)
    array of weights to create a population of reservoirs
    """

    init_pop = np.zeros((pop_size, spring_count ** 2))
    for i in range(pop_size):
        init_pop[i] = np.random.uniform(-max_weight, max_weight, (spring_count, spring_count)).flatten()
    return init_pop


def callback_gen(ga_instance):
    print("Generation : ", ga_instance.generations_completed)
    print("Fitness of the best solution :", ga_instance.best_solution()[1])


def pygad_fitness(solution, solution_idx):
    """Fitness function for GA in Pygad."""

    duration = 10
    dt = 0.01
    start_pos = (50, 50)
    size = 2
    spacing = 50

    weights = solution.reshape(6, 6)  # Reshape weights to (spring_count, spring_count)
    res = Reservoir(start_pos, size, spacing, weights)

    run_sim_once(res, duration, dt)

    distance = res.get_distance()
    broken = res.get_broken_springs()

    return distance - (5000 * broken)


def run_sim_once(res, duration, dt):
    """
    Run simulation once.

    Params
    ------
    res: Reservoir
    The reservoir entity to perform a simulation on

    duration: int
    Duration of simulation

    dt: float
    delta t, amount to increase time by per iteration
    """

    t = 0
    while t < duration:
        res.step(dt)  # Step controller
        res.update(dt)  # Update "physical" body
        # Increment Time
        t += dt


if __name__ == '__main__':
    main()