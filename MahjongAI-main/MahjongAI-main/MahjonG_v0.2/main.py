import cv2
import numpy as np
import os
import sys
import io
from selenium.webdriver.common.by import By
from classifier import Classify
from selenium import webdriver

import local_detection
import check_win_gui as ck
import cv2
from datetime import datetime

sc = local_detection.ScreenCapture()
x, y, width, height = 0,0,0,0
count = 0
templates = ['0m.png','1m.png', '2m.png','3m.png','4m.png','5m.png','6m.png','7m.png','8m.png','9m.png',
             '0p.png','1p.png', '2p.png','3p.png','4p.png','5p.png','6p.png','7p.png','8p.png','9p.png',
             '0s.png','1s.png', '2s.png','3s.png','4s.png','5s.png','6s.png','7s.png','8s.png','9s.png',
             '1z.png', '2z.png','3z.png','4z.png','5z.png','6z.png','7z.png'
             ]
cards = []
photo_root = r"clips"
photo_lis = os.listdir(photo_root)
final_str = ""

def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN: # 当左键按下时触发该事件
        print("Clicked at ({}, {})".format(x, y))


def cv_show(img):
    cv2.imshow('', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def extract_sift_feature(img):
    # 创建SIFT检测器
    sift = cv2.SIFT_create()
    # 提取图像的特征点和描述子信息
    keypoints, descriptors = sift.detectAndCompute(img, None)
    return keypoints, descriptors


def cal_SIFT_sim(img1,img2):
    #将图片转换为灰度图
    img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    #提取图片的SIFT特征
    keypoints1,descriptors1 = extract_sift_feature(img1)
    keypoints2,descriptors2 = extract_sift_feature(img2)
    #创建一个匹配器
    bf = cv2.BFMatcher()
    #记录图1和图2的匹配的关键点
    matches1 = bf.knnMatch(descriptors1,descriptors2,k=2)
    top_results1 = []
    for m,n in matches1:
        if m.distance < 0.7 * n.distance:
            top_results1.append(m)
    #记录图2和图1匹配的关键点
    matches2 = bf.knnMatch(descriptors2,descriptors1,k=2)
    top_results2 = []
    for m,n in matches2:
        if m.distance < 0.7 * n.distance:
            top_results2.append(m)
    #从匹配的关键点中选择出有效的匹配
    #确保匹配的关键点信息在图1和图2以及图2和图1是一致的
    top_results = []
    for m1 in top_results1:
        m1_query_idx = m1.queryIdx
        m1_train_idx = m1.trainIdx
        for m2 in top_results2:
            m2_query_idx = m2.queryIdx
            m2_train_idx = m2.trainIdx
            if m1_query_idx == m2_train_idx and m1_train_idx == m2_query_idx:
                top_results.append(m1)

    image_sim = len(top_results) / min(len(keypoints1),len(keypoints2))
    return image_sim

def mse(img1, img2):
    diff = cv2.absdiff(img1, img2)
    diff_squared = diff ** 2
    mse = np.mean(diff_squared)
    return mse

def calculate_ssim(img1, img2):
    # 将图片转换为灰度
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ssim = cv2.xfeatures2d.SIFT_create()
    ssim_index = ssim.compare(gray1, gray2)
    return ssim_index

while(True):
        count = 0
        now_time = str(int(datetime.now().timestamp()))
        x, y, width, height = ck.get_window_pos_size()
        if width==1 and height ==1:
            continue
        for i in range(13):
            im = sc.grab_screen_mss(x + 158 + 63*(i), y + 660, x  + 158 + 63*i + 62, y + 755)
            im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
            cv2.imwrite("clips/{}.png".format(i+1),im)
        im_hand =  sc.grab_screen_mss(x + 158 + 840  , y + 660, x  + 158  + 899 , y + 755)
        im_hand = cv2.cvtColor(im_hand, cv2.COLOR_BGRA2BGR)
        cv2.imwrite("clips/{}.png".format(14), im_hand)
        break

c = Classify()

for each in photo_lis:
    court = []
    photo_each_root = photo_root+'\\'+each
    img = cv2.imread(photo_each_root)
    result = c(img)
    cards.append(result)

for each in cards:
    final_str += each

website = "https://tenhou.net/2/?q={}".format(final_str)

print(website)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
driver = webdriver.Chrome()
driver.get(website)
driver.implicitly_wait(10)
html = driver.page_source
driver.quit()

for line in html.splitlines():
    if line and line[0] == "打":
        print(line)