from Classes.Entity import Entity
from Classes.Particle import Particle
from Classes.Spring import Spring

import numpy as np


class Circle(Entity):
    """ Creates a Circle Entity. """

    def __init__(self, pos, size, particles, spacing, fill):
        """
        Create Circle Entity.
        TODO: Implement Class
        Params
        ------
        pos: tuple
        (x, y) center position of Circle, Circle formed around this position.

        size: int
        Diameter of Circle.

        particles: int
        How many particles form the circumference of the circle.

        spacing: int
        Space between particles when at rest.
        """

    def update(self):
        """
        Update all springs and particles in the Circle.

        Called every frame / iteration.
        """
        super(Circle, self).update()

    def draw(self, screen):
        """
        Draw square to screen.

        Called every frame / iteration.
        """
        super(Circle, self).draw(screen)
