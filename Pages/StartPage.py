import os
import tkinter as tk

from PIL import Image, ImageTk

from Pages import InitializationPage as iP


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(
            self,
            text="Crowd density estimation based on local binary pattern \n"
            "co-occurence matrix - LBPCM",
            font=(
                "Times",
                18,
                "roman"))
        label.pack(side="top", pady=100)

        middleFrame = tk.Frame(self)
        middleFrame.pack(pady=20)

        im1 = Image.open(
            os.path.join(
                controller.app.configuration['iconsDirectory'],
                "s1.png"))
        # im = im.resize((20, 20), Image.ANTIALIAS)
        self.im1 = ImageTk.PhotoImage(im1)

        im1 = tk.Label(middleFrame, image=self.im1)
        im1.pack(side="left", padx=10)

        arrow1 = Image.open(
            os.path.join(
                controller.app.configuration['iconsDirectory'],
                "arrow.png"))
        arrow1 = arrow1.resize((80, 30), Image.ANTIALIAS)
        self.arrow = ImageTk.PhotoImage(arrow1)

        arrow = tk.Label(middleFrame, image=self.arrow)
        arrow.pack(side="left", padx=10)

        im2 = Image.open(
            os.path.join(
                controller.app.configuration['iconsDirectory'],
                "s2.png"))
        self.im2 = ImageTk.PhotoImage(im2)

        im2 = tk.Label(middleFrame, image=self.im2)
        im2.pack(side="left", padx=10)

        arrow2 = tk.Label(middleFrame, image=self.arrow)
        arrow2.pack(side="left", padx=10)

        lbp = tk.Label(
            middleFrame,
            text="LBP = 31",
            font=(
                "Times",
                12,
                "roman"))
        lbp.pack(side="left", padx=10)

        buttonAgree = tk.Button(
            self,
            text="Main screen",
            command=lambda: controller.show_frame(
                iP.InitializationPage))
        buttonAgree.pack(side="bottom", pady=10)
