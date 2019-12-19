import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
from os import listdir
from os.path import isfile, join
import os
import cv2 as cv
import numpy as np
from PIL import ImageTk, Image
import util
from skimage.feature import local_binary_pattern
import random
import Haralick
import LBPCM
from math import radians
from math import pi
import re
import threading
import queue

# boja obruba celije
color = (255, 0, 0)
# debljina crte putujuce celije
thickness = 2


# main class------------------------------
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

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

        # radijus LBP-a
        self.radius = 1
        # velicina celije
        self.cellSize = [64, 64]
        # velicina koraka
        self.stepSize = 32
        # kutevi za glcm
        self.angles = [pi / 4, pi / 2, pi - pi / 4]
        # razred za dohvat ko matrice lokalnih binarnih znacajki i izracun vektora znacajki
        self.lbpcm = LBPCM.LBPCM(self.radius, self.stepSize, self.cellSize,
                                 self.angles)  # stvaranje lbpcm s defaultnim vrijednostima
        # trenutna slika na stranici za parametre
        self.currPicPar = [[]]
        # rjecnik svih stranica
        self.frames = {}
        # staza do foldera sa slikama za treniranje
        self.trainingPath = ""
        # staza do foldera sa slikama za testiranje
        self.testPath = ""
        # trenutna slika
        self.currPicPath = ""
        # staza do slika za pretprocesiranje
        self.dataPath = ""
        # postotak ukupnih slika koje ce se iskoristiti za treniranje
        self.trainingSetSize = 0.7
        # polje slika za pretprocesiranje
        self.dataPictures = []
        # polje lokacija celije koja se krece po slici
        self.picDims = []
        # brojac trenutne celije
        self.currCell = 0
        # brojac trenutne slike
        self.picCounter = 0
        # polje imena slika za treniranje
        self.trainPictures = []
        # polje imena slika za testiranje
        self.testPictures = []
        # brojac za slike kod oznacavanja
        self.dataAnnotationCounter = 0
        # staza do procesiranih slika
        self.pathToProcessedData = r"data\processedData"
        # lista imena procesiranih slika
        self.processedDataPictures = []
        # rjecnik s oznacenim slikama
        self.labelDictionary = {}

        for F in (PreprocessPage,
                  StartPage,
                  PageInitialization,
                  ParameterSetting,
                  SlidingWindow,
                  DataAnnotation,
                  FeatureVectorCreation):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        """funkcija za prikaz odredjenog frame-a"""
        frame = self.frames[cont]
        frame.tkraise()

    def setTrainPath(self, path):
        """funkcija za postavljanje staze za treniranje"""

        self.trainingPath = path

    def setTestPath(self, path):
        """funkcija za postavljanje staze za testiranje"""

        self.testPath = path

    def nextCell(self):
        """ funkcija za pomicanje na sljedecu celiju u pojedinom slikovnom elementu
        """

        # ako nismo stigli do kraja slikovnog elementa
        if self.currCell < self.picDims.__len__() - 1:
            image = cv.imread(self.currPicPath)
            self.currCell += 1
            self.updateSlidingWindowImage(image)
            self.updateParameterFrame()
        else:
            self.console.insert(tk.END, "[WARNING] no more cells remaining\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def nextPic(self):
        """funkcija za dohvat sljedece slike"""
        #TODO napraviti da funkcionira kad se prvo izabere training folder, sad samo radi kad se prvo izabere data folder
        # resetiranje brojaca celije
        self.currCell = 0

        # ako ima jos slikovnih elemenata
        if self.picCounter < len(self.processedDataPictures):
            self.picCounter += 1
            fileName = self.pathToProcessedData + "/" + self.processedDataPictures[self.picCounter]
            self.currPicPath = fileName
            image = cv.imread(fileName)
            self.updateSlidingWindowImage(image)
            self.updateParameterFrame()
        else:
            self.console.insert(tk.END, "[WARNING] no more pictures remaining\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def prevPic(self):
        """funkcija za dohvat prethodne slike"""

        # resetriranje brojaca celije
        self.currCell = 0

        # ako ima jos slikovnih elemenata
        if self.picCounter >= 1:
            self.picCounter -= 1
            # staza do sljedece slike
            fileName = self.pathToProcessedData + "/" + self.processedDataPictures[self.picCounter]
            self.currPicPath = fileName
            image = cv.imread(fileName)
            # azuriranje slike
            self.updateSlidingWindowImage(image)
            self.updateParameterFrame()
        else:
            self.console.insert(tk.END, "[WARNING] no previous pictures remaining\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def resetCell(self):
        """ funkcija za resetiranje celije na sliding window stranici
        """

        self.currCell = 0
        image = cv.imread(self.currPicPath)
        self.updateSlidingWindowImage(image)
        self.updateParameterFrame()
        self.console.insert(tk.END, "[INFO] cell has been reset\n")
        self.console.insert(tk.END, "----------------------------------------\n")
        self.console.see(tk.END)

    def process(self):
        """ funkcija za dohvat dimenzija slikovnih elemenata i stvaranje istih
        """
        try:
            # dohvat x, y dimenzija
            x = int(self.frames[PreprocessPage].entryX.get())
            y = int(self.frames[PreprocessPage].entryY.get())
            # dimenzija svakog slikovnog elementa
            dim = (x, y)
            # stvaranje slikovnih elemenata
            self.makePictureElements(dim)
        except AttributeError:
            self.console.insert(tk.END, "[ERROR] invalid dimensions")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def makePictureElements(self, dim):
        """ funkcija za stvaranje slikovnih elemenata od slika koje se nalaze u data folderu,
            svaki slikovni element je velicine dim i sprema se u processeddata folder nakon
            sto je pretvoren u nijanse sive
        """

        if os.path.exists(self.pathToProcessedData):
            util.clearDirectory(self.pathToProcessedData)
        else:
            os.mkdir(self.pathToProcessedData)

        # popis svih slika izvorne velicine
        onlyFiles = [f for f in listdir(self.dataPath)]

        # mijesanje slika
        random.shuffle(onlyFiles)
        # spremanje slika za treniranje
        for f in onlyFiles:
            fileName = self.dataPath + "/" + f
            # normalna slika
            im = cv.imread(fileName)
            # # slika u sivim tonovima
            im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
            # spremanje slike
            util.saveImage(im_gray, self.pathToProcessedData, dim)

            self.dataAnnotationCounter += 1
            self.frames[PreprocessPage].progressbar.step()
            self.update()

        self.processedDataPictures = [f for f in listdir(self.pathToProcessedData)]
        # omogucavanje gumba za oznacavanje slika
        self.frames[PageInitialization].buttonDataAnnotation["state"] = "normal"
        # progressbar u feature vector creation frameu
        self.frames[FeatureVectorCreation].progressbarVector.configure(maximum=self.processedDataPictures.__len__())

        self.currPicPath = self.pathToProcessedData + "/" + self.processedDataPictures[0]
        image = cv.imread(self.currPicPath)
        # stvaranje koordinata putujuce celije kod tehnike kliznog prozora
        self.picDims = util.makePicDims(image, self.stepSize,
                                        self.cellSize)  # FIXME zamijeniti ovaj kurac sa manualnim unosom dimenzije slike
        self.updateSlidingWindowImage(image)
        self.updateParameterFrame()

        # self.trainPictures = [f for f in listdir(self.trainingPath)]
        # self.frames[PageInitialization].buttonSW['state'] = "normal"

    def selectImg(self):
        """ funkcija za dohvat i prikaz odabrane slike na stranici parametersetting
            i dodatno izracun LBP-a
        """

        try:
            # staza do odabrane slike preko izbornika
            path = filedialog.askopenfilename(initialdir=r"C:\Users\kuzmi\PycharmProjects\untitled",
                                              title="Select file",
                                              filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

            # pamcenje slike radi moguconsti refresha prilikom promjene parametra
            self.currPicPar = cv.imread(path, cv.IMREAD_GRAYSCALE)
            # omogucavanje gumba refresh
            self.frames[ParameterSetting].buttonRefresh.config(state="normal")
            self.im = ImageTk.PhotoImage(image=Image.fromarray(self.currPicPar))
            # postavaljanje slike u frame parametersetting
            self.frames[ParameterSetting].labelNormalPic.configure(image=self.im)
            # postavljanje imena ucitane slike
            self.frames[ParameterSetting].labelImageName.configure(text="image: " + path.split("/")[-1])
            # izracun LBP-a
            lbp = local_binary_pattern(self.currPicPar, self.radius * 8, self.radius)

            self.lbp = ImageTk.PhotoImage(image=Image.fromarray(lbp))
            # postavljanje lbp u labelu
            self.frames[ParameterSetting].labelLBPPic.configure(image=self.lbp)

        except AttributeError:
            pass

    def refreshLBP(self):
        """ funkcija za refresh LBP-a ako su se promjenili parametri na stranici parametersetting
        """

        # ponovni izracun LBP-a
        lbp = local_binary_pattern(self.currPicPar, self.radius * 8, self.radius)
        # konstrukcija slike iz polja
        self.lbp = ImageTk.PhotoImage(image=Image.fromarray(lbp))
        # prikaz slike u odgovarajucoj labeli
        self.frames[ParameterSetting].labelLBPPic.configure(image=self.lbp)

    def saveParameters(self, radius, cellSize, stepSize, angles):
        """funkcija za spremanje parametara u razerd"""

        flag = True
        try:
            self.radius = int(radius)
        except ValueError:
            self.console.insert(tk.END, "[ERROR] -- radius must be positive integer\n")
            self.console.see(tk.END)
            flag = False

        # konverzija stringa npr. 64x64 u int [64, 64]
        pattern = r"\b[0-9]{2}x[0-9]{2}\b"
        if re.match(pattern, cellSize):
            self.cellSize = [int(i) for i in cellSize.split("x")]
        else:
            self.console.insert(tk.END, "[ERROR] -- invalid cellsize configuration\n")
            self.console.see(tk.END)
            flag = False

        try:
            self.stepSize = int(stepSize)
        except ValueError:
            self.console.insert(tk.END, "[ERROR] -- step must be positive integer\n")
            self.console.see(tk.END)
            flag = False

        try:
            self.angles = [radians(int(i)) for i in angles.split(",")]
            self.lbpcm.setAngles(self.angles)
            self.frames[SlidingWindow].labelAnglesListValue.configure(text=str(self.angles))
        except ValueError:
            self.console.insert(tk.END, "[ERROR] -- angles must be positive integers, eg. 45,90\n")
            self.console.see(tk.END)
            flag = False

        if flag is True:
            self.console.insert(tk.END, "[INFO] -- parameters saved\n")
            self.console.see(tk.END)

        # azuriranje sliding window framea
        image = cv.imread(self.currPicPath)
        self.picDims = util.makePicDims(image, self.stepSize,
                                        self.cellSize)
        self.currCell = 0
        self.updateSlidingWindowImage(image)
        self.updateParameterFrame()

        self.console.insert(tk.END, "----------------------------------------\n")
        self.console.see(tk.END)

    def selectDataFolder(self):
        """ funkcija za odabir foldera koji se koristi za preprocesiranje
        """

        directory = filedialog.askdirectory()

        if directory != "":
            self.dataPath = directory
            self.console.insert(tk.END, "[INFO] data folder set: " + directory + "\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)
        else:
            self.console.insert(tk.END, "[WARNING] you did not select folder\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def updatePics(self):
        """ funkcija za azuriranje polja slika i maksimalne velicine progressbara
            prilikom ucitavanja i procesiranja slika
        """

        self.dataPictures = [f for f in listdir(self.dataPath)]
        if not self.dataPictures:
            self.console.insert(tk.END, "[WARNING] no pictures were found on: " + self.dataPath)
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)
        else:
            # postavljanje progressbara na maksimalnu vrijednost velicine polje slika koje treba obraditi
            self.frames[PreprocessPage].progressbar.configure(maximum=self.dataPictures.__len__())
            # staza do prve slike koja se postavlja u frameu radi prikaza kako dimenzije utjecu na slikovne elemente
            path = self.dataPath + "/" + self.dataPictures[0]
            image = cv.imread(path)

            # ako je visina slike veca od 300 piksela, radi se skaliranje
            if image.shape[0] > 300:
               image = util.resizePercent(image, 30)

            self.img = ImageTk.PhotoImage(image=Image.fromarray(image))
            self.frames[PreprocessPage].labelSeePicElements.configure(image=self.img)

    def updateSlidingWindowImage(self, image):
        """ funkcija za azuriranje slike i informacija na sliding window stranici
        """

        # pocetna i zavrsna tocka trenutne celije
        start_point, end_point = self.picDims[self.currCell]
        # stvaranje kopije izvorne slike kako celija ne bi ostala u slici prilikom kretanja na sljedecu celiju
        image_copy = cv.rectangle(np.copy(image), start_point, end_point, color, thickness)
        # trenutno pamcenje slike da se ne izbrise
        self.img = ImageTk.PhotoImage(image=Image.fromarray(image_copy))
        # postavaljanje imena slike u odgovarajucu labelu
        if not self.processedDataPictures:
            self.frames[SlidingWindow].labelPicName.configure(text=self.trainPictures[self.picCounter])
        else:
            self.frames[SlidingWindow].labelPicName.configure(text=self.processedDataPictures[self.picCounter])
        # postavljanje slike
        self.frames[SlidingWindow].labelPic.configure(image=self.img)

    def selectFolder(self, testOrTrain):
        """ funkcija za odabir folera za treniranje ili testiranje
        """

        # odabran put
        filename = filedialog.askdirectory()
        if testOrTrain == "train":
            # staza za treniranje
            self.setTrainPath(filename)
            # stvaranje polja slika za treniranje
            self.trainPictures = [f for f in listdir(self.trainingPath)]
            # postavljanje progressbara u frameu feature vector creation
            self.frames[FeatureVectorCreation].progressbarVector.configure(maximum=self.trainPictures.__len__())
            # dohvat prve slike
            self.currPicPath = filename + "/" + self.trainPictures[0]
            image = cv.imread(self.currPicPath)
            # stvaranje koordinata putujuce celije kod tehnike kliznog prozora
            self.picDims = util.makePicDims(image, self.stepSize,
                                            self.cellSize)  # FIXME zamijeniti ovaj kurac sa manualnim unosom dimenzije slike
            self.updateSlidingWindowImage(image)
            self.updateParameterFrame()

            # omogucavanje gumba sliding window
            self.frames[PageInitialization].buttonSW.config(state="normal")

            self.console.insert(tk.END, "[INFO] training path set: " + filename + "\n")
            self.console.insert(tk.END, "[INFO] loaded " + str(self.trainPictures.__len__()) + " training pictures\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)
        else:
            self.setTestPath(filename)
            self.testPictures = [f for f in listdir(self.testPath)]
            self.console.insert(tk.END, "[INFO] test path set: " + filename + "\n")
            self.console.insert(tk.END, "[INFO] loaded " + str(self.testPictures.__len__()) + " test pictures\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def updateParameterFrame(self):
        """ funkcija za azuriranje parametara na stranici s LBP-om
        """

        self.frames[SlidingWindow].labelCellNumberValue.configure(text=str(self.currCell))
        self.frames[SlidingWindow].labelAnglesListValue.configure(text=str(self.angles))
        # trenutna slika
        image = cv.imread(self.currPicPath, cv.IMREAD_GRAYSCALE)
        # dohvacanje pozicija trenutne celije
        picDims = self.picDims[self.currCell]
        # izlucivanje dijela slike koji priakzuje celija
        croppedImage = image[picDims[0][0]:picDims[1][0], picDims[0][1]:picDims[1][1]]
        # razred s haralickovim funkcijama
        haralick = Haralick.HaralickFeatures(self.lbpcm.getGLCM(croppedImage))
        # prikaz kontrasta
        contrast = haralick.contrast()
        self.frames[SlidingWindow].labelContrastValue.configure(text=str(contrast))

        energy = haralick.energy()
        self.frames[SlidingWindow].labelEnergyValue.configure(text=str(energy))

        homogeneity = haralick.homogeneity()
        self.frames[SlidingWindow].labelHomogeneityValue.configure(text=str(homogeneity))

        entropy = haralick.entropy()
        self.frames[SlidingWindow].labelEntropyValue.configure(text=str(entropy))

        self.update()

    def selectProcessedDataFolder(self):
        """ funkcija za odabir folders s vec procesiranim slikama
        """

        directory = filedialog.askdirectory()

        # ako je izabran neki direktorij
        if directory != "":

            self.pathToProcessedData = directory
            self.processedDataPictures = [f for f in listdir(self.pathToProcessedData)]
            self.frames[FeatureVectorCreation].progressbarVector.configure(maximum=self.processedDataPictures.__len__())
            self.frames[PageInitialization].buttonSW["state"] = "normal"

            self.currPicPath = self.pathToProcessedData + "/" + self.processedDataPictures[0]
            image = cv.imread(self.currPicPath)
            # stvaranje koordinata putujuce celije kod tehnike kliznog prozora
            self.picDims = util.makePicDims(image, self.stepSize,
                                            self.cellSize)  # FIXME zamijeniti ovaj kurac sa manualnim unosom dimenzije slike
            self.updateSlidingWindowImage(image)
            self.updateParameterFrame()

            # omogucavanje gumba za oznacavanje slika
            self.frames[PageInitialization].buttonDataAnnotation['state'] = "normal"

            self.console.insert(tk.END, "[INFO] processed data folder path set: " + directory + "\n")
            self.console.insert(tk.END,
                                "[INFO] loaded " + str(self.processedDataPictures.__len__()) + " processed pictures\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)
        else:
            self.console.insert(tk.END, "[WARNING] you did not select folder\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def updateDataAnnotationFrame(self):
        """ funkcija za azuriranje stranice za oznacavanje slika
        """

        # staza do trenutne slike
        imagePath = self.pathToProcessedData + "/" + self.processedDataPictures[self.dataAnnotationCounter]
        image = cv.imread(imagePath)
        self.im = ImageTk.PhotoImage(image=Image.fromarray(image))
        # postavljanje slike u labelu
        self.frames[DataAnnotation].labelPic.configure(image=self.im)
        # postavljanje imena slike u labelu
        self.frames[DataAnnotation].labelImageName.configure(
            text=self.processedDataPictures[self.dataAnnotationCounter])

    def prevPicAnnotation(self):
        """ funkcija za prikaz prethodne slike na stranici za oznacavanje slika
        """

        if self.dataAnnotationCounter >= 1:
            self.dataAnnotationCounter -= 1
            self.updateDataAnnotationFrame()
        else:
            self.console.insert(tk.END, "[WARNING] no previous pictures remaining\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def annotate(self, label):
        """ funkcija za stvaranje oznake pojedine slke i spremanje u rjecnik i datoteku
        """

        # ime slike
        picName = self.processedDataPictures[self.dataAnnotationCounter]
        # dodijeljena labela
        saveString = picName + ":" + label
        self.labelDictionary[picName] = label

        # ako smo dosli do zadnje onda se staje
        if self.dataAnnotationCounter < self.processedDataPictures.__len__():
            self.dataAnnotationCounter += 1
            self.updateDataAnnotationFrame()
            self.console.insert(tk.END, saveString + "\n")
            self.console.see(tk.END)
        else:
            self.console.insert(tk.END, "[INFO] all pictures labeled\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def saveAnnotedData(self):
        """ funkcija za spremanje rjecnika slika i oznaka
        """

        path = r"data\labeledData.txt"
        f = open(path, "w")
        for i in self.labelDictionary:
            row = str(i) + ":" + str(self.labelDictionary[i]) + "\n"
            f.write(row)
        f.close()

        self.console.insert(tk.END, "[INFO] labels and images saved to: " + path + "\n")
        self.console.insert(tk.END, "----------------------------------------\n")
        self.console.see(tk.END)

    def seeOnPic(self):
        """ funkcija za prikaz slikovnih elemenata na slici ako su zadane dimenzije
            slikovnih elemenata
        """

        # ako nije izabran folder prvo, nista se dalje ne izvodi
        if self.dataPath == "":
            self.console.insert(tk.END, "[WARNING] please select data folder" + "\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)
        else:
            # slika na kojoj se prikazuju slikovni elementi
            image = cv.imread(self.dataPath + "/" + self.dataPictures[0])

            # ako nisu upisane dimenzije slikovnog elementa
            if self.frames[PreprocessPage].entryX.get() == "" or self.frames[PreprocessPage].entryY.get() == "":
                self.console.insert(tk.END, "[WARNING] you haven't specifeid dimensions of a picture element" + "\n")
                self.console.insert(tk.END, "----------------------------------------\n")
                self.console.see(tk.END)
            else:
                # zeljena sirina slikovnog elementa
                x_size = int(self.frames[PreprocessPage].entryX.get())
                # zeljena visina slikovnog elementa
                y_size = int(self.frames[PreprocessPage].entryY.get())
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
                    cv.line(image, (x * x_size, 0), (x * x_size, imageY), color, thickness)

                # stvaranje crta u vertikalnom smjeru
                for y in range(stepY + 1):
                    cv.line(image, (0, y * y_size), (imageX, y * y_size), color, thickness)

                # ako je potrebno promijeniti velicinu slike
                if image.shape[0] > 300:
                    image = util.resizePercent(image, 30)

                # postavljanje slike u labelu
                self.img = ImageTk.PhotoImage(image=Image.fromarray(image))
                self.frames[PreprocessPage].labelSeePicElements.configure(image=self.img)

    def showFVCinfo(self):
        """ funkcija za azuriranje informacija u frameu feature vector creation
        """

        # data staza
        if self.dataPath == "":
            self.frames[FeatureVectorCreation].labelDataPathValue.configure(text="NOT SET")
        else:
            self.frames[FeatureVectorCreation].labelDataPathValue.configure(
                text=self.dataPath + "  (" + str(self.dataPictures.__len__()) + ") pictures")

        if self.pathToProcessedData == "":
            self.frames[FeatureVectorCreation].labelProcessedValue.configure(text="NOT SET")
        else:
            self.frames[FeatureVectorCreation].labelProcessedValue.configure(text=self.pathToProcessedData)

        # training staza
        if self.trainingPath == "":
            self.frames[FeatureVectorCreation].labelTrainValue.configure(text="NOT SET")
        else:
            self.frames[FeatureVectorCreation].labelTrainValue.configure(
                text=self.trainingPath + "  (" + str(self.trainPictures.__len__()) + ") pictures")

        # test staza
        if self.testPath == "":
            self.frames[FeatureVectorCreation].labelTestValue.configure(text="NOT SET")
        else:
            self.frames[FeatureVectorCreation].labelTestValue.configure(
                text=self.testPath + "  (" + str(self.testPictures.__len__()) + ") pictures")

        # LBP radius
        self.frames[FeatureVectorCreation].labelLBPRadiusValue.configure(text=self.radius)

        # velicina celije
        self.frames[FeatureVectorCreation].labelCellSizeValue.configure(text=self.cellSize)

        # kutevi za lpbcm
        self.frames[FeatureVectorCreation].labelAnglesValue.configure(text=self.angles)

        # velicina koraka celije
        self.frames[FeatureVectorCreation].labelStepSizeValue.configure(text=self.stepSize)

        # labela za napredak
        self.frames[FeatureVectorCreation].labelProgress.configure(text="0/" + str(self.processedDataPictures.__len__()))

    def makeFeatureVectors(self):
        """ funkcija za stvaranje vektora znacajki
        """

        # ako staza za treniranje nije postavljena
        if self.pathToProcessedData == "":
            self.console.insert(tk.END, "[WARNING] processed data path not set" + "\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)
        else:
            self.lbpcm.calculateFeatureVectors(self.pathToProcessedData,
                                               self.frames[FeatureVectorCreation].progressbarVector,
                                               self.frames[FeatureVectorCreation].labelProgress,
                                               self.frames[FeatureVectorCreation].labelFVCSize)

            self.console.insert(tk.END, "[INFO] feature vector creation completed\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def loadLabels(self):
        """ funkcija za ucitavanje oznaka slika koje su vec procesirane
        """

        file = filedialog.askopenfilename(initialdir=r"C:\Users\kuzmi\PycharmProjects\untitled\data",
                                          title="Select file",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))

        if file == "":
            self.console.insert(tk.END, "[WARNING] you did not select folder\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)
        else:
            with open(file) as f:
                rows = f.read()
                lines = rows.split("\n")

                for i in lines:
                    if i != "":
                        keyVal = i.split(":")
                        self.labelDictionary[keyVal[0]] = keyVal[1]


# frames----------------------------------
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        frame = tk.Frame(self)
        frame.place(in_=self, anchor="c", relx=.5, rely=.5)

        welcomeText = "This is the starting screen of the app.\nPlease use with caution!"
        label = tk.Label(frame, text=welcomeText)
        label.pack()

        buttonAgree = tk.Button(frame, text="Agree", command=lambda: controller.show_frame(PageInitialization))
        buttonAgree.pack()


class PageInitialization(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        description = tk.Label(self, text="Here you select training and testing folder.")
        description.pack(padx=10, pady=10)

        buttonFrame = tk.Frame(self)
        buttonFrame.pack()

        buttonPreprocess = tk.Button(buttonFrame, text="Preprocess data",
                                     command=lambda: controller.show_frame(PreprocessPage))

        buttonPreprocess.pack(padx=5, pady=10, fill="x")

        buttonSelectProcessedData = tk.Button(buttonFrame, text="Processed data",
                                              command=controller.selectProcessedDataFolder)
        buttonSelectProcessedData.pack(padx=5, pady=10, fill="x")

        buttonSelectTraining = tk.Button(buttonFrame, text="Training Folder",
                                         command=lambda: controller.selectFolder("train"))
        buttonSelectTraining.pack(padx=5, pady=10, fill="x")

        buttonSelectTest = tk.Button(buttonFrame, text="Test Folder", command=lambda: controller.selectFolder("test"))
        buttonSelectTest.pack(padx=10, pady=10, fill="x")

        self.buttonDataAnnotation = tk.Button(buttonFrame, text="Data Annotation", state="disabled",
                                              command=lambda: [controller.show_frame(DataAnnotation),
                                                               controller.updateDataAnnotationFrame()])

        self.buttonDataAnnotation.pack(padx=10, pady=10, fill="x")

        buttonParameters = tk.Button(buttonFrame, text="Parameters",
                                     command=lambda: controller.show_frame(ParameterSetting))
        buttonParameters.pack(padx=10, pady=10, fill="x")

        self.buttonSW = tk.Button(buttonFrame, text="Sliding Window", state="disabled",
                                  command=lambda: controller.show_frame(SlidingWindow))
        self.buttonSW.pack(padx=10, pady=10, fill="x")

        buttonFVC = tk.Button(buttonFrame, text="FVC", command=lambda: [controller.show_frame(FeatureVectorCreation),
                                                                        controller.showFVCinfo()])
        buttonFVC.pack(padx=10, pady=10, fill="x")

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(StartPage))
        buttonBack.pack(padx=10, pady=10, fill="x")


class ParameterSetting(tk.Frame):
    """ razred gdje se odabiru parametri LBP-a
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        description = tk.Label(self, text="Here you select parameters required for LBP.")
        description.pack()
        # prvi redak---------------------------
        frame1 = tk.Frame(self)
        frame1.pack(padx=10, pady=10, expand=True)

        labelRadius = tk.Label(frame1, text="Specify LBP radius:")
        labelRadius.pack(side="left")
        # upis radijusa
        entryRadius = tk.Entry(frame1)
        entryRadius.pack(side="right")

        # drugi redak--------------------------
        frame2 = tk.Frame(self)
        frame2.pack(padx=10, pady=10, expand=True)

        labelCellSize = tk.Label(frame2, text="Specify cell size, eg. \"64x64\".")
        labelCellSize.pack(side="left")
        # upis velicine celije za klizni prozor
        entryCellSize = tk.Entry(frame2)
        entryCellSize.pack(side="right")

        # treci redak--------------------------
        frame3 = tk.Frame(self)
        frame3.pack(padx=10, pady=10, expand=True)

        labelStepSize = tk.Label(frame3, text="Specify step size:")
        labelStepSize.pack(side="left")
        # upis velicine koraka
        entryStepSize = tk.Entry(frame3)
        entryStepSize.pack(side="right")

        frame31 = tk.Frame(self)
        frame31.pack(padx=10, pady=10, expand=True)

        labelAngles = tk.Label(frame31,
                               text="Specify angles(in degrees) for which you'd like to \ncalculate co-occurence matrix(separate them by comma, eg. 45,90,135): ")
        labelAngles.pack(side="left")

        entryAngles = tk.Entry(frame31)
        entryAngles.pack(side="right")

        labelRepresentation = tk.Label(self, text="Loaded image on the left and LBP on the right")
        labelRepresentation.pack()

        self.labelImageName = tk.Label(self, text="")
        self.labelImageName.pack()

        # cetvrti redak---------------------------
        frame4 = tk.Frame(self)
        frame4.pack(padx=10, pady=10, expand=True)

        self.labelNormalPic = tk.Label(frame4, text="no pic\nselected")
        self.labelNormalPic.grid(row=0, column=0, padx=10, pady=10)

        self.labelLBPPic = tk.Label(frame4, text="select pic\nfirst")
        self.labelLBPPic.grid(row=0, column=1, padx=10, pady=10)

        # peti redak------------------------
        frame5 = tk.Frame(self)
        frame5.pack(expand=True)
        # gumb za spremanje parametara LBP-a
        buttonSave = tk.Button(frame5, text="Save", command=lambda: controller.saveParameters(entryRadius.get(),
                                                                                              entryCellSize.get(),
                                                                                              entryStepSize.get(),
                                                                                              entryAngles.get()))
        buttonSave.pack(padx=10, pady=5, side="left")

        buttonSelectPic = tk.Button(frame5, text="Select img", command=controller.selectImg)
        buttonSelectPic.pack(padx=10, pady=5, side="left")

        self.buttonRefresh = tk.Button(frame5, text="Refresh", state="disabled", command=controller.refreshLBP)
        self.buttonRefresh.pack(padx=10, pady=5, side="left")

        buttonBack = tk.Button(frame5, text="Back", command=lambda: controller.show_frame(PageInitialization))
        buttonBack.pack(padx=10, pady=5, side="left")


class SlidingWindow(tk.Frame):
    """Razred gdje se prikazuje funkcionalnost kliznog prozora i vrijednost
        haralickovih funkcija u odredjenenim celijama slikovnog elementa
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        mainFrame = tk.Frame(self)
        # mainFrame.pack(side="left")
        mainFrame.grid(row=1, column=0, padx=20, pady=20)

        # opis stranice
        description = tk.Label(self, text="Here you can see sliding window method.")
        description.grid(padx=10, pady=10, row=0, columnspan=2)
        # labela za ime slike
        self.labelPicName = tk.Label(mainFrame, text="")
        self.labelPicName.pack()
        # labela za sliku
        self.labelPic = tk.Label(mainFrame, text="No picture\nloaded")
        self.labelPic.pack()

        # gumbi--------------------------
        buttonFrame = tk.Frame(mainFrame)
        buttonFrame.pack(padx=20, pady=20, side="bottom", expand=True)

        buttonNextPicture = tk.Button(buttonFrame, text="Next pic", command=controller.nextPic)
        buttonNextPicture.grid(row=0, column=1, padx=5, pady=5)

        buttonPreviousPicture = tk.Button(buttonFrame, text="Prev pic", command=controller.prevPic)
        buttonPreviousPicture.grid(row=0, column=0, padx=5, pady=5)

        buttonNextCell = tk.Button(buttonFrame, text="Next cell", command=controller.nextCell)
        buttonNextCell.grid(row=0, column=2, padx=5, pady=5)

        buttonReset = tk.Button(buttonFrame, text="Reset", command=controller.resetCell)
        buttonReset.grid(row=0, column=3, padx=5, pady=5)

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(PageInitialization))
        buttonBack.grid(row=0, column=4, padx=5, pady=5)

        # dio stranice s izracunatim vrijednostima haralickovih funkcija
        parameterFrame = tk.Frame(self)
        parameterFrame.grid(row=1, column=1, padx=20, pady=20)

        labelAnglesList = tk.Label(parameterFrame, text="Function values for angles(in rad): ")
        labelAnglesList.grid(row=0, column=0, padx=10, pady=10)

        self.labelAnglesListValue = tk.Label(parameterFrame, text="")
        self.labelAnglesListValue.grid(row=0, column=1, padx=10, pady=10)

        labelCellNumber = tk.Label(parameterFrame, text="Cell num. ")
        labelCellNumber.grid(row=1, column=0, padx=10, pady=10)

        self.labelCellNumberValue = tk.Label(parameterFrame, text="")
        self.labelCellNumberValue.grid(row=1, column=1, padx=10, pady=10)

        labelContrast = tk.Label(parameterFrame, text="Contrast: ")
        labelContrast.grid(row=2, column=0, padx=10, pady=10)

        self.labelContrastValue = tk.Label(parameterFrame, text="")
        self.labelContrastValue.grid(row=2, column=1, padx=10, pady=10)

        labelEnergy = tk.Label(parameterFrame, text="Energy: ")
        labelEnergy.grid(row=3, column=0, padx=10, pady=10)

        self.labelEnergyValue = tk.Label(parameterFrame, text="")
        self.labelEnergyValue.grid(row=3, column=1, padx=10, pady=10)

        labelHomogeneity = tk.Label(parameterFrame, text="Homogeneity: ")
        labelHomogeneity.grid(row=4, column=0, padx=10, pady=10)

        self.labelHomogeneityValue = tk.Label(parameterFrame, text="")
        self.labelHomogeneityValue.grid(row=4, column=1, padx=10, pady=10)

        labelEntropy = tk.Label(parameterFrame, text="Entropy: ")
        labelEntropy.grid(row=5, column=0, padx=10, pady=10)

        self.labelEntropyValue = tk.Label(parameterFrame, text="")
        self.labelEntropyValue.grid(row=5, column=1, padx=10, pady=10)


class PreprocessPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        labelDescription = tk.Label(self, text="Here you can specify parameters needed for data preprocessing")
        labelDescription.pack(padx=10, pady=10)

        frame1 = tk.Frame(self)
        frame1.pack()

        buttonSelectFolder = tk.Button(frame1, text="Select data folder",
                                       command=lambda: [controller.selectDataFolder(),
                                                        controller.updatePics()])
        buttonSelectFolder.pack(padx=10, pady=5)

        frame2 = tk.Frame(self)
        frame2.pack()

        labelRatio = tk.Label(frame2, text="training set size, eg. \"0.7\"")
        labelRatio.pack(padx=10, pady=5, side="left")

        self.entryRatio = tk.Entry(frame2)
        self.entryRatio.pack(side="right")

        labelDimDescription = tk.Label(self, text="Specify size of a picture element")
        labelDimDescription.pack(padx=10, pady=10)

        # frame s unosom dimenzija slikovnih elemenata-------------------------
        frame3 = tk.Frame(self)
        frame3.pack()

        labelDimensionX = tk.Label(frame3, text="X:")
        labelDimensionX.pack(side="left", padx=10, pady=5)

        self.entryX = tk.Entry(frame3)
        self.entryX.pack(side="left")

        labelDimensionY = tk.Label(frame3, text="Y:")
        labelDimensionY.pack(side="left", padx=10, pady=5)

        self.entryY = tk.Entry(frame3)
        self.entryY.pack(side="left")

        buttonSeePicElements = tk.Button(frame3, text="See on pic", command=controller.seeOnPic)
        buttonSeePicElements.pack(side="left", padx=10, pady=10)

        self.labelSeePicElements = tk.Label(self, text="No picture\nloaded.\nSelect data\nfolder first.")
        self.labelSeePicElements.pack(padx=10, pady=10)

        # frame s gumbom i progressbar-----------------------------------------
        frame4 = tk.Frame(self)
        frame4.pack()

        buttonProcess = tk.Button(frame4, text="Preprocess", command=controller.process)
        buttonProcess.pack(side="left", padx=10, pady=10)

        self.progressbar = Progressbar(frame4, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progressbar.pack(side="left", padx=10, pady=10)

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(PageInitialization))
        buttonBack.pack(padx=10, pady=10)


class DataAnnotation(tk.Frame):
    """ razred za oznacavanje pripadnosti pojedinog slikovnog elementa odredjenom razredu gustoce
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.labelImageName = tk.Label(self, text="")
        self.labelImageName.pack(padx=10, pady=10)

        self.labelPic = tk.Label(self, text="")
        self.labelPic.pack(padx=10, pady=10)

        buttonFrame = tk.Frame(self)
        buttonFrame.pack()

        # gumbi
        buttonZero = tk.Button(buttonFrame, text="No flow", command=lambda: controller.annotate('0'))
        buttonZero.grid(row=0, column=0, padx=10, pady=10)

        buttonFreeFlow = tk.Button(buttonFrame, text="Free Flow", command=lambda: controller.annotate('1'))
        buttonFreeFlow.grid(row=0, column=1, padx=10, pady=10)

        buttonRestrictedFlow = tk.Button(buttonFrame, text="Restricted flow", command=lambda: controller.annotate('2'))
        buttonRestrictedFlow.grid(row=0, column=2, padx=10, pady=10)

        buttonDenseFlow = tk.Button(buttonFrame, text="Dense flow", command=lambda: controller.annotate('3'))
        buttonDenseFlow.grid(row=0, column=3, padx=10, pady=10)

        buttonJammedFlow = tk.Button(buttonFrame, text="Jammed flow", command=lambda: controller.annotate('4'))
        buttonJammedFlow.grid(row=0, column=4, padx=10, pady=10)

        frameNav = tk.Frame(self)
        frameNav.pack(padx=10, pady=10)

        buttonPreviousPic = tk.Button(frameNav, text="Prev pic", command=controller.prevPicAnnotation)
        buttonPreviousPic.grid(row=0, column=0, padx=10, pady=10)

        buttonSave = tk.Button(frameNav, text="Save", command=controller.saveAnnotedData)
        buttonSave.grid(row=0, column=1, padx=10, pady=10)

        buttonBack = tk.Button(frameNav, text="Back", command=lambda: controller.show_frame(PageInitialization))
        buttonBack.grid(row=0, column=2, padx=10, pady=10)


class FeatureVectorCreation(tk.Frame):
    """ razred za stvaranje vektora znacajki
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        labelDescription = tk.Label(self, text="Here you can see program parameters and available info")
        labelDescription.pack(padx=10, pady=10)

        # frame s parametrima
        parameterFrame = tk.Frame(self)
        parameterFrame.pack()

        # frame sa stazom do foldera sa slikama za procesiranje
        dataFrame = tk.Frame(parameterFrame)
        dataFrame.pack()

        labelDataPath = tk.Label(dataFrame, text="Data path")
        labelDataPath.pack(side="left", padx=10, pady=5)

        self.labelDataPathValue = tk.Label(dataFrame, text="")
        self.labelDataPathValue.pack(side="right", padx=10, pady=5)

        # frame sa stazom do foldera sa procesiranim slikama
        processedFrame = tk.Frame(parameterFrame)
        processedFrame.pack()

        labelProcessed = tk.Label(processedFrame, text="Processed data path: ")
        labelProcessed.pack(side="left", padx=10, pady=5)

        self.labelProcessedValue = tk.Label(processedFrame, text="")
        self.labelProcessedValue.pack(side="right", padx=10, pady=5)

        # frame sa stazom do foldera sa slikama za treniranje
        trainFrame = tk.Frame(parameterFrame)
        trainFrame.pack()

        labelTrain = tk.Label(trainFrame, text="Training path: ")
        labelTrain.pack(side="left", padx=10, pady=5)

        self.labelTrainValue = tk.Label(trainFrame, text="")
        self.labelTrainValue.pack(side="right", padx=10, pady=5)

        # frame sa stazom do foldera sa slikama za testiranje
        testFrame = tk.Frame(parameterFrame)
        testFrame.pack()

        labelTest = tk.Label(testFrame, text="Test path: ")
        labelTest.pack(side="left", padx=10, pady=5)

        self.labelTestValue = tk.Label(testFrame, text="")
        self.labelTestValue.pack(side="right", padx=10, pady=5)

        # frame s parametrima LBP
        frameLBPParameters = tk.Frame(parameterFrame)
        frameLBPParameters.pack(pady=20)

        labelLBPParameters = tk.Label(frameLBPParameters, text="LBP parameters")
        labelLBPParameters.grid(row=0, padx=10, pady=5, columnspan=2)

        labelLBPRadius = tk.Label(frameLBPParameters, text="LBP radius: ")
        labelLBPRadius.grid(row=1, column=0, padx=10, pady=5)

        self.labelLBPRadiusValue = tk.Label(frameLBPParameters, text="")
        self.labelLBPRadiusValue.grid(row=1, column=1, padx=10, pady=5)

        labelCellSize = tk.Label(frameLBPParameters, text="Cell size: ")
        labelCellSize.grid(row=2, column=0, padx=10, pady=5)

        self.labelCellSizeValue = tk.Label(frameLBPParameters, text="")
        self.labelCellSizeValue.grid(row=2, column=1, padx=10, pady=5)

        labelAngles = tk.Label(frameLBPParameters, text="Angles: ")
        labelAngles.grid(row=3, column=0, padx=10, pady=5)

        self.labelAnglesValue = tk.Label(frameLBPParameters, text="")
        self.labelAnglesValue.grid(row=3, column=1, padx=10, pady=5)

        labelStepSize = tk.Label(frameLBPParameters, text="Step size: ")
        labelStepSize.grid(row=4, column=0, padx=10, pady=5)

        self.labelStepSizeValue = tk.Label(frameLBPParameters, text="")
        self.labelStepSizeValue.grid(row=4, column=1, padx=10, pady=5)

        frameProgress = tk.Frame(self)
        frameProgress.pack()

        self.progressbarVector = Progressbar(frameProgress, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progressbarVector.pack(side="left", padx=10, pady=5)

        self.labelProgress = tk.Label(frameProgress, text="")
        self.labelProgress.pack(side="right", padx=10, pady=5)

        # frame s gumbimaS
        buttonFrame = tk.Frame(self)
        buttonFrame.pack()

        buttonLoadAnnotedData = tk.Button(buttonFrame, text="Load labels", command=controller.loadLabels)
        buttonLoadAnnotedData.pack(side="left", padx=10, pady=5)

        buttonMakeVectors = tk.Button(buttonFrame, text="Make vectors", command=lambda: [threading.Thread(target=controller.makeFeatureVectors, daemon=True).start()])
        buttonMakeVectors.pack(side="left", padx=10, pady=5)

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(PageInitialization))
        buttonBack.pack(side="left", padx=10, pady=5)

        # frame s informacijom o velicini vektora znacajki
        frameFVCSize = tk.Frame(self)
        frameFVCSize.pack(pady=10)

        labelFVCSize = tk.Label(frameFVCSize, text="Feature vector dimension: ")
        labelFVCSize.pack(side="left", padx=10, pady=5)

        self.labelFVCSize = tk.Label(frameFVCSize, text="")
        self.labelFVCSize.pack(side="right", padx=10, pady=5)


if __name__ == "__main__":
    app = App()
    app.geometry("800x600")
    app.mainloop()
