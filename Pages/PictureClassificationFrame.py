import tkinter as tk
import cv2 as cv
from PIL import ImageTk, Image

import util

class PictureClassificationPanel(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        self.labelModelName = tk.Label(self, text="SVM - gray - 0.8%")
        self.labelModelName.pack(padx=10, pady=10)

        blank = cv.imread(controller.app.configuration['blankImagePath'])
        blank = util.resizePercent(blank, 40)
        self.blank = ImageTk.PhotoImage(image=Image.fromarray(blank))
        self.labelImage = tk.Label(self, image=self.blank)
        self.labelImage.pack(padx=10, pady=10)