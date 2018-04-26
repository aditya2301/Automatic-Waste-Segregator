from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2,os,socket,sys,time
import numpy as np
import RPi.GPIO as GPIO
from twilio.rest import Client


def sendSMS(msg):
    account_sid = "AC3b65d4b08b4242625715cb559f5410b0"
    auth_token = "a4f4e1298494f1e9f166df22e48912f2"
    client = Client(account_sid, auth_token)
    client.api.account.messages.create(to="+918147661833",from_="+18043125524",body=msg)
    print("SMS sent !")


def binStatus():

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16,GPIO.IN) #GPIO 16 bio degradable 
    GPIO.setup(18,GPIO.IN) #GPIO 18 non bio degradable bin
    
    
    bio = GPIO.input(16)
    nonbio= button_state = GPIO.input(18)
    if bio != False : #object is near   
        time.sleep(2)
        if bio!=False :
            msg="Biodegradable bin is full. Please replace."
            sendSMS(msg)
    
    if nonbio != False : #object is near  
        time.sleep(2)
        if nonbio!=False :
            msg="Non-biodegradable bin is full. Please replace."
            sendSMS(msg)

    print("Bin status is updated !")


def flap(direction):
    print("Operating flap..")
    center=260
    left=60
    right=500
    pin=0
    if direction=='l':
        for i in range(center,left,-1):
            pwm.set_pwm(pin,0,i)
            #time.sleep(0.01)
        time.sleep(2)
        for i in range(left,center,1):
            pwm.set_pwm(pin,0,i)
            #time.sleep(0.01)
    elif direction=='r':
        center=350
        for i in range(center,right,1):
            pwm.set_pwm(pin,0,i)
            #time.sleep(0.01)
        time.sleep(2)
        for i in range(right,center,-1):
            pwm.set_pwm(pin,0,i)


def extractForegroundImage(img_name):
    img_rgb = cv2.imread(img_name)

    img = cv2.cvtColor(img_rgb,cv2.COLOR_RGB2HSV)
    img = cv2.bilateralFilter(img,9,105,105)

    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    ret,thresh_image = cv2.threshold(gray,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    equalize= cv2.equalizeHist(thresh_image)


    canny_image = cv2.Canny(equalize,250,255)
    canny_image = cv2.convertScaleAbs(canny_image)
    kernel = np.ones((3,3), np.uint8)
    dilated_image = cv2.dilate(canny_image,kernel,iterations=1)

    new,contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours= sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    c=contours[0]
    final = cv2.drawContours(img, [c], -1, (255,0, 0), 3)

    mask = np.zeros(img_rgb.shape[:2],np.uint8)
    new_image = cv2.drawContours(mask,[c],0,255,-1,)
    new_image = cv2.bitwise_and(img_rgb,img_rgb,mask=mask)

    cv2.imwrite(img_name,new_image)


def clientResponse(img):
	#os.system("clear")
    filename="newimg.jpg"
	cv2.imwrite(filename,img)
    #extractForegroundImage(filename)
	s = socket.socket()         
	port = 60000              
	s.connect(("192.168.2.8", port))
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

def  imageProcessing():
    x=440
    y=252
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
        #kernel = np.ones((5,5),np.uint8)
        #diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)
        #diff=cv2.erode(diff,kernel,iterations = 2)
        #diff=cv2.dilate(diff,kernel,iterations = 2)
        cv2.imshow("Background",refImg)
        diff=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        _, thresholded = cv2.threshold(diff, 0 , 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)
        _, contours, _= cv2.findContours(thresholded,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        try:
            c=max(contours,key=cv2.contourArea)

            mask = np.zeros(newThresh.shape[:2],np.uint8)
            new_image = cv2.drawContours(mask,[c],0,255,-1,)
            cv2.namedWindow("detected",cv2.WINDOW_NORMAL)
            cv2.imshow("detected",new_image)
            #x,y,w,h = cv2.boundingRect(c)
            #cv2.rectangle(thresholded,(x,y),(x+w,y+h),(125,125,125),2)
            if cv2.contourArea(c)>300:
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

                    print("Object detected with area = ",cv2.contourArea(c))
                    print("Object's X,Y=",cX,cY)
        

                    binDir=clientResponse(iamge)
                    flap(binDir) # call the flap function
                    binStatus()
                    first_time=0
                    frame_buffer=0
                    counter=0
                    print("Waste segregated !")
                    continue
            #cv2.imshow("Threshold",thresholded)

            if frame_buffer%60==0:
                frame_buffer=0
                refImg=image
                #refImg=refImg[0:x,0:y-90]
                refThresh=imageSubtract(refImg)
                os.system("clear")
                print("Refrence Image changed")

            if key == ord('q'):
                stop_flag.value=1
                camera.close()
                cv2.destroyAllWindows()
                break

        except Exception as e:
            print(e)
            pass

if __name__ == "__main__" :
    try:

        imageProcessing()
        print("Started the system !")
                       
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        GPIO.cleanup() 