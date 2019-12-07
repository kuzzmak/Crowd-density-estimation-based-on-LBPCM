import tkinter as tk
from tkinter import filedialog


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # konzola
        self.console = tk.Text(self, height=2, width=30)
        self.console.pack(side="bottom", fill="both", expand=True)
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

        for F in (StartPage, PageOne, PageTwo, PageInitialization, ParameterSetting):

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

def printTrainingPath():
    print(app.trainingPath)

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
        description.grid(row=0)


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
        app.console.insert(tk.END, "[INFO] training path set: " + filename + "\n")
        app.console.insert(tk.END, "----------------------------------------\n")
    else:
        app.setTestPath(filename)
        app.console.insert(tk.END, "[INFO] test path set: " + filename + "\n")
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
