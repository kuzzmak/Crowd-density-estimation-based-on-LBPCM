import numpy as np

class HaralickFeatures:

    def __init__(self, glcm, normalize=True):

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
        # rječnik sa prethodno izračunatim vrijednostima funkcije
        self.pxminyDict = {}

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

    def pxminy(self, k):
        """
        Funkcija koja pripomaže izračunu pojedinih Haralickovih funkcija.
        Zbrajaju se brojevi na dijagonalama ovisno o parametru k.
        Za k=0 je to je sporedna dijagonala, za k!=0 to su koncentrične dijagonale oko sporedne
        uključujuću prethodnu iteraciju naredbe.

        :param k:
        :return:
        """

        assert 0 <= k < self.num_level, "k must be < " + str(self.num_level) + " and >= 0"

        if len(self.pxminyDict) == 0:
            self.pxminyDict[0] = np.sum(self.glcm.diagonal(), axis=2)

        _sum = np.array(self.pxminyDict[len(self.pxminyDict) - 1])

        for _k in range(len(self.pxminyDict), k + 1, 1):
            for i in range(self.num_level):
                for d in range(self.num_dist):
                    for a in range(self.num_angle):
                        j1 = i + _k
                        j2 = i - _k

                        if j1 < self.num_level:
                            _sum[d][a] += self.glcm[i, j1, d, a]
                        if j2 >= 0:
                            _sum[d][a] += self.glcm[i, j2, d, a]

            self.pxminyDict[_k] = _sum
        return _sum

    def Q(self, i, j):

        assert 0 <= i < self.num_level and 0 <= i < self.num_level, "i and j must be in range of glcm levels"

        row_i = self.glcm[i, :, :, :]
        row_j = self.glcm[j, :, :, :]
        i_y = row_i * row_j

        p_x = np.apply_over_axes(np.sum, self.glcm, axes=1)
        p_y = np.apply_over_axes(np.sum, self.glcm, axes=0)

        p_x_y = (p_x[i] * p_y)
        p_x_y[p_x_y == 0] = 1

        return np.apply_over_axes(np.sum, i_y / p_x_y, axes=(0, 1))

    def greycoprops(self, prop='contrast'):
        """
        Funkcija za izračunavanje Haralickovih funkcija

        f1 -> angular second moment +
        f2 -> contrast +
        f3 -> correlation +
        f4 -> sum of squares: variance +
        f5 -> inverse difference moment +
        f6 -> sum average +
        f7 -> sum variance +
        f8 -> sum entropy +
        f9 -> entropy +
        f10 -> difference variance +
        f11 -> difference entropy +
        f12 -> imoc1 +
        f13 -> imoc2 +
        f14 -> maximal correlation coefficient

        :param prop: funkcija koju je potrebno izračunati
        :return: vrijednost funkcije koja se izračunava
        """

        # težine za pojedine Haralickove funkcije
        I, J = np.ogrid[0:self.num_level, 0:self.num_level]
        if prop == 'contrast':
            weights = (I - J) ** 2
        elif prop == 'inverse difference moment':
            weights = 1. / (1. + (I - J) ** 2)
        elif prop == 'correlation':
            weights = I * J
        elif prop == 'sum of squares: variance':
            weights = I
        elif prop in ['angular second moment',
                      'entropy',
                      'sum average',
                      'sum variance',
                      'sum entropy',
                      'difference variance',
                      'difference entropy',
                      'imoc1',
                      'imoc2',
                      'maximal correlation coefficient']:
            pass
        else:
            raise ValueError('%s is an invalid property' % prop)

        # Haralickove funkcije
        if prop == 'angular second moment':
            results = np.apply_over_axes(np.sum, (self.glcm ** 2), axes=(0, 1))[0, 0]

        elif prop == 'entropy':
            results = np.apply_over_axes(np.sum, -self.glcm * np.log10(self.glcm + 1e-12), axes=(0, 1))[0, 0]

        elif prop == 'correlation':

            p_x = np.apply_over_axes(np.sum, self.glcm, axes=1)
            p_y = np.apply_over_axes(np.sum, self.glcm, axes=0)

            mean_x = np.sum(p_x, axis=(0, 1)) / self.num_level
            mean_y = np.sum(p_y, axis=(0, 1)) / self.num_level

            temp_x = np.apply_over_axes(np.sum, (self.glcm - mean_x) ** 2, axes=(0, 1))
            temp_y = np.apply_over_axes(np.sum, (self.glcm - mean_y) ** 2, axes=(0, 1))

            sigma_x = np.sqrt(1 / (self.num_level - 1) * temp_x)[0, 0]
            sigma_y = np.sqrt(1 / (self.num_level - 1) * temp_y)[0, 0]

            weights = weights.reshape((self.num_level, self.num_level, 1, 1))
            results = np.apply_over_axes(np.sum, self.glcm * weights, axes=(0, 1))[0, 0]
            results -= mean_x * mean_y
            results /= np.divide(results, sigma_x * sigma_y)

        elif prop == 'sum average':
            _sum = np.zeros((self.num_dist, self.num_angle))
            for i in range(2, 2 * self.num_level + 1, 1):
                _sum += i * self.pxory(i)
            results = _sum

        elif prop == 'sum variance':
            f8 = self.greycoprops(prop='sum entropy')
            _sum = np.zeros((self.num_dist, self.num_angle))

            for i in range(2, 2 * self.num_level + 1, 1):
                _sum += (i - f8) ** 2 * self.pxory(i)
            results = _sum

        elif prop == 'sum entropy':
            _sum = np.zeros((self.num_dist, self.num_angle))
            for i in range(2, 2 * self.num_level + 1, 1):
                temp = self.pxory(i)
                _sum += temp * np.log(temp + 1e-12)
            results = -_sum

        elif prop == 'difference variance':

            variance = np.zeros((self.num_dist, self.num_angle))

            for i in range(self.num_level):
                variance += np.power(self.pxminy(i), 2) / self.num_level

            results = variance

        elif prop == 'difference entropy':
            _sum = np.zeros((self.num_dist, self.num_angle))
            for i in range(self.num_level):
                temp = self.pxminy(i)
                _sum += temp * np.log(temp + 1e-12)
            results = -_sum

        elif prop == 'imoc1' or prop == 'imoc2': # information measures of correlation
            p_x = np.apply_over_axes(np.sum, self.glcm, axes=1)
            p_y = np.apply_over_axes(np.sum, self.glcm, axes=0)
            HXY = self.greycoprops(prop='entropy')
            p_x_y = p_x * p_y
            HXY1 = -np.sum(self.glcm * np.log(p_x_y + 1e-12), axis=(0, 1))
            HXY2 = -np.sum(p_x_y * np.log(p_x_y + 1e-12), axis=(0, 1))
            HX = -np.sum(p_x * np.log(p_x + 1e-12), axis=(0, 1))
            HY = -np.sum(p_y * np.log(p_y + 1e-12), axis=(0, 1))

            if prop == 'imoc1':
                results = (HXY - HXY1) / np.maximum(HX, HY)
            else:
                results = np.sqrt(1 - np.exp(-2 * (HXY2 - HXY)))

        elif prop == 'sum of squares: variance':

            mean = np.apply_over_axes(np.mean, self.glcm, axes=(0, 1))
            weights = weights.reshape((self.num_level, 1, 1, 1))
            results = np.apply_over_axes(np.sum, np.power(weights - mean, 2) * self.glcm, axes=(0, 1))

        elif prop in ['contrast', 'inverse difference moment']:
            weights = weights.reshape((self.num_level, self.num_level, 1, 1))
            results = np.apply_over_axes(np.sum, (self.glcm * weights), axes=(0, 1))[0, 0]

        return results
