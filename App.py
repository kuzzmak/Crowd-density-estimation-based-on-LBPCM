import json
import GUI
import Writer
from tkinter import filedialog
from math import radians
from tkinter import IntVar, END

from Pages import ConfigurationsPage as coP
from Pages import FeatureVectorCreationPage as fvcP

class App:

    def __init__(self):

        # rječnik konfiguracije, sadrži staze do potrebnih resursa za aplikaciju
        self.configuration = {}
        # razred za manipulaciju s konfiguracijama, modelima i labelama
        self.writer = Writer.Writer()
        # rječnik labela
        self.labelDictionary = {}
        # lista konfiguracija za učenje modela
        self.configurations = []

        with open("configuration.json") as json_file:

            self.configuration = json.load(json_file)

        self.gui = GUI.App(self)

    def loadLabels(self):
        """
        Funkcija za učitavanje oznaka slika koje su već procesirane
        """

        file = filedialog.askopenfilename(initialdir=self.configuration['labeledDataDirectory'],
                                          title="Select labeled data file",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))

        if len(file) == 0:
            self.gui.consolePrint("[WARNING] you did not select file with labeled data")
        else:
            self.writer.loadAnnotedDataFromFile(file)
            self.labelDictionary = self.writer.labelDictionary
            # self.dataAnnotationCounter = self.writer.labelDictionary.__len__()

            self.gui.consolePrint("[INFO] loaded " + str(self.labelDictionary.__len__()) + " labels")

    def addConf(self):
        """
        Funkcija za dohvaćanje parametara konfiguracije iz polja za unos sa stranice
        ConfigurationsPage
        """

        parametersOK = True

        # dohvat vrste slike nad kojom se provodi postupak LBP
        picType = self.gui.frames[coP.ConfigurationsPage].rPicType.get()

        classifierType = self.gui.frames[coP.ConfigurationsPage].rClassifierType.get()

        # dohvat parametara za konfiguraciju
        try:
            radius = int(self.gui.frames[coP.ConfigurationsPage].entryLBPRadius.get())
            if radius < 1:
                raise ValueError
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for radius")

        try:
            glcmDistance = [int(x) for x in self.gui.frames[coP.ConfigurationsPage].entryGLCMDistance.get().split(",")]
            for d in glcmDistance:
                if d < 1:

                    raise ValueError
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for glcm distance")

        try:
            stepSize = int(self.gui.frames[coP.ConfigurationsPage].entryStepSize.get())
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for step size")

        try:
            cellSize = [int(x) for x in self.gui.frames[coP.ConfigurationsPage].entryCellSize.get().split(",")]
            if len(cellSize) != 2:
                raise ValueError
            for c in cellSize:
                if c < 1:
                    raise ValueError
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for cell size")

        try:
            angles = [radians(int(i)) for i in self.gui.frames[coP.ConfigurationsPage].entryAngles.get().split(",")]
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for angles")

        try:
            numOfNeighbors = int(self.gui.frames[coP.ConfigurationsPage].entryNumOfNeighbors.get())
            if numOfNeighbors < 1:
                raise ValueError
        except ValueError:
            parametersOK = False
            self.gui.consolePrint("[ERROR] please check your input for number of neighbors")

        combineDistances = self.gui.frames[coP.ConfigurationsPage].rCombineDistances.get()
        combineAngles = self.gui.frames[coP.ConfigurationsPage].rCombineAngles.get()

        functions = []

        # dohvaćanje imena odabranih funkcija
        for _, name, c in self.gui.functionButtons:
            if c.get():
                functions.append(name)

        if len(functions) == 0:
            parametersOK = False
            self.gui.consolePrint("[INFO] please select one or more Haralick functions")

        if parametersOK:
            # pojedina konfiguracija
            conf = [classifierType,
                    picType,
                    radius,
                    glcmDistance,
                    stepSize,
                    cellSize,
                    angles,
                    numOfNeighbors,
                    combineDistances,
                    combineAngles,
                    functions]

            self.configurations.append(conf)

            # ažuriranje labele broja konfiguracija
            self.gui.frames[fvcP.FeatureVectorCreationPage].labelProgressConf.configure(
                text="0/" + str(len(self.configurations)) + "   Configurations completed.")

            self.gui.console.insert(END, "new configuration added\n")
            self.gui.console.insert(END, str(conf) + "\n")
            self.gui.console.see(END)

if __name__ == "__main__":

    app = App()

    app.gui.mainloop()

