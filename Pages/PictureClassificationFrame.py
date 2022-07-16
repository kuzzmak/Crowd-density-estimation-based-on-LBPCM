import os
import tkinter as tk

import cv2 as cv
from PIL import Image, ImageTk

import util

"""
Razred koji predstavlja "panel" u frameu koji se otvori kad je klasifikacija započela.
Taj panel se sastoji od slike koja se klasificira i iznad nje je vrsta modela, vrsta slike
i greška klasifikacije modela.
"""
class PictureClassificationPanel(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        # labela iznad modela gdje piše vrsta modela, vrsta slike i greška klasifikacije
        self.labelModelName = tk.Label(self, text="SVM - gray - 0.8%")
        self.labelModelName.pack(padx=10, pady=10)

        # bijela pozadina slike kad još nije ništa učitano
        blank = cv.imread(os.path.join(controller.app.configuration['iconsDirectory'], 'blankImage.jpg'))
        blank = util.resizePercent(blank, 20)
        self.blank = ImageTk.PhotoImage(image=Image.fromarray(blank))
        self.labelImage = tk.Label(self, image=self.blank)
        self.labelImage.pack(padx=10, pady=10)

