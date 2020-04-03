import tkinter as tk
from tkinter import filedialog
from os import listdir
import os
import cv2 as cv
import numpy as np
from PIL import ImageTk, Image
import util
from skimage.feature import local_binary_pattern
import random


import Pages.InitializationPage as iP
import Pages.GradientPage as gP
import Pages.StartPage as sP
import Pages.FeatureVectorCreationPage as fvcP
import Pages.ConfigurationsPage as coP
import Pages.PreprocessPage as pP
import Pages.ParameterSettingPage as psP
import Pages.SlidingWindowPage as swP
import Pages.DataAnnotationPage as daP
import Pages.ClassificationPage as clP
import Pages.FVC2Page as fvc2P


class App(tk.Tk):

    def __init__(self, app, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.app = app

        # frame koji sadrzi pojedinu stranicu
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # konzola
        consoleFrame = tk.Frame(self)
        consoleFrame.pack(side="bottom", fill="both", expand=True)
        # scrollbar konzole
        scroll = tk.Scrollbar(consoleFrame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.console = tk.Text(consoleFrame, height=5, width=30)
        self.console.pack(side="left", fill="both", expand=True)
        scroll.config(command=self.console.yview)
        self.console.config(yscrollcommand=scroll.set)

        labelConsole = tk.Label(self, text="Console window")
        labelConsole.pack(side="bottom")


        # trenutna slika na stranici za parametre
        self.currPicPar = [[]]
        # rjecnik svih stranica
        self.frames = {}
        # trenutna slika
        self.currPicPath = ""


        # polje slika za pretprocesiranje
        self.dataPictures = []
        # polje lokacija celije koja se krece po slici
        self.picDims = []
        # brojac trenutne slike
        self.picCounter = 0

        # brojac za slike kod oznacavanja
        self.dataAnnotationCounter = 0

        # lista imena procesiranih slika
        self.processedDataPictures = []

        # check gumbi za funkcije koje sačinjavaju vektore značajki
        self.functionButtons = []
        # stvaranje gumba za svaku od 14 funkcija
        self.names = ["angular second moment",
                 "contrast",
                 "correlation",
                 "sum of squares: variance",
                 "inverse difference moment",
                 "sum average",
                 "sum variance",
                 "sum entropy",
                 "entropy",
                 "difference variance",
                 "difference entropy",
                 "imoc1",
                 "imoc2",
                 "maximal correlation coefficient"]

        for c in range(14):
            name = "f" + str(c + 1)
            self.functionButtons.append((name, self.names[c], tk.IntVar()))

        for F in (pP.PreprocessPage,
                  sP.StartPage,
                  iP.InitializationPage,
                  psP.ParameterSettingPage,
                  swP.SlidingWindowPage,
                  daP.DataAnnotationPage,
                  fvcP.FeatureVectorCreationPage,
                  coP.ConfigurationsPage,
                  clP.ClassificationPage,
                  gP.GradientPage,
                  fvc2P.FVC2Page):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, sticky="nsew")

        self.show_frame(iP.InitializationPage)

    def show_frame(self, cont):
        """
        Funkcija za prikaz određenog frame-a
        """

        frame = self.frames[cont]
        frame.tkraise()

    def process(self):
        """
        Funkcija za dohvat dimenzija slikovnih elemenata i stvaranje istih
        """
        try:
            # dohvat x, y dimenzija
            x = int(self.frames[pP.PreprocessPage].entryX.get())
            y = int(self.frames[pP.PreprocessPage].entryY.get())
            # dimenzija svakog slikovnog elementa
            dim = (x, y)
            # stvaranje slikovnih elemenata
            self.makePictureElements(dim)
        except AttributeError:
            self.consolePrint("[ERROR] invalid dimensions")

    def makePictureElements(self, dim):
        """ funkcija za stvaranje slikovnih elemenata od slika koje se nalaze u data folderu,
            svaki slikovni element je velicine dim i sprema se u processeddata folder nakon
            sto je pretvoren u nijanse sive
        """

        if os.path.exists(self.app.configuration['processedImagesPath']):
            util.clearDirectory(self.app.configuration['processedImagesPath'])
        else:
            os.mkdir(self.app.configuration['processedImagesPath'])

        # popis svih slika izvorne velicine
        onlyFiles = [f for f in listdir(self.app.configuration['dataPath'])]

        # mijesanje slika
        random.shuffle(onlyFiles)
        # spremanje slika za treniranje
        for f in onlyFiles:
            fileName = self.app.configuration['dataPath'] + "/" + f
            # normalna slika
            im = cv.imread(fileName)
            # # slika u sivim tonovima
            im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
            # spremanje slike
            util.saveImage(im_gray, self.app.configuration['processedImagesPath'], dim)

            self.dataAnnotationCounter += 1

        self.processedDataPictures = [f for f in listdir(self.app.configuration['processedImagesPath'])]
        # omogucavanje gumba za oznacavanje slika
        self.frames[iP.InitializationPage].buttonDataAnnotation["state"] = "normal"

        self.currPicPath = self.app.configuration['processedImagesPath'] + "/" + self.processedDataPictures[0]
        image = cv.imread(self.currPicPath)
        # stvaranje koordinata putujuce celije kod tehnike kliznog prozora
        self.picDims = util.makePicDims(image, self.stepSize,
                                        self.cellSize)  # FIXME zamijeniti ovaj kurac sa manualnim unosom dimenzije slike

    def updateDataAnnotationFrame(self):
        pass
    #     """ funkcija za azuriranje stranice za oznacavanje slika
    #     """
    #
    #     # staza do trenutne slike
    #     imagePath = self.app.configuration['processedImagesPath'] + "/" + self.processedDataPictures[self.dataAnnotationCounter]
    #     image = cv.imread(imagePath)
    #     self.im = ImageTk.PhotoImage(image=Image.fromarray(image))
    #     # postavljanje slike u labelu
    #     self.frames[daP.DataAnnotationPage].labelPic.configure(image=self.im)
    #     # postavljanje imena slike u labelu
    #     self.frames[daP.DataAnnotationPage].labelImageName.configure(
    #         text=self.processedDataPictures[self.dataAnnotationCounter])
    #
    #     self.frames[daP.DataAnnotationPage].labelAnnotedDataCounter.configure(
    #         text=str(self.dataAnnotationCounter) + "/" + str(self.processedDataPictures.__len__()))

    def prevPicAnnotation(self):
        pass
    #     """ funkcija za prikaz prethodne slike na stranici za oznacavanje slika
    #     """
    #
    #     if self.dataAnnotationCounter >= 1:
    #         self.dataAnnotationCounter -= 1
    #         self.updateDataAnnotationFrame()
    #     else:
    #         self.console.insert(tk.END, "[WARNING] no previous pictures remaining\n")
    #         self.console.insert(tk.END, "----------------------------------------\n")
    #         self.console.see(tk.END)

    def annotate(self, label):
        pass
    #     """ funkcija za stvaranje oznake pojedine slke i spremanje u rjecnik i datoteku
    #     """
    #
    #     # ime slike
    #     picName = self.processedDataPictures[self.dataAnnotationCounter]
    #     # dodijeljena labela
    #     saveString = picName + ":" + label
    #     self.labelDictionary[picName] = label
    #
    #     # ako smo dosli do zadnje onda se staje
    #     if self.dataAnnotationCounter < self.processedDataPictures.__len__():
    #         self.dataAnnotationCounter += 1
    #         self.updateDataAnnotationFrame()
    #         self.console.insert(tk.END, saveString + "\n")
    #         self.console.see(tk.END)
    #     else:
    #         self.console.insert(tk.END, "[INFO] all pictures labeled\n")
    #         self.console.insert(tk.END, "----------------------------------------\n")
    #         self.console.see(tk.END)

    def saveAnnotedData(self):
        pass
    #     """ funkcija za spremanje rjecnika slika i oznaka
    #     """
    #
    #     self.writer.saveDirectory = r"data/normalData"
    #     self.writer.labelDictionary = self.labelDictionary
    #     self.writer.writeAnnotedDataToFile()
    #
    #     self.console.insert(tk.END, "[INFO] labels and images saved to: " + self.writer.saveDirectory + "\n")
    #     self.console.insert(tk.END, "[INFO] saved " + str(self.labelDictionary.__len__()) + " labeled images\n")
    #     self.console.insert(tk.END, "----------------------------------------\n")
    #     self.console.see(tk.END)

    def seeOnPic(self):
        """ funkcija za prikaz slikovnih elemenata na slici ako su zadane dimenzije
            slikovnih elemenata
        """

        # ako nije izabran folder prvo, nista se dalje ne izvodi
        if self.app.configuration['dataPath'] == "":
            self.console.insert(tk.END, "[WARNING] please select data folder" + "\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)
        else:
            # slika na kojoj se prikazuju slikovni elementi
            image = cv.imread(self.app.configuration['dataPath'] + "/" + self.dataPictures[0])

            # ako nisu upisane dimenzije slikovnog elementa
            if self.frames[pP.PreprocessPage].entryX.get() == "" or self.frames[pP.PreprocessPage].entryY.get() == "":
                self.console.insert(tk.END, "[WARNING] you haven't specifeid dimensions of a picture element" + "\n")
                self.console.insert(tk.END, "----------------------------------------\n")
                self.console.see(tk.END)
            else:
                # zeljena sirina slikovnog elementa
                x_size = int(self.frames[pP.PreprocessPage].entryX.get())
                # zeljena visina slikovnog elementa
                y_size = int(self.frames[pP.PreprocessPage].entryY.get())
                # sirina slike
                imageX = np.shape(image)[1]
                # visina slike
                imageY = np.shape(image)[0]
                # cjelobrojni broj koraka u x smjeru(koliko je moguce napraviti slikovnih elemenata sa sirinom x_size)
                stepX = imageX // x_size
                # koraci u y smjeru
                stepY = imageY // y_size

                # stvaranje crta u horizontalnom smjeru
                for x in range(stepX + 1):
                    cv.line(image, (x * x_size, 0), (x * x_size, imageY), (255, 0, 0), 2)

                # stvaranje crta u vertikalnom smjeru
                for y in range(stepY + 1):
                    cv.line(image, (0, y * y_size), (imageX, y * y_size), (255, 0, 0), 2)

                # ako je potrebno promijeniti velicinu slike
                if image.shape[0] > 300:
                    image = util.resizePercent(image, 30)

                # postavljanje slike u labelu
                self.img = ImageTk.PhotoImage(image=Image.fromarray(image))
                self.frames[pP.PreprocessPage].labelSeePicElements.configure(image=self.img)

    def showFVCinfo(self):
        """ funkcija za azuriranje informacija u frameu feature vector creation
        """

        # data staza
        # if self.dataPath == "":
        #     self.frames[fvcP.FeatureVectorCreationPage].labelDataPathValue.configure(text="NOT SET")
        # else:
        #     self.frames[fvcP.FeatureVectorCreationPage].labelDataPathValue.configure(
        #         text=self.dataPath + "  (" + str(self.dataPictures.__len__()) + ") pictures")
        #
        # # training staza
        # if self.trainingPath == "":
        #     self.frames[fvcP.FeatureVectorCreationPage].labelTrainValue.configure(text="NOT SET")
        # else:
        #     self.frames[fvcP.FeatureVectorCreationPage].labelTrainValue.configure(
        #         text=self.trainingPath + "  (" + str(self.trainPictures.__len__()) + ") pictures")
        #
        # # test staza
        # if self.testPath == "":
        #     self.frames[fvcP.FeatureVectorCreationPage].labelTestValue.configure(text="NOT SET")
        # else:
        #     self.frames[fvcP.FeatureVectorCreationPage].labelTestValue.configure(
        #         text=self.testPath + "  (" + str(self.testPictures.__len__()) + ") pictures")
        #
        # # LBP radius
        # self.frames[fvcP.FeatureVectorCreationPage].labelLBPRadiusValue.configure(text=self.radius)

        # # velicina celije
        # self.frames[fvcP.FeatureVectorCreationPage].labelCellSizeValue.configure(text=self.cellSize)
        #
        # # kutevi za lpbcm
        # self.frames[fvcP.FeatureVectorCreationPage].labelAnglesValue.configure(text=str(util.shortAngles(self.angles)))
        #
        # # velicina koraka celije
        # self.frames[fvcP.FeatureVectorCreationPage].labelStepSizeValue.configure(text=self.stepSize)

        # labela za napredak
        self.frames[fvcP.FeatureVectorCreationPage].labelProgress.configure(text="0/" + str(self.processedDataPictures.__len__())
                                                                        + "   Feature vectors completed.")
        self.frames[fvcP.FeatureVectorCreationPage].labelProgressConf.configure(text="0/0   Configurations completed.")

    def consolePrint(self, message, dots=True):
        """
        Funkcija za ispis poruke u konzolu

        :param message: poruka za ispis
        :param dots: ispisuju li se crtice za odvajanje poruka
        """

        self.console.insert(tk.END, message + "\n")
        if dots:
            self.console.insert(tk.END, "----------------------------------------\n")
        self.console.see(tk.END)

    def showClassifiedImage(self):

        filename = filedialog.askopenfilename(initialdir=r"data/normalData/View_001",
                                          title="Select picture",
                                          filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))

        # conf = self.writer.getConfiguration()

        self.frames[clP.ClassificationPage].labelPictureName.configure(text=filename)
        self.im = ImageTk.PhotoImage(image=Image.fromarray(util.resizePercent(cv.imread(filename), 60)))
        self.frames[clP.ClassificationPage].labelPicture.configure(image=self.im)

        # output = util.classifyImage(filename, self.writer.model, conf, self.console)

        # self.im = ImageTk.PhotoImage(image=Image.fromarray(output))
        # # postavljanje slike u labelu
        # self.frames[clP.ClassificationPage].labelPicture.configure(image=self.im)

    def loadColors(self):

        self.c0c = ImageTk.PhotoImage(image=Image.fromarray(cv.imread("icons/colors/0.jpg")))
        self.c1c = ImageTk.PhotoImage(image=Image.fromarray(cv.imread("icons/colors/1.jpg")))
        self.c2c = ImageTk.PhotoImage(image=Image.fromarray(cv.imread("icons/colors/2.jpg")))
        self.c3c = ImageTk.PhotoImage(image=Image.fromarray(cv.imread("icons/colors/3.jpg")))
        self.c4c = ImageTk.PhotoImage(image=Image.fromarray(cv.imread("icons/colors/4.jpg")))

        self.frames[clP.ClassificationPage].c0c.configure(image=self.c0c)
        self.frames[clP.ClassificationPage].c1c.configure(image=self.c1c)
        self.frames[clP.ClassificationPage].c2c.configure(image=self.c2c)
        self.frames[clP.ClassificationPage].c3c.configure(image=self.c3c)
        self.frames[clP.ClassificationPage].c4c.configure(image=self.c4c)



