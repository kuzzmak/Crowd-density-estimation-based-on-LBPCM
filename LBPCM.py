import cv2 as cv
from os import listdir
from skimage.feature import local_binary_pattern
from skimage.feature import greycomatrix
import util
import numpy as np
import Haralick
import tkinter as tk


class LBPCM:

    def __init__(self, picType, radius, stepSize, windowSize, angles, glcmDistance, functions, combineDistances=0, combineAngles=0):
        # vrsta slike na kojoj se radi LBP
        self.picType = picType
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
        # Haralickove funkcije koje se izračunavaju za pojedinu konfiguraciju
        self.functions = functions
        # kombiniraju li se matrice za sve udaljenosti u jednu ili ne
        self.combineDistances = combineDistances
        # kombiniraju li se matrice za kutove ili ne
        self.combineAngles = combineAngles
        # lista vektora znacajki
        self.featureVectors = []

    # funkcija za stvaranje LBP-a odredjene slike
    def getLBP(self, img):
        return local_binary_pattern(img, self.no_points, self.radius, method='default')

    # funkcija za dohvat liste vektora znacajki
    def getFeatureVectors(self):
        return np.array(self.featureVectors)

    def getFeatureVector(self, img):
        """
        Funkcija za stvaranje vektora značajki predane slike img

        :param img: slika čiji vektor značajki treba izračunati
        :return: vektor značajki predane slike
        """

        featureVector = []
        # stvaranje vektora znacajki za svaku celiju slikovnog elementa
        for im in util.sliding_window(self.getLBP(img), self.stepSize, self.windowSize):

            glcm = self.getGLCM(im)

            hf = Haralick.HaralickFeatures(glcm)

            for f in self.functions:
                temp = hf.greycoprops(prop=f)
                for t in temp:
                    featureVector.extend(list(t))

            # if self.combineDistances:
            #     energy = np.sum(energy, axis=0)
            #     contrast = np.sum(contrast, axis=0)
            #     homogeneity = np.sum(homogeneity, axis=0)
            #     entropy = np.sum(entropy, axis=0)
            #
            # if self.combineAngles:
            #     energy = np.sum(energy, axis=1)
            #     contrast = np.sum(contrast, axis=1)
            #     homogeneity = np.sum(homogeneity, axis=1)
            #     entropy = np.sum(entropy, axis=1)
            #
            # if self.combineDistances == 0 and self.combineAngles == 0:
            #
            #     for i in energy:
            #         featureVector.extend(i)
            #     for i in contrast:
            #         featureVector.extend(i)
            #     for i in homogeneity:
            #         featureVector.extend(i)
            #     for i in entropy:
            #         featureVector.extend(i)

            # featureVector.extend(entropy)
            # featureVector.extend(contrast)
            # featureVector.extend(homogeneity)
            # featureVector.extend(entropy)

        return featureVector

    def getGLCM(self, image):
        """
        Funkcija za dobivanje matrice pojavnosti sivih razina predane slike img
        Matrica je dimenzija (num_level, num_level, num_distances, num_angles), gdje je
        num_level broj sivih razina slike, num_distances broj različitih udaljenosti za koje
        se matrica računa, a num_angles broj kutova za koje se matrica računa

        :param image: slika čija se matrica pojavnosti računa
        :return: matrica pojavnosti
        """
        return greycomatrix(image.astype(int), self.glcmDistance, self.angles, levels=256)

    def calculateFeatureVectors(self, pathToProcessedData, console, progressbar, labelProgress):
        # list svih slika u folderu
        pictures = [f for f in listdir(pathToProcessedData)]
        self.featureVectors = []
        i = 0

        if not (console is None):
            console.insert(tk.END, "[INFO] started feature vector creation\n")
            console.see(tk.END)

        for pic in pictures:
            # staza do slike
            fileName = pathToProcessedData + "/" + pic

            image = cv.imread(fileName, cv.IMREAD_GRAYSCALE)

            if self.picType == 'grad':
                image = cv.Sobel(image, cv.CV_8U, 1, 1, ksize=3)

            self.featureVectors.append(self.getFeatureVector(image))
            i += 1

            if not(progressbar is None or labelProgress is None):
                progressbar.step()
                labelProgress.configure(text=str(i) + "/" + str(pictures.__len__()) + "   Feature vectors completed.")

            if not (console is None):
                console.insert(tk.END, str(i) + "/" + str(pictures.__len__()) + "\n")
                console.see(tk.END)

        if not (console is None):
            console.insert(tk.END, "[INFO] vector creation finished\n")
            console.see(tk.END)

