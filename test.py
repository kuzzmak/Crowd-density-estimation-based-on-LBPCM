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