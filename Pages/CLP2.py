import tkinter as tk

import cv2 as cv
from PIL import ImageTk, Image

import util
from Pages import FVC2Page as fvcP2
from Pages import PictureClassificationFrame as pcp

class CLP2(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        # polje PictureClassificationFramea
        self.pcpFrames = []

        description = tk.Label(self, text="Here you can see classified image.")
        description.pack(side="top", padx=10, pady=20)

        colorFrame = tk.Frame(self)
        colorFrame.pack(side="top")

        self.c0c = ImageTk.PhotoImage(image=Image.fromarray(
            cv.imread(controller.app.configuration['iconsDirectory'] + '/0.jpg')))
        self.c1c = ImageTk.PhotoImage(image=Image.fromarray(
            cv.imread(controller.app.configuration['iconsDirectory'] + '/1.jpg')))
        self.c2c = ImageTk.PhotoImage(image=Image.fromarray(
            cv.imread(controller.app.configuration['iconsDirectory'] + '/2.jpg')))
        self.c3c = ImageTk.PhotoImage(image=Image.fromarray(
            cv.imread(controller.app.configuration['iconsDirectory'] + '/3.jpg')))
        self.c4c = ImageTk.PhotoImage(image=Image.fromarray
        (cv.imread(controller.app.configuration['iconsDirectory'] + '/4.jpg')))

        c0c = tk.Label(colorFrame, image=self.c0c)
        c0c.pack(side="left", padx=5)
        c0cLabel = tk.Label(colorFrame, text="No flow")
        c0cLabel.pack(side="left", padx=5)

        c1c = tk.Label(colorFrame, image=self.c1c)
        c1c.pack(side="left", padx=5)
        c1cLabel = tk.Label(colorFrame, text="Free flow")
        c1cLabel.pack(side="left", padx=5)

        c2c = tk.Label(colorFrame, image=self.c2c)
        c2c.pack(side="left", padx=5)
        c2cLabel = tk.Label(colorFrame, text="Restricted flow")
        c2cLabel.pack(side="left", padx=5)

        c3c = tk.Label(colorFrame, image=self.c3c)
        c3c.pack(side="left", padx=5)
        c3cLabel = tk.Label(colorFrame, text="Dense flow")
        c3cLabel.pack(side="left", padx=5)

        c4c = tk.Label(colorFrame, image=self.c4c)
        c4c.pack(side="left", padx=5)
        c4cLabel = tk.Label(colorFrame, text="Jammed flow")
        c4cLabel.pack(side="left", padx=5)

        # frame s panelima koji sadrže slike za klasifikaciju
        self.middleFrame = tk.Frame(self)
        self.middleFrame.pack(padx=10, pady=10)

        _pcp = pcp.PictureClassificationPanel(self.middleFrame, controller)
        _pcp.pack(side="left", padx=10, pady=10)
        self.pcpFrames.append(_pcp)

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(fvcP2.FVC2Page))
        buttonBack.pack(side="bottom", padx=5, pady=5)

        buttonStartClassification = tk.Button(self, text="Start classification",
                                              command=lambda: controller.app.classify())
        buttonStartClassification.pack(side="bottom", padx=10, pady=10)

    def updateClassificationFrame(self, controller):
        """
        Funkcija za ažuriranje panela sa slikama za klasifikaciju. Pojave se jedna ili dvije
        odabrane slike za klasifikaciju koje se zatim pritiskom na gumb "start classification"
        klasificiraju po razredima gustoće.

        :param controller: referenca do glavnog prozora
        """

        self.pcpFrames = []

        self.middleFrame.destroy()
        self.middleFrame = tk.Frame(self)
        self.middleFrame.pack(padx=10, pady=10)

        _pcp1 = pcp.PictureClassificationPanel(self.middleFrame, controller)
        _pcp1.pack(side="left", padx=10, pady=10)

        if controller.frames[fvcP2.FVC2Page].numberOfModels.get() == 2:

            _pcp2 = pcp.PictureClassificationPanel(self.middleFrame, controller)
            _pcp2.pack(side="left", padx=10, pady=10)

            self.pcpFrames.append(_pcp2)

        self.pcpFrames.append(_pcp1)

        # odabrana slika, postavlja se u oba panela u middleframe
        image = cv.imread(controller.app.pictureToClassify)
        image = util.resizePercent(image, 40)
        self.im = ImageTk.PhotoImage(image=Image.fromarray(image))

        # prikaz vrste modela, vrste slike i greške svakog modela na stranici s klasifikacijom
        i = 0
        for p in self.pcpFrames:
            conf = controller.app.writers[i].modelConfiguration
            # naziv koji se pojavljuje iznad slike koja se klasificira
            modelString = conf[0] + " - " + conf[1] + " - " + str(round(conf[13], 2)) + "%"
            p.labelModelName.configure(text=modelString)
            p.labelImage.configure(image=self.im)
            i += 1