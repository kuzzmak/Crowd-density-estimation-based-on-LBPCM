import numpy as np
import cv2 as cv
from skimage.feature import greycomatrix
import math
import util


image = np.array([[0, 0, 1, 1], [0, 0, 1, 1], [0, 2, 2, 2], [2, 2, 3, 3]])
# image = cv.imread("/home/tonkec/Desktop/220px-Lenna_(test_image).png", cv.IMREAD_GRAYSCALE)
glcm = greycomatrix(image.astype(int), [1, 2], [0, np.pi], levels=4)
(num_level, num_level2, num_dist, num_angle) = glcm.shape

def pxminy(k):
    """
        Funkcija koja pripomaže izračunu pojedinih Haralickovih funkcija.
        Zbrajaju se brojevi na dijagonalama ovisno o parametru k.
        Za k=0 je to je sporedna dijagonala, za k!=0 to su koncentrične dijagonale oko sporedne
        uključujuću prethodnu iteraciju naredbe.
    :param k:
    :return:
    """

    assert 0 <= k < num_level, "k must be < " + str(num_level) + " and >= 0"

    _sum = np.sum(glcm.diagonal(), axis=2)

    if k == 0:
        return _sum

    for d in range(num_dist):
        for a in range(num_angle):
            for _k in range(1, k + 1, 1):

                for i in range(num_level):
                    j1 = i + _k
                    j2 = i - _k

                    if j1 < num_level:
                        _sum[d][a] += glcm[i, j1, d, a]
                    if j2 >= 0:
                        _sum[d][a] += glcm[i, j2, d, a]
    return _sum

import time
start = time.time()
print(pxminy(3))
end = time.time()
print(end-start)

# import time
# from Haralick import HaralickFeatures as hf
#
# # funkcijski model
#
# start = time.time()
# prop1 = util.greycoprops(glcm, prop='sum average')
# prop2 = util.greycoprops(glcm, prop='entropy')
# prop3 = util.greycoprops(glcm, prop='angular second moment')
# prop4 = util.greycoprops(glcm, prop='correlation')
# prop5 = util.greycoprops(glcm, prop='sum variance')
# prop6 = util.greycoprops(glcm, prop='sum entropy')
# prop7 = util.greycoprops(glcm, prop='entropy')
# end = time.time()
# print("funkcijski model")
# print(end-start)
#
# # objektni model
#
# start = time.time()
# hFeatures = hf(glcm)
#
#
# prop1 = hFeatures.greycoprops(prop='sum average')
# prop2 = hFeatures.greycoprops(prop='entropy')
# prop3 = hFeatures.greycoprops(prop='angular second moment')
# prop4 = hFeatures.greycoprops(prop='correlation')
# prop5 = hFeatures.greycoprops(prop='sum variance')
# prop6 = hFeatures.greycoprops(prop='sum entropy')
# prop7 = hFeatures.greycoprops(prop='entropy')
# end = time.time()
# print("objektni model")
# print(end-start)





# sobelx = cv.Sobel(img, cv.CV_16S, 1, 0, ksize=3)
# sobely = cv.Sobel(img, cv.CV_16S, 0, 1, ksize=3)
#
# # sobel1 = np.power(sobelx, 2) + np.power(sobely, 2)
# sobel1 = np.abs(sobelx) / 2 + np.abs(sobely) / 2
# # sobel1 = np.sqrt(sobel1)
#
#
# sobel = cv.Sobel(img, cv.CV_8U, 1, 1, ksize=3)
#
# lbp = local_binary_pattern(sobel1, 8, 1, method='default')
# print(np.amin(lbp))
# print(np.amax(lbp))
# print(lbp)
# cv.imshow("pic", lbp.astype('uint8'))
# cv.waitKey(0)



# a = np.array([[[[1, 2, 3],
#                [2, 2, 2],
#                [3, 3, 3]],
#
#               [[1, 1, 1],
#                [0, 0, 0],
#                [5, 3, 1]]],
#
#               [[[1, 2, 3],
#                 [2, 2, 2],
#                 [3, 3, 3]],
#
#                [[1, 1, 1],
#                 [0, 0, 0],
#                 [5, 3, 1]]]])



# import multiprocessing
#
# print(multiprocessing.cpu_count())
#
# a = [1, 2 , 3, 4]
# b = [2]

# import numpy as np
# X = np.array([[-1, -1], [-2, -2], [1, 1], [2, 1]])
# y = np.array([1, 2, 2, 2])
#
# from sklearn.svm import SVC
#
# clf = SVC(gamma='auto')
# clf.fit(X, y)
# print(clf.predict([[3, 1]]))
