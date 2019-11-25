import cv2 as cv
from skimage.feature import local_binary_pattern


def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield (image[y:y + windowSize[1], x:x + windowSize[0]])


# radijus oko centralnog piksela
radius = 1;
# broj piksela u susjedstvu
no_points = 8 * radius

# velicina klizeceg prozora
xy = 64
windowSize = [xy, xy]
# velicina koraka
stepSize = xy // 2

cv.namedWindow("output", cv.WINDOW_NORMAL)
im = cv.imread(r"C:\Users\kuzmi\Desktop\frame_0100.jpg")
im_gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

i = 0
for im in sliding_window(im_gray, stepSize, windowSize):
    lbp = local_binary_pattern(im, no_points, radius, method='default')
    imName = r"data\im" + str(i) + ".jpg"
    lbpName = r"data\lbp" + str(i) + ".jpg"
    cv.imwrite(imName, im)
    cv.imwrite(lbpName, lbp)
    i += 1
    print(str(i))
    # print(lbp)
    # imS = cv.resize(lbp, (256, 256))
    # cv.imshow("output", imS)
    # cv.waitKey(0)
    # cv.destroyAllWindows()




