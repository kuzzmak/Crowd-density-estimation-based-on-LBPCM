import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
from Pages import InitializationPage as iP
import util

class GradientPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        pageDescription = tk.Label(self, text="Here you can view gradient images.")
        pageDescription.pack(side="top", padx=10, pady=10)

        pictureFrame = tk.Frame(self)
        pictureFrame.grid_columnconfigure(0, weight=1)
        pictureFrame.grid_rowconfigure(0, weight=1)
        pictureFrame.grid_columnconfigure(1, weight=1)
        pictureFrame.grid_rowconfigure(1, weight=1)
        pictureFrame.pack(padx=10, pady=10, fill="both", expand=1)

        # labela i normalna slika
        normalFrame = tk.Frame(pictureFrame)
        normalFrame.grid(row=0, column=0, padx=10, pady=5)

        normalImageLabel = tk.Label(normalFrame, text="Normal image")
        normalImageLabel.pack(padx=10, pady=10)

        sobelFrame = tk.Frame(pictureFrame)
        sobelFrame.grid(row=0, column=1, padx=10, pady=5)

        sobelImageLabel = tk.Label(sobelFrame, text="Sobel image")
        sobelImageLabel.pack(padx=10, pady=10)

        sobelXFrame = tk.Frame(pictureFrame)
        sobelXFrame.grid(row=1, column=0, padx=10, pady=5)

        sobelXImageLabel = tk.Label(sobelXFrame, text="Sobel_x image")
        sobelXImageLabel.pack(padx=10, pady=10)

        sobelYFrame = tk.Frame(pictureFrame)
        sobelYFrame.grid(row=1, column=1, padx=10, pady=5)

        sobelYImageLabel = tk.Label(sobelYFrame, text="Sobel_y image")
        sobelYImageLabel.pack(padx=10, pady=10)

        # prikaz normalne slike
        figa = Figure(figsize=(2, 1), dpi=100)
        self.a = figa.add_subplot(111)
        self.a.set_yticks([])
        self.a.set_xticks([])
        # self.a.imshow(img, cmap='gray')

        self.canvasa = FigureCanvasTkAgg(figa, master=normalFrame)
        # self.canvasa.draw()
        self.canvasa.get_tk_widget().pack(side="top", fill="both", expand=1)

        # prikaz sobel slike
        figb = Figure(figsize=(2, 1), dpi=100)
        self.b = figb.add_subplot(111)
        self.b.set_yticks([])
        self.b.set_xticks([])
        # self.b.imshow(sobel, cmap='gray')

        self.canvasb = FigureCanvasTkAgg(figb, master=sobelFrame)
        # self.canvasb.draw()
        self.canvasb.get_tk_widget().pack(side="top", fill="both", expand=1)

        # prikaz sobelx slike
        figc = Figure(figsize=(2, 1), dpi=100)
        self.c = figc.add_subplot(111)
        self.c.set_yticks([])
        self.c.set_xticks([])
        # self.c.imshow(sobelx, cmap='gray')

        self.canvasc = FigureCanvasTkAgg(figc, master=sobelXFrame)
        # self.canvasc.draw()
        self.canvasc.get_tk_widget().pack(side="top", fill="both", expand=1)

        # prikaz sobely slike
        figd = Figure(figsize=(2, 1), dpi=100)
        self.d = figd.add_subplot(111)
        self.d.set_yticks([])
        self.d.set_xticks([])
        # self.d.imshow(sobely, cmap='gray')

        self.canvasd = FigureCanvasTkAgg(figd, master=sobelYFrame)
        # self.canvasd.draw()
        self.canvasd.get_tk_widget().pack(side="top", fill="both", expand=1)

        buttonFrame = tk.Frame(self)
        buttonFrame.pack(padx=10, pady=5, fill="both", expand=1)

        buttonSelectPicture = tk.Button(buttonFrame, text="Select picture",
                                        command=lambda: self.selectGradientPicture(controller))
        buttonSelectPicture.pack(side="left", expand=1, padx=10, pady=10)

        buttonBack = tk.Button(buttonFrame, text="Back", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonBack.pack(side="left", expand=1, padx=10, pady=10)

    def selectGradientPicture(self, controller):
        """
        Funkcija za izbor slike na kojoj se primjenjuje operator gradijenta
        """

        filename = filedialog.askopenfilename(
            initialdir=controller.app.configuration['processedImagesPath'],
            title="Select picture",
            filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))

        if len(filename) > 0:

            img, sobel, sobelx, sobely = util.gradientImage(filename)
            # postavljanje normalne slike
            self.a.imshow(img, cmap='gray')
            self.canvasa.draw()

            # postavljanje sobel slike
            self.b.imshow(sobel, cmap='gray')
            self.canvasb.draw()

            # postavljanje sobel_x slike
            self.c.imshow(sobelx, cmap='gray')
            self.canvasc.draw()

            # postavljanje sobel_y slike
            self.d.imshow(sobely, cmap='gray')
            self.canvasd.draw()

        else:
            controller.gui.consolePrint("[WARNING] no image was selected")