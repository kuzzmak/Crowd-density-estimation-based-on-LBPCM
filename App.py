import tkinter as tk
from os import listdir
from tkinter import filedialog
import cv2 as cv
import numpy as np
from PIL import ImageTk, Image
import util
from skimage.feature import local_binary_pattern
from tkinter.ttk import Progressbar

# boja obruba celije
color = (255, 0, 0)
# debljina crte celije
thickness = 2


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


def nextCell():
    """funkcija za pomicanje na sljedecu celiju u pojedinom slikovnom elementu"""
    # ako nismo stigli do kraja slikovnog elementa
    if app.currCell < app.picDims.__len__():
        image = cv.imread(app.currPicPath)
        # dohvat pocetne i krajnje tocke pojedine celije
        start_point, end_point = app.picDims[app.currCell]
        app.currCell += 1
        # kopija slike kako celija ne bi ostala na slici nakon svake iteracije
        image_copy = cv.rectangle(np.copy(image), start_point, end_point, color, thickness)
        # stvaranje slike iz numpy arraya
        app.img = ImageTk.PhotoImage(image=Image.fromarray(image_copy))
        # postavljanje slike u labelu
        app.frames[SlidingWindow].labelPic.configure(image=app.img)
        app.frames[SlidingWindow].labelPicName.configure(text=app.trainPictures[app.picCounter])
    else:
        app.console.insert(tk.END, "[WARNING] no more cells remaining\n")
        app.console.insert(tk.END, "----------------------------------------\n")
        app.console.see(tk.END)

def nextPic():
    """funkcija za dohvat sljedece slike"""

    # ako ima jos slikovnih elemenata
    if app.picCounter < len(app.trainPictures):
        print(app.picCounter)
        app.picCounter += 1
        fileName = app.trainingPath + "/" + app.trainPictures[app.picCounter]
        image = cv.imread(fileName)
        app.photo = ImageTk.PhotoImage(image=Image.fromarray(image))
        app.frames[SlidingWindow].labelPic.configure(image=app.photo)
        app.frames[SlidingWindow].labelPicName.configure(text=app.trainPictures[app.picCounter])
        app.currPicPath = fileName
        # resetiranje brojaca celije
        app.currCell = 0
    else:
        app.console.insert(tk.END, "[WARNING] no more pictures remaining\n")
        app.console.insert(tk.END, "----------------------------------------\n")
        app.console.see(tk.END)


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

        buttonPreprocess = tk.Button(buttonFrame, text="Preprocess data", command=lambda: controller.show_frame(PreprocessPage))
        buttonPreprocess.pack(padx=5, pady=10, fill="x")
        #TODO dodati da se ovo ispod napravi nakon klika na gumb preprocess data
        # app.console.insert(tk.END, "[WARNING] data path not set yet\n")
        # app.console.insert(tk.END, "----------------------------------------\n")
        # app.console.see(tk.END)

        buttonSelectTraining = tk.Button(buttonFrame, text="Training Folder", command=lambda: selectFolder("train"))
        buttonSelectTraining.pack(padx=5, pady=10, fill="x")

        buttonSelectTest = tk.Button(buttonFrame, text="Test Folder", command=lambda: selectFolder("test"))
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
        buttonSave = tk.Button(frame5, text="Save", command=lambda: saveParameters(entryRadius.get(),
                                                                                   entryCellSize.get(),
                                                                                   entryStepSize.get()))
        buttonSave.pack(padx=10, pady=5, side="left")

        buttonSelectPic = tk.Button(frame5, text="Select img", command=selectImg)
        buttonSelectPic.pack(padx=10, pady=5, side="left")

        self.buttonRefresh = tk.Button(frame5, text="Refresh", state="disabled", command=refreshLBP)
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

        buttonNextPicture = tk.Button(buttonFrame, text="Next pic", command=nextPic)
        buttonNextPicture.grid(row=0, column=1, padx=5, pady=5)

        buttonPreviousPicture = tk.Button(buttonFrame, text="Prev pic")
        buttonPreviousPicture.grid(row=0, column=0, padx=5, pady=5)

        buttonNextCell = tk.Button(buttonFrame, text="Next cell", command=nextCell)
        buttonNextCell.grid(row=0, column=2, padx=5, pady=5)

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(PageInitialization))
        #FIXME dodati mogucnost resetiranja slike na pcetak prilikom klika nazad

        buttonBack.grid(row=0, column=4, padx=5, pady=5)


class PreprocessPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        labelDescription = tk.Label(self, text="Here you can specify parameters needed for data preprocessing")
        labelDescription.pack(padx=10, pady=10)

        frame1 = tk.Frame(self)
        frame1.pack()

        buttonSelectFolder = tk.Button(frame1, text="Select data folder", command=lambda: [selectDataFolder(), updatePics()])
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

        buttonProcess = tk.Button(frame4, text="Preprocess", command=process)
        buttonProcess.pack(side="left", padx=10, pady=10)

        self.progressbar = Progressbar(frame4, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progressbar.pack(side="left", padx=10, pady=10)

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(PageInitialization))
        buttonBack.pack(padx=10, pady=10)


def process():
    # dohvat x, y dimenzija
    x = int(app.frames[PreprocessPage].entryX.get())
    y = int(app.frames[PreprocessPage].entryY.get())
    # dimenzija svakog slikovnog elementa
    dim = (x, y)
    # stvaranje slikovnih elemenata
    util.makePictureElements(app.dataPath, app.trainingPath, app.testPath, *dim)
    app.frames[PreprocessPage].progressbar.step()

def selectImg():
    """ funkcija za dohvat i prikaz odabrane slike na stranici parametersetting
        i dodatno izracun LBP-a
    """

    try:
        # staza do odabrane slike preko izbornika
        path = filedialog.askopenfilename(initialdir=r"C:\Users\kuzmi\PycharmProjects\untitled", title="Select file",
                                          filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        # pamcenje slike radi moguconsti refresha prilikom promjene parametra
        app.currPicPar = cv.imread(path, cv.IMREAD_GRAYSCALE)
        # omogucavanje gumba refresh
        app.frames[ParameterSetting].buttonRefresh.config(state="normal")
        app.im = ImageTk.PhotoImage(image=Image.fromarray(app.currPicPar))
        # postavaljanje slike u frame parametersetting
        app.frames[ParameterSetting].labelNormalPic.configure(image=app.im)
        # postavljanje imena ucitane slike
        app.frames[ParameterSetting].labelImageName.configure(text="image: " + path.split("/")[-1])
        # izracun LBP-a
        lbp = local_binary_pattern(app.currPicPar, app.radius * 8, app.radius)

        app.lbp = ImageTk.PhotoImage(image=Image.fromarray(lbp))
        # postavljanje lbp u labelu
        app.frames[ParameterSetting].labelLBPPic.configure(image=app.lbp)

    except AttributeError:
        pass

def refreshLBP():
    """ funkcija za refresh LBP-a ako su se promjenili parametri na stranici parametersetting
    """

    # ponovni izracun LBP-a
    lbp = local_binary_pattern(app.currPicPar, app.radius * 8, app.radius)
    # konstrukcija slike iz polja
    app.lbp = ImageTk.PhotoImage(image=Image.fromarray(lbp))
    # prikaz slike u odgovarajucoj labeli
    app.frames[ParameterSetting].labelLBPPic.configure(image=app.lbp)

def saveParameters(radius, cellSize, stepSize):
    """funkcija za spremanje parametara u razerd"""

    flag = True
    try:
        app.radius = int(radius)
    except ValueError:
        app.console.insert(tk.END, "[ERROR] -- radius must be positive integer\n")
        app.console.see(tk.END)
        flag = False

    # konverzija stringa npr. 64x64 u int [64, 64]
    try:
        app.cellSize = [int(i) for i in cellSize.split("x")]
    except ValueError:
        app.console.insert(tk.END, "[ERROR] -- invalid cellsize configuration\n")
        app.console.see(tk.END)
        flag = False

    try:
        app.stepSize = int(stepSize)
    except ValueError:
        app.console.insert(tk.END, "[ERROR] -- step must be positive integer\n")
        app.console.see(tk.END)
        flag = False

    if flag is True:
        app.console.insert(tk.END, "[INFO] -- parameters saved\n")
        app.console.see(tk.END)

    app.console.insert(tk.END, "----------------------------------------\n")
    app.console.see(tk.END)

def selectDataFolder():
    """ funkcija za odabir foldera koji se koristi za preprocesiranje
    """
    directory = filedialog.askdirectory()

    if directory != "":
        app.dataPath = directory
        app.console.insert(tk.END, "[INFO] data folder set: " + directory + "\n")
        app.console.insert(tk.END, "----------------------------------------\n")
        app.console.see(tk.END)
    else:
        app.console.insert(tk.END, "[WARNING] you did not select folder\n")
        app.console.insert(tk.END, "----------------------------------------\n")
        app.console.see(tk.END)

def updatePics():
    app.dataPictures = [f for f in listdir(app.dataPath)]
    app.frames[PreprocessPage].progressbar.configure(maximum=app.dataPictures.__len__())

def selectFolder(testOrTrain):
    """ funkcija za odabir folera za treniranje ili testiranje
    """

    # odabran put
    filename = filedialog.askdirectory()
    if testOrTrain == "train":
        # staza za treniranje
        app.setTrainPath(filename)
        # stvaranje polja slika za treniranje
        app.trainPictures = [f for f in listdir(app.trainingPath)]
        # dohvat prve slike
        app.currPicPath = filename + "/" + app.trainPictures[0]
        image = cv.imread(app.currPicPath)
        # trenutno pamcenje da se ne ukloni iz memorije
        app.im = ImageTk.PhotoImage(image=Image.fromarray(image))
        # postavaljanje imena slike u odgovarajucu labelu
        app.frames[SlidingWindow].labelPicName.configure(text=app.trainPictures[0])
        # postavljanje slike
        app.frames[SlidingWindow].labelPic.configure(image=app.im)
        # stvaranje koordinata putujuce celije kod tehnike kliznog prozora
        app.picDims = util.makePicDims(image, app.stepSize, app.cellSize)  #FIXME zamijeniti ovaj kurac sa manualnim unosom dimenzije slike
        # omogucavanje gumba sliding window
        app.frames[PageInitialization].buttonSW.config(state="normal")

        app.console.insert(tk.END, "[INFO] training path set: " + filename + "\n")
        app.console.insert(tk.END, "[INFO] loaded " + str(app.trainPictures.__len__()) + " training pictures\n")
        app.console.insert(tk.END, "----------------------------------------\n")
        app.console.see(tk.END)
    else:
        app.setTestPath(filename)
        app.testPictures = [f for f in listdir(app.testPath)]
        app.console.insert(tk.END, "[INFO] test path set: " + filename + "\n")
        app.console.insert(tk.END, "[INFO] loaded " + str(app.testPictures.__len__()) + " test pictures\n")
        app.console.insert(tk.END, "----------------------------------------\n")
        app.console.see(tk.END)


if __name__ == "__main__":
    app = App()
    # app.geometry("800x600")
    app.mainloop()
