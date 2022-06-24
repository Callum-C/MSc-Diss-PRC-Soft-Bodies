from turtle import update
from matplotlib.pyplot import fill
from Classes.Entity import Entity
from Classes.Particle import Particle
from Classes.Spring import Spring

from colours import SILVER, FILL

import numpy as np

class C_Elegen(Entity):
    """ Creates a C Elegen Object. """

    def __init__(self, pos, size, spacing):
        """
        Create a C Elegen Entity.

        Params
        ------

        pos: tuple
        (x, y) head position of the C_Elegen

        size: int
        Length of C_Elegen, how many particles / mass points make up the elegen.

        spacing: int
        Space between particles when at rest.
        """

        super(C_Elegen, self).__init__(pos)

        particles = []
        springs = []

        for i in range(size):
            ppos = np.array((self.pos[0] + (i * spacing), self.pos[1] + (i * spacing)))
            particles.append(Particle(ppos, SILVER))

            if i != 0:
                springs.append(Spring(particles[i-1], particles[i], spacing, 0.01, fill))

        self.particles = particles
        self.head = particles[0]
        self.springs = springs
        
    def move_to_cursor(self, pos):
        """
        Move head of Elegen to mouse cursor.
        
        Params
        ------

        pos: tuple
        (x, y) position to move to.
        """

        self.head.set_pos(pos)


    def update(self):
        """
        Update all springs and particles in the elegen.

        Called every frame / iteration.
        """

        super(C_Elegen, self).update()

        for particle in self.particles:
            particle.update_pos()


    def draw(self, screen):
        """
        Draw elegen to screen.

        Called every frame / iteration.
        """

        super(C_Elegen, self).draw(screen)

        for particle in self.particles:
            particle.draw(screen)


    def lock_head(self):
        """Lock head of elegan in place."""

        self.head.locked = True

    def unlock_head(self):
        """Allow head of elegen to move freely."""

        self.head.locked = False