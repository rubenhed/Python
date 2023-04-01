import tkinter as tk
from GameGUI import gameGUI
import pickle
#import numpy as np
#from load_files import loadSaveData, loadDicom

save_path = r'C:\\Users\\ruben\\OneDrive\\Skrivbord\\Segmenteringsförsök\\Segmentation.seg.nrrd'
dicom_path = r'C:\\Users\\ruben\\OneDrive\\Skrivbord\\Thorax_+C_10_I31f_2_15\\'

#readdata, segment_names, segment_values = loadSaveData(save_path)
#img3d, img_shape = loadDicom(dicom_path)
#img3d = np.stack((img3d,)*3, axis=-1) #makes into rgb

#Saving the objects:
#with open('objs.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
#    pickle.dump([readdata, segment_names, segment_values, img3d, img_shape], f)

# Getting back the objects:
#with open('objs.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
#    readdata, segment_names, segment_values, img3d, img_shape = pickle.load(f)

class menuGUI:

    def __init__(self, canvas):
        self.c = canvas

        NG_button = tk.Button(self.c, text='Start new game', command=self.newGame)
        NG_button.grid(row=0,column=0,pady=5)

    def newGame(self):
        with open('objs.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
            readdata, segment_names, segment_values, img3d, img_shape = pickle.load(f)
        gameGUI(self.c, img3d, segment_names, segment_values, readdata, img_shape)
        #Scrollbar()

