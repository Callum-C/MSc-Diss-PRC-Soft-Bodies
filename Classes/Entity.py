import numpy as np


class Entity:
    """An entity is an object within the simulation made up of many Particles and Springs"""

    def __init__(self, pos):
        """Create new entity."""

        self.particles = []
        self.springs = []

        self.pos = (float(pos[0]), float(pos[1]))

    def update(self):
        """
        Update all springs in the entity.
        
        Called every frame / iteration.
        """

        for spring in self.springs:
            spring.update()

    def draw(self, screen):
        """
        Draw entity to screen.

        Called every frame / iteration.
        """

        for spring in self.springs:
            spring.draw(screen)