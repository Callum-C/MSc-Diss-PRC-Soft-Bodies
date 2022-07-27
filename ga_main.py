import pygame
import numpy as np
import math
import time

from classes.test_ent import Test
from classes.fc_square import FCSquare
from classes.reservoir import Reservoir
from ga_functions import fitness, mutate

(width, height) = (1800, 1200)
entities = []
titlefont = None
myfont = None


def main():
    running = True

    start_pos = (50, 50)

    dt = 0.01  # Delta time, amount to increase time by per iteration of sim
    duration = 10

    pop_size = 6  # Population Size
    num_of_gens = 100  # Number of generations to perform
    num_of_mutations = 3
    global_stats = None

    init_pop = create_init_pop(pop_size, start_pos, 2, 50)
    population = [init_pop]

    # Perform GA
    for gen in range(num_of_gens):
        run_sim_once(population[gen], duration, dt)
        stats = assess_gen_fitness(population[gen])

        # Perform Selection


        global_stats = track_all_stats(stats, global_stats)

    running = False



def create_init_pop(pop_size, start_pos, size=2, spacing=50):
    """
    Create random initial population.

    Params
    ------
    pop_size: int
    Population size

    start_pos: tuple(int, int)
    starting position of reservoir entity

    size: int
    size of reservoir entity, 2 here makes 2x2 square

    spacing: int
    space between particles at rest

    Returns
    -------
    init_pop: list(Reservoir)
    List of Reservoir entities for initial population
    """

    init_pop = []
    for i in range(pop_size):
        init_pop.append(Reservoir(start_pos, size, spacing))

    return init_pop


def run_sim_once(generation, duration, dt):
    """
    Run simulation once.

    Params
    ------
    generation: list(Reservoir)
    The generation to perform the simulation with

    duration: int
    Duration of simulation

    dt: float
    delta t, amount to increase time by per iteration
    """

    t = 0
    while t < duration:
        for pheno in generation:
            pheno.step(dt)  # Step controller
            pheno.update(dt)  # Update "physical" body
        # Increment Time
        t += dt


def assess_gen_fitness(generation):
    """
    Assess Fitness of a Generation

    Params
    ------
    generation: list(Reservoir)
    Generation of Reservoir entities

    Returns
    -------
    stats: dict("avg", "max_fit", "fittest_pheno")
    The generation fitness statistics
    """

    max_gen_fit = 0
    fittest_pheno = None
    running_total = None
    size = len(generation)

    for pheno in generation:
        fit = fitness(pheno)

        if pheno is not None:
            running_total += fit
        else:
            max_gen_fit = fit
            fittest_pheno = pheno
            running_total = fit

        if fit > max_gen_fit:
            max_gen_fit = fit
            fittest_pheno = pheno

    avg_fit = running_total / size
    stats = {"avg": avg_fit, "max_fit": max_gen_fit, "fittest_pheno": fittest_pheno}

    return stats


def track_all_stats(gen_stats, global_stats):
    """
    Tracks all statistics.

    Params
    ------
    gen_stats: dict
    Dictionary of all statistics for a SINGLE generation

    global_stats: dict
    Dictionary of all statistics for ALL generations

    Returns
    -------
    global_stats: dict
    Dictionary of global statistics
    """

    if global_stats is not None:
        for key, value in gen_stats:
            global_stats[key].append(value)
    else:
        # Initialise Global Stats
        global_stats = {}
        for key, value in gen_stats:
            global_stats[key] = [value]

    return global_stats


if __name__ == '__main__':
    main()
