from classes.entity import Entity
from classes.particle import Particle
from classes.spring import Spring

import math
import numpy as np
from numpy.linalg import norm


class HydrostatTriangle(Entity):
    """ Creates a hydrostatic triangle. """

    def __init__(self, pos, spacing):
        """
        Create a hydrostatic isosceles triangle entity.

        Particle A will ultimately be the center of a FC Square.

        Params
        ------

        pos: tuple
        (x, y) Position of Particle A in triangle

        spacing: int
        Space between particles when at rest.

        height: float
        Height of triangle, half the width / length / height of a square it would create.
        """

        super().__init__(pos)

        self.height = spacing/2
        self.particles = self.init_particles(spacing)
        self.springs = self.init_springs(spacing)

        # Area calculation
        # - Works at start, but gets more complicated as shape moves and changes
        self.has_area = True
        self.area = 0.5 * (spacing * self.height)
        self.volume = (self.area * 0.9)

        print("area: {} volume: {}".format(self.area, self.volume))
    
    def init_particles(self, spacing):
        """
        Initialise particles.
        Called during __init__.
        """
        particles = []

        # Particle A
        ppos = np.array((self.pos[0], self.pos[1]))
        particles.append(Particle(ppos))
        self.head = particles[0]

        length = spacing/2

        # Particles B ("Down and to the left of Particle A")
        ppos = np.array((self.pos[0] - length, self.pos[1] + length))
        particles.append(Particle(ppos))

        # Particle C ("Down and to the right of Particle A")
        ppos = np.array((self.pos[0] + length, self.pos[1] + length))
        particles.append(Particle(ppos))

        return particles

    def init_springs(self, spacing):
        """
        Initialise springs.
        Called during __init__.
        """
        spring_length = ((spacing / 2) ** 2) + ((spacing / 2) ** 2)
        spring_length = math.sqrt(spring_length)

        springs = [Spring(self.particles[0], self.particles[1], spring_length, 0.01),  # A to B
                   Spring(self.particles[0], self.particles[2], spring_length, 0.01),  # A to C
                   Spring(self.particles[1], self.particles[2], spacing, 0.01)]        # B to C

        return springs

    def calc_area(self):

        A = self.particles[0].get_pos()
        B = self.particles[1].get_pos()
        C = self.particles[2].get_pos()

        AB = norm(A - B)
        AC = norm(A - C)
        BC = norm(B - C)

        if not self.has_a_broken_spring:
            if AB > AC and AB > BC:
                # AB longest side * Distance to C
                d = norm(np.cross(B - A, A - C)) / norm(B - A)
                self.area = 0.5 * AB * d
                return self.area, "AB"

            elif AC > AB and AC > BC:
                # AC longest side * Distance to B
                d = norm(np.cross(C - A, A - B)) / norm(C - A)
                self.area = 0.5 * AC * d
                return self.area, "AC"
            else:
                # BC longest side or sides equal * Distance to A
                d = norm(np.cross(C - B, B - A)) / norm(C - B)
                self.area = 0.5 * BC * d
                return self.area, "BC"
        else:
            return 0, "NA"

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

        super().update()

        for particle in self.particles:
            particle.update_pos(dt)

    def draw(self, screen):
        """
        Draw elegen to screen.

        Called every frame / iteration.
        """

        super().draw(screen)

        for particle in self.particles:
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