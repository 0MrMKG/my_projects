import local_detection
import check_win_gui as ck
import cv2
import math
from datetime import datetime

sc = local_detection.ScreenCapture()
x, y, width, height = 0,0,0,0
count = 0
k = cv2.waitKey(100)
while(True):
        count = 0
        now_time = str(int(datetime.now().timestamp()))
        x, y, width, height = ck.get_window_pos_size()
        a_cuts=5
        b_cuts=4
        a = width//a_cuts
        b = height//b_cuts
        if width==1 and height ==1:
            continue
        # im = sc.grab_screen_mss(x,y,x+width,y+height)
        # im = cv2.cvtColor(im,cv2.COLOR_BGRA2BGR)
        #
        # im1 = sc.grab_screen_mss(x, y, x + width//3, y + height//2)
        # im1 = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        # cv2.imshow("ha",im1)
        # cv2.imwrite("photos\\" + str(count) +".png",im1)

        # for i in range(a_cuts-1):
        #     for j in range(b_cuts-1,b_cuts):
        #         count += 1
        #         im1 = sc.grab_screen_mss(x+a*i+40,y+j*b,x+a*i+a,y+j*b+b)
        #         im1 = cv2.cvtColor(im1, cv2.COLOR_BGRA2BGR)
        #         cv2.imwrite("photos\\" +now_time+"_"+str(count)+ ".png", im1)
        im1 = sc.grab_screen_mss(x+a//2+30,y,x+int(3.5*a)+20,y+4*b)
        im1 = cv2.cvtColor(im1, cv2.COLOR_BGRA2BGR)
        im1 = cv2.resize(im1,dsize=(1280,1280))
        cv2.imwrite("photos\\" +now_time+".png", im1)
        break