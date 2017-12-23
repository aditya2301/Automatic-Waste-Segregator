import cv2
import numpy as np

img1 = cv2.imread('object2.jpeg')
img1=cv2.resize(img1,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)
img=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

#img=cv2.resize(img,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)


img = cv2.GaussianBlur(img,(5,5),0)
ret,thresh1 = cv2.threshold(img,79,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

_, contours, _= cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
c=max(contours,key=cv2.contourArea)
M = cv2.moments(c)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])


draw=np.zeros(img1.shape,np.uint8)
cv2.drawContours(draw,[c],0,(175,111,65),1)
cv2.circle(draw,(cx,cy), 5, (175,111,65), -1)

cv2.line(draw,(0,120),(365,120),(15,95,165),1)
cv2.line(draw,(0,240),(365,240),(15,95,165),1)
cv2.line(draw,(160,0),(160,384),(15,95,165),1)


if (cx>120 and cy>160) and (cx<240 and cy<365):
	print("Image is lying at QUADRANT 4")

cv2.imshow("draw",draw)
cv2.imshow("img",img1)
print("Center of the image is at co-ordinate - "+str(cx)+","+str(cy))

#print(img.shape)

cv2.waitKey(0)

#365,384