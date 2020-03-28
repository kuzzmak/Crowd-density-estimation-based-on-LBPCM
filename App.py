import json
import GUI
import Writer
from tkinter import filedialog

class App:

    def __init__(self):

        # rječnik konfiguracije, sadrži staze do potrebnih resursa za aplikaciju
        self.configuration = {}
        # razred za manipulaciju s konfiguracijama, modelima i labelama
        self.writer = Writer.Writer()
        # rječnik labela
        self.labelDictionary = {}

        with open("configuration.json") as json_file:

            self.configuration = json.load(json_file)

        self.gui = GUI.App(self)

    def loadLabels(self):
        """ funkcija za ucitavanje oznaka slika koje su vec procesirane
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




if __name__ == "__main__":

    app = App()

    app.gui.mainloop()

