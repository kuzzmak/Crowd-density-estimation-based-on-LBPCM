import tkinter as tk
import Pages.GradientPage as gP
import Pages.StartPage as sP
import Pages.ClassificationPage as clP
import Pages.FeatureVectorCreationPage as fvcP
import Pages.DataAnnotationPage as daP
import Pages.ParameterSettingPage as psP
import Pages.PreprocessPage as pP
import Pages.SlidingWindowPage as swP

class InitializationPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        # dio s opisom stranice, najgornji dio stranice
        descriptionFrame = tk.Frame(self)
        descriptionFrame.pack(padx=10, pady=10)

        description = tk.Label(descriptionFrame, text="Here you select training and testing folder.")
        description.pack()

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

        buttonSelectProcessedData = tk.Button(preprocessingFrame, text="Processed data",
                                              command=controller.selectProcessedDataFolder)
        buttonSelectProcessedData.pack(padx=5, pady=10, fill="x")

        self.buttonDataAnnotation = tk.Button(preprocessingFrame, text="Data Annotation", state="disabled",
                                              command=lambda: [controller.show_frame(daP.DataAnnotationPage),
                                                               controller.updateDataAnnotationFrame()])

        self.buttonDataAnnotation.pack(padx=10, pady=10, fill="x")

        # gumbi parameter frame-a------------------------------------------------------
        parameterDescription = tk.Label(parameterFrame, text="Parameters")
        parameterDescription.pack(pady=10, padx=10)

        buttonParameters = tk.Button(parameterFrame, text="Parameters",
                                     command=lambda: controller.show_frame(psP.ParameterSettingPage))
        buttonParameters.pack(padx=10, pady=10, fill="x")

        self.buttonSW = tk.Button(parameterFrame, text="Sliding Window", state="disabled",
                                  command=lambda: controller.show_frame(swP.SlidingWindowPage))
        self.buttonSW.pack(padx=10, pady=10, fill="x")

        self.buttonGradient = tk.Button(parameterFrame, text="Gradient", state="disabled",
                                        command=lambda: controller.show_frame(gP.GradientPage))
        self.buttonGradient.pack(padx=10, pady=10, fill="x")

        # gumbi classification frame-a--------------------------------------------------

        classificationDescription = tk.Label(classificationFrame, text="Classification")
        classificationDescription.pack(pady=10, padx=10)

        buttonFVC = tk.Button(classificationFrame, text="FVC",
                              command=lambda: [controller.show_frame(fvcP.FeatureVectorCreationPage),
                                               controller.showFVCinfo()])
        buttonFVC.pack(padx=10, pady=10, fill="x")

        buttonClassification = tk.Button(classificationFrame, text="Classification",
                                         command=lambda: [controller.show_frame(clP.ClassificationPage),
                                                          controller.loadColors()])
        buttonClassification.pack(padx=10, pady=10, fill="x")

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(sP.StartPage))
        buttonBack.pack(padx=10, pady=10, fill="x")