
# X = [[0], [1], [2], [3]]
# y = [0, 0, 1, 1]
# from sklearn.neighbors import KNeighborsClassifier
# neigh = KNeighborsClassifier(n_neighbors=3)
# neigh.fit(X, y)
#
# print(neigh.predict([[1.1]]))
#
# print(neigh.predict_proba([[1.1]]))


# import cv2 as cv
#
# picCounter = 0
#
# # funkcija za rezanje slike u 4 dijela i spremanje
# def saveImage(im, dim):
#
#     global picCounter
#
#     # zeljena sirina slikovnog elementa
#     x_size = dim[0]
#     # zeljena visina slikovnog elementa
#     y_size = dim[1]
#     # sirina slike
#     imageX = im.shape[1]
#     # visina slike
#     imageY = im.shape[0]
#     # cjelobrojni broj koraka u x smjeru(koliko je moguce napraviti slikovnih elemenata sa sirinom x_size)
#     stepX = imageX // x_size
#     # koraci u y smjeru
#     stepY = imageY // y_size
#
#     for y in range(stepY):
#         for x in range(stepX):
#             croppedImage = im[y * y_size:(y + 1) * y_size, x * x_size:(x + 1) * x_size]
#             imName = path + "/" + str(picCounter) + ".jpg"
#             cv.imwrite(imName, croppedImage)
#             picCounter += 1





# path = r"C:\Users\kuzmi\Desktop\Crowd_PETS09\S1\L1\Time_13-57\View_001\frame_0000.jpg"
# image = cv.imread(path)
# dimension = (180, 144)
# saveImage(image, dimension)

# dictionary = {}
#
# with open(r"C:\Users\kuzmi\PycharmProjects\untitled\data\labeledData.txt") as f:
#     row = f.read()
#     lines = row.split("")
#
#     for i in lines:
#         if i != "":
#             keyVal = i.split(":")
#             dictionary[keyVal[0]] = keyVal[1]
#
# print(dictionary)

# import LBPCM
# from math import radians
# import cv2 as cv
# import numpy as np
# radius = 1
# stepSize = 32
# windowSize = [64, 64]
# angles = [radians(45), radians(90), radians(135)]
# lbpcm = LBPCM.LBPCM(radius, stepSize, windowSize, angles)
# im = cv.imread(r"C:\Users\kuzmi\PycharmProjects\Crowd-density-estimation-based-on-LBPCM\data\processedData\5.jpg")
# # mat = lbpcm.getGLCM(im)
# # lbp = lbpcm.getLBP(im)
# start_point = (0, 0)
# end_point = (64, 64)
# color = (255, 0, 0)
# thickness = 2
#
# image_copy = cv.rectangle(np.copy(im), start_point, end_point, color, thickness)
#
# cv.imshow("wind", image_copy)
# cv.waitKey(0)

import numpy as np
import math

vecs = [[1,2,3,4,5], [0,6,10,2,1], [0,8,8,1,4]]

def normalize(vectors):

    numOfVecs = vecs.__len__()
    dimension = vecs[0].__len__()

    sums = [0] * dimension

    for v in range(numOfVecs):
        for i in range(dimension):
            sums[i] += vecs[v][i]

    mean = [x / numOfVecs for x in sums]

    sigma = [0] * dimension

    for v in range(numOfVecs):
        for i in range(dimension):
            sigma[i] += (vecs[v][i] - mean[i]) ** 2

    sigma = [1 / (numOfVecs - 1) * x for x in sigma]
    sigma = [math.sqrt(x) for x in sigma]
    print(vecs)
    print(sums)
    print(mean)
    print(sigma)


if __name__ == "__main__":
    normalize(vecs)
