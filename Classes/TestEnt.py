from Classes.Entity import Entity
from Classes.Particle import Particle
from Classes.Spring import Spring

from colours import SILVER

import numpy as np


class Test(Entity):
    """Creates a square entity."""

    def __init__(self, pos):
        """
        Create Test Entity.
        
        Params
        ------
        pos: tuple
        (x, y) position of top left particle of Test Entity.

        spacing: int
        Space between particles when at rest.
        
        """
        super(Test, self).__init__(pos)

        particles = []
        springs = []
        
        particles.append(Particle(pos, SILVER))
        particles.append(Particle((pos[0] + 50, pos[1]), SILVER))
        particles.append(Particle((pos[0] + 100, pos[1]), SILVER))

        springs.append(Spring(particles[0], particles[1], 50, 0.01))
        springs.append(Spring(particles[1], particles[2], 50, 0.01))

        self.particles = particles
        self.springs = springs

    def update(self, dt):
        """
        Update all springs and particles in the Test Entity.

        Called every frame / iteration.

        Params
        ------

        dt: float
        delta t, change in time
        """

        super(Test, self).update()

        for particle in self.particles:
            particle.update_pos(dt)

    def draw(self, screen):
        """
        Draw Test Entity to screen.

        Called every frame / iteration.
        """

        super(Test, self).draw(screen)

        for particle in self.particles:
            particle.draw(screen)

        

