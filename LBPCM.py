import cv2 as cv
from os import listdir
from skimage.feature import local_binary_pattern
from skimage.feature import greycomatrix
import util
import numpy as np
import Haralick

class LBPCM:

    def __init__(self, radius, stepSize, windowSize, angles, glcmDistance, combine=0):
        # udaljenost centralnog piksela
        self.radius = radius
        # velicina pomaka udesno ili dolje
        self.stepSize = stepSize
        # velicina stranice kvadrata celije koja se mice po slici
        self.windowSize = windowSize
        # broj piksela oko centralnog piksela
        self.no_points = 8 * radius
        # kutovi za koje se racuna glcm
        self.angles = angles
        # udaljenosti za koje se racuna matrica
        self.glcmDistance = glcmDistance
        # kombiniraju li se matrice za sve kuteve u jednu ili ne
        self.combine = combine
        # lista vektora znacajki
        self.featureVectors = []

    # funkcija za stvaranje LBP-a odredjene slike
    def getLBP(self, im_gray):
        return local_binary_pattern(im_gray, self.no_points, self.radius, method='default')

    # funkcija za dohvat liste vektora znacajki
    def getFeatureVectors(self):
        return self.featureVectors

    def getFeatureVector(self, im_gray):

        # # vektor znacajki
        featureVector = []
        # stvaranje vektora znacajki za svaku celiju slikovnog elementa
        for im in util.sliding_window(self.getLBP(im_gray), self.stepSize, self.windowSize):
            # gray level co-occurence matrix
            glcm = self.getGLCM(im)
            # razred s harlickovim funkcijama
            hf = Haralick.HaralickFeatures(glcm)
            # energija
            energy = hf.energy()
            featureVector.extend(energy)
            # kontrast
            contrast = hf.contrast()
            featureVector.extend(contrast)
            # homogenost
            homogeneity = hf.homogeneity()
            featureVector.extend(homogeneity)
            # entropija
            entropy = hf.entropy()
            featureVector.extend(entropy)

        return featureVector

    def getGLCM(self, image):
        return greycomatrix(image.astype(int), self.glcmDistance, self.angles, levels=256, normed=True)

    def setAngles(self, angles):
        self.angles = angles

    def setStepSize(self, stepSize):
        self.stepSize = stepSize

    def setWindowSize(self, windowSize):
        self.windowSize= windowSize

    def setRadius(self, radius):
        self.radius = radius

    def calculateFeatureVectors(self, pathToProcessedData, progressbar, labelProgress):
        # list svih slika u folderu
        pictures = [f for f in listdir(pathToProcessedData)]
        i = 0

        # vecSize = str(self.getFeatureVector(cv.imread(pathToProcessedData + "/" + pictures[0], cv.IMREAD_GRAYSCALE)).__len__())
        # labelFVCSize.configure(text=vecSize)

        for pic in pictures:
            # staza do slike
            fileName = pathToProcessedData + "/" + pic
            image = cv.imread(fileName, cv.IMREAD_GRAYSCALE)
            self.featureVectors.append(self.getFeatureVector(image))
            i += 1
            if not(progressbar is None or labelProgress is None):
                progressbar.step()
                labelProgress.configure(text=str(i) + "/" + str(pictures.__len__()))
            print(str(i) + " " + str(self.angles))


if __name__ == "__main__":
    lbpcm = LBPCM(radius=1)
    lbpcm.calculateFeatureVectors("data//trainingData")
    featureVectors = lbpcm.getFeatureVectors()
