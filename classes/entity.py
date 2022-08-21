import numpy as np


class Entity:
    """An entity is an object within the simulation made up of many Particles and Springs"""

    def __init__(self, pos):
        """Create new entity."""

        self.head = None
        self.has_area = False
        self.has_a_broken_spring = False  # If entity has a broken spring. care: function with similar name.
        self.particles = []
        self.springs = []

        self.pos = (float(pos[0]), float(pos[1]))  # Position of first / top left particle

    def update(self):
        """
        Update all springs in the entity.
        
        Called every frame / iteration.
        """

        for spring in self.springs:
            spring.update(self)

    def draw(self, screen):
        """
        Draw entity to screen.

        Called every frame / iteration.
        """

        for spring in self.springs:
            spring.draw(screen)

    def step(self, dt):
        """
        Step function for entities with controllers.

        Not implemented here in parent, here to prevent errors.
        """
        NotImplemented

    def calc_area(self):
        """
        Calculate area of entity.

        Not implemented in parent, but here to prevent errors.
        - Some subclasses use this, most don't.
        """
        NotImplemented

    def add_force(self, changes):
        """
        Manually add force to springs.
        
        Params
        ------
        changes: list
        changes[0] affects self.springs[0]
        """

        for i, change in enumerate(changes):
            self.springs[i].add_force(change)


    # --- Getters and Setters --- #

    def has_head(self):
        """If entity has a particle assigned as its 'head'."""

        if self.head:
            return True
        else:
            return False

    def has_broken_spring(self):
        """Return if entity has at least 1 broken spring."""

        for spring in self.springs:
            if spring.broken:
                return True

        return False

    def get_broken_springs(self):
        """Returns how many springs within the entity are broken."""

        num_of_springs = 0
        for spring in self.springs:
            if spring.broken:
                num_of_springs += 1

        return num_of_springs

    def get_center(self):
        """
        Get center of entity.
        """

        positions = np.zeros((len(self.particles), 2))

        for i, particle in enumerate(self.particles):
            positions[i] = particle.get_pos()

        return positions.mean(0)

    def get_distance(self):
        """
        Uses starting position to calculate distance travelled.
        """

        dist = self.get_center() - self.start_pos
        dist = np.linalg.norm(dist)
        return dist

    def get_distance_coords(self):
        """
        Uses starting position to calculate distance travelled.

        distance[0] - Movement left to right
        distance[1] - Movement up to down
        """

        dist = self.get_center() - self.start_pos
        return dist

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
        """Searches all entity springs and returns the max force exerted."""

        forces = []
        for spring in self.springs:
            forces.append(spring.get_max_force())

        return max(forces)

    def get_min_force(self):
        """Searches all entity springs and returns the min force exerted."""

        forces = []
        for spring in self.springs:
            forces.append(spring.get_min_force())

        return min(forces)