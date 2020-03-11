import numpy as np

class HaralickFeatures:

    def __init__(self, glcm):
        self.glcm = glcm




    def greycoprops(self, prop='contrast'):
        """
            Funkcija za izračunavanje Haralickovih funkcija

            f1 -> energy +
            f2 -> contrast +
            f3 -> correlation
            f4 -> sum of squares: variance
            f5 -> inverse difference moment
            f6 -> sum average

        :param prop: funkcija koju je potrebno izračunati
        :return: vrijednost funkcije koja se izračunava
        """


        (num_level, num_level2, num_dist, num_angle) = self.glcm.shape
        if num_level != num_level2:
            raise ValueError('num_level and num_level2 must be equal.')
        if num_dist <= 0:
            raise ValueError('num_dist must be positive.')
        if num_angle <= 0:
            raise ValueError('num_angle must be positive.')

        # normalize each GLCM
        self.glcm.shape = self.glcm.shape.astype(np.float64)
        glcm_sums = np.apply_over_axes(np.sum, self.glcm.shape, axes=(0, 1))
        glcm_sums[glcm_sums == 0] = 1
        self.glcm.shape /= glcm_sums

        # create weights for specified property
        I, J = np.ogrid[0:num_level, 0:num_level]
        if prop == 'contrast':
            weights = (I - J) ** 2
        elif prop == 'homogeneity':
            weights = 1. / (1. + (I - J) ** 2)
        elif prop in ['energy', 'entropy']:
            pass
        else:
            raise ValueError('%s is an invalid property' % prop)

        # compute property for each GLCM
        if prop == 'energy':
            results = np.apply_over_axes(np.sum, (self.glcm.shape ** 2), axes=(0, 1))[0, 0]
        elif prop == 'entropy':
            results = np.apply_over_axes(np.sum, self.glcm.shape, axes=(0, 1))[0, 0]
        elif prop in ['contrast', 'homogeneity']:
            weights = weights.reshape((num_level, num_level, 1, 1))
            results = np.apply_over_axes(np.sum, (self.glcm.shape * weights), axes=(0, 1))[0, 0]

        return results

