import cv2
import numpy as np
 
img =  cv2.imread('D:/asset/i.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = cv2.GaussianBlur(gray,(3,3) ,0)

edged = cv2.Laplacian(gray, -1, ksize=5)

edged = 255 - edged

edgedPreserve = cv2.edgePreservingFilter(img, flags=2, sigma_s=150, sigma_r=0.9)
result = cv2.bitwise_and(edgedPreserve, edgedPreserve, mask=edged)
result = cv2.GaussianBlur(result,(3,3) ,0)
result = cv2.medianBlur(result,3)
cv2.imshow("resultat",result)
cv2.imwrite("results/i2.jpg",result)
