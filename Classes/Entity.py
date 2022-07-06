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

    """ --- Getters and Setters -- """
    def set_pos(self, pos):
        self.pos = (float(pos[0]), float(pos[1]))

    def get_max_force(self):
        """Searches all entity spring's and returns the max force exerted."""

        forces = []
        for spring in self.springs:
            forces.append(spring.get_max_force())

        return(max(forces))

    def get_min_force(self):
        """Searches all entity spring's and returns the min force exerted."""

        forces = []
        for spring in self.springs:
            forces.append(spring.get_min_force())

        return(min(forces))