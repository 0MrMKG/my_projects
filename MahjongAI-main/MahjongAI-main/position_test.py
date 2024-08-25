import cv2
import numpy as np
import time
import pyautogui


def cv_show(img) -> None:
    cv2.imshow('', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def photo_cut(background:str,top_left: tuple, bottom_right: tuple) -> None:
    img = cv2.imread(f'./{background}.png')
    x1, y1 = top_left
    x2, y2 = bottom_right
    cropped_image = img[y1:y2, x1:x2]
    cv2.imwrite('./cropped_image.png',cropped_image)


def locate_position(background:str,aim:str) -> None:
    image_a = cv2.imread(f'./{background}.png')
    image_b = cv2.imread(f'./cards/{aim}.png')
    result = cv2.matchTemplate(image_a, image_b, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # 获取图像B在图像A中的位置
    top_left = max_loc #左上
    bottom_right = (top_left[0] + image_b.shape[1], top_left[1] + image_b.shape[0]) #右下

    cv2.rectangle(image_a, top_left, bottom_right, 255, 2)
    center = (int(top_left[0] + image_b.shape[1]/2), int(top_left[1] + image_b.shape[0]/2))#中点
    cv2.circle(image_a, center, 5, (255, 255, 255), -1)
    image_a = cv2.resize(image_a, (image_a.shape[1]//2, image_a.shape[0]//2))
    #cv_show(image_a)
    print(top_left,bottom_right)
    for i in range(2):
        pyautogui.click(int(top_left[0] + image_b.shape[1]/2), int(top_left[1] + image_b.shape[0]/2))


def locate_button_position(background:str,aim:str) -> tuple:
    image_a = cv2.imread(f'./{background}.png')
    image_b = cv2.imread(f'./call_selection_buttons/{aim}.png')
    result = cv2.matchTemplate(image_a, image_b, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # 获取图像B在图像A中的位置
    top_left = max_loc #左上
    bottom_right = (top_left[0] + image_b.shape[1], top_left[1] + image_b.shape[0]) #右下

    cv2.rectangle(image_a, top_left, bottom_right, 255, 2)
    center = (int(top_left[0] + image_b.shape[1]/2), int(top_left[1] + image_b.shape[0]/2))#中点
    cv2.circle(image_a, center, 5, (255, 255, 255), -1)
    image_a = cv2.resize(image_a, (image_a.shape[1]//2, image_a.shape[0]//2))
    cv_show(image_a)
    #print(top_left, bottom_right)
    for i in range(2):
        pyautogui.click(int(top_left[0] + image_b.shape[1]/2), int(top_left[1] + image_b.shape[0]/2))
    return (top_left, bottom_right)


'''
def locate_position(background:str, aim:str) -> None:
    image_a = cv2.imread(f'./{background}.png')
    image_b = cv2.imread(f'./cards/{aim}.png')
    top_left, _ = match_and_get_location(image_a, image_b)
    click_center(top_left, image_b)

def locate_button_position(background:str, aim:str) -> None:
    image_a = cv2.imread(f'./{background}.png')
    image_b = cv2.imread(f'./call_selection_buttons/{aim}.png')
    top_left, _ = match_and_get_location(image_a, image_b)
    click_center(top_left, image_b)

def match_and_get_location(image_a, image_b):
    result = cv2.matchTemplate(image_a, image_b, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    return top_left, image_b

def click_center(top_left, image_b):
    center = (int(top_left[0] + image_b.shape[1] / 2), int(top_left[1] + image_b.shape[0] / 2))
    for i in range(2):
        pyautogui.click(center)
'''

if __name__ == "__main__":
    #locate_position("game3", '7z')
    photo_cut('mask',(568, 234), (672, 316))