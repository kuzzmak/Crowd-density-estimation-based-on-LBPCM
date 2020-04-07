import tkinter as tk
from tkinter.filedialog import askdirectory
import json
from Pages import InitializationPage as iP

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

        dataPathButton = tk.Button(rightFrame, text="Select folder",
                                   command=lambda: self.selectFolder(controller, 'dataPath'))
        dataPathButton.grid(pady=5, row=0, sticky="e")

        normalDataPath = tk.Label(leftFrame, text="unprocessed data path:")
        normalDataPath.grid(pady=10, row=1, sticky="e")

        normalDataPathButton = tk.Button(rightFrame, text="Select folder",
                                         command=lambda: self.selectFolder(controller, 'unprocessedDataPath'))
        normalDataPathButton.grid(pady=5, row=1, sticky="w")

        processedDataPathLabel = tk.Label(leftFrame, text="processed data:")
        processedDataPathLabel.grid(pady=10, row=2, sticky="e")

        processedDataPathButton = tk.Button(rightFrame, text="Select folder",
                                            command=lambda: self.selectFolder(controller, 'processedImagesPath'))
        processedDataPathButton.grid(pady=5, row=2, sticky="w")

        labeledDataDirectory = tk.Label(leftFrame, text="label directory path:")
        labeledDataDirectory.grid(pady=10, row=3, sticky="e")

        labeledDataDirectoryButton = tk.Button(rightFrame, text="Select folder",
                                               command=lambda: self.selectFolder(controller, 'labeledDataDirectory'))
        labeledDataDirectoryButton.grid(pady=5, row=3, sticky="w")

        grayModelsPath = tk.Label(leftFrame, text="gray models path:")
        grayModelsPath.grid(pady=10, row=4, sticky="e")

        grayModelsPathButton = tk.Button(rightFrame, text="Select folder",
                                         command=lambda: self.selectFolder(controller, 'grayModelsPath'))
        grayModelsPathButton.grid(pady=5, row=4, sticky="w")

        gradModelsPath = tk.Label(leftFrame, text="gradient models path:")
        gradModelsPath.grid(pady=10, row=5, sticky="e")

        gradModelsPathButton = tk.Button(rightFrame, text="Select folder",
                                         command=lambda: self.selectFolder(controller, 'gradModelsPath'))
        gradModelsPathButton.grid(pady=5, row=5, sticky="w")

        iconsPath = tk.Label(leftFrame, text="icons path:")
        iconsPath.grid(pady=10, row=6, sticky="e")

        iconsPathButton = tk.Button(rightFrame, text="Select folder",
                                    command=lambda: self.selectFolder(controller, 'iconsPath'))
        iconsPathButton.grid(pady=5, row=6, sticky="w")

        # panel sa trenutnom konfiguracijom
        currentConfigurationFrame = tk.Frame(self)
        currentConfigurationFrame.pack(padx=10)

        currentConfigurationDescription = tk.Label(currentConfigurationFrame, text="Current configuration")
        currentConfigurationDescription.pack(pady=10)

        leftValuesFrame = tk.Frame(currentConfigurationFrame)
        leftValuesFrame.pack(side="left")

        rightValuesFrame = tk.Frame(currentConfigurationFrame)
        rightValuesFrame.pack(side="left")

        labelCurrentDataPath = tk.Label(leftValuesFrame, text="data path: ")
        labelCurrentDataPath.grid(row=0, pady=3, sticky="e")

        self.labelCurrentDataPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['dataPath'])
        self.labelCurrentDataPathValue.grid(row=0, pady=3, sticky="w")

        labelCurrentNormalDataPath = tk.Label(leftValuesFrame, text="unprocessed data path: ")
        labelCurrentNormalDataPath.grid(row=1, pady=3, sticky="e")

        self.labelCurrentNormalDataPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['unprocessedDataPath'])
        self.labelCurrentNormalDataPathValue.grid(row=1, pady=3, sticky="w")

        labelProcessedDataPath = tk.Label(leftValuesFrame, text="processed data path: ")
        labelProcessedDataPath.grid(row=2, pady=3, sticky="e")

        self.labelProcessedDataPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['processedImagesPath'])
        self.labelProcessedDataPathValue.grid(row=2, pady=3, sticky="w")

        labelLabelDirectoryPath = tk.Label(leftValuesFrame, text="label data directory: ")
        labelLabelDirectoryPath.grid(row=3, pady=3, sticky="e")

        self.labelLabelDirectoryPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['labeledDataDirectory'])
        self.labelLabelDirectoryPathValue.grid(row=3, pady=3, sticky="w")

        labelGrayModelsPath = tk.Label(leftValuesFrame, text="gray models path: ")
        labelGrayModelsPath.grid(row=4, pady=3, sticky="e")

        self.labelGrayModelsPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['grayModelsPath'])
        self.labelGrayModelsPathValue.grid(row=4, pady=3, sticky="w")

        labelGradModelsPath = tk.Label(leftValuesFrame, text="grad models path: ")
        labelGradModelsPath.grid(row=5, pady=3, sticky="e")

        self.labelGradModelsPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['gradModelsPath'])
        self.labelGradModelsPathValue.grid(row=5, pady=3, sticky="w")

        labelIconsPath = tk.Label(leftValuesFrame, text="icons path: ")
        labelIconsPath.grid(row=6, pady=3, sticky="e")

        self.labelIconsPathValue = tk.Label(rightValuesFrame, text=controller.app.configuration['iconsPath'])
        self.labelIconsPathValue.grid(row=6, pady=3, sticky="w")

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(padx=10, pady=5, side="bottom")

    def selectFolder(self, controller, settingName):
        """
        Funkcija za odabir foldera

        :param controller: referenca do glavne aplikacije
        :param settingName: parametar za koji se bira folder
        """

        folderName = askdirectory(title='Select Folder')

        if len(folderName) > 0:

            controller.app.configuration[settingName] = folderName

            with open('configuration.json', 'w') as f:
                json.dump(controller.app.configuration, f, indent=4)

            self.refreshParameters(controller)

        else:
            controller.consolePrint("[WARNING] you did not select any folder")

    def refreshParameters(self, controller, settingName):
        """
        Funkcija za osvježavanje parametara na parameter stranici

        :param controller: referenca do glavne aplikacije
        :param settingName: parametar koji se osvježava
        """

        if settingName == 'dataPath':
            self.labelCurrentDataPathValue.configure(text=controller.app.configuration[settingName])
        elif settingName == 'unprocessedDataPath':
            self.labelCurrentNormalDataPathValue.configure(text=controller.app.configuration[settingName])
        elif settingName == 'processedImagesPath':
            self.labelProcessedDataPathValue.configure(text=controller.app.configuration[settingName])
        elif settingName == 'labeledDataDirectory':
            self.labelLabelDirectoryPathValue.configure(text=controller.app.configuration[settingName])
        elif settingName == 'grayModelsPath':
            self.labelGrayModelsPathValue.configure(text=controller.app.configuration[settingName])
        elif settingName == 'gradModelsPath':
            self.labelGradModelsPathValue.configure(text=controller.app.configuration[settingName])
        elif settingName == 'iconsPath':
            self.labelIconsPathValue.configure(text=controller.app.configuration[settingName])