import numpy as np
import pygame

class Spring:
    """Defines a spring within an object, connects two particles."""
    def __init__(self, A, B, rest_length, k, fill):
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
        Spring damping value or Spring Constant.

        fill: tuple
        (r, g, b) colour value for pygame.draw
        """
        
        self.A = A 
        self.B = B
        self.rest_length = rest_length
        self.k = k 
        self.fill = fill

        self.force = np.array((0.0, 0.0))

    def update(self):
        """Update Spring force."""
        
        spring_vector = self.B.get_pos() - self.A.get_pos()
        spring_length = np.linalg.norm(spring_vector)
        x = spring_length - self.rest_length

        v_hat = 0
        if spring_length != 0:
            v_hat = spring_vector / spring_length   # Unit vector 

        self.force = ((self.k * x) * v_hat)

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