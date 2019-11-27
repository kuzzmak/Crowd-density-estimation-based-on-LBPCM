from os import listdir
from os.path import isfile, join
import os
import cv2 as cv
import shutil
import numpy as np

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
    # brojac za imana slika
    i = 0
    for f in onlyFiles:
        fileName = path + "\\" + f
        # normalna slika
        im = cv.imread(fileName)
        # slika u sivim tonovima
        im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

        for i in range(4):
            croppedImage = im_gray[i * dim[1]:(i + 1) * dim[1], i * dim[0]:(i + 1) * dim[0]]
            imName = pathToTrainingData + "\\" + str(i) + ".jpg"
            cv.imwrite(imName, croppedImage)
            i += 1
        cv.imshow("test", im)
        cv.waitKey(0)
        cv.destroyAllWindows()

if __name__ == "__main__":
    path = r"C:\Users\kuzmi\Desktop\Crowd_PETS09\S1\L1\Time_13-57\View_001"
    pathToTrainingData = r"data\trainingData"
    pathToTestData = r"data\testData"
    makePictureElements(path, pathToTrainingData, pathToTestData, *(192, 144))