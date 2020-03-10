# import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
#
imagePath = r"/home/tonkec/PycharmProjects/Crowd-density-estimation-based-on-LBPCM/data/processedData/21.jpg"

img = cv.imread(imagePath, 0)

sobelx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=5)
sobely = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=5)
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
import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np


root = tkinter.Tk()
root.wm_title("Embedding in Tk")


plt.subplot(2, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original')
plt.xticks([])
plt.yticks([])

fig = Figure(figsize=(5, 4), dpi=100)
a = fig.add_subplot(111)
a.imshow(sobelx, cmap='gray')

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()