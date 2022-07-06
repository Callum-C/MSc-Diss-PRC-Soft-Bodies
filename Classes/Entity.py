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

    def add_force(self, changes):
        """
        Add Force to springs.
        
        Params
        ------
        changes: list
        changes[0] affects self.springs[0]
        """

        for i, change in enumerate(changes):
            self.springs[i].add_force(change)

    # --- Getters and Setters --- #

    def get_spring_lengths(self):
        """Retrieve Length of All Springs."""

        lengths = []
        for spring in self.springs:
            lengths.append(spring.get_length())

        return lengths

    def get_spring_forces(self):

        forces = []
        for spring in self.springs:
            forces.append(spring.get_force())

        return forces

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