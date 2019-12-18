# from tkinter import Button, Tk, HORIZONTAL
#
# from tkinter.ttk import Progressbar
# import time
# import threading
#
# class MonApp(Tk):
#     def __init__(self):
#         super().__init__()
#
#
#         self.btn = Button(self, text='Traitement', command=self.traitement)
#         self.btn.pack()
#         self.progress = Progressbar(self, orient=HORIZONTAL,length=100,  mode='indeterminate')
#
#
#     def traitement(self):
#         def real_traitement():
#             self.progress.pack()
#             self.progress.start()
#             time.sleep(5)
#             self.progress.stop()
#             self.progress.pack_forget()
#
#             self.btn['state']='normal'
#
#         self.btn['state']='disabled'
#         threading.Thread(target=real_traitement).start()
#
# if __name__ == '__main__':
#
#     app = MonApp()
#     app.mainloop()

# f = open("test.txt", "w")
#
# row1 = "pic1.jpg:1\n"
# row2 = "pic2.jpg:2\n"
#
#
# f.write(row1)
# f.write(row2)

from tkinter import *

import threading # should use the threading module instead!
import queue

import os

class ThreadSafeConsole(Text):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.queue = queue.Queue()
        self.update_me()
    def write(self, line):
        self.queue.put(line)
    def clear(self):
        self.queue.put(None)
    def update_me(self):
        try:
            while 1:
                line = self.queue.get_nowait()
                if line is None:
                    self.delete(1.0, END)
                else:
                    self.insert(END, str(line))
                self.see(END)
                self.update_idletasks()
        except queue.Empty:
            pass
        self.after(100, self.update_me)

# this function pipes input to an widget
def pipeToWidget(input, widget):
    widget.clear()
    while 1:
        line = input.readline()
        if not line:
            break
        widget.write(line)

def funcThread(widget):
    input = os.popen('dir', 'r')
    pipeToWidget(input, widget)



