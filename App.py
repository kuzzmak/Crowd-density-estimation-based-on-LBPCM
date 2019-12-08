import tkinter as tk
from os import listdir
from tkinter import filedialog
import cv2 as cv
import numpy as np
from PIL import ImageTk, Image
import util

color = (255, 0, 0)
thickness = 2


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

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
        # rjecnik svih stranica
        self.frames = {}

        # trenutna slika
        self.currPicPath = r"C:\Users\kuzmi\PycharmProjects\untitled\data\trainingData\0.jpg"
        # pocetna slika
        self.initialImage = cv.imread(self.currPicPath)
        # polje lokacija celije koja se krece po slici
        self.picDims = util.makePicDims(self.initialImage, self.stepSize, self.cellSize)
        # brojac trenutne celije
        self.currCell = 0
        # brojac trenutne slike
        self.picCounter = 0
        # polje imena slika za treniranje
        self.trainPictures = []
        # polje imena slika za testiranje
        self.testPictures = []

        for F in (StartPage, PageOne, PageTwo, PageInitialization, ParameterSetting, SlidingWindow):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def setTrainPath(self, path):
        self.trainingPath = path

    def setTestPath(self, path):
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


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        welcomeText = "This is the starting screen of the app.\nPlease use with caution!"
        label = tk.Label(self, text=welcomeText)
        label.pack(padx=10, pady=10)

        buttonAgree = tk.Button(self, text="Agree", command=lambda: controller.show_frame(PageInitialization))
        buttonAgree.pack()


class PageInitialization(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        description = tk.Label(self, text="Here you select training and testing folder.")
        description.pack(padx=10, pady=10)

        buttonFrame = tk.Frame(self)
        buttonFrame.pack()

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(StartPage))
        buttonBack.pack(padx=10, pady=10, side=tk.LEFT)

        buttonSelectTraining = tk.Button(buttonFrame, text="Training Folder", command=lambda: selectFolder("train"))
        buttonSelectTraining.pack(padx=5, pady=10, side=tk.LEFT)

        buttonSelectTest = tk.Button(buttonFrame, text="Test Folder", command=lambda: selectFolder("test"))
        buttonSelectTest.pack(padx=10, pady=10, side=tk.LEFT)

        buttonParameters = tk.Button(buttonFrame,text="Parameters", command=lambda: controller.show_frame(ParameterSetting))
        buttonParameters.pack(padx=10, pady=10, side=tk.LEFT)

        buttonSW = tk.Button(buttonFrame, text="Sliding Window", command=lambda: controller.show_frame(SlidingWindow))
        buttonSW.pack(padx=10, pady=10, side=tk.LEFT)


class ParameterSetting(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        description = tk.Label(self, text="Here you select parameters required for LBP.")
        description.grid(row=0, columnspan=2)
        # lijevi dio prozora
        leftFrame = tk.Frame(self)
        leftFrame.grid(row=1, column=0)
        # desni dio prozora
        rightFrame = tk.Frame(self, width=400)
        rightFrame.grid(row=1, column=1)

        labelRadius = tk.Label(leftFrame, text="Specify LBP radius:")
        labelRadius.pack()
        # upis radijusa
        entryRadius = tk.Entry(rightFrame, width=15)
        entryRadius.pack(padx=10, pady=5)

        labelCellSize = tk.Label(leftFrame, text="Specify cell size, eg. \"64x64\".")
        labelCellSize.pack()
        # upis velicine celije za klizni prozor
        entryCellSize = tk.Entry(rightFrame, width=15)
        entryCellSize.pack(padx=10, pady=5)

        labelStepSize = tk.Label(leftFrame, text="Specify step size:")
        labelStepSize.pack()
        # upis velicine koraka
        entryStepSize = tk.Entry(rightFrame, width=15)
        entryStepSize.pack(padx=10, pady=5)
        # gumb za spremanje parametara LBP-a
        buttonSave = tk.Button(self, text="Save", command=lambda: saveParameters(entryRadius.get(),
                                                                                 entryCellSize.get(),
                                                                                 entryStepSize.get()))
        buttonSave.grid(row=2, column=0)

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(PageInitialization))
        buttonBack.grid(row=2, column=1)


class SlidingWindow(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        description = tk.Label(self, text="Here you can see sliding window method.")
        description.pack()

        self.labelPicName = tk.Label(self, text="")
        self.labelPicName.pack()

        self.labelPic = tk.Label(self, text="No picture\nloaded")
        self.labelPic.pack()

        buttonFrame = tk.Frame(self)
        buttonFrame.pack(side="bottom", expand=True)

        buttonNextPicture = tk.Button(buttonFrame, text="Next pic", command=nextPic)
        buttonNextPicture.grid(row=0, column=0, padx=5, pady=5)

        buttonPreviousPicture = tk.Button(buttonFrame, text="Prev pic")
        buttonPreviousPicture.grid(row=0, column=1, padx=5, pady=5)

        buttonNextCell = tk.Button(buttonFrame, text="Next cell", command=nextCell)
        buttonNextCell.grid(row=0, column=2, padx=5, pady=5)

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(PageInitialization))
        buttonBack.grid(row=0, column=4, padx=5, pady=5)


def saveParameters(radius, cellSize, stepSize):

    """funkcija za spremanje parametara u razerd"""

    flag = True
    try:
        app.radius = int(radius)
    except ValueError:
        app.console.insert(tk.END, "[ERROR] -- radius must be positive integer\n")
        flag = False
    # konverzija stringa npr. 64x64 u int [64, 64]
    try:
        app.cellSize = [int(i) for i in cellSize.split("x")]
    except ValueError:
        app.console.insert(tk.END, "[ERROR] -- invalid cellsize configuration\n")
        flag = False

    try:
        app.stepSize = int(stepSize)
    except ValueError:
        app.console.insert(tk.END, "[ERROR] -- step must be positive integer\n")
        flag = False

    if flag is True:
        app.console.insert(tk.END, "[INFO] -- parameters saved\n")
    app.console.insert(tk.END, "----------------------------------------\n")


class PageOne(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page one")
        label.pack(padx=10, pady=10)

        button1 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page 2", command=lambda: controller.show_frame(PageTwo))
        button2.pack()


def selectFolder(testOrTrain):
    filename = filedialog.askdirectory()
    if testOrTrain == "train":
        app.setTrainPath(filename)
        app.trainPictures = [f for f in listdir(app.trainingPath)]
        app.console.insert(tk.END, "[INFO] training path set: " + filename + "\n")
        app.console.insert(tk.END, "[INFO] loaded " + str(app.trainPictures.__len__()) + " training pictures\n")
        app.console.insert(tk.END, "----------------------------------------\n")
    else:
        app.setTestPath(filename)
        app.testPictures = [f for f in listdir(app.testPath)]
        app.console.insert(tk.END, "[INFO] test path set: " + filename + "\n")
        app.console.insert(tk.END, "[INFO] loaded " + str(app.testPictures.__len__()) + " test pictures\n")
        app.console.insert(tk.END, "----------------------------------------\n")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page two")
        label.pack(padx=10, pady=10)

        button2 = tk.Button(self, text="Start Page", command=lambda: controller.show_frame(StartPage))
        button2.pack()

        button1 = tk.Button(self, text="Page 1", command=lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = tk.Button(self, text="Select train folder", command=lambda: selectFolder("train"))
        button2.pack()


if __name__ == "__main__":
    app = App()
    # app.geometry("640x320")
    app.mainloop()
