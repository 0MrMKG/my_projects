import pygetwindow as gw
import cv2
import time
from PIL import ImageGrab
from cardmatching import match_card
from call_selection import feasible_call_situation

def find_window(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    for window in windows:
            return window
    return None

while True:
    window = find_window("雀魂麻將")
    if window is not None:
        print(window.left, window.top)
        print(window.width, window.height)
        print("\n")
        # 截图并保存
        screenshot = ImageGrab.grab(
            bbox=(window.left*1.27, window.top*1.27, window.left*1.27 + window.width*1.24, window.top*1.27 + window.height*1.24))
        screenshot.save('./screenshot.png')
        print("截图已保存")
        img = cv2.imread(('./screenshot.png'))
        match_card(img)
    else:
        print("未找到指定窗口")
    time.sleep(5)