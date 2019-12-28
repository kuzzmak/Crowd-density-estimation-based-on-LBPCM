import os


class Writer:

    def __init__(self, saveDirectory=""):

        self.labelDictionary = {}
        self.saveDirectory = saveDirectory

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

    def saveResults(self):

        filename = self.saveDirectory + "/" + "results.txt"

        f = open(filename, "a")

        f.close()


if __name__ == "__main__":

    saveDirectory = r"data/normalData"
    writer = Writer(saveDirectory)
    dic = {}
    dic[1] = 1
    dic[2] = 2
    writer.labelDictionary = dic
    writer.writeAnnotedDataToFile()
