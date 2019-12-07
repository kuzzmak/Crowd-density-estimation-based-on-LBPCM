import tkinter as tk
from tkinter import filedialog


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.trainingPath = ""
        self.testPath = ""

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageInitialization, ParameterSetting):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def setTrainPath(self, path):
        self.trainingPath = path

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
        description = tk.Label(self, text="Here you select parameters required for LBP.")
        description.grid(row=0)
        # lijevi dio prozora
        leftFrame = tk.Frame(self)
        leftFrame.grid(row=1, column=0)
        # desni dio prozora
        rightFrame = tk.Frame(self)
        rightFrame.grid(row=1, column=1)

        labelRadius = tk.Label(leftFrame, text="Specify LBP radius:")
        labelRadius.pack()
        # upis radijusa
        entryRadius = tk.Entry(rightFrame, width=15)
        entryRadius.pack()


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
    else:
        app.setTestPath(filename)
    # errorLabel.configure(text="Folder selected: " + filename)

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
    app.mainloop()