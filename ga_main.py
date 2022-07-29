import numpy as np
import math
import random
from random import randrange
import os

from classes.reservoir import Reservoir
from ga_functions import fitness_function, mutate_locus, make_file

(width, height) = (1800, 1200)
entities = []
titlefont = None
myfont = None

def main():
    """
    Code inspirations:

    Microbial GA ECAL2009 - Inmanh (In Reading Directory)
        - GA Selection Method
    """

    running = True

    start_pos = (50, 50)

    dt = 0.01  # Delta time, amount to increase time by per iteration of sim
    duration = 25

    pop_size = 100  # Population Size
    num_of_gens = 2000  # Number of generations to perform
    global_stats = None

    max_weight = 0.1
    size = 2
    spacing = 50

    method_params = {"method": "Microbial", "sim_duration": duration, "fitness_func": "Fitness_Day3",
                     "pop_size": pop_size, "gen_size": num_of_gens, "weight_search": max_weight}
    file = make_file(method_params)

    init_pop = create_init_pop(pop_size, start_pos, max_weight, size, spacing)
    population = [init_pop]

    # Perform GA
    best_perf = {'gen': 0, 'max_fit': -100000, 'weights': None}
    for gen in range(num_of_gens):
        print("\nPerforming Generation: {}".format(gen))

        run_sim_once(population[gen], duration, dt)
        next_gen = perform_generation_tournaments(population[gen], pop_size, start_pos, size, spacing)
        population.append(next_gen)

        stats = assess_gen_fitness(population[gen])
        global_stats = track_all_stats(stats, global_stats)

        print(" - Generation Stats: Avg: {} Max: {}".format(stats['avg'], stats['max_fit']))

        if stats['max_fit'] > best_perf['max_fit']:
            best_perf['gen'] = gen
            best_perf['max_fit'] = stats['max_fit']
            best_perf['weights'] = stats['fittest_pheno'].get_weights()
            print(" - New Max Weights: {}\n".format(repr(best_perf['weights'])))
            f = open(file, "a")
            f.write("Gen: {} Fitness: {} Weights: {} \n\n".format(gen, best_perf['max_fit'], repr(best_perf['weights'])))
            f.close()

    running = False

    f = open(file, "a")
    f.write("\nGenerations: {} Fitness: {} \n".format(num_of_gens, max(global_stats['max_fit'])))
    f.close()


def create_init_pop(pop_size, start_pos, max_weight=0.5, size=2, spacing=50):
    """
    Create random initial population.

    Params
    ------
    pop_size: int
    Population size

    start_pos: tuple(int, int)
    starting position of reservoir entity

    max_weight: float
    The max weight size to initially randomize - 0.5 here yields weights -0.5 to 0.5

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
        init_pop.append(Reservoir(start_pos, size, spacing, max_weight=max_weight))
    return init_pop


def run_sim_once(generation, duration, dt):
    """
    Run simulation once.

    Params
    ------
    generation: list(Reservoir)
    The generation to perform the simulation with
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


def perform_generation_tournaments(generation, pop_size, start_pos=(50,50), size=2, spacing=50):
    """
    Perform all tournaments for a single generation.

    Params
    ------
    generation: list(Reservoir)
    current generation

    pop_size: int
    population size

    start_pos: tuple(int, int)
    starting position of reservoir entities

    size: int
    size of entity, 2 here makes a 2x2 square

    spacing: int
    space between particles when at rest

    Returns
    -------
    next_gen: list(Reservoir)
    Next generation
    """

    next_gen = []
    temp_gen = np.array(generation)
    for i in range(int(pop_size/2)):
        temp_gen, win_weights, loss_weights = microbial_tournament(temp_gen)
        next_gen.append(Reservoir(start_pos, size, spacing, win_weights))
        next_gen.append(Reservoir(start_pos, size, spacing, loss_weights))

    return next_gen


def microbial_tournament(generation, local=5, rec=0.5, mut=0.5):
    """
    Perform microbial tournament

    Params
    ------
    generation: list(Reservoir)
    Generation of Reservoir entities to select parents from.

    pop_size: int
    Population size

    local: int
    Neighborhood to look for B's index from A's Index

    rec: float
    Probability to recombine locus

    mut: float
    Probability to mutate locus

    Returns
    -------
    winner_weights: array(floats)
    Weights of the Tournament winner

    loser_weights: array(floats)
    Microbial weights from A, B and Mutations
    """

    Ai = randrange(len(generation))  # Index of A
    A = generation[Ai]
    generation = np.delete(generation, Ai, 0)

    Bi = abs((Ai + 1 + math.ceil(local * random.random())) % len(generation))   # Index of B
    B = generation[Bi]
    generation = np.delete(generation, Bi, 0)

    if fitness_function(A) > fitness_function(B):
        winner_weights = A.get_weights()
        loser_weights = B.get_weights()
    else:
        winner_weights = B.get_weights()
        loser_weights = A.get_weights()

    for i in range(len(loser_weights)):
        if random.random() < rec:
            loser_weights[i] = winner_weights[i]
        if random.random() < mut:
            loser_weights[i] = mutate_locus(loser_weights[i])

    return generation, winner_weights, loser_weights


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
        fit = fitness_function(pheno)

        if fittest_pheno is not None:
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
        for key, value in gen_stats.items():
            global_stats[key].append(value)
    else:
        # Initialise Global Stats
        global_stats = {}
        for key, value in gen_stats.items():
            global_stats[key] = [value]

    return global_stats


if __name__ == '__main__':
    main()
