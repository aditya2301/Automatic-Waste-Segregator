from picamera.array import PiRGBArray
from picamera import PiCamera
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import cv2,sys
import time
import numpy as np
import picamera.array
import os , io


def imageSubtract(img):
    blur = cv2.GaussianBlur(img,(5,5),0)
    ret,thresh = cv2.threshold(blur,65,255,cv2.THRESH_BINARY_INV)
    return thresh

def googleApi():
    #cv2.imshow("Detected Object",cv2.imread("DetectedObject.jpg"))
    time.sleep(2)
    camera = PiCamera()
    camera.resolution=(512,512)
    time.sleep(10)
    camera.start_preview()
    camera.capture('/home/pi/Desktop/DetectedObjects.jpg')
    camera.stop_preview()
    camera.close()
    time.sleep(2)
    
    image = ClImage(file_obj=open('/home/pi/Desktop/DetectedObjects.jpg', 'rb'))
    
    print('\n\nThe detected Labels:')
    l=model.predict([image])['outputs'][0]['data']['concepts']
    for i in l:
        print(i['name'])
    print("\n\n")
    



app = ClarifaiApp(api_key='df0093d074f8489c88cc8bb7894b94c9')
model = app.models.get("general-v1.3")

#Clicking the reference image and storing it in refimg variable
camera = PiCamera()
#camera.resolution = (320, 240)
camera.resolution = (500, 500)
camera.framerate = 30
camera.flash_mode='off'
rawCapture = PiRGBArray(camera, size=(500, 500))
#display_window = cv2.namedWindow("Faces")

first_time=0
counter=0
time.sleep(4)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    if first_time==0:
        os.system("clear")
        time.sleep(4)
        refImg=frame.array
        refImg=cv2.cvtColor(refImg,cv2.COLOR_BGR2GRAY)
        refThresh=imageSubtract(refImg)
        first_time=1

    
    image = frame.array
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.imshow("NewImage", gray)
    key = cv2.waitKey(1)

    rawCapture.truncate(0)

    newThresh=imageSubtract(gray)
    diff=cv2.absdiff(refThresh,newThresh)
    diff=cv2.bitwise_xor(diff,refThresh)
    kernel = np.ones((3,3),np.uint8)
    diff=cv2.erode(diff,kernel,iterations = 4)
    diff=cv2.dilate(diff,kernel,iterations = 2)
    try:
    
        _, contours, _= cv2.findContours(diff,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        c=max(contours,key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(diff,(x,y),(x+w,y+h),(125,125,125),2)
        if cv2.contourArea(c)>500:
            if counter==0:
                print("Object entering frame . Going into sleep for 2 sec and resuming")
                time.sleep(2)
                counter=1
                continue
            else:
                
                print("Object Detected ! Sending it to Vision API !")
                print("Object Area =",cv2.contourArea(c))
                #cv2.imwrite("DetectedObject.jpg",image)
                camera.close()
                googleApi()
                counter=1
                break
            
            #break
    except Exception as e:
        #print(e)
        pass
  

    #cv2.imshow("DiffImage", diff)
    #cv2.imshow("Reference Image",refImg)

    if key == 27:
        camera.close()
        cv2.destroyAllWindows()
        break
sys.exit()
