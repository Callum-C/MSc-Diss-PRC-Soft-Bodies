
import pygad
import numpy as np
import math

from classes.hydrostat_reservoir import HydrostatReservoir
from ga_functions import make_file

duration = 500
dt = 0.05
start_pos = (50, 50)
# size = 2
volume = 0.03
spacing = 50
file = None


def main():
    global file
    title = "Correct-Pressure-Training-D:500-" + str(volume)

    pop_size = 200
    num_of_gens = 1000

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

    file, filename = make_file(method_params, pygad_params, title)

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

    for i in range(pop_size):
        init_pop[i] = np.random.uniform(-max_weight, max_weight, (spring_count, spring_count)).flatten()

    weights = np.array([-0.33138332, -0.2061462 , -0.33940707, -0.09294962,  0.39894064,
       -0.34908249, -0.50136109, -0.30869855, -0.27921833,  0.15210379,
        0.06928178, -0.45825665,  0.07045   , -0.4165459 , -0.35735861,
       -0.43272907,  0.44870974, -0.38770815,  0.10818001,  0.05371161,
        0.18784924, -0.10966364, -0.1695446 ,  0.13121126,  0.27519443,
        0.20774097, -0.20705607,  0.48230523,  0.23178528, -0.45879303,
        0.15801299, -0.11269312, -0.10298238,  0.27071882,  0.17062201,
       -0.48259728,  0.42591287, -0.36024528,  0.48407879, -0.36900792,
       -0.29200959, -0.28408202, -0.4291406 , -0.33470749,  0.26871601,
       -0.07909388, -0.49335478,  0.2706788 , -0.09332857,  0.01054229,
        0.14392124,  0.13513356,  0.04726519, -0.33917514, -0.44892106,
        0.13548187, -0.43346842, -0.1379763 , -0.371887  , -0.29297644,
        0.23667948, -0.33677384, -0.07413276,  0.10565391])

    init_pop[0] = weights

    weights = np.array([-1.97519618e-01, -9.39839401e-02, -4.08059452e-01,  2.76122841e-02,
       -2.94817238e-01, -4.11427543e-01, -1.85089410e-01, -3.28823543e-01,
       -4.25781841e-01,  3.09212168e-01, -3.67667125e-01,  2.40792187e-04,
       -1.25253931e-01, -2.53281592e-01,  1.30152444e-02, -5.63531684e-02,
       -4.51398052e-01, -1.84809550e-01, -3.82995523e-01, -8.55043106e-02,
        3.74512125e-01,  3.73676683e-01, -8.20380542e-02,  1.70132026e-01,
       -3.71618531e-01, -3.74816183e-01, -5.01751661e-01, -2.27627744e-01,
       -6.79172171e-02,  3.71957779e-01, -2.00662085e-01,  4.55462126e-01,
        1.67729274e-01, -4.79626390e-01,  3.35493380e-01, -1.79237459e-01,
       -3.73072387e-02, -8.69427953e-02, -4.79738539e-01, -4.06313571e-01,
        4.57903558e-01, -4.31665978e-01, -3.46737274e-02, -1.81148167e-01,
       -4.20108095e-01, -2.70327128e-01, -4.99112803e-02,  2.35213117e-01,
       -2.97395334e-01, -1.06578100e-01, -4.48777601e-01, -8.16710453e-02,
        2.64061388e-01, -2.23332830e-01, -8.39058384e-02,  7.73284887e-02,
       -1.19313098e-01, -2.27596167e-01, -4.56071444e-01, -1.22475008e-01,
        3.99350947e-01,  4.38677807e-01,  1.46942426e-01, -4.79714585e-01])

    init_pop[1] = weights

    weights = np.array([-0.19751962, -0.11810784, -0.39437976,  0.01924451, -0.29481724,
       -0.42188617, -0.17610861, -0.32882354, -0.41836879,  0.31076775,
       -0.39214451, -0.00417202, -0.13055731, -0.24964642,  0.03609906,
       -0.06448757, -0.44423081, -0.17440527, -0.39037926, -0.07695319,
        0.38543742,  0.34886577, -0.08897331,  0.16183839, -0.37567446,
       -0.37468406, -0.4955103 , -0.24285253, -0.09782435,  0.37390702,
       -0.20184409,  0.44638911, -0.20909938, -0.49177521,  0.33452371,
       -0.18993387, -0.02471582, -0.12661276, -0.11943181, -0.39840228,
        0.47404478, -0.45731435,  0.00877242, -0.19620082, -0.42285934,
       -0.24357615, -0.36875013,  0.23987109, -0.29030067, -0.1149457 ,
       -0.42760117, -0.036378  ,  0.25198915, -0.19018495, -0.06795525,
        0.07764397, -0.09845772, -0.21547351, -0.44903891, -0.12641612,
        0.39140017,  0.4349442 ,  0.12813137, -0.47550478])

    init_pop[2] = weights

    weights = np.array([-0.19876898, -0.21301871, -0.32904147, -0.09196898,  0.4098574 ,
       -0.37988682, -0.51410338, -0.30586786, -0.2671001 ,  0.16778807,
        0.08149534,  0.28744636,  0.05336846,  0.06614167, -0.25834944,
        0.12871914,  0.43711102, -0.41313492, -0.06922462,  0.04268888,
        0.18938349,  0.14513079, -0.17188172,  0.12061769, -0.28834388,
        0.31204111, -0.18777111,  0.47358926,  0.21544358, -0.24753968,
       -0.34962343, -0.22271349, -0.31196831,  0.25401976,  0.15107493,
       -0.48188299,  0.43103725, -0.45449099,  0.49533625, -0.3664892 ,
       -0.20718791, -0.40671988, -0.43600293, -0.36603085, -0.04398212,
       -0.08739334, -0.49163281,  0.2676404 , -0.10155   ,  0.01313236,
        0.16494478, -0.24597674,  0.04315609, -0.39034333, -0.46346574,
        0.13282178, -0.43330468, -0.15649574, -0.33367294,  0.18769011,
        0.22356912, -0.33287587, -0.06834056,  0.10120849])

    init_pop[3] = weights

    return init_pop


def callback_gen(ga_instance):

    generation = ga_instance.generations_completed
    best_solution = ga_instance.best_solution()
    gen_avg_fit = np.average(ga_instance.last_generation_fitness)
    min_fit = min(ga_instance.last_generation_fitness)

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

    run_sim_once(res, duration, dt)

    if res.has_broken_spring():
        return 0

    return res.get_distance()


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