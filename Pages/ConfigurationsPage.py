import tkinter as tk
import FunctionDescriptions
import Pages.FeatureVectorCreationPage as fvcP

class ConfigurationsPage(tk.Frame):
    """ razred za ucenje klasifikatora, nakon stvorenih vektora znacajki i oznacenih slika
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        # opis framea
        descriptionLabel = tk.Label(self, text="Here you specify different configurations for running.\n")
        descriptionLabel.grid(row=0, padx=10, pady=10, columnspan=2)

        # frame s parametrima svake konfiguracije
        parameterFrame = tk.Frame(self)
        parameterFrame.grid(row=1, column=0, padx=10, pady=5)

        # frame s odabirom funkcija koje se koriste kod kreiranja vektora značajki
        functionsFrame = tk.Frame(self)
        functionsFrame.grid(row=1, column=1, padx=20, pady=5)

        # odabir vrste slike nad kojim se primjenjuje LBP
        picTypeDescription = tk.Label(parameterFrame, text="Select picture type")
        picTypeDescription.pack(padx=10, pady=10)

        picTypeFrame = tk.Frame(parameterFrame)
        picTypeFrame.pack()

        functionsDescription = tk.Label(functionsFrame,
                                        text="Please select which functions\n to use in feature vector creation.")
        functionsDescription.grid(row=0, padx=10, pady=10, sticky="w")

        # stvaranje checkbox gumba
        i = 1
        for name, fName, c in controller.functionButtons:
            tk.Checkbutton(functionsFrame, text=name + " - " + fName, variable=c).grid(row=i, pady="2", sticky="w")
            i += 1

        functionDefinitions = tk.Button(functionsFrame, text="Function definitions",
                                        command=lambda: FunctionDescriptions.FD(self))
        functionDefinitions.grid(row=i, pady=2, sticky="we")

        # predpostavljena vrijednost varijable za odabir vrste slike na kojoj se prmjenjuje LBP
        controller.rType.set(0)

        rGray = tk.Radiobutton(picTypeFrame, text="Gray", variable=controller.rType, value=0)
        rGray.pack(side="left", padx=20, pady=5)

        rGradient = tk.Radiobutton(picTypeFrame, text="Gradient", variable=controller.rType, value=1)
        rGradient.pack(side="right", padx=20, pady=5)

        # LBP parametri
        labelLBP = tk.Label(parameterFrame, text="LBP parameters")
        labelLBP.pack(padx=10, pady=10)

        frameLBP = tk.Frame(parameterFrame)
        frameLBP.pack()

        labelLBPRadius = tk.Label(frameLBP, text="LBP radius")
        labelLBPRadius.pack(side="left", padx=10, pady=10)

        self.entryLBPRadius = tk.Entry(frameLBP)
        self.entryLBPRadius.pack(side="right", padx=10, pady=10)

        # frame s glcm parametrima
        labelGLCM = tk.Label(parameterFrame, text="GLCM parameters")
        labelGLCM.pack()

        frameGLCM = tk.Frame(parameterFrame)
        frameGLCM.pack()

        labelGLCMDistance = tk.Label(frameGLCM, text="Distance")
        labelGLCMDistance.grid(row=0, column=0, padx=10, pady=10)

        self.entryGLCMDistance = tk.Entry(frameGLCM)
        self.entryGLCMDistance.grid(row=0, column=1, padx=10, pady=10)

        labelStepSize = tk.Label(frameGLCM, text="Step size")
        labelStepSize.grid(row=1, column=0, padx=10, pady=10)

        self.entryStepSize = tk.Entry(frameGLCM)
        self.entryStepSize.grid(row=1, column=1, padx=10, pady=10)

        labelCellSize = tk.Label(frameGLCM, text="Cell size")
        labelCellSize.grid(row=2, column=0, padx=10, pady=10)

        self.entryCellSize = tk.Entry(frameGLCM)
        self.entryCellSize.grid(row=2, column=1, padx=10, pady=10)

        labelAngles = tk.Label(frameGLCM, text="Angles")
        labelAngles.grid(row=3, column=0, padx=10, pady=10)

        self.entryAngles = tk.Entry(frameGLCM)
        self.entryAngles.grid(row=3, column=1, padx=10, pady=10)

        # parametri za klasifikator
        labelClassifier = tk.Label(parameterFrame, text="Classifier parameters")
        labelClassifier.pack()

        classifierFrame = tk.Frame(parameterFrame)
        classifierFrame.pack()

        labelNumOfNeighbors = tk.Label(classifierFrame, text="Number of neighbors")
        labelNumOfNeighbors.grid(row=0, column=0, padx=10, pady=10)

        self.entryNumOfNeighbors = tk.Entry(classifierFrame)
        self.entryNumOfNeighbors.grid(row=0, column=1, padx=10, pady=10)

        labelCombineDistances = tk.Label(classifierFrame, text="Combine multiple distances")
        labelCombineDistances.grid(row=1, column=0, padx=10, pady=10)

        options = [(0, "Don't combine"),
                   (1, "Combine")]

        controller.rbDistances.set(0)

        frameRB1 = tk.Frame(classifierFrame)
        frameRB1.grid(row=1, column=1, padx=10)
        for val, name in enumerate(options):
            tk.Radiobutton(frameRB1, text=name, padx=10, pady=10,
                           variable=controller.rbDistances, value=val).pack(side="left")

        labelCombineAngles = tk.Label(classifierFrame, text="Combine multiple angles")
        labelCombineAngles.grid(row=2, column=0, padx=10, pady=10)

        controller.rbAngles.set(0)

        frameRB2 = tk.Frame(classifierFrame)
        frameRB2.grid(row=2, column=1, padx=10)

        for val, name in enumerate(options):
            tk.Radiobutton(frameRB2, text=name, padx=10, pady=10,
                           variable=controller.rbAngles, value=val).pack(side="left")

        # frame s gumbima
        buttonFrame = tk.Frame(self)
        buttonFrame.grid(row=2, padx=10, pady=5, columnspan=2)

        buttonAdd = tk.Button(buttonFrame, text="Add", command=lambda: controller.addConf())
        buttonAdd.pack(side="left", padx=10, pady=10)

        buttonRunConfigurations = tk.Button(buttonFrame, text="Run configurations",
                                            command=lambda: controller.runConfigurations())
        buttonRunConfigurations.pack(side="left", padx=10, pady=10)

        buttonBack = tk.Button(buttonFrame, text="Back",
                               command=lambda: controller.show_frame(fvcP.FeatureVectorCreationPage))
        buttonBack.pack(side="left", padx=10, pady=10)

        self.entryLBPRadius.insert(tk.END, "1")
        self.entryGLCMDistance.insert(tk.END, "1,2")
        self.entryStepSize.insert(tk.END, "32")
        self.entryCellSize.insert(tk.END, "64,64")
        self.entryAngles.insert(tk.END, "0,45,90")
        self.entryNumOfNeighbors.insert(tk.END, "1")