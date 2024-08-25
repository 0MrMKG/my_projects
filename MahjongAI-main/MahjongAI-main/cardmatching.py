import cv2
import numpy as np
from algorithm import *
from position_test import locate_position

cards = []
img = cv2.imread('./screenshot.png')
templates = ['1m.png', '2m.png','3m.png','4m.png','5m.png','0m.png','6m.png','7m.png','8m.png','9m.png',
             '1p.png', '2p.png','3p.png','4p.png','5p.png','0p.png','6p.png','7p.png','8p.png','9p.png',
             '1s.png', '2s.png','3s.png','4s.png','5s.png','0s.png','6s.png','7s.png','8s.png','9s.png',
             '1z.png', '2z.png','3z.png','4z.png','5z.png','6z.png','7z.png'
             ]


def cv_show(img):
    cv2.imshow('', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def cards_to_string(cards):
    counts = {'m': '', 'p': '', 's': '', 'z': ''}
    for card in cards:
        suit = card[-1]
        number = card[:-1]
        if suit in counts:
            counts[suit] += number
    result = counts['m'] + 'm' + counts['p'] + 'p' + counts['s'] + 's' + counts['z'] + 'z'
    return result


def count_groups(arr):
    arr_copy = arr.copy()
    count = 0
    while len(arr_copy) > 0:
        num = arr_copy[0]
        count += 1
        arr_copy = np.delete(arr_copy, np.where((arr_copy >= num - 5) & (arr_copy <= num + 5)))
    return count


def match_card(img):
    try:
        cards = []
        for template_file in templates:
            templ = cv2.imread('./cards/' + template_file)
            result = cv2.matchTemplate(img, templ, cv2.TM_CCOEFF_NORMED)
            threshold = 0.9
            loc = np.where(result >= threshold)
            if loc[0].size > 0 and loc[1].size > 0:
                num = count_groups(loc[1])
                for pt in zip(*loc[::-1]):
                    bottom_right = (pt[0] + templ.shape[1], pt[1] + templ.shape[0])
                    cv2.rectangle(img, pt, bottom_right, (0, 255, 0), 2)
                for i in range(num):
                    cards.append(template_file.split('.')[0])
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        print(cards)
        result = card_matching_algorithm(cards_to_string(cards))
        print(result)
        locate_position("screenshot", result)
    except cv2.error as e:
        print("OpenCV error:", e)
        match_card(img)


def match_card_sift(img):
    cards = []
    sift = cv2.SIFT_create()
    for template_file in templates:
        templ = cv2.imread('./cards/' + template_file, 0)
        kp1, des1 = sift.detectAndCompute(templ, None)
        kp2, des2 = sift.detectAndCompute(img, None)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        if len(good_matches) > 10:
            cards.append(template_file.split('.')[0])
    print(cards_to_string(cards))
    card_matching_algorithm(cards_to_string(cards))


if __name__ == "__main__":
    img = cv2.imread('./game.png')
    match_card(img)