import copy

import numpy as np
import os
import math

from classes.hydrostat_square import HydrostatSquare
from colours import SILVER

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class HydrostatReservoir(HydrostatSquare):

    def __init__(self, pos, spacing, weights=None, max_weight=0.5, draw_parts=False, fill=SILVER):
        """
        Create a Hydrostat Reservoir Object.
        Creates a hydrostat square entity controlled by a Reservoir.

        Params
        ------
        pos: tuple
        (x, y) position of top left particle of square.

        spacing: int
        Space between particles when at rest.

        weights: array(size, size)
        Weight matrix for the Reservoir, if none will be randomly initialised

        max_weight: float
        The max weight size to initially randomize - 0.5 here yields weights -0.5 to 0.5

        draw_parts: boolean
        Draw particles, false here will only draw springs.

        fill: hex code
        Colour to draw particles as
        """

        super().__init__(pos, spacing, draw_parts, fill)
        self.start_pos = self.get_center()  # Position of center of the entity

        self.t = 0  # Tracks time since last lock switch
        self.fitness = 0  # Running track of fitness throughout the sim, applied to final fitness at the end of sim
        self.deviation = 25  # Distance particles can travel in the y-axis before penalised

        num_of_springs = len(self.springs)

        if weights is not None:
            if weights.ndim == 1:
                # If weights is 1D, Reshape to 2D
                weight_size = int(math.sqrt(len(weights)))
                weights = weights.reshape(weight_size, weight_size)
            self.W = weights
        else:
            self.W = np.random.uniform(-max_weight, max_weight, (num_of_springs, num_of_springs))  # Reservoir weights

        # Particle Groups
        self.left = [self.particles[1], self.particles[4]]
        self.right = [self.particles[2], self.particles[3]]

        self.locked = 'right'
        for particle in self.right:
            particle.locked = True

    def step(self, dt):
        """
        Step the control reservoir.
        Called every iteration.

        Params
        ------
        dt: float
        delta t, amount time has changed.
        """

        displacements = self.get_displacement()
        Rout = np.dot(displacements, self.W)
        self.set_new_rest_lengths(Rout)

        if 4.98 <= self.t <= 5.08:
            self.switch_lock()
            # self.check_particle_deviation()
            self.t = 0

        self.t += dt

    def check_particle_deviation(self):
        """Checks how far particles have deviated in the y-axis."""

        fitness = 0
        for particles in self.particles:
            for particle in particles:
                distance = particle.get_distance()
                displacement = abs(distance[1]) - self.deviation  # Abs because we don't care if up or down
                fitness -= max(displacement, 0)  # Penalise for moving up or down
                fitness += 2*distance[0]  # Reward for moving right / forward, penalise for moving left / back

        return fitness

    def switch_lock(self):
        """Switches which group of particles is locked."""

        if self.locked == 'left':
            for particle in self.left:
                particle.locked = False
            for particle in self.right:
                particle.locked = True
            self.locked = 'right'
        else:
            for particle in self.left:
                particle.locked = True
            for particle in self.right:
                particle.locked = False
            self.locked = 'left'

    # --- Getters and Setters --- #

    def get_weights(self):
        """Returns this objects weight matrix."""
        return self.W

    def get_displacement(self):
        """
        Get Displacement of all entity's springs.

        Returns
        -------
        displacement: np array(float)
        Array of every springs displacement
        """

        displacement = np.zeros((len(self.springs)))
        for i, spring in enumerate(self.springs):
            displacement[i] = spring.x

        return displacement

    def set_new_rest_lengths(self, lengths):
        """
        Update entity's springs rest lengths.

        Params
        ------
        lengths: array(floats)
        new rest lengths of entity's springs
        """

        for i, spring in enumerate(self.springs):
            spring.set_rest_length(lengths[i])
