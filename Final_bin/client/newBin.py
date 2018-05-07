from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2,os,socket,sys,time,Adafruit_PCA9685
import numpy as np
from twilio.rest import Client
import RPi.GPIO as GPIO

import lcd
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line


def default_lcd_msg():
    lcd.lcd_string("Automatic Waste",LCD_LINE_1)
    lcd.lcd_string("Segregation",LCD_LINE_2)
    time.sleep(2)

      
def sendSMS(msg):
    account_sid = "AC3b65d4b08b4242625715cb559f5410b0"
    auth_token = "a4f4e1298494f1e9f166df22e48912f2"
    client = Client(account_sid, auth_token)
    client.api.account.messages.create(to="+918147661833",from_="+18043125524",body=msg)
    print("SMS sent !")


def binStatus():

    
    bio = GPIO.input(37)
    nonbio= GPIO.input(38)
    if  GPIO.input(37) != False : #object is near   
        time.sleep(2)
        if  GPIO.input(37) != False :
            msg="Biodegradable bin is full. Please REPLACE."
            lcd.lcd_string("Alert!!!",LCD_LINE_1)
            lcd.lcd_string("Bio bin full",LCD_LINE_2)
            sendSMS(msg)
            print(msg)
            time.sleep(2)
    
    if  GPIO.input(38) != False : #object is near  
        time.sleep(2)
        if  GPIO.input(38) !=False :
            msg="Non-biodegradable bin is full. Please REPLACE."
            lcd.lcd_string("Alert!!!",LCD_LINE_1)
            lcd.lcd_string("Non-Bio bin full",LCD_LINE_2)
            sendSMS(msg)
            print(msg)
            time.sleep(2)

    print("Bin status is updated !")
    default_lcd_msg()


def flap(direction):
    print("Operating flap..")
    center=185
    left=80
    right=340
    pin=0
    if direction=='l':
        for i in range(center,left,-1):
            pwm.set_pwm(pin,0,i)
            time.sleep(0.01)
        time.sleep(2)
        for i in range(left,215,1):
            pwm.set_pwm(pin,0,i)
            time.sleep(0.01)
    elif direction=='r':
        center=170
        for i in range(center,right,1):
            pwm.set_pwm(pin,0,i)
            time.sleep(0.01)
        time.sleep(2)
        for i in range(right,center,-1):
            pwm.set_pwm(pin,0,i)
            time.sleep(0.01)


def clientResponse(img,Ip_addr):
    filename="newimg.jpg"
    cv2.imwrite(filename,img)
    #extractForegroundImage(filename)
    s = socket.socket()         
    port = 60000              
    s.connect((Ip_addr, port))
    print("Established connection.")
    f=open(filename,"rb")
    data=f.read()
    f.close()
    print("\nSending Length information..")
    length=str(len(data))
    s.send(bytes(length,"utf-8"))
    
    status=s.recv(2)
    print("Length Reception Acknowledgement - "+str(status.decode("utf-8")))
    print("Sending the image to Google Cloud for Tensorflow processing. . .")
    f=open(filename,"rb")
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
    
    binFlag=s.recv(1)
    print("Cloud response received.")
    if str(binFlag.decode("utf-8"))=="l":
        print("Object is biodegradable. Rotating bin on the left side.")
    elif str(binFlag.decode("utf-8"))=="r":
        print("Object is non-biodegradable. Rotating bin on the right side.")
    s.close()
    os.system("clear")
    return binFlag.decode("utf-8")




def imageSubtract(img):
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return hsv

def  imageProcessing(Ip_addr):
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
        key = cv2.waitKey(1)

        diff=cv2.absdiff(refThresh,newThresh)
        #cv2.imshow("subtracted",diff)
        cv2.imshow("Background",refThresh)
        diff=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        kernel = np.ones((5,5),np.uint8)
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)
        diff=cv2.erode(diff,kernel,iterations = 2)
        diff=cv2.dilate(diff,kernel,iterations = 6)

        _, thresholded = cv2.threshold(diff, 0 , 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)
        _, contours, _= cv2.findContours(thresholded,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print("Total contours ",len(contours))
        try:
            c=max(contours,key=cv2.contourArea)
            mask = np.zeros(newThresh.shape[:2],np.uint8)
            new_image = cv2.drawContours(mask,[c],0,255,-1,)
            cv2.imshow("new",new_image)
            cv2.imshow("threshold",thresholded)
            #print("Area ",str(cv2.contourArea(c)))
            #print("Total contours ",str(len(contours)))
            if cv2.contourArea(c)>500 and len(contours)<=4:
                if counter==0:
                    print("Possible object detcted ! Going to sleep for 3 seconds")
                    time.sleep(3)
                    counter=1
                    continue
                else:
                    os.system("clear")
                    M=cv2.moments(c)
                    cX = int(M['m10']/M['m00'])
                    cY = int(M['m01']/M['m00'])
                    print("Total contours found=",len(contours))
                    print("Object detected with area = ",cv2.contourArea(c))
                    lcd.lcd_string("Alert!!!",LCD_LINE_1)
                    lcd.lcd_string("Detected Object",LCD_LINE_2)
                    time.sleep(2)
                    binDir=clientResponse(image,Ip_addr)
                    lcd.lcd_string("Waste Detected:-",LCD_LINE_1)
                    if binDir=='l':
                        lcd.lcd_string("Biodegradable",LCD_LINE_2)
                    elif binDir=='r':
                        lcd.lcd_string("Non-Bio",LCD_LINE_2)
                    flap(binDir) # call the flap function
                    first_time=0
                    frame_buffer=0
                    counter=0
                    print("Waste segregated !")
                    time.sleep(2)
                    binStatus()
                    continue
                default_lcd_msg()
            
        except Exception as e:
            print(e)
            pass
        
        if key == ord('q'):
            camera.close()
            cv2.destroyAllWindows()
            break



if __name__ == "__main__" :
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(37,GPIO.IN) #GPIO 16 bio degradable 
        GPIO.setup(38,GPIO.IN) #GPIO 18 non bio degradable bin
    
        pwm = Adafruit_PCA9685.PCA9685()
        pwm.set_pwm_freq(50)
        print("Started the system !")
        lcd.main()
        default_lcd_msg()
        Ip_addr = input("Enter server's IP address for connection: ")
        imageProcessing(Ip_addr)
        
         
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        GPIO.cleanup() 
    except Exception as e:
        print(e)
