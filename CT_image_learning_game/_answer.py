import time
import numpy as np

def load_correct(self):
    print('started')
    if self.prompt_id in self.save_dict:
         self.ans = self.save_dict[self.prompt_id]
    else:
        self.ans = np.where(self.readdata==self.prompt_id) #1 = spine, should be changed to a dynamic number
        self.save_dict[self.prompt_id] = self.ans
    print("done")

def show_correct(self, idx):
        while self.load_data.is_alive():
            print('Loading answer:', self.load_data.is_alive())
            time.sleep(0.3)
        #print('xD')
        #for y,x,z in zip(self.ans[0],self.ans[1],self.ans[2]):
            #self.current_img_array[x,y,self.z_shape-z] = self.current_img_array[x,y,self.z_shape-z]*self.alpha + (0,255*(1-self.alpha),0) #highlights correct part with green
        self.current_img_array[self.ans[1], self.ans[0], self.z_shape-self.ans[2]] = \
            self.current_img_array[self.ans[1], self.ans[0], self.z_shape-self.ans[2]]*self.alpha + \
            (0,255*(1-self.alpha),0) #highlights correct part with green
        
        print("done")
        #print(self.idx_ax, self.idx_sag, self.idx_cor)
        self.c.temp1 = self.set_img(self.ax_arr[self.idx_ax], self.image_ax,self.ax_mid,self.zoomdist_ax)
        self.c.temp2 = self.set_img(self.sag_arr[self.idx_sag], self.image_sag,self.sag_mid,self.zoomdist_sag)
        self.c.temp3 = self.set_img(self.cor_arr[self.idx_cor], self.image_cor,self.cor_mid,self.zoomdist_cor)
        #self.setAllImages(idx)

def return_original(self):
    #for y,x,z in zip(self.ans[0],self.ans[1],self.ans[2]):
    #    self.current_img_array[x,y,self.z_shape-z] = (self.current_img_array[x,y,self.z_shape-z] - (0,255*(1-self.alpha),0))/self.alpha
    self.current_img_array[self.ans[1],self.ans[0],self.z_shape-self.ans[2]] = \
        (self.current_img_array[self.ans[1],self.ans[0],self.z_shape-self.ans[2]] - (0,255*(1-self.alpha),0))/self.alpha