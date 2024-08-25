import cv2
import numpy as np
from position_test import locate_button_position
# 这个文件不会被使用

'''
image = cv2.imread('./buttonsituation.png')

# 将图片转换为灰度图像
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用 Canny 边缘检测算法
edges = cv2.Canny(gray_image, 100, 200)  # 100 和 200 是 Canny 算法的阈值参数
edges = cv2.resize(edges,(0,0),fx = 0.5,fy = 0.5)

kernel = np.ones((2, 2), np.uint8)  # 5x5 的膨胀核，可以根据需要调整大小

# 对边缘图像进行膨胀操作
dilated_edges = cv2.dilate(edges, kernel, iterations=1)  # iterations 控制膨胀的次数
tophat = cv2.morphologyEx(edges, cv2.MORPH_TOPHAT, kernel)
# 显示边缘检测结果
cv2.imshow('Edges', dilated_edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('Edges', tophat)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

def cv_show(img) -> None:
    cv2.imshow('', img)
    cv2.waitKey()
    cv2.destroyAllWindows()


img = cv2.imread('./buttonsituation.png')
#img = cv2.resize(img,(0,0),fx=0.7,fy=0.7)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
draw_img = img.copy()
res = cv2.drawContours(draw_img, contours, -1, (0, 0, 255), 2)


hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv_image_res = cv2.cvtColor(hsv_image, cv2.COLOR_BGR2HSV)
#cv_show(hsv_image)
#cv_show(hsv_image_res)

lower_color = np.array([15, 15, 15])
upper_color = np.array([255, 255, 255])

mask = cv2.inRange(hsv_image_res, lower_color, upper_color)
cv2.imwrite('./mask.png', mask)
#cv_show(mask)
#result = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)
#cv_show(result)



def guess_what_is_it() -> None:
    guesser = cv2.imread('./cropped_image.png')

    cv_show(guesser)




if __name__ == "__main__":
    locate_button_position("mask","find_card_circle")
    guess_what_is_it()

