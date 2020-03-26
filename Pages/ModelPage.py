import tkinter as tk

class ModelPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        # lijevi panel sa selekcijom modela
        selectFrame1 = tk.Frame(self)
        selectFrame1.pack(side="left")
        # frame sa selekcijom vrste modela
        frameRadioGrayGrad = tk.Frame(selectFrame1)
        frameRadioGrayGrad.pack()

        rGray = tk.Radiobutton(frameRadioGrayGrad, text="Gray", variable=controller.modelType, value='gray')
        rGray.pack(side="left", padx=10)

        rGrad = tk.Radiobutton(frameRadioGrayGrad, text="Grad", variable=controller.modelType, value='grad')
        rGrad.pack(side="left", padx=10)

        frameButtonPrevNext = tk.Frame(selectFrame1)
        frameButtonPrevNext.pack()

        buttonPrev1 = tk.Button(frameButtonPrevNext, text="Previous")
        buttonPrev1.pack(side="left", padx=10, pady=5, fill="x")

        buttonNext1 = tk.Button(frameButtonPrevNext, text="Next")
        buttonNext1.pack(side="left", padx=10, pady=5, fill="x")