import tkinter as tk
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

        buttonFrame = tk.Frame(self)
        buttonFrame.pack()

        # gumbi
        buttonZero = tk.Button(buttonFrame, text="No flow", command=lambda: controller.annotate('0'))
        buttonZero.grid(row=0, column=0, padx=10, pady=10)

        buttonFreeFlow = tk.Button(buttonFrame, text="Free Flow", command=lambda: controller.annotate('1'))
        buttonFreeFlow.grid(row=0, column=1, padx=10, pady=10)

        buttonRestrictedFlow = tk.Button(buttonFrame, text="Restricted flow", command=lambda: controller.annotate('2'))
        buttonRestrictedFlow.grid(row=0, column=2, padx=10, pady=10)

        buttonDenseFlow = tk.Button(buttonFrame, text="Dense flow", command=lambda: controller.annotate('3'))
        buttonDenseFlow.grid(row=0, column=3, padx=10, pady=10)

        buttonJammedFlow = tk.Button(buttonFrame, text="Jammed flow", command=lambda: controller.annotate('4'))
        buttonJammedFlow.grid(row=0, column=4, padx=10, pady=10)

        frameNav = tk.Frame(self)
        frameNav.pack(padx=10, pady=10)

        buttonPreviousPic = tk.Button(frameNav, text="Prev pic", command=controller.prevPicAnnotation)
        buttonPreviousPic.grid(row=0, column=0, padx=10, pady=10)

        buttonSave = tk.Button(frameNav, text="Save", command=controller.saveAnnotedData, state="disabled")
        buttonSave.grid(row=0, column=1, padx=10, pady=10)

        buttonBack = tk.Button(frameNav, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.grid(row=0, column=2, padx=10, pady=10)