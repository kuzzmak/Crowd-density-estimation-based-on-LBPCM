import os
from sklearn.externals import joblib
from tkinter import filedialog


class Writer:

    def __init__(self, saveDirectory=""):

        self.labelDictionary = {}
        self.saveDirectory = saveDirectory
        self.modelPath = r"data/models/"

    def writeAnnotedDataToFile(self):
        """ Funkcija za spremanje oznacenih slika u datoteku self.pathToLabels
        """

        if not os.path.isdir(self.saveDirectory):
            os.mkdir(self.saveDirectory)

        filename = self.saveDirectory + "/" + "labeledData.txt"

        f = open(filename, "w")

        for i in self.labelDictionary:
            row = str(i) + ":" + str(self.labelDictionary[i]) + "\n"
            f.write(row)
        f.close()

    def loadAnnotedDataFromFile(self, labeledData):
        """ Funkcija za ucitavanje vec oznacenih slika iz datoteke
        """

        with open(labeledData, "r") as f:
            rows = f.read()
            lines = rows.split("\n")

            for i in lines:
                if i != "":
                    keyVal = i.split(":")
                    self.labelDictionary[keyVal[0]] = keyVal[1]

    def saveResults(self, saveString):

        filename = self.saveDirectory + "/" + "results.txt"

        f = open(filename, "a")

        f.write(saveString)

        f.close()

    def saveModel(self, model, paramString):

        filename = self.modelPath + paramString
        joblib.dump(model, filename, compress=9)

    def loadModel(self):

        file = filedialog.askopenfilename(initialdir=r"C:\Users\kuzmi\PycharmProjects\untitled\data\models",
                                          title="Select model",
                                          filetypes=(("pickel files", "*.pkl"), ("all files", "*.*")))

        classifier = joblib.load(file)

        return classifier


