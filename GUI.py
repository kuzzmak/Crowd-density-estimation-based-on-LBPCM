import tkinter as tk

import Pages.InitializationPage as iP
import Pages.GradientPage as gP
import Pages.StartPage as sP
import Pages.FeatureVectorCreationPage as fvcP
import Pages.ConfigurationsPage as coP
import Pages.PreprocessPage as pP
import Pages.ParameterSettingPage as psP
import Pages.SlidingWindowPage as swP
import Pages.DataAnnotationPage as daP
import Pages.FVC2Page as fvc2P
import Pages.CLP2 as clp2

class App(tk.Tk):

    def __init__(self, app, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.app = app

        # frame koji sadrzi pojedinu stranicu
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # konzola
        consoleFrame = tk.Frame(self)
        consoleFrame.pack(side="bottom", fill="both", expand=True)
        # scrollbar konzole
        scroll = tk.Scrollbar(consoleFrame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.console = tk.Text(consoleFrame, height=5, width=30)
        self.console.pack(side="left", fill="both", expand=True)
        scroll.config(command=self.console.yview)
        self.console.config(yscrollcommand=scroll.set)

        labelConsole = tk.Label(self, text="Console window")
        labelConsole.pack(side="bottom")

        # trenutna slika na stranici za parametre
        self.currPicPar = [[]]
        # rjecnik svih stranica
        self.frames = {}

        # polje slika za pretprocesiranje
        self.dataPictures = []
        # polje lokacija celije koja se krece po slici
        self.picDims = []
        # brojac trenutne slike
        self.picCounter = 0

        # brojac za slike kod oznacavanja
        self.dataAnnotationCounter = 0

        # lista imena procesiranih slika
        self.processedDataPictures = []

        # check gumbi za funkcije koje sačinjavaju vektore značajki
        self.functionButtons = []
        # stvaranje gumba za svaku od 14 funkcija
        self.names = ["angular second moment",
                 "contrast",
                 "correlation",
                 "sum of squares: variance",
                 "inverse difference moment",
                 "sum average",
                 "sum variance",
                 "sum entropy",
                 "entropy",
                 "difference variance",
                 "difference entropy",
                 "imoc1",
                 "imoc2",
                 "maximal correlation coefficient"]

        for c in range(14):
            name = "f" + str(c + 1)
            self.functionButtons.append((name, self.names[c], tk.IntVar()))

        for F in (pP.PreprocessPage,
                  sP.StartPage,
                  iP.InitializationPage,
                  psP.ParameterSettingPage,
                  swP.SlidingWindowPage,
                  daP.DataAnnotationPage,
                  fvcP.FeatureVectorCreationPage,
                  coP.ConfigurationsPage,
                  gP.GradientPage,
                  fvc2P.FVC2Page,
                  clp2.CLP2):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, sticky="nsew")

        self.show_frame(iP.InitializationPage)

    def show_frame(self, cont):
        """
        Funkcija za prikaz određenog frame-a
        """

        frame = self.frames[cont]
        frame.tkraise()

    def updateDataAnnotationFrame(self):
        pass
    #     """ funkcija za azuriranje stranice za oznacavanje slika
    #     """
    #
    #     # staza do trenutne slike
    #     imagePath = self.app.configuration['processedImagesPath'] + "/" + self.processedDataPictures[self.dataAnnotationCounter]
    #     image = cv.imread(imagePath)
    #     self.im = ImageTk.PhotoImage(image=Image.fromarray(image))
    #     # postavljanje slike u labelu
    #     self.frames[daP.DataAnnotationPage].labelPic.configure(image=self.im)
    #     # postavljanje imena slike u labelu
    #     self.frames[daP.DataAnnotationPage].labelImageName.configure(
    #         text=self.processedDataPictures[self.dataAnnotationCounter])
    #
    #     self.frames[daP.DataAnnotationPage].labelAnnotedDataCounter.configure(
    #         text=str(self.dataAnnotationCounter) + "/" + str(self.processedDataPictures.__len__()))

    def prevPicAnnotation(self):
        pass
    #     """ funkcija za prikaz prethodne slike na stranici za oznacavanje slika
    #     """
    #
    #     if self.dataAnnotationCounter >= 1:
    #         self.dataAnnotationCounter -= 1
    #         self.updateDataAnnotationFrame()
    #     else:
    #         self.console.insert(tk.END, "[WARNING] no previous pictures remaining\n")
    #         self.console.insert(tk.END, "----------------------------------------\n")
    #         self.console.see(tk.END)

    def annotate(self, label):
        pass
    #     """ funkcija za stvaranje oznake pojedine slke i spremanje u rjecnik i datoteku
    #     """
    #
    #     # ime slike
    #     picName = self.processedDataPictures[self.dataAnnotationCounter]
    #     # dodijeljena labela
    #     saveString = picName + ":" + label
    #     self.labelDictionary[picName] = label
    #
    #     # ako smo dosli do zadnje onda se staje
    #     if self.dataAnnotationCounter < self.processedDataPictures.__len__():
    #         self.dataAnnotationCounter += 1
    #         self.updateDataAnnotationFrame()
    #         self.console.insert(tk.END, saveString + "\n")
    #         self.console.see(tk.END)
    #     else:
    #         self.console.insert(tk.END, "[INFO] all pictures labeled\n")
    #         self.console.insert(tk.END, "----------------------------------------\n")
    #         self.console.see(tk.END)

    def saveAnnotedData(self):
        pass
    #     """ funkcija za spremanje rjecnika slika i oznaka
    #     """
    #
    #     self.writer.saveDirectory = r"data2/normalData"
    #     self.writer.labelDictionary = self.labelDictionary
    #     self.writer.writeAnnotedDataToFile()
    #
    #     self.console.insert(tk.END, "[INFO] labels and images saved to: " + self.writer.saveDirectory + "\n")
    #     self.console.insert(tk.END, "[INFO] saved " + str(self.labelDictionary.__len__()) + " labeled images\n")
    #     self.console.insert(tk.END, "----------------------------------------\n")
    #     self.console.see(tk.END)

    def consolePrint(self, message, dots=True):
        """
        Funkcija za ispis poruke u konzolu

        :param message: poruka za ispis
        :param dots: ispisuju li se crtice za odvajanje poruka
        """

        self.console.insert(tk.END, message + "\n")
        if dots:
            self.console.insert(tk.END, "----------------------------------------\n")
        self.console.see(tk.END)