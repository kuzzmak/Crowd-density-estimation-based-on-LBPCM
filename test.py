import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from skimage.feature import local_binary_pattern

imagePath = r"/home/tonkec/PycharmProjects/Crowd-density-estimation-based-on-LBPCM/data/processedData/21.jpg"

# imagePath = r"/home/tonkec/Desktop/220px-Lenna_(test_image).png"

img = cv.imread(imagePath, cv.IMREAD_GRAYSCALE)

sobelx = cv.Sobel(img, cv.CV_16S, 1, 0, ksize=3)
sobely = cv.Sobel(img, cv.CV_16S, 0, 1, ksize=3)

# sobel1 = np.power(sobelx, 2) + np.power(sobely, 2)
sobel1 = np.abs(sobelx) / 2 + np.abs(sobely) / 2
# sobel1 = np.sqrt(sobel1)


sobel = cv.Sobel(img, cv.CV_8U, 1, 1, ksize=3)

lbp = local_binary_pattern(sobel1, 8, 1, method='default')
print(np.amin(lbp))
print(np.amax(lbp))
print(lbp)
cv.imshow("pic", lbp.astype('uint8'))
cv.waitKey(0)


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