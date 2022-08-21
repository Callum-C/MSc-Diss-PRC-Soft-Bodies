from classes.entity import Entity
from classes.triangle import Triangle
from colours import SILVER
import numpy as np

class HydrostatSquare(Entity):
    """ Creates a hydrostatic square. """

    def __init__(self, pos, spacing, draw_parts=False, stretch=False, fill=SILVER):
        """
        Create a hydrostatic square with hydrostatic triangle entities.

        5 Particles, 8 Springs, 4 hydrostat triangles.

        Params
        ------

        pos: tuple
        (x, y) Position of Particle A in triangle

        spacing: int
        Space between particles when at rest.

        draw_parts: boolean
        Draw particles, false here will only draw springs.

        stretch: boolean
        Spawn in entity with displaced / extended springs.

        fill: hex code
        Colour to draw particles as
        """

        super().__init__(pos)

        self.draw_parts = draw_parts

        self.particles = []
        self.springs = []
        self.triangles = []

        self._init_triangles(spacing)

        # Area calculation
        self.has_area = True
        self.area = self.calc_area()

        self.volume = self.area * 25
        self.fluid_pressure = self.volume / self.area


    def _init_triangles(self, spacing):
        """
        Initialise the 4 triangles that make this object.
        Called during __init__.
        """

        # Triangle 1
        self.triangles.append(Triangle(self.pos, spacing, 1))

        self.particles = self.triangles[0].get_all_particles()
        self.head = self.particles[0]

        self.springs = self.triangles[0].get_all_springs()

        # Triangle 2
        new_parts, new_springs = self._init_triangle_two(spacing)
        self.particles.append(new_parts)
        self.springs += new_springs

        # Triangle 3
        new_parts, new_springs = self._init_triangle_three(spacing)
        self.particles.append(new_parts)
        self.springs += new_springs

        # Triangle 4
        self.springs.append(self._init_triangle_four(spacing))

    def _init_triangle_two(self, spacing):
        """
        Initialise Triangle 2 of 4.
        Triangle 2 is the right triangle.

        Called during init_triangles.
        """

        # This Triangle's B is triangle 1's C
        A = self.triangles[0].get_particle_a()
        B = self.triangles[0].get_particle_c()
        AB = self.triangles[0].get_spring_ac()

        new_triangle = Triangle(self.pos, spacing, 2, A, B, AB=AB)
        self.triangles.append(new_triangle)

        new_particles = new_triangle.get_particle_c()
        new_springs = [new_triangle.get_spring_ac(), new_triangle.get_spring_bc()]

        return new_particles, new_springs

    def _init_triangle_three(self, spacing):
        """
        Initialise Triangle 3 of 4.
        Triangle 3 is the top triangle.

        Called during init_triangles.
        """

        # This Triangle's B is Triangle 2's C
        A = self.triangles[1].get_particle_a()
        B = self.triangles[1].get_particle_c()
        AB = self.triangles[1].get_spring_ac()

        new_triangle = Triangle(self.pos, spacing, 3, A, B, AB=AB)
        self.triangles.append(new_triangle)

        new_particles = new_triangle.get_particle_c()
        new_springs = [new_triangle.get_spring_ac(), new_triangle.get_spring_bc()]

        return new_particles, new_springs

    def _init_triangle_four(self, spacing):
        """
        Initialise Triangle 4 of 4.
        Triangle 4 is the left triangle.

        Called during init_triangles.
        """

        # This triangle connects up Triangle 1 and 3. Only adds one new spring

        # This Triangle's B is Triangle 3's C
        # This Triangle's C is Triangle 1's B
        A = self.triangles[2].get_particle_a()
        B = self.triangles[2].get_particle_c()
        C = self.triangles[0].get_particle_b()

        AB = self.triangles[2].get_spring_ac()
        AC = self.triangles[0].get_spring_ab()

        new_triangle = Triangle(self.pos, spacing, 4, A, B, C, AB, AC)
        self.triangles.append(new_triangle)

        return new_triangle.get_spring_bc()

    def calc_area(self):
        """
        Calculate square area.
        Return summation of triangle's areas.
        """

        if self.has_a_broken_spring:
            return 0

        area = 0

        for triangle in self.triangles:
            tri_area, _ = triangle.calc_area()
            area += tri_area
        self.area = area
        return area

    def calc_fluid_pressure(self):
        """
        Calculate internal fluid pressure.
        """
        self.fluid_pressure = self.volume / self.area
        return self.fluid_pressure

    def calc_fluid_force(self):
        """
        Calculate force of fluid from fluid pressure.
        Applies fluid force to each external spring.

        Call calc_area() first.
        Called every iteration in update()
        """

        self.fluid_pressure = self.volume / self.area

        # all external springs, don't apply force to internal springs
        ext_springs = [self.springs[2],  # Bottom spring
                       self.springs[4],  # Right spring
                       self.springs[6],  # Top spring
                       self.springs[7]]  # left spring

        for spring in ext_springs:
            self.apply_fluid_force(spring, self.fluid_pressure)

    def apply_fluid_force(self, spring, pressure):
        """
        Apply fluid force for an individual spring.

        Params
        ------
        spring: Spring
        The spring to calculate force on. Should be exterior spring

        pressure: float
        Internal fluid pressure

        direction: vector
        direction to apply force in, e.g.: (-1, 1) - force would apply to the left and up
        """

        v_hat = spring.get_unit_vector()  # Unit vector of spring
        try:
            temp = (pressure / spring.get_length()) * v_hat  # Temp force pressure should exert
            force = np.array((temp[1], temp[0]))  # Invert axis so that force works against spring rather than with

            # Apply force
            spring.A.apply_force(force)
            spring.B.apply_force(force)

        except:
            spring.broken = True
            self.has_a_broken_spring = True

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

        self.calc_area()
        self.calc_fluid_force()

        for particle in self.particles:
            particle.update_pos(dt)


    def draw(self, screen):
        """
        Draw elegen to screen.

        Called every frame / iteration.
        """

        super().draw(screen)

        if self.draw_parts:
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

    def get_area(self):
        return self.area

    def get_fluid_pressure(self):
        return self.fluid_pressure
