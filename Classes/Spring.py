import numpy as np
import pygame
import math

from colours import B_R_GRADIENT, GRADIENT_KEYS, FILL

class Spring:
    """Defines a spring within an object, connects two particles."""
    def __init__(self, A, B, rest_length, k, fill=FILL):
        """
        Create Spring object that connects two Particles.
        
        Params
        ------
        A: Particle
        Particle object at one end of the Spring.

        B: Particle
        Particle object at other end of the Spring.

        rest_length: int
        Length of spring when at rest.

        k: float
        Spring Constant, how "springy".

        fill: tuple
        (r, g, b) colour value for pygame.draw
        """
        
        self.A = A 
        self.B = B
        self.rest_length = rest_length
        self.k = k 

        self.force = np.array((0.0, 0.0))
        self.f_change = np.array((0.0, 0.0)) # Some change to force, used in self.add_force()
        self.forces = [] 

        # Calculate Initial Force
        self.update()

        # Set Spring Colour
        key = self.get_colour_key()
        self.fill = B_R_GRADIENT[key]


    def update(self):
        """Update Spring force."""
        
        spring_vector = self.B.get_pos() - self.A.get_pos()
        spring_length = np.linalg.norm(spring_vector)
        x = spring_length - self.rest_length

        v_hat = 0
        if spring_length != 0:
            v_hat = spring_vector / spring_length   # Unit vector 

        self.length = spring_length
        self.force = ((self.k * x) * v_hat) + self.f_change
        self.f_change = 0

        self.forces.append(self.force)

        # Update Spring display colour
        key = self.get_colour_key()
        self.fill = B_R_GRADIENT[key]

        # Apply Force
        self.A.apply_force(self.force)
        # - Invert Force
        self.force = -1 * self.force
        self.B.apply_force(self.force)

    def draw(self, screen):
        """
        Draw Spring to pygame screen.
        
        Params
        ------
        Screen: PyGame Screen
        Display to draw Spring to.
        """
       
        pygame.draw.line(screen, self.fill, self.A.get_pos(), self.B.get_pos(), 2)

    def get_colour_key(self):
        """Get colour gradient key for display."""
        l = GRADIENT_KEYS
        max_force = 0

        for value in self.force:
            # Remove negative sign
            sqr = value ** 2
            sqr_rt = math.sqrt(sqr)

            if sqr_rt > max_force:
                max_force = sqr_rt

        closest = min(l, key=lambda x: abs(x - max_force))

        return closest


    def add_force(self, change):
        """
        Changes spring force by given amount
        
        Params
        ------
        change: np array, shape 2, floats
        (0.0, 0.0) increases or decreases force by this amount
        """

        self.f_change = change

    # --- Post-Sim Data Collection --- #

    def get_max_force(self):
        """Return max force in self.forces."""
        
        max_force = None
        for force in self.forces:
            value = max(force)
            if max_force == None or value > max_force:
                max_force = value
        return max_force

    def get_min_force(self):
        """Return minimum force in self.forces"""

        min_force = None
        for force in self.forces:
            value = min(force)
            if min_force == None or value < min_force:
                min_force = value
        return min_force

    # --- Getters and Setters --- #

    def get_length(self):
        """Return spring length"""

        return self.length

    def get_force(self):
        """Return Spring Force Vector"""

        return self.force