import time
import pygad
import numpy as np
import math
import random
from random import randrange

from classes.reservoir import Reservoir
from ga_functions import make_file

duration = 25
dt = 0.01
start_pos = (50, 50)
size = 2
spacing = 50
file = None


def main():
    global file
    pop_size = 200
    num_of_gens = 1000
    num_of_parents = pop_size  # math.floor(pop_size / 2)

    if (num_of_parents % 2) == 1:
        num_of_parents -= 1  # Ensure num of parents is even

    max_weight = 0.5

    # pygad init variables:
    parent_selection_type = "rank"
    keep_parents = 100
    crossover_type = "uniform"

    mutation_type = "random"
    mutation_probability = 0.5
    mutation_min_val = -0.01
    mutation_max_val = 0.01

    method_params = {"method": "PyGAD", "sim_duration": duration, "fitness_func": "pygad_fitness",
                     "pop_size": pop_size, "gen_size": num_of_gens, "weight_search": max_weight}

    pygad_params = {"parent_selection_type": parent_selection_type, "parents mating": num_of_parents,
                    "keep parents": keep_parents, "crossover type": crossover_type, "mutation type": mutation_type,
                    "mutation prob": mutation_probability, "mutation_max_val": mutation_max_val,
                    "mutation_min_val": mutation_min_val}

    init_pop = pygad_init_pop(pop_size, 6, max_weight)

    file, filename = make_file(method_params, pygad_params)

    ga_instance = pygad.GA(num_generations=num_of_gens,
                           num_parents_mating=num_of_parents,
                           fitness_func=pygad_fitness,
                           initial_population=init_pop,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_probability=mutation_probability,
                           random_mutation_min_val=mutation_min_val,
                           random_mutation_max_val=mutation_max_val,
                           callback_generation=callback_gen,
                           parallel_processing=['process', 8])

    ga_instance.run()

    print(ga_instance.best_solution())

    ga_instance.save(filename)


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
    init_pop[0] = np.array([ 0.39803714,  0.00914718,  0.1500078 , -0.38611251,  0.41685062,
        0.00391305,  0.46670877,  0.36150358, -0.43278976,  0.14746209,
       -0.16166249,  0.11581155,  0.26025891, -0.40120317, -0.32832799,
        0.00709017, -0.01506968, -0.16408635,  0.42180661,  0.3738667 ,
        0.36403733,  0.43931295,  0.15180423,  0.14149314, -0.24320341,
       -0.06265801,  0.30394548,  0.28134214, -0.20638621, -0.20013465,
        0.4661868 , -0.4916331 , -0.08052372,  0.50322551, -0.46058362,
        0.01557552])
    for i in range(1, pop_size):
        init_pop[i] = np.random.uniform(-max_weight, max_weight, (spring_count, spring_count)).flatten()
    return init_pop


def callback_gen(ga_instance):

    generation = ga_instance.generations_completed
    best_solution = ga_instance.best_solution()
    gen_avg_fit = np.average(ga_instance.last_generation_fitness)

    print("Generation : ", generation)
    print("Fitness of the best solution :", best_solution[1])
    print("Average fitness: {}\n".format(gen_avg_fit))

    f = open(file, "a")
    f.write("\nGeneration: {} \n - Generation Avg Fit: {} \n - Best Fitness: {}"
            "\n - Best Solution: {} \n".format(generation, gen_avg_fit, best_solution[1], repr(best_solution[0])))
    f.close()


def pygad_fitness(solution, solution_idx):
    """Fitness function for GA in Pygad."""

    weights = solution.reshape(6, 6)  # Reshape weights to (spring_count, spring_count)
    res = Reservoir(start_pos, size, spacing, weights)

    run_sim_once(res, duration, dt)

    distance = res.get_distance()
    broken = res.get_broken_springs()

    if broken:
        return 0

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