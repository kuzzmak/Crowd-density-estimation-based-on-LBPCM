import tkinter as tk
from PIL import ImageTk, Image
import Pages.InitializationPage as iP
import Pages.ModelPage as mp

class FVC2Page(tk.Frame):

    def __init__(self, parent, controller):

        self.numberOfModels = tk.IntVar()
        self.numberOfModels.set(1)
        self.modelPages = []

        self.checkmark = r'data/model_icons/checkmark.jpg'
        self.xmark = r'data/model_icons/xmark.jpg'

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        numOfModelsFrame = tk.Frame(self)
        numOfModelsFrame.grid(row=0, sticky="n")

        numOfModelsLabel = tk.Label(numOfModelsFrame, text="Select number of models to be used for classification.")
        numOfModelsLabel.pack(pady=5)

        rButtonFrame = tk.Frame(numOfModelsFrame)
        rButtonFrame.pack()

        rOne = tk.Radiobutton(rButtonFrame, text="One", variable=self.numberOfModels, value=1,
                              command=lambda: [self.showModelsPanel(controller), self.showModelIcon()])
        rOne.pack(side="left", padx=10, pady=5)

        rTwo = tk.Radiobutton(rButtonFrame, text="Two", variable=self.numberOfModels, value=2,
                              command=lambda: [self.showModelsPanel(controller), self.showModelIcon()])
        rTwo.pack(side="left", padx=10, pady=5)

        self.middleFrame = tk.Frame(self)
        self.middleFrame.grid(row=1, sticky="n")

        leftModel = mp.ModelPage(self.middleFrame, self, controller)
        leftModel.grid(row=0, column=0, padx=10)

        self.modelPages.append(leftModel)

        buttonFrame = tk.Frame(self)
        buttonFrame.grid(row=2, sticky="s", pady=10)

        buttonPrintModels = tk.Button(buttonFrame, text="print", command=self.printModels)
        buttonPrintModels.pack(side="left", padx=10)

        self.buttonClassify = tk.Button(buttonFrame, text="Classify", state="disabled")
        self.buttonClassify.pack(side="left", padx=10, pady=10)

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(side="left", padx=10, pady=10)

    def showModelsPanel(self, controller):
        """
        Stvara se onoliko informacijskih panela koliko je izabrano

        :param controller: referenca do glavnog prozora
        """

        numOfModels = self.numberOfModels.get()

        try:
            self.buttonClassify['state'] = 'disabled'
        except:
            pass

        if numOfModels == 2:

            rightModel = mp.ModelPage(self.middleFrame, self, controller)
            rightModel.grid(row=0, column=1, padx=30)

            # micanje modela lijevog dijela stranice
            self.modelPages[0].writer.model = []

            # ako je ponovno kliknutno na dva modela
            if len(self.modelPages) == 2:
                # miče se zadnje dodani
                self.modelPages.pop(1)
                # dodaje se nova desna stranica
                self.modelPages.append(rightModel)
            else:
                self.modelPages.append(rightModel)
        else:

            self.middleFrame.destroy()
            self.middleFrame = tk.Frame(self)
            self.middleFrame.grid(row=1)

            leftModel = mp.ModelPage(self.middleFrame, self, controller)
            leftModel.grid(row=0, column=0, padx=30)

            self.modelPages = []
            self.modelPages.append(leftModel)

    def showModelIcon(self):
        """
        Funkcija koja prikazuje ispravnu ikonu ako je model učitan ili nije
        """

        for mp in self.modelPages:

            im = Image.open(self.xmark)
            im = im.resize((20, 20), Image.ANTIALIAS)
            mp.im = ImageTk.PhotoImage(im)

            mp.imageLabel.configure(image=mp.im)
            mp.imageLabelDescription.configure(text="model not loaded")

    def printModels(self):

        for m in self.modelPages:
            print(m.writer.model)
        print()