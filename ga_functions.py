import copy
import numpy as np
import random

# --- Genetic Algorithm Functions --- #
def fitness(reservoir):
    """
    Assess Controller's Fitness.

    Params
    ------
    reservoir: reservoir
    Reservoir entity to assess fitness of

    TODO - Reward maintaining shape
    """
    distance = reservoir.get_distance()

    return distance[0] - (2.5 * abs(distance[1]))


def mutate(weights, mutations=1, lr=0.01):
    """
    Mutate controller.
    - Take passed weights, mutate them, set them as own weights.

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
