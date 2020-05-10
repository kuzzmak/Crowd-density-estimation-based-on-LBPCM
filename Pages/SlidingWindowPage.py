import tkinter as tk
from tkinter import filedialog
from os import listdir
import cv2 as cv
from PIL import ImageTk, Image
import numpy as np

import FunctionDescriptions
import util
from skimage.feature import local_binary_pattern
from skimage.feature import greycomatrix
from Pages import InitializationPage as iP
import Haralick

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

        self.currentPicturePath = ""

        self.processedImages = listdir(controller.app.configuration['processedDataDirectory'])
        if len(self.processedImages) > 0:
            # trenutno prikazana slika u frameu
            self.currentPicturePath = controller.app.configuration['processedDataDirectory'] + "/" + \
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
        leftPanel.grid(row=0, column=0, padx=20, sticky="n")

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

        buttonSelectImage = tk.Button(leftPanel, text="Select image", command=lambda: self.selectImage(controller))
        buttonSelectImage.pack(pady=5)

        # desni panel s gumbima za Haralickove funkcije
        rightPanel = tk.Frame(middleFrame)
        rightPanel.grid(row=0, column=1, padx=20, sticky="e")

        i = 1
        for name, fName, c in controller.functionButtons:
            tk.Checkbutton(rightPanel, text=name + " - " + fName, variable=c).grid(row=i, pady="2", sticky="w")
            i += 1

        buttonCalculate = tk.Button(rightPanel, text="Calculate function(s)",
                                    command=lambda: self.calculateFunctions(controller))
        buttonCalculate.grid(row=15, padx=5, pady=2, sticky="w")

        buttonFunctionDefinitions = tk.Button(rightPanel, text="Function definitions",
                                              command=lambda: FunctionDescriptions.FD(self))
        buttonFunctionDefinitions.grid(row=16, padx=5, pady=2, sticky="w")

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(side="bottom", padx=5, pady=5)

        # frame s unosom parametara
        parameterFrame = tk.Frame(self)
        parameterFrame.pack(padx=10, pady=10, side="bottom")

        labelStepSize = tk.Label(parameterFrame, text="Step size:")
        labelStepSize.pack(side="left", padx=5)

        self.entryStepSize = tk.Entry(parameterFrame, width=5)
        self.entryStepSize.pack(side="left", padx=5)
        self.entryStepSize.insert(0, 32)

        labelCellSize = tk.Label(parameterFrame, text="Cell size:")
        labelCellSize.pack(side="left", padx=5)

        self.entryCellSize = tk.Entry(parameterFrame, width=5)
        self.entryCellSize.pack(side="left", padx=5)
        self.entryCellSize.insert(0, "64x64")

        labelAngles = tk.Label(parameterFrame, text="Angles:")
        labelAngles.pack(side="left", padx=5)

        self.entryAngles = tk.Entry(parameterFrame, width=10)
        self.entryAngles.pack(side="left", padx=5)
        self.entryAngles.insert(0, 0)

        labelDistances = tk.Label(parameterFrame, text="Distances:")
        labelDistances.pack(side="left", padx=5)

        self.entryDistances = tk.Entry(parameterFrame, width=5)
        self.entryDistances.pack(side="left", padx=5)
        self.entryDistances.insert(0, 1)

        self.radius = 1

        if len(self.processedImages) > 0:
            self.updateImages()

    def updateImages(self):

        image = cv.imread(self.currentPicturePath, cv.IMREAD_GRAYSCALE)

        if self.rType.get() == 'gray':
            lbp = local_binary_pattern(image, 8 * self.radius, self.radius, method='default')
        else:
            sobel = cv.Sobel(image, cv.CV_8U, 1, 1, ksize=3)
            lbp = local_binary_pattern(sobel, 8 * self.radius, self.radius, method='default')
            image = sobel

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
            self.currentPicturePath = controller.app.configuration['processedDataDirectory'] + "/" + \
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

            self.currentPicturePath = controller.app.configuration['processedDataDirectory'] + "/" + \
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

    def calculateFunctions(self, controller):
        """
        Funkcija za izračun odabranih Haralickovih funkcija u desno panelu.

        :param controller: referenca do glavnog programa
        """

        controller.console.delete(1.0, tk.END)

        if self.currentPicturePath == "":
            controller.consolePrint("[ERROR] no picture selected")
            return

        self.picType = self.rType.get()
        self.stepSize = int(self.entryStepSize.get())
        self.cellSize = [int(x) for x in self.entryCellSize.get().split('x')]
        self.angles = [int(x) for x in self.entryAngles.get().split(',')]
        self.glcmDistances = [int(x) for x in self.entryDistances.get().split(',')]

        functions = []

        for _, name, c in controller.functionButtons:
            if c.get():
                functions.append(name)

        image = cv.imread(self.currentPicturePath, cv.IMREAD_GRAYSCALE)

        picDim = self.picDims[self.currentCell]
        cellImage = image[picDim[0][0]:picDim[1][0], picDim[0][1]:picDim[1][1]]

        if self.picType == 'grad':
            sobel = cv.Sobel(cellImage, cv.CV_8U, 1, 1, ksize=3)
            lbp = local_binary_pattern(sobel, 8 * self.radius, self.radius, method='default')
        else:
            lbp = local_binary_pattern(cellImage, 8 * self.radius, self.radius, method='default')

        glcm = greycomatrix(lbp.astype(int), self.glcmDistances, self.angles, levels=256, normed=True)

        hf = Haralick.HaralickFeatures(glcm)

        for f in functions:

            result = hf.greycoprops(prop=f)

            string = []
            for t in result:
                string.extend(list(t))

            controller.consolePrint(f + ": " + str(string), dots=False)

    def selectImage(self, controller):
        """
        Funkcija za odabir slike u slidingWidow frame-u

        :param controller: referenca do glavnog programa
        """

        path = filedialog.askopenfilename(initialdir=controller.app.configuration['processedDataDirectory'],
                                          title="Select picture",
                                          filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        if len(path) < 0:
            controller.consolePrint("[WARNING] you did not select any picture")
        else:

            self.currentPicturePath = path
            self.picDims = util.makePicDims(cv.imread(self.currentPicturePath))
            self.updateImages()