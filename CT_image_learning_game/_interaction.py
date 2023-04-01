def drag_start(self, event):
    widget = event.widget
    widget.startY = event.y

def drag_motion(self, event):
    widget = event.widget
    y = widget.winfo_y() - widget.startY + event.y

    #print(x,widget.winfo_x())

    if widget.winfo_y() > y:
        print('left')
    elif widget.winfo_y() < y:
        print('right')
    widget.place(y=y)

def click_ax(self,event):
    x0,y0,x1,y1 = self.c.bbox(self.image_ax)
    imgsize_x = x1-x0
    imgsize_y = y1-y0
    inx = event.x-x0
    iny = event.y-y0
    #x,y = self.zoom_click(self.ax_mid,imgsize_x, imgsize_y, inx, iny)
    x = inx*self.img_shape[0]//imgsize_x
    y = iny*self.img_shape[1]//imgsize_y

    if self.zoomed:
        x,y = self.zoom_click(x,y, self.ax_mid, self.img_shape[0], self.img_shape[1],self.zoomdist_ax)
        
    x_range, y_range = self.readdata[:,:,0].shape
    if x in range(x_range) and y in range(y_range):
        ans = self.readdata[x,y,self.idx_ax]
        self.click_correct(ans, self.idx_ax)

def click_sag(self,event):
    x0,y0,x1,y1 = self.c.bbox(self.image_sag)
    imgsize_x = x1-x0
    imgsize_y = y1-y0

    
    x = (event.x-x0)*self.img_shape[1]//imgsize_x
    y = (event.y-y0)*self.img_shape[2]//imgsize_y

    if self.zoomed:
        x,y = self.zoom_click(x,y, self.sag_mid, self.img_shape[1], self.img_shape[2],self.zoomdist_sag)
        #y = int(self.img_shape[2] + y)

    y = self.img_shape[2]- y
    #print(x,y)

    x_range, y_range = self.readdata[0,:,:].shape
    if x in range(x_range) and y in range(y_range):
        ans = self.readdata[self.idx_sag,x,y]
        self.click_correct(ans, self.idx_sag)

def click_cor(self,event):
    x0,y0,_,_ = self.c.bbox(self.image_cor)
    x = (event.x-x0)*self.img_shape[0]//self.imgsize
    y = (event.y-y0)*self.img_shape[2]//self.imgsize

    if self.zoomed:
        x,y = self.zoom_click(x,y, self.cor_mid, self.img_shape[0], self.img_shape[2],self.zoomdist_cor)
        #y = self.img_shape[2] + y
    y = self.img_shape[2] - y
    #print(x,y)

    x_range, y_range = self.readdata[:,0,:].shape
    if x in range(x_range) and y in range(y_range):
        ans = self.readdata[x,self.idx_cor,y]
        self.click_correct(ans, self.idx_cor)

def zoom_click(self,x,y, mid, shape_x, shape_y, zoomdist):
    x = mid[0] - (shape_x/2 - x)/zoomdist
    y = mid[1] - (shape_y/2 - y)/zoomdist
    x = int(x)
    y = int(y)
    return x,y

def click_correct(self,ans,idx):
    #self.idx_ax = self.idx_sag = self.idx_cor = idx

    if not self.clicked or self.clicked:
        self.tries+=1
        if ans == self.prompt_id:
            print(self.prompt,'was found!')
            self.points+=1
        else:
            print('failed to find',self.prompt)
        self.score.config(text='Total score: '+str(self.points)+'/'+str(self.tries))
        self.show_correct(idx)
        self.clicked = True
    #self.setAllImages(idx)

def scroll_ax(self,event):
    wheelup = event.time>1000
    if wheelup:
        if self.idx_ax + 1 == self.img_shape[2]:
            return
        self.idx_ax +=1
    else:
        if self.idx_ax == 0:
            return
        self.idx_ax -=1

    #self.ax_arr = self.current_img_array[:, :, self.idx_ax]
    self.c.temp1 = self.set_img(self.ax_arr[self.idx_ax],self.image_ax,self.ax_mid,self.zoomdist_ax)
    if self.crosshair_on:
        self.delete_crosshair()
        self.ax_ch()

def scroll_sag(self,event):
    wheelup = event.time<1000
    if wheelup:
        if self.idx_sag + 1 == self.img_shape[1]:
            return
        self.idx_sag +=1
    else:
        if self.idx_sag == 0:
            return
        self.idx_sag -=1

    #self.sag_arr = self.current_img_array[:, self.idx_sag, :]
    #self.sag_arr = self.transpose(self.sag_arr)
    self.c.temp2 = self.set_img(self.sag_arr[self.idx_sag],self.image_sag,self.sag_mid,self.zoomdist_sag)
    if self.crosshair_on:
        self.delete_crosshair()
        self.sag_ch()

def scroll_cor(self,event):
    wheelup = event.time>1000
    if wheelup:
        if self.idx_cor + 1 == self.img_shape[0]:
            return
        self.idx_cor +=1
    else:
        if self.idx_cor == 0:
            return
        self.idx_cor -=1
    #self.cor_arr = self.current_img_array[self.idx_cor, :, :]
    #self.cor_arr = self.transpose(self.cor_arr)
    self.c.temp3 = self.set_img(self.cor_arr[self.idx_cor],self.image_cor,self.cor_mid,self.zoomdist_cor)
    if self.crosshair_on:
        self.delete_crosshair()
        self.cor_ch()