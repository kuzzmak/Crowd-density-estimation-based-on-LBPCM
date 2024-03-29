import cv2 as cv
from os import listdir
from skimage.feature import local_binary_pattern
from skimage.feature import greycomatrix
import util
import numpy as np
import Haralick
from Pages import FeatureVectorCreationPage as fvcP

class LBPCM:

    def __init__(self, picType, radius, stepSize, windowSize, angles, glcmDistance, functions, combineDistances, combineAngles):

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

    def getFeatureVector(self, img, imageType):
        """
        Funkcija za stvaranje vektora značajki predane slike img

        :param img: slika čiji vektor značajki treba izračunati
        :param imageType vrsta slike nad kojom se izvodi LBP
        :return: vektor značajki predane slike
        """

        featureVector = []
        # stvaranje vektora znacajki za svaku celiju slikovnog elementa

        if imageType == 'grad':
            img = cv.Sobel(img, cv.CV_8U, 1, 1, ksize=3)

        lbp = self.getLBP(img)

        for im in util.sliding_window(lbp, self.stepSize, self.windowSize):

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

    def calculateFeatureVectors(self, app, verbose=True, progressBar=None, progressLabel=None):
        """
        Funkcija za izračunavanje vektora značajki slika koje su već procesirane

        :param app: referenca do glavne aplikacije
        :param verbose: ispis koraka ili ne
        :param progressBar progrss bar pojedine konfiguracije
        :param progressLabel labela za broj odrađenih vektora značajki
        """

        # staza do foldera s već izrezanim slikama
        pathToProcessedData = app.configuration['processedDataDirectory']

        # list svih slika u folderu
        pictures = [f for f in listdir(pathToProcessedData)]
        # labele su dodijeljene slikama po abecednom poretku
        pictures = sorted(pictures)
        # postavljanje maximalne vrijednosti progerssbara
        if not(progressBar is None):
            progressBar.configure(maximum=len(pictures))

        self.featureVectors = []
        i = 0

        if verbose:
            app.gui.consolePrint("[INFO] started feature vector creation")

        for pic in pictures:
            # staza do slike
            fileName = pathToProcessedData + "/" + pic

            image = cv.imread(fileName, cv.IMREAD_GRAYSCALE)

            self.featureVectors.append(self.getFeatureVector(image, self.picType))
            i += 1

            if not(progressBar is None):
                progressBar.step()
            if not(progressLabel is None):
                progressLabel.configure(text=str(i) + "/" + str(pictures.__len__()) + "   Feature vectors completed.")

        if verbose:
            app.gui.consolePrint("[INFO] vector creation finished")
