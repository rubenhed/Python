import random
import threading

def toggle_crosshair(self):#stipple='gray50'
    if not self.crosshair_on:
        self.create_crosshair()
    else:
        self.delete_crosshair()

def create_crosshair(self):
    # color = 'blue'
    # #ax
    # x0,y0,x1,y1 = self.c.bbox(self.image_ax)

    # y = (self.idx_cor*(y1-y0))/(self.img_shape[0]) + y0
    # self.ax_x = self.c.create_line(x0, y, x1, y, fill=color)

    # x =(self.idx_sag*(x1-x0))/(self.img_shape[1]) + x0
    # self.ax_y = self.c.create_line(x, y0, x, y1, fill=color)
    # #sag
    # x0,y0,x1,y1 = self.c.bbox(self.image_sag)

    # y = (self.idx_ax*(y1-y0))/(self.img_shape[2]) + y0
    # self.sag_x = self.c.create_line(x0, y, x1, y, fill=color)

    # x = (self.idx_cor*(x1-x0))/(self.img_shape[0]) + x0
    # self.sag_y = self.c.create_line(x, y0, x, y1, fill=color)
    # #cor
    # x0,y0,x1,y1 = self.c.bbox(self.image_cor)

    # y = (self.idx_ax*(y1-y0))/(self.img_shape[2]) + y0
    # self.cor_x = self.c.create_line(x0, y, x1, y, fill=color)

    # x = (self.idx_sag*(x1-x0))/(self.img_shape[1]) + x0
    # self.cor_y = self.c.create_line(x, y0, x, y1, fill=color)
    
    # self.crosshair_on = True
    self.cor_ch()
    self.sag_ch()
    self.ax_ch()

def adjust_ch(self, mid, shape, imgsize, zoomdist):
    ad_axis = ((mid - shape//2)/(shape/imgsize))*zoomdist
    return ad_axis

def cor_ch(self):
    color = 'blue'
    x0,y0,x1,y1 = self.c.bbox(self.image_ax)
    imgsize_y = y1-y0
    midy = self.adjust_ch(self.ax_mid[1], self.img_shape[1], y1-y0, self.zoomdist_ax)
    #midy = ((self.ax_mid[1] - self.img_shape[1]//2)/(self.img_shape[1]/imgsize_y))*self.zoomdist_ax  #WORKS

    y = (self.idx_cor*(imgsize_y))/(self.img_shape[0]) + y0
    y -= midy
    self.ax_x = self.c.create_line(x0, y, x1, y, fill=color)

    x0,y0,x1,y1 = self.c.bbox(self.image_sag)
    x = (self.idx_cor*(x1-x0))/(self.img_shape[0]) + x0
    self.sag_y = self.c.create_line(x, y0, x, y1, fill=color)

    self.crosshair_on = True
    self.ch_cor = True

def sag_ch(self):
    color = 'blue'
    x0,y0,x1,y1 = self.c.bbox(self.image_ax)

    imgsize_x = x1-x0
    #midx = ((self.ax_mid[0] - self.img_shape[0]//2)/(self.img_shape[0]/imgsize_x))*self.zoomdist_ax  #WORKS
    midx = self.adjust_ch(self.ax_mid[0], self.img_shape[0], x1-x0, self.zoomdist_ax)

    x =(self.idx_sag*(x1-x0))/(self.img_shape[1]) + x0
    x -= midx
    self.ax_y = self.c.create_line(x, y0, x, y1, fill=color)

    x0,y0,x1,y1 = self.c.bbox(self.image_cor)
    x = (self.idx_sag*(x1-x0))/(self.img_shape[1]) + x0
    self.cor_y = self.c.create_line(x, y0, x, y1, fill=color)

    self.crosshair_on = True
    self.ch_sag = True

def ax_ch(self):
    color = 'blue'
    x0,y0,x1,y1 = self.c.bbox(self.image_sag)

    y = (self.idx_ax*(y1-y0))/(self.img_shape[2]) + y0
    self.sag_x = self.c.create_line(x0, y, x1, y, fill=color)

    x0,y0,x1,y1 = self.c.bbox(self.image_cor)

    y = (self.idx_ax*(y1-y0))/(self.img_shape[2]) + y0
    self.cor_x = self.c.create_line(x0, y, x1, y, fill=color)

    self.crosshair_on = True
    self.ch_ax = True

    

def delete_crosshair(self):
    line_lst = [self.ax_x,self.ax_y,self.sag_x,self.sag_y,self.cor_x,self.cor_y]
    for ch in line_lst:
        try:
            self.c.delete(ch)
        except:
            pass

    self.crosshair_on = False
    self.ch_ax = False
    self.ch_sag = False
    self.ch_cor = False

def prompt_generator(self):
    self.prompt_id = random.choice(self.segment_values)
    self.prompt = self.segment_names[self.prompt_id-1]

    self.prompt_label.config(text = 'Find: ' + self.prompt)


def next_prompt(self):
    if self.clicked:
        self.prompt_generator()
        self.return_original()

        self.clicked = False
        #self.current_img_array = self.orginal_array
        #self.setAllImages()

        self.load_data = threading.Thread(target=self.load_correct)
        self.load_data.start()

        w = self.c.winfo_width()
        h = self.c.winfo_height()
        self.center_images(w, h)
    
def zoom_ax(self, event):
    x0,y0,x1,y1 = self.c.bbox(self.image_ax)
    x = event.x
    y = event.y

    imgsize_x = x1-x0
    imgsize_y = y1-y0

    x = (x-x0)*self.img_shape[0]//imgsize_x
    y = (y-y0)*self.img_shape[1]//imgsize_y

    #print(x,y)

    x,y = self.zoom_click(x,y, self.ax_mid, self.img_shape[0], self.img_shape[1], self.zoomdist_ax)

    self.ax_mid = [x,y]
    self.zoomdist_ax += 0.1
    #print(x,y)
    self.update_image()
    if self.crosshair_on:
        self.delete_crosshair()
        self.ax_ch()
        #self.cor_ch()

def zoom_sag(self, event):
    x0,y0,x1,y1 = self.c.bbox(self.image_sag)
    x = event.x
    y = event.y

    imgsize_x = x1-x0
    imgsize_y = y1-y0

    x = (x-x0)*self.img_shape[1]//imgsize_x
    y = (y-y0)*self.img_shape[2]//imgsize_y
    #print(y)

    x,y = self.zoom_click(x,y, self.sag_mid, self.img_shape[1], self.img_shape[2],self.zoomdist_sag)

    self.sag_mid = [x, y]
    self.zoomdist_sag += 0.1
    #print(x,y)
    self.update_image()

def zoom_cor(self, event):
    x0,y0,x1,y1 = self.c.bbox(self.image_cor)
    x = event.x
    y = event.y

    imgsize_x = x1-x0
    imgsize_y = y1-y0

    x = (x-x0)*self.img_shape[0]//imgsize_x
    y = (y-y0)*self.img_shape[2]//imgsize_y

    x,y = self.zoom_click(x,y, self.cor_mid, self.img_shape[0], self.img_shape[2],self.zoomdist_cor)

    self.cor_mid = [x,y]
    self.zoomdist_cor += 0.1
    #print(x,y)
    self.update_image()

def drag_start(self,event):
    self.old_x = event.x
    self.old_y = event.y

def drag_ax(self, event):
    new_x, new_y = self.drag(event.x, event.y)
    self.ax_mid[0] -= new_x
    self.ax_mid[1] -= new_y
    self.update_image()
    if self.crosshair_on:
        self.delete_crosshair()
        self.ax_ch()
        #self.cor_ch()

def drag_sag(self, event):
    new_x, new_y = self.drag(event.x, event.y)
    self.sag_mid[0] -= new_x
    self.sag_mid[1] -= new_y
    self.update_image()

def drag_cor(self, event):
    new_x, new_y = self.drag(event.x, event.y)
    self.cor_mid[0] -= new_x
    self.cor_mid[1] -= new_y
    self.update_image()

def update_image(self):
    self.zoomed = True
    self.center_images(self.c.winfo_width(), self.c.winfo_height())

def drag(self, x, y):
    new_x = x - self.old_x
    new_y = y - self.old_y
    self.old_x = x
    self.old_y = y
    return new_x, new_y


    #print(x,y)

   # x,y = self.zoom_click(x,y, self.ax_mid, self.img_shape[0], self.img_shape[1],self.zoomdist_ax)