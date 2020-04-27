import tkinter as tk
from tkinter.ttk import Progressbar
import cv2 as cv
import os
import numpy as np
import random
from PIL import Image, ImageTk
import util
from Pages import InitializationPage as iP

class PreprocessPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        labelDescription = tk.Label(self, text="Here you can specify parameters needed for data preprocessing")
        labelDescription.pack(padx=10, pady=10)

        buttonSelectFolder = tk.Button(self, text="Select data folder")
        buttonSelectFolder.pack(padx=10, pady=5)

        middleFrame = tk.Frame(self)
        middleFrame.pack()

        leftFrame = tk.Frame(middleFrame)
        leftFrame.pack(side="left", padx=5, pady=10)

        rightFrame = tk.Frame(middleFrame)
        rightFrame.pack(side="left")

        labelDimX = tk.Label(leftFrame, text="Picture element size x: ")
        labelDimX.grid(row=0, pady=10, sticky="e")

        labelDimY = tk.Label(leftFrame, text="Picture element size y: ")
        labelDimY.grid(row=1, pady=10, sticky="e")

        self.entryX = tk.Entry(rightFrame)
        self.entryX.grid(row=0, pady=6)
        self.entryX.insert(0, 192)

        self.entryY = tk.Entry(rightFrame)
        self.entryY.grid(row=1, pady=6)
        self.entryY.insert(0, 144)

        self.dim = (192, 144)

        buttonSeePicElements = tk.Button(self, text="See on pic", command=lambda: self.seeOnPic(controller))
        buttonSeePicElements.pack(padx=10, pady=10)

        self.labelSeePicElements = tk.Label(self)
        self.labelSeePicElements.pack(padx=10, pady=10)



        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(side="bottom", padx=10, pady=10)

    def seeOnPic(self, controller):
        """ funkcija za prikaz slikovnih elemenata na slici ako su zadane dimenzije
            slikovnih elemenata
        """

        # ako nije izabran folder prvo, nista se dalje ne izvodi
        if controller.app.configuration['rawDataDirectory'] == "":
            controller.consolePrint("[WARNING] please select data folder")
        else:
            data = os.listdir(controller.app.configuration['rawDataDirectory'])
            # slika na kojoj se prikazuju slikovni elementi
            image = cv.imread(os.path.join(controller.app.configuration['rawDataDirectory'], data[0]))

            # ako nisu upisane dimenzije slikovnog elementa
            if self.entryX.get() == "" or self.entryY.get() == "":
                controller.consolePrint("[WARNING] you haven't specifeid dimensions of a picture element")
            else:
                # zeljena sirina slikovnog elementa
                x_size = int(self.entryX.get())
                # zeljena visina slikovnog elementa
                y_size = int(self.entryY.get())
                # sirina slike
                imageX = np.shape(image)[1]
                # visina slike
                imageY = np.shape(image)[0]
                # cjelobrojni broj koraka u x smjeru(koliko je moguce napraviti slikovnih elemenata sa sirinom x_size)
                stepX = imageX // x_size
                # koraci u y smjeru
                stepY = imageY // y_size

                self.dim = (x_size, y_size)

                # stvaranje crta u horizontalnom smjeru
                for x in range(stepX + 1):
                    cv.line(image, (x * x_size, 0), (x * x_size, imageY), (255, 0, 0), 2)

                # stvaranje crta u vertikalnom smjeru
                for y in range(stepY + 1):
                    cv.line(image, (0, y * y_size), (imageX, y * y_size), (255, 0, 0), 2)

                # ako je potrebno promijeniti velicinu slike
                if image.shape[0] > 300:
                    image = util.resizePercent(image, 30)

                # postavljanje slike u labelu
                self.img = ImageTk.PhotoImage(image=Image.fromarray(image))
                self.labelSeePicElements.configure(image=self.img)

            buttonProcess = tk.Button(self, text="Process", command=lambda: self.process(controller))
            buttonProcess.pack(padx=10, pady=10)

    def process(self, controller):
        """ funkcija za stvaranje slikovnih elemenata od slika koje se nalaze u data2 folderu,
            svaki slikovni element je velicine dim i sprema se u processeddata folder nakon
            sto je pretvoren u nijanse sive
        """

        dataDir = controller.app.configuration['rawDataDirectory']

        data = os.listdir(dataDir)

        progressbar = Progressbar(self, orient=tk.HORIZONTAL, length=200, mode='determinate', maximum=len(data))
        progressbar.pack(side="left", padx=10, pady=10)

        # mijesanje slika
        random.shuffle(data)
        # spremanje slika za treniranje
        for f in data:
            fileName = os.path.join(dataDir, f)
            # normalna slika
            im = cv.imread(fileName)
            # # slika u sivim tonovima
            im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
            # spremanje slike
            util.saveImage(im_gray, controller.configuration['processedImagesPath'], self.dim)
            progressbar.step()

        progressbar['value'] = 0
