import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import os
os.environ["PATH"] += os.pathsep + '/usr/local/texlive/2019/bin/x86_64-linux'

import matplotlib
matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt

figsize = (10, 3)
fontsize = 14

class FD:

    def __init__(self, root):

        window = tk.Toplevel(root)

        # frame s opisom
        notationFrame = tk.Frame(window)
        notationFrame.pack()
        notationFrame.grid_columnconfigure(0, weight=1)



        notationTextRow1 = r'$p(i,j) - (i,j)$th entry in a normalized gray-tone spatial- dependence matrix\\'
        notationTextRow2 = r'$p_x(i) - i$th' + r' entry in the marginal-probability matrix obtained by summing the rows of $p(i,j)\\$'
        notationTextRow3 = r'$N_g$ - number of distinct gray levels in the quantized image'
        notationTextRow4 = r'$p_y(j) = \sum_{i=1}^{N_g}p(i,j)$'
        notationTextRow5 = r'$p_{x+y}(k) = \sum_{i=1}^{N_g} \sum_{j=1}^{N_g} p(i,j)$, $k=$ 2,3,...,$2N_g$; $i+j=k$'
        notationTextRow6 = r'$p_{x-y}(k) = \sum_{i=1}^{N_g} \sum_{j=1}^{N_g} p(i,j)$, $k=$ 0,1,...,$N_g-1$; $|i-j|=k$'

        text = [notationTextRow6,
                notationTextRow5,
                notationTextRow4,
                notationTextRow3,
                notationTextRow2,
                notationTextRow1]

        i = 0
        fig, ax = plt.subplots(figsize=figsize)
        canvas = FigureCanvasTkAgg(fig, master=window)
        fig.patch.set_visible(False)
        ax.patch.set_visible(False)
        ax.axis('off')
        canvas.get_tk_widget().pack(anchor="w", pady=2, padx=5)
        for t in text:
            ax.text(0, i * 0.15, t, fontsize=fontsize)
            i += 1

        f1 = r'Angular second momentum: $f_1 = \sum_{i} \sum_{j} p(i,j)^2$'

        f2 = r'Contrast: \\$f_2 = \displaystyle \sum_{n=0}^{N_g-1}n^2\{\sum_{i=1}^{N_g} \sum_{j=1}^{N_g} p(i,j)\}$'

        functionNotation = [f2, f1]

        figf1, axf1 = plt.subplots(figsize=figsize)
        figf1.patch.set_visible(False)
        axf1.patch.set_visible(False)
        axf1.axis('off')
        canvasf1 = FigureCanvasTkAgg(figf1, master=window)
        canvasf1.get_tk_widget().pack(side="top", fill="both", expand=1)

        i = 0
        for f in functionNotation:
            axf1.text(0, i * 0.2, f, fontsize=fontsize)
            i += 1






        # figf2, axf2 = plt.subplots(figsize=figsize)
        # f2Text = notationTextRow2
        # axf2.text(0, 0, f2Text, fontsize=fontsize)
        # figf2.patch.set_visible(False)
        # axf2.patch.set_visible(False)
        # axf2.axis('off')
        # canvasf2 = FigureCanvasTkAgg(figf2, master=window)
        # canvasf2.get_tk_widget().pack(side="top", fill="both", expand=1)

