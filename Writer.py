import os


class Writer:

    def __init__(self):

        self.labelDictionary = {}

    def writeAnnotedDataToFile(self, labelDictionary, saveDirectory):
        """ Funkcija za spremanje oznacenih slika u datoteku self.pathToLabels
        """

        if not os.path.isdir(saveDirectory):
            os.mkdir(saveDirectory)

        filename = saveDirectory + "/" + "labeledData.txt"

        f = open(filename, "w")

        for i in labelDictionary:
            row = str(i) + ":" + str(labelDictionary[i]) + "\n"
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

    def getLabelDictionary(self):
        """ Funkcija za dohvat rjecnika labeala
        """

        return self.labelDictionary

    def saveResults(self, saveDirectory):

        filename = saveDirectory + "/" + "results.txt"

        f = open(filename, "a")

        f.close()


if __name__ == "__main__":

    writer = Writer()
    saveDirectory = r"data/normalData"
    writer.writeAnnotedDataToFile(writer.labelDictionary, saveDirectory)
