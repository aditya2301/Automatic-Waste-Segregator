from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2,os
import numpy as np
import threading


def imageSubtract(img):
    bilateral_filtered_image = cv2.bilateralFilter(img, 7,70,70)
    bilateral_filtered_image = cv2.cvtColor(bilateral_filtered_image,cv2.COLOR_BGR2GRAY)
    return bilateral_filtered_image

def  imageProcessing():
    camera = PiCamera()
    camera.resolution = (512,512)
    camera.awb_mode="fluorescent"
    camera.iso = 800
    camera.contrast=25
    camera.brightness=64
    camera.sharpness=100
    rawCapture = PiRGBArray(camera, size=(512, 512))

    first_time=0
    frame_buffer=0
    counter=0
    camera.start_preview()
    sleep(2)
   

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
        if first_time==0:
            rawCapture.truncate(0)
            if frame_buffer<10:
               print("Frame rejected -",str(frame_buffer))
               frame_buffer+=1
               continue
            os.system("clear")
            refImg=frame.array
            refThresh=imageSubtract(refImg)
            first_time=1
            frame_buffer=0


        frame_buffer+=1
        image = frame.array
        cv2.imshow("Foreground", image)
        key = cv2.waitKey(1)
        rawCapture.truncate(0)
        newThresh=imageSubtract(image)

        diff=cv2.absdiff(refThresh,newThresh)
        kernel = np.ones((5,5),np.uint8)
        #diff=cv2.erode(diff,kernel,iterations = 1)
        diff=cv2.dilate(diff,kernel,iterations = 2)
        cv2.imshow("Background",refImg)
        _, thresholded = cv2.threshold(diff, 0 , 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)
        
        

        _, contours, _= cv2.findContours(thresholded,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        try:
           c=max(contours,key=cv2.contourArea)
           x,y,w,h = cv2.boundingRect(c)
           
           cv2.rectangle(thresholded,(x,y),(x+w,y+h),(125,125,125),2)
           if cv2.contourArea(c)>300 and len(contours)<=5:
              print("Total contours found=",len(contours))
              print("Object detected with area = ",cv2.contourArea(c))
              #print("Object detected with area = ",cv2.contourArea(c))
           
           cv2.imshow("Threshold",thresholded)
           if frame_buffer%50==0:
              refImg=image
              refThresh=imageSubtract(refImg)
              print("Refrence Image changed")
           if key == ord('q'):
               camera.close()
               cv2.destroyAllWindows()
               break
           #print(frame_buffer)
        except Exception as e:
           pass

if __name__ == "__main__" :
   imageProcessing()
