
# X = [[0], [1], [2], [3]]
# y = [0, 0, 1, 1]
# from sklearn.neighbors import KNeighborsClassifier
# neigh = KNeighborsClassifier(n_neighbors=3)
# neigh.fit(X, y)
#
# print(neigh.predict([[1.1]]))
#
# print(neigh.predict_proba([[1.1]]))


# import cv2 as cv
#
# picCounter = 0
#
# # funkcija za rezanje slike u 4 dijela i spremanje
# def saveImage(im, dim):
#
#     global picCounter
#
#     # zeljena sirina slikovnog elementa
#     x_size = dim[0]
#     # zeljena visina slikovnog elementa
#     y_size = dim[1]
#     # sirina slike
#     imageX = im.shape[1]
#     # visina slike
#     imageY = im.shape[0]
#     # cjelobrojni broj koraka u x smjeru(koliko je moguce napraviti slikovnih elemenata sa sirinom x_size)
#     stepX = imageX // x_size
#     # koraci u y smjeru
#     stepY = imageY // y_size
#
#     for y in range(stepY):
#         for x in range(stepX):
#             croppedImage = im[y * y_size:(y + 1) * y_size, x * x_size:(x + 1) * x_size]
#             imName = path + "/" + str(picCounter) + ".jpg"
#             cv.imwrite(imName, croppedImage)
#             picCounter += 1





# path = r"C:\Users\kuzmi\Desktop\Crowd_PETS09\S1\L1\Time_13-57\View_001\frame_0000.jpg"
# image = cv.imread(path)
# dimension = (180, 144)
# saveImage(image, dimension)

# dictionary = {}
#
# with open(r"C:\Users\kuzmi\PycharmProjects\untitled\data\labeledData.txt") as f:
#     row = f.read()
#     lines = row.split("")
#
#     for i in lines:
#         if i != "":
#             keyVal = i.split(":")
#             dictionary[keyVal[0]] = keyVal[1]
#
# print(dictionary)
