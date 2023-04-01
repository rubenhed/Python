from PIL import Image, ImageTk
import numpy as np

def create_image(self, im_arr):
    image = Image.fromarray(im_arr.astype('uint8'), 'RGB')
    #image = self.resizeImage(image, im_arr.shape)
    img =  ImageTk.PhotoImage(image=image)
    disp = self.c.create_image(0,0, image = img)
    return disp, img

def window_size(self,event):
    w = self.c.winfo_width()
    h = self.c.winfo_height()
    self.imgsize = min(w,h)//2
    #if oldimgsize != self.imgsize:
    #    self.resizeImages(w)
    if w != self.old_w or h != self.old_h: #make it so it resizes if changes in self.imgsize, and only places images if changes to w or h
        self.center_images(w, h)
        #print(w,h)
    self.old_h = h
    self.old_w = w


def center_images(self, w, h):
    im = self.ax_arr[self.idx_ax]
    self.c.temp1 = self.set_img(im, self.image_ax, self.ax_mid,self.zoomdist_ax)
    self.c.moveto(self.image_ax, w//2, h//2 - self.imgsize)

    im = self.sag_arr[self.idx_sag]
    #im = self.transpose(im)
    self.c.temp2 = self.set_img(im, self.image_sag, self.sag_mid,self.zoomdist_sag)
    self.c.moveto(self.image_sag, w//2 - self.imgsize, h//2)

    im = self.cor_arr[self.idx_cor]
    #im = self.transpose(im)
    self.c.temp3 = self.set_img(im, self.image_cor, self.cor_mid,self.zoomdist_cor)
    self.c.moveto(self.image_cor, w//2, h//2)

    if self.crosshair_on:
        temp = -1
        chs = [self.ch_ax, self.ch_sag, self.ch_cor]
        for i in range(0,len(chs)):
            if chs[i]:
                temp = i
        self.delete_crosshair()
        if temp == -1:
            self.create_crosshair()
        elif temp == 0:
            self.ax_ch()
        elif temp == 1:
            self.sag_ch()
        else:
            self.cor_ch()

def set_img(self, img_array, disp, mid, zoomdist):
        image = Image.fromarray(img_array.astype('uint8'), 'RGB')
        if self.zoomed:
            image = self.zoom_at(image, mid[0],mid[1], zoomdist)
        image.thumbnail((self.imgsize,self.imgsize))
        
        img =  ImageTk.PhotoImage(image=image)
        self.c.itemconfig(disp, image = img)
        
        return img

def zoom_at(self, img, x, y, zoom):
    #print('xD')
    #y  = self.img_shape[2]-y
    w, h = img.size
    zoom2 = zoom * 2
    img = img.crop((x - w / zoom2, y - h / zoom2, 
                    x + w / zoom2, y + h / zoom2))
    return img.resize((w, h), Image.LANCZOS)