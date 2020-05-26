import tkinter as tk
import cv2 as cv
import os
from PIL import Image, ImageTk
from Pages import InitializationPage as iP
import Writer

class DataAnnotationPage(tk.Frame):
    """ razred za oznacavanje pripadnosti pojedinog slikovnog elementa određenom razredu gustoće
    """

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.labelImageName = tk.Label(self, text="")
        self.labelImageName.pack(padx=10, pady=10)

        self.labelPic = tk.Label(self, text="")
        self.labelPic.pack(padx=10, pady=10)

        self.labelAnnotedDataCounter = tk.Label(self, text="")
        self.labelAnnotedDataCounter.pack(padx=10, pady=10)

        self.processedDataPictures = [f for f in os.listdir(controller.app.configuration['processedDataDirectory'])]
        self.dataAnnotationCounter = 0

        buttonFrame = tk.Frame(self)
        buttonFrame.pack()

        # gumbi
        buttonZero = tk.Button(buttonFrame, text="No flow",
                               command=lambda: self.annotate('0', controller))
        buttonZero.grid(row=0, column=0, padx=10, pady=10)

        buttonFreeFlow = tk.Button(buttonFrame, text="Free Flow",
                                   command=lambda: self.annotate('1', controller))
        buttonFreeFlow.grid(row=0, column=1, padx=10, pady=10)

        buttonRestrictedFlow = tk.Button(buttonFrame, text="Restricted flow",
                                         command=lambda: self.annotate('2', controller))
        buttonRestrictedFlow.grid(row=0, column=2, padx=10, pady=10)

        buttonDenseFlow = tk.Button(buttonFrame, text="Dense flow",
                                    command=lambda: self.annotate('3', controller))
        buttonDenseFlow.grid(row=0, column=3, padx=10, pady=10)

        buttonJammedFlow = tk.Button(buttonFrame, text="Jammed flow",
                                     command=lambda: self.annotate('4', controller))
        buttonJammedFlow.grid(row=0, column=4, padx=10, pady=10)

        frameNav = tk.Frame(self)
        frameNav.pack(padx=10, pady=10)

        buttonLoadLabels = tk.Button(frameNav, text="Load labels", command=lambda: self.loadLabels(controller))
        buttonLoadLabels.grid(row=0, column=0, padx=10, pady=10)

        buttonPreviousPic = tk.Button(frameNav, text="Prev pic", command=lambda: self.prevPicAnnotation(controller))
        buttonPreviousPic.grid(row=0, column=1, padx=10, pady=10)

        buttonSave = tk.Button(frameNav, text="Save", command=lambda: self.saveAnnotedData(controller))
        buttonSave.grid(row=0, column=2, padx=10, pady=10)

        buttonBack = tk.Button(frameNav, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.grid(row=0, column=3, padx=10, pady=10)

        self.writer = Writer.Writer()
        self.labelDictionary = {}

    def updateDataAnnotationFrame(self, controller):
        pass
        """ funkcija za azuriranje stranice za oznacavanje slika
        """

        # staza do trenutne slike
        imagePath = os.path.join(controller.app.configuration['processedDataDirectory'],
                                 self.processedDataPictures[self.dataAnnotationCounter])
        image = cv.imread(imagePath)
        self.im = ImageTk.PhotoImage(image=Image.fromarray(image))
        # postavljanje slike u labelu
        self.labelPic.configure(image=self.im)
        # postavljanje imena slike u labelu
        self.labelImageName.configure(text="image: " + self.processedDataPictures[self.dataAnnotationCounter])

        self.labelAnnotedDataCounter.configure(
            text=str(self.dataAnnotationCounter) + "/" + str(self.processedDataPictures.__len__()))

    def prevPicAnnotation(self, controller):
        """ funkcija za prikaz prethodne slike na stranici za oznacavanje slika
        """

        if self.dataAnnotationCounter >= 1:
            self.dataAnnotationCounter -= 1
            self.updateDataAnnotationFrame(controller)
        else:
            controller.consolePrint("[WARNING] no previous pictures remaining")

    def annotate(self, label, controller):
        """ funkcija za stvaranje oznake pojedine slke i spremanje u rjecnik i datoteku
        """

        # ime slike
        picName = self.processedDataPictures[self.dataAnnotationCounter]
        # dodijeljena labela
        saveString = picName + ":" + label
        self.labelDictionary[picName] = label

        # ako smo dosli do zadnje onda se staje
        if self.dataAnnotationCounter < self.processedDataPictures.__len__():
            self.dataAnnotationCounter += 1
            self.updateDataAnnotationFrame(controller)
            controller.consolePrint(saveString, dots=False)
        else:
            controller.consolePrint("[INFO] all pictures labeled")

    def saveAnnotedData(self, controller):
        """ funkcija za spremanje rječnika slika i oznaka
        """

        self.writer.labelDictionary = self.labelDictionary
        self.writer.writeAnnotedDataToFile(controller)

        controller.consolePrint("[INFO] labels and images saved to: " +
                                os.path.join(controller.app.configuration['labeledDataDirectory'], 'labeledData.txt'),
                                dots=False)

        controller.consolePrint("[INFO] saved " + str(self.labelDictionary.__len__()) + " labeled images")

    def loadLabels(self, controller):

        self.writer.loadAnnotedDataFromFile(
            os.path.join(controller.app.configuration['labeledDataDirectory'], "labeledData.txt"))
        self.labelDictionary = self.writer.labelDictionary
        self.dataAnnotationCounter = self.labelDictionary.__len__()
        self.updateDataAnnotationFrame(controller)
        controller.consolePrint("[INFO] loaded " + str(self.labelDictionary.__len__()) + " labels")
