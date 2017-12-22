import RPi.GPIO as GPIO
from time import sleep

#pin for elbow=7,wrist=5,grip=3
elbow=7
wrist=5
grip=3

def SetPinAngle(pin,angle):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7,GPIO.OUT)
    pwm=GPIO.PWM(pin,50)
    duty=angle/18 + 2
    GPIO.output(7,True)
    pwm.ChangeDutyCycle(duty)
    sleep(2)
    GPIO.output(7,False)
    pwm.ChangeDutyCycle(0)


#move to starting position
SetPinAngle(elbow,70)
SetPinAngle(wrist,120)
SetPinAngle(grip,0)

#Pick the Object
SetPinAngle(elbow,10)
SetPinAngle(grip,40)
SetPinAngle(grip,0)

#Move towards Waste-Bin
SetPinAngle(elbow,70)
SetPinAngle(wrist,30)

#Drop the Object
SetPinAngle(grip,40)
SetPinAngle(grip,0)


pwm.stop()
GPIO.cleanup()
GPIO.setwarnings(False)



