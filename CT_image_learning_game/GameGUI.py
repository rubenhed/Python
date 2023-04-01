import threading
import time
import tkinter as tk
from PIL import Image, ImageTk
import random
import numpy as np


class gameGUI():
    points = 0
    tries = 0
    clicked = False
    crosshair_on = False
    ch_ax = False
    ch_sag = False
    ch_cor = False
    zoomed = False
    zoomdist_ax = 1
    zoomdist_sag = 1
    zoomdist_cor = 1
    old_w = 0
    old_h = 0
    save_dict = {}
    from _init import init,transpose

    from _answer import load_correct,show_correct,return_original

    from _interaction import click_ax,click_cor,click_sag,click_correct,drag_motion,drag_start,scroll_ax,scroll_cor,scroll_sag,zoom_click

    from _functions import create_crosshair,delete_crosshair,toggle_crosshair,prompt_generator,next_prompt,cor_ch,ax_ch,sag_ch,\
        zoom_ax,zoom_cor,zoom_sag,drag_ax,drag_start,adjust_ch,drag,update_image,drag_cor,drag_sag
    
    from _images import center_images,create_image,window_size,set_img,zoom_at


    def __init__(self, canvas, img3d, segment_names, segment_values, readdata, img_shape):
        self.init(canvas, img3d, segment_names, segment_values, readdata, img_shape)