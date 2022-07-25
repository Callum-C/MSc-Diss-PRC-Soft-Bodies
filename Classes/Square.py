from classes.entity import Entity
from classes.particle import Particle
from classes.spring import Spring

import numpy as np


class Square(Entity):
    """Creates a square entity."""

    def __init__(self, pos, size, spacing, fill):
        """
        Create Square Entity.
        
        Params
        ------
        pos: tuple
        (x, y) position of top left particle of square.

        size: int
        Size of square, 5 here will make a 5x5 square.

        spacing: int
        Space between particles when at rest.
        
        """
        super(Square, self).__init__(pos)

        particles = []
        springs = []
        for i in range(size):
            row_particles = []

            for j in range(size):
                ppos = np.array((self.pos[0] + (i * (spacing + 100)), self.pos[1] + (j * (spacing + 100))))
                row_particles.append(Particle(ppos, fill))

                if j != 0:
                    springs.append(Spring(row_particles[j - 1], row_particles[j], spacing, 0.01, fill))

                if i != 0:
                    springs.append(Spring(particles[i - 1][j], row_particles[j], spacing, 0.01, fill))

            particles.append(row_particles)

        self.particles = particles
        self.springs = springs

    def update(self, dt):
        """
        Update all springs and particles in the square.

        Called every frame / iteration.
        """

        super(Square, self).update()

        for row in self.particles:
            for particle in row:
                particle.update_pos(dt)

    def draw(self, screen):
        """
        Draw square to screen.

        Called every frame / iteration.
        """

        super(Square, self).draw(screen)

        for row in self.particles:
            for particle in row:
                particle.draw(screen)

        

