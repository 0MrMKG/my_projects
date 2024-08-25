import cv2
import pygetwindow as gw
import time

def find_window(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    for window in windows:
            return window
    return None

def get_window_pos_size(title="雀魂麻將"):
    window = find_window(title)
    if window is not None:
        return [window.left,window.top,window.width,window.height]
    else:
        return [0,0,1,1]












