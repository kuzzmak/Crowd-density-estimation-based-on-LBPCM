import numpy as np

class HaralickFeatures:

    def __init__(self, glcm, normalize=True):

        self.setGLCM(glcm, normalize)

    def setGLCM(self, glcm, normalize):

        (self.num_level, num_level2, self.num_dist, self.num_angle) = glcm.shape

        if self.num_level != num_level2:
            raise ValueError('num_level and num_level2 must be equal.')
        if self.num_dist <= 0:
            raise ValueError('num_dist must be positive.')
        if self.num_angle <= 0:
            raise ValueError('num_angle must be positive.')

        self.glcm = glcm

        if normalize:
            # normalize each GLCM
            self.glcm = self.glcm.astype(np.float64)
            glcm_sums = np.apply_over_axes(np.sum, self.glcm, axes=(0, 1))
            glcm_sums[glcm_sums == 0] = 1
            self.glcm /= glcm_sums

        self.p_x = np.apply_over_axes(np.sum, glcm, axes=1)
        self.p_y = np.apply_over_axes(np.sum, glcm, axes=0)

        self.mean_x = np.sum(self.p_x, axis=(0, 1)) / self.num_level
        self.mean_y = np.sum(self.p_y, axis=(0, 1)) / self.num_level

        temp_x = np.apply_over_axes(np.sum, (self.glcm - self.mean_x) ** 2, axes=(0, 1))
        temp_y = np.apply_over_axes(np.sum, (self.glcm - self.mean_y) ** 2, axes=(0, 1))

        self.sigma_x = np.sqrt(1 / (self.num_level - 1) * temp_x)[0, 0]
        self.sigma_y = np.sqrt(1 / (self.num_level - 1) * temp_y)[0, 0]

    def pxory(self, k):
        """
            Funkcija za zbrajanje elemenata na dijagonali matrice, potebna u izračunu
            pojedinih Haralickovih funkcija.

        :param glcm: matrica u kojoj se zbrajaju elementi
        :param k: dijagonala + 1 na kojoj se zbrajaju elementi
        :return: zbroj elemenata na dijagonali
        """

        _sum = np.zeros((self.num_dist, self.num_angle))

        # zbrajanje elemenata na dijagonali prvog trokuta matrice
        if k <= self.num_level + 1:
            for i in range(k - 1):
                for d in range(self.num_dist):
                    for a in range(self.num_angle):
                        _sum[d][a] += self.glcm[k - i - 2][i][d][a]
        else:
            # drugi trokut matrice
            for d in range(self.num_dist):
                for a in range(self.num_angle):
                    for i in range(2 * self.num_level - k + 1):
                        _sum[d][a] += self.glcm[self.num_level - 1 - i][k - self.num_level - 1 + i][d][a]

        return _sum

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

        # težine za pojedine Haralickove funkcije
        I, J = np.ogrid[0:self.num_level, 0:self.num_level]
        if prop == 'contrast':
            weights = (I - J) ** 2
        elif prop == 'homogeneity':
            weights = 1. / (1. + (I - J) ** 2)
        elif prop == 'correlation':
            weights = I * J
        elif prop in ['angular second moment', 'entropy', 'sum average', 'sum variance', 'sum entropy']:
            pass
        else:
            raise ValueError('%s is an invalid property' % prop)

        # Haralickove funkcije
        if prop == 'angular second moment':
            results = np.apply_over_axes(np.sum, (self.glcm ** 2), axes=(0, 1))[0, 0]

        elif prop == 'entropy':
            results = np.apply_over_axes(np.sum, -self.glcm * np.log10(self.glcm + 1e-12), axes=(0, 1))[0, 0]

        elif prop == 'correlation':
            weights = weights.reshape((self.num_level, self.num_level, 1, 1))
            results = np.apply_over_axes(np.sum, self.glcm * weights, axes=(0, 1))[0, 0]

            results -= self.mean_x * self.mean_y

            results /= np.divide(results, self.sigma_x * self.sigma_y)

        elif prop == 'sum average':
            _sum = np.zeros((self.num_dist, self.num_angle))
            for i in range(2, 2 * self.num_level + 1, 1):
                _sum += i * self.pxory(i)
            results = _sum

        # elif prop == 'sum variance':
        #     f8 = greycoprops(P, prop='sum entropy')
        #     summ = 0
        #     for i in range(2, 2 * num_level):
        #         summ += math.pow(i - f8, 2) * pxory(i, P)
        #     results = summ
        #
        # elif prop == 'sum entropy':
        #     summ = 0
        #     for i in range(2, 2 * num_level):
        #         temp = pxory(i, P)
        #         summ += temp * math.log10(temp + 1e-12)
        #     results = -summ

        elif prop in ['contrast', 'homogeneity']:
            weights = weights.reshape((self.num_level, self.num_level, 1, 1))
            results = np.apply_over_axes(np.sum, (self.glcm * weights), axes=(0, 1))[0, 0]

        return results
