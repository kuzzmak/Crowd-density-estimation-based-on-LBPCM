import tkinter as tk
from os import listdir
import cv2 as cv
from PIL import ImageTk, Image
import numpy as np
import util
from skimage.feature import local_binary_pattern
from skimage.feature import greycomatrix
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

        buttonCalculate = tk.Button(buttonFrame, text="Calculate function(s)",
                                    command=lambda: self.calculateFunctions(controller))
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

    def calculateFunctions(self, controller):

        controller.console.delete(1.0, tk.END)

        functions = []

        for _, name, c in controller.functionButtons:
            if c.get():
                functions.append(name)

        picType = self.rType.get()
        radius = 1
        stepSize = 32
        cellSize = [64, 64]
        angles = [0, 1.57]
        glcmDistances = [1]

        image = cv.imread(self.currentPicturePath, cv.IMREAD_GRAYSCALE)

        picDim = self.picDims[self.currentCell]
        cellImage = image[picDim[0][0]:picDim[1][0], picDim[0][1]:picDim[1][1]]

        if picType == 'grad':
            sobel = cv.Sobel(cellImage, cv.CV_8U, 1, 1, ksize=3)
            lbp = local_binary_pattern(sobel, 8, 1, method='default')
        else:
            lbp = local_binary_pattern(cellImage, 8, 1, method='default')

        glcm = greycomatrix(lbp.astype(int), glcmDistances, angles, levels=256, normed=True)

        for f in functions:

            result = util.greycoprops(glcm, prop=f)

            string = []
            for t in result:
                string.extend(list(t))

            controller.consolePrint(f + ": " + str(string), dots=False)




