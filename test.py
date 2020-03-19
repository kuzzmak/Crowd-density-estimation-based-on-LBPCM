# import numpy as np
# import cv2 as cv
# from matplotlib import pyplot as plt
# from skimage.feature import local_binary_pattern
#
# imagePath = r"/home/tonkec/PycharmProjects/Crowd-density-estimation-based-on-LBPCM/data/processedData/21.jpg"
#
# # imagePath = r"/home/tonkec/Desktop/220px-Lenna_(test_image).png"
#
# img = cv.imread(imagePath, cv.IMREAD_GRAYSCALE)
#
# sobelx = cv.Sobel(img, cv.CV_16S, 1, 0, ksize=3)
# sobely = cv.Sobel(img, cv.CV_16S, 0, 1, ksize=3)
#
# # sobel1 = np.power(sobelx, 2) + np.power(sobely, 2)
# sobel1 = np.abs(sobelx) / 2 + np.abs(sobely) / 2
# # sobel1 = np.sqrt(sobel1)
#
#
# sobel = cv.Sobel(img, cv.CV_8U, 1, 1, ksize=3)
#
# lbp = local_binary_pattern(sobel1, 8, 1, method='default')
# print(np.amin(lbp))
# print(np.amax(lbp))
# print(lbp)
# cv.imshow("pic", lbp.astype('uint8'))
# cv.waitKey(0)


# import tkinter
#
# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg, NavigationToolbar2Tk)
# # Implement the default Matplotlib key bindings.
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure
#
# import numpy as np
#
#
# root = tkinter.Tk()
# root.wm_title("Embedding in Tk")
#
#
# plt.subplot(2, 2, 1)
# plt.imshow(img, cmap='gray')
# plt.title('Original')
# plt.xticks([])
# plt.yticks([])
#
# fig = Figure(figsize=(5, 4), dpi=100)
# a = fig.add_subplot(111)
# a.imshow(sobelx, cmap='gray')
#
# canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# canvas.draw()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#
#
# def on_key_press(event):
#     print("you pressed {}".format(event.key))
#     key_press_handler(event, canvas, toolbar)
#
#
# canvas.mpl_connect("key_press_event", on_key_press)
#
#
# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate
#
#
# button = tkinter.Button(master=root, text="Quit", command=_quit)
# button.pack(side=tkinter.BOTTOM)
#
# tkinter.mainloop()

# a = np.array([[1, 2, 3], [1, 1, 1], [0, 4, 2]])
# print(a)
#
# print()
# column_sum = np.sum(a, axis=0)
# row_sum = np.sum(a, axis=1)

# meanx = np.sum(row_sum) / len(row_sum)
# print(str(meanx))

# b = np.apply_over_axes(np.sum, (a ** 2), axes=(0, 1))
#
# print(b)

import cv2 as cv
# from skimage.feature import greycomatrix
# from math import radians
# import math
# import util
# #
# #
# filename = r"/home/tonkec/PycharmProjects/Crowd-density-estimation-based-on-LBPCM/data/processedData/21.jpg"
#
# image = cv.imread(filename, cv.IMREAD_GRAYSCALE)
#
# cell = image[0:64, 0:64]
#
# distances = [1, 2]
# angles = [0, radians(90), radians(45)]
#
# # dimension = len(distances) * len(angles)
# #
# # img, sobel, sobelx, sobely = util.gradientImage(filename)
#
# P = greycomatrix(cell.astype(int), distances, angles, levels=256)
#
# s_a = util.greycoprops(P, prop="sum average")
#
# print(s_a)



#
# entropy = util.greycoprops(P, prop='sum average')
#
# print(entropy)



#
# print(glcm)

# import time
#
# start = time.time()
# sums_x = []
# sums_y = []
# #
# for d in range(len(distances)):
#     for a in range(len(angles)):
#         sums_x.append(np.sum(np.sum(glcm[:, :, d, a], axis=0)))
#         sums_y.append(np.sum(np.sum(glcm[:, :, d, a], axis=1)))
#
# mean_x = [x / 256 for x in sums_x]
# mean_y = [y / 256 for y in sums_y]
#
# #
# print(mean_x)
# print(mean_y)
# # mean_y = [y / 256 for y in sums_y]
# #
# sigma_x = [0] * dimension
#
# # sigma_y = [math.sqrt(1 / (256 - 1) * y) for y in sigma_y]
# #
# k = 0
#
# for d in range(len(distances)):
#     for a in range(len(angles)):
#         for i in range(256):
#             for j in range(256):
#                 sigma_x[k] += (glcm[i][j][d][a] - mean_x[k]) ** 2
# #                 sigma_y[k] += (glcm[i][j][d][a] - mean_y[k]) ** 2
# #                 f3[k] += (i * j * glcm[i][i][d][a] - mean_x[k] * mean_y[k]) / (sigma_x[k] * sigma_y[k])
#         k += 1
#
# sigma_x = [math.sqrt(1 / (256 - 1) * x) for x in sigma_x]
# end = time.time()
# print(end - start)
# print(sigma_x)

# a = np.array([[[[1, 2, 3],
#                [2, 2, 2],
#                [3, 3, 3]],
#
#               [[1, 1, 1],
#                [0, 0, 0],
#                [5, 3, 1]]],
#
#               [[[1, 2, 3],
#                 [2, 2, 2],
#                 [3, 3, 3]],
#
#                [[1, 1, 1],
#                 [0, 0, 0],
#                 [5, 3, 1]]]])
#
# column = np.sum(a, axis=(0, 1, 2)) # po stupcu
# row = np.sum(a, axis=(0, 1, 3)) # po redu
# print(row)

# (num_level, num_level2, num_dist, num_angle) = glcm.shape

# start = time.time()

# glcm = glcm.astype(np.float64)
# glcm_sums = np.apply_over_axes(np.sum, glcm, axes=(0, 1))
# glcm_sums[glcm_sums == 0] = 1
# glcm /= glcm_sums
# I, J = np.ogrid[0:num_level, 0:num_level]
# weights = I * J
# weights = weights.reshape((num_level, num_level, 1, 1))
# mean = np.apply_over_axes(np.sum, glcm / num_level, axes=(0, 1))
# b = np.apply_over_axes(np.sum, (glcm - mean) ** 2, axes=(0, 1))
# sigma = np.sqrt(1 / (num_level - 1) * b)
# c = np.apply_over_axes(np.sum, (glcm * weights - mean ** 2) / (sigma ** 2), axes=(0, 1))
# import util
# print(c)
# print(util.greycoprops(glcm, 'correlation'))

# a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# def pxory(k, glcm):
#
#     (num_level, num_level2, num_dist, num_angle) = glcm.shape
#
#     sum = 0
#
#     for d in range(num_dist):
#         for a in range(num_angle):
#             for i in range(1, num_level):
#                 if k - i > 0:
#                     for j in range(k - i, num_level):
#                         sum += glcm[i][j][d][a]
#                 else:
#                     break
#     return sum
# #
# #
# # summ = 0
# #
# for i in range(2, 2 * 256):
#     print(i)
#     summ += pxory(i, glcm)
#
# print(summ)

# import multiprocessing
#
# print(multiprocessing.cpu_count())
#
# a = [1, 2 , 3, 4]
# b = [2]

