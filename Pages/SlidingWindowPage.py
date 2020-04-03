import tkinter as tk
from os import listdir
import cv2 as cv
from PIL import ImageTk, Image
import numpy as np
import util
from skimage.feature import local_binary_pattern
import Pages.InitializationPage as iP

class SlidingWindowPage(tk.Frame):
    """
    Razred gdje se prikazuje funkcionalnost kliznog prozora i vrijednost
    Haralickovih funkcija u odredjenenim celijama slikovnog elementa
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.functionButtons = []
        # vrsta slike na kojoj se primjenjuje LBP
        self.rType = tk.StringVar()

        self.currentPicture = 0
        self.currentCell = 0

        self.processedImages = listdir(controller.app.configuration['processedImagesPath'])
        # trenutno prikazana slika u frameu
        self.currentPicturePath = controller.app.configuration['processedImagesPath'] + "/" + \
                                  self.processedImages[self.currentPicture]
        # koordinate na slici za putujuću ćeliju
        self.picDims = util.makePicDims(cv.imread(self.currentPicturePath))

        for c in range(14):
            name = "f" + str(c + 1)
            self.functionButtons.append((name, controller.names[c], tk.IntVar()))

        # opis stranice
        description = tk.Label(self, text="Here you can see sliding window method on gray and gradient images.")
        description.pack(padx=10, pady=10)

        middleFrame = tk.Frame(self)
        middleFrame.pack()

        # panel sa slikom i gumbima za sljedeću sliku i sljedeću ćeliju
        leftPanel = tk.Frame(middleFrame)
        leftPanel.grid(row=0, column=0, sticky="n")

        rPanel = tk.Frame(leftPanel)
        rPanel.pack(padx=10, pady=10)

        rGray = tk.Radiobutton(rPanel, text="Gray", variable=self.rType, value='gray', command=self.updateImages)
        rGray.pack(side="left", padx=10)

        rGrad = tk.Radiobutton(rPanel, text="Gradient", variable=self.rType, value='grad', command=self.updateImages)
        rGrad.pack(side="left", padx=10)

        self.rType.set('gray')

        self.labelNormalImage = tk.Label(leftPanel, text="NO IMAGE\nLOADED")
        self.labelNormalImage.pack(padx=10, pady=10)

        self.labelLBPImage = tk.Label(leftPanel, text="NO IMAGE\nLOADED")
        self.labelLBPImage.pack(padx=10, pady=10)

        # frame s gumbima za sljedeću sliku, ćeliju
        buttonFrame = tk.Frame(leftPanel)
        buttonFrame.pack(pady=5)

        buttonPreviousPicture = tk.Button(buttonFrame, text="Prev pic", command=lambda: self.previousImage(controller))
        buttonPreviousPicture.pack(side="left", padx=5, pady=5)

        buttonNextPicture = tk.Button(buttonFrame, text="Next pic", command=lambda: self.nextImage(controller))
        buttonNextPicture.pack(side="left", padx=5, pady=5)

        buttonNextCell = tk.Button(buttonFrame, text="Next cell", command=lambda: self.nextCell(controller))
        buttonNextCell.pack(side="left", padx=5, pady=5)

        buttonCalculate = tk.Button(buttonFrame, text="Calculate function(s)")
        buttonCalculate.pack(side="left", padx=5, pady=5)

        # desni panel s gumbima za Haralickove funkcije
        rightPanel = tk.Frame(middleFrame)
        rightPanel.grid(row=0, column=1, sticky="e")

        i = 1
        for name, fName, c in controller.functionButtons:
            tk.Checkbutton(rightPanel, text=name + " - " + fName, variable=c).grid(row=i, pady="2", sticky="w")
            i += 1

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(side="bottom", padx=5, pady=5)

        self.updateImages()

    def updateImages(self):



        image = cv.imread(self.currentPicturePath, cv.IMREAD_GRAYSCALE)

        if self.rType.get() == 'gray':
            lbp = local_binary_pattern(image, 8, 1, method='default')
        else:
            sobel = cv.Sobel(image, cv.CV_8U, 1, 1, ksize=3)
            lbp = local_binary_pattern(sobel, 8, 1, method='default')

        start_point, end_point = self.picDims[self.currentCell]

        image = cv.cvtColor(image.astype('uint8'), cv.COLOR_GRAY2RGB)
        lbp = cv.cvtColor(lbp.astype('uint8'), cv.COLOR_GRAY2RGB)

        image_copy = cv.rectangle(np.copy(image), start_point, end_point, (255, 0, 0), 2)
        image_copy_lbp = cv.rectangle(np.copy(lbp), start_point, end_point, (255, 0, 0), 2)

        self.im = ImageTk.PhotoImage(image=Image.fromarray(image_copy))
        self.lbp = ImageTk.PhotoImage(image=Image.fromarray(image_copy_lbp))

        self.labelNormalImage.configure(image=self.im)
        self.labelLBPImage.configure(image=self.lbp)

    def nextImage(self, controller):
        """
        Funkcija za prelazak na sljedeću sliku.

        :param controller: referenca na glavni program
        """

        if self.currentPicture < len(self.processedImages):

            self.currentCell = 0
            self.currentPicture += 1
            self.currentPicturePath = controller.app.configuration['processedImagesPath'] + "/" + \
                                      self.processedImages[self.currentPicture]

            self.updateImages()
        else:
            controller.consolePrint("[ERROR] no remaining pictures")

    def previousImage(self, controller):
        """
        Funkcija za prelazak na prethodnu sliku.

        :param controller: referenca na glavni program
        """

        if self.currentPicture > 0:

            self.currentCell = 0
            self.currentPicture -= 1

            self.currentPicturePath = controller.app.configuration['processedImagesPath'] + "/" + \
                                      self.processedImages[self.currentPicture]

            self.updateImages()
        else:
            controller.consolePrint("[ERROR] no previous pictures")

    def nextCell(self, controller):
        """
        Funkcija za prelazak na sljedeću ćeliju na slici.

        :param controller: referenca do glavnog programa
        """

        if self.currentCell < len(self.picDims) - 1:

            self.currentCell += 1
            self.updateImages()
        else:
            controller.consolePrint("[ERROR] no more cells remaining")

    def calculateFunctions(self):

        pass


        # # labela za ime slike
        # self.labelPicName = tk.Label(mainFrame, text="")
        # self.labelPicName.pack()
        # # labela za sliku
        # self.labelPic = tk.Label(mainFrame, text="No picture\nloaded")
        # self.labelPic.pack(padx=10, pady=10)
        # # labela za lbp sliku
        # self.labelLBPPic = tk.Label(mainFrame)
        # self.labelLBPPic.pack(padx=10, pady=10)
        #
        # # gumbi--------------------------
        # buttonFrame = tk.Frame(mainFrame)
        # buttonFrame.pack(padx=20, pady=20, side="bottom", expand=True)
        #
        # buttonNextPicture = tk.Button(buttonFrame, text="Next pic", command=controller.nextPic)
        # buttonNextPicture.grid(row=0, column=1, padx=5, pady=5)
        #
        # buttonPreviousPicture = tk.Button(buttonFrame, text="Prev pic", command=controller.prevPic)
        # buttonPreviousPicture.grid(row=0, column=0, padx=5, pady=5)
        #
        # buttonNextCell = tk.Button(buttonFrame, text="Next cell", command=controller.nextCell)
        # buttonNextCell.grid(row=0, column=2, padx=5, pady=5)
        #
        # buttonReset = tk.Button(buttonFrame, text="Reset", command=controller.resetCell)
        # buttonReset.grid(row=0, column=3, padx=5, pady=5)
        #
        # buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        # buttonBack.grid(row=0, column=4, padx=5, pady=5)
        #
        # # dio stranice s izracunatim vrijednostima haralickovih funkcija
        # parameterFrame = tk.Frame(self)
        # parameterFrame.grid(row=1, column=1, padx=20, pady=20)
        #
        # labelAnglesList = tk.Label(parameterFrame, text="Function values for angles(in rad): ")
        # labelAnglesList.grid(row=0, column=0, padx=10, pady=10)
        #
        # self.labelAnglesListValue = tk.Label(parameterFrame, text="")
        # self.labelAnglesListValue.grid(row=0, column=1, padx=10, pady=10)
        #
        # labelCellNumber = tk.Label(parameterFrame, text="Cell num. ")
        # labelCellNumber.grid(row=1, column=0, padx=10, pady=10)
        #
        # self.labelCellNumberValue = tk.Label(parameterFrame, text="")
        # self.labelCellNumberValue.grid(row=1, column=1, padx=10, pady=10)
        #
        # labelContrast = tk.Label(parameterFrame, text="Contrast: ")
        # labelContrast.grid(row=2, column=0, padx=10, pady=10)
        #
        # self.labelContrastValue = tk.Label(parameterFrame, text="")
        # self.labelContrastValue.grid(row=2, column=1, padx=10, pady=10)
        #
        # labelEnergy = tk.Label(parameterFrame, text="Energy: ")
        # labelEnergy.grid(row=3, column=0, padx=10, pady=10)
        #
        # self.labelEnergyValue = tk.Label(parameterFrame, text="")
        # self.labelEnergyValue.grid(row=3, column=1, padx=10, pady=10)
        #
        # labelHomogeneity = tk.Label(parameterFrame, text="Homogeneity: ")
        # labelHomogeneity.grid(row=4, column=0, padx=10, pady=10)
        #
        # self.labelHomogeneityValue = tk.Label(parameterFrame, text="")
        # self.labelHomogeneityValue.grid(row=4, column=1, padx=10, pady=10)
        #
        # labelEntropy = tk.Label(parameterFrame, text="Entropy: ")
        # labelEntropy.grid(row=5, column=0, padx=10, pady=10)
        #
        # self.labelEntropyValue = tk.Label(parameterFrame, text="")
        # self.labelEntropyValue.grid(row=5, column=1, padx=10, pady=10)