import tkinter as tk
import threading
import Pages.InitializationPage as iP

class ClassificationPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        pageDescription = tk.Label(self, text="Here you can classify images.")
        pageDescription.pack(side="top", padx=10, pady=10)

        leftFrame = tk.Frame(self)
        leftFrame.pack(side="left", padx=10, pady=10)

        rightFrame = tk.Frame(self)
        rightFrame.pack(side="left", padx=10, pady=10, fill=tk.BOTH, expand=True)

        # frame s bojama
        colorFrame = tk.Frame(leftFrame)
        colorFrame.pack(padx=10, pady=10)

        # row0 = tk.Frame(colorFrame)
        # row0.pack()

        self.c0c = tk.Label(colorFrame, text="")
        self.c0c.grid(row=0, column=0, padx=10, pady=5)

        c0 = tk.Label(colorFrame, text="no flow")
        c0.grid(row=0, column=1, padx=10, pady=5)

        # row1 = tk.Frame(colorFrame)
        # row1.pack()

        self.c1c = tk.Label(colorFrame, text="")
        self.c1c.grid(row=1, column=0, padx=10, pady=5)

        c1 = tk.Label(colorFrame, text="free flow")
        c1.grid(row=1, column=1, padx=10, pady=5)

        # row2 = tk.Label(colorFrame)
        # row2.pack()

        self.c2c = tk.Label(colorFrame, text="")
        self.c2c.grid(row=2, column=0, padx=10, pady=5)

        c2 = tk.Label(colorFrame, text="restricted flow")
        c2.grid(row=2, column=1, padx=10, pady=5)

        # row3 = tk.Label(colorFrame)
        # row3.pack()

        self.c3c = tk.Label(colorFrame, text="")
        self.c3c.grid(row=3, column=0, padx=10, pady=5)

        c3 = tk.Label(colorFrame, text="dense flow")
        c3.grid(row=3, column=1, padx=10, pady=5)

        # row4 = tk.Frame(colorFrame)
        # row4.pack()

        self.c4c = tk.Label(colorFrame, text="")
        self.c4c.grid(row=4, column=0, padx=10, pady=5)

        c4 = tk.Label(colorFrame, text="jammed flow")
        c4.grid(row=4, column=1, padx=10, pady=5)

        # gumbi
        buttonLoadModel = tk.Button(leftFrame, text="Load model", command=lambda: controller.loadModel())
        buttonLoadModel.pack(padx=10, pady=5, fill="x")

        self.buttonSelectFolder = tk.Button(leftFrame, text="Select folder", state="disabled")
        self.buttonSelectFolder.pack(padx=10, pady=5, fill="x")

        self.buttonSelectPicture = tk.Button(leftFrame, text="Select picture", state="disabled",
                                        command=lambda: threading.Thread(
                                            target=controller.showClassifiedImage, daemon=True).start())
        self.buttonSelectPicture.pack(padx=10, pady=5, fill="x")

        buttonBack = tk.Button(leftFrame, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(padx=10, pady=5, fill="x")

        self.labelPictureName = tk.Label(rightFrame, text="Select picture first")
        self.labelPictureName.pack(pady=10)

        self.labelPicture = tk.Label(rightFrame, text="Select picture or select folder")
        self.labelPicture.pack(pady=10)

        # frame s parametrima ucitanog modela
        parameterFrame = tk.Frame(self)
        parameterFrame.pack(side="left", padx=10, pady=10, fill=tk.BOTH)

        labelLBPRadius = tk.Label(parameterFrame, text="LBP radius:")
        labelLBPRadius.grid(row=0, column=0, padx=10, pady=10)

        self.labelLBPRadiusValue = tk.Label(parameterFrame, text="")
        self.labelLBPRadiusValue.grid(row=0, column=1, padx=10, pady=10)

        labelGLCMDistance = tk.Label(parameterFrame, text="GLCM disance:")
        labelGLCMDistance.grid(row=1, column=0, padx=10, pady=10)

        self.labelGLCMDIstance = tk.Label(parameterFrame, text="")
        self.labelGLCMDIstance.grid(row=1, column=1, padx=10, pady=10)

        labelStepSize = tk.Label(parameterFrame, text="Step size:")
        labelStepSize.grid(row=2, column=0, padx=10, pady=10)

        self.labelStepSize = tk.Label(parameterFrame, text="")
        self.labelStepSize.grid(row=2, column=1, padx=10, pady=10)

        labelCellSize = tk.Label(parameterFrame, text="Cell size")
        labelCellSize.grid(row=3, column=0, padx=10, pady=10)

        self.labelCellSize = tk.Label(parameterFrame, text="")
        self.labelCellSize.grid(row=3, column=1, padx=10, pady=10)

        labelAngles = tk.Label(parameterFrame, text="Angles(in rad):")
        labelAngles.grid(row=4, column=0, padx=10, pady=10)

        self.labelAnglesValue = tk.Label(parameterFrame, text="")
        self.labelAnglesValue.grid(row=4, column=1, padx=10, pady=10)

        labelNumberOfNeighbors = tk.Label(parameterFrame, text="No. of neighbors:")
        labelNumberOfNeighbors.grid(row=5, column=0, padx=10, pady=10)

        self.numberOfNeighborsValue = tk.Label(parameterFrame, text="")
        self.numberOfNeighborsValue.grid(row=5, column=1, padx=10, pady=10)

        labelCombineDistances = tk.Label(parameterFrame, text="Cobine distances:")
        labelCombineDistances.grid(row=6, column=0, padx=10, pady=10)

        self.labelCombineDistancesValue = tk.Label(parameterFrame, text="")
        self.labelCombineDistancesValue.grid(row=6, column=1, padx=10, pady=10)

        labelCombineAngles = tk.Label(parameterFrame, text="Combine angles")
        labelCombineAngles.grid(row=7, column=0, padx=10, pady=10)

        self.labelCombineAnglesValue = tk.Label(parameterFrame, text="")
        self.labelCombineAnglesValue.grid(row=7, column=1, padx=10, pady=10)