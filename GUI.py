import tkinter as tk

import Pages.CLP2 as clp2
import Pages.ConfigurationsPage as coP
import Pages.DataAnnotationPage as daP
import Pages.FeatureVectorCreationPage as fvcP
import Pages.FVC2Page as fvc2P
import Pages.GradientPage as gP
import Pages.InitializationPage as iP
import Pages.ParameterSettingPage as psP
import Pages.PreprocessPage as pP
import Pages.SlidingWindowPage as swP
import Pages.StartPage as sP


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

        self.onlyVotingClassifier = tk.IntVar()
        self.onlyVotingClassifier.set(1)

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

        self.show_frame(sP.StartPage)

    def show_frame(self, cont):
        """
        Funkcija za prikaz određenog frame-a
        """

        frame = self.frames[cont]
        frame.tkraise()

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
