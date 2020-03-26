# import LBPCM
# import numpy as np
# import util
# from sklearn.preprocessing import normalize
# from scipy import stats
# lbpcm = LBPCM.LBPCM('grad',
#                             1,
#                             32,
#                             [64, 64],
#                             [0],
#                             [1],
#                             ['angular second moment', 'contrast', 'correlation'],
#                             0,
#                             0)
#
# lbpcm.calculateFeatureVectors(r'/home/tonkec/Desktop/fo', None, None, None)
#
# fv = lbpcm.getFeatureVectors()

# for f in fv:
#     print(f)
# print()

# util.normalize(fv)

# print("vectors")
# for f in fv:
#     print(f)
# import time
# print("moje")
# start = time.time()
# util.normalize(fv)
# end = time.time()
# print(end-start)


# for f in fv:
#     print(f)
#
# print()
# print("lib")
# a = stats.zscore(fv, ddof=1)
# for i in a:
#     print(i)
# print("lib")
# start = time.time()
# a = stats.zscore(fv, ddof=1)
# end = time.time()
# print(end-start)
# print()





# import numpy as np
# import cv2 as cv
# from skimage.feature import greycomatrix
# import math
# import util
#
# from Haralick import HaralickFeatures as hf
#
# image = np.array([[0, 0, 1, 1], [0, 0, 1, 1], [0, 2, 2, 2], [2, 2, 3, 3]])
# # image = cv.imread("/home/tonkec/Desktop/220px-Lenna_(test_image).png", cv.IMREAD_GRAYSCALE)
# glcm = greycomatrix(image.astype(int), [1, 2], [0], levels=4)
#
#
#
# print(glcm.shape)


#
# # glcm = glcm.astype(np.float64)
# # glcm_sums = np.apply_over_axes(np.sum, glcm, axes=(0, 1))
# # glcm_sums[glcm_sums == 0] = 1
# # glcm /= glcm_sums
#
# def Q(i, j):
#     #TODO napraviti nešto s dijeljenjem sa 0
#     # dodati assert
#     row_i = glcm[i, :, :, :]
#     row_j = glcm[j, :, :, :]
#     i_y = row_i * row_j
#
#     p_x = np.apply_over_axes(np.sum, glcm, axes=1)
#     p_y = np.apply_over_axes(np.sum, glcm, axes=0)
#
#     p_x_y = (p_x[i] * p_y)
#     p_x_y[p_x_y == 0] = 1
#
#     return np.apply_over_axes(np.sum, i_y / p_x_y, axes=(0, 1))
#
#
# # print(glcm[:, :, 0, 0])
# # print(glcm[:, :, 1, 0])
# print(Q(0, 1))

# glcm = glcm.astype(np.float64)
# glcm_sums = np.apply_over_axes(np.sum, glcm, axes=(0, 1))
# glcm_sums[glcm_sums == 0] = 1
# glcm /= glcm_sums

# import time
# start = time.time()
#
# p_x = np.apply_over_axes(np.sum, glcm, axes=1)
# p_y = np.apply_over_axes(np.sum, glcm, axes=0)
# HXY = -np.sum(glcm * np.log(glcm + 1e-12), axis=(0, 1))
# p_x_y = p_x * p_y
# HXY1 = -np.sum(glcm * np.log(p_x_y + 1e-12), axis=(0, 1))
# HXY2 = -np.sum(p_x_y * np.log(p_x_y + 1e-12), axis=(0, 1))
# HX = -np.sum(p_x * np.log(p_x + 1e-12), axis=(0, 1))
# HY = -np.sum(p_y * np.log(p_y + 1e-12), axis=(0, 1))
# results = (HXY - HXY1) / np.maximum(HX, HY)
#
# results2 = np.sqrt(1 - np.exp(-2 * (HXY2 - HXY)))

# print(results)
# end = time.time()
# print(end-start)
# p_x_y = p_x * p_y
# print("prod")
# print(-np.sum(glcm * np.log(p_x_y), axis=(0,1)))


# hFeatures = hf(glcm)
# # hFeatures.greycoprops(prop='difference entropy')
# hFeatures.pxminy(0)
# hFeatures.pxminy(1)
# print("dict")
# print(hFeatures.pxminyDict)

# import time
# start = time.time()
# end = time.time()
# print(end-start)

# import time
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
# objektni model

# start = time.time()



#
#
# prop1 = hFeatures.greycoprops(prop='sum average')
# prop2 = hFeatures.greycoprops(prop='entropy')
# prop3 = hFeatures.greycoprops(prop='angular second moment')
# prop4 = hFeatures.greycoprops(prop='correlation')
# prop5 = hFeatures.greycoprops(prop='sum variance')
# prop6 = hFeatures.greycoprops(prop='sum entropy')
# prop7 = hFeatures.greycoprops(prop='entropy')
# print(hFeatures.greycoprops(prop='difference entropy'))
# end = time.time()
# print("objektni model")
# print(end-start)



# from skimage.feature import local_binary_pattern
#
# img = cv.imread("/home/tonkec/Desktop/220px-Lenna_(test_image).png", cv.IMREAD_GRAYSCALE)
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
#
# lbp = local_binary_pattern(sobel1, 8, 1, method='default')
# print(sobel)
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
# X_test = np.array([[3, 1], [0, 0], [3, 0]])
# Y_test = np.array([2, 2, 2])
#
# from sklearn.svm import SVC
#
# clf = SVC(gamma='auto')
# clf.fit(X, y)
# error = 1 - clf.score(X_test, Y_test)
#
# a = []
# a.append(error)
# a.append(2)
#
# print(a)

# import Writer
#
# writer = Writer.Writer()
# import json
# with open("data/models_v2/models.json") as f:
#     data = json.load(f)
#
# conf = writer.loadConfFromJSON(3)
# print(conf)
