import cv2 as cv
from os import listdir
from os.path import isfile, join
import numpy as np
import util
import skimage.feature

color = (255, 0, 0)
thickness = 2

xy = 64
windowSize = [xy, xy]
stepSize = xy // 2
desired_window_name = "picture"

onlyFiles = [f for f in listdir(r"data\trainingData")]

# for y in range(0, image.shape[0], stepSize):
#     for x in range(0, image.shape[1], stepSize):
#         start_point = (x, y)
#         end_point = (x + windowSize[0], y + windowSize[1])
#         image_copy = cv.rectangle(np.copy(image), start_point, end_point, color, thickness)
#         cv.imshow(desired_window_name, image_copy)
#         cv.waitKey(0)


from tkinter import *
from PIL import ImageTk, Image

pictures = [f for f in listdir(r"data\trainingData")]
picCounter = 0

def nextPic(path):
    """funkcija za dohvat sljedece slike"""
    global picCounter
    global currPicPath
    global currCell
    errorLabel.configure(text="")
    if picCounter < len(pictures):
        fileName = path + "\\" + pictures[picCounter + 1]
        image = cv.imread(fileName)
        root.photo = ImageTk.PhotoImage(image=Image.fromarray(image))
        panelPic.configure(image=root.photo)
        currPicPath = fileName
        picCounter += 1
        currCell = 0
        currPicPath = fileName
    else:
        errorLabel.configure(text="No more images.")

def prevPic(path):
    """funkcija za dohvat prethodne slike"""
    global picCounter
    global currPicPath
    global currCell
    if picCounter > 0:
        fileName = path + "\\" + pictures[picCounter - 1]
        image = cv.imread(fileName)
        root.photo = ImageTk.PhotoImage(image=Image.fromarray(image))
        panelPic.configure(image=root.photo)
        currPicPath = fileName
        picCounter -= 1
        currCell = 0
    else:
        errorLabel.configure(text="No previous images.")

# staza do slike po kojoj se trenutno iterira
currPicPath = r"C:\Users\kuzmi\PycharmProjects\untitled\data\trainingData\0.jpg"
# lista pozicija celije u nekom slikovnom elementu
picDims = []
# indeks trenutne celije
currCell = 0

def nextCell():
    """funkcija za pomicanje na sljedecu celiju u pojedinom slikovnom elementu"""

    global currCell
    # ako nismo stigli do kraja slikovnog elementa
    if currCell < picDims.__len__():
        image = cv.imread(currPicPath)
        # dohvat pocetne i krajnje tocke pojedine celije
        start_point, end_point = picDims[currCell]
        currCell += 1
        # kopija slike kako celija ne bi ostala na slici nakon svake iteracije
        image_copy = cv.rectangle(np.copy(image), start_point, end_point, color, thickness)
        # stvaranje slike iz numpy arraya
        root.img = ImageTk.PhotoImage(image=Image.fromarray(image_copy))
        # postavljanje slike u labelu
        panelPic.configure(image=root.img)
    else:
        errorLabel.configure(text="No further cells remaining.")

def makePicDims(image):
    """funkcija koja sluzi za stvaranje prozora iz kojeg
    se tvori vektor znacajki

    u polju dims su elementi oblika (start_point, end_point), a koji
    oznacavaju lijevi desni i desni donji kut celije koje se koristi
    za stvaranje vektora znacajki
    """

    dims = []
    for y in range(0, image.shape[0] - stepSize, stepSize):
        for x in range(0, image.shape[1] - stepSize, stepSize):
            start_point = (x, y)
            end_point = (x + windowSize[0], y + windowSize[1])
            dims.append((start_point, end_point))
    return dims

# pocetni prozor
root = Tk()
root.title("App")
# staza do slika za treniranje
picPath = r"data\trainingData"

# inicijalizacija prvog slikovnog elementa
initialImage = cv.imread(currPicPath)
img = ImageTk.PhotoImage(image=Image.fromarray(initialImage))
picDims = makePicDims(initialImage)

# gornji frame
frameUp = Frame(root)
frameUp.pack()

# labela IMAGE
picLbl = Label(frameUp, text="IMAGE")
picLbl.pack(padx=10, pady=2)

# labela za ispis errora
errorLabel = Label(frameUp, text="")
errorLabel.pack()

# labela za prikaz slike
panelPic = Label(frameUp, image=img)
panelPic.pack(padx=10, pady=10, fill=BOTH)

# donji frame
frameDown = Frame(root)
frameDown.pack(side=BOTTOM)

buttonOK = Button(frameDown, text="NextPic", command=lambda: nextPic(picPath))
buttonOK.pack(padx=5, pady=5, side=RIGHT)

buttonPrev = Button(frameDown, text="PrevPic", command=lambda: prevPic(picPath))
buttonPrev.pack(padx=5, pady=5, side=LEFT)

buttonNextCell = Button(frameDown, text="NextCell", command=nextCell)
buttonNextCell.pack(padx=5, pady=5, side=LEFT)

root.mainloop()
