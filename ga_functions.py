import copy
import numpy as np
import random
import os

# --- Genetic Algorithm Functions --- #


def fitness_day2(reservoir):
    """
    Assess Controller's Fitness.

    As used for Day 1 and Day 2 Sims
    - 27th and 28th of July

    Params
    ------
    reservoir: reservoir
    Reservoir entity to assess fitness of

    TODO - Reward maintaining shape
         - Improve Y penalty to particle level
         - Check horizontal springs are parallel
         - Back group can't "overtake" front group
         - Bigger Penalty for breaking springs
    """
    distance = reservoir.get_distance()

    broken = reservoir.get_broken_springs()  # Added for Day2  Sims

    return distance[0] - (2.5 * abs(distance[1])) - (1000 * broken)


def fitness_day3(reservoir):
    """
    Assess Controller's Fitness. - Fitness_day3

    For use on Day 3 Simulations

    Changes from Day 1/2 Fitness:
        - Bigger penalty for a broken spring
        - Distance calculated particle - instead of average entity location

    Params
    ------
    reservoir: reservoir
    Reservoir entity to assess fitness of

    TODO - Reward maintaining shape
            - Check horizontal springs are parallel
            - Back group can't "overtake" front group
    """

    distance = reservoir.get_distance()
    broken = reservoir.get_broken_springs()

    dist_fit = reservoir.check_particle_deviation()

    return dist_fit - (5000 * broken)


def fitness_function(reservoir):
    """
    Assess Controller's Fitness. - Fitness_day4

    For use on Day 34 Simulations

    Changes from Day 3 Fitness:

    Params
    ------
    reservoir: reservoir
    Reservoir entity to assess fitness of
    """

    distance = reservoir.get_distance()
    broken = reservoir.get_broken_springs()

    return distance - (5000 * broken)


def make_file(method_params, pygad_params=None):
    """
    Make a unique file for storing GA Training Data.

    Params
    ------
    method_params: dict
    Dictionary of GA method parameters

    pygad_params: dict
    Dictionary of parameters for pygad instance

    Returns
    -------
    file: string
    file directory to store data into

    filename: string
    The name of the file without extension
    """

    directory = "training/"
    name = "GA-Pygad-Training"
    filename = directory + name
    file = filename + ".txt"

    if os.path.exists(file):
        flag = True
        i = 0
        while flag:
            if os.path.exists(file):
                filename = directory + filename + "-" + str(i)
                file = filename + ".txt"
            else:
                f = open(file, 'a')
                flag = False
            i += 1
    else:
        f = open(file, 'a')

    print("Using file: {}".format(file))
    f.write("\n-------------------------------------------------------------------------------------------------------")
    f.write("\n                                --- Method Parameters ---                                            \n")
    f.write("-------------------------------------------------------------------------------------------------------\n")
    f.write("\n")

    for key, value in method_params.items():
        f.write("{}: {}, ".format(str(key), str(value)))

    f.write("\n")

    if pygad_params is not None:
        f.write(
            "\n-------------------------------------------------------------------------------------------------------")
        f.write(
            "\n                                --- Pygad  Parameters ---                                            \n")
        f.write(
            "-------------------------------------------------------------------------------------------------------\n")
        f.write("\n")

        for key, value in pygad_params.items():
            f.write("{}: {}, ".format(str(key), str(value)))
            if str(key) == "crossover type":
                f.write("\n")

    f.write("\n\n"
            "======================================================================================================="
            "\n\n")

    f.close()

    return file, filename


def mutate(weights, mutations=1, lr=0.01):
    """
    Mutate controller.
    - Take passed weights and mutate them

    Params
    ------
    weights: array(floats)
    numpy array of floats for weights.

    mutations: int
    Number of mutations to make.

    lr: float
    learning rate, amount to adjust weights by.

    Returns
    -------
    mutated: array(floats)
    mutated weights to be used by a Reservoir entity
    """

    mutated = copy.deepcopy(weights)
    r = random.randint(0, 1)

    for i in range(mutations):
        index = np.random.randint(len(mutated))

        # Random positive or minus
        if r:
            mutated[index] = mutated[index] + lr
        else:
            mutated[index] = mutated[index] - lr

    return mutated


def mutate_locus(weight, lr=0.01):
    """
    Mutate an individual weight, or locus.

    Params
    ------
    weight: float
    weight to mutate

    lr: float
    learning rate, amount to change the weight by

    Returns
    -------
    weight: float
    the new mutated weight
    """

    if random.random() < 0.5:
        weight += lr
    else:
        weight -= lr

    return weight