import cv2 as cv
from os import listdir
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

color = (255, 0, 0)
thickness = 2

# stranica kvadrata celije
xy = 64
windowSize = [xy, xy]
# velicina koraka u x, y smjeru kod klizeceg prozora
stepSize = xy // 2
# lista slika u datom folderu
pictures = [f for f in listdir(r"data\trainingData")]
# brojac za dohvat slike iz polja slikovnih elemenata koja se trenutno prikazuje
picCounter = 0

trainingFolderPath = ""
testFolderPath = ""


# def nextPic(path):
#     """funkcija za dohvat sljedece slike"""
#
#     global picCounter, currPicPath, currCell
#     # brisanje eventualnih prethodnih poruka
#     errorLabel.configure(text="")
#     # ako ima jos slikovnih elemenata
#     if picCounter < len(pictures):
#         fileName = path + "\\" + pictures[picCounter + 1]
#         image = cv.imread(fileName)
#         root.photo = ImageTk.PhotoImage(image=Image.fromarray(image))
#         panelPic.configure(image=root.photo)
#         currPicPath = fileName
#         picCounter += 1
#         # resetiranje brojaca celije
#         currCell = 0
#     else:
#         pass
#         # errorLabel.configure(text="No more images.")
#
# def prevPic(path):
#     """funkcija za dohvat prethodne slike"""
#
#     global picCounter, currPicPath, currCell
#     # errorLabel.configure(text="")
#     if picCounter > 0:
#         fileName = path + "\\" + pictures[picCounter - 1]
#         image = cv.imread(fileName)
#         root.photo = ImageTk.PhotoImage(image=Image.fromarray(image))
#         panelPic.configure(image=root.photo)
#         currPicPath = fileName
#         picCounter -= 1
#         currCell = 0
#     else:
#         pass
#         # errorLabel.configure(text="No previous images.")
#

#
# def nextCell():
#     """funkcija za pomicanje na sljedecu celiju u pojedinom slikovnom elementu"""
#
#     global currCell
#     # ako nismo stigli do kraja slikovnog elementa
#     if currCell < picDims.__len__():
#         image = cv.imread(currPicPath)
#         # dohvat pocetne i krajnje tocke pojedine celije
#         start_point, end_point = picDims[currCell]
#         currCell += 1
#         # kopija slike kako celija ne bi ostala na slici nakon svake iteracije
#         image_copy = cv.rectangle(np.copy(image), start_point, end_point, color, thickness)
#         # stvaranje slike iz numpy arraya
#         root.img = ImageTk.PhotoImage(image=Image.fromarray(image_copy))
#         # postavljanje slike u labelu
#         panelPic.configure(image=root.img)
#     else:
#         pass
#         # errorLabel.configure(text="No further cells remaining.")

# def createWindow():
#     # pocetni prozor
#     window = Toplevel(root)
#     window.title("Window")
#
#     # inicijalizacija prvog slikovnog elementa
#     initialImage = cv.imread(currPicPath)
#     img = ImageTk.PhotoImage(image=Image.fromarray(initialImage))
#     picDims = makePicDims(initialImage)
#
#     # gornji frame
#     frameUp = Frame(root)
#     frameUp.pack()
#
#     # labela IMAGE
#     picLbl = Label(frameUp, text="IMAGE")
#     picLbl.pack(padx=10, pady=2)
#
#     # labela za ispis errora
#     errorLabel = Label(frameUp, text="")
#     errorLabel.pack()
#
#     # labela za prikaz slike
#     panelPic = Label(frameUp, image=img)
#     panelPic.pack(padx=10, pady=10, fill=BOTH)
#
#     # donji frame
#     frameDown = Frame(root)
#     frameDown.pack(side=BOTTOM)
#
#     # gumbi
#     buttonOK = Button(frameDown, text="NextPic", command=lambda: nextPic(picPath))
#     buttonOK.pack(padx=5, pady=5, side=RIGHT)
#
#     buttonPrev = Button(frameDown, text="PrevPic", command=lambda: prevPic(picPath))
#     buttonPrev.pack(padx=5, pady=5, side=LEFT)
#
#     buttonNextCell = Button(frameDown, text="NextCell", command=nextCell)
#     buttonNextCell.pack(padx=5, pady=5, side=LEFT)
#
#     buttonNewWindow = Button(frameDown, text="NewWindow", command=createWindow)
#     buttonNewWindow.pack(padx=5, pady=5, side=RIGHT)
#



# root = Tk()
# root.title("App")
#
# buttonTraining = Button(root, text="Select folder for training", command=lambda: selectFolder("train"))
# buttonTraining.pack(padx=10, pady=10)
#
# buttonTest = Button(root, text="Select folder for test", command=lambda: selectFolder("test"))
# buttonTest.pack(padx=10, pady=10)
#
# buttonOpen = Button(root, text="Open", command=createWindow)
# buttonOpen.pack(padx=10, pady=10)
#
# root.mainloop()

# staza do slike po kojoj se trenutno iterira
currPicPath = r"C:\Users\kuzmi\PycharmProjects\untitled\data\trainingData\0.jpg"
# lista pozicija celije u nekom slikovnom elementu
picDims = []
# indeks trenutne celije
currCell = 0

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        buttonTraining = Button(self, text="Select folder for training")
        buttonTraining.pack(padx=10, pady=10)

        buttonTest = Button(self, text="Select folder for test")
        buttonTest.pack(padx=10, pady=10)

        buttonOpen = Button(self, text="Open", command=createWindow)
        buttonOpen.pack(padx=10, pady=10)


picPath = r"data\trainingData"

def createWindow():
    window = Toplevel(prog)
    frame = Open(window)
    frame.pack()


class Open(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.createWidgets()
        # inicijalizacija prvog slikovnog elementa
        initialImage = cv.imread(currPicPath)
        img = ImageTk.PhotoImage(image=Image.fromarray(initialImage))
        picDims = makePicDims(initialImage)

        self.frameUp = Frame(self)
        self.frameUp.pack()

        # labela za ispis errora
        self.errorLabel = Label(self.frameUp, text="")
        self.errorLabel.pack()

        # labela IMAGE
    def createWidgets(self):
        picLbl = Label(self, text="IMAGE")
        picLbl.pack(padx=10, pady=2)

    def change(self, text):
        self.errorLabel.configure(text=text)

        #
        # # labela za prikaz slike
        # panelPic = Label(frameUp, image=img)
        # panelPic.pack(padx=10, pady=10, fill=BOTH)
        #
        # # donji frame
        # frameDown = Frame(self)
        # frameDown.pack(side=BOTTOM)
        #
        # # gumbi
        # buttonNext = Button(frameDown, text="NextPic")
        # buttonNext.pack(padx=5, pady=5, side=RIGHT)
        #
        # buttonPrev = Button(frameDown, text="PrevPic")
        # buttonPrev.pack(padx=5, pady=5, side=LEFT)
        #
        # buttonNextCell = Button(frameDown, text="NextCell")
        # buttonNextCell.pack(padx=5, pady=5, side=LEFT)


prog = App()
prog.title("Prog")
prog.mainloop()

