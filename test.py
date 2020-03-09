# import numpy as np
# import cv2 as cv
# from matplotlib import pyplot as plt
#
# imagePath = r"/home/tonkec/PycharmProjects/Crowd-density-estimation-based-on-LBPCM/data/processedData/21.jpg"
#
# img = cv.imread(imagePath, 0)
#
# sobelx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=5)
# sobely = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=5)
#
# plt.subplot(2, 2, 1)
# plt.imshow(img, cmap='gray')
# plt.title('Original')
# plt.xticks([])
# plt.yticks([])
#
# plt.subplot(2, 2, 3)
# plt.imshow(sobelx, cmap='gray')
# plt.title('Sobel X')
# plt.xticks([])
# plt.yticks([])

from tkinter import *

tk = Tk()
Button(tk, text="button1").grid(row=1, column=1, sticky=NSEW)
Button(tk, text="button2").grid(row=1, column=2, sticky=NSEW)
Button(tk, text="button3").grid(row=2, column=1, sticky=NSEW)
Button(tk, text="button4").grid(row=2, column=2, sticky=NSEW)

tk.grid_rowconfigure(0, weight=1)
tk.grid_rowconfigure(3, weight=1)
tk.grid_columnconfigure(0, weight=1)
tk.grid_columnconfigure(3, weight=1)

tk.mainloop()
#
# plt.subplot(2, 2, 4)
# plt.imshow(sobely, cmap='gray')
# plt.title('Sobel Y')
# plt.xticks([])
# plt.yticks([])
#
# sobel = np.power(sobelx, 2) + np.power(sobely, 2)
# sobel  = np.sqrt(sobel)
#
# plt.subplot(2, 2, 2)
# plt.imshow(sobely, cmap='gray')
# plt.title('Sobel')
# plt.xticks([])
# plt.yticks([])
#
# plt.show()