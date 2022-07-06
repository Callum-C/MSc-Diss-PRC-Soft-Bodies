from Classes.Genotype import Genotype

from copy import deepcopy
from random import randrange
import math

class GeneticAlgorithm:
    """ Simple GA that searches for timings of locking particles in place to move entity. """

    def __init__(self, start_pos, pop_count, gen_count, time):
        """
        Simple GA that searches for timings of locking particles in place to move entity.

        Params
        ------

        start_pos: tuple
        (x, y) start position of each genotype

        pop_count: int
        Population Size - Number of Genotypes in each generation

        gen_count: int
        Number of evolutions GA searches for

        time: int
        How long a geno has to move before assessed
        """

        spacing = 100

        self.start_pos = start_pos
        self.pop_count = pop_count
        self.gen_count = gen_count
        self.time = time

        self.population = []  # Nested list - population[0] is Generation 0 Population
        init_pop = []

        for i in range(pop_count):
            init_pop.append(Genotype(start_pos, spacing))

        self.population.append(init_pop)

    def run_ga(self):
        """ Run the Genetic Algorithm. """

        for gen in range(self.gen_count):
            count = 0
            runtime = 0

            # Perform Generation
            while runtime < self.time:

                self.update(count)

                runtime += 1
                if count < 50:
                    count += 1
                else:
                    count = 0

            # Asses Generation
            avg, max_fit, index = self.gen_fitness(gen)
            print("Generation: {} Max Fitness: {} Index: {} Avg Fitness: {}".format(gen, max_fit, index, avg))

            # Perform Selection
            next_pop = []
            current_pop = self.population[gen]

            for i in range(math.ceil(self.pop_count / 2)):
                A = randrange(0, len(current_pop))
                A = current_pop[A]
                current_pop.remove(A)

                B = randrange(0, len(current_pop))
                B = current_pop[B]
                current_pop.remove(B)

                AFit = self.fitness(A)
                BFit = self.fitness(B)

                # Add Fittest, Mutate Weakest
                if AFit > BFit:
                    spacing, a_lock, b_lock = A.get_params()
                    A = Genotype(self.start_pos, spacing)
                    next_pop.append(A)
                    B = Genotype(self.start_pos, spacing)
                    next_pop.append(B)
                else:
                    spacing, a_lock, b_lock = B.get_params()
                    B = Genotype(self.start_pos, spacing)
                    next_pop.append(B)
                    A = Genotype(self.start_pos, spacing)
                    next_pop.append(A)

            self.population.append(next_pop)

        return self.population[gen][index].get_params()

    def update(self, count, generation=0):
        """
        Called every Step / Iteration, Updates all Genos.

        Params
        ------
        count: int
        Iteration count, resets every 50

        generation: int
        What generation GA is on
        """

        for geno in self.population[generation]:
            geno.update(count)

    """ --- Fitness --- """

    def gen_fitness(self, generation):
        """
        Assess fitness of every genotype in a generation.

        Params
        ------

        generation: int
        Which generation to test fitness of

        Returns
        -------

        avg: float
        Average fitness of generation

        max_fit: float
        Best fitness achieved this generation

        index: int
        Index of Geno w/ Best Fitness
        """
        max_fit = 0
        running_total = 0
        index = 0
        for i, geno in enumerate(self.population[generation]):
            fit = self.fitness(geno)
            running_total += fit

            if fit > max_fit or i == 0:
                max_fit = fit
                index = i

        avg = running_total / self.pop_count

        return avg, max_fit, index

    def fitness(self, genotype):
        """
        Assess fitness of single Genotype.

        Params
        ------

        genotype: genotype
        The genotype to assess fitness of.
        """

        return genotype.get_distance()
