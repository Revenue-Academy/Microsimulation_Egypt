import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter.messagebox import showinfo

from tkinter import filedialog

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

from taxcalc import *

from PIL import Image

   
root = tk.Tk()
root.geometry('1500x600')
root.title('The World Bank')
img=Image.open('WB_logo1.png')
img.save('icon.ico', format='ICO', sizes=[(30,30)])
root.iconbitmap('icon.ico')
app = Application(root)
app.mainloop()


