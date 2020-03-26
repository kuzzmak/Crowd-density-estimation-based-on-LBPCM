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
import Haralick
import LBPCM
from math import radians
from math import pi
import re
import threading
import pickle
import Writer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

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
        # udaljenosti za koje se racuna glcm
        self.glcmDistance = [1]
        # razred za dohvat ko matrice lokalnih binarnih znacajki i izracun vektora znacajki
        self.lbpcm = LBPCM.LBPCM('grad', self.radius, self.stepSize, self.cellSize,
                                 self.angles, self.glcmDistance, ['f1', 'f2'])  # stvaranje lbpcm s defaultnim vrijednostima
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
        self.pathToProcessedData = r"data/processedData"
        # lista imena procesiranih slika
        self.processedDataPictures = []
        # rjecnik s oznacenim slikama
        self.labelDictionary = {}
        # lista konfiguracija koje se trebaju izvesti
        self.configurations = []
        # vrijednost radio gumba combine distances
        self.rbDistances = tk.IntVar()
        # vrijednost radio gumba combine angles
        self.rbAngles = tk.IntVar()
        # razred za spremanje rezultata i labela
        self.writer = Writer.Writer()
        # varijabla za odabir vrste slika na kojima se primjenjuje LBP, na sivim ili gradijentnim slikama
        self.rType = tk.IntVar()
        # variajble za odabir vrste klasifikatora
        self.cType = tk.IntVar()
        # koristi li se za klasifikaciju jedan ili dva modela
        self.numOfModels = tk.IntVar()
        # vrsta modela koji se gleda u izborniku modela
        self.modelType = tk.StringVar()

        # check gumbi za funkcije koje sačinjavaju vektore značajki
        self.functionButtons = []
        # stvaranje gumba za svaku od 14 funkcija

        names = ["angular second moment",
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
            self.functionButtons.append((name, names[c], tk.IntVar()))

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

        self.show_frame(sP.StartPage)

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
            self.currCell += 1
            self.updateSlidingWindowImage()
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
            self.updateSlidingWindowImage()
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
            # azuriranje slike
            self.updateSlidingWindowImage()
            self.updateParameterFrame()
        else:
            self.console.insert(tk.END, "[WARNING] no previous pictures remaining\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def resetCell(self):
        """ funkcija za resetiranje celije na sliding window stranici
        """

        self.currCell = 0
        self.updateSlidingWindowImage()
        self.updateParameterFrame()
        self.console.insert(tk.END, "[INFO] cell has been reset\n")
        self.console.insert(tk.END, "----------------------------------------\n")
        self.console.see(tk.END)

    def process(self):
        """ funkcija za dohvat dimenzija slikovnih elemenata i stvaranje istih
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
            self.frames[pP.PreprocessPage].progressbar.step()
            self.update()

        self.processedDataPictures = [f for f in listdir(self.pathToProcessedData)]
        # omogucavanje gumba za oznacavanje slika
        self.frames[iP.InitializationPage].buttonDataAnnotation["state"] = "normal"
        # progressbar u feature vector creation frameu
        self.frames[fvcP.FeatureVectorCreationPage].progressbarVector.configure(maximum=self.processedDataPictures.__len__())

        self.currPicPath = self.pathToProcessedData + "/" + self.processedDataPictures[0]
        image = cv.imread(self.currPicPath)
        # stvaranje koordinata putujuce celije kod tehnike kliznog prozora
        self.picDims = util.makePicDims(image, self.stepSize,
                                        self.cellSize)  # FIXME zamijeniti ovaj kurac sa manualnim unosom dimenzije slike
        self.updateSlidingWindowImage()
        self.updateParameterFrame()

        # self.trainPictures = [f for f in listdir(self.trainingPath)]
        # self.frames[iP.InitializationPage].buttonSW['state'] = "normal"

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
            self.frames[psP.ParameterSettingPage].buttonRefresh.config(state="normal")
            self.im = ImageTk.PhotoImage(image=Image.fromarray(self.currPicPar))
            # postavaljanje slike u frame parametersetting
            self.frames[psP.ParameterSettingPage].labelNormalPic.configure(image=self.im)
            # postavljanje imena ucitane slike
            self.frames[psP.ParameterSettingPage].labelImageName.configure(text="image: " + path.split("/")[-1])
            # izracun LBP-a
            lbp = local_binary_pattern(self.currPicPar, self.radius * 8, self.radius)

            self.lbp = ImageTk.PhotoImage(image=Image.fromarray(lbp))
            # postavljanje lbp u labelu
            self.frames[psP.ParameterSettingPage].labelLBPPic.configure(image=self.lbp)

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
        self.frames[psP.ParameterSettingPage].labelLBPPic.configure(image=self.lbp)

    def saveParameters(self, radius, cellSize, stepSize, angles):
        """funkcija za spremanje parametara u razerd"""

        flag = True
        try:
            self.radius = int(radius)
            self.lbpcm.setRadius(self.radius)
        except ValueError:
            self.console.insert(tk.END, "[ERROR] -- radius must be positive integer\n")
            self.console.see(tk.END)
            flag = False

        # konverzija stringa npr. 64x64 u int [64, 64]
        pattern = r"\b[0-9]{2}x[0-9]{2}\b"
        if re.match(pattern, cellSize):
            self.cellSize = [int(i) for i in cellSize.split("x")]
            self.lbpcm.setWindowSize(self.cellSize)
        else:
            self.console.insert(tk.END, "[ERROR] -- invalid cellsize configuration\n")
            self.console.see(tk.END)
            flag = False

        try:
            self.stepSize = int(stepSize)
            self.lbpcm.setStepSize(self.stepSize)
        except ValueError:
            self.console.insert(tk.END, "[ERROR] -- step must be positive integer\n")
            self.console.see(tk.END)
            flag = False

        try:
            self.angles = [radians(int(i)) for i in angles.split(",")]
            self.lbpcm.setAngles(self.angles)
            self.frames[swP.SlidingWindowPage].labelAnglesListValue.configure(text=str(self.angles))
        except ValueError:
            self.console.insert(tk.END, "[ERROR] -- angles must be positive integers, eg. 45,90\n")
            self.console.see(tk.END)
            flag = False

        if flag is True:
            self.console.insert(tk.END, "[INFO] -- parameters saved\n")
            self.console.see(tk.END)

        # azuriranje sliding window framea
        image = cv.imread(self.currPicPath)
        self.picDims = util.makePicDims(image, self.stepSize, self.cellSize)
        self.currCell = 0
        self.updateSlidingWindowImage()
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
            self.frames[pP.PreprocessPage].progressbar.configure(maximum=self.dataPictures.__len__())
            # staza do prve slike koja se postavlja u frameu radi prikaza kako dimenzije utjecu na slikovne elemente
            path = self.dataPath + "/" + self.dataPictures[0]
            image = cv.imread(path)

            # ako je visina slike veca od 300 piksela, radi se skaliranje
            if image.shape[0] > 300:
               image = util.resizePercent(image, 30)

            self.img = ImageTk.PhotoImage(image=Image.fromarray(image))
            self.frames[pP.PreprocessPage].labelSeePicElements.configure(image=self.img)

    def updateSlidingWindowImage(self):
        """ funkcija za azuriranje slike i informacija na sliding window stranici
        """

        # pocetna i zavrsna tocka trenutne celije
        start_point, end_point = self.picDims[self.currCell]
        # trenutna slika
        image = cv.imread(self.currPicPath, cv.IMREAD_GRAYSCALE)
        # lbp trenutne slike
        lbp = self.lbpcm.getLBP(image)
        # samo za prikaz pravokutnika u boji na slici koja je grayscale
        lbp = cv.cvtColor(lbp.astype('uint8') * 255, cv.COLOR_GRAY2RGB)

        # stvaranje kopije izvorne slike kako celija ne bi ostala u slici prilikom kretanja na sljedecu celiju
        image_copy = cv.rectangle(np.copy(lbp), start_point, end_point, (255, 0, 0), 2)

        # trenutno pamcenje slike da se ne izbrise
        self.LBPimg = ImageTk.PhotoImage(image=Image.fromarray(image_copy))
        self.im = ImageTk.PhotoImage(image=Image.fromarray(image))

        # postavaljanje imena slike u odgovarajucu labelu
        if not self.processedDataPictures:
            self.frames[swP.SlidingWindowPage].labelPicName.configure(text=self.trainPictures[self.picCounter])
        else:
            self.frames[swP.SlidingWindowPage].labelPicName.configure(text=self.processedDataPictures[self.picCounter])
        # postavljanje slike
        self.frames[swP.SlidingWindowPage].labelLBPPic.configure(image=self.LBPimg)
        self.frames[swP.SlidingWindowPage].labelPic.configure(image=self.im)

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
            self.frames[fvcP.FeatureVectorCreationPage].progressbarVector.configure(maximum=self.trainPictures.__len__())
            # dohvat prve slike
            self.currPicPath = filename + "/" + self.trainPictures[0]
            image = cv.imread(self.currPicPath)
            # stvaranje koordinata putujuce celije kod tehnike kliznog prozora
            self.picDims = util.makePicDims(image, self.stepSize,
                                            self.cellSize)  # FIXME zamijeniti ovaj kurac sa manualnim unosom dimenzije slike
            self.updateSlidingWindowImage()
            self.updateParameterFrame()

            # omogucavanje gumba sliding window
            self.frames[iP.InitializationPage].buttonSW.config(state="normal")

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

        self.frames[swP.SlidingWindowPage].labelCellNumberValue.configure(text=str(self.currCell))
        self.frames[swP.SlidingWindowPage].labelAnglesListValue.configure(text=str(util.shortAngles(self.angles)))

        # trenutna slika
        image = cv.imread(self.currPicPath, cv.IMREAD_GRAYSCALE)

        # lbp trenutne slike
        lbp = self.lbpcm.getLBP(image)
        # dohvacanje pozicija trenutne celije
        picDims = self.picDims[self.currCell]
        # izlucivanje dijela slike koji prikazuje celija
        croppedImage = lbp[picDims[0][0]:picDims[1][0], picDims[0][1]:picDims[1][1]]

        # razred s haralickovim funkcijama
        haralick = Haralick.HaralickFeatures(self.lbpcm.getGLCM(croppedImage))
        # prikaz kontrasta
        contrast = haralick.contrast()
        self.frames[swP.SlidingWindowPage].labelContrastValue.configure(text=str(util.shortAngles(contrast)))
        # prikaz energije
        energy = haralick.energy()
        self.frames[swP.SlidingWindowPage].labelEnergyValue.configure(text=str(util.shortAngles(energy)))
        # prikaz homogenosti
        homogeneity = haralick.homogeneity()
        self.frames[swP.SlidingWindowPage].labelHomogeneityValue.configure(text=str(util.shortAngles(homogeneity)))
        # prikaz entropije
        entropy = haralick.entropy()
        self.frames[swP.SlidingWindowPage].labelEntropyValue.configure(text=str(util.shortAngles(entropy)))

        self.update()

    def selectProcessedDataFolder(self):
        """ funkcija za odabir folders s vec procesiranim slikama
        """

        directory = filedialog.askdirectory(initialdir=r"data/processedData")

        # ako je izabran neki direktorij
        if directory != "":

            self.pathToProcessedData = directory
            self.processedDataPictures = [f for f in listdir(self.pathToProcessedData)]
            self.frames[fvcP.FeatureVectorCreationPage].progressbarVector.configure(maximum=self.processedDataPictures.__len__())
            self.frames[iP.InitializationPage].buttonSW["state"] = "normal"
            self.frames[iP.InitializationPage].buttonGradient["state"] = "normal"

            self.currPicPath = self.pathToProcessedData + "/" + self.processedDataPictures[0]
            image = cv.imread(self.currPicPath)
            # stvaranje koordinata putujuce celije kod tehnike kliznog prozora
            self.picDims = util.makePicDims(image, self.stepSize,
                                            self.cellSize)  # FIXME zamijeniti ovaj kurac sa manualnim unosom dimenzije slike
            # self.updateSlidingWindowImage()
            # self.updateParameterFrame()

            # omogucavanje gumba za oznacavanje slika
            self.frames[iP.InitializationPage].buttonDataAnnotation['state'] = "normal"

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
        self.frames[daP.DataAnnotationPage].labelPic.configure(image=self.im)
        # postavljanje imena slike u labelu
        self.frames[daP.DataAnnotationPage].labelImageName.configure(
            text=self.processedDataPictures[self.dataAnnotationCounter])

        self.frames[daP.DataAnnotationPage].labelAnnotedDataCounter.configure(
            text=str(self.dataAnnotationCounter) + "/" + str(self.processedDataPictures.__len__()))

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

        self.writer.saveDirectory = r"data/normalData"
        self.writer.labelDictionary = self.labelDictionary
        self.writer.writeAnnotedDataToFile()

        self.console.insert(tk.END, "[INFO] labels and images saved to: " + self.writer.saveDirectory + "\n")
        self.console.insert(tk.END, "[INFO] saved " + str(self.labelDictionary.__len__()) + " labeled images\n")
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
        if self.dataPath == "":
            self.frames[fvcP.FeatureVectorCreationPage].labelDataPathValue.configure(text="NOT SET")
        else:
            self.frames[fvcP.FeatureVectorCreationPage].labelDataPathValue.configure(
                text=self.dataPath + "  (" + str(self.dataPictures.__len__()) + ") pictures")

        # training staza
        if self.trainingPath == "":
            self.frames[fvcP.FeatureVectorCreationPage].labelTrainValue.configure(text="NOT SET")
        else:
            self.frames[fvcP.FeatureVectorCreationPage].labelTrainValue.configure(
                text=self.trainingPath + "  (" + str(self.trainPictures.__len__()) + ") pictures")

        # test staza
        if self.testPath == "":
            self.frames[fvcP.FeatureVectorCreationPage].labelTestValue.configure(text="NOT SET")
        else:
            self.frames[fvcP.FeatureVectorCreationPage].labelTestValue.configure(
                text=self.testPath + "  (" + str(self.testPictures.__len__()) + ") pictures")

        # LBP radius
        self.frames[fvcP.FeatureVectorCreationPage].labelLBPRadiusValue.configure(text=self.radius)

        # velicina celije
        self.frames[fvcP.FeatureVectorCreationPage].labelCellSizeValue.configure(text=self.cellSize)

        # kutevi za lpbcm
        self.frames[fvcP.FeatureVectorCreationPage].labelAnglesValue.configure(text=str(util.shortAngles(self.angles)))

        # velicina koraka celije
        self.frames[fvcP.FeatureVectorCreationPage].labelStepSizeValue.configure(text=self.stepSize)

        # labela za napredak
        self.frames[fvcP.FeatureVectorCreationPage].labelProgress.configure(text="0/" + str(self.processedDataPictures.__len__())
                                                                        + "   Feature vectors completed.")
        self.frames[fvcP.FeatureVectorCreationPage].labelProgressConf.configure(text="0/0   Configurations completed.")

    def loadLabels(self):
        """ funkcija za ucitavanje oznaka slika koje su vec procesirane
        """

        file = filedialog.askopenfilename(initialdir=r"data/normalData",
                                          title="Select labeled data file",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))

        if len(file) == 0:
            self.console.insert(tk.END, "[WARNING] you did not select file with labeled data\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)
        else:
            self.writer.loadAnnotedDataFromFile(file)
            self.labelDictionary = self.writer.labelDictionary
            self.dataAnnotationCounter = self.writer.labelDictionary.__len__()

            self.console.insert(tk.END, "[INFO] loaded " + str(self.labelDictionary.__len__()) + " labels\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def consolePrint(self, message):
        self.console.insert(tk.END, message + "\n")
        self.console.insert(tk.END, "----------------------------------------\n")
        self.console.see(tk.END)

    def addConf(self):
        """
            Funkcija za dohvaćanje parametara konfiguracije iz polja za unos sa stranice
            ConfigurationsPage
        :return:
        """

        parametersOK = True

        # dohvat vrste slike nad kojom se provodi postupak LBP
        picType = self.rType.get()
        if picType == 0:
            picType = "gray"
        else:
            picType = "grad"

        classifierType = self.cType.get()
        if classifierType == 0:
            classifierType = "kNN"
        else:
            classifierType = "SVM"

        # dohvat parametara za konfiguraciju
        try:
            radius = int(self.frames[coP.ConfigurationsPage].entryLBPRadius.get())
            if radius < 1:
                raise ValueError
        except ValueError:
            parametersOK = False
            self.consolePrint("[ERROR] please check your input for radius")

        try:
            glcmDistance = [int(x) for x in self.frames[coP.ConfigurationsPage].entryGLCMDistance.get().split(",")]
            for d in glcmDistance:
                if d < 1:

                    raise ValueError
        except ValueError:
            parametersOK = False
            self.consolePrint("[ERROR] please check your input for glcm distance")

        try:
            stepSize = int(self.frames[coP.ConfigurationsPage].entryStepSize.get())
        except ValueError:
            parametersOK = False
            self.consolePrint("[ERROR] please check your input for step size")

        try:
            cellSize = [int(x) for x in self.frames[coP.ConfigurationsPage].entryCellSize.get().split(",")]
            if len(cellSize) != 2:
                raise ValueError
            for c in cellSize:
                if c < 1:
                    raise ValueError
        except ValueError:
            parametersOK = False
            self.consolePrint("[ERROR] please check your input for cell size")

        try:
            angles = [radians(int(i)) for i in self.frames[coP.ConfigurationsPage].entryAngles.get().split(",")]
        except ValueError:
            parametersOK = False
            self.consolePrint("[ERROR] please check your input for angles")

        try:
            numOfNeighbors = int(self.frames[coP.ConfigurationsPage].entryNumOfNeighbors.get())
            if numOfNeighbors < 1:
                raise ValueError
        except ValueError:
            parametersOK = False
            self.consolePrint("[ERROR] please check your input for number of neighbors")

        combineDistances = int(self.rbDistances.get())
        combineAngles = int(self.rbAngles.get())

        functions = []

        for _, name, c in self.functionButtons:
            if c.get():
                functions.append(name)

        if len(functions) == 0:
            parametersOK = False
            self.consolePrint("[INFO] please select one or more Haralick functions")

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

            # ažuriranje labele broja konfiguracija
            self.frames[fvcP.FeatureVectorCreationPage].labelProgressConf.configure(text="0/" + str(len(self.configurations))
                                                                                + "   Configurations completed.")

            self.console.insert(tk.END, "new configuration added\n")
            self.console.insert(tk.END, str(conf) + "\n")
            self.console.see(tk.END)

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
        functions = conf

        lbpcm = LBPCM.LBPCM(picType,
                            radius,
                            stepSize,
                            cellSize,
                            angles,
                            glcmDistance,
                            functions,
                            combineDistances,
                            combineAngles)

        lbpcm.calculateFeatureVectors(self.pathToProcessedData,
                                      self.console,
                                      self.frames[fvcP.FeatureVectorCreationPage].progressbarVector,
                                      self.frames[fvcP.FeatureVectorCreationPage].labelProgress)

        fv = lbpcm.getFeatureVectors()

        # normalizacija vektora
        fv, mean, sigma = util.normalize(fv)
        conf.extend(mean.tolist())
        conf.extend(sigma.tolist())



        X_train = fv[:round(0.7 * fv.__len__())]
        X_test = fv[round(0.7 * fv.__len__()):]

        Y = []
        for i in self.labelDictionary.values():
            Y.append(int(i))

        Y_train = Y[:round(0.7 * fv.__len__())]
        Y_test = Y[round(0.7 * fv.__len__()):fv.__len__()]

        Y_train = Y_train[:100]
        Y_test = Y_test[:100]

        self.console.insert(tk.END, "[INFO] fitting started\n")
        self.console.see(tk.END)

        writer = Writer.Writer()

        if classifierType == 'kNN':
            kneighbors = KNeighborsClassifier(n_neighbors=numOfNeighbors)
            kneighbors.fit(X_train, Y_train)
            error = 1 - kneighbors.score(X_test, Y_test)
            self.consolePrint("[INFO] error: " + str(error))
            conf.append(error)
            writer.saveModel(kneighbors, conf)

        else:
            svm = SVC(gamma='auto')
            svm.fit(X_train, Y_train)
            error = 1 - svm.score(X_test, Y_test)
            self.consolePrint("[INFO] error: " + str(error))
            conf.append(error)
            writer.saveModel(svm, conf)

        # saveString = str(conf) + "--error: " + str(error)
        #
        # self.writer.saveDirectory = r"data/normalData"
        # self.writer.saveResults(saveString)
        # self.writer.saveModel(kneighbors, conf)

        self.consolePrint("[INFO] configuration completed")

    def runConfigurations(self):
        """ Funkcija za pokretanje pojedine unesene konfiguracije
        :return:
        """
        for conf in self.configurations:

            # self.runConf(conf)
            threading.Thread(target=self.runConf, args=(conf,), daemon=True).start()

    def showClassifiedImage(self):

        filename = filedialog.askopenfilename(initialdir=r"data/normalData/View_001",
                                          title="Select picture",
                                          filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))

        conf = self.writer.getConfiguration()

        self.frames[clP.ClassificationPage].labelPictureName.configure(text=filename)
        self.im = ImageTk.PhotoImage(image=Image.fromarray(util.resizePercent(cv.imread(filename), 60)))
        self.frames[clP.ClassificationPage].labelPicture.configure(image=self.im)

        output = util.classifyImage(filename, self.writer.model, conf, self.console)

        self.im = ImageTk.PhotoImage(image=Image.fromarray(output))
        # postavljanje slike u labelu
        self.frames[clP.ClassificationPage].labelPicture.configure(image=self.im)

    def loadModel(self):

        self.writer.loadModel()
        conf = self.writer.getConfiguration()
        self.console.insert(tk.END, "[INFO] configuration loaded\n")
        self.console.insert(tk.END, str(conf) + "\n")
        self.console.see(tk.END)

        # omogucavanje gumba
        self.frames[clP.ClassificationPage].buttonSelectPicture['state'] = "normal"
        self.frames[clP.ClassificationPage].buttonSelectFolder['state'] = "normal"

        # postavljanje parametera modela u frameu
        self.frames[clP.ClassificationPage].labelLBPRadiusValue.configure(text=conf[0])
        self.frames[clP.ClassificationPage].labelGLCMDIstance.configure(text=str(conf[1]))
        self.frames[clP.ClassificationPage].labelStepSize.configure(text=conf[2])
        self.frames[clP.ClassificationPage].labelCellSize.configure(text=str(conf[3]))
        self.frames[clP.ClassificationPage].labelAnglesValue.configure(text=str(util.shortAngles(conf[4])))
        self.frames[clP.ClassificationPage].numberOfNeighborsValue.configure(text=conf[5])
        self.frames[clP.ClassificationPage].labelCombineDistancesValue.configure(text=conf[6])
        self.frames[clP.ClassificationPage].labelCombineAnglesValue.configure(text=conf[7])

    def loadColors(self):

        self.c0c = ImageTk.PhotoImage(image=Image.fromarray(cv.imread("colors/0.jpg")))
        self.c1c = ImageTk.PhotoImage(image=Image.fromarray(cv.imread("colors/1.jpg")))
        self.c2c = ImageTk.PhotoImage(image=Image.fromarray(cv.imread("colors/2.jpg")))
        self.c3c = ImageTk.PhotoImage(image=Image.fromarray(cv.imread("colors/3.jpg")))
        self.c4c = ImageTk.PhotoImage(image=Image.fromarray(cv.imread("colors/4.jpg")))

        self.frames[clP.ClassificationPage].c0c.configure(image=self.c0c)
        self.frames[clP.ClassificationPage].c1c.configure(image=self.c1c)
        self.frames[clP.ClassificationPage].c2c.configure(image=self.c2c)
        self.frames[clP.ClassificationPage].c3c.configure(image=self.c3c)
        self.frames[clP.ClassificationPage].c4c.configure(image=self.c4c)

    def selectGradientPicture(self):
        """
            Funkcija za izbor slike na kojoj se primjenjuje operator gradijenta
        :return:
        """

        filename = filedialog.askopenfilename(
            initialdir=r"data/processedData",
            title="Select picture",
            filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))

        if len(filename) > 0:

            img, sobel, sobelx, sobely = util.gradientImage(filename)
            # postavljanje normalne slike
            self.frames[gP.GradientPage].a.imshow(img, cmap='gray')
            self.frames[gP.GradientPage].canvasa.draw()

            # postavljanje sobel slike
            self.frames[gP.GradientPage].b.imshow(sobel, cmap='gray')
            self.frames[gP.GradientPage].canvasb.draw()

            # postavljanje sobel_x slike
            self.frames[gP.GradientPage].c.imshow(sobelx, cmap='gray')
            self.frames[gP.GradientPage].canvasc.draw()

            # postavljanje sobel_y slike
            self.frames[gP.GradientPage].d.imshow(sobely, cmap='gray')
            self.frames[gP.GradientPage].canvasd.draw()

        else:
            self.console.insert(tk.END, "[WARNING] no image was selected\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)


if __name__ == "__main__":
    app = App()
    # app.geometry("1100x600")
    app.mainloop()
