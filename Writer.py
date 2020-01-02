import os
from sklearn.externals import joblib
from tkinter import filedialog


class Writer:

    def __init__(self, saveDirectory=""):

        self.labelDictionary = {}
        self.saveDirectory = saveDirectory
        self.modelPath = r"data/models/"
        self.model = []
        self.modelString = ""

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

        if os.path.isfile(filename):

            f = open(filename, "a")

            f.write(saveString + "\n")

            f.close()
        else:
            f = open(filename, "w")

            f.write(saveString + "\n")

            f.close()

    def saveModel(self, model, conf):

        saveString = ""

        radius = conf[0]
        glcmDistance = conf[1]
        stepSize = conf[2]
        cellSize = conf[3]
        angles = conf[4]
        numOfNeighbors = conf[5]
        combine = conf[6]

        saveString += str(radius)
        saveString += "-"

        for i in glcmDistance:
            saveString += str(i)
            saveString += ","
        saveString = saveString[:-1]
        saveString += "-"

        saveString += str(stepSize)

        for i in cellSize:
            saveString += str(i)
            saveString += ","
        saveString = saveString[:-1]
        saveString += "-"

        for i in angles:
            saveString += str(i)
            saveString += ","
        saveString = saveString[:-1]
        saveString += "-"

        saveString += str(numOfNeighbors)
        saveString += "-"

        saveString += str(combine)

        filename = self.modelPath + saveString + ".pkl"
        joblib.dump(model, filename, compress=9)

    def loadModel(self):

        file = filedialog.askopenfilename(initialdir=r"C:\Users\kuzmi\PycharmProjects\untitled\data\models",
                                          title="Select model",
                                          filetypes=(("pickel files", "*.pkl"), ("all files", "*.*")))

        self.modelString = file.split("/")[-1]
        self.model = joblib.load(file)

    def getConfiguration(self):

        conf = []

        # uklanjanje .pkl
        modelString = self.modelString[:-4]
        # svaki parametar posebno
        splitStrings = modelString.split("-")

        radius = int(splitStrings[0])
        glcmDistance = [int(x) for x in splitStrings[1].split(",")]
        stepSize = int(splitStrings[2])
        cellSize = [int(x) for x in splitStrings[3].split(",")]
        angles = [float(x) for x in splitStrings[4].split(",")]
        numOfNeighbors = int(splitStrings[5])
        combine = int(splitStrings[6])

        conf.append(radius)
        conf.append(glcmDistance)
        conf.append(stepSize)
        conf.append(cellSize)
        conf.append(angles)
        conf.append(numOfNeighbors)
        conf.append(combine)

        return conf



