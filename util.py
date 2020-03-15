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
import threading
import concurrent.futures

lbpcm = None
modell = None


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
    """ Funkcija za računanje greške na testnom setu blokova

    :param model: klasifikator koji se ocjenjuje
    :param X_test: vektori značajki testnih blokova
    :param Y_test: prave oznake testnih blokova
    :return: postotak točno klasificiranih blokova
    """

    # labele dobivene klasificiranjem
    predictions = []

    for x in X_test:
        predictions.append(int(model.predict([x])[0]))

    counter = 0

    # ako se prave labele poklapaju s izračunatim onda povečamo brojač
    # točno klasificiranih blokova
    for i in range(predictions.__len__()):
        if predictions[i] == Y_test[i]:
            counter += 1

    return counter / predictions.__len__()

def classifyImage(filename, model, conf, console):
    """ Funkcija za klasifikaciju slike, odnosno svrstavanje svakog bloka slike
    u neki od razreda gustoće mnoštva. Svaka slika se sastoji od 16 blokova
    veličine (192, 144) piksela. Iz svakog bloka se stvori vektor značajki koji
    se nakon toga klasificira pomoću modela, odnosno klasifikatora na temelju
    susjeda ili udaljenosti prema susjedima.

    :param filename: staza do slike koju želimo klasificirati
    :param model: objekt klasifikatora koji radi klasifikaciju svakog bloka slike
    :param conf: konfiguracija prema kojoj se tvori vektor značajki svakog bloka
    :param console: konzola za ispis poruka
    :return: vraća se slika na kojoj je svaki blok u određenoj boji, ovisno o
    razredu gustoće kojem pripada
    """

    # slika na koju se "stavljaju" kvadrati u boji, ovisno o razredu gustoće
    image = cv.imread(filename)
    # ista slika iznad samo u sivoj inačici, služi za stvaranje vektora značajki
    image_gray = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    overlay = image.copy()
    output = image.copy()

    # dohvat parametara za lbpcm
    radius = conf[0]
    glcmDistance = conf[1]
    stepSize = conf[2]
    cellSize = conf[3]
    angles = conf[4]
    numOfNeighbors = conf[5]
    combineDistances = conf[6]
    lbpcm = LBPCM.LBPCM(radius, stepSize, cellSize, angles, glcmDistance, combineDistances)

    # lista labela koje odgovaraju pojedinom bloku na slici
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

    subImages = []

    for y in range(stepY):
        for x in range(stepX):
            subImage = image_gray[y * y_size:(y + 1) * y_size, x * x_size:(x + 1) * x_size]
            subImages.append((subImage, lbpcm, model))

    labels = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for subImage, label in zip(subImages, executor.map(classify, subImages)):
            labels.append(label)

    print(labels)
    # i = 0
    # for y in range(stepY):
    #     for x in range(stepX):
    #
    #         # početna i završna točka trenutnog bloka na slici
    #         start_point = (x * x_size, y * y_size)
    #         end_point = ((x + 1) * x_size, (y + 1) * y_size)
    #
    #         # trenutni blok slike za koji se stvara vektor značajki
    #         subImage = image_gray[y * y_size:(y + 1) * y_size, x * x_size:(x + 1) * x_size]
    #         # vektor značajki trenutnog bloka
    #         subImageFv = lbpcm.getFeatureVector(subImage)
    #         # dodavanje labele u listu labela za koja je dobivena klasifikatorom
    #         labels.append(int(model.predict([subImageFv])[0]))
    #
    #         # bojanje trenutnoh bloka slike ovisno o labeli koju je dobivena
    #         if labels[i] == 0:
    #             cv.rectangle(overlay, start_point, end_point, (127, 255, 0), -1)
    #         elif labels[i] == 1:
    #             cv.rectangle(overlay, start_point, end_point, (255, 255, 0), -1)
    #         elif labels[i] == 2:
    #             cv.rectangle(overlay, start_point, end_point, (255, 165, 0), -1)
    #         elif labels[i] == 3:
    #             cv.rectangle(overlay, start_point, end_point, (255, 69, 0), -1)
    #         else:
    #             cv.rectangle(overlay, start_point, end_point, (255, 0, 0), -1)
    #
    #         i += 1
    #         console.insert(tk.END, "[INFO] " + str(i) + "/16 sub images processed\n")
    #         console.see(tk.END)

    # # intenzitet boje kojoj je svaki blok obojan
    # alpha = 0.5
    # cv.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
    # # reskaliranje slike koja se prikazuje u aplikaciji
    # output = resizePercent(output, 60)

    return output

def classify(subImage):
    fv = subImage[1].getFeatureVector(subImage[0])
    return int(subImage[2].predict([fv])[0])

def shortAngles(angles):
    """ Funkcija za kraći zapis kutova kad ih treba prikazati u aplikaciji,
    ovdje se koristi zapis s dvije najznačajnije znamenke

    :param angles: lista kutova koje treba zaokružiti
    :return: lista zaokruženih kutova
    """

    result = []

    for i in angles:
        result.append(round(i, 2))

    return result

def makeColors(dim):
    """ Funkcija za stvaranje kvadrata u boji koji predstavljaju razine gustoce
    u prozoru za klasifikaciju slike.
    Sličice su spremljene u rgb formatu, međutim kod učitavanja se učitaju
    u bgr formatu

    :param dim: dimenzija pojedinog kvadratića
    :return:
    """

    # direktorij u koji su spremljeni kvadratići
    dir = r"colors"

    # svaka gustoća mnoštva je određene boje
    colors = [(127, 255, 0), (255, 255, 0), (255, 165, 0), (255, 69, 0), (255, 0, 0)]

    for c in range(colors.__len__()):
        rgb = np.zeros((dim[0], dim[1], 3))
        rgb[:, :, 0] = colors[c][0]
        rgb[:, :, 1] = colors[c][1]
        rgb[:, :, 2] = colors[c][2]
        cv.imwrite(dir + "/" + str(c) + ".jpg", rgb)

def greycoprops(P, prop='contrast'):
    """
        Funkcija za izračunavanje Haralickovih funkcija

        f1 -> energy +
        f2 -> contrast +
        f3 -> correlation +
        f4 -> sum of squares: variance
        f5 -> inverse difference moment - homogeneity +
        f6 -> sum average

    :param P: glcm matrica
    :param prop: funkcija koju je potrebno izračunati
    :return: vrijednost funkcije koja se izračunava
    """

    (num_level, num_level2, num_dist, num_angle) = P.shape
    if num_level != num_level2:
        raise ValueError('num_level and num_level2 must be equal.')
    if num_dist <= 0:
        raise ValueError('num_dist must be positive.')
    if num_angle <= 0:
        raise ValueError('num_angle must be positive.')

    # normalize each GLCM
    P = P.astype(np.float64)
    glcm_sums = np.apply_over_axes(np.sum, P, axes=(0, 1))
    glcm_sums[glcm_sums == 0] = 1
    P /= glcm_sums

    mean = np.apply_over_axes(np.sum, P / num_level, axes=(0, 1))
    b = np.apply_over_axes(np.sum, (P - mean) ** 2, axes=(0, 1))
    sigma = np.sqrt(1 / (num_level - 1) * b)

    # create weights for specified property
    I, J = np.ogrid[0:num_level, 0:num_level]
    if prop == 'contrast':
        weights = (I - J) ** 2
    elif prop == 'homogeneity':
        weights = 1. / (1. + (I - J) ** 2)
    elif prop == 'correlation':
        weights = I * J
    elif prop in ['energy', 'entropy']:
        pass
    else:
        raise ValueError('%s is an invalid property' % prop)

    # compute property for each GLCM
    if prop == 'energy':
        results = np.apply_over_axes(np.sum, (P ** 2), axes=(0, 1))[0, 0]
    elif prop == 'entropy':
        results = np.apply_over_axes(np.sum, P, axes=(0, 1))[0, 0]
    elif prop == 'correlation':
        weights = weights.reshape((num_level, num_level, 1, 1))
        results = np.apply_over_axes(np.sum, (P * weights - mean ** 2) / (sigma ** 2), axes=(0, 1))[0, 0]
    elif prop in ['contrast', 'homogeneity']:
        weights = weights.reshape((num_level, num_level, 1, 1))
        results = np.apply_over_axes(np.sum, (P * weights), axes=(0, 1))[0, 0]

    return results

def gradientImage(imagePath):
    """
    Funkcija za izracun gradijenta slike

    :param imagePath: staza do slike na kojoj se gradijent racuna
    :return: izvorna slika, gradijentna slika, gradijent slike u smjeru x, gradijent slike u smjeru y
    """
    img = cv.imread(imagePath, cv.IMREAD_GRAYSCALE)

    sobelx = cv.Sobel(img, -1, 1, 0, ksize=3)
    sobely = cv.Sobel(img, -1, 0, 1, ksize=3)

    sobel = sobelx ** 2 + sobely ** 2

    sobel = np.sqrt(sobel)

    # sobel = cv.Sobel(img, cv.CV_64F, 1, 1, ksize=5)

    return img, sobel, sobelx, sobely
