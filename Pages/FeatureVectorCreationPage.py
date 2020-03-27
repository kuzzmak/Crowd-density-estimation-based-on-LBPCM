import tkinter as tk
from tkinter.ttk import Progressbar
import Pages.ConfigurationsPage as coP
import Pages.InitializationPage as iP

class FeatureVectorCreationPage(tk.Frame):
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
        frameLBPParameters.pack()

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

        progressDescription = tk.Label(frameProgress, text="Progress")
        progressDescription.grid(row=0, padx=10, pady=5)

        # progressbar za broj završenih vektora značajki
        self.progressbarVector = Progressbar(frameProgress, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.progressbarVector.grid(row=1, column=0, padx=10, pady=5)

        self.labelProgress = tk.Label(frameProgress, text="")
        self.labelProgress.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # progressbar za broj završenih konfiguracija
        self.progressbarConf = Progressbar(frameProgress, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.progressbarConf.grid(row=2, column=0, padx=10, pady=5)

        self.labelProgressConf = tk.Label(frameProgress, text="")
        self.labelProgressConf.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # frame s gumbima
        buttonFrame = tk.Frame(self)
        buttonFrame.pack(pady=20, side="bottom")

        buttonAddConfigurations = tk.Button(buttonFrame, text="Add configurations",
                                            command=lambda: controller.show_frame(coP.ConfigurationsPage))
        buttonAddConfigurations.pack(side="left", padx=10, pady=5)

        buttonLoadAnnotedData = tk.Button(buttonFrame, text="Load labels", command=controller.loadLabels)
        buttonLoadAnnotedData.pack(side="left", padx=10, pady=5)

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(side="left", padx=10, pady=5)