import tkinter as tk

from Pages import DataAnnotationPage as daP
from Pages import FeatureVectorCreationPage as fvcP
from Pages import FVC2Page as fvc2
from Pages import GradientPage as gP
from Pages import ParameterSettingPage as psP
from Pages import PreprocessPage as pP
from Pages import SlidingWindowPage as swP
from Pages import StartPage as sP


class InitializationPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        # dio s gumbima, srednji dio
        middleFrame = tk.Frame(self)
        middleFrame.pack(padx=10, pady=10, fill="both", expand=1)

        preprocessingFrame = tk.Frame(middleFrame)
        preprocessingFrame.pack(side="left", padx=10, pady=10, expand=1, fill="both")

        parameterFrame = tk.Frame(middleFrame)
        parameterFrame.pack(side="left", padx=10, pady=10, expand=1, fill="both")

        classificationFrame = tk.Frame(middleFrame)
        classificationFrame.pack(side="left", padx=10, pady=10, expand=1, fill="both")

        # donji dio prozora
        buttonFrame = tk.Frame(self)
        buttonFrame.pack(padx=10, pady=10)

        # gumbi processing frame-a----------------------------------------------------
        preprocessingDescription = tk.Label(preprocessingFrame, text="Preprocessing")
        preprocessingDescription.pack(padx=10, pady=10)

        buttonPreprocess = tk.Button(preprocessingFrame, text="Preprocess data",
                                     command=lambda: controller.show_frame(pP.PreprocessPage))

        buttonPreprocess.pack(padx=5, pady=10, fill="x")

        self.buttonDataAnnotation = tk.Button(preprocessingFrame, text="Data Annotation",
                                              command=lambda: [controller.show_frame(daP.DataAnnotationPage),
                                                               controller.frames[daP.DataAnnotationPage].updateDataAnnotationFrame(controller)])

        self.buttonDataAnnotation.pack(padx=10, pady=10, fill="x")

        # gumbi parameter frame-a------------------------------------------------------
        parameterDescription = tk.Label(parameterFrame, text="Parameters")
        parameterDescription.pack(pady=10, padx=10)

        buttonParameters = tk.Button(parameterFrame, text="Parameters",
                                     command=lambda: controller.show_frame(psP.ParameterSettingPage))
        buttonParameters.pack(padx=10, pady=10, fill="x")

        self.buttonSW = tk.Button(parameterFrame, text="Sliding Window",
                                  command=lambda: controller.show_frame(swP.SlidingWindowPage))
        self.buttonSW.pack(padx=10, pady=10, fill="x")

        self.buttonGradient = tk.Button(parameterFrame, text="Gradient",
                                        command=lambda: controller.show_frame(gP.GradientPage))
        self.buttonGradient.pack(padx=10, pady=10, fill="x")

        # gumbi classification frame-a--------------------------------------------------

        classificationDescription = tk.Label(classificationFrame, text="Classification")
        classificationDescription.pack(pady=10, padx=10)

        featureVectorCreation = tk.Button(classificationFrame, text="Feature Vector Creation",
                              command=lambda: controller.show_frame(fvcP.FeatureVectorCreationPage))
        featureVectorCreation.pack(padx=10, pady=10, fill="x")

        classification = tk.Button(classificationFrame, text="Classification",
                              command=lambda: controller.show_frame(fvc2.FVC2Page))
        classification.pack(padx=10, pady=10, fill="x")

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(sP.StartPage))
        buttonBack.pack(padx=10, pady=10, fill="x")