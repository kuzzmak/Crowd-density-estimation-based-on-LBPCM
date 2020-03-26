import tkinter as tk
import Pages.InitializationPage as iP
import Pages.ModelPage as mp

class FVC2Page(tk.Frame):

    def __init__(self, parent, controller):

        self.numberOfModels = tk.IntVar()
        self.numberOfModels.set(1)

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        numOfModelsFrame = tk.Frame(self, bg="blue")
        numOfModelsFrame.grid(row=0)

        numOfModelsLabel = tk.Label(numOfModelsFrame, text="Select number of models to be used for classification.")
        numOfModelsLabel.pack(pady=5)

        rButtonFrame = tk.Frame(numOfModelsFrame)
        rButtonFrame.pack()

        rOne = tk.Radiobutton(rButtonFrame, text="One", variable=self.numberOfModels, value=1,
                              command=lambda: self.showModelsPanel(controller))
        rOne.pack(side="left", padx=10, pady=5)

        rTwo = tk.Radiobutton(rButtonFrame, text="Two", variable=self.numberOfModels, value=2,
                              command=lambda: self.showModelsPanel(controller))
        rTwo.pack(side="left", padx=10, pady=5)

        self.middleFrame = tk.Frame(self)
        self.middleFrame.grid(row=1)

        leftModel = mp.ModelPage(self.middleFrame, controller)
        leftModel.grid(row=0, column=0, padx=10, pady=10)

        buttonBack = tk.Button(self, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.grid(row=2, padx=10, pady=10)

    def showModelsPanel(self, controller):

        numOfModels = self.numberOfModels.get()
        print(numOfModels)

        if numOfModels == 2:

            rightModel = mp.ModelPage(self.middleFrame, controller)
            rightModel.grid(row=0, column=1, padx=10, pady=10)
        else:

            self.middleFrame.destroy()

            self.middleFrame = tk.Frame(self)
            self.middleFrame.grid(row=1)

            leftModel = mp.ModelPage(self.middleFrame, controller)
            leftModel.grid(row=0, column=0, padx=10, pady=10)
