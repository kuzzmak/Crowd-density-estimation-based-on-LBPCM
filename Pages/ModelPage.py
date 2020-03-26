import tkinter as tk
from os import listdir
import Writer

class ModelPage(tk.Frame):

    def __init__(self, parent, upperFrame, controller):

        self.currentGrayModel = 0
        self.currentGradModel = 0

        self.writer = Writer.Writer()

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        # lijevi panel sa selekcijom modela
        selectFrame1 = tk.Frame(self)
        selectFrame1.pack(side="left")

        rDescription = tk.Label(selectFrame1, text="Select classifier type")
        rDescription.pack(pady=5)

        # frame sa selekcijom vrste modela
        frameRadioGrayGrad = tk.Frame(selectFrame1)
        frameRadioGrayGrad.pack()

        rGray = tk.Radiobutton(frameRadioGrayGrad, text="Gray", variable=upperFrame.modelType, value='gray',
                               command=lambda: self.loadModel(upperFrame, controller))
        rGray.pack(side="left", padx=10)

        rGrad = tk.Radiobutton(frameRadioGrayGrad, text="Grad", variable=upperFrame.modelType, value='grad',
                               command=lambda: self.loadModel(upperFrame, controller))
        rGrad.pack(side="left", padx=10)

        frameButtonPrevNext = tk.Frame(selectFrame1)
        frameButtonPrevNext.pack()

        buttonPrev1 = tk.Button(frameButtonPrevNext, text="Previous")
        buttonPrev1.pack(side="left", padx=10, pady=5, fill="x")

        buttonNext1 = tk.Button(frameButtonPrevNext, text="Next")
        buttonNext1.pack(side="left", padx=10, pady=5, fill="x")

        # frame s parametrima pojedinog modela
        parameterFrame = tk.Frame(selectFrame1)
        parameterFrame.pack()

        nameFrame = tk.Frame(parameterFrame)
        nameFrame.pack(side="left", padx=5, pady=10)

        valueFrame = tk.Frame(parameterFrame)
        valueFrame.pack(side="left", padx=5, pady=10)

        classifierTypeLabel = tk.Label(nameFrame, text="classifier type:")
        classifierTypeLabel.grid(row=0, sticky="e")

        self.classifierTypeLabelValue = tk.Label(valueFrame, text="")
        self.classifierTypeLabelValue.grid(row=0, sticky="w")

        picTypeLabel = tk.Label(nameFrame, text="pic type:")
        picTypeLabel.grid(row=1, sticky="e")

        self.picTypeLabelValue = tk.Label(valueFrame, text="")
        self.picTypeLabelValue.grid(row=1, sticky="w")

        radiusLabel = tk.Label(nameFrame, text="radius:")
        radiusLabel.grid(row=2, sticky="e")

        self.radiusLabelValue = tk.Label(valueFrame, text="")
        self.radiusLabelValue.grid(row=2, sticky="w")

        glcmDistancesLabel = tk.Label(nameFrame, text="glcm distance(s):")
        glcmDistancesLabel.grid(row=3, sticky="e")

        self.glcmDistancesLabel = tk.Label(valueFrame, text="")
        self.glcmDistancesLabel.grid(row=3, sticky="w")

        stepSizeLabel = tk.Label(nameFrame, text="step size:")
        stepSizeLabel.grid(row=4, sticky="e")

        self.stepSizeLabelValue = tk.Label(valueFrame, text="")
        self.stepSizeLabelValue.grid(row=4, sticky="w")

        cellSizeLabel = tk.Label(nameFrame, text="cell size:")
        cellSizeLabel.grid(row=5, sticky="e")

        self.cellSizeLabelValue = tk.Label(valueFrame, text="")
        self.cellSizeLabelValue.grid(row=5, sticky="w")

        anglesLabel = tk.Label(nameFrame, text="angles:")
        anglesLabel.grid(row=6, sticky="e")

        self.anglesLabelValue = tk.Label(valueFrame, text="")
        self.anglesLabelValue.grid(row=6, sticky="w")

        numOfNeighborsLabel = tk.Label(nameFrame, text="num of neighbors:")
        numOfNeighborsLabel.grid(row=7, sticky="e")

        self.numOfNeighborsLabelValue = tk.Label(valueFrame, text="")
        self.numOfNeighborsLabelValue.grid(row=7, sticky="w")

        combineDistancesLabel = tk.Label(nameFrame, text="combine distances:")
        combineDistancesLabel.grid(row=8, sticky="e")

        self.combineDistancesLabelValue = tk.Label(valueFrame, text="")
        self.combineDistancesLabelValue.grid(row=8, sticky="w")

        combineAnglesLabel = tk.Label(nameFrame, text="combine angles:")
        combineAnglesLabel.grid(row=9, sticky="e")

        self.combineAnglesLabelValue = tk.Label(valueFrame, text="")
        self.combineAnglesLabelValue.grid(row=9, sticky="w")

        functionsLabel = tk.Label(nameFrame, text="functions:")
        functionsLabel.grid(row=10, sticky="e")

        self.functionsLabelValue = tk.Label(valueFrame, text="")
        self.functionsLabelValue.grid(row=10, sticky="w")

    def loadModel(self, upperFrame, controller):

        modelType = upperFrame.modelType.get()

        if modelType == 'gray':

            grayDir = controller.grayModelsDirectory

            # dohvat svih .pkl imena
            models = [x for x in listdir(grayDir) if x.endswith('.pkl')]
            # dohvat svih id-ja modela
            models = [int(x.split('.')[0]) for x in models]

            modelId = models[self.currentGrayModel]

            conf = self.writer.loadConfFromJSON(modelId)

            print(conf)

        else:
            pass
