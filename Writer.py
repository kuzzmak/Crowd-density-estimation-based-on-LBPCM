from sklearn.externals import joblib
import json

class Writer:

    def __init__(self):

        self.labelDictionary = {}
        self.model = []
        self.modelConfiguration = []

    def writeAnnotedDataToFile(self, controller):
        """
        Funkcija za spremanje oznacenih slika u datoteku self.pathToLabels
        """

        filename = controller.configuration['modelsDirectory'] + "/" + "labeledData.txt"

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

    def saveModel(self, model, conf, controller):
        """
        Funkcija za spremanje modela i konfuguracije modela. Model se sprema
        kao objekt u pkl obliku, a konfiguracija se dodaje u json datoteku
        postojećih konfiguracija.

        :param model: model koji se sprema
        :param conf: konfiguracija koja se sprema
        :param controller referenca do glavnog programa
        """

        with open(controller.configuration['modelsDirectory'] + '/models.json') as f:
            data = json.load(f)

        # sljedeći indeks modela, za jedan više od postojećih modela
        nextIndex = len(data['models']) + 1

        if conf[1] == 'gray':
            saveString = controller.configuration['grayModelsDirectory'] + "/" + str(nextIndex) + ".pkl"
        else:
            saveString = controller.configuration['gradModelsDirectory'] + "/" + str(nextIndex) + ".pkl"

        # spremanje modela
        joblib.dump(model, saveString, compress=9)
        # spremanje konfiguracije
        self.appendToJSON(conf, controller)

    def findModel(self, json_object, id):
        """
        Funkcija za pronalazak konfiguracije modela prema njegovom id-ju.

        :param json_object: json objekt u kojem su zapisane konfiguracije modela
        :param id: id modela čija se konfiguracije traži
        :return: konfiguracija traženog modela
        """

        try:
            return [obj for obj in json_object["models"] if obj['id'] == id][0]
        except IndexError:
            print("Json file empty or there is no model with given index: " + str(id))

    @staticmethod
    def appendToJSON(conf, controller):
        """
        Funkcija za spremanje konfiguracije modela u json file

        :param conf: konfiguracija koju treba spremiti
        :param controller referenca fo glavnog programa
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

        with open(controller.configuration['modelsDirectory'] + '/models.json') as json_file:

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

        with open(controller.configuration['modelsDirectory'] + '/models.json', 'w') as f:
            json.dump(data, f, indent=4)

    def loadConfFromJSON(self, id, controller):
        """
        Funkcija koja služi za učitavanje parametara modela prema njegvom id-u

        :param id: identifikacijski broj pojedinog modela
        :param controller referenca do glavnog programa
        """

        with open(controller.app.configuration['modelsDirectory'] + '/models.json') as f:

            data = json.load(f)

            temp = self.findModel(data, id)

            conf = [temp['classifier_type'], temp['image_type'], temp['lbp_radius'], temp['distances'],
                    temp['step_size'], temp['cell_size'], temp['angles'], temp['num_of_neighbors'],
                    temp['combine_distances'], temp['combine_angles'], temp['functions'], temp['mean'], temp['sigma'],
                    temp['error']]

        return conf
