from Classes.Entity import Entity
from Classes.Particle import Particle
from Classes.Spring import Spring

from colours import SILVER

import numpy as np
from random import randrange


class Genotype(Entity):
    """A genotype entity for the Genetic Algorithm"""

    def __init__(self, pos, spacing, a_lock=None, b_lock=None):
        """
        Create a Genotype for simple locomotion.
        Two particles and Singular Spring

        Params
        ------

        pos: tuple
        (x, y) head position of the Genotype

        spacing: int
        Space between particles when at rest.
        """

        super(Genotype, self).__init__(pos)

        self.start_pos = self.pos
        self.spacing = spacing

        if a_lock:
            self.a_lock = a_lock
        else:
            self.a_lock = randrange(0, 51)

        if b_lock:
            self.b_lock = b_lock
        else:
            self.b_lock = randrange(0, 51)

        particles = []
        springs = []
        particles.append(Particle(pos, SILVER))
        particles.append(Particle((pos[0]+(spacing*2), pos[1]), SILVER))
        springs.append(Spring(particles[0], particles[1], spacing, 0.01))

        self.particles = particles
        self.springs = springs

    def mutate(self, mutations=1):
        """
        Mutate Genotype

        Params
        ------

        mutations: int
        Number of mutations to make
        """

        val = randrange(0, 2)

        if val == 0:
            self.a_lock = randrange(0, 51)
        else:
            self.b_lock = randrange(0, 51)

    """ --- Getters and Setters --- """

    def get_params(self):
        """
        Return Parameters as Evolved by the GA.

        Returns
        -------

        spacing: int
        Spacing between particles when at rest

        a_lock: int
        At which count to lock Particle A

        b_lock: int
        At which count to lock Particle B
        """

        return self.spacing, self.a_lock, self.b_lock

    def get_distance(self):
        """ Get Distance Genotype has moved. """

        starter = self.particles[0]
        new_pos = starter.get_pos()

        vector = new_pos - self.start_pos
        distance = np.linalg.norm(vector)

        return distance

    """ --- Overriding Entity Methods --- """

    def update(self, count):
        """ Called every iteration. """
        super(Genotype, self).update()

        if count == self.a_lock:
            self.particles[0].locked = True
            self.particles[1].locked = False

        if count == self.b_lock:
            self.particles[0].locked = False
            self.particles[1].locked = True

        for particle in self.particles:
            particle.update_pos()

    def draw(self, screen):

        super(Genotype, self).draw(screen)

        for particle in self.particles:
            particle.draw(screen)

