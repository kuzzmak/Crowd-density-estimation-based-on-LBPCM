import cv2 as cv
from os import listdir
from skimage.feature import local_binary_pattern
from skimage.feature import greycomatrix
import util
import numpy as np
import Haralick
import tkinter as tk

class LBPCM:

    def __init__(self, radius, stepSize, windowSize, angles, glcmDistance, combineDistances=0, combineAngles=0):
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
        # kombiniraju li se matrice za sve udaljenosti u jednu ili ne
        self.combineDistances = combineDistances
        # kombiniraju li se matrice za kutove ili ne
        self.combineAngles = combineAngles
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

            energy = util.greycoprops(glcm, 'energy')
            contrast = util.greycoprops(glcm, 'contrast')
            homogeneity = util.greycoprops(glcm, 'homogeneity')
            entropy = util.greycoprops(glcm, 'entropy')

            if self.combineDistances:
                energy = np.sum(energy, axis=0)
                contrast = np.sum(contrast, axis=0)
                homogeneity = np.sum(homogeneity, axis=0)
                entropy = np.sum(entropy, axis=0)

            if self.combineAngles:
                energy = np.sum(energy, axis=1)
                contrast = np.sum(contrast, axis=1)
                homogeneity = np.sum(homogeneity, axis=1)
                entropy = np.sum(entropy, axis=1)

            if self.combineDistances == 0 and self.combineAngles == 0:

                for i in energy:
                    featureVector.extend(i)
                for i in contrast:
                    featureVector.extend(i)
                for i in homogeneity:
                    featureVector.extend(i)
                for i in entropy:
                    featureVector.extend(i)

            else:
                featureVector.extend(entropy)
                featureVector.extend(contrast)
                featureVector.extend(homogeneity)
                featureVector.extend(entropy)

        return featureVector

    def getGLCM(self, image):
        return greycomatrix(image.astype(int), self.glcmDistance, self.angles, levels=256)

    def setAngles(self, angles):
        self.angles = angles

    def setStepSize(self, stepSize):
        self.stepSize = stepSize

    def setWindowSize(self, windowSize):
        self.windowSize= windowSize

    def setRadius(self, radius):
        self.radius = radius

    def calculateFeatureVectors(self, pathToProcessedData, console, progressbar, labelProgress):
        # list svih slika u folderu
        pictures = [f for f in listdir(pathToProcessedData)]
        # pictures = pictures[:100]
        self.featureVectors = []
        i = 0
        # vecSize = str(self.getFeatureVector(cv.imread(pathToProcessedData + "/" + pictures[0], cv.IMREAD_GRAYSCALE)).__len__())
        # labelFVCSize.configure(text=vecSize)
        if not (console is None):
            console.insert(tk.END, "[INFO] started feature vector creation\n")
            console.see(tk.END)

        for pic in pictures:
            # staza do slike
            fileName = pathToProcessedData + "/" + pic
            image = cv.imread(fileName, cv.IMREAD_GRAYSCALE)
            self.featureVectors.append(self.getFeatureVector(image))
            i += 1
            if not(progressbar is None or labelProgress is None):
                progressbar.step()
                labelProgress.configure(text=str(i) + "/" + str(pictures.__len__()))

            if not (console is None):
                console.insert(tk.END, str(i) + "/" + str(pictures.__len__()) + "\n")
                console.see(tk.END)

        if not (console is None):
            console.insert(tk.END, "[INFO] vector creation finished\n")
            console.see(tk.END)

if __name__ == "__main__":
    lbpcm = LBPCM(radius=1)
    lbpcm.calculateFeatureVectors("data//trainingData")
    featureVectors = lbpcm.getFeatureVectors()
