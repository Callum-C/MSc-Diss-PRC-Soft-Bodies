from classes.entity import Entity
from classes.particle import Particle
from classes.spring import Spring

from colours import SILVER, FILL

import numpy as np


class CElegen(Entity):
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

        super(CElegen, self).__init__(pos)
                
        self.particles = self.init_particles(size, spacing)
        self.springs = self.init_springs(spacing)
    
    def init_particles(self, size, spacing):
        """
        Initialize Elegen Particles.
        Called During Entity __init__.
        """
        particles = []
        ppos = np.array((self.pos[0], self.pos[1]))
        particles.append([Particle(ppos, SILVER, 1)])
        self.head = particles[0][0]

        for i in range(1, size):
            group_particles = []
            # Create first particle in pair for stage of body
            ppos = np.array((self.pos[0] + (i * spacing), self.pos[1] - 20))
            group_particles.append(Particle(ppos, SILVER, 1))

            # Create second particle in pair for stage of body
            ppos = np.array((self.pos[0] + (i * spacing), self.pos[1] + 20))
            group_particles.append(Particle(ppos, SILVER))

            particles.append(group_particles)
        
        return particles

    def init_springs(self, spacing):
        """
        Initialize Elegen Springs
        Called During __init__.
        """
        springs = []

        for i, group in enumerate(self.particles):

            if i == 1:
                # Create "Neck" Springs, connecting head to "shoulders" and shoulders to each other #
                springs.append(Spring(self.head, group[0], spacing, 0.01, FILL))
                springs.append(Spring(self.head, group[1], spacing, 0.01, FILL))
                springs.append(Spring(group[0], group[1], 40, 0.0, FILL))

            elif i > 1:
                # Create body springs
                springs.append(Spring(self.particles[i-1][0], group[0], spacing, 0.01, FILL))
                springs.append(Spring(self.particles[i-1][1], group[1], spacing, 0.01, FILL))
                springs.append(Spring(group[0], group[1], 40, 0.0, FILL))

        return springs

    def move_to_cursor(self, pos):
        """
        Move head of Elegen to mouse cursor.
        
        Params
        ------

        pos: tuple
        (x, y) position to move to.
        """

        self.head.set_pos(pos)


    def update(self, dt):
        """
        Update all springs and particles in the elegen.

        Called every frame / iteration.
        """

        super(CElegen, self).update()

        for group in self.particles:
            for particle in group:
                particle.update_pos(dt)


    def draw(self, screen):
        """
        Draw elegen to screen.

        Called every frame / iteration.
        """

        super(CElegen, self).draw(screen)

        for group in self.particles:
            for particle in group:
                particle.draw(screen)

    # --- Lock Head In Place --- #

    def lock_head(self):
        """Lock head of elegan in place."""

        self.head.locked = True

    def unlock_head(self):
        """Allow head of elegen to move freely."""

        self.head.locked = False

    def toggle_head_lock(self):
        """If head is currently unlocked, lock it in place and vice versa."""

        if self.head.locked:
            self.head.locked = False
        else:
            self.head.locked = True