import tkinter as tk
import Pages.InitializationPage as iP

class ParameterSettingPage(tk.Frame):
    """ razred gdje se odabiru parametri LBP-a
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="blue")

        description = tk.Label(self, text="Here you select parameters required for LBP.")
        description.pack(pady=5)
        # prvi redak---------------------------
        frame1 = tk.Frame(self)
        frame1.pack(pady=5)

        labelRadius = tk.Label(frame1, text="Specify LBP radius:")
        labelRadius.pack(side="left")
        # upis radijusa
        entryRadius = tk.Entry(frame1)
        entryRadius.pack(side="right")

        # drugi redak--------------------------
        frame2 = tk.Frame(self)
        frame2.pack()

        labelCellSize = tk.Label(frame2, text="Specify cell size, eg. \"64x64\".")
        labelCellSize.pack(side="left")
        # upis velicine celije za klizni prozor
        entryCellSize = tk.Entry(frame2)
        entryCellSize.pack(side="right")

        # treci redak--------------------------
        frame3 = tk.Frame(self)
        frame3.pack(pady=5)

        labelStepSize = tk.Label(frame3, text="Specify step size:")
        labelStepSize.pack(side="left")
        # upis velicine koraka
        entryStepSize = tk.Entry(frame3)
        entryStepSize.pack(side="right")

        frame31 = tk.Frame(self)
        frame31.pack()

        labelAngles = tk.Label(frame31,
                               text="Specify angles(in degrees) for which you'd like to \ncalculate co-occurence matrix(separate them by comma, eg. 45,90,135): ")
        labelAngles.pack(side="left")

        entryAngles = tk.Entry(frame31)
        entryAngles.pack(side="right")

        labelRepresentation = tk.Label(self, text="Loaded image on the left and LBP on the right")
        labelRepresentation.pack()

        self.labelImageName = tk.Label(self, text="")
        self.labelImageName.pack()

        # cetvrti redak---------------------------
        frame4 = tk.Frame(self)
        frame4.pack(padx=10, pady=5)

        self.labelNormalPic = tk.Label(frame4, text="no pic\nselected")
        self.labelNormalPic.grid(row=0, column=0, padx=10, pady=10)

        self.labelLBPPic = tk.Label(frame4, text="select pic\nfirst")
        self.labelLBPPic.grid(row=0, column=1, padx=10, pady=10)

        # peti redak------------------------
        frame5 = tk.Frame(self)
        frame5.pack(pady=5)
        # gumb za spremanje parametara LBP-a
        buttonSave = tk.Button(frame5, text="Save", command=lambda: controller.saveParameters(entryRadius.get(),
                                                                                              entryCellSize.get(),
                                                                                              entryStepSize.get(),
                                                                                              entryAngles.get()))
        buttonSave.pack(padx=10, pady=5, side="left")

        buttonSelectPic = tk.Button(frame5, text="Select img", command=controller.selectImg)
        buttonSelectPic.pack(padx=10, pady=5, side="left")

        self.buttonRefresh = tk.Button(frame5, text="Refresh", state="disabled", command=controller.refreshLBP)
        self.buttonRefresh.pack(padx=10, pady=5, side="left")

        buttonBack = tk.Button(frame5, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(padx=10, pady=5, side="left")
