import tkinter as tk
import cv2 as cv
import os
from PIL import Image, ImageTk
from Pages import InitializationPage as iP

class DataAnnotationPage(tk.Frame):
    """ razred za oznacavanje pripadnosti pojedinog slikovnog elementa odredjenom razredu gustoce
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
        buttonZero = tk.Button(buttonFrame, text="No flow", command=lambda: self.annotate('0'))
        buttonZero.grid(row=0, column=0, padx=10, pady=10)

        buttonFreeFlow = tk.Button(buttonFrame, text="Free Flow", command=lambda: self.annotate('1'))
        buttonFreeFlow.grid(row=0, column=1, padx=10, pady=10)

        buttonRestrictedFlow = tk.Button(buttonFrame, text="Restricted flow", command=lambda: self.annotate('2'))
        buttonRestrictedFlow.grid(row=0, column=2, padx=10, pady=10)

        buttonDenseFlow = tk.Button(buttonFrame, text="Dense flow", command=lambda: self.annotate('3'))
        buttonDenseFlow.grid(row=0, column=3, padx=10, pady=10)

        buttonJammedFlow = tk.Button(buttonFrame, text="Jammed flow", command=lambda: self.annotate('4'))
        buttonJammedFlow.grid(row=0, column=4, padx=10, pady=10)

        frameNav = tk.Frame(self)
        frameNav.pack(padx=10, pady=10)

        buttonPreviousPic = tk.Button(frameNav, text="Prev pic", command=self.prevPicAnnotation)
        buttonPreviousPic.grid(row=0, column=0, padx=10, pady=10)

        buttonSave = tk.Button(frameNav, text="Save", command=self.saveAnnotedData, state="disabled")
        buttonSave.grid(row=0, column=1, padx=10, pady=10)

        buttonBack = tk.Button(frameNav, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.grid(row=0, column=2, padx=10, pady=10)

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