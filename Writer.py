import os
from sklearn.externals import joblib
from tkinter import filedialog
import json


class Writer:

    def __init__(self, saveDirectory=""):

        self.labelDictionary = {}
        self.saveDirectory = saveDirectory
        self.grayModelsPath = r"data/models_v2/grayModels"
        self.gradModelsPath = r"data/models_v2/gradModels"
        self.modelJSON = r'data/models_v2/models.json'
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
        """
        Funkcija za ucitavanje vec oznacenih slika iz datoteke

        :param labeledData staza do datoteke s označenim slikama
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

    # def saveModel(self, model, conf):
    #
    #     saveString = ""
    #
    #     radius = conf[0]
    #     glcmDistance = conf[1]
    #     stepSize = conf[2]
    #     cellSize = conf[3]
    #     angles = conf[4]
    #     numOfNeighbors = conf[5]
    #     combineDistances = conf[6]
    #     combineAngles = conf[7]
    #
    #     saveString += str(radius)
    #     saveString += "-"
    #
    #     for i in glcmDistance:
    #         saveString += str(i)
    #         saveString += ","
    #     saveString = saveString[:-1]
    #     saveString += "-"
    #
    #     saveString += str(stepSize)
    #     saveString += "-"
    #
    #     for i in cellSize:
    #         saveString += str(i)
    #         saveString += ","
    #     saveString = saveString[:-1]
    #     saveString += "-"
    #
    #     for i in angles:
    #         saveString += str(i)
    #         saveString += ","
    #     saveString = saveString[:-1]
    #     saveString += "-"
    #
    #     saveString += str(numOfNeighbors)
    #     saveString += "-"
    #
    #     saveString += str(combineDistances)
    #     saveString += "-"
    #
    #     saveString += str(combineAngles)
    #
    #     filename = self.modelPath + saveString + ".pkl"
    #     joblib.dump(model, filename, compress=9)

    def saveModel(self, model, conf):
        """
        Funkcija za spremanje modela i konfuguracije modela. Model se sprema
        kao objekt u pkl obliku, a konfiguracija se dodaje u json datoteku
        postojećih konfiguracija.

        :param model: model koji se sprema
        :param conf: konfiguracija koja se sprema
        """

        with open(self.modelJSON) as f:
            data = json.load(f)

        # sljedeći indeks modela, za jedan više od postojećih modela
        nextIndex = len(data['models']) + 1

        if conf[1] == 'gray':
            saveString = self.grayModelsPath + "/" + str(nextIndex) + ".pkl"
        else:
            saveString = self.gradModelsPath + "/" + str(nextIndex) + ".pkl"

        # spremanje modela
        joblib.dump(model, saveString, compress=9)
        # spremanje konfiguracije
        self.appendToJSON(conf)

    def loadModel(self):

        file = filedialog.askopenfilename(initialdir=r"data/models",
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
        combineDistances = int(splitStrings[6])
        combineAngles = int(splitStrings[7])

        conf.append(radius)
        conf.append(glcmDistance)
        conf.append(stepSize)
        conf.append(cellSize)
        conf.append(angles)
        conf.append(numOfNeighbors)
        conf.append(combineDistances)
        conf.append(combineAngles)

        return conf

    def findModel(self, json_object, id):
        try:
            return [obj for obj in json_object["models"] if obj['id'] == id][0]
        except IndexError:
            print("Json file empty or there is no model with given index: " + str(id))

    def appendToJSON(self, conf):
        """
        Funkcija za spremanje konfiguracije modela u json file

        :param conf: konfiguracija koju treba spremiti
        """
        classifierType, \
        picType, \
        lbpRadius, \
        glcmDistances, \
        stepSize, \
        cellSize, \
        angles, \
        numberOfNeighbors, \
        combineDistances, \
        combineAngles, \
        functions, \
        mean, \
        sigma,\
        error = conf

        with open(self.modelJSON) as json_file:

            data = json.load(json_file)

            temp = data['models']

            y = {
                "id": len(temp) + 1,
                "classifier_type": classifierType,
                "image_type": picType,
                "lbp_radius": lbpRadius,
                "distances": glcmDistances,
                "step_size": stepSize,
                "cell_size": cellSize,
                "angles": angles,
                "num_of_neighbors": numberOfNeighbors,
                "combine_distances": combineDistances,
                "combine_angles": combineAngles,
                "functions": functions,
                "mean": mean,
                "sigma": sigma,
                "error": error
            }

            temp.append(y)

        with open(self.modelJSON, 'w') as f:
            json.dump(data, f, indent=4)

    def loadConfFromJSON(self, id):
        """
        Funkcija koja služi za učitavanje parametara modela prema njegvom id-u

        :param id: identifikacijski broj pojedinog modela
        """

        with open(self.modelJSON) as f:

            data = json.load(f)

            temp = self.findModel(data, id)

            conf = [temp['classifier_type'], temp['image_type'], temp['lbp_radius'], temp['distances'],
                    temp['step_size'], temp['cell_size'], temp['angles'], temp['num_of_neighbors'],
                    temp['combine_distances'], temp['combine_angles'], temp['functions'], temp['mean'], temp['sigma'],
                    temp['error']]

        return conf
