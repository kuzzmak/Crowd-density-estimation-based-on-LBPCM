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
    errorLabel.configure(text="")
    if picCounter < len(pictures):
        fileName = path + "\\" + pictures[picCounter + 1]

        root.photo = ImageTk.PhotoImage(Image.open(fileName))
        panelPic.configure(image=root.photo)
        picCounter += 1
        currPicPath = fileName
        print("Pic counter: " + str(picCounter) + "pic: " + currPicPath)
    else:
        errorLabel.configure(text="No more images.")

def prevPic(path):
    """funkcija za dohvat prethodne slike"""
    global picCounter
    global currPicPath
    global picDims
    if picCounter > 0:
        fileName = path + "\\" + pictures[picCounter - 1]
        root.photo = ImageTk.PhotoImage(Image.open(fileName))
        panelPic.configure(image=root.photo)
        currPicPath = fileName
        print("Pic counter: " + str(picCounter) + "pic: " + currPicPath)
        picCounter -= 1
    else:
        errorLabel.configure(text="No previous images.")


currXCoord = 0
currYCoord = 0
currRow = 0
currColumn = 0

currPicPath = r"C:\Users\kuzmi\PycharmProjects\untitled\data\trainingData\0.jpg"
picDims = []


def nextCell():
    global currXCoord, currYCoord, currRow, currColumn
    start_point = (currXCoord, currYCoord)
    end_point = (currXCoord + windowSize[0], currYCoord + windowSize[1])

    image = cv.imread(currPicPath)

    if currXCoord + stepSize > image.shape[1]:


    currXCoord += stepSize
    currYCoord += stepSize


    image_copy = cv.rectangle(np.copy(image), start_point, end_point, color, thickness)
    root.img = ImageTk.PhotoImage(image=Image.fromarray(image_copy))
    panelPic.configure(image=root.img)

def makePicDims(image):

    dims = []

    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            start_point = (x, y)
            end_point = (x + windowSize[0], y + windowSize[1])
            dims.append((start_point, end_point))
    return dims

# pocetni prozor
root = Tk()
root.title("App")
# staza do slika za treniranje
picPath = r"data\trainingData"

# staza do prve slke za treniranje
path0 = r"C:\Users\kuzmi\PycharmProjects\untitled\data\trainingData\0.jpg"
img = ImageTk.PhotoImage(Image.open(path0))

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
