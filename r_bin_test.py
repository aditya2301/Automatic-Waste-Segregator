import Rpi.GPIO as GPIO
import time as sleep

#signal is sent as input for this module:1=biodegradable;  0=relax position; -1=non-biodegradable

#r_bin servo motor pwm pin output
r_bin=7

#run servo motor in bin
def SetPinAngle(pin,angle):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin,GPIO.OUT)
    pwm=GPIO.PWM(pin,50)
    duty=angle/18 + 2
    GPIO.output(pin,True)
    pwm.ChangeDutyCycle(duty)
    sleep(2)
    GPIO.output(pin,False)
    pwm.ChangeDutyCycle(0)


#r_bin lid position based on signal received
if signal==1
    SetPinAngle(r_bin,180)
    sleep(1)
    SetPinAngle(r_bin,90)
elif signal==-1
    SetPinAngle(r_bin,0)
    sleep(1)
    SetPinAngle(r_bin,90)
else
    SetPinAngle(r_bin,90)


pwm.stop()
GPIO.cleanup()
GPIO.setwarnings(False)
