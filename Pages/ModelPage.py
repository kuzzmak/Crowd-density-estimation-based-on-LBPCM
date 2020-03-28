import tkinter as tk
from os import listdir
import Writer
import util
from sklearn.externals import joblib
from PIL import ImageTk, Image

class ModelPage(tk.Frame):

    def __init__(self, parent, upperFrame, controller):

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        self.currentGrayModel = 0
        self.currentGradModel = 0
        self.modelType = tk.StringVar()
        self.modelType.set('gray')

        # dohvat svih .pkl imena
        models = [x for x in listdir(controller.app.configuration["grayModelsPath"]) if x.endswith('.pkl')]
        # id-jevi modela sa sivim slikama
        self.grayModels = [int(x.split('.')[0]) for x in models]

        models = [x for x in listdir(controller.app.configuration["gradModelsPath"]) if x.endswith('.pkl')]
        # id-jevi modela s gradijentnim slikama
        self.gradModels = [int(x.split('.')[0]) for x in models]

        # broj modela koji koristi sive ili gradijentne slike, koristi se kod brojača za trenutni prikazani model
        self.numberOfGrayModels = len(self.grayModels)
        self.numberOfGradModels = len(self.gradModels)
        # razred za učitavanje modela i konfiguracije modela
        self.writer = Writer.Writer()

        # lijevi panel sa selekcijom modela
        selectFrame1 = tk.Frame(self)
        selectFrame1.pack(side="left")

        rDescription = tk.Label(selectFrame1, text="Select classifier type")
        rDescription.pack(pady=5)

        # frame sa selekcijom vrste modela
        frameRadioGrayGrad = tk.Frame(selectFrame1)
        frameRadioGrayGrad.pack()

        rGray = tk.Radiobutton(frameRadioGrayGrad, text="Gray", variable=self.modelType, value='gray',
                               command=lambda: self.loadModelInfo())
        rGray.pack(side="left", padx=10)

        rGrad = tk.Radiobutton(frameRadioGrayGrad, text="Grad", variable=self.modelType, value='grad',
                               command=lambda: self.loadModelInfo())
        rGrad.pack(side="left", padx=10)

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

        errorLabel = tk.Label(nameFrame, text="error:")
        errorLabel.grid(row=11, sticky="e")

        self.errorLabelValue = tk.Label(valueFrame, text="")
        self.errorLabelValue.grid(row=11, sticky="w")

        frameButtonPrevNext = tk.Frame(selectFrame1)
        frameButtonPrevNext.pack()

        self.currentModelLabel = tk.Label(frameButtonPrevNext, text="")
        self.currentModelLabel.pack()

        self.modelStatusFrame = tk.Frame(frameButtonPrevNext)
        self.modelStatusFrame.pack()

        im = Image.open(controller.app.configuration["xMarkPath"])
        im = im.resize((20, 20), Image.ANTIALIAS)
        self.im = ImageTk.PhotoImage(im)

        self.imageLabel = tk.Label(self.modelStatusFrame, image=self.im)
        self.imageLabel.pack(side="left", padx=5, pady=5)

        self.imageLabelDescription = tk.Label(self.modelStatusFrame, text="model not loaded")
        self.imageLabelDescription.pack(side="left", padx=5, pady=5)

        buttonPrev = tk.Button(frameButtonPrevNext, text="Previous")
        buttonPrev.pack(side="left", padx=10, pady=5, fill="x")

        buttonLoadModel = tk.Button(frameButtonPrevNext, text="Load model", command=lambda: self.loadModel(
            controller, upperFrame))
        buttonLoadModel.pack(side="left", padx=10, pady=5, fill="x")

        buttonNext = tk.Button(frameButtonPrevNext, text="Next", command=lambda: self.nextModel(self.modelType.get()))
        buttonNext.pack(side="left", padx=10, pady=5, fill="x")

        self.loadModelInfo()

    def loadModelInfo(self):
        """
        Funkcija za učitavanje i prikazivanje konfiguracije dostupnih modela
        """

        modelType = self.modelType.get()

        if modelType == 'gray':

            if len(self.gradModels) > 0:
                self.currentModelLabel.configure(text="Current model: " + str(self.currentGrayModel + 1) +
                                                      "/" + str(self.numberOfGrayModels))
                modelId = self.grayModels[self.currentGrayModel]
            else:
                # ako nema nikakvog modela sa sivim slikama
                self.currentModelLabel.configure(text="Current model: 0/0")
                modelId = -1

        else:

            if len(self.gradModels) > 0:
                self.currentModelLabel.configure(text="Current model: " + str(self.currentGradModel + 1) +
                                                      "/" + str(self.numberOfGradModels))
                modelId = self.gradModels[self.currentGradModel]
            else:
                self.currentModelLabel.configure(text="Current model: 0/0")
                modelId = -1

        self.showInfo(modelId)

    def loadModel(self, controller, upperFrame):
        """
        Funkcija za učitavanje trenutno izabranog modela

        :param upperFrame:
        :param controller: referenca do glavnog programa
        """

        modelType = self.modelType.get()

        if modelType == 'gray':
            modelPath = controller.app.configuration["grayModelsPath"] + "/" + str(self.grayModels[self.currentGrayModel]) + ".pkl"
            self.writer.model = joblib.load(modelPath)

        else:
            modelPath = controller.app.configuration["gradModelsPath"] + "/" + str(self.gradModels[self.currentGradModel]) + ".pkl"
            self.writer.model = joblib.load(modelPath)

        if upperFrame.numberOfModels.get() == 1 and upperFrame.modelPages[0].writer.model != []:
            upperFrame.buttonSelectPicture['state'] = 'normal'

        if upperFrame.numberOfModels.get() == 2 \
                and upperFrame.modelPages[0].writer.model != [] \
                and upperFrame.modelPages[1].writer.model != []:
            upperFrame.buttonSelectPicture['state'] = 'normal'

        im = Image.open(controller.app.configuration["checkMarkPath"])
        im = im.resize((20, 20), Image.ANTIALIAS)
        self.im = ImageTk.PhotoImage(im)

        self.imageLabel.configure(image=self.im)
        self.imageLabelDescription.configure(text="model loaded")

    def showInfo(self, modelId):
        """
        Ova funkcija prikazuje detalje konfiguracije modela kojem je id modelId

        :param modelId: id modela čija se konfiguracija prikazuje
        """

        if modelId != -1:
            classifierType, \
            picType, \
            lbpRadius, \
            glcmDistances, \
            stepSize, \
            cellSize, \
            angles, \
            numberOfNeighbors, \
            combineDistances, \
            combineAngles, \
            functions, \
            mean, \
            sigma, \
            error = self.writer.loadConfFromJSON(modelId)

            fun = []

            for f in functions:
                if f == 'angular second moment':
                    fun.append('f1')
                elif f == 'contrast':
                    fun.append('f2')
                elif f == 'correlation':
                    fun.append('f3')
                elif f == 'sum of squares: variance':
                    fun.append('f4')
                elif f == 'inverse difference moment':
                    fun.append('f5')
                elif f == 'sum average':
                    fun.append('f6')
                elif f == 'sum variance':
                    fun.append('f7')
                elif f == 'sum entropy':
                    fun.append('f8')
                elif f == 'entropy':
                    fun.append('f9')
                elif f == 'difference variance':
                    fun.append('f10')
                elif f == 'difference entropy':
                    fun.append('f11')

            self.classifierTypeLabelValue.configure(text=classifierType)
            self.picTypeLabelValue.configure(text=picType)
            self.radiusLabelValue.configure(text=lbpRadius)
            self.glcmDistancesLabel.configure(text=glcmDistances)
            self.stepSizeLabelValue.configure(text=stepSize)
            self.cellSizeLabelValue.configure(text=cellSize)
            self.anglesLabelValue.configure(text=util.shortAngles(angles))
            self.numOfNeighborsLabelValue.configure(text=numberOfNeighbors)
            self.combineDistancesLabelValue.configure(text=combineDistances)
            self.combineAnglesLabelValue.configure(text=combineAngles)
            self.functionsLabelValue.configure(text=fun)
            self.errorLabelValue.configure(text=round(error, 2))

        else:
            # slučaj kada nema niti jednog modela
            self.classifierTypeLabelValue.configure(text="NO MODEL")
            self.picTypeLabelValue.configure(text="NO MODEL")
            self.radiusLabelValue.configure(text="NO MODEL")
            self.glcmDistancesLabel.configure(text="NO MODEL")
            self.stepSizeLabelValue.configure(text="NO MODEL")
            self.cellSizeLabelValue.configure(text="NO MODEL")
            self.anglesLabelValue.configure(text="NO MODEL")
            self.numOfNeighborsLabelValue.configure(text="NO MODEL")
            self.combineDistancesLabelValue.configure(text="NO MODEL")
            self.combineAnglesLabelValue.configure(text="NO MODEL")
            self.functionsLabelValue.configure(text="NO MODEL")
            self.errorLabelValue.configure(text="NO MODEL")

    def nextModel(self, modelType):
        """
        Služi za prkikaz konfiguracije sljedećeg modela tipa modelType

        :param modelType: vrsta modela
        """

        if modelType == 'gray':

            next = self.currentGrayModel + 1
            if next >= self.numberOfGrayModels:
                next %= self.numberOfGrayModels
                self.currentGrayModel = next
                self.loadModelInfo()
            else:
                self.currentGrayModel = next
                self.loadModelInfo()
        else:

            next = self.currentGradModel + 1
            if next >= self.numberOfGradModels:
                next %= self.numberOfGradModels
                self.currentGradModel = next
                self.loadModelInfo()
            else:
                self.currentGradModel = next
                self.loadModelInfo()
