import os
import tkinter as tk

from Pages import ConfigurationsPage as coP
from Pages import InitializationPage as iP


class FeatureVectorCreationPage(tk.Frame):
    """ razred za stvaranje vektora znacajki
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        labelDescription = tk.Label(
            self,
            text="Here you can add new configurations for classifier training",
        )
        labelDescription.pack(padx=10, pady=10)

        processedImages = os.listdir(
            controller.app.configuration['processedDataDirectory']
        )
        labelProcessedImages = tk.Label(
            self,
            text="processed images: " + str(len(processedImages)),
        )
        labelProcessedImages.pack(pady=20)

        loadedFrame = tk.Frame(self)
        loadedFrame.pack(pady=5)

        labelLabelsLoaded = tk.Label(loadedFrame, text="Labels: ")
        labelLabelsLoaded.pack(side="left", padx=2)

        self.labelLabelsLoadedColor = tk.Label(
            loadedFrame,
            text="NOT LOADED",
            fg="red",
        )
        self.labelLabelsLoadedColor.pack(side="left", padx=2)

        self.middleFrame = tk.Frame(self)
        self.middleFrame.pack()

        # list svih progressbarova kako bi svaka konfiguracija ažurirala svoj
        self.progressBars = []
        self.progressLabels = []

        # frame s gumbima
        buttonFrame = tk.Frame(self)
        buttonFrame.pack(pady=20, side="bottom")

        buttonAddConfigurations = tk.Button(
            buttonFrame,
            text="Add configurations",
            command=lambda: controller.show_frame(coP.ConfigurationsPage),
        )
        buttonAddConfigurations.pack(side="left", padx=10, pady=5)

        buttonLoadAnnotedData = tk.Button(
            buttonFrame,
            text="Load labels",
            command=controller.app.loadLabels,
        )
        buttonLoadAnnotedData.pack(side="left", padx=10, pady=5)

        buttonBack = tk.Button(
            buttonFrame,
            text="Back",
            command=lambda: controller.show_frame(iP.InitializationPage),
        )
        buttonBack.pack(side="left", padx=10, pady=5)
