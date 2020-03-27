import tkinter as tk

class CLP2(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

