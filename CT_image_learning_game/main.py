import tkinter as tk
#from imageGUI import imageGUI
from menuGUI import menuGUI
#import numpy as np
#from load_files import loadSaveData, loadDicom


def onMouseWheel(event):
    event.widget.event_generate('<<MouseWheel>>', x=event.x, y=event.y, time=event.delta)

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(10,10)
    root.geometry('800x800')
    canvas = tk.Canvas(root)
    canvas.pack(fill='both',expand=True)
    canvas.config(background='gray')
    canvas.bind('<MouseWheel>', onMouseWheel)
    menuGUI(canvas)
    #imageGUI(canvas, img3d, segment_names, segment_values, readdata, img_shape)

    root.mainloop()