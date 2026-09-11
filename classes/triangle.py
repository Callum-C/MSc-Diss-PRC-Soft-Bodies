from classes.entity import Entity
from classes.particle import Particle
from classes.spring import Spring

import math
import numpy as np
from numpy.linalg import norm


class Triangle(Entity):
    """ Creates a triangle. """

    def __init__(self, pos, spacing, triangle_num=1, A=None, B=None, C=None, AB=None, AC=None, BC=None):
        """
        Create a triangle to be used within a Hydrostatic Square entity.

        Particle A will ultimately be the center of a Hydrostat Square.

        Params
        ------

        pos: tuple
        (x, y) Position of Particle A in triangle

        spacing: int
        Space between particles when at rest.

        height: float
        Height of triangle, half the width / length / height of a square it would create.

        triangle_num: int
        Which number triangle this object is within a bigger hydrostat square.
        Starting at the bottom and incrementing anti-clockwise.

        A: Particle
        Particle A, the central particle in the bigger hydrostart square.

        B: Particle
        Particle B, the particle down and to the left of Particle A.

        C: Particle
        Particle C, the particle down and to the right of Particle A.

        AB: Spring
        Spring that connects Particle A to Particle B

        AC: Spring
        Spring that connects Particle A to Particle C

        BC: Spring
        Spring that connects Particle B to Particle C
        """

        super().__init__(pos)  # self.pos is the position of Particle A

        self.triangle_num = triangle_num
        self.height = spacing/2
        self.particles = self.init_particles(spacing, A, B, C)
        self.springs = self.init_springs(spacing, AB, AC, BC)

        # Area calculation
        self.has_area = True
        self.area = self.calc_area()

    def init_particles(self, spacing, A, B, C):
        """
        Initialise particles.
        Called during __init__.
        """
        particles = []

        # Particle A
        if A is None:
            # A not given, generate new particle
            ppos = np.array((self.pos[0], self.pos[1]))
            particles.append(Particle(ppos))
        else:
            # A given, use A
            particles.append(A)

        self.head = particles[0]
        length = spacing/2

        # Particles B ("Down and to the left of Particle A")
        if B is None:
            ppos = np.array((self.pos[0] - length, self.pos[1] + length))
            particles.append(Particle(ppos))
        else:
            particles.append(B)

        # Particle C ("Down and to the right of Particle A")
        if C is None:
            particles.append(self._init_particle_c(length))
        else:
            particles.append(C)

        return particles

    def _init_particle_c(self, length):
        """
        Initialise particle C
        For procedural generation, this is the particle that has to be generated for Triangle 2 and 3.

        Called During init_particles
        """

        if self.triangle_num == 1:
            ppos = np.array((self.pos[0] + length, self.pos[1] + length))
            return Particle(ppos)
        elif self.triangle_num == 2:
            ppos = np.array((self.pos[0] + length, self.pos[1] - length))
            return Particle(ppos)
        elif self.triangle_num == 3:
            ppos = np.array((self.pos[0] - length, self.pos[1] - length))
            return Particle(ppos)
        else:
            # Triangle 4 only connects up existing particles
            # Currently max triangles is 4
            print("_init_particle_c not required here.")

    def init_springs(self, spacing, AB, AC, BC):
        """
        Initialise springs.
        Called during __init__.
        """
        # Pythagoras Theorem
        spring_length = ((spacing / 2) ** 2) + ((spacing / 2) ** 2)
        spring_length = math.sqrt(spring_length)

        springs = []

        # A to B
        if AB is None:
            springs.append(Spring(self.particles[0], self.particles[1], spring_length, 0.01))
        else:
            springs.append(AB)

        # A to C
        if AC is None:
            springs.append(Spring(self.particles[0], self.particles[2], spring_length, 0.01))
        else:
            springs.append(AC)

        # B to C
        if BC is None:
            springs.append(Spring(self.particles[1], self.particles[2], spacing, 0.01))
        else:
            springs.append(BC)

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
            # Entity has a broken spring, area not applicable.
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

    # --- Getters and Setters --- #

    def get_all_particles(self):
        return self.particles

    def get_particle_a(self):
        return self.particles[0]

    def get_particle_b(self):
        return self.particles[1]

    def get_particle_c(self):
        return self.particles[2]

    def get_all_springs(self):
        return self.springs

    def get_spring_ab(self):
        return self.springs[0]

    def get_spring_ac(self):
        return self.springs[1]

    def get_spring_bc(self):
        return self.springs[2]