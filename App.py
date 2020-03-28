import json
import GUI

class App:

    def __init__(self):

        # rječnik konfiguracije, sadrži staze do potrebnih resursa za aplikaciju
        self.configuration = {}

        with open("configuration.json") as json_file:

            self.configuration = json.load(json_file)

        self.gui = GUI.App()


if __name__ == "__main__":

    app = App()

    app.gui.mainloop()

