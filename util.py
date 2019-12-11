from os import listdir
from os.path import isfile, join
import os
import cv2 as cv
import random
import shutil
from skimage.feature import local_binary_pattern
import numpy as np

# postotak ukupne kolicine slika koji se koristi za treniranje
ratio = 0.7
# brojac za slikovne elemente
picCounter = 0

# funkcija za rezanje slike u 4 dijela i spremanje
def saveImage(im, path, dim):
    global picCounter

    for i in range(4):
        croppedImage = im[i * dim[1]:(i + 1) * dim[1], i * dim[0]:(i + 1) * dim[0]]
        imName = path + "/" + str(picCounter) + ".jpg"
        cv.imwrite(imName, croppedImage)
        picCounter += 1
    print(picCounter)

# funkcija za brisanje sadrzaja direktorija
def clearDirectory(pathToDirectory):
    for filename in os.listdir(pathToDirectory):
        file_path = os.path.join(pathToDirectory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# rezolucjia slika 768 x 576
def makePictureElements(path, pathToTrainingData, pathToTestData, *dim):
    # ako ne postoje folderi za treniranje i testiranje, stovre se, a
    # ako postoje onda se njihov sadrzaj brise
    if os.path.exists(pathToTrainingData):
        clearDirectory(pathToTrainingData)
    else:
        train = r"data\trainingData"
        os.mkdir(train)
    if os.path.exists(pathToTestData):
        clearDirectory(pathToTestData)
    else:
        test = r"data\testData"
        os.mkdir(test)

    # popis svih slika izvorne velicine
    onlyFiles = [f for f in listdir(path) if isfile(join(path, f))]

    # mijesanje slika
    random.shuffle(onlyFiles)
    # spremanje slika za treniranje
    for f in range(round(ratio * onlyFiles.__len__())):
        fileName = path + "\\" + onlyFiles[f]
        # normalna slika
        im = cv.imread(fileName)
        # slika u sivim tonovima
        im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        # spremanje slike
        saveImage(im_gray, dim, pathToTrainingData)

    # spremanje ostalih slika
    for f in range(round(ratio * onlyFiles.__len__()), onlyFiles.__len__(), 1):
        fileName = path + "\\" + onlyFiles[f]
        im = cv.imread(fileName)
        im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        saveImage(im_gray, dim, pathToTestData)

# funkcija za dobivanje slikovnih celija iz polazne slike
# tehnikom kliznog prozora
def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield image[y:y + windowSize[1], x:x + windowSize[0]]

def makePicDims(image, stepSize, windowSize):
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