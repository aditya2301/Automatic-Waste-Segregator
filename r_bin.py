import Rpi as GPIO
import time as sleep

r_bin=7

#run servo motor in bin
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


#r_bin lid position based on signal received
if signal==1
    SetPinAngle(r_bin,180)
elif signal==-1
    SetPinAngle(r_bin,0)
else
    SetPinAngle(r_bin,90)
