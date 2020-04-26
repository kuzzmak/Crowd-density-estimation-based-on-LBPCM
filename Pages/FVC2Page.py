import tkinter as tk
from PIL import ImageTk, Image
from Pages import InitializationPage as iP
import Pages.ModelPage as mp
from Pages import CLP2 as clP2
from tkinter import filedialog
import os

class FVC2Page(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.numberOfModels = tk.IntVar()
        self.numberOfModels.set(1)
        self.modelPages = []

        self.numberOfModelsLoaded = 0

        numOfModelsFrame = tk.Frame(self)
        numOfModelsFrame.grid(row=0, sticky="n")

        numOfModelsLabel = tk.Label(numOfModelsFrame, text="Select number of models to be used for classification.")
        numOfModelsLabel.pack(pady=5)

        rButtonFrame = tk.Frame(numOfModelsFrame)
        rButtonFrame.pack()

        rOne = tk.Radiobutton(rButtonFrame, text="One", variable=self.numberOfModels, value=1,
                              command=lambda: [self.showModelsPanel(controller), self.showModelIcon(controller)])
        rOne.pack(side="left", padx=10, pady=5)

        rTwo = tk.Radiobutton(rButtonFrame, text="Two", variable=self.numberOfModels, value=2,
                              command=lambda: [self.showModelsPanel(controller), self.showModelIcon(controller)])
        rTwo.pack(side="left", padx=10, pady=5)

        self.middleFrame = tk.Frame(self)
        self.middleFrame.grid(row=1, sticky="n")

        leftModel = mp.ModelPage(self.middleFrame, self, controller)
        leftModel.grid(row=0, column=0, padx=10)

        self.modelPages.append(leftModel)

        buttonFrame = tk.Frame(self)
        buttonFrame.grid(row=2, sticky="s", pady=10)

        self.buttonSelectPicture = tk.Button(buttonFrame, text="Select picture",
                                             command=lambda: self.selectPicture(controller), state="disabled")
        self.buttonSelectPicture.pack(side="left", padx=10, pady=10)

        self.buttonClassify = tk.Button(buttonFrame, text="Classify", state="disabled",
                                        command=lambda: [controller.show_frame(clP2.CLP2),
                                                         clP2.CLP2.updateClassificationFrame(controller.frames[clP2.CLP2], controller)])
        self.buttonClassify.pack(side="left", padx=10, pady=10)

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(side="left", padx=10, pady=10)

    def showModelsPanel(self, controller):
        """
        Stvara se onoliko informacijskih panela koliko je izabrano

        :param controller: referenca do glavnog prozora
        """

        numOfModels = self.numberOfModels.get()
        self.numberOfModelsLoaded = 0

        try:
            self.buttonClassify['state'] = 'disabled'
            self.buttonSelectPicture['state'] = 'disabled'
        except:
            pass

        if numOfModels == 2:

            rightModel = mp.ModelPage(self.middleFrame, self, controller)
            rightModel.grid(row=0, column=1, padx=30)

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

    def showModelIcon(self, controller):
        """
        Funkcija koja prikazuje ispravnu ikonu ako je model učitan ili nije
        """

        for mp in self.modelPages:

            im = Image.open(os.path.join(controller.app.configuration['iconsDirectory'], 'xmark.jpg'))
            im = im.resize((20, 20), Image.ANTIALIAS)
            mp.im = ImageTk.PhotoImage(im)

            mp.imageLabel.configure(image=mp.im)
            mp.imageLabelDescription.configure(text="model not loaded")

    def selectPicture(self, controller):
        """
        Funkcija za izbor slike za klasifikaciju
        """

        # staza do odabrane slike preko izbornika
        path = filedialog.askopenfilename(initialdir=controller.app.configuration['rawDataDirectory'],
                                          title="Select picture you want to classify",
                                          filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        if len(path) > 0:

            controller.app.pictureToClassify = path
            # omogućavanje gumba za klasifikaciju
            self.buttonClassify['state'] = 'normal'

        else:
            controller.consolePrint("[WARNING] you did not select any picture")

