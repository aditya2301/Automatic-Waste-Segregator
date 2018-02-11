from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2,os
import numpy as np


def imageSubtract(img):
    blur = cv2.GaussianBlur(img,(5,5),0)
    ret,thresh = cv2.threshold(blur,65,255,cv2.THRESH_BINARY_INV)
    return thresh

camera = PiCamera()
camera.resolution = (512,512)
camera.awb_mode="fluorescent"
camera.iso = 800
camera.contrast=25
camera.brightness=55
camera.sharpness=100
camera.saturation=30
rawCapture = PiRGBArray(camera, size=(512, 512))

first_time=0
frame_buffer=0
counter=0
camera.start_preview()
sleep(2)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    if first_time==0:
        rawCapture.truncate(0)
        if frame_buffer<15:
           frame_buffer+=1
           continue
        os.system("clear")
        refImg=frame.array
        refImg1=cv2.cvtColor(refImg,cv2.COLOR_BGR2GRAY)
        refThresh=imageSubtract(refImg1)
        first_time=1



    image = frame.array
    cv2.imshow("NewImage", image)
    key = cv2.waitKey(1)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    rawCapture.truncate(0)

    newThresh=imageSubtract(gray)
    diff=cv2.absdiff(refThresh,newThresh)
    diff=cv2.bitwise_xor(diff,refThresh)
    kernel = np.ones((3,3),np.uint8)
    #diff=cv2.erode(diff,kernel,iterations = 1)
    diff=cv2.dilate(diff,kernel,iterations = 7)
    
    try:
    
        _, contours, _= cv2.findContours(diff,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        c=max(contours,key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(diff,(x,y),(x+w,y+h),(125,125,125),2)
        print("Object Area =",cv2.contourArea(c))
        if cv2.contourArea(c)>250:
            if counter==0:
                print("Object entering frame . Going into sleep for 2 sec and resuming")
                sleep(2)
                counter=1
                continue
            else:
                
                print("Object Detected ! Sending it to Tensorflow !")
                print("Object Area =",cv2.contourArea(c))
                #cv2.imwrite("DetectedObject.jpg",image)
                #camera.close()
                counter=1
                #break
    except Exception as e:
        print(e)
        #pass
    cv2.imshow("DiffImage", diff)
    cv2.imshow("Reference Image",refImg)

    if key == ord('q'):
        camera.close()
        cv2.destroyAllWindows()
        break
