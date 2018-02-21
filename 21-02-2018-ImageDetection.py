from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2,os
import numpy as np
import threading


def imageSubtract(img):
    #img = cv2.bilateralFilter(img,3,60,60)  
    yuv=cv2.cvtColor(img,cv2.COLOR_BGR2LUV)
    l,u,v=cv2.split(yuv)
    #y=cv2.equalizeHist(y)
    return v

def contourWindow(c):
    x=422
    y=512
    vertical=int(x/2)
    horizontal=int(y/2)
    
    quadrant= np.zeros((512,422),np.uint8)
    cv2.line(quadrant,(vertical,0),(vertical,y),(255,0,0),3)#vertical line
    cv2.line(quadrant,(0,horizontal),(x,horizontal),(159,73,14),3)
    cv2.drawContours(quadrant, [c] , 0, (126,76,0), -1)
    cv2.imshow("quadrant",quadrant)
    print("contour function called")
    return 1

def  imageProcessing():
    x=422
    y=512
    vertical=int(x/2)
    horizontal=int(y/2)
    
    camera = PiCamera()
    camera.resolution = (512,512)
    #camera.zoom=(0.0,0.0,0.4,0.5)
    camera.awb_mode="fluorescent"
    camera.iso = 800
    camera.contrast=25
    camera.brightness=64
    camera.sharpness=100
    rawCapture = PiRGBArray(camera, size=(512, 512))

    is_quadrantWindow_open=0
    sleep_time=0
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
            #y,x=refImg.shape
            
            refImg=refImg[0:512,0:512-90]
            refThresh=imageSubtract(refImg)
            first_time=1
            frame_buffer=0


        frame_buffer+=1
        
        
        
        
        image = frame.array
        image=image[0:512,0:512-90]
        cv2.imshow("Foreground", image)
        key = cv2.waitKey(1)
        rawCapture.truncate(0)
        newThresh=imageSubtract(image)

        diff=cv2.absdiff(refThresh,newThresh)
        kernel = np.ones((5,5),np.uint8)
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)
        #diff=cv2.erode(diff,kernel,iterations = 2)
        diff=cv2.dilate(diff,kernel,iterations = 2)
        cv2.imshow("Background",refImg)
        _, thresholded = cv2.threshold(diff, 0 , 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)
        
        

        _, contours, _= cv2.findContours(thresholded,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        try:
           c=max(contours,key=cv2.contourArea)
           x,y,w,h = cv2.boundingRect(c)
           
           cv2.rectangle(thresholded,(x,y),(x+w,y+h),(125,125,125),2)
           if cv2.contourArea(c)>300 and len(contours)<=5:
              os.system("clear")
              M=cv2.moments(c)
              cY = int(M['m10']/M['m00'])
              cX = int(M['m01']/M['m00'])
              print("Total contours found=",len(contours))
              print("Object detected with area = ",cv2.contourArea(c))
              print("Object's X,Y=",cX,cY)

              print("Object is located at = ",end="")
              if cX<horizontal and cY<vertical:
                  print("1st Quadrant")
              elif cX<horizontal and cY>vertical:
                  print("2nd Quadrant")
              elif cX>horizontal and cY<vertical:
                  print("3rd Quadrant")
              elif cX>horizontal and cY>vertical:
                  print("4th Quadrant")
              elif cX==horizontal and cY<vertical:
                  print("Between 1 and 3rd Quadrant")
              elif cX==horizontal and cY>vertical:
                  print("Between 2 and 4th Quadrant")
              elif cX<horizontal and cY==vertical:
                  print("Between 1 and 2nd Quadrant")
              elif cX>horizontal and cY==vertical:
                  print("Between 3 and 4th Quadrant")
              else:
                  print("Right at the centre !")

              
           
           cv2.imshow("Threshold",thresholded)
           if frame_buffer%40==0:
              refImg=image
              #refImg=refImg[0:x,0:y-90]
              refThresh=imageSubtract(refImg)
              os.system("clear")
              print("Refrence Image changed")
           if key == ord('q'):
               camera.close()
               cv2.destroyAllWindows()
               break
           #print(frame_buffer)
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__" :
   imageProcessing()
