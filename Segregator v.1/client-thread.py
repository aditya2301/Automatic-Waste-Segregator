# This script contains the client side program which runs on the Raspberry Pi 3.
# The following dependencies are imported.
# picamera ---> PiCamera library.
# cv2 ---> OpenCV for Image Processing.
# os ---> system file handling.
# multhreading ---> Runs multiple threads at a time.
# socket ---> To create the connection to remote cloud system.
# bluetooth ---> To receive the commands to control the bot via bluetooth.
# RPi.GPIO ---> Raspberry Pi GPIO handling.
# servoControl ---> Contains codes for controlling the robotic arm.

from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2,os,socket,sys
import numpy as np
import threading
import RPi.GPIO as GPIO
import time,os,sys
import bluetooth
import servoControl

# MotorPinX ---> GPIO pins to control the wheels.

MotorPin1   = 11    # pin11
MotorPin2   = 12    # pin12
MotorEnable1 = 13    # pin13
MotorPin3   = 16    # pin11
MotorPin4   = 15    # pin12
MotorEnable2 = 18

# Motor_speed_X ---> Manipulate this to control the RPM of the DC motor.

Motor_speed_f=50#41#34
Motor_speed_b=50#41#30
Motor_speed_r=50#41#37
Motor_speed_l=50#41#37

stop_flag=0
base_off=0

# GPIO settings of each I/O pins.
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)          # Numbers GPIOs by physical location. ALternative ---> BCM.
GPIO.setup(MotorPin1, GPIO.OUT)   # mode --- output
GPIO.setup(MotorPin2, GPIO.OUT)
GPIO.setup(MotorEnable1, GPIO.OUT)
GPIO.setup(MotorPin3, GPIO.OUT)   # mode --- output
GPIO.setup(MotorPin4, GPIO.OUT)
GPIO.setup(MotorEnable2, GPIO.OUT)

# Initialize the PWM signals on the MotorEnable Pins.

pwm1=GPIO.PWM(13,100)
pwm2=GPIO.PWM(18,100)
pwm1.start(0)
pwm2.start(0)

# The following sections contains code for controlling the motion of the wheels.
# forward() ---> consists of mechanism to control the forward rotation of the wheel.
# start ---> a counter to record the time spent in that particular direction.

def forward():
        global start
        pwm1.ChangeDutyCycle(Motor_speed_f)
        pwm2.ChangeDutyCycle(Motor_speed_f)
        GPIO.output(MotorPin1, GPIO.HIGH)  # clockwise
        GPIO.output(MotorPin2, GPIO.LOW)
        GPIO.output(MotorPin3, GPIO.LOW)  # clockwise
        GPIO.output(MotorPin4, GPIO.HIGH)
        start=time.time()
        
# backward() ---> consists of mechanism to control the backward rotation of the wheel.
# start ---> a counter to record the time spent in that particular direction.

def backward():
        global start
        pwm1.ChangeDutyCycle(Motor_speed_b)
        pwm2.ChangeDutyCycle(Motor_speed_b)
        GPIO.output(MotorPin1, GPIO.LOW)   # anticlockwise
        GPIO.output(MotorPin2, GPIO.HIGH)
        GPIO.output(MotorPin3, GPIO.HIGH)  # clockwise
        GPIO.output(MotorPin4, GPIO.LOW)
        start=time.time()

# left() ---> consists of mechanism to control the left rotation of the wheel.
# start ---> a counter to record the time spent in that particular direction.

def left():
        global start
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(Motor_speed_l)
        GPIO.output(MotorPin1, GPIO.LOW)  # clockwise
        GPIO.output(MotorPin2, GPIO.LOW)
        GPIO.output(MotorPin3, GPIO.LOW)  # clockwise
        GPIO.output(MotorPin4, GPIO.HIGH)
        start=time.time()

# right() ---> consists of mechanism to control the right rotation of the wheel.
# start ---> a counter to record the time spent in that particular direction.

def right():
        global start
        pwm1.ChangeDutyCycle(Motor_speed_r)
        pwm2.ChangeDutyCycle(0)
        GPIO.output(MotorPin1, GPIO.HIGH)   # anticlockwise
        GPIO.output(MotorPin2, GPIO.LOW)
        GPIO.output(MotorPin3, GPIO.LOW)  # clockwise
        GPIO.output(MotorPin4, GPIO.LOW)
        start=time.time()

# stop() ---> consists of mechanism to stop the rotation of the wheel.

def stop():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)

'''destroy() ---> It stops the wheel rotation, clean GPIO of 
any stray output voltages and also closes the socket connection 
with the Bluetooth client device.'''

def destroy():
        client_socket.close()
        server_socket.close()
        stop()
        GPIO.cleanup() 

''' 
* The following function handles the communication with the Cloud system where Machine Learning 
analysis of the image takes place.

* The IP address is hardcoded here which is generally considered a bad practice. 
  Avoid hardcoding any value.

* img ---> refers to the image of the detected image.
* s---> instance of the socket class.
* data ---> stores the byte content of the image.
* length ---> length of the total bytes in data.
* status ---> acknowledgemnt from server.
*  binFlag ---> Direction to rotate the flap.
'''

def clientResponse(img):
	#os.system("clear")
	cv2.imwrite("newimg.jpg",img)
	s = socket.socket()         
	port = 60000              
	s.connect(('192.168.2.4', port))
	print("connected")
	f=open("newimg.jpg","rb")
	data=f.read()
	f.close()
	print("\nSending Length information..")
	length=str(len(data))
	s.send(bytes(length,"utf-8"))
	
	status=s.recv(2)
	print("Length Reception Acknowledgement - "+str(status.decode("utf-8")))
	print("Sending the image to server for Tensorflow processing. . .")
	f=open("newimg.jpg","rb")
	data=f.read(1)
	# Progress bar to indicate status of sending the image.
	length=int(length)
	count=0
	counter=0
	slab=int(length/10)
	print("\nProgress-")
	while data:
		s.send(data)
		data=f.read(1)
		count+=1
		if count==slab:
		    counter+=1
		    sys.stdout.write('\r')
		    sys.stdout.write('['+"#"*counter+" "*(10-counter)+']'+" "+str(counter*10)+"%")
		    sys.stdout.flush()
		    count=0
	sys.stdout.write("\n")
	sys.stdout.flush()
	print("Sent sucessfully!")
	f.close()
	
	binFlag=s.recv(20)
	print("Server response received.")
	if str(binFlag.decode("utf-8"))=="l":
		print("Object is biodegradable. Rotating bin on the left side.")
	elif str(binFlag.decode("utf-8"))=="r":
		print("Object is non-biodegradable. Rotating bin on the right side.")
	s.close()
	os.system("clear")
	return binFlag.decode("utf-8")

'''
* The following function contains code for planning the path of the bot.
* 'f' ---> forward , 'b' ---> backward , 'l' ---> left, 'r' ---> right.
* difference ---> stores the time difference betwween start and stop of
  naviagtion in one particular direction.

* The database is updated in the format of ---> direction duration.
'''

def loop():
        server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        server_socket.bind(("",port))
        server_socket.listen(1)
        client_socket,address = server_socket.accept()
        while True:
                data = client_socket.recv(1024)
                if data.decode('utf-8')=='f':
                        flag="forward"
                        forward()
                elif data.decode('utf-8')=='b':
                        flag="backward"
                        backward()
                elif data.decode('utf-8')=='l':
                        flag="left"
                        left()
                elif data.decode('utf-8')=='r':
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
                        destroy()

'''
* The following functions controls the movement of the bot in autonomous mode.
* A delay of 3 seconds is included to allow the Camera function to execute.
* The following function is run as a seprate threads to allow parallel movement of bot 
  along with the camera processing.

* The database values are fetched ---> direction duration.
* The bot is moved in the direction for that particular duration before the direction is changed.
* stop_flag --> 1, when Camera picks up an object in its path. Otherwise, 0. 
* base_off ---> indicates end of the path.
'''

def autonomous():
        current_time=time.time()+3
        while time.time()<=current_time:
            continue  # This is to give 3 seconds warm up time for the Image processing module.

        with open("Database.txt","r") as f:
                data=f.readlines()
        for i in range(0,len(data)):
        	    data[i]=data[i].rstrip("\n")

        for row in data:
                direction,duration=row.split()
                if direction=="forward":
                        forward()
                        end=time.time()+float(duration)
                        while (end>=time.time()):
                                global stop_flag
                                if stop_flag==1:
                                  stop()
                                  remaining_time=end-time.time()
                                  print("Stopped the vehicle")
                                  global stop
                                  while stop_flag==1:
                                    continue
                                  print("Resumed the vehicle")
                                  forward()
                                  end=time.time()+remaining_time
                                continue
                elif direction=="backward":
                        backward()
                        end=time.time()+float(duration)
                        while (end>=time.time()):
                                global stop_flag
                                if stop_flag==1:
                                  stop()
                                  remaining_time=end-time.time()
                                  print("Stopped the vehicle")
                                  global stop_flag
                                  while stop_flag==1:
                                    continue
                                  print("Resumed the vehicle")
                                  backward()
                                  end=time.time()+remaining_time
                                continue
                elif direction=="left":
                        left()
                        end=time.time()+float(duration)
                        while (end>=time.time()):
                                global stop_flag
                                if stop_flag==1:
                                  stop()
                                  remaining_time=end-time.time()
                                  print("Stopped the vehicle")
                                  global stop_flag
                                  while stop_flag==1:
                                    continue
                                  print("Resumed the vehicle")
                                  left()
                                  end=time.time()+remaining_time
                                continue
                elif direction=="right":
                        right()
                        end=time.time()+float(duration)
                        while (end>=time.time()):
                                global stop_flag
                                if stop_flag==1:
                                  stop()
                                  remaining_time=end-time.time()
                                  print("Stopped the vehicle")
                                  global stop_flag
                                  while stop_flag==1:
                                    continue
                                  print("Resumed the vehicle")
                                  right()
                                  end=time.time()+remaining_time
                                continue
        stop()
        print("Base movement finished")
        global base_off
        base_off=1
                
                  
# The following function converts the RGB image into LUV color space.
def imageSubtract(img):
    yuv=cv2.cvtColor(img,cv2.COLOR_BGR2LUV)
    l,u,v=cv2.split(yuv)
    return v

'''
* The following function analyses the path of the bot for thr presence of any object.
* camera ---> Initialises to PiCamera class.
* First 10 frames are rejected to properly intialise the camera on startup.
* Reference image and new images are subtracted.
* Contours of size > 300 and number <3 are searched. If found, object is detected.
* cX, cY ---> centre of the object in the image frame.
* The image frame is divided into 2 quadrants for ease of the robotic arm to identify the onject's position.
* The object is picked up by invoking the appropriate servoControl function.
* binDir ---> contains the ML analysis of the detected object.
* The background image is refreshed after every 30 frames for maintaining keeping noise effects to minimum.
'''

def  imageProcessing():
    x=440
    y=252
    vertical=int(x/2)
    horizontal=int(y/2)
    
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
    sleep(1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if first_time==0:
            rawCapture.truncate(0)
            if frame_buffer<10:
               print("Frame rejected -",str(frame_buffer))
               frame_buffer+=1
               continue
            os.system("clear")
            refImg=frame.array
            refImg=refImg[260:512,50:490]
            refThresh=imageSubtract(refImg)
            first_time=1
            frame_buffer=0


        frame_buffer+=1
        image = frame.array
        image=image[260:512,50:490]
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
           if cv2.contourArea(c)>300 and len(contours)<=3:
            if counter==0:
                print("Going to sleep for 0.1 second")
                time.sleep(0.1)
                counter=1
                continue
            else:
                global stop_flag
                stop_flag=1
                os.system("clear")
                M=cv2.moments(c)
                cX = int(M['m10']/M['m00'])
                cY = int(M['m01']/M['m00'])
                print("Total contours found=",len(contours))
                print("Object detected with area = ",cv2.contourArea(c))
                print("Object's X,Y=",cX,cY)
                print("Object is located at = ",end="")
                if  cX<vertical:
                    print("Object located in 1st Quadrant")
                    binDir=clientResponse(image)
                    servoControl.quadrant2(binDir)
                    first_time=0
                    frame_buffer=0
                    continue
                elif  cX>vertical:
                    print("Object located 2nd Quadrant")
                    binDir=clientResponse(image)
                    servoControl.quadrant1(binDir)
                    first_time=0
                    frame_buffer=0
                    continue
                elif cX==vertical:
                    print(" Object located between 1 and 2nd Quadrant")
                    binDir=clientResponse(iamge)
                    servoControl.quadrant12(binDir)
                    first_time=0
                    frame_buffer=0
                    continue
                counter=0
           else:
            global stop_flag
            stop_flag=0

           cv2.imshow("Threshold",thresholded)
           if frame_buffer%30==0:
              frame_buffer=0
              refImg=image
              refThresh=imageSubtract(refImg)
              os.system("clear")
              print("Refrence Image changed")
           
           global base_off
           if key == ord('q') or base_off==1:
               camera.close()
               cv2.destroyAllWindows()
               break
        except Exception as e:
            print(e)
            pass

'''
* The program execution begins from here.
* 1 ---> For setting the path via bluetooth client.
* 2 ---> Autonomous movement and detecting waste.
* t1 ---> Thread 1 which controls the base movement.
* t2 ---> PThread 2 which controls the Image Processing.
* stop_flag is set to 1 by ImageProcessing funtion whenevr an object is detected. It stops the bot from moving.
* base_off is set to 1 by baseMovement function after the complete path is traversed.
'''

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
                        else:
                                print("Database not found . Please plan the path ..")
                                loop()
                                
                elif choice=="1":
                        os.remove('Database.txt')
                        loop()
  except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()