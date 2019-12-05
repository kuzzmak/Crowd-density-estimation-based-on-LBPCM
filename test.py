# import cv2 as cv
# from os import listdir
# from os.path import isfile, join
# import numpy as np
# import util
# import skimage.feature
#
# from win32gui import GetWindowText, GetForegroundWindow
#
#
# from pynput import keyboard
#
# def on_press(key):
#     print('{0} pressed'.format(
#         key))
#     if key == keyboard.Key.space:
#         print("baba")
#         return False
#
#
# def on_release(key):
#     print('{0} release'.format(
#         key))
#     if key == keyboard.Key.esc:
#         cv.destroyAllWindows()
#         return False
#
#
# path = r"C:\Users\kuzmi\Desktop\frame_0100.jpg"
#
# image = cv.imread(path)
# color = (255, 0, 0)
# thickness = 2
#
# xy = 64
# windowSize = [xy, xy]
# stepSize = xy // 2
# desired_window_name = "picture"
#
# current_window = (GetWindowText(GetForegroundWindow()))
#
# onlyFiles = [f for f in listdir(r"data\trainingData")]
# for f in onlyFiles:
#     path2 = r"data\trainingData"
#     fileName = path2 + "\\" + f
#     # normalna slika
#     im = cv.imread(fileName)
#     cv.imshow(desired_window_name, im)
#     current_window = (GetWindowText(GetForegroundWindow()))
#     if current_window == desired_window_name:
#         with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#             listener.join()
#         cv.imshow(desired_window_name, im)
#         cv.waitKey(0)



# for y in range(0, image.shape[0], stepSize):
#     for x in range(0, image.shape[1], stepSize):
#         start_point = (x, y)
#         end_point = (x + windowSize[0], y + windowSize[1])
#         image_copy = cv.rectangle(np.copy(image), start_point, end_point, color, thickness)
#         cv.imshow(desired_window_name, image_copy)
#         cv.waitKey(0)


from tkinter import *
from PIL import ImageTk, Image
from os import listdir
import cv2 as cv

onlyFiles = [f for f in listdir(r"data\trainingData")]
picCounter = 1

def nextPic():
    global picCounter
    picPath = r"data\trainingData"
    if picCounter < len(onlyFiles):
        fileName = picPath + "\\" + onlyFiles[picCounter]
        root.photo = ImageTk.PhotoImage(Image.open(fileName))
        panel.configure(image=root.photo)
        picCounter += 1
        print("Pic counter: " + str(picCounter))
    else:
        picLbl.configure(text="No more images.")


root = Tk()
"""window"""
root.title("App")
""""label"""
# lbl = Label(window, text="Hello", font=("Arial Bold", 25))
# lbl.grid(column=0, row=0)
# # lbl = Label(window, text="Hello")
# """"button"""
# button = Button(window, text='Click me', command=clicked)
# button.grid(row=0, column=2)
# """entry"""
# entry = Entry(window, width=10)
# entry.grid(column=1, row=0)
# entry.focus()





path = r"C:\Users\kuzmi\PycharmProjects\untitled\data\trainingData\0.jpg"
img = ImageTk.PhotoImage(Image.open(path))
# img = PhotoImage(file=r"C:\Users\kuzmi\PycharmProjects\untitled\data\trainingData\0.jpg")
picLbl = Label(root, text="IMAGE")
picLbl.pack(padx=10, pady=2)
panel = Label(root, image=img)
panel.pack(padx=10, pady=10, side=LEFT)

button = Button(root, text="Next", command=nextPic)
button.pack(side=RIGHT)

root.mainloop()