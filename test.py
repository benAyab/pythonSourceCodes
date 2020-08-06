import numpy as np
import cv2
from matplotlib import pyplot as plt


img1 = cv2.imread('person1_bacteria_1.jpeg')
img2 = cv2.imread('n.jpeg')

imgray1  = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
imgray2  = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#Operations
blur1 = cv2.GaussianBlur(imgray1,(5,5),0)
blur2 = cv2.GaussianBlur(imgray2,(5,5),0)

ret,thresh1 = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
ret,thresh2 = cv2.threshold(blur2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#thresh3 = cv2.adaptiveThreshold(copy,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

contours1, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours2, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


#img_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img_c1 = cv2.drawContours(img1, contours1, -1, (255,0,0), 3)
img_c2 = cv2.drawContours(img2, contours2, -1, (255,0,0), 3)

plt.subplot(1,2,1), plt.imshow(img_c1,'gray'), plt.title('Pneumia')
plt.xticks([]), plt.yticks([])
plt.subplot(1,2,2), plt.imshow(img_c2,'gray'), plt.title('Normal')
plt.xticks([]), plt.yticks([])

plt.show()
