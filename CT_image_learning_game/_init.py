import tkinter as tk
import threading
import numpy as np


def init(self, canvas, img3d, segment_names, segment_values, readdata, img_shape):
    self.c = canvas
    self.current_img_array = img3d
    self.segment_names = segment_names
    self.segment_values = segment_values
    self.readdata = readdata
    self.img_shape = img_shape
    
    self.z_shape = self.current_img_array.shape[2]-1

    self.alpha = 0.8

    self.img_shape = img_shape
    self.idx_ax = img_shape[2]//2
    self.idx_sag = img_shape[1]//2
    self.idx_cor = img_shape[0]//2
    self.imgsize = img_shape[0]

    self.ax_mid = [self.img_shape[0]//2, self.img_shape[1]//2]
    self.sag_mid = [self.img_shape[1]//2, self.img_shape[2]//2]
    self.cor_mid = [self.img_shape[0]//2, self.img_shape[2]//2]

    #self.ax_arr = self.current_img_array[:, :, self.idx_ax]

    #self.sag_arr = self.current_img_array[:, self.idx_sag, :]
    #self.sag_arr = self.transpose(self.sag_arr)

    #self.cor_arr = self.current_img_array[self.idx_cor, :, :]
    #self.cor_arr = self.transpose(self.cor_arr)

    self.cor_arr, self.sag_arr, self.ax_arr = generateImages(self, self.current_img_array)

    self.c.bind('<Configure>', self.window_size)
    
    self.image_ax, self.c.temp1 = self.create_image(self.ax_arr[self.idx_ax])
    self.image_sag, self.c.temp2 = self.create_image(self.sag_arr[self.idx_sag])
    self.image_cor, self.c.temp3 = self.create_image(self.cor_arr[self.idx_cor])
    self.window_size(0)

    self.c.tag_bind(self.image_ax, "<Button-1>", self.click_ax)
    self.c.tag_bind(self.image_sag, "<Button-1>", self.click_sag)
    self.c.tag_bind(self.image_cor, "<Button-1>", self.click_cor)

    self.c.tag_bind(self.image_ax, "<<MouseWheel>>", self.scroll_ax)
    self.c.tag_bind(self.image_sag, "<<MouseWheel>>", self.scroll_sag)
    self.c.tag_bind(self.image_cor, "<<MouseWheel>>", self.scroll_cor)

    self.prompt_label = tk.Label(self.c,text='', font=40)
    self.prompt_label.grid(row=3, column=2, sticky=tk.E)
    self.prompt_generator()

    self.load_data = threading.Thread(target=self.load_correct)
    self.load_data.start()

    next = tk.Button(self.c, text='Next prompt', command=self.next_prompt)
    next.grid(row=0,column=1)

    ch_b = tk.Button(self.c, text="Toggle crosshair", command=self.toggle_crosshair)
    ch_b.grid(row=1,column=0)

    self.score = tk.Label(self.c, text='Total score: '+str(self.points))
    self.score.grid(row=2,column=0,pady=10)

    self.c.tag_bind(self.image_ax, "<Button-3>", self.zoom_ax)
    self.c.tag_bind(self.image_sag, "<Button-3>", self.zoom_sag)
    self.c.tag_bind(self.image_cor, "<Button-3>", self.zoom_cor)

    self.c.tag_bind(self.image_ax, "<Button-2>", self.drag_start)
    self.c.tag_bind(self.image_sag, "<Button-2>", self.drag_start)
    self.c.tag_bind(self.image_cor, "<Button-2>", self.drag_start)

    self.c.tag_bind(self.image_ax, "<B2-Motion>", self.drag_ax)
    self.c.tag_bind(self.image_sag, "<B2-Motion>", self.drag_sag)
    self.c.tag_bind(self.image_cor, "<B2-Motion>", self.drag_cor)

    #label = tk.Label(self.c,bg="blue",width=10,height=5)
    #label.place(x=0,y=0)
    #label.bind("<Button-1>",self.drag_start)
    #label.bind("<B1-Motion>",self.drag_motion)

def generateImages(self, im_arr):
    ax_lst = []
    sag_lst = []
    cor_lst = []

    for i in range(0, im_arr.shape[0]):
        cor_T = self.transpose(im_arr[i,:,:])
        cor_lst.append(cor_T)

    for i in range(0, im_arr.shape[1]):
        sag_T = self.transpose(im_arr[:,i,:])
        sag_lst.append(sag_T)

    for i in range(0, im_arr.shape[2]):
        ax = im_arr[:,:,i]
        ax_lst.append(ax)

    return cor_lst,sag_lst,ax_lst

def transpose(self,im):
    return np.transpose(im, (1, 0, 2)) #transpose, but not rgb