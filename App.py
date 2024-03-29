import json

from math import radians

import tkinter as tk
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image
import cv2 as cv

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
import os

import LBPCM
import GUI
import Writer
import util
import VotingClassifier

from Pages import ConfigurationsPage as coP
from Pages import FeatureVectorCreationPage as fvcP
from Pages import CLP2 as clP2

class App:

    def __init__(self):

        # rječnik konfiguracije, sadrži staze do potrebnih resursa za aplikaciju
        self.configuration = {}
        # razred za manipulaciju s konfiguracijama, modelima i labelama
        self.writer = Writer.Writer()
        # rječnik labela
        self.labelDictionary = {}
        # lista konfiguracija za učenje modela
        self.configurations = []

        self.pictureToClassify = ""
        self.writers = []

        self.confNumber = 0



        if os.path.isfile("configuration.json"):
            with open("configuration.json") as json_file:
                self.configuration = json.load(json_file)

        else:
            util.makeConfigurationFile()

            with open("configuration.json") as json_file:
                self.configuration = json.load(json_file)

        self.gui = GUI.App(self)

    def loadLabels(self):
        """
        Funkcija za učitavanje oznaka slika koje su već procesirane
        """

        self.writer.loadAnnotedDataFromFile(os.path.join(self.configuration['labeledDataDirectory'], 'labeledData.txt'))
        self.labelDictionary = self.writer.labelDictionary
        self.dataAnnotationCounter = self.writer.labelDictionary.__len__()
        self.gui.consolePrint("[INFO] loaded " + str(self.labelDictionary.__len__()) + " labels")
        self.gui.frames[fvcP.FeatureVectorCreationPage].labelLabelsLoadedColor.configure(text="LOADED", fg="green")

    def addConf(self):
        """
        Funkcija za dohvaćanje parametara konfiguracije iz polja za unos sa stranice
        ConfigurationsPage
        """

        parametersOK = True

        # dohvat vrste slike nad kojom se provodi postupak LBP
        picType = self.gui.frames[coP.ConfigurationsPage].rPicType.get()

        classifierType = self.gui.frames[coP.ConfigurationsPage].rClassifierType.get()

        # dohvat parametara za konfiguraciju
        try:
            radius = int(self.gui.frames[coP.ConfigurationsPage].entryLBPRadius.get())
            if radius < 1:
                raise ValueError
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for radius")

        try:
            glcmDistance = [int(x) for x in self.gui.frames[coP.ConfigurationsPage].entryGLCMDistance.get().split(",")]
            for d in glcmDistance:
                if d < 1:
                    raise ValueError
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for glcm distance")

        try:
            stepSize = int(self.gui.frames[coP.ConfigurationsPage].entryStepSize.get())
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for step size")

        try:
            cellSize = [int(x) for x in self.gui.frames[coP.ConfigurationsPage].entryCellSize.get().split(",")]
            if len(cellSize) != 2:
                raise ValueError
            for c in cellSize:
                if c < 1:
                    raise ValueError
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for cell size")

        try:
            angles = [radians(int(i)) for i in self.gui.frames[coP.ConfigurationsPage].entryAngles.get().split(",")]
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for angles")

        try:
            numOfNeighbors = int(self.gui.frames[coP.ConfigurationsPage].entryNumOfNeighbors.get())
            if numOfNeighbors < 1:
                raise ValueError
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for number of neighbors")

        combineDistances = self.gui.frames[coP.ConfigurationsPage].rCombineDistances.get()
        combineAngles = self.gui.frames[coP.ConfigurationsPage].rCombineAngles.get()

        functions = []

        # dohvaćanje imena odabranih funkcija
        for _, name, c in self.gui.functionButtons:
            if c.get():
                functions.append(name)

        if len(functions) == 0:
            parametersOK = False
            self.gui.consolePrint("[INFO] please select one or more Haralick functions")

        if parametersOK:
            # pojedina konfiguracija
            conf = [classifierType,
                    picType,
                    radius,
                    glcmDistance,
                    stepSize,
                    cellSize,
                    angles,
                    numOfNeighbors,
                    combineDistances,
                    combineAngles,
                    functions]

            self.configurations.append(conf)

            self.gui.console.insert(tk.END, "new configuration added\n")
            self.gui.console.insert(tk.END, str(conf) + "\n")
            self.gui.console.see(tk.END)

            frame = tk.Frame(self.gui.frames[fvcP.FeatureVectorCreationPage].middleFrame)
            frame.pack(pady=10)

            progressBar = Progressbar(frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
            progressBar.pack(side="left", padx=10)

            numOfPictures = len(os.listdir(self.configuration['processedDataDirectory']))

            progressLabel = tk.Label(frame, text="0/" + str(numOfPictures) + "   Feature vectors completed.")
            progressLabel.pack(side="left")

            self.gui.frames[fvcP.FeatureVectorCreationPage].progressBars.append(progressBar)
            self.gui.frames[fvcP.FeatureVectorCreationPage].progressLabels.append(progressLabel)

            conf.append(self.confNumber)
            self.confNumber += 1

    def runConf(self, conf):
        """ Funkcija koja napravi vektore znacajki i klasifikator za pojedinu konfuguraciju parametara
        """

        classifierType, \
        picType, \
        radius, \
        glcmDistance, \
        stepSize, \
        cellSize, \
        angles, \
        numOfNeighbors, \
        combineDistances, \
        combineAngles, \
        functions, \
        confNumber = conf

        lbpcm = LBPCM.LBPCM(picType,
                            radius,
                            stepSize,
                            cellSize,
                            angles,
                            glcmDistance,
                            functions,
                            combineDistances,
                            combineAngles)

        lbpcm.calculateFeatureVectors(self,
                                      verbose=True,
                                      progressBar=self.gui.frames[fvcP.FeatureVectorCreationPage].progressBars[confNumber],
                                      progressLabel=self.gui.frames[fvcP.FeatureVectorCreationPage].progressLabels[confNumber])

        fv = lbpcm.getFeatureVectors()

        conf = conf[:len(conf) - 1]
        # normalizacija vektora
        fv, mean, sigma = util.normalize(fv)
        conf.extend(mean.tolist())
        conf.extend(sigma.tolist())

        trainRatio = 0.7

        #TODO napraviti funkciju koja radi ovo ispod
        X_train = fv[:round(trainRatio * fv.__len__())]
        X_test = fv[round(trainRatio * fv.__len__()):]

        Y = []
        for i in self.labelDictionary.values():
            Y.append(int(i))

        Y_train = Y[:round(trainRatio * fv.__len__())]
        Y_test = Y[round(trainRatio * fv.__len__()):fv.__len__()]

        self.gui.consolePrint("\t[INFO] fitting started")

        if classifierType == 'kNN':
            kneighbors = KNeighborsClassifier(n_neighbors=numOfNeighbors)
            kneighbors.fit(X_train, Y_train)
            error = 1 - kneighbors.score(X_test, Y_test)
            self.gui.consolePrint("\t[INFO] error: " + str(error))
            conf.append(error)
            self.writer.saveModel(kneighbors, conf, self)

        else:
            svm = SVC(probability=True)
            svm.fit(X_train, Y_train)
            error = 1 - svm.score(X_test, Y_test)
            self.gui.consolePrint("\t[INFO] error: " + str(error))
            conf.append(error)
            self.writer.saveModel(svm, conf, self)

        self.gui.consolePrint("\t[INFO] fitting finished")

        self.gui.consolePrint("[INFO] configuration completed")

    def runConfigurations(self):
        """
        Funkcija za pokretanje pojedine unesene konfiguracije.
        """

        with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
            executor.map(self.runConf, self.configurations)

    def classify(self):
        """
        Metoda za klasifikaciju izabrane slike.
        """

        models = [x.model for x in self.writers]
        configurations = [x.modelConfiguration for x in self.writers]

        if self.gui.onlyVotingClassifier.get() == 0:
            i = 0
            self.im = [0, 0]

            for model in models:

                output = util.classifyImage(self.pictureToClassify, model, configurations[i])

                self.im[i] = ImageTk.PhotoImage(image=Image.fromarray(util.resizePercent(output, 20)))

                self.gui.frames[clP2.CLP2].pcpFrames[i].labelImage.configure(image=self.im[i])
                i += 1

        vc = VotingClassifier.VotingClassifier(models, configurations)

        image = cv.imread(self.pictureToClassify)

        labels = vc.clasify(cv.cvtColor(image, cv.COLOR_BGR2GRAY))
        output = util.showLabeledImage(labels, image)

        self.img = ImageTk.PhotoImage(image=Image.fromarray(util.resizePercent(output, 50)))

        self.gui.frames[clP2.CLP2].resultImage.configure(image=self.img)
        self.gui.frames[clP2.CLP2].labelPeopleCount.configure(text="Estimated people count = " +
                                                                   str(util.getPeopleCount(labels)))


if __name__ == "__main__":

    app = App()
    app.gui.title("Crowd density estimation based on LBPCM")
    app.gui.mainloop()

