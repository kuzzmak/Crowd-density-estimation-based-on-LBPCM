from os import listdir
from os.path import isfile, join
import os
import cv2 as cv
import random
import shutil
import math
from skimage.feature import local_binary_pattern
import numpy as np
import LBPCM
import tkinter as tk

# postotak ukupne kolicine slika koji se koristi za treniranje
ratio = 0.7
# brojac za slikovne elemente
picCounter = 0


def saveImage(im, path, dim):
    """ Funkcija za spremanje slikovnih elemenata iz izvorne slike

    :param im: izvorna slika
    :param path: staza do slike koja sluzi za spremanje slikovnih elemenata
    :param dim: dimenzije slikovnog elementa
    :return:
    """

    global picCounter

    # zeljena sirina slikovnog elementa
    x_size = dim[0]
    # zeljena visina slikovnog elementa
    y_size = dim[1]
    # sirina slike
    imageX = im.shape[1]
    # visina slike
    imageY = im.shape[0]
    # cjelobrojni broj koraka u x smjeru(koliko je moguce napraviti slikovnih elemenata sa sirinom x_size)
    stepX = imageX // x_size
    # koraci u y smjeru
    stepY = imageY // y_size

    for y in range(stepY):
        for x in range(stepX):
            croppedImage = im[y * y_size:(y + 1) * y_size, x * x_size:(x + 1) * x_size]
            imName = path + "/" + str(picCounter) + ".jpg"
            cv.imwrite(imName, croppedImage)
            picCounter += 1

def clearDirectory(pathToDirectory):
    """ Funkcija za brisanje sadrzaja direktorija

    :param pathToDirectory: direktorij ciji se sadrzaj brise
    :return:
    """

    for filename in os.listdir(pathToDirectory):
        file_path = os.path.join(pathToDirectory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# def makePictureElements(path, pathToTrainingData, pathToTestData, *dim):
#     # ako ne postoje folderi za treniranje i testiranje, stovre se, a
#     # ako postoje onda se njihov sadrzaj brise
#     if os.path.exists(pathToTrainingData):
#         clearDirectory(pathToTrainingData)
#     else:
#         train = r"data\trainingData"
#         os.mkdir(train)
#     if os.path.exists(pathToTestData):
#         clearDirectory(pathToTestData)
#     else:
#         test = r"data\testData"
#         os.mkdir(test)
#
#     # popis svih slika izvorne velicine
#     onlyFiles = [f for f in listdir(path) if isfile(join(path, f))]
#
#     # mijesanje slika
#     random.shuffle(onlyFiles)
#     # spremanje slika za treniranje
#     for f in range(round(ratio * onlyFiles.__len__())):
#         fileName = path + "\\" + onlyFiles[f]
#         # normalna slika
#         im = cv.imread(fileName)
#         # slika u sivim tonovima
#         im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
#         # spremanje slike
#         saveImage(im_gray, pathToTrainingData, dim)
#
#     # spremanje ostalih slika
#     for f in range(round(ratio * onlyFiles.__len__()), onlyFiles.__len__(), 1):
#         fileName = path + "\\" + onlyFiles[f]
#         im = cv.imread(fileName)
#         im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
#         saveImage(im_gray, pathToTestData, dim)

def sliding_window(image, stepSize, windowSize):
    """ Funkcija koja koristi tehniku klizeceg prozora kako bi
    se generirali slikovni elementi pocetne slike

    :param image: pocetna slika
    :param stepSize: velicina koraka jedne celije
    :param windowSize: dimenzije celije koja putuje
    :return: jedan slikovni element
    """

    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield image[y:y + windowSize[1], x:x + windowSize[0]]

def makePicDims(image, stepSize=32, windowSize=[64, 64]):

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

def resizePercent(image, percent):
    """ Funkcija za reskaliranje slike na percent pocetne velicine

    :param image: slika koja se reskalira
    :param percent: postotak pocetne slike na koji se reskalira
    :return: reskalirana slika
    """

    width = int(image.shape[1] * percent / 100)
    height = int(image.shape[0] * percent / 100)
    dim = (width, height)
    imageResized = cv.resize(image, dim, interpolation=cv.INTER_AREA)
    return imageResized

def normalize(vectors, progressbar, labelprogress):
    """ Funkcija koja sluzi normalizaciji vektora znacajki
    na srednju vrijednost oko nule i jedinicnu standardnu devijaciju

    :param vectors: vektori znacajki koji se trebaju normalizirati
    :return: normalizirani vektori znacajki
    """
    numOfVecs = vectors.__len__()
    dimension = vectors[0].__len__()

    sums = [0] * dimension

    for v in range(numOfVecs):
        for i in range(dimension):
            sums[i] += vectors[v][i]

    mean = [x / numOfVecs for x in sums]

    sigma = [0] * dimension

    for v in range(numOfVecs):
        for i in range(dimension):
            sigma[i] += (vectors[v][i] - mean[i]) ** 2

    sigma = [math.sqrt(1 / (numOfVecs - 1) * x) for x in sigma]

    for i in range(numOfVecs):
        for j in range(dimension):
            vectors[i][j] = (vectors[i][j] - mean[j]) / sigma[j]

        # azuriranje progressbara i brojaca obradjenih vektora
        progressbar.step()
        labelprogress.configure(text=str(i) + "/" + str(numOfVecs))

def calculateError(model, X_test, Y_test):

    predictions = []

    for x in X_test:
        predictions.append(int(model.predict([x])[0]))

    counter = 0
    print("u calculate error metodi")
    print("Y_test")
    print(Y_test)
    print("predictions")
    print(predictions)

    for i in range(predictions.__len__()):
        if predictions[i] == Y_test[i]:
            counter += 1

    return counter / predictions.__len__()

def classifyImage(filename, model, conf, console):

    image = cv.imread(filename)
    image_gray = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    overlay = image.copy()
    output = image.copy()

    radius = conf[0]
    glcmDistance = conf[1]
    stepSize = conf[2]
    cellSize = conf[3]
    angles = conf[4]
    numOfNeighbors = conf[5]
    combine = conf[6]

    lbpcm = LBPCM.LBPCM(radius, stepSize, cellSize, angles, glcmDistance)

    labels = []

    dim = (192, 144)
    # zeljena sirina slikovnog elementa
    x_size = dim[0]
    # zeljena visina slikovnog elementa
    y_size = dim[1]
    # sirina slike
    imageX = image.shape[1]
    # visina slike
    imageY = image.shape[0]
    # cjelobrojni broj koraka u x smjeru(koliko je moguce napraviti slikovnih elemenata sa sirinom x_size)
    stepX = imageX // x_size
    # koraci u y smjeru
    stepY = imageY // y_size

    i = 0
    for y in range(stepY):
        for x in range(stepX):

            start_point = (x * x_size, y * y_size)
            end_point = ((x + 1) * x_size, (y + 1) * y_size)

            subImage = image_gray[y * y_size:(y + 1) * y_size, x * x_size:(x + 1) * x_size]

            subImageFv = lbpcm.getFeatureVector(subImage)

            labels.append(int(model.predict([subImageFv])[0]))

            if labels[i] == 0:
                cv.rectangle(overlay, start_point, end_point, (127, 255, 0), -1)
            elif labels[i] == 1:
                cv.rectangle(overlay, start_point, end_point, (255, 255, 0), -1)
            elif labels[i] == 2:
                cv.rectangle(overlay, start_point, end_point, (255, 165, 0), -1)
            elif labels[i] == 3:
                cv.rectangle(overlay, start_point, end_point, (255, 69, 0), -1)
            else:
                cv.rectangle(overlay, start_point, end_point, (255, 0, 0), -1)

            i += 1
            console.insert(tk.END, "[INFO] " + str(i) + "/16 sub images processed\n")
            console.see(tk.END)

    print(labels)
    alpha = 0.5
    cv.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    output = resizePercent(output, 60)

    return output

def shortAngles(angles):

    result = []

    for i in angles:
        result.append(round(i, 2))

    return result

def makeColors(dim):

    dir = r"colors"

    colors = [(127, 255, 0), (255, 255, 0), (255, 165, 0), (255, 69, 0), (255, 0, 0)]

    for c in range(colors.__len__()):
        rgb = np.zeros((dim[0], dim[1], 3))
        rgb[:, :, 0] = colors[c][0]
        rgb[:, :, 1] = colors[c][1]
        rgb[:, :, 2] = colors[c][2]
        cv.imwrite(dir + "/" + str(c) + ".jpg", rgb)