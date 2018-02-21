from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2,os
import numpy as np
import threading
import RPi.GPIO as GPIO
import time,os,sys
import bluetooth

port = 1
MotorPin1   = 11    # pin11
MotorPin2   = 12    # pin12
MotorEnable1 = 13    # pin13

MotorPin3   = 15    # pin11
MotorPin4   = 16    # pin12
MotorEnable2 = 18

Motor_speed_f=34
Motor_speed_b=30
Motor_speed_r=37
Motor_speed_l=37

stop=0
base_on=0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)          # Numbers GPIOs by physical location
GPIO.setup(MotorPin1, GPIO.OUT)   # mode --- output
GPIO.setup(MotorPin2, GPIO.OUT)
GPIO.setup(MotorEnable1, GPIO.OUT)
#GPIO.output(MotorEnable1, GPIO.LOW) # motor stop
GPIO.setup(MotorPin3, GPIO.OUT)   # mode --- output
GPIO.setup(MotorPin4, GPIO.OUT)
GPIO.setup(MotorEnable2, GPIO.OUT)
#GPIO.output(MotorEnable2, GPIO.LOW)
pwm1=GPIO.PWM(13,100)
pwm2=GPIO.PWM(18,100)
pwm1.start(0)
pwm2.start(0)

def forward():
        global start
        pwm1.ChangeDutyCycle(Motor_speed_f)
        pwm2.ChangeDutyCycle(Motor_speed_f)
        GPIO.output(MotorPin1, GPIO.HIGH)  # clockwise
        GPIO.output(MotorPin2, GPIO.LOW)
        GPIO.output(MotorPin3, GPIO.LOW)  # clockwise
        GPIO.output(MotorPin4, GPIO.HIGH)
        
        start=time.time()
        
def backward():
        global start
        pwm1.ChangeDutyCycle(Motor_speed_b)
        pwm2.ChangeDutyCycle(Motor_speed_b)
        GPIO.output(MotorPin1, GPIO.LOW)   # anticlockwise
        GPIO.output(MotorPin2, GPIO.HIGH)
        GPIO.output(MotorPin3, GPIO.HIGH)  # clockwise
        GPIO.output(MotorPin4, GPIO.LOW)
        
        start=time.time()

def left():
        global start
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(Motor_speed_l)
        GPIO.output(MotorPin1, GPIO.LOW)  # clockwise
        GPIO.output(MotorPin2, GPIO.LOW)
        GPIO.output(MotorPin3, GPIO.LOW)  # clockwise
        GPIO.output(MotorPin4, GPIO.HIGH)
        
        start=time.time()

def right():
        global start
        pwm1.ChangeDutyCycle(Motor_speed_r)
        pwm2.ChangeDutyCycle(0)
        GPIO.output(MotorPin1, GPIO.HIGH)   # anticlockwise
        GPIO.output(MotorPin2, GPIO.LOW)
        GPIO.output(MotorPin3, GPIO.LOW)  # clockwise
        GPIO.output(MotorPin4, GPIO.LOW)
        
        start=time.time()

def stop():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)

def destroy():
        client_socket.close()
        server_socket.close()
        stop()
        GPIO.cleanup() 

def loop():
        server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        server_socket.bind(("",port))
        server_socket.listen(1)
        
        client_socket,address = server_socket.accept()
        while True:
                
                data = client_socket.recv(1024)
                if data.decode('utf-8')=='f':
                        #start=time.time()
                        flag="forward"
                        forward()
                elif data.decode('utf-8')=='b':
                        #start=time.time()
                        flag="backward"
                        backward()
                        
                elif data.decode('utf-8')=='l':
                        #start=time.time()
                        flag="left"
                        left()
                elif data.decode('utf-8')=='r':
                        #start=time.time()
                        flag="right"
                        right() 
                        
                elif data.decode('utf-8')=='s':
                        
                        
                        stop()
                        end=time.time()
                        global start
                        difference=(end-start)
                        
                        if not flag=="":
                                with open("Database.txt","a+")as f:
                                        f.write(flag+"   "+str(difference)+"\n")
                                flag=""
                                end=0
                                start=0
                                difference=0
                elif data.decode('utf-8')=='q':
                        stop()
                        GPIO.cleanup()
                        sys.exit()
def autonomous():
        global base_on
        base_on=1
        with open("Database.txt","r")as f:
                data=f.readlines()
        for row in data:
                row=row.rstrip("\n")
                direction,duration=row.split()
                if direction=="forward":
                        forward()
                        end=time.time()+float(duration)
                        while (end>=time.time()):
                                global stop
                                if stop==1:
                                  stop()
                                  remaining_time=end-time.time()
                                  print("Stopped the vehicle")
                                  global stop
                                  while stop==1:
                                    continue
                                  print("Resumed the vehicle")
                                  forward()
                                  end=time.time()+remaining_time

                                continue
                elif direction=="backward":
                        backward()
                        end=time.time()+float(duration)
                        while (end>=time.time()):
                                continue
                        #stop()
                elif direction=="left":
                        left()
                        end=time.time()+float(duration)
                        while (end>=time.time()):
                                continue
                        #stop()
                elif direction=="right":
                        right()
                        end=time.time()+float(duration)
                        while (end>=time.time()):
                                continue
                        #stop()
        stop()
        print("Base movement finished")
        global base_on
        base_on=0
                
                  

def imageSubtract(img):
    #img = cv2.bilateralFilter(img,3,60,60)  
    yuv=cv2.cvtColor(img,cv2.COLOR_BGR2LUV)
    l,u,v=cv2.split(yuv)
    #y=cv2.equalizeHist(y)
    return v


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

    first_time=0
    frame_buffer=0
    counter=0
    camera.start_preview()
    sleep(1)

    global base_on
    while base_on==0:
      continue
   

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
        if first_time==0:
            rawCapture.truncate(0)
            if frame_buffer<10:
               print("Frame rejected -",str(frame_buffer))
               frame_buffer+=1
               continue
            os.system("clear")
            refImg=frame.array
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
            if counter=0:
                print("Going to sleep for 2 second")
                time.sleep(2)
                counter=1
                continue
            else:
                global stop
                stop=1
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
                counter=0

           else:
            global stop
            stop=0

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
  try:
                choice=input("Enter-  1. Plan path . 2. Autonomous movement\n")
                if choice == "2":
                        if os.path.exists(os.getcwd()+"/Database.txt")==True:
                                t1=threading.Thread(target=autonomous)
                                t2=threading.Thread(target=imageProcessing)
                                t1.start()
                                t2.start()
                                print("Started both the threads succesfully !")

                                #autonomous()
                                #stop()
                                #sys.exit()
                        else:
                                print("Database not found . Please plan the path ..")
                                loop()
                                
                elif choice=="1":
                        os.remove('Database.txt')
                        loop()
  except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()
