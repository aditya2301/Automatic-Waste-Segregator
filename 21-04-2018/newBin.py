from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2,os,socket,sys,time
import numpy as np





def imageSubtract(img):
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
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
            if frame_buffer<10:
                print("Frame rejected -",str(frame_buffer))
                frame_buffer+=1
                continue
            os.system("clear")
            refImg=frame.array
            #refImg=refImg[260:512,50:490]
            refThresh=imageSubtract(refImg)
            first_time=1
            frame_buffer=0

        frame_buffer+=1

        image = frame.array
        
        rawCapture.truncate(0)
        newThresh=imageSubtract(image)
        cv2.imshow("Foreground", newThresh)
        key = cv2.waitKey(1)

        diff=cv2.absdiff(refThresh,newThresh)
        #cv2.imshow("subtracted",diff)
        cv2.imshow("Background",refThresh)
        diff=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        kernel = np.ones((5,5),np.uint8)
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)
        diff=cv2.erode(diff,kernel,iterations = 2)
        diff=cv2.dilate(diff,kernel,iterations = 4)

        _, thresholded = cv2.threshold(diff, 0 , 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)
        _, contours, _= cv2.findContours(thresholded,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print("Total contours ",len(contours))
        try:
            c=max(contours,key=cv2.contourArea)
            mask = np.zeros(newThresh.shape[:2],np.uint8)
            new_image = cv2.drawContours(mask,[c],0,255,-1,)
            cv2.imshow("new",new_image)
            cv2.imshow("threshold",thresholded)
            if cv2.contourArea(c)>300 and len(contours)<=3:
                if counter==0:
                    print("Possible object detcted ! Going to sleep for 2 seconds")
                    time.sleep(2)
                    counter=1
                    continue
                else:
                    os.system("clear")
                    M=cv2.moments(c)
                    cX = int(M['m10']/M['m00'])
                    cY = int(M['m01']/M['m00'])
                    print("Total contours found=",len(contours))
                    print("Object detected with area = ",cv2.contourArea(c))

                    '''binDir=clientResponse(iamge)
                    flap(binDir) # call the flap function
                    first_time=0
                    frame_buffer=0
                    counter=0
                    print("Waste segregated !")'''
                    continue
            
        except Exception as e:
            print(e)
            pass
            
        if key == ord('q'):
            
            camera.close()
            cv2.destroyAllWindows()
            break

       

if __name__ == "__main__" :
    try:

        imageProcessing()
        print("Started the system !")
                       
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        GPIO.cleanup() 