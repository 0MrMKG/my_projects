import cv2
import numpy as np
from position_test import locate_button_position, photo_cut

img = cv2.imread("./buttonsituation.png")
templates = ['ron.png', 'peng.png', 'chi.png']  # 这里应该按照有限度排列 后续会加上Pei,Richi,Gang,EndMatch
jump_template = ['jump.png']

# 顺序应该为： Pei EndMatch Ron Richi Peng Gang Chi


def cv_show(img) -> None:
    cv2.imshow('', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def locate_possible_card(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    draw_img = img.copy()
    res = cv2.drawContours(draw_img, contours, -1, (0, 0, 255), 2)
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_image_res = cv2.cvtColor(hsv_image, cv2.COLOR_BGR2HSV)
    lower_color = np.array([15, 15, 15])
    upper_color = np.array([255, 255, 255])
    mask = cv2.inRange(hsv_image_res, lower_color, upper_color)
    cv2.imwrite('./mask.png', mask)
    # result = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)
    # cv_show(result)
    label_x,label_y = locate_button_position("mask","find_card_circle")
    return label_x,label_y


def feasible_call_situation(img):
    for template_file in templates:
        templ = cv2.imread('./call_selection_buttons/' + template_file)
        result = cv2.matchTemplate(img, templ, cv2.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where(result >= threshold)
        if loc[0].size > 0:
            return template_file.split('.')[0]


if __name__ == '__main__':
    #locate_card_test
    labelx,labely = locate_possible_card(img)
    photo_cut('buttonsituation',labelx,labely)




    #button_test
    '''
    result = feasible_call_situation(img)
    print (result)
    if result:
        locate_button_position("buttonsituation",'jump')
    locate_button_position("buttonsituation", str(result))
    '''

