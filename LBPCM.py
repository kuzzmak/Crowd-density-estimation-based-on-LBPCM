import cv2 as cv
from os import listdir
from skimage.feature import local_binary_pattern
from skimage.feature import greycomatrix
from skimage.feature import greycoprops
import util
import numpy as np

class LBPCM:

    def __init__(self, radius):
        # udaljenost centralnog piksela
        self.radius = radius
        # broj piksela oko centralnog piksela
        self.no_points = 8 * radius
        self.featureVectors = []


    def getLBP(self, im_gray):
        return local_binary_pattern(im_gray, self.no_points, self.radius, method='default')


    def getFeatureVector(self, im_gray):
        # velicina klizeceg prozora
        xy = 64
        windowSize = [xy, xy]
        # velicina koraka
        stepSize = xy // 2

        featureVector = []

        for im in util.sliding_window(self.getLBP(im_gray), stepSize, windowSize):
            glcm = greycomatrix(im.astype(int), [1], [0, np.pi / 2, np.pi, np.pi + np.pi / 2], levels=256)
            hf = util.HaralickFeatures(glcm)
            energy = hf.energy()
            featureVector.extend(energy)
            contrast = hf.contrast()
            featureVector.extend(contrast)
            homogeneity = hf.homogeneity()
            featureVector.extend(homogeneity)
            entropy = hf.entropy()
            featureVector.extend(entropy)



        return featureVector

    def calculateFeatureVectors(self, pathToTrainingData):
        pictures = [f for f in listdir(pathToTrainingData)]
        for pic in pictures:
            fileName = pathToTrainingData + "\\" + pic
            image = cv.imread(fileName, cv.IMREAD_GRAYSCALE)
            self.featureVectors.append(self.getFeatureVector(image))


if __name__ == "__main__":
    lbpcm = LBPCM(radius=1)
    lbpcm.calculateFeatureVectors("data//trainingData")

