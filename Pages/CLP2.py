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

        self.pcpFrames = []

        self.middleFrame = tk.Frame(self)
        self.middleFrame.pack(padx=10, pady=10)

        _pcp = pcp.PictureClassificationPanel(self.middleFrame, controller)
        _pcp.pack(side="left", padx=10, pady=10)
        self.pcpFrames.append(_pcp)

        buttonStartClassification = tk.Button(self, text="Start classification", command=lambda: controller.app.classify())
        buttonStartClassification.pack(padx=10, pady=10)

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(fvcP2.FVC2Page))
        buttonBack.pack(side="bottom", padx=5, pady=5)

    def updateClassificationFrame(self, controller):

        #TODO popraviti ovo ispod
        if controller.frames[fvcP2.FVC2Page].numberOfModels.get() == 2:

            if len(self.pcpFrames) == 2:
                pass
            else:
                _pcp = pcp.PictureClassificationPanel(self.middleFrame, controller)
                _pcp.pack(side="left", padx=10, pady=10)
                self.pcpFrames.append(_pcp)
        else:

            self.middleFrame.destroy()
            self.middleFrame = tk.Frame(self)
            self.middleFrame.pack(padx=10, pady=10)

            _pcp = pcp.PictureClassificationPanel(self.middleFrame, controller)
            _pcp.pack(side="left", padx=10, pady=10)

            self.pcpFrames = [_pcp]

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