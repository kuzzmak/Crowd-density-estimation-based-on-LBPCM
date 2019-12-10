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

# TODO dodati funkciju koja osvjezava na potrebnim mjestima sliku koja se prikazuje u sliding window - da ima onaj
#  crveni kvadrat

# TODO napraviti da se picDims updatea ako se ne izaberu pocetni folderi->ako je kliknuto odmah na preprocess

# boja obruba celije
color = (255, 0, 0)
# debljina crte celije
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

        # staza do slika za treniranje
        self.trainingPath = ""
        # staza do slika za testiranje
        self.testPath = ""
        # radijus LBP-a
        self.radius = 1
        # velicina celije
        self.cellSize = [64, 64]
        # velicina koraka
        self.stepSize = 32
        # trenutna slika na stranici za parametre
        self.currPicPar = [[]]
        # rjecnik svih stranica
        self.frames = {}

        # trenutna slika
        self.currPicPath = ""
        # staza do slika za pretprocesiranje
        self.dataPath = ""
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

        for F in (PreprocessPage, StartPage, PageInitialization, ParameterSetting, SlidingWindow):

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

    def step(self):
        self.frames[PreprocessPage].progressbar.step()

    def nextCell(self):
        """ funkcija za pomicanje na sljedecu celiju u pojedinom slikovnom elementu
        """

        # ako nismo stigli do kraja slikovnog elementa
        if self.currCell < self.picDims.__len__() - 1:
            image = cv.imread(self.currPicPath)
            self.currCell += 1
            self.updateSlidingWindowImage(image)
        else:
            self.console.insert(tk.END, "[WARNING] no more cells remaining\n")
            self.console.insert(tk.END, "----------------------------------------\n")
            self.console.see(tk.END)

    def nextPic(self):
        """funkcija za dohvat sljedece slike"""

        # resetiranje brojaca celije
        self.currCell = 0

        # ako ima jos slikovnih elemenata
        if self.picCounter < len(self.trainPictures):
            self.picCounter += 1
            fileName = self.trainingPath + "/" + self.trainPictures[self.picCounter]
            image = cv.imread(fileName)
            self.updateSlidingWindowImage(image)
            self.currPicPath = fileName
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
            fileName = self.trainingPath + "/" + self.trainPictures[self.picCounter]
            image = cv.imread(fileName)
            # azuriranje slike
            self.updateSlidingWindowImage(image)
            self.currPicPath = fileName
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
        self.console.insert(tk.END, "[INFO] cell has been reset\n")
        self.console.insert(tk.END, "----------------------------------------\n")
        self.console.see(tk.END)

    def process(self):
        # dohvat x, y dimenzija
        x = int(self.frames[PreprocessPage].entryX.get())
        y = int(self.frames[PreprocessPage].entryY.get())
        # dimenzija svakog slikovnog elementa
        dim = (x, y)
        # stvaranje slikovnih elemenata
        self.makePictureElements(self.dataPath, self.trainingPath, self.testPath, *dim)

    def makePictureElements(self, path, pathToTrainingData, pathToTestData, *dim):
        # ako ne postoje folderi za treniranje i testiranje, stovre se, a
        # ako postoje onda se njihov sadrzaj brise
        if os.path.exists(pathToTrainingData):
            util.clearDirectory(pathToTrainingData)
        else:
            self.trainingPath = r"data\trainingData"
            os.mkdir(app.trainingPath)
        if os.path.exists(pathToTestData):
            util.clearDirectory(pathToTestData)
        else:
            self.testPath = r"data\testData"
            os.mkdir(app.testPath)

        # popis svih slika izvorne velicine
        onlyFiles = [f for f in listdir(path) if isfile(join(path, f))]

        # mijesanje slika
        random.shuffle(onlyFiles)
        # spremanje slika za treniranje
        for f in range(round(0.7 * onlyFiles.__len__())):
            fileName = path + "/" + onlyFiles[f]
            # normalna slika
            im = cv.imread(fileName)
            # # slika u sivim tonovima
            im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
            # spremanje slike
            util.saveImage(im_gray, dim, self.trainingPath)
            self.frames[PreprocessPage].progressbar.step()
            self.update()

        # spremanje ostalih slika
        for f in range(round(0.7 * onlyFiles.__len__()), onlyFiles.__len__(), 1):
            fileName = path + "/" + onlyFiles[f]
            im = cv.imread(fileName)
            im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
            util.saveImage(im_gray, dim, self.testPath)
            self.frames[PreprocessPage].progressbar.step()
            self.update()

        self.trainPictures = [f for f in listdir(self.trainingPath)]
        self.frames[PageInitialization].buttonSW['state'] = "normal"

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

    def saveParameters(self, radius, cellSize, stepSize):
        """funkcija za spremanje parametara u razerd"""

        flag = True
        try:
            self.radius = int(radius)
        except ValueError:
            self.console.insert(tk.END, "[ERROR] -- radius must be positive integer\n")
            self.console.see(tk.END)
            flag = False

        # konverzija stringa npr. 64x64 u int [64, 64]
        try:
            self.cellSize = [int(i) for i in cellSize.split("x")]
        except ValueError:
            self.console.insert(tk.END, "[ERROR] -- invalid cellsize configuration\n")
            self.console.see(tk.END)
            flag = False

        try:
            self.stepSize = int(stepSize)
        except ValueError:
            self.console.insert(tk.END, "[ERROR] -- step must be positive integer\n")
            self.console.see(tk.END)
            flag = False

        if flag is True:
            self.console.insert(tk.END, "[INFO] -- parameters saved\n")
            self.console.see(tk.END)

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
        self.frames[PreprocessPage].progressbar.configure(maximum=self.dataPictures.__len__())

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
        self.frames[SlidingWindow].labelPicName.configure(text=self.trainPictures[self.picCounter])
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
            # dohvat prve slike
            self.currPicPath = filename + "/" + self.trainPictures[0]
            image = cv.imread(self.currPicPath)
            # stvaranje koordinata putujuce celije kod tehnike kliznog prozora
            self.picDims = util.makePicDims(image, self.stepSize,
                                           self.cellSize)  # FIXME zamijeniti ovaj kurac sa manualnim unosom dimenzije slike
            self.updateSlidingWindowImage(image)

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

        buttonSelectTraining = tk.Button(buttonFrame, text="Training Folder", command=lambda: controller.selectFolder("train"))
        buttonSelectTraining.pack(padx=5, pady=10, fill="x")

        buttonSelectTest = tk.Button(buttonFrame, text="Test Folder", command=lambda: controller.selectFolder("test"))
        buttonSelectTest.pack(padx=10, pady=10, fill="x")

        buttonParameters = tk.Button(buttonFrame, text="Parameters", command=lambda: controller.show_frame(ParameterSetting))
        buttonParameters.pack(padx=10, pady=10, fill="x")

        self.buttonSW = tk.Button(buttonFrame, text="Sliding Window", state="disabled", command=lambda: controller.show_frame(SlidingWindow))
        self.buttonSW.pack(padx=10, pady=10, fill="x")

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
                                                                                   entryStepSize.get()))
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
        # opis stranice
        description = tk.Label(self, text="Here you can see sliding window method.")
        description.pack()
        # labela za ime slike
        self.labelPicName = tk.Label(self, text="")
        self.labelPicName.pack()
        # labela za sliku
        self.labelPic = tk.Label(self, text="No picture\nloaded")
        self.labelPic.pack()

        # gumbi--------------------------
        buttonFrame = tk.Frame(self)
        buttonFrame.pack(side="bottom", expand=True)

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


class PreprocessPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        labelDescription = tk.Label(self, text="Here you can specify parameters needed for data preprocessing")
        labelDescription.pack(padx=10, pady=10)

        frame1 = tk.Frame(self)
        frame1.pack()

        buttonSelectFolder = tk.Button(frame1, text="Select data folder", command=lambda: [controller.selectDataFolder(),
                                                                                           controller.updatePics()])
        buttonSelectFolder.pack(padx=10, pady=5)

        frame2 = tk.Frame(self)
        frame2.pack()

        labelRatio = tk.Label(frame2, text="training set:test set, eg. \"0.7:0.3\"")
        labelRatio.pack(padx=10, pady=5, side="left")

        entryRatio = tk.Entry(frame2)
        entryRatio.pack(side="right")

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

        # frame s gumbom i progressbar-----------------------------------------
        frame4 = tk.Frame(self)
        frame4.pack()

        buttonProcess = tk.Button(frame4, text="Preprocess", command=controller.process)
        buttonProcess.pack(side="left", padx=10, pady=10)

        self.progressbar = Progressbar(frame4, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progressbar.pack(side="left", padx=10, pady=10)

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(PageInitialization))
        buttonBack.pack(padx=10, pady=10)















if __name__ == "__main__":
    app = App()
    # app.geometry("800x600")
    app.mainloop()
