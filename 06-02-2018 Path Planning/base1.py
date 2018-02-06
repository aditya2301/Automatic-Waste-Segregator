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
def forward():
        GPIO.output(MotorEnable1, GPIO.HIGH) # motor driver enable
        GPIO.output(MotorPin1, GPIO.HIGH)  # clockwise
        GPIO.output(MotorPin2, GPIO.LOW)
        GPIO.output(MotorEnable2, GPIO.HIGH) # motor driver enable
        GPIO.output(MotorPin3, GPIO.LOW)  # clockwise
        GPIO.output(MotorPin4, GPIO.HIGH)
def backward():
        GPIO.output(MotorEnable1, GPIO.HIGH) # motor driver enable
        GPIO.output(MotorPin1, GPIO.LOW)   # anticlockwise
        GPIO.output(MotorPin2, GPIO.HIGH)
        GPIO.output(MotorEnable2, GPIO.HIGH) # motor driver enable
        GPIO.output(MotorPin3, GPIO.HIGH)  # clockwise
        GPIO.output(MotorPin4, GPIO.LOW)

def left():
        GPIO.output(MotorEnable1, GPIO.LOW) # motor driver enable
        GPIO.output(MotorEnable2, GPIO.HIGH) # motor driver enable
        GPIO.output(MotorPin3, GPIO.LOW)  # clockwise
        GPIO.output(MotorPin4, GPIO.HIGH)

def right():
        GPIO.output(MotorEnable1, GPIO.HIGH) # motor driver enable
        GPIO.output(MotorPin1, GPIO.HIGH)   # anticlockwise
        GPIO.output(MotorPin2, GPIO.LOW)
        GPIO.output(MotorEnable2, GPIO.LOW)
def stop():
        GPIO.output(MotorEnable1, GPIO.LOW) # motor stop
        GPIO.output(MotorEnable2, GPIO.LOW)
        
def setup():
        GPIO.setwarnings(False)
        server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        server_socket.bind(("",port))
        server_socket.listen(1)
        global client_socket
        client_socket,address = server_socket.accept()
        #print ("Accepted connection from ",address)
        GPIO.setmode(GPIO.BOARD)          # Numbers GPIOs by physical location
        GPIO.setup(MotorPin1, GPIO.OUT)   # mode --- output
        GPIO.setup(MotorPin2, GPIO.OUT)
        GPIO.setup(MotorEnable1, GPIO.OUT)
        GPIO.output(MotorEnable1, GPIO.LOW) # motor stop
        GPIO.setup(MotorPin3, GPIO.OUT)   # mode --- output
        GPIO.setup(MotorPin4, GPIO.OUT)
        GPIO.setup(MotorEnable2, GPIO.OUT)
        GPIO.output(MotorEnable2, GPIO.LOW)
        #print('Press Ctrl+C to end the program...')

def loop():
	while True:
                global client_socket
                data = client_socket.recv(1024)
                if data.decode('utf-8')=='f':
                        start=time.time()
                        flag="forward"
                        forward()
                elif data.decode('utf-8')=='b':
                        start=time.time()
                        flag="backward"
                        backward()
                        
                elif data.decode('utf-8')=='l':
                        start=time.time()
                        flag="left"
                        left()
                elif data.decode('utf-8')=='r':
                        start=time.time()
                        flag="right"
                        right() 
                        
                elif data.decode('utf-8')=='s':
                        
                        stop()
                        end=time.time()
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
                        sys.exit()
def autonomous():
        with open("Database.txt","r")as f:
                data=f.readlines()
        for row in data:
                row=row.rstrip("\n")
                direction,duration=row.split()
                if direction=="forward":
                        forward()
                        end=time.time()+float(duration)
                        while (end>time.time()):
                                continue
                        #stop()
                elif direction=="backward":
                        backward()
                        end=time.time()+float(duration)
                        while (end>time.time()):
                                continue
                        #stop()
                elif direction=="left":
                        left()
                        end=time.time()+float(duration)
                        while (end>time.time()):
                                continue
                        #stop()
                elif direction=="right":
                        right()
                        end=time.time()+float(duration)
                        while (end>time.time()):
                                continue
                        #stop()
def destroy():
        client_socket.close()
        server_socket.close()
        stop()
        GPIO.cleanup()                     # Release resource
        
if __name__ == '__main__':     # Program start from here
	setup()
	try:
                choice=input("Enter-  1. Plan path . 2. Autonomous movement\n")
                if choice == "2":
                        if os.path.exists(os.getcwd()+"/Database.txt")==True:
                                autonomous()
                                stop()
                                sys.exit()
                        else:
                                print("Database not found . Please plan the path ..")
                                loop()
                                
                elif choice=="1":
                        loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
