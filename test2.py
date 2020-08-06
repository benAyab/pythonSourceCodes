import cv2
import numpy as np
def nothing(x):
    pass
# Create a black image, a window
img = img = cv2.imread('testimg.jpg', 0)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
ret,thresh4 = cv2.threshold(img,64,255,cv2.THRESH_TOZERO)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('Threshold','image',0,255,nothing)


# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)
while(1):
    cv2.imshow('image',thresh4)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
# get current positions of four trackbars
        r = cv2.getTrackbarPos('R','image')
        s = cv2.getTrackbarPos(switch,'image')
        if s == 0:
            ret,thresh4 = cv2.threshold(img,64,255,cv2.THRESH_TOZERO)
        else:
         ret,thresh4 = cv2.threshold(img,r,255,cv2.THRESH_TOZERO)   
cv2.destroyAllWindows()
