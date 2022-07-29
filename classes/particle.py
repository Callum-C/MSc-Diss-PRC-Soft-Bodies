import numpy as np
import pygame

from colours import RED


class Particle:
    """Defines a particle within an object, connected by springs."""

    def __init__(self, pos, fill, mass=1, lock=False, gravity=False):
        """
        Initialize particle object.
        
        Params
        ------
        pos: tuple
        (x, y) position

        fill: tuple
        (r, g, b) colour value for pygame draw

        lock: boolean
        Lock particle in place, unaffected by physics.

        gravity: boolean
        Is particle affected by gravity? 
        Gravity hard coded to 0.1
        """
        gravity_strength = 0.1

        self.pos = np.array((float(pos[0]), float(pos[1])))
        self.start_pos = np.array(self.pos)
        self.positions = [self.start_pos]

        self.fill = fill
        self.mass = mass

        # Is particle locked in place?
        self.locked = lock

        # Is particle affected by gravity?
        if gravity:
            self.gravity = np.array((0.0, gravity_strength * mass))
        else:
            self.gravity = np.array((0.0, 0.0))

        self.acceleration = np.array((0.0, 0.0))
        self.velocity = np.array((0.0, 0.0))

    def apply_force(self, force):
        """Apply force from spring to particle.
        
        Params
        ------

        force: numpy float
        The force being exerted onto Particle.
        """

        ff = np.copy(force)
        acc = ff / self.mass
        self.acceleration += acc

    def update_pos(self, dt):
        """
        Update particle position via force enacted upon it.

        Params
        ------

        dt: float
        delta t, change in t
        """

        if not self.locked:
            self.velocity += (self.acceleration * dt)
            self.velocity = self.velocity * 0.98
            self.pos += self.velocity

            self.acceleration = self.acceleration * 0

        self.positions.append(self.pos)

    def draw(self, screen):
        """
        Draw particle to pygame screen.
        
        Params
        ------
        Screen: PyGame Screen
        Display to draw Particle to.
        """

        size = self.mass * 8

        if self.locked:
            pygame.draw.circle(screen, RED, self.pos, size, 2)
        else:
            pygame.draw.circle(screen, self.fill, self.pos, size, 2)

    """--- Getters and Setters ---"""

    def get_distance(self):
        """
        Returns distance particle has moved from its starting position.

        Moving left and up will return negative values.
        """

        distance = self.pos - self.start_pos

        return distance

    def set_pos(self, pos):
        """Manually update particle's position."""
        self.pos = (float(pos[0]), float(pos[1]))
        self.velocity = 0

    def get_pos(self):
        """Returns particle position."""
        return self.pos

    def get_start_pos(self):
        """Returns particle starting position."""
        return self.start_pos
