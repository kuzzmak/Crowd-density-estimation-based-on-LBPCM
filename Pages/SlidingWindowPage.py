import tkinter as tk
import Pages.InitializationPage as iP

class SlidingWindowPage(tk.Frame):
    """
    Razred gdje se prikazuje funkcionalnost kliznog prozora i vrijednost
    Haralickovih funkcija u odredjenenim celijama slikovnog elementa
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.functionButtons = []

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
        leftPanel.pack(side="left")

        self.labelNormalImage = tk.Label(leftPanel, text="NO IMAGE\nLOADED")
        self.labelNormalImage.pack(padx=10, pady=10)

        self.labelLBPImage = tk.Label(leftPanel, text="NO IMAGE\nLOADED")
        self.labelLBPImage.pack(padx=10, pady=10)

        # frame s gumbima za sljedeću sliku, ćeliju
        buttonFrame = tk.Frame(leftPanel)
        buttonFrame.pack(pady=5)

        buttonNextPicture = tk.Button(buttonFrame, text="Next pic")
        buttonNextPicture.pack(side="left", padx=5, pady=5)

        buttonPreviousPicture = tk.Button(buttonFrame, text="Prev pic")
        buttonPreviousPicture.pack(side="left", padx=5, pady=5)

        buttonNextCell = tk.Button(buttonFrame, text="Next cell")
        buttonNextCell.pack(side="left", padx=5, pady=5)





        # desni panel s gumbima za Haralickove funkcije
        rightPanel = tk.Frame(middleFrame)
        rightPanel.pack(side="left")

        i = 1
        for name, fName, c in controller.functionButtons:
            tk.Checkbutton(rightPanel, text=name + " - " + fName, variable=c).grid(row=i, pady="2", sticky="w")
            i += 1






        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(side="bottom", padx=5, pady=5)

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