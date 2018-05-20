import cv2
import numpy as np
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
'''camera = PiCamera()
camera.resolution = (512,512)
#camera.zoom=(0.5,0.5,0.9,0.9)
camera.awb_mode="fluorescent"
camera.iso = 800
camera.contrast=25
camera.brightness=64
camera.sharpness=100
rawCapture = PiRGBArray(camera, size=(512, 512))
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	image=image[160:490,20:]
	cv2.imshow("Foreground", image)
	key = cv2.waitKey(1)	
	rawCapture.truncate(0)
	if key==ord('q'):
		cv2.destroyAllWindows()
		break'''

def imageSubtract(img):
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return hsv

def  imageProcessing():
    camera = PiCamera()
    camera.resolution = (512,512)
    #camera.zoom=(0.0,0.0,0.4,0.5)
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
    time.sleep(1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if first_time==0:
            rawCapture.truncate(0)
            if frame_buffer<30:
                print("Frame rejected -",str(frame_buffer))
                frame_buffer+=1
                continue
            #os.system("clear")
            refImg=frame.array
            refImg=refImg[40:490,25:]
            refThresh=imageSubtract(refImg)
            first_time=1
            frame_buffer=0

        frame_buffer+=1

        image = frame.array
        image=image[40:490,25:]
        rawCapture.truncate(0)
        newThresh=imageSubtract(image)
        cv2.imshow("Foreground", newThresh)
        cv2.imshow("Background", refThresh)
        key = cv2.waitKey(1)
        if key == ord('q'):
            camera.close()
            cv2.destroyAllWindows()
            break
imageProcessing()