from os import listdir
from os.path import isfile, join
import os
import cv2 as cv
import random
import shutil
import numpy as np

# postotak ukupne kolicine slika koji se koristi za treniranje
ratio = 0.7
picCounter = 0

# funkcija za rezanje slike u 4 dijela i spremanje
def saveImage(im_gray, dim, path):
    global picCounter
    for i in range(4):
        croppedImage = im_gray[i * dim[1]:(i + 1) * dim[1], i * dim[0]:(i + 1) * dim[0]]
        imName = path + "\\" + str(picCounter) + ".jpg"
        cv.imwrite(imName, croppedImage)
        picCounter += 1

# rezolucjia slika 768 x 576
def makePictureElements(path, pathToTrainingData, pathToTestData, *dim):
    # shutil.rmtree("data")
    # os.remove(pathToTestData)
    # os.remove(pathToTrainingData)
    # popis svih slika
    onlyFiles = [f for f in listdir(path) if isfile(join(path, f))]
    # ako ne postoje direktoriji za treniranje i testiranje, stvore se
    if not os.path.exists(pathToTrainingData):
        os.mkdir(pathToTrainingData)
    if not os.path.exists(pathToTestData):
        os.mkdir(pathToTestData)


    # mijesanje slika
    random.shuffle(onlyFiles)
    for f in range(round(ratio * onlyFiles.__len__())):
        fileName = path + "\\" + onlyFiles[f]
        # normalna slika
        im = cv.imread(fileName)
        # slika u sivim tonovima
        im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        # spremanje slike
        saveImage(im_gray, dim, pathToTrainingData)

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
            yield (image[y:y + windowSize[1], x:x + windowSize[0]])

class HaralickFeatures:
    def __init__(self, glcm):
        self.glcm = glcm
        self.num_level, _, _, _ = self.glcm.shape
        self.I, self.J = np.ogrid[0:self.num_level, 0:self.num_level]

    def contrast(self):
        weights = (self.I - self.J) ** 2
        weights = weights.reshape((self.num_level, self.num_level, 1, 1))
        results = np.apply_over_axes(np.sum, (self.glcm * weights), axes=(0, 1))[0, 0, 0]
        return results

    def energy(self):
        results = np.apply_over_axes(np.sum, (self.glcm ** 2), axes=(0, 1))[0, 0, 0]
        return results

    def homogeneity(self):
        weights = 1. / (1. + (self.I - self.J) ** 2)
        weights = weights.reshape((self.num_level, self.num_level, 1, 1))
        results = np.apply_over_axes(np.sum, (self.glcm * weights), axes=(0, 1))[0, 0, 0]
        return results

    def entropy(self):
        results = np.apply_over_axes(np.sum, self.glcm, axes=(0, 1))[0, 0, 0]
        return results

if __name__ == "__main__":
    # view1 = r"C:\Users\kuzmi\Desktop\Crowd_PETS09\S1\L1\Time_13-57\View_001"
    # view2 = r"C:\Users\kuzmi\Desktop\Crowd_PETS09\S1\L1\Time_13-57\View_002"
    # view3 = r"C:\Users\kuzmi\Desktop\Crowd_PETS09\S1\L1\Time_13-57\View_003"
    # view4 = r"C:\Users\kuzmi\Desktop\Crowd_PETS09\S1\L1\Time_13-57\View_004"
    #
    #
    # pathToTrainingData = r"data\trainingData"
    # pathToTestData = r"data\testData"
    # makePictureElements(view1, pathToTrainingData, pathToTestData, *(192, 144))
    # makePictureElements(view2, pathToTrainingData, pathToTestData, *(192, 144))
    # makePictureElements(view3, pathToTrainingData, pathToTestData, *(192, 144))
    # makePictureElements(view4, pathToTrainingData, pathToTestData, *(192, 144))
    a = np.arange(24).reshape(2,3,4)
    print(a)
    b = np.apply_over_axes(np.sum, (a ** 2), [0,1])[0,0]
    print(b)