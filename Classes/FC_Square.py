from classes.entity import Entity
from classes.particle import Particle
from classes.spring import Spring
from colours import SILVER

import numpy as np
import math


class FCSquare(Entity):
    """Creates a Fully Connected square entity."""

    def __init__(self, pos, size, spacing, draw_parts=False, fill=SILVER):
        """
        Create a fully connected Square Entity.
        
        Params
        ------
        pos: tuple
        (x, y) position of top left particle of square.

        size: int
        Size of square, 5 here will make a 5x5 square.

        spacing: int
        Space between particles when at rest.

        draw_parts: boolean
        Draw particles, false here will only draw springs.

        fill: hex code
        Colour to draw particles as
        """

        super(FCSquare, self).__init__(pos)
        self.draw_parts = draw_parts

        particles = []
        springs = []
        for i in range(size):
            row_particles = []

            for j in range(size):
                ppos = np.array((self.pos[0] + (i * (spacing * 3)), self.pos[1] + (j * (spacing * 3))))
                row_particles.append(Particle(ppos, fill))

                # Vertical Springs
                if j != 0:
                    springs.append(Spring(row_particles[j - 1], row_particles[j], spacing, 0.05, fill))

                # Horizontal Springs
                if i != 0:
                    springs.append(Spring(particles[i - 1][j], row_particles[j], spacing, 0.05, fill))

                # bottom left particle to top right particle
                if i > 0 and j < size-1:
                    spring_length = (spacing ** 2) + (spacing ** 2)
                    spring_length = math.sqrt(spring_length)
                    springs.append(Spring(particles[i - 1][j + 1], row_particles[j], spring_length, 0.05, fill))

                # bottom right to top left particle
                if i > 0 and j > 0:
                    spring_length = (spacing ** 2) + (spacing ** 2)
                    spring_length = math.sqrt(spring_length)

                    springs.append(Spring(particles[i-1][j - 1], row_particles[j], spring_length, 0.05, fill))

            particles.append(row_particles)

        self.particles = particles
        self.springs = springs

        self.head = particles[0][0]
        self.start_pos = self.get_center()  # Position of center of the entity

    def update(self, dt):
        """
        Update all springs and particles in the square.

        Called every frame / iteration.
        """

        super(FCSquare, self).update()

        for row in self.particles:
            for particle in row:
                particle.update_pos(dt)

    def move_to_cursor(self, pos):
        """
        Move head of Elegen to mouse cursor.

        Params
        ------

        pos: tuple
        (x, y) position to move to.
        """

        self.head.set_pos(pos)

    def draw(self, screen):
        """
        Draw square to screen.

        Called every frame / iteration.
        """

        super(FCSquare, self).draw(screen)

        if self.draw_parts:
            for row in self.particles:
                for particle in row:
                    particle.draw(screen)

    # --- Getters and Setters --- #

