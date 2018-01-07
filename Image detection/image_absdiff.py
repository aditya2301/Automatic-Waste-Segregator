import numpy as np
import cv2,time

img1=cv2.imread("back.jpeg")
blur1 = cv2.GaussianBlur(img1,(5,5),0)
gray1=cv2.cvtColor(blur1,cv2.COLOR_BGR2GRAY)
ret,thresh1 = cv2.threshold(gray1,65,255,cv2.THRESH_BINARY_INV)

img2=cv2.imread("front5.jpeg")
blur2 = cv2.GaussianBlur(img2,(5,5),0)
gray2=cv2.cvtColor(blur2,cv2.COLOR_BGR2GRAY)
ret,thresh2 = cv2.threshold(gray2,65,255,cv2.THRESH_BINARY_INV)

diff=cv2.absdiff(thresh2,thresh1)
diff=cv2.bitwise_xor(diff,thresh1)

kernel = np.ones((5,5),np.uint8)
diff = cv2.dilate(diff,kernel,iterations = 7)

_, contours, _= cv2.findContours(diff,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
c=max(contours,key=cv2.contourArea)
x,y,w,h = cv2.boundingRect(c)
cv2.rectangle(diff,(x,y),(x+w,y+h),(40,255,0),5)


cv2.imshow("thresh",diff)
cv2.waitKey(0)