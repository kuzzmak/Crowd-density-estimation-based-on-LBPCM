from os import listdir
from os.path import isfile, join
import os
import cv2 as cv

path = r"C:\Users\kuzmi\Desktop\Crowd_PETS09\S1\L1\Time_13-57\View_001"

def printFiles(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for f in onlyfiles:
        print(f)
        im = cv.imread(path + "\\" + f)
        cv.imshow("test", im)
        cv.waitKey(0)
        cv.destroyAllWindows()

if __name__ == "__main__":
    printFiles(path)