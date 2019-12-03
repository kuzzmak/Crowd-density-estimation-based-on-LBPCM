import numpy as np

class HaralickFeatures:
    def __init__(self, glcm):
        self.glcm = glcm
        self.num_level, _, _, _ = self.glcm.shape
        self.I, self.J = np.ogrid[0:self.num_level, 0:self.num_level]

    def contrast(self):
        weights = (self.I - self.J) ** 2
        weights = weights.reshape((self.num_level, self.num_level, 1, 1))
        results = np.apply_over_axes(np.sum, (self.glcm * weights), axes=(0, 1))[0, 0, 0]
        return results

    def energy(self):
        results = np.apply_over_axes(np.sum, (self.glcm ** 2), axes=(0, 1))[0, 0, 0]
        return results

    def homogeneity(self):
        weights = 1. / (1. + (self.I - self.J) ** 2)
        weights = weights.reshape((self.num_level, self.num_level, 1, 1))
        results = np.apply_over_axes(np.sum, (self.glcm * weights), axes=(0, 1))[0, 0, 0]
        return results

    def entropy(self):
        results = np.apply_over_axes(np.sum, self.glcm, axes=(0, 1))[0, 0, 0]
        return results