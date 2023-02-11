import numpy as np

# simulates the world (ground truth)

class WorldSimulation:

    def __init__(self, A_t, starting_mean):
        self.A_t = A_t
        self.true_states = starting_mean

    # randomly samples a value from a distribution
    def sample_distribution(self):
        return np.random.normal(loc=0, scale=1)

    def sample_position(self, variance):
        return np.random.normal(variance)

    # updates position based on acceleration
    def update_states(self):
        acceleration = self.sample_distribution()
        velocity = self.true_states.item(1) + acceleration 
        position = self.true_states.item(0) + velocity + (0.5 * acceleration)
        self.true_states = np.matrix([[position], [velocity]])

    # returns the ground truth state
    def get_ground_truth(self):
        return self.true_states