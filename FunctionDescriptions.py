from tkinter import *
from PIL import ImageTk, Image
import cv2 as cv
import util

class FD:

    def __init__(self, root):

        window = Toplevel(root)

        # frame s opisom
        notationFrame = Frame(window)
        notationFrame.pack()
        notationFrame.grid_rowconfigure(0, weight=1)
        notationFrame.grid_columnconfigure(0, weight=1)

        xscrollbar = Scrollbar(notationFrame, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=E + W)

        yscrollbar = Scrollbar(notationFrame)
        yscrollbar.grid(row=0, column=1, sticky=N + S)

        canvas = Canvas(notationFrame, bd=0, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        canvas.grid(row=0, column=0, sticky=N + S + E + W)

        image = cv.imread("_data/Latex/main.jpg")

        image = util.resizePercent(image, 40)

        img = ImageTk.PhotoImage(image=Image.fromarray(image))

        canvas.create_image(0, 0, image=img, anchor="nw")

        xscrollbar.config(command=canvas.xview)
        yscrollbar.config(command=canvas.yview)

        canvas.config(scrollregion=canvas.bbox(ALL))
        canvas.config(width=992, height=600)

        window.geometry("1020x600")
        window.mainloop()



