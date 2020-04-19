import os
import cv2 as cv
import shutil
import numpy as np
import LBPCM
import tkinter as tk
import concurrent.futures
import copy
import json

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

def sliding_window(image, stepSize, windowSize):
    """
    Funkcija koja koristi tehniku klizeceg prozora kako bi
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

def makePicDims(image, stepSize=None, windowSize=None):

    """funkcija koja sluzi za stvaranje prozora iz kojeg
    se tvori vektor znacajki

    u polju dims su elementi oblika (start_point, end_point), a koji
    oznacavaju lijevi desni i desni donji kut celije koje se koristi
    za stvaranje vektora znacajki
    """

    if windowSize is None:
        windowSize = [64, 64]

    if stepSize is None:
        stepSize = 32

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

def normalize(vectors):
    """
    Funkcija koja sluzi normalizaciji vektora znacajki
    na srednju vrijednost oko nule i jedinicnu standardnu devijaciju

    :param vectors: vektori znacajki koji se trebaju normalizirati
    :return: normalizirani vektori znacajki, srednje vrijednosti vektora i standardna devijacija vektora
    """

    numOfVecs, dimension = vectors.shape
    sums = np.apply_over_axes(np.sum, vectors, axes=0)
    sums /= numOfVecs
    sigma = np.apply_over_axes(np.sum, (vectors - sums) ** 2, axes=0)
    sigma = np.sqrt(1 / (numOfVecs - 1) * sigma + 1e-12)
    vectors = (vectors - sums) / sigma

    return vectors, sums, sigma

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

def classifyImage(filename, model, configuration, console=None):
    """ Funkcija za klasifikaciju slike, odnosno svrstavanje svakog bloka slike
    u neki od razreda gustoće mnoštva. Svaka slika se sastoji od 16 blokova
    veličine (192, 144) piksela. Iz svakog bloka se stvori vektor značajki koji
    se nakon toga klasificira pomoću modela, odnosno klasifikatora na temelju
    susjeda ili udaljenosti prema susjedima.

    :param filename: staza do slike koju želimo klasificirati
    :param model: objekt klasifikatora koji radi klasifikaciju svakog bloka slike
    :param configuration: konfiguracija prema kojoj se tvori vektor značajki svakog bloka
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
    picType = configuration[1]
    radius = configuration[2]
    stepSize = configuration[4]
    cellSize = configuration[5]
    angles = configuration[6]
    glcmdistances = configuration[3]
    functions = configuration[10]
    combineAngles = configuration[9]
    combineDistances = configuration[8]

    lbpcm = LBPCM.LBPCM(picType,
                        radius,
                        stepSize,
                        cellSize,
                        angles,
                        glcmdistances,
                        functions,
                        combineDistances,
                        combineAngles)

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

    # tuple podslike, lbpcm i modela
    image_lbpcm_model = []

    # stvaranje podslika i stavljanje u listu radi lakšeg dohvata svake pojedine podslike
    for y in range(stepY):
        for x in range(stepX):
            subImage = image_gray[y * y_size:(y + 1) * y_size, x * x_size:(x + 1) * x_size]
            image_lbpcm_model.append((subImage, copy.deepcopy(lbpcm), copy.deepcopy(model), configuration))

    # pokretanje onoliko novih procesa koliko računalo procesora ima
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for subImage, label in zip(image_lbpcm_model, executor.map(classify, image_lbpcm_model)):
            # izlaz je labela pripadnosti pojedine podslike nekom od razreda gustoće
            labels.append(label)

    i = 0
    for y in range(stepY):
        for x in range(stepX):

            # početna i završna točka trenutnog bloka na slici
            start_point = (x * x_size, y * y_size)
            end_point = ((x + 1) * x_size, (y + 1) * y_size)

            # bojanje trenutnoh bloka slike ovisno o labeli koju je dobivena
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
            if console is not None:
                console.insert(tk.END, "[INFO] " + str(i) + "/16 sub images processed\n")
                console.see(tk.END)

    # intenzitet boje kojoj je svaki blok obojan
    alpha = 0.5
    cv.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
    # reskaliranje slike koja se prikazuje u aplikaciji
    output = resizePercent(output, 40)

    return output

def classify(tuple):
    """
    Funkcija za klasifikaciju liste slika

    :param tuple (podslika, razred LBPCM, model)
    :return: oznaka pripadnosti razredu slike
    """

    subImage = tuple[0]
    lbpcm = tuple[1]
    model = tuple[2]
    # normalizacija
    mean = np.array(tuple[3][11])
    sigma = np.array(tuple[3][12])
    picType = tuple[3][1]

    fv = lbpcm.getFeatureVector(subImage, picType)
    fv -= mean
    fv /= sigma
    label = model.predict([fv])[0]

    return int(label)

def shortAngles(angles):
    """
    Funkcija za kraći zapis kutova kad ih treba prikazati u aplikaciji,
    ovdje se koristi zapis s dvije najznačajnije znamenke

    :param angles: lista kutova koje treba zaokružiti
    :return: lista zaokruženih kutova
    """

    result = []

    for i in angles:
        result.append(round(i, 2))

    return result

def makeColors(dim):
    """
    Funkcija za stvaranje kvadrata u boji koji predstavljaju razine gustoce
    u prozoru za klasifikaciju slike.
    Sličice su spremljene u rgb formatu, međutim kod učitavanja se učitaju
    u bgr formatu

    :param dim: dimenzija pojedinog kvadratića
    :return:
    """

    # direktorij u koji su spremljeni kvadratići
    dir = r"icons/colors"

    # svaka gustoća mnoštva je određene boje
    colors = [(127, 255, 0), (255, 255, 0), (255, 165, 0), (255, 69, 0), (255, 0, 0)]

    for c in range(colors.__len__()):
        rgb = np.zeros((dim[0], dim[1], 3))
        rgb[:, :, 0] = colors[c][0]
        rgb[:, :, 1] = colors[c][1]
        rgb[:, :, 2] = colors[c][2]
        cv.imwrite(dir + "/" + str(c) + ".jpg", rgb)

def gradientImage(imagePath):
    """
    Funkcija za izracun gradijenta slike

    :param imagePath: staza do slike na kojoj se gradijent racuna
    :return: izvorna slika, gradijentna slika, gradijent slike u smjeru x, gradijent slike u smjeru y
    """
    img = cv.imread(imagePath, cv.IMREAD_GRAYSCALE)

    sobelx = cv.Sobel(img, -1, 1, 0, ksize=3)
    sobely = cv.Sobel(img, -1, 0, 1, ksize=3)

    sobel = cv.Sobel(img, cv.CV_8U, 1, 1, ksize=3)

    return img, sobel, sobelx, sobely

def makeConfigurationFile():
    """
    Funkcija za stvaranje konfiguracijske datoteke u kojoj
    su zapisani podatci potrebni za normalno funkcioniranje
    aplikacije
    """

    fileName = 'configuration.json'

    data = {
        'dataDirectory': r'data',
        'rawDataDirectory': r'data/rawData',
        'processedDataDirectory': r'data/processedData',
        'modelsDirectory': r'data/models',
        'grayModelsDirectory': r'data/models/grayModels',
        'gradModelsDirectory': r'data/models/gradModels',
        'iconsDirectory': r'data/icons',
    }

    with open(fileName, 'w') as f:
        json.dump(data, f, indent=4)

def copyFiles():
    """
    Funkcija za kopiranje potrebnih resursa za normalni
    rad aplikacije iz foldera koji dolazi s aplikacijom
    """

    with open('configuration.json') as f:
        configuration = json.load(f)

    mainDir = "_data"

    # kopiranje labela
    shutil.copy(mainDir + '/' + 'labeledData.txt', configuration['modelsDirectory'])

    # kopiranje izvornih slika
    for file in os.listdir(mainDir + '/' + 'rawData'):
        fileName = mainDir + '/' + 'rawData' + '/' + file
        shutil.copy(fileName, configuration['rawDataDirectory'])

    # kopiranje procesiranih slika
    for file in os.listdir(mainDir + '/' + 'processedData'):
        fileName = mainDir + '/' + 'processedData' + '/' + file
        shutil.copy(fileName, configuration['processedDataDirectory'])

    # kopiranje ikona aplikacije
    for file in os.listdir(mainDir + '/' + 'icons'):
        fileName = mainDir + '/' + 'icons' + '/' + file
        shutil.copy(fileName, configuration['iconsDirectory'])