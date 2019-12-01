import cv2 as cv
from skimage.feature import local_binary_pattern
import util

class LBPCM:

    def __init__(self, radius, no_points):
        # udaljenost centralnog piksela
        self.radius = radius
        # broj piksela oko centralnog piksela
        self.no_points = 8 * radius


    def getLBP(self, im_gray):
        return local_binary_pattern(im_gray, self.no_points, self.radius, method='default')


    def getFeatureVector(self, im_gray):
        # velicina klizeceg prozora
        xy = 64
        windowSize = [xy, xy]
        # velicina koraka
        stepSize = xy // 2

        for im in util.sliding_window(self.getLBP(im_gray), stepSize, windowSize):
