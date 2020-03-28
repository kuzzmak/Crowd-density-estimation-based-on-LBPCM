import tkinter as tk
from tkinter.ttk import Progressbar
import Pages.InitializationPage as iP

class PreprocessPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        labelDescription = tk.Label(self, text="Here you can specify parameters needed for data preprocessing")
        labelDescription.pack(padx=10, pady=10)

        frame1 = tk.Frame(self)
        frame1.pack()

        buttonSelectFolder = tk.Button(frame1, text="Select data folder")
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

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(padx=10, pady=10)