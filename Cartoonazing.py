import numpy as np
import cv2
from matplotlib import pyplot as plt


img = cv2.imread('D:/asset/i.jpg')
#imgray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = cv2.GaussianBlur(img,(3,3),0)

Z = img.reshape((-1,3))

Z = np.float32(Z)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)

K = 13


ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))
cv2.imshow('res2',res2)
cv2.imwrite('r1.jpg',res2)
cv2.waitKey(0)
cv2.destroyAllWindows()
