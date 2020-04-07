import tkinter as tk
from Pages import InitializationPage as iP

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        frame = tk.Frame(self)
        frame.place(in_=self, anchor="c", relx=.5, rely=.5)

        welcomeText = "This is the starting screen of the app.\nPlease use with caution!"
        label = tk.Label(frame, text=welcomeText)
        label.pack()

        buttonAgree = tk.Button(frame, text="Agree", command=lambda: controller.show_frame(iP.InitializationPage))
        buttonAgree.pack()