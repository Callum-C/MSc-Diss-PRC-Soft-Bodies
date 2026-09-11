import pygad
import numpy as np
import math

from classes.hydrostat_reservoir import HydrostatReservoir
from ga_functions import make_file

duration = 100
dt = 0.05
start_pos = (50, 50)
# size = 2
spacing = 50
file = None
volume


def main():
    global file, volume
    values = [40, 50, 70, 80, 90, 100]  # Parameter sweep values
    volume = 40
    title = "Volume-Parameter-Sweep"
    for value in values:

        volume = value  # Sub in value for param sweep
        pop_size = 200
        num_of_gens = 5000

        num_of_parents = math.floor(pop_size / 2)

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

        method_params = {"method": "PyGAD", "entity": "hydrostat_reservoir", "volume": volume, "sim_duration": duration,
                         "dt": dt, "fitness_func": "pygad_fitness", "pop_size": pop_size, "gen_size": num_of_gens,
                         "weight_search": max_weight}

        pygad_params = {"parent_selection_type": parent_selection_type, "parents mating": num_of_parents,
                        "keep parents": keep_parents, "crossover type": crossover_type, "mutation type": mutation_type,
                        "mutation prob": mutation_probability, "mutation_max_val": mutation_max_val,
                        "mutation_min_val": mutation_min_val}

        init_pop = pygad_init_pop(pop_size, 8, max_weight)

        file, filename = make_file(method_params, pygad_params, title=title, value=value)

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
                               on_fitness=pygad_on_fitness,
                               parallel_processing=['process', 8])

        ga_instance.run()

        print(ga_instance.best_solution())

        ga_instance.save(filename)


def pygad_init_pop(pop_size, spring_count=8, max_weight=0.5):
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

    for i in range(1, pop_size):
        init_pop[i] = np.random.uniform(-max_weight, max_weight, (spring_count, spring_count)).flatten()
    return init_pop


def callback_gen(ga_instance):

    generation = ga_instance.generations_completed
    best_solution = ga_instance.best_solution()
    gen_avg_fit = np.average(ga_instance.last_generation_fitness)

    print("Generation : ", generation)
    print("Fitness of the best solution :", best_solution[1])
    print("Fitness of worst solution : ", min_fit)
    print("Average fitness: {}\n".format(gen_avg_fit))

    f = open(file, "a")
    f.write("\nGeneration: {} \n - Generation Avg Fit: {} \n - Best Fitness: {} \n - Worst Fitness: {}"
            "\n - Best Solution: {} \n".format(generation, gen_avg_fit, best_solution[1], min_fit,
                                               repr(best_solution[0])))
    f.close()


def pygad_fitness(solution, solution_idx):
    """Fitness function for GA in Pygad."""
    weights = solution.reshape(8, 8)  # Reshape weights to (spring_count, spring_count)
    res = HydrostatReservoir(start_pos, spacing, volume, weights)
    print(volume)
    run_sim_once(res, duration, dt)

    if res.has_a_broken_spring:
        return 0

    return res.get_distance()


def pygad_on_fitness(ga, fitness_vals):
    """
    Pygad_on_fitness() function.

    Called when all fitness vals for a population are calculated.
    """

    global min_fit

    min_fit = min(fitness_vals)


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