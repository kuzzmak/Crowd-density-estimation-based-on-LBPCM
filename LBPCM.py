import cv2 as cv
from os import listdir
from skimage.feature import local_binary_pattern
from skimage.feature import greycomatrix
import util
import numpy as np
import Haralick
import tkinter as tk
import Pages.FeatureVectorCreationPage as fvcP


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

    def calculateFeatureVectors(self, app, verbose=True):
        # staza do foldera s već izrezanim slikama
        pathToProcessedData = app.configuration['processedImagesPath']

        progressBar = app.gui.frames[fvcP.FeatureVectorCreationPage].progressbarVector
        labelProgress = app.gui.frames[fvcP.FeatureVectorCreationPage].labelProgress

        # list svih slika u folderu
        pictures = [f for f in listdir(pathToProcessedData)]
        # postavljanje maximalne vrijednosti progerssbara
        progressBar.configure(maximum=len(pictures))

        self.featureVectors = []
        i = 0

        if verbose:
            app.gui.consolePrint("[INFO] started feature vector creation")

        for pic in pictures:
            # staza do slike
            fileName = pathToProcessedData + "/" + pic

            image = cv.imread(fileName, cv.IMREAD_GRAYSCALE)

            if self.picType == 'grad':
                image = cv.Sobel(image, cv.CV_8U, 1, 1, ksize=3)

            self.featureVectors.append(self.getFeatureVector(image))
            i += 1

            progressBar.step()
            labelProgress.configure(text=str(i) + "/" + str(pictures.__len__()) + "   Feature vectors completed.")

            if verbose:
                app.gui.consolePrint("\t\t" + str(i) + "/" + str(pictures.__len__()))

        if verbose:
            app.gui.consolePrint("[INFO] vector creation finished")
