import cv2

cap=cv2.imread("back.jpeg")
new=cap[140:,:]
cv2.imshow("original",cap)

cv2.imshow("cropped",new)
key=cv2.waitKey()
if key==ord("q"):
	cv2.destroyAllWindows()