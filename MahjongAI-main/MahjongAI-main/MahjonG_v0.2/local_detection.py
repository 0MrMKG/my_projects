import argparse
import time
import cv2
import numpy as np
import time
import win32com.client
import win32con
import win32gui
import mss
class ScreenCapture:
    def __init__(self,window_name='test'):
        self.rect = (0,0,1,1)
        self.cap = mss.mss()
        self.window_name = window_name
        self.img = None

    def grab_screen_mss(self,x=0,y=0,w=1,h=1):
        self.rect = (x,y,w,h)
        self.img = cv2.cvtColor(np.array(self.cap.grab(self.rect)), cv2.COLOR_BGRA2BGR)
        return self.img


