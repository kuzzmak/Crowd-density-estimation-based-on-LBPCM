import tkinter as tk
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

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(fvcP2.FVC2Page))
        buttonBack.pack(side="bottom", padx=5, pady=5)

    def updateClassificationFrame(self, controller):

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

        # prikaz vrste modela, vrste slike i greške svakog modela na stranici s klasifikacijom
        i = 0
        for p in self.pcpFrames:
            conf = controller.app.writers[i].modelConfiguration
            modelString = conf[0] + " - " + conf[1] + " - " + str(round(conf[13], 2)) + "%"
            p.labelModelName.configure(text=modelString)
            i += 1