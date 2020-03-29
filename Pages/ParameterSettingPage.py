import tkinter as tk
import Pages.InitializationPage as iP

class ParameterSettingPage(tk.Frame):
    """ razred gdje se odabiru parametri LBP-a
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        description = tk.Label(self, text="Here you select parameters required for normal app functioning.")
        description.pack(pady=5)

        parameterFrame = tk.Frame(self)
        parameterFrame.pack()

        leftFrame = tk.Frame(parameterFrame)
        leftFrame.pack(side="left", padx=10, pady=10)

        rightFrame = tk.Frame(parameterFrame)
        rightFrame.pack(side="left", padx=10, pady=10)

        dataPathLabel = tk.Label(leftFrame, text="data path:")
        dataPathLabel.grid(pady=10, row=0, sticky="e")

        dataPathButton = tk.Button(rightFrame, text="Select folder")
        dataPathButton.grid(pady=5, row=0, sticky="e")

        normalDataPath = tk.Label(leftFrame, text="unprocessed data path:")
        normalDataPath.grid(pady=10, row=1, sticky="e")

        normalDataPathButton = tk.Button(rightFrame, text="Select folder")
        normalDataPathButton.grid(pady=5, row=1, sticky="w")

        processedDataPathLabel = tk.Label(leftFrame, text="processed data:")
        processedDataPathLabel.grid(pady=10, row=2, sticky="e")

        processedDataPathButton = tk.Button(rightFrame, text="Select folder")
        processedDataPathButton.grid(pady=5, row=2, sticky="w")

        labeledDataDirectory = tk.Label(leftFrame, text="label directory path:")
        labeledDataDirectory.grid(pady=10, row=3, sticky="e")

        labeledDataDirectoryButton = tk.Button(rightFrame, text="Select folder")
        labeledDataDirectoryButton.grid(pady=5, row=3, sticky="w")

        grayModelsPath = tk.Label(leftFrame, text="gray models path:")
        grayModelsPath.grid(pady=10, row=4, sticky="e")

        grayModelsPathButton = tk.Button(rightFrame, text="Select folder")
        grayModelsPathButton.grid(pady=5, row=4, sticky="w")

        gradModelsPath = tk.Label(leftFrame, text="gradient models path:")
        gradModelsPath.grid(pady=10, row=5, sticky="e")

        gradModelsPathButton = tk.Button(rightFrame, text="Select folder")
        gradModelsPathButton.grid(pady=5, row=5, sticky="w")


        # panel sa trenutnom konfiguracijom
        currentConfigurationFrame = tk.Frame(self)
        currentConfigurationFrame.pack()

        currentConfigurationDescription = tk.Label(currentConfigurationFrame, text="Current configuration")
        currentConfigurationDescription.pack(pady=10)

        leftValuesFrame = tk.Frame(currentConfigurationFrame)
        leftValuesFrame.pack(side="left")

        rightValuesFrame = tk.Frame(currentConfigurationFrame)
        rightValuesFrame.pack(side="left")

        labelCurrentDataPath = tk.Label(leftValuesFrame, text="data path: ")
        labelCurrentDataPath.grid(row=0, pady=3, sticky="e")

        labelCurrentDataPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['dataPath'])
        labelCurrentDataPathValue.grid(row=0, pady=3, sticky="w")

        labelCurrentNormalDataPath = tk.Label(leftValuesFrame, text="unprocessed data path: ")
        labelCurrentNormalDataPath.grid(row=1, pady=3, sticky="e")

        labelCurrentNormalDataPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['unprocessedDataPath'])
        labelCurrentNormalDataPathValue.grid(row=1, pady=3, sticky="w")

        labelProcessedDataPath = tk.Label(leftValuesFrame, text="processed data path: ")
        labelProcessedDataPath.grid(row=2, pady=3, sticky="e")

        labelProcessedDataPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['processedImagesPath'])
        labelProcessedDataPathValue.grid(row=2, pady=3, sticky="w")

        labelLabelDirectoryPath = tk.Label(leftValuesFrame, text="label data directory: ")
        labelLabelDirectoryPath.grid(row=3, pady=3, sticky="e")

        labelLabelDirectoryPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['labeledDataDirectory'])
        labelLabelDirectoryPathValue.grid(row=3, pady=3, sticky="w")

        labelGrayModelsPath = tk.Label(leftValuesFrame, text="gray models path: ")
        labelGrayModelsPath.grid(row=4, pady=3, sticky="e")

        labelGrayModelsPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['grayModelsPath'])
        labelGrayModelsPathValue.grid(row=4, pady=3, sticky="w")

        labelGradModelsPath = tk.Label(leftValuesFrame, text="grad models path: ")
        labelGradModelsPath.grid(row=5, pady=3, sticky="e")

        labelGradModelsPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['gradModelsPath'])
        labelGradModelsPathValue.grid(row=5, pady=3, sticky="w")






        # # prvi redak---------------------------
        # frame1 = tk.Frame(self)
        # frame1.pack(pady=5)
        #
        # labelRadius = tk.Label(frame1, text="Specify LBP radius:")
        # labelRadius.pack(side="left")
        # # upis radijusa
        # entryRadius = tk.Entry(frame1)
        # entryRadius.pack(side="right")
        #
        # # drugi redak--------------------------
        # frame2 = tk.Frame(self)
        # frame2.pack()
        #
        # labelCellSize = tk.Label(frame2, text="Specify cell size, eg. \"64x64\".")
        # labelCellSize.pack(side="left")
        # # upis velicine celije za klizni prozor
        # entryCellSize = tk.Entry(frame2)
        # entryCellSize.pack(side="right")
        #
        # # treci redak--------------------------
        # frame3 = tk.Frame(self)
        # frame3.pack(pady=5)
        #
        # labelStepSize = tk.Label(frame3, text="Specify step size:")
        # labelStepSize.pack(side="left")
        # # upis velicine koraka
        # entryStepSize = tk.Entry(frame3)
        # entryStepSize.pack(side="right")
        #
        # frame31 = tk.Frame(self)
        # frame31.pack()
        #
        # labelAngles = tk.Label(frame31,
        #                        text="Specify angles(in degrees) for which you'd like to \ncalculate co-occurence matrix(separate them by comma, eg. 45,90,135): ")
        # labelAngles.pack(side="left")
        #
        # entryAngles = tk.Entry(frame31)
        # entryAngles.pack(side="right")
        #
        # labelRepresentation = tk.Label(self, text="Loaded image on the left and LBP on the right")
        # labelRepresentation.pack()
        #
        # self.labelImageName = tk.Label(self, text="")
        # self.labelImageName.pack()
        #
        # # cetvrti redak---------------------------
        # frame4 = tk.Frame(self)
        # frame4.pack(padx=10, pady=5)
        #
        # self.labelNormalPic = tk.Label(frame4, text="no pic\nselected")
        # self.labelNormalPic.grid(row=0, column=0, padx=10, pady=10)
        #
        # self.labelLBPPic = tk.Label(frame4, text="select pic\nfirst")
        # self.labelLBPPic.grid(row=0, column=1, padx=10, pady=10)
        #
        # # peti redak------------------------
        # frame5 = tk.Frame(self)
        # frame5.pack(pady=5)
        #
        # buttonSelectPic = tk.Button(frame5, text="Select img", command=controller.selectImg)
        # buttonSelectPic.pack(padx=10, pady=5, side="left")
        #
        # self.buttonRefresh = tk.Button(frame5, text="Refresh", state="disabled", command=controller.refreshLBP)
        # self.buttonRefresh.pack(padx=10, pady=5, side="left")

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(padx=10, pady=5, side="bottom")
