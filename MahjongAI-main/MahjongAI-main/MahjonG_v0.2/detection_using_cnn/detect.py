from classifier import Classify
import cv2
import numpy as np
img = cv2.imread("6m.png")
c = Classify()
print(c(img))

