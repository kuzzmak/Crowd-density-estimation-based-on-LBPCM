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
import math
string = "45,90,135, 180"

temp = [math.radians(int(i)) for i in string.split(",")]
print(str(temp))